#!/usr/bin/python

import os
import posix
import socket
import select
import subprocess
import sys
import time

service_port = 12042

class FdPipe:
    """Connect two pairs of file objects"""
    def __init__(self, in0, out0, in1, out1):
        flags = select.POLLERR | select.POLLIN | select.POLLHUP
        self.poller = select.poll()
        self.fd_map = {
            out0.fileno(): in1.fileno(),
            out1.fileno(): in0.fileno()
        }

        for fd in self.fd_map:
            self.select_for_read(fd)

        self.out_buf = {}

    def select_for_flush(self, fd):
        self.poller.register(fd, select.POLLERR | select.POLLHUP | \
            select.POLLIN | select.POLLOUT)

    def select_for_write(self, fd):
        self.poller.register(fd, select.POLLERR | select.POLLHUP | \
            select.POLLIN | select.POLLOUT)

    def select_for_read(self, fd):
        self.poller.register(fd, select.POLLERR | select.POLLHUP | \
            select.POLLIN)

    def do_write(self, outfd):
        if not self.out_buf[outfd]:
            return

        (rl, wl, el) = select.select([], [outfd], [outfd])
        if outfd in wl:
            length = posix.write(outfd, self.out_buf[outfd])
            self.out_buf[outfd] = self.out_buf[outfd][length:]
            if not self.out_buf[outfd]:
                self.select_for_read(outfd)
                del self.out_buf[outfd]
        elif fd in el:
            raise Exception('could not flush fd')

    def queue_write(self, outfd, data):
        self.out_buf[outfd] = self.out_buf.setdefault(outfd, '') + data
        self.select_for_write(outfd)

    def flush_outputs(self):
        while self.out_buf:
            for outfd in self.out_buf:
                try:
                    self.do_write(outfd)
                except OSError, e:
                    return

    def one_loop(self):
        ret = True
        for (fd, ev) in self.poller.poll(1000):
            if ev & (select.POLLERR | select.POLLHUP):
                self.flush_outputs()
                self.poller.unregister(fd)
                ret = False
            if ev & select.POLLIN:
                data = posix.read(fd, 4096)
                if not data:
                    posix.close(self.fd_map[fd])
                    ret = False
                self.queue_write(self.fd_map[fd], data)
            if ev & select.POLLOUT:
                self.do_write(fd)
        return ret

def scp(addr, user, local_path, remote_path, local_key=None):
    scp_call = ['scp', local_path, 
        '%s@[%s]:%s' % (user, addr, remote_path)
    ]

    if local_key:
        scp_call.insert(1, local_key)
        scp_call.insert(1, '-i')

    subprocess.call(scp_call)

def tcp4_to_unix(local_port, unix_path):
    server = socket.socket(socket.AF_INET,
        socket.SOCK_STREAM, socket.IPPROTO_TCP)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        server.bind(('127.0.0.1', local_port))
    except socket.error, e:
        sys.stderr.write('remote cant grab port %d\n' % service_port)
        # let other end time to connect to maintain ssh up
        time.sleep(10)
        sys.exit(0)
    server.listen(32)

    while True:
        (rl, wl, el) = select.select([server], [], [server], 1)
        if server in rl:
            (client, _) = server.accept()
            if not posix.fork():
                unix = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
                unix.connect(unix_path)
                pipe = FdPipe(client, client, unix, unix)
                while pipe.one_loop():
                    pass
                return
        try:
            posix.waitpid(-1, posix.WNOHANG)
        except OSError:
            pass

def _ssh_master_cmd(addr, user, command, local_key=None):
    """Exit or check ssh mux"""
    ssh_call = ['ssh', '-qNfL%d:127.0.0.1:%d' % (service_port, service_port),
        '-o', 'ControlPath=~/.ssh/unixpipe_%r@%h:%p',
        '-O', command,
        '%s@%s' % (user, addr,)
    ]

    if local_key:
        ssh_call.insert(1, local_key)
        ssh_call.insert(1, '-i')
    
    return subprocess.call(ssh_call)

def is_alive(addr, user):
    """Check whether a tunnel is alive"""
    return _ssh_master_cmd(addr, user, 'check') == 0

def setup(addr, user, remote_path, local_key=None):
    """Setup the tunnel"""
    if is_alive(addr, user):
        return

    scp(addr, user, __file__, '~/unixpipe', local_key)

    ssh_call = ['ssh', '-fL%d:127.0.0.1:%d' % (service_port, service_port),
        '-o', 'ExitOnForwardFailure=yes',
        '-o', 'ControlPath=~/.ssh/unixpipe_%r@%h:%p',
        '-o', 'ControlMaster=auto',
        '%s@%s' % (user, addr,), 'python', '~/unixpipe', 
            'server', remote_path]
    if local_key:
        ssh_call.insert(1, local_key)
        ssh_call.insert(1, '-i')
    
    subprocess.call(ssh_call)
    #XXX Sleep is a bad way to wait for the tunnel endpoint
    time.sleep(1)

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'server':
        tcp4_to_unix(service_port, sys.argv[2])

#!/usr/bin/python

import os
import socket
import select
import subprocess
import sys
import time


class FdPipe:

    """Connect two pairs of file objects"""

    def __init__(self, in0, out0, in1, out1):
        self.poller = select.poll()
        self.fd_map = {
            out0.fileno(): in1.fileno(),
            out1.fileno(): in0.fileno()
        }

        for fd in self.fd_map:
            self.select_for_read(fd)

        self.out_buf = {}

    def select_for_flush(self, fd):
        self.poller.register(fd, select.POLLERR | select.POLLHUP |
                             select.POLLIN | select.POLLOUT)

    def select_for_write(self, fd):
        self.poller.register(fd, select.POLLERR | select.POLLHUP |
                             select.POLLIN | select.POLLOUT)

    def select_for_read(self, fd):
        self.poller.register(fd, select.POLLERR | select.POLLHUP |
                             select.POLLIN)

    def do_write(self, outfd):
        if not self.out_buf[outfd]:
            return

        (rl, wl, el) = select.select([], [outfd], [outfd])
        if outfd in wl:
            length = os.write(outfd, self.out_buf[outfd])
            self.out_buf[outfd] = self.out_buf[outfd][length:]
            if not self.out_buf[outfd]:
                self.select_for_read(outfd)
                del self.out_buf[outfd]
        elif outfd in el:
            raise Exception('could not flush fd')

    def queue_write(self, outfd, data):
        self.out_buf[outfd] = self.out_buf.setdefault(outfd, '') + data
        self.select_for_write(outfd)

    def flush_outputs(self):
        while self.out_buf:
            for outfd in self.out_buf:
                try:
                    self.do_write(outfd)
                except OSError:
                    return

    def one_loop(self):
        ret = True
        for (fd, ev) in self.poller.poll(1000):
            if ev & (select.POLLERR | select.POLLHUP):
                self.flush_outputs()
                self.poller.unregister(fd)
                ret = False
            if ev & select.POLLIN:
                data = os.read(fd, 4096)
                if not data:
                    os.close(self.fd_map[fd])
                    ret = False
                self.queue_write(self.fd_map[fd], data)
            if ev & select.POLLOUT:
                self.do_write(fd)
        return ret


def scp(addr, user, local_path, remote_path, local_key=None):
    scp_call = ['scp', local_path,
                '%s@[%s]:%s' % (user, addr, remote_path)]

    if local_key:
        scp_call.insert(1, local_key)
        scp_call.insert(1, '-i')

    subprocess.call(scp_call)


def tcp4_to_unix(local_port, unix_path):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM,
                           socket.IPPROTO_TCP)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        server.bind(('127.0.0.1', local_port))
    except socket.error as e:
        sys.stderr.write('remote cant grab port %d\n' % local_port)
        # let other end time to connect to maintain ssh up
        time.sleep(10)
        sys.exit(0)
    server.listen(32)

    while True:
        (rl, wl, el) = select.select([server], [], [server], 1)
        if server in rl:
            (client, _) = server.accept()
            if not os.fork():
                unix = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
                try:
                    unix.connect(unix_path)
                except socket.error as e:
                    print('Unable to grab %s: %s' % (unix_path, e))
                pipe = FdPipe(client, client, unix, unix)
                while pipe.one_loop():
                    pass
                return
            client.close()
        try:
            os.waitpid(-1, os.WNOHANG)
        except OSError:
            pass


def find_port(addr, user):
    """Find local port in existing tunnels"""
    import pwd
    home = pwd.getpwuid(os.getuid()).pw_dir
    for name in os.listdir('%s/.ssh/' % home):
        if name.startswith('unixpipe_%s@%s_' % (user, addr,)):
            return int(name.split('_')[2])


def new_port():
    """Find a free local port and allocate it"""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
    for i in range(12042, 16042):
        try:
            s.bind(('127.0.0.1', i))
            s.close()
            return i
        except socket.error:
            pass
    raise Exception('No local port available')


def _ssh_master_cmd(addr, user, command, local_key=None):
    """Exit or check ssh mux"""
    ssh_call = ['ssh', '-qNfL%d:127.0.0.1:12042' % find_port(addr, user),
                '-o', 'ControlPath=~/.ssh/unixpipe_%%r@%%h_%d' %
                       find_port(addr, user),
                '-O', command, '%s@%s' % (user, addr,)]

    if local_key:
        ssh_call.insert(1, local_key)
        ssh_call.insert(1, '-i')

    return subprocess.call(ssh_call)


def is_alive(addr, user):
    """Check wether a tunnel is alive"""
    return _ssh_master_cmd(addr, user, 'check') == 0


def setup(addr, user, remote_path, local_key=None):
    """Setup the tunnel"""
    port = find_port(addr, user)

    if not port or not is_alive(addr, user):
        port = new_port()

        scp(addr, user, __file__, '~/unixpipe', local_key)

        ssh_call = ['ssh', '-fL%d:127.0.0.1:12042' % port,
                    '-o', 'ExitOnForwardFailure=yes',
                    '-o', 'ControlPath=~/.ssh/unixpipe_%%r@%%h_%d' % port,
                    '-o', 'ControlMaster=auto',
                    '%s@%s' % (user, addr,), 'python', '~/unixpipe',
                    'server', remote_path]
        if local_key:
            ssh_call.insert(1, local_key)
            ssh_call.insert(1, '-i')

        subprocess.call(ssh_call)
        # XXX Sleep is a bad way to wait for the tunnel endpoint
        time.sleep(1)

    return port

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'server':
        tcp4_to_unix(12042, sys.argv[2])

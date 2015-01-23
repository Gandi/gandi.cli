try:
    from xmlrpc.client import DateTime
except ImportError:
    from xmlrpclib import DateTime


def datacenter_list(options):
    return [{'iso': 'FR',
             'name': 'Equinix Paris',
             'id': 1,
             'country': 'France'},
            {'iso': 'US',
             'name': 'Level3 Baltimore',
             'id': 2,
             'country': 'United States of America'},
            {'iso': 'LU',
             'name': 'Bissen',
             'id': 3,
             'country': 'Luxembourg'}]


def disk_list(options):
    disks = [{'can_snapshot': True,
              'type': 'data',
              'size': 10240,
              'label': None,
              'snapshot_profile_id': None,
              'date_created': DateTime('20120521T22:20:57'),
              'id': 4126,
              'name': 'data',
              'is_boot_disk': False,
              'datacenter_id': 1,
              'source': None,
              'vms_id': [80458],
              'state': 'created',
              'date_updated': DateTime('20140728T10:52:45'),
              'visibility': 'private',
              'kernel_version': None,
              'total_size': 10240,
              'snapshots_id': []},
             {'can_snapshot': True,
              'type': 'data',
              'size': 10240,
              'label': 'ArchLinux 64 bits',
              'snapshot_profile_id': None,
              'date_created': DateTime('20130601T10:33:53'),
              'id': 4204,
              'name': 'arch64',
              'is_boot_disk': True,
              'datacenter_id': 1,
              'source': 136529,
              'vms_id': [80458],
              'state': 'created',
              'date_updated': DateTime('20140728T10:52:45'),
              'visibility': 'private',
              'kernel_version': '3.2-x86_64',
              'total_size': 6240,
              'snapshots_id': []},
             {'visibility': 'private',
              'size': 3072,
              'kernel_version': '3.12-x86_64 (hvm)',
              'name': 'sys_docker',
              'datacenter_id': 3,
              'label': 'Ubuntu 14.04 64 bits LTS (HVM)',
              'id': 9184,
              'date_updated': DateTime('20150103T15:27:22'),
              'vms_id': [128620],
              'source': 3316160,
              'total_size': 3072,
              'snapshots_id': [],
              'type': 'data',
              'is_boot_disk': True,
              'state': 'created',
              'date_created': DateTime('20150103T15:26:52'),
              'snapshot_profile_id': None,
              'can_snapshot': True}
            ]

    if 'name' in options:
        disks = dict([(disk['name'], disk) for disk in disks])
        return [disks[options['name']]]

    return disks


def disk_info(id):
    disks = disk_list({})
    disks = dict([(disk['id'], disk) for disk in disks])
    return disks[id]


def vm_list(options):

    return [{'cores': 1,
             'hostname': 'arch64',
             'datacenter_id': 1,
             'state': 'running',
             'id': 80458,
             'ifaces_id': [65087],
             'description': None,
             'date_updated': DateTime('20141008T16:13:59'),
             'memory': 512,
             'console': 0,
             'disks_id': [4204, 4126],
             'date_created': DateTime('20130601T10:33:53'),
             'flex_shares': 0,
             'ai_active': 0,
             'vm_max_memory': 2048},
            {'cores': 1,
             'hostname': 'docker',
             'datacenter_id': 3,
             'state': 'running',
             'id': 128620,
             'ifaces_id': [126368],
             'description': None,
             'date_updated': DateTime('20150103T15:27:57'),
             'memory': 256,
             'console': 0,
             'disks_id': [9184],
             'date_created': DateTime('20150103T15:26:52'),
             'flex_shares': 0,
             'ai_active': 0,
             'vm_max_memory': 2048}]


def vm_disk_detach(vm_id, disk_id):
    if vm_id == 80458 and disk_id == 4126:
        return {'id': 200,
                'step': 'WAIT'}


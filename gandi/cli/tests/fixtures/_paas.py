try:
    # python3
    from xmlrpc.client import DateTime
except ImportError:
    # python2
    from xmlrpclib import DateTime


def snapshotprofile_list(options):
    ret = [{'id': 7,
            'kept_total': 3,
            'name': 'paas_normal',
            'quota_factor': 1.3,
            'schedules': [{'kept_version': 1, 'name': 'daily'},
                          {'kept_version': 1, 'name': 'weekly'},
                          {'kept_version': 1, 'name': 'weekly4'}]}]

    for fkey in options:
        ret = [snp for snp in ret if snp[fkey] == options[fkey]]

    return ret


def list(options):

    ret = [{'catalog_name': 'phpmysql_s',
            'console': '1656411@console.dc0.gpaas.net',
            'data_disk_additional_size': 0,
            'datacenter_id': 1,
            'date_end': DateTime('20160408T00:00:00'),
            'date_end_commitment': None,
            'date_start': DateTime('20130903T22:14:13'),
            'id': 126276,
            'name': 'paas_owncloud',
            'need_upgrade': False,
            'servers': [{'id': 126273}],
            'size': 's',
            'snapshot_profile': None,
            'state': 'halted',
            'type': 'phpmysql'},
           {'catalog_name': 'nodejsmongodb_s',
            'console': '185290@console.dc2.gpaas.net',
            'data_disk_additional_size': 0,
            'datacenter_id': 3,
            'date_end': DateTime('20161125T15:52:56'),
            'date_end_commitment': DateTime('20151118T18:00:00'),
            'date_start': DateTime('20141025T15:52:56'),
            'id': 163744,
            'name': 'paas_cozycloud',
            'need_upgrade': False,
            'servers': [{'id': 163728}],
            'size': 's',
            'snapshot_profile': None,
            'state': 'running',
            'type': 'nodejsmongodb'}]

    options.pop('items_per_page', None)

    for fkey in options:
        ret = [paas for paas in ret if paas[fkey] == options[fkey]]

    return ret


def info(paas_id):

    ret = [{'autorenew': None,
            'catalog_name': 'nodejsmongodb_s',
            'console': '185290@console.dc2.gpaas.net',
            'data_disk_additional_size': 0,
            'datacenter': {'country': 'Luxembourg',
                           'dc_code': 'LU-BI1',
                           'id': 3,
                           'iso': 'LU',
                           'name': 'Bissen'},
            'datadisk_total_size': 10.0,
            'date_end': DateTime('20161125T15:52:56'),
            'date_end_commitment': DateTime('20151118T00:00:00'),
            'date_start': DateTime('20141025T15:52:56'),
            'ftp_server': 'sftp.dc2.gpaas.net',
            'git_server': 'git.dc2.gpaas.net',
            'id': 163744,
            'name': 'paas_cozycloud',
            'need_upgrade': False,
            'owner': {'handle': 'PXP561-GANDI', 'id': 2920674},
            'servers': [{'graph_urls': {'vcpu': [''], 'vdi': [''],
                                        'vif': ['']},
                         'id': 163728,
                         'uuid': 19254}],
            'size': 's',
            'snapshot_profile': None,
            'state': 'running',
            'type': 'nodejsmongodb',
            'user': 185290,
            'vhosts': [{'date_creation': DateTime('20141025T15:50:54'),
                        'id': 1177216,
                        'name': '187832c2b34.testurl.ws',
                        'state': 'running'},
                       {'date_creation': DateTime('20141025T15:50:54'),
                        'id': 1177220,
                        'name': 'cloud.iheartcli.com',
                        'state': 'running'},
                       {'date_creation': DateTime('20150728T17:50:56'),
                        'id': 1365951,
                        'name': 'cli.sexy',
                        'state': 'running'}]},
           {'autorenew': None,
            'catalog_name': 'phpmysql_s',
            'console': '1656411@console.dc0.gpaas.net',
            'data_disk_additional_size': 0,
            'datacenter': {'country': 'France',
                           'dc_code': 'FR-SD2',
                           'id': 1,
                           'iso': 'FR',
                           'name': 'Equinix Paris'},
            'datadisk_total_size': 10.0,
            'date_end': DateTime('20160408T00:00:00'),
            'date_end_commitment': None,
            'date_start': DateTime('20130903T22:14:13'),
            'ftp_server': 'sftp.dc0.gpaas.net',
            'git_server': 'git.dc0.gpaas.net',
            'id': 126276,
            'name': 'sap',
            'need_upgrade': False,
            'owner': {'handle': 'PXP561-GANDI', 'id': 2920674},
            'servers': [{'graph_urls': {'vcpu': [''], 'vdi': [''],
                                        'vif': ['']},
                         'id': 126273,
                         'uuid': 195339}],
            'size': 's',
            'snapshot_profile': None,
            'state': 'halted',
            'type': 'phpmysql',
            'user': 1656411,
            'vhosts': [{'date_creation': DateTime('20130903T22:11:54'),
                        'id': 160126,
                        'name': 'aa3e0e26f8.url-de-test.ws',
                        'state': 'running'},
                       {'date_creation': DateTime('20130903T22:24:06'),
                        'id': 160127,
                        'name': 'cloud.cat.lol',
                        'state': 'running'}]},
           {'autorenew': None,
            'catalog_name': 'pythonpgsql_s',
            'console': '1185290@console.dc2.gpaas.net',
            'data_disk_additional_size': 0,
            'datacenter': {'country': 'Luxembourg',
                           'dc_code': 'LU-BI1',
                           'id': 3,
                           'iso': 'LU',
                           'name': 'Bissen'},
            'datadisk_total_size': 10.0,
            'date_end': DateTime('20161125T15:52:56'),
            'date_end_commitment': DateTime('20151118T00:00:00'),
            'date_start': DateTime('20141025T15:52:56'),
            'ftp_server': 'sftp.dc2.gpaas.net',
            'git_server': 'git.dc2.gpaas.net',
            'id': 123456,
            'name': '123456',
            'need_upgrade': False,
            'owner': {'handle': 'PXP561-GANDI', 'id': 2920674},
            'servers': [{'graph_urls': {'vcpu': [''], 'vdi': [''],
                                        'vif': ['']},
                         'id': 1123456,
                         'uuid': 119254}],
            'size': 's',
            'snapshot_profile': None,
            'state': 'running',
            'type': 'pythonpgsql',
            'user': 1185290,
            'vhosts': [{'date_creation': DateTime('20141025T15:50:54'),
                        'id': 2177216,
                        'name': '987832c2b34.testurl.ws',
                        'state': 'running'}]}]

    instances = dict([(paas['id'], paas) for paas in ret])
    return instances[paas_id]


def vhost_list(options):

    ret = [{'cert_id': None,
            'date_creation': DateTime('20130903T22:11:54'),
            'id': 160126,
            'name': 'aa3e0e26f8.url-de-test.ws',
            'paas_id': 126276,
            'state': 'running'},
           {'cert_id': None,
            'date_creation': DateTime('20130903T22:24:06'),
            'id': 160127,
            'name': 'cloud.cat.lol',
            'paas_id': 126276,
            'state': 'running'},
           {'cert_id': None,
            'date_creation': DateTime('20141025T15:50:54'),
            'id': 1177216,
            'name': '187832c2b34.testurl.ws',
            'paas_id': 163744,
            'state': 'running'},
           {'cert_id': None,
            'date_creation': DateTime('20141025T15:50:54'),
            'id': 1177220,
            'name': 'cloud.iheartcli.com',
            'paas_id': 163744,
            'state': 'running'},
           {'cert_id': None,
            'date_creation': DateTime('20150728T17:50:56'),
            'id': 1365951,
            'name': 'cli.sexy',
            'paas_id': 163744,
            'state': 'running'}]

    options.pop('items_per_page', None)

    for fkey in options:
        ret = [paas for paas in ret if paas[fkey] == options[fkey]]

    return ret


def vhost_info(name):
    vhosts = vhost_list({})
    vhosts = dict([(vhost['name'], vhost) for vhost in vhosts])
    return vhosts[name]


def vhost_delete(name):
    return {'id': 200, 'step': 'WAIT', 'name': 'rproxy_update',
            'paas_id': 1177220,
            'date_creation': DateTime('20150728T17:50:56')}


def type_list(options):

    ret = [{'database': 'MySQL',
            'language': 'PHP',
            'name': 'phpmysql'},
           {'database': 'PostgreSQL',
            'language': 'PHP',
            'name': 'phppgsql'},
           {'database': 'PostgreSQL',
            'language': 'Node.js',
            'name': 'nodejspgsql'},
           {'database': 'MongoDB',
            'language': 'Node.js',
            'name': 'nodejsmongodb'},
           {'database': 'MySQL',
            'language': 'Node.js',
            'name': 'nodejsmysql'},
           {'database': 'MongoDB',
            'language': 'PHP',
            'name': 'phpmongodb'},
           {'database': 'MySQL',
            'language': 'Python',
            'name': 'pythonmysql'},
           {'database': 'PostgreSQL',
            'language': 'Python',
            'name': 'pythonpgsql'},
           {'database': 'MongoDB',
            'language': 'Python',
            'name': 'pythonmongodb'},
           {'database': 'MySQL',
            'language': 'Ruby',
            'name': 'rubymysql'},
           {'database': 'PostgreSQL',
            'language': 'Ruby',
            'name': 'rubypgsql'},
           {'database': 'MongoDB',
            'language': 'Ruby',
            'name': 'rubymongodb'}]

    return ret


def update(paas_id, options):
    return {'id': 200, 'step': 'WAIT'}


def vhost_create(options):
    return {'id': 200, 'step': 'WAIT'}


def delete(paas_id):
    return {'id': 200, 'step': 'WAIT'}


def create(options):
    return {'id': 200, 'step': 'WAIT'}


def restart(options):
    return {'id': 200, 'step': 'WAIT'}


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

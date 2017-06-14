# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re

from ..compat import mock
from .base import CommandTestCase
from gandi.cli.commands import paas
from gandi.cli.core.base import GandiContextHelper


class PaasTestCase(CommandTestCase):

    def test_list(self):
        result = self.invoke_with_exceptions(paas.list, [])

        self.assertEqual(result.output, """\
name       : paas_owncloud
state      : halted
vhost      : aa3e0e26f8.url-de-test.ws
vhost      : cloud.cat.lol
----------
name       : paas_cozycloud
state      : running
vhost      : 187832c2b34.testurl.ws
vhost      : cloud.iheartcli.com
vhost      : cli.sexy
""")

        self.assertEqual(result.exit_code, 0)

    def test_list_id(self):
        result = self.invoke_with_exceptions(paas.list, ['--id'])

        self.assertEqual(result.output, """\
name       : paas_owncloud
state      : halted
id         : 126276
vhost      : aa3e0e26f8.url-de-test.ws
vhost      : cloud.cat.lol
----------
name       : paas_cozycloud
state      : running
id         : 163744
vhost      : 187832c2b34.testurl.ws
vhost      : cloud.iheartcli.com
vhost      : cli.sexy
""")

        self.assertEqual(result.exit_code, 0)

    def test_list_type(self):
        result = self.invoke_with_exceptions(paas.list, ['--type'])

        self.assertEqual(result.output, """\
name       : paas_owncloud
state      : halted
type       : phpmysql
vhost      : aa3e0e26f8.url-de-test.ws
vhost      : cloud.cat.lol
----------
name       : paas_cozycloud
state      : running
type       : nodejsmongodb
vhost      : 187832c2b34.testurl.ws
vhost      : cloud.iheartcli.com
vhost      : cli.sexy
""")

        self.assertEqual(result.exit_code, 0)

    def test_list_filter_state(self):
        result = self.invoke_with_exceptions(paas.list, ['--state', 'halted'])

        self.assertEqual(result.output, """\
name       : paas_owncloud
state      : halted
vhost      : aa3e0e26f8.url-de-test.ws
vhost      : cloud.cat.lol
""")

        self.assertEqual(result.exit_code, 0)

    def test_info(self):
        result = self.invoke_with_exceptions(paas.info, ['paas_cozycloud'])

        self.assertEqual(result.output, """\
name       : paas_cozycloud
type       : nodejsmongodb
size       : s
console    : 185290@console.dc2.gpaas.net
git_server : git.dc2.gpaas.net
sftp_server: sftp.dc2.gpaas.net
vhost      : 187832c2b34.testurl.ws
vhost      : cloud.iheartcli.com
vhost      : cli.sexy
datacenter : LU-BI1
quota used : 0.5%
snapshot   :
""")

        self.assertEqual(result.exit_code, 0)

    def test_info_stat(self):
        args = ['paas_cozycloud', '--stat']
        result = self.invoke_with_exceptions(paas.info, args)

        self.assertEqual(result.output, """\
name       : paas_cozycloud
type       : nodejsmongodb
size       : s
console    : 185290@console.dc2.gpaas.net
git_server : git.dc2.gpaas.net
sftp_server: sftp.dc2.gpaas.net
vhost      : 187832c2b34.testurl.ws
vhost      : cloud.iheartcli.com
vhost      : cli.sexy
datacenter : LU-BI1
quota used : 0.5%
snapshot   :
cache      :
\thit  : 0.0%
\tmiss : 100.0%
\tnot  : 0.0%
\tpass : 0.0%
""")

        self.assertEqual(result.exit_code, 0)

    def test_types(self):
        result = self.invoke_with_exceptions(paas.types, [])

        self.assertEqual(result.output, """\
phpmysql
phppgsql
nodejspgsql
nodejsmongodb
nodejsmysql
phpmongodb
pythonmysql
pythonpgsql
pythonmongodb
rubymysql
rubypgsql
rubymongodb
""")

        self.assertEqual(result.exit_code, 0)

    def test_console(self):
        result = self.invoke_with_exceptions(paas.console, ['paas_cozycloud'])

        self.assertEqual(re.sub(r'\[#+\]', '[###]',
                                result.output.strip()), """\
/!\ Use ~. ssh escape key to exit.
Activation of the console on your PaaS instance
\rProgress: [###] 100.00%  00:00:00  \n\
ssh 185290@console.dc2.gpaas.net""")

        self.assertEqual(result.exit_code, 0)

    def test_clone_missing(self):
        result = self.invoke_with_exceptions(paas.clone, [])

        self.assertEqual(result.output, """\
Usage: paas clone [OPTIONS] NAME

Error: Missing argument "name".
""")

        self.assertEqual(result.exit_code, 2)

    def test_clone(self):
        with mock.patch('gandi.cli.modules.vhost.os.chdir',
                        create=True) as mock_chdir:
            mock_chdir.return_value = mock.MagicMock()

            result = self.invoke_with_exceptions(paas.clone, ['cli.sexy'])

        self.assertEqual(result.output, """\
git clone ssh+git://185290@git.dc2.gpaas.net/default.git cli.sexy \
--origin gandi
Use `git push gandi master` to push your code to the instance.
Then `$ gandi deploy` to build and deploy your application.
""")

        self.assertEqual(result.exit_code, 0)

    def test_clone_directory(self):
        with mock.patch('gandi.cli.modules.vhost.os.chdir',
                        create=True) as mock_chdir:
            mock_chdir.return_value = mock.MagicMock()

            args = ['cli.sexy', '--directory', 'project']
            result = self.invoke_with_exceptions(paas.clone, args)

        self.assertEqual(result.output, """\
git clone ssh+git://185290@git.dc2.gpaas.net/default.git project --origin gandi
Use `git push gandi master` to push your code to the instance.
Then `$ gandi deploy` to build and deploy your application.
""")

        self.assertEqual(result.exit_code, 0)

    def test_clone_vhost(self):
        with mock.patch('gandi.cli.modules.vhost.os.chdir',
                        create=True) as mock_chdir:
            mock_chdir.return_value = mock.MagicMock()

            args = ['paas_cozycloud', '--vhost', 'cli.sexy']
            result = self.invoke_with_exceptions(paas.clone, args)

        self.assertEqual(result.output, """\
git clone ssh+git://185290@git.dc2.gpaas.net/cli.sexy.git cli.sexy \
--origin gandi
Use `git push gandi master` to push your code to the instance.
Then `$ gandi deploy` to build and deploy your application.
""")

        self.assertEqual(result.exit_code, 0)

    def test_attach(self):
        result = self.invoke_with_exceptions(paas.attach, ['paas_cozycloud'])

        self.assertEqual(result.output, """\
git remote add gandi ssh+git://185290@git.dc2.gpaas.net/default.git
Added remote `gandi` to your local git repository.
Use `git push gandi master` to push your code to the instance.
Then `$ gandi deploy` to build and deploy your application.
""")

        self.assertEqual(result.exit_code, 0)

    def test_attach_remote(self):
        args = ['paas_cozycloud', '--remote', 'production']
        result = self.invoke_with_exceptions(paas.attach, args)

        self.assertEqual(result.output, """\
git remote add production ssh+git://185290@git.dc2.gpaas.net/default.git
Added remote `production` to your local git repository.
Use `git push production master` to push your code to the instance.
Then `$ gandi deploy` to build and deploy your application.
""")

        self.assertEqual(result.exit_code, 0)

    def test_deploy_invalid_remote_empty(self):
        args = []

        git_content = """
[blabla]
dummy=dududududud
"""
        result = self.isolated_invoke_with_exceptions(paas.deploy, args,
                                                      temp_dir='.git',
                                                      temp_name='config',
                                                      temp_content=git_content)

        self.assertEqual(result.output, """\
Error: Could not find git remote to extract deploy url from.
This usually happens when:
- the current directory has no Simple Hosting git remote attached,
  in this case, please see $ gandi paas attach --help
- the local branch being deployed hasn't been pushed \
to the remote repository yet,
  in this case, please try $ git push <remote> master

Otherwise, it's recommended to use the --remote and/or --branch options:
$ gandi deploy --remote <remote> [--branch <branch>]
""")

        self.assertEqual(result.exit_code, 2)

    def test_deploy_invalid_remote_content(self):
        args = []

        git_content = """
[remote "origin"]
        fetch = +refs/heads/*:refs/remotes/origin/*
        url = https://github.com/Gandi/gandi.cli.git
[branch "master"]
        remote = origin
        merge = refs/heads/master
"""
        result = self.isolated_invoke_with_exceptions(paas.deploy, args,
                                                      temp_dir='.git',
                                                      temp_name='config',
                                                      temp_content=git_content)

        self.assertEqual(result.output, """\
Error: https://github.com/Gandi/gandi.cli.git \
is not a valid Simple Hosting git remote.
This usually happens when:
- the current directory has no Simple Hosting git remote attached,
  in this case, please see $ gandi paas attach --help
- the local branch being deployed hasn't been pushed \
to the remote repository yet,
  in this case, please try $ git push <remote> master

Otherwise, it's recommended to use the --remote and/or --branch options:
$ gandi deploy --remote <remote> [--branch <branch>]
""")

        self.assertEqual(result.exit_code, 2)

    def test_deploy(self):
        args = []

        git_content = """
[remote "gandi"]
        fetch = +refs/heads/*:refs/remotes/gandi/*
        url = ssh+git://185290@git.dc2.gpaas.net/default.git
"""
        result = self.isolated_invoke_with_exceptions(paas.deploy, args,
                                                      temp_dir='.git',
                                                      temp_name='config',
                                                      temp_content=git_content)

        self.assertEqual(result.output, """\
ssh 185290@git.dc2.gpaas.net 'deploy default.git master'
""")

        self.assertEqual(result.exit_code, 0)

    def test_deploy_remote(self):
        args = ['--remote', 'origin']

        git_content = """
[remote "origin"]
        fetch = +refs/heads/*:refs/remotes/origin/*
        url = ssh+git://185290@git.dc2.gpaas.net/default.git
[branch "master"]
        remote = origin
        merge = refs/heads/master
"""
        result = self.isolated_invoke_with_exceptions(paas.deploy, args,
                                                      temp_dir='.git',
                                                      temp_name='config',
                                                      temp_content=git_content)

        self.assertEqual(result.output, """\
ssh 185290@git.dc2.gpaas.net 'deploy default.git master'
""")

        self.assertEqual(result.exit_code, 0)

    def test_deploy_guess_remote_with_branch(self):
        args = ['--branch', 'stable']

        git_content = """
[remote "origin"]
        fetch = +refs/heads/*:refs/remotes/origin/*
        url = https://github.com/Gandi/gandi.cli.git
[remote "production"]
        fetch = +refs/heads/*:refs/remotes/production/*
        url = ssh+git://185290@git.dc2.gpaas.net/default.git
[branch "master"]
        remote = origin
        merge = refs/heads/master
[branch "stable"]
        remote = production
        merge = refs/heads/stable
"""
        result = self.isolated_invoke_with_exceptions(paas.deploy, args,
                                                      temp_dir='.git',
                                                      temp_name='config',
                                                      temp_content=git_content)

        self.assertEqual(result.output, """\
ssh 185290@git.dc2.gpaas.net 'deploy default.git stable'
""")

        self.assertEqual(result.exit_code, 0)

    def test_delete_unknown(self):
        result = self.invoke_with_exceptions(paas.delete, ['unknown_paas'])

        self.assertEqual(result.output, """\
Sorry PaaS instance unknown_paas does not exist
Please use one of the following: ['paas_owncloud', 'paas_cozycloud', \
'126276', '163744', 'aa3e0e26f8.url-de-test.ws', 'cloud.cat.lol', \
'187832c2b34.testurl.ws', 'cloud.iheartcli.com', 'cli.sexy']
""")

        self.assertEqual(result.exit_code, 0)

    def test_delete(self):
        result = self.invoke_with_exceptions(paas.delete, ['paas_owncloud'])
        self.assertEqual(result.output.strip(), """\
Are you sure to delete PaaS instance 'paas_owncloud'? [y/N]:""")
        self.assertEqual(result.exit_code, 0)

    def test_delete_ko(self):
        args = ['paas_owncloud']
        result = self.invoke_with_exceptions(paas.delete, args, input='N\n')
        self.assertEqual(re.sub(r'\[#+\]', '[###]',
                                result.output.strip()), """\
Are you sure to delete PaaS instance 'paas_owncloud'? [y/N]: N\
""")
        self.assertEqual(result.exit_code, 0)

    def test_delete_ok(self):
        args = ['paas_owncloud']
        result = self.invoke_with_exceptions(paas.delete, args, input='y\n')
        self.assertEqual(re.sub(r'\[#+\]', '[###]',
                                result.output.strip()), """\
Are you sure to delete PaaS instance 'paas_owncloud'? [y/N]: y
Deleting your PaaS instance.
\rProgress: [###] 100.00%  00:00:00""")
        self.assertEqual(result.exit_code, 0)

    def test_delete_background(self):
        args = ['paas_owncloud', '--force', '--background']
        result = self.invoke_with_exceptions(paas.delete, args)
        self.assertEqual(result.output, """\
id        : 200
step      : WAIT
""")
        self.assertEqual(result.exit_code, 0)

    def test_create_default(self):
        args = []
        result = self.invoke_with_exceptions(paas.create, args,
                                             obj=GandiContextHelper(),
                                             input='ploki\nploki\n')

        output = re.sub(r'\[#+\]', '[###]', result.output.strip())

        self.assertEqual(re.sub(r'paas\d+', 'paas', output), """\
password: \nRepeat for confirmation: \n\
Creating your PaaS instance.
\rProgress: [###] 100.00%  00:00:00  \n\
Your PaaS instance paas has been created.""")

        self.assertEqual(result.exit_code, 0)
        params = self.api_calls['paas.create'][0][0]
        self.assertEqual(params['datacenter_id'], 3)
        self.assertEqual(params['size'], 's')
        self.assertEqual(params['duration'], '1m')
        self.assertEqual(params['password'], 'ploki')
        self.assertTrue(params['name'].startswith('paas'))

    def test_create_name(self):
        args = ['--name', '123456']
        result = self.invoke_with_exceptions(paas.create, args,
                                             obj=GandiContextHelper(),
                                             input='ploki\nploki\n')

        self.assertEqual(re.sub(r'\[#+\]', '[###]',
                                result.output.strip()), """\
password: \nRepeat for confirmation: \n\
Creating your PaaS instance.
\rProgress: [###] 100.00%  00:00:00  \n\
Your PaaS instance 123456 has been created.""")

        self.assertEqual(result.exit_code, 0)

    def test_create_name_vhost(self):
        self.maxDiff = None
        args = ['--name', '123456', '--vhosts', 'ploki.fr', '--ssl']
        with mock.patch('gandi.cli.modules.vhost.os.chdir',
                        create=True) as mock_chdir:
            mock_chdir.return_value = mock.MagicMock()

            result = self.invoke_with_exceptions(paas.create, args,
                                                 obj=GandiContextHelper(),
                                                 input='ploki\nploki\n')

        self.assertEqual(re.sub(r'\[#+\]', '[###]',
                                result.output.strip()), """\
password: \nRepeat for confirmation: \n\
There is no certificate for ploki.fr.
Create the certificate with (for exemple) :
$ gandi certificate create --cn ploki.fr --type std \n\
Or relaunch the current command with --poll-cert option
Creating your PaaS instance.
\rProgress: [###] 100.00%  00:00:00  \n\
Your PaaS instance 123456 has been created.
Creating a new vhost.
\rProgress: [###] 100.00%  00:00:00  \n\
Your vhost ploki.fr has been created.""")

        self.assertEqual(result.exit_code, 0)

    def test_create_name_vhost_ssl(self):
        self.maxDiff = None
        args = ['--name', '123456', '--vhosts', 'inter.net', '--ssl']
        with mock.patch('gandi.cli.modules.vhost.os.chdir',
                        create=True) as mock_chdir:
            mock_chdir.return_value = mock.MagicMock()

            result = self.invoke_with_exceptions(paas.create, args,
                                                 obj=GandiContextHelper(),
                                                 input='ploki\nploki\n')

        self.assertEqual(re.sub(r'\[#+\]', '[###]',
                                result.output.strip()), """\
password: \nRepeat for confirmation: \n\
Please give the private key for certificate id 706 (CN: inter.net)""")

        self.assertEqual(result.exit_code, 0)

    def test_create_datacenter_limited(self):
        args = ['--datacenter', 'FR-SD2']
        result = self.invoke_with_exceptions(paas.create, args,
                                             obj=GandiContextHelper(),
                                             input='ploki\nploki\n')

        output = re.sub(r'\[#+\]', '[###]', result.output.strip())

        self.assertEqual(re.sub(r'paas\d+', 'paas', output), """\
/!\ Datacenter FR-SD2 will be closed on 25/12/2017, please consider using \
another datacenter.
password: \nRepeat for confirmation: \n\
Creating your PaaS instance.
\rProgress: [###] 100.00%  00:00:00  \n\
Your PaaS instance paas has been created.""")

        self.assertEqual(result.exit_code, 0)
        params = self.api_calls['paas.create'][0][0]
        self.assertEqual(params['datacenter_id'], 1)
        self.assertEqual(params['size'], 's')
        self.assertEqual(params['duration'], '1m')
        self.assertEqual(params['password'], 'ploki')
        self.assertTrue(params['name'].startswith('paas'))

        self.assertEqual(result.exit_code, 0)

    def test_create_datacenter_closed(self):
        args = ['--datacenter', 'US-BA1']
        result = self.invoke_with_exceptions(paas.create, args,
                                             obj=GandiContextHelper(),
                                             input='ploki\nploki\n')

        output = re.sub(r'\[#+\]', '[###]', result.output.strip())

        self.assertEqual(re.sub(r'paas\d+', 'paas', output), """\
Error: /!\ Datacenter US-BA1 is closed, please choose another datacenter.""")

        self.assertEqual(result.exit_code, 1)

    def test_update(self):
        args = ['paas_owncloud']
        result = self.invoke_with_exceptions(paas.update, args)

        self.assertEqual(re.sub(r'\[#+\]', '[###]',
                                result.output.strip()), """\
Updating your PaaS instance.
\rProgress: [###] 100.00%  00:00:00""")

        self.assertEqual(result.exit_code, 0)

    def test_update_for_upgrade(self):
        args = ['paas_owncloud', '--upgrade']
        result = self.invoke_with_exceptions(paas.update, args)

        self.assertEqual(re.sub(r'\[#+\]', '[###]',
                                result.output.strip()), """\
Updating your PaaS instance.
\rProgress: [###] 100.00%  00:00:00""")

        self.assertEqual(result.exit_code, 0)
        params = self.api_calls['paas.update'][0][1]
        self.assertEqual(params['upgrade'], True)

    def test_update_snapshotprofile_conflict(self):
        args = ['paas_owncloud', '--delete-snapshotprofile',
                '--snapshotprofile', '7']
        result = self.invoke_with_exceptions(paas.update, args)
        self.assertEqual(result.exit_code, 2)

    def test_update_password(self):
        args = ['paas_owncloud', '--password']
        result = self.invoke_with_exceptions(paas.update, args,
                                             obj=GandiContextHelper(),
                                             input='ploki\nploki\n')

        self.assertEqual(re.sub(r'\[#+\]', '[###]',
                                result.output.strip()), """\
password: \nRepeat for confirmation: \n\
Updating your PaaS instance.
\rProgress: [###] 100.00%  00:00:00""")

        self.assertEqual(result.exit_code, 0)

    def test_update_delete_snapshotprofile(self):
        args = ['paas_owncloud', '--delete-snapshotprofile']
        result = self.invoke_with_exceptions(paas.update, args)

        self.assertEqual(re.sub(r'\[#+\]', '[###]',
                                result.output.strip()), """\
Updating your PaaS instance.
\rProgress: [###] 100.00%  00:00:00""")

        self.assertEqual(result.exit_code, 0)
        params = self.api_calls['paas.update'][0][1]
        self.assertFalse('upgrade' in params)

    def test_update_background(self):
        args = ['paas_owncloud', '--bg']
        result = self.invoke_with_exceptions(paas.update, args)

        self.assertEqual(re.sub(r'\[#+\]', '[###]',
                                result.output.strip()), """\
{'id': 200, 'step': 'WAIT'}""")

        self.assertEqual(result.exit_code, 0)

    def test_restart_unknown(self):
        args = ['unknown_paas']
        result = self.invoke_with_exceptions(paas.restart, args)
        self.assertEqual(result.output, """\
Sorry PaaS instance unknown_paas does not exist
Please use one of the following: ['paas_owncloud', 'paas_cozycloud', \
'126276', '163744', 'aa3e0e26f8.url-de-test.ws', 'cloud.cat.lol', \
'187832c2b34.testurl.ws', 'cloud.iheartcli.com', 'cli.sexy']
""")

    def test_restart_prompt_ko(self):
        args = ['paas_owncloud']
        result = self.invoke_with_exceptions(paas.restart, args, input='N\n')
        self.assertEqual(re.sub(r'\[#+\]', '[###]',
                                result.output.strip()), """\
Are you sure to restart PaaS instance 'paas_owncloud'? [y/N]: N\
""")
        self.assertEqual(result.exit_code, 0)

    def test_restart(self):
        args = ['paas_owncloud', '--force']
        result = self.invoke_with_exceptions(paas.restart, args)
        self.assertEqual(re.sub(r'\[#+\]', '[###]',
                                result.output.strip()), """\
Restarting your PaaS instance.
\rProgress: [###] 100.00%  00:00:00""")
        self.assertEqual(result.exit_code, 0)

    def test_restart_background(self):
        args = ['paas_owncloud', '--force', '--bg']
        result = self.invoke_with_exceptions(paas.restart, args)
        self.assertEqual(re.sub(r'\[#+\]', '[###]',
                                result.output.strip()), """\
id        : 200
step      : WAIT""")
        self.assertEqual(result.exit_code, 0)

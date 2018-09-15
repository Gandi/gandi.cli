# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from ..core.utils.password import hash_password
from .compat import unittest, mock


class TestHashPwd(unittest.TestCase):

    @mock.patch('gandi.cli.core.utils.password.mkpassword')
    def test_hash_pwd(self, mkpassword):
        mkpassword.return_value = 'aSaltSting.12345'

        self.assertEqual(hash_password('.aPwd42!'),
                         '$6$aSaltSting.12345$'
                         'kQ0e3QAP5MxJA4un4xkGCK4OwMc5dX/xKubYypmasAb'
                         'U6ptnq5vyPi8IDfPm9zsKrUMKHhL056bD5rXsZqAt6.')

    def test_pwd_hashed(self):
        pwd = ('$6$aSaltSting.12345$'
               'kQ0e3QAP5MxJA4un4xkGCK4OwMc5dX/xKubYypmasAb'
               'U6ptnq5vyPi8IDfPm9zsKrUMKHhL056bD5rXsZqAt6.')

        self.assertEqual(hash_password(pwd), pwd)

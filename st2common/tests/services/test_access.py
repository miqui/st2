# Licensed to the StackStorm, Inc ('StackStorm') under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import datetime

from oslo.config import cfg
from st2tests.base import DbTestCase
from st2common.util import isotime
from st2common.exceptions.access import TokenNotFoundError
from st2common.persistence.access import Token
from st2common.services import access
import st2tests.config as tests_config


class AccessServiceTest(DbTestCase):

    @classmethod
    def setUpClass(cls):
        super(AccessServiceTest, cls).setUpClass()
        tests_config.parse_args()

    def test_create_token(self):
        token = access.create_token('manas')
        self.assertTrue(token is not None)
        self.assertTrue(token.token is not None)
        self.assertEqual(token.user, 'manas')

    def test_create_token_fail(self):
        try:
            access.create_token(None)
            self.assertTrue(False, 'Create succeeded was expected to fail.')
        except ValueError:
            self.assertTrue(True)

    def test_delete_token(self):
        token = access.create_token('manas')
        access.delete_token(token.token)
        try:
            token = Token.get(token.token)
            self.assertTrue(False, 'Delete failed was expected to pass.')
        except TokenNotFoundError:
            self.assertTrue(True)

    def test_create_token_ttl_ok(self):
        ttl = 10
        token = access.create_token('manas', 10)
        self.assertTrue(token is not None)
        self.assertTrue(token.token is not None)
        self.assertEqual(token.user, 'manas')
        expected_expiry = datetime.datetime.utcnow() + datetime.timedelta(seconds=ttl)
        expected_expiry = isotime.add_utc_tz(expected_expiry)
        self.assertLess(isotime.parse(token.expiry), expected_expiry)

    def test_create_token_ttl_capped(self):
        ttl = cfg.CONF.auth.token_ttl + 10
        expected_expiry = datetime.datetime.utcnow() + datetime.timedelta(seconds=ttl)
        expected_expiry = isotime.add_utc_tz(expected_expiry)
        token = access.create_token('manas', 10)
        self.assertTrue(token is not None)
        self.assertTrue(token.token is not None)
        self.assertEqual(token.user, 'manas')
        self.assertLess(isotime.parse(token.expiry), expected_expiry)

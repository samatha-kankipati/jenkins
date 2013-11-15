from datetime import datetime, timedelta
import re
from time import strptime, struct_time, mktime, gmtime, localtime

from testrepo.common.testfixtures.identity.v2_0.identity \
    import BaseIdentityFixture
from ccengine.common.decorators import attr
from ccengine.domain.identity.v2_0.response.access import Access
from dateutil.parser import parse


class AuthenticationTest(BaseIdentityFixture):
    @classmethod
    def setUpClass(cls):
        super(AuthenticationTest, cls).setUpClass()
        cls.datetime = datetime
        cls.default_token_length = 32

    @classmethod
    def tearDownClass(cls):
        pass

    @attr('regression', type='positive')
    def test_base_authentication_username_and_api_key(self):
        '''TODO:>>> offset needs to be unhardcoded'''
        auth_resp = self.public_client.authenticate_user_apikey(
            self.config.identity_api.username,
            self.config.identity_api.api_key)

        self.assertIsInstance(auth_resp.entity, Access)

        self.assertIsNotNone(
            auth_resp.entity.token.id,
            msg="Token is present returned %s".
            format(type(auth_resp.entity.token.id)))

        try:
            token_length = len(auth_resp.entity.token.id)
        except TypeError:
            token_length = 0

        self.assertEqual(
            token_length,
            self.default_token_length,
            msg='Default token length: {0} length of returned token {1}'.
            format(self.default_token_length, token_length))

        regex = re.compile('{0}{1}{2}{3}'.format(
            '^([a-zA-Z0-9]+-?)',
            '([a-zA-Z0-9]+-?)',
            '([a-zA-Z0-9]+-?)',
            '([a-zA-Z0-9]+-?)$'))

        self.assertIsNotNone(
            regex.match(auth_resp.entity.token.id),
            msg='Invalid token format')

        parsed_time = None
        try:
            parsed_time = parse(auth_resp.entity.token.expires)
            ptime = parsed_time.timetuple()
        except ValueError:
            pass

        self.assertIsInstance(
            ptime,
            struct_time,
            msg='Token expiration time stamp format is correct')

        current_time = self.datetime.now(parsed_time.tzinfo)

        delta = (parsed_time - current_time)

        self.assertGreaterEqual(
            delta,
            timedelta(days=0),
            msg='Token Expiration >= Current Time returned {0}'.
            format(delta >= timedelta(days=0)))

        self.assertLessEqual(
            delta, timedelta(days=1),
            msg='Token Expiration Delta <= 24hrs returned {0}'.
            format(delta <= timedelta(days=1)))

    @attr('regression', type='positive')
    def test_base_authentication_username_api_key_and_tenant_id(self):
        '''TODO:>>> offset needs to be unhardcoded'''
        auth_resp = self.public_client.authenticate_user_apikey_tenant_id(
            self.config.identity_api.username,
            self.config.identity_api.api_key,
            self.config.compute_api.tenant_id)

        self.assertIsInstance(auth_resp.entity, Access)

        self.assertIsNotNone(
            auth_resp.entity.token.id,
            msg="Token is present returned %s".
            format(type(auth_resp.entity.token.id)))

        try:
            token_length = len(auth_resp.entity.token.id)
        except TypeError:
            token_length = 0

        self.assertEqual(
            token_length,
            self.default_token_length,
            msg='Default token length: {0} length of returned token {1}'.
            format(self.default_token_length, token_length))

        regex = re.compile('{0}{1}{2}{3}'.format(
            '^([a-zA-Z0-9]+-?)',
            '([a-zA-Z0-9]+-?)',
            '([a-zA-Z0-9]+-?)',
            '([a-zA-Z0-9]+-?)$'))

        self.assertIsNotNone(
            regex.match(auth_resp.entity.token.id),
            msg='Invalid token format')

        parsed_time = None
        try:
            parsed_time = parse(auth_resp.entity.token.expires)
            ptime = parsed_time.timetuple()
        except ValueError:
            pass

        self.assertIsInstance(
            ptime,
            struct_time,
            msg='Token expiration time stamp format is correct')

        current_time = self.datetime.now(parsed_time.tzinfo)

        delta = (parsed_time - current_time)

        self.assertGreaterEqual(
            delta,
            timedelta(days=0),
            msg='Token Expiration >= Current Time returned {0}'.
            format(delta >= timedelta(days=0)))

        self.assertLessEqual(
            delta, timedelta(days=1),
            msg='Token Expiration Delta <= 24hrs returned {0}'.
            format(delta <= timedelta(days=1)))

    @attr('regression', type='positive')
    def test_base_authentication_username_and_password(self):
        '''TODO:>>> offset needs to be unhardcoded'''
        auth_resp = self.public_client.authenticate_user_password(
            self.config.identity_api.username,
            self.config.identity_api.password)

        self.assertIsInstance(auth_resp.entity, Access)

        self.assertIsNotNone(
            auth_resp.entity.token.id,
            msg="Token is present returned %s".
            format(type(auth_resp.entity.token.id)))

        try:
            token_length = len(auth_resp.entity.token.id)
        except TypeError:
            token_length = 0

        self.assertEqual(
            token_length,
            self.default_token_length,
            msg='Default token length: {0} length of returned token {1}'.
            format(self.default_token_length, token_length))

        regex = re.compile('{0}{1}{2}{3}'.format(
            '^([a-zA-Z0-9]+-?)',
            '([a-zA-Z0-9]+-?)',
            '([a-zA-Z0-9]+-?)',
            '([a-zA-Z0-9]+-?)$'))

        self.assertIsNotNone(
            regex.match(auth_resp.entity.token.id),
            msg='Invalid token format')

        parsed_time = None
        try:
            parsed_time = parse(auth_resp.entity.token.expires)
            ptime = parsed_time.timetuple()
        except ValueError:
            pass

        self.assertIsInstance(
            ptime,
            struct_time,
            msg='Token expiration time stamp format is correct')

        current_time = self.datetime.now(parsed_time.tzinfo)

        delta = (parsed_time - current_time)

        self.assertGreaterEqual(
            delta,
            timedelta(days=0),
            msg='Token Expiration >= Current Time returned {0}'.
            format(delta >= timedelta(days=0)))

        self.assertLessEqual(
            delta, timedelta(days=1),
            msg='Token Expiration Delta <= 24hrs returned {0}'.
            format(delta <= timedelta(days=1)))

    @attr('regression', type='positive')
    def test_base_authentication_username_password_and_tenant_id(self):
        '''TODO:>>> offset needs to be unhardcoded'''
        auth_resp = self.public_client.authenticate_user_password_tenant_id(
            self.config.identity_api.username,
            self.config.identity_api.password,
            self.config.compute_api.tenant_id)

        self.assertIsInstance(auth_resp.entity, Access)

        self.assertIsNotNone(
            auth_resp.entity.token.id,
            msg="Token is present returned %s".
            format(type(auth_resp.entity.token.id)))

        try:
            token_length = len(auth_resp.entity.token.id)
        except TypeError:
            token_length = 0

        self.assertEqual(
            token_length,
            self.default_token_length,
            msg='Default token length: {0} length of returned token {1}'.
            format(self.default_token_length, token_length))

        regex = re.compile('{0}{1}{2}{3}'.format(
            '^([a-zA-Z0-9]+-?)',
            '([a-zA-Z0-9]+-?)',
            '([a-zA-Z0-9]+-?)',
            '([a-zA-Z0-9]+-?)$'))

        self.assertIsNotNone(
            regex.match(auth_resp.entity.token.id),
            msg='Invalid token format')

        parsed_time = None
        try:
            parsed_time = parse(auth_resp.entity.token.expires)
            ptime = parsed_time.timetuple()
        except ValueError:
            pass

        self.assertIsInstance(
            ptime,
            struct_time,
            msg='Token expiration time stamp format is correct')

        current_time = self.datetime.now(parsed_time.tzinfo)

        delta = (parsed_time - current_time)

        self.assertGreaterEqual(
            delta,
            timedelta(days=0),
            msg='Token Expiration >= Current Time returned {0}'.
            format(delta >= timedelta(days=0)))

        self.assertLessEqual(
            delta, timedelta(days=1),
            msg='Token Expiration Delta <= 24hrs returned {0}'.
            format(delta <= timedelta(days=1)))

    @attr('regression', type='positive')
    def test_base_authentication_tenant_id_and_token(self):
        '''TODO:>>> offset needs to be unhardcoded'''
        base_resp = self.public_client.authenticate_user_apikey(
            self.config.identity_api.username,
            self.config.identity_api.api_key)

        auth_resp = self.public_client.authenticate_tenantid_and_token(
            self.config.identity_api.tenant_id,
            base_resp.entity.token.id)

        self.assertIsInstance(auth_resp.entity, Access)

        self.assertIsNotNone(
            auth_resp.entity.token.id,
            msg="Token is present returned %s".
            format(type(auth_resp.entity.token.id)))

        try:
            token_length = len(auth_resp.entity.token.id)
        except TypeError:
            token_length = 0

        self.assertEqual(
            token_length,
            self.default_token_length,
            msg='Default token length: {0} length of returned token {1}'.
            format(self.default_token_length, token_length))

        regex = re.compile('{0}{1}{2}{3}'.format(
            '^([a-zA-Z0-9]+-?)',
            '([a-zA-Z0-9]+-?)',
            '([a-zA-Z0-9]+-?)',
            '([a-zA-Z0-9]+-?)$'))

        self.assertIsNotNone(
            regex.match(auth_resp.entity.token.id),
            msg='Invalid token format')

        parsed_time = None
        try:
            parsed_time = parse(auth_resp.entity.token.expires)
            ptime = parsed_time.timetuple()
        except ValueError:
            pass

        self.assertIsInstance(
            ptime,
            struct_time,
            msg='Token expiration time stamp format is correct')

        current_time = self.datetime.now(parsed_time.tzinfo)

        delta = (parsed_time - current_time)

        self.assertGreaterEqual(
            delta,
            timedelta(days=0),
            msg='Token Expiration >= Current Time returned {0}'.
            format(delta >= timedelta(days=0)))

        self.assertLessEqual(
            delta, timedelta(days=1),
            msg='Token Expiration Delta <= 24hrs returned {0}'.
            format(delta <= timedelta(days=1)))

    @attr('regression', type='positive')
    def test_base_authentication_tenant_name_and_token(self):
        '''TODO:>>> offset needs to be unhardcoded'''
        username = self.config.identity_api.username
        api_key = self.config.identity_api.api_key
        user_admin_auth = self.public_client.authenticate_user_apikey(
            username=username,
            api_key=api_key).entity
        self.public_client.token = user_admin_auth.token.id
        base_resp = self.public_client.get_tenants()
        del self.public_client.token
        sample_tenant = base_resp.entity[0]

        auth_resp = self.public_client.authenticate_tenantname_and_token(
            sample_tenant.name,
            user_admin_auth.token.id)

        self.assertIsInstance(auth_resp.entity, Access)

        self.assertIsNotNone(
            auth_resp.entity.token.id,
            msg="Token is present returned %s".
            format(type(auth_resp.entity.token.id)))

        try:
            token_length = len(auth_resp.entity.token.id)
        except TypeError:
            token_length = 0

        self.assertEqual(
            token_length,
            self.default_token_length,
            msg='Default token length: {0} length of returned token {1}'.
            format(self.default_token_length, token_length))

        regex = re.compile('{0}{1}{2}{3}'.format(
            '^([a-zA-Z0-9]+-?)',
            '([a-zA-Z0-9]+-?)',
            '([a-zA-Z0-9]+-?)',
            '([a-zA-Z0-9]+-?)$'))

        self.assertIsNotNone(
            regex.match(auth_resp.entity.token.id),
            msg='Invalid token format')

        parsed_time = None
        try:
            parsed_time = parse(auth_resp.entity.token.expires)
            ptime = parsed_time.timetuple()
        except ValueError:
            pass

        self.assertIsInstance(
            ptime,
            struct_time,
            msg='Token expiration time stamp format is correct')

        current_time = self.datetime.now(parsed_time.tzinfo)

        delta = (parsed_time - current_time)

        self.assertGreaterEqual(
            delta,
            timedelta(days=0),
            msg='Token Expiration >= Current Time returned {0}'.
            format(delta >= timedelta(days=0)))

        self.assertLessEqual(
            delta, timedelta(days=1),
            msg='Token Expiration Delta <= 24hrs returned {0}'.
            format(delta <= timedelta(days=1)))

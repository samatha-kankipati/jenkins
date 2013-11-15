"""Basic Positive Tests for Rax Auth Admin"""
from datetime import datetime, timedelta
from time import struct_time, mktime
from testrepo.common.testfixtures.identity.v2_0.identity \
    import IdentityAdminFixture
from ccengine.clients.identity.v2_0.rax_auth_api import IdentityClient
from ccengine.common.decorators import attr
from ccengine.common.tools.datagen import rand_name
from dateutil.parser import parse


class AdminTokenTest(IdentityAdminFixture):
    """Basic Smoke Tests - Check HTTP Resoponses Authentication Admin"""

    @classmethod
    def setUpClass(cls):
        super(AdminTokenTest, cls).setUpClass()
        cls.datetime = datetime
        cls.default_token_length = 32
        cls.public_client_no_token = IdentityClient(
            url=cls.config.identity_api.authentication_endpoint,
            serialize_format=cls.config.misc.serializer,
            deserialize_format=cls.config.misc.deserializer)

    @classmethod
    def tearDownClass(cls):
        pass

    @attr('regression', type='positive')
    def test_validate_token(self):
        auth_resp = self.public_client_no_token.authenticate_user_apikey(
            self.config.identity_api.username,
            self.config.identity_api.api_key)

        token = auth_resp.entity.token.id
        token_resp = self.admin_client.validate_token(
            token_id=token)

        self.assertEqual(token_resp.status_code, 200,
                         msg="Expected response 200 received response %s" %
                             token_resp.status_code)
        parsed_time = None
        try:
            parsed_time = parse(token_resp.entity.token.expires)
            ptime = parsed_time.timetuple()
        except ValueError:
            pass
        self.assertIsInstance(
            ptime, struct_time,
            msg='Token expiration time stamp format is correct')
        current_time = self.datetime.now()
        exp_time = datetime.fromtimestamp(mktime(ptime))
        delta = (exp_time - current_time)
        self.assertGreaterEqual(
            delta, timedelta(days=0),
            msg='Token Expiration >= Current Time returned %s' %
                (delta >= timedelta(days=0)))

    @attr('regression', type='positive')
    def test_validate_token_belongs_to(self):
        '''TODO: add belongs to'''
        normal_response_codes = [200, 203]
        auth_resp = self.public_client.authenticate_user_apikey(
            self.config.identity_api.username,
            self.config.identity_api.api_key)

        self.assertEqual(auth_resp.status_code, 200,
                         msg="Expected response 200 received response %s" %
                             auth_resp.status_code)

        token = auth_resp.entity.token.id
        token_resp = self.admin_client.validate_token(
            token_id=token)

        self.assertEqual(token_resp.status_code, 200,
                         msg="Expected response 200 received response %s" %
                             token_resp.status_code)

    @attr('regression', type='positive')
    def test_validate_token_user_part(self):
        auth_resp = self.public_client_no_token.authenticate_user_apikey(
            self.config.identity_api.username,
            self.config.identity_api.api_key)
        self.assertEqual(auth_resp.status_code, 200,
                         msg="Expected response 200 received response %s" %
                             auth_resp.status_code)
        token = auth_resp.entity.token.id
        token_resp = self.admin_client.validate_token(
            token_id=token)
        self.assertEqual(token_resp.status_code, 200,
                         msg="Expected response 200 received response %s" %
                             token_resp.status_code)
        self.assertEqual(token_resp.entity.user.name,
                         self.config.identity_api.username,
                         msg="Expected names match %s" %
                             token_resp.status_code)
        self.assertTrue(token_resp.entity.user.roles[0] is not None,
                        msg="At least one role is present is present")

    @attr('regression', type='positive')
    def test_check_token(self):
        auth_resp = self.public_client_no_token.authenticate_user_apikey(
            self.config.identity_api.username,
            self.config.identity_api.api_key)
        self.assertEqual(auth_resp.status_code, 200,
                         msg="Expected response 200 received response %s" %
                             auth_resp.status_code)
        token = auth_resp.entity.token.id
        token_resp = self.admin_client.check_token(
            token_id=token)
        self.assertEqual(token_resp.status_code, 200,
                         msg="Expected response 200 received response %s" %
                             token_resp.status_code)

    @attr('regression', type='positive')
    def test_list_endpoints_for_token(self):
        auth_resp = self.public_client_no_token.authenticate_user_apikey(
            self.config.identity_api.username,
            self.config.identity_api.api_key)
        self.assertEqual(
            auth_resp.status_code, 200,
            msg="Expected response 200 received response %s" %
                auth_resp.status_code)
        token = auth_resp.entity.token.id
        token_resp = self.admin_client.list_endpoints_for_token(
            token_id=token)
        self.assertEqual(
            token_resp.status_code, 200,
            msg="Expected response 200 received response %s" %
                token_resp.status_code)
        self.assertTrue(token_resp.entity[0] is not None,
                        msg="At least one role is present is present")

    @attr('regression', type='positive')
    def test_revoke_token(self):
        username = rand_name("cctestname")
        email = '@'.join([username, 'supra.com'])
        password = 'Gellpass8'
        domains = self.admin_client.get_domains().entity
        create_user = self.admin_client.add_user(
            username=username,
            email=email,
            enabled=True,
            password=password,
            domain_id=domains[0].id)
        # Delete user after test completion
        self.addCleanup(self.delete_user_permanently,
                        user_id=create_user.entity.id,
                        client=self.admin_client)
        #authenticate with new user
        auth_resp = self.admin_client.authenticate_user_password(
            username=username, password=password)
        self.assertEquals(auth_resp.status_code, 200,
                          'Exepected response code {0} actual {1}'
                          .format(200, auth_resp.status_code))
        #get new client using new user's token
        token_client = self.provider.get_client(
            token=auth_resp.entity.token.id)
        #check that token can successfully be used
        list_users_resp = token_client.list_users()
        self.assertEquals(list_users_resp.status_code, 200,
                          'Exepected response code {0} actual {1}'
                          .format(200, list_users_resp.status_code))
        #check check token
        check_resp = self.admin_client.check_token(auth_resp.entity.token.id)
        self.assertEquals(check_resp.status_code, 200,
                          'Exepected response code {0} actual {1}'
                          .format(200, check_resp.status_code))
        #revoke token
        revoke_resp = self.admin_client.revoke_token(auth_resp.entity.token.id)
        self.assertEquals(revoke_resp.status_code, 204,
                          'Exepected response code {0} actual {1}'
                          .format(200, revoke_resp.status_code))
        #should not be allowed
        list_users_resp = token_client.list_users()
        self.assertEquals(list_users_resp.status_code, 401,
                          'Exepected response code {0} actual {1}'
                          .format(401, list_users_resp.status_code))
        check_resp = self.admin_client.check_token(auth_resp.entity.token.id)
        self.assertEquals(check_resp.status_code, 404,
                          'Exepected response code {0} actual {1}'
                          .format(404, check_resp.status_code))
        validate_resp = self.admin_client.validate_token(
            auth_resp.entity.token.id)
        self.assertEquals(validate_resp.status_code, 404,
                          'Exepected response code {0} actual {1}'
                          .format(404, validate_resp.status_code))

    @attr('regression', type='positive')
    def test_authentication_response(self):
        username = rand_name("ccadminname_auth_response")
        email = username + "@supra.com"
        domain_id = "421342654"
        default_region = self.config.identity_api.default_region
        password = "Password1"
        api_key = "1234567890"

        create_user = self.admin_client.add_user(username=username,
                                                 email=email, enabled=True,
                                                 default_region=default_region,
                                                 domain_id=domain_id,
                                                 password=password)
        self.assertEqual(create_user.status_code, 201,
                         msg="Response for add user is not 201.")
        # Delete user after test completion
        self.addCleanup(self.delete_user_permanently,
                        user_id=create_user.entity.id,
                        client=self.admin_client)

        update_cred = self.admin_client.update_user_credentials(
            create_user.entity.id, username, api_key)

        auth_resp_password = self.admin_client.authenticate_user_password(
            username, password)

        auth_resp_apikey = self.admin_client.authenticate_user_apikey(
            username, api_key)

        #RSA is also needed. Hard to automate.

        self.assertEqual(create_user.status_code, 201,
                         msg="Create user should return %d but received %s" % (
                             200, create_user.status_code))
        self.assertEqual(update_cred.status_code, 200,
                         msg="Create user should return %d but received %s" % (
                             200, update_cred.status_code))
        self.assertEquals(
            auth_resp_password.entity.token.authenticatedBy[0],
            'PASSWORD', 'Expected PASSWORD, received %s'
                        % auth_resp_password.entity.token.authenticatedBy)
        self.assertEquals(
            auth_resp_apikey.entity.token.authenticatedBy[0],
            'APIKEY', 'Expected APIKEY, received %s'
                      % auth_resp_apikey.entity.token.authenticatedBy)

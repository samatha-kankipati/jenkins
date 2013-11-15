from datetime import datetime
from re import match
from time import struct_time

from dateutil.parser import parse
from ccengine.common.decorators import attr
from ccengine.common.tools.datagen import rand_name
from ccengine.common.tools.datagen import random_int
from testrepo.common.testfixtures.identity.v1_1.identity import IdentityFixture


class AdminTokenTest(IdentityFixture):
    @classmethod
    def setUpClass(cls):
        super(AdminTokenTest, cls).setUpClass()
        cls.uid = rand_name("ccusername")
        cls.key = 'asdasdasd-adsasdads-asdasdasd-adsadsasd'
        cls.mosso_id = random_int(1000000, 9000000)
        cls.nast_id = random_int(1000000, 9000000)
        cls.enabled = True
        cls.password = 'CCPassword1'
        cls.create_user = cls.admin_client.create_user(
            id=cls.uid,
            key=cls.key,
            enabled=cls.enabled,
            mosso_id=cls.mosso_id,
            nast_id=cls.nast_id)
        get_user = cls.admin_client_vsec.get_user_by_name(name=cls.uid)
        cls.admin_client_vsec.add_user_credentials(
            user_id=get_user.entity.id,
            username=get_user.entity.username,
            password=cls.password)
        cls.datetime = datetime
        cls.default_token_length = 32

    @classmethod
    def tearDownClass(cls):
        get_user = cls.admin_client_vsec.get_user_by_name(name=cls.uid)
        cls.admin_client.delete_user(user_id=cls.create_user.entity.id)
        cls.service_client.delete_user_hard(get_user.entity.id)

    def _test_token_assertion(self, auth_resp, token_obj=None):
        """
        Token related assertions and verifications

        """
        normal_response_codes = [200, 203]
        token_length = len(auth_resp.entity.token.id.strip())
        msg = 'Default length: {0} length of returned token {1}'.format(
            self.default_token_length, token_length)
        self.assertEqual(token_length, self.default_token_length, msg)

        regex = ''.join(['^([a-zA-Z0-9]+-?)',
                         '([a-zA-Z0-9]+-?)',
                         '([a-zA-Z0-9]+-?)',
                         '([a-zA-Z0-9]+-?)$'])
        valid_token = match(regex, auth_resp.entity.token.id) is not None
        self.assertTrue(
            valid_token,
            msg=('Token contains only valid chars, returned {0}'.format(
                valid_token)))

        parsed_time = None
        parsed_time = parse(auth_resp.entity.token.expires)
        ptime = parsed_time.timetuple()
        self.assertIsInstance(
            ptime, struct_time,
            msg='Token expiration time stamp format is In-correct')

        if token_obj is None:
            validate_token = self.admin_client.validate_token(
                token_id=auth_resp.entity.token.id)
            token_obj = validate_token
        self.assertIn(
            token_obj.status_code,
            normal_response_codes,
            msg="Expected response {0}, received {1}".format(
                normal_response_codes, token_obj.status_code))
        self.assertEquals(
            token_obj.entity.id,
            auth_resp.entity.token.id,
            msg="Token received doesn't match with auth response token")
        self.assertEquals(
            token_obj.entity.userId,
            self.uid,
            msg="User Ids received doesn't match")
        self.assertEquals(
            token_obj.entity.expires,
            auth_resp.entity.token.expires,
            msg="Expiration date received doesn't match with auth response")
        self.assertTrue('v1.1/users/{0}'.format(self.uid) in
                        token_obj.entity.userURL,
                        msg="Expecting username in the userURL is correct")

        delta = self.get_token_ttl_delta(token_obj)
        cloud_token_ttl = self.config.identity_api.cloud_token_ttl
        token_entropy = self.config.identity_api.token_entropy
        token_exp_upper = (float(cloud_token_ttl) *
                           (1 + float(token_entropy) / 100))
        token_exp_low = (float(cloud_token_ttl) *
                         (1 - float(token_entropy) / 100))
        self.assertTrue(
            token_exp_low <= delta <= token_exp_upper,
            msg="Token is out of Cloud Token Time to live range")

    def _test_revoke_token(self, auth_resp):
        """
        Test to revoke token and verifying revoke

        """
        response_code_revoke = [204]
        revoke_token = self.admin_client.revoke_token(
            token_id=auth_resp.entity.token.id)
        self.assertIn(
            revoke_token.status_code,
            response_code_revoke,
            msg='Get base URLs expected {0} received {1}'.format(
                response_code_revoke,
                revoke_token.status_code))
        get_token = self.admin_client.get_token(
            token_id=auth_resp.entity.token.id)
        self.assertEqual(
            get_token.status_code, 404,
            msg="Get Token Response is 404")
        self.assertTrue('{0} not found'.format('Token') in get_token.content,
                        msg="Token shouldn't be in the system")

    @attr('regression', type='positive')
    def test_mosso_authentication(self):
        """
        Test to verify Authentication with mossoid and key response

        """
        normal_response_codes = [200, 203]
        self.assertEqual(
            self.create_user.status_code, 201,
            msg=("Create User expected response 201 received {0}"
                 .format(self.create_user.status_code)))
        auth_resp = self.admin_client.authenticate_mosso(
            mosso_id=self.mosso_id,
            key=self.key)
        self.assertIn(
            auth_resp.status_code, normal_response_codes,
            msg=("Auth response expected {0} received {1}".format(
                normal_response_codes, auth_resp.status_code)))
        self.assertIsNotNone(
            auth_resp.entity.token.id,
            msg="Token received {0}".format(auth_resp.entity.token.id))

        self._test_token_assertion(auth_resp=auth_resp)
        self._test_revoke_token(auth_resp)

    @attr('regression', type='positive')
    def test_nast_authentication(self):
        """
        Test to verify Authentication with nastid and key response

        """
        normal_response_codes = [200, 203]
        self.assertEqual(
            self.create_user.status_code, 201,
            msg=("Create User expected response 201 received {0}"
                 .format(self.create_user.status_code)))
        auth_resp = self.admin_client.authenticate_nast(
            nast_id=self.create_user.entity.nastId,
            key=self.key)
        self.assertIn(
            auth_resp.status_code, normal_response_codes,
            msg=("Auth response expected {0} received {1}".format(
                normal_response_codes, auth_resp.status_code)))
        self.assertIsNotNone(
            auth_resp.entity.token.id,
            msg="Token received {0}".format(auth_resp.entity.token.id))

        self._test_token_assertion(auth_resp=auth_resp)
        self._test_revoke_token(auth_resp)

    @attr('regression', type='positive')
    def test_password_authentication(self):
        """
        Test to verify Authentication with password response

        """
        normal_response_codes = [200, 203]
        auth_resp = self.admin_client.authenticate_password(
            username=self.uid,
            password=self.password)
        self.assertIn(
            auth_resp.status_code, normal_response_codes,
            msg=('Get base URLs expected {0} received {1}'.format(
                normal_response_codes, auth_resp.status_code)))
        self.assertIsNotNone(
            auth_resp.entity.token.id,
            msg="Token received {0}".format(auth_resp.entity.token.id))

        self._test_token_assertion(auth_resp=auth_resp)
        self._test_revoke_token(auth_resp)

    @attr('regression', type='positive')
    def test_get_token(self):
        """
        Test to verify get token response

        """
        normal_response_codes = [200, 203]
        auth_resp = self.admin_client.authenticate_password(
            username=self.uid,
            password=self.password)
        self.assertIn(
            auth_resp.status_code, normal_response_codes,
            msg=("Auth response expected {0} received {1}".format(
                normal_response_codes, auth_resp.status_code)))
        self.assertIsNotNone(
            auth_resp.entity.token.id,
            msg="Token received {0}".format(auth_resp.entity.token.id))

        get_token = self.admin_client.get_token(
            token_id=auth_resp.entity.token.id)
        self._test_token_assertion(auth_resp=auth_resp,
                                   token_obj=get_token)
        self._test_revoke_token(auth_resp)

    @attr('regression', type='positive')
    def test_validate_and_revoke_token(self):
        """
        Test to verify validate and revoke token responses

        """
        normal_response_codes = [200, 203]
        auth_resp = self.admin_client.authenticate_password(
            username=self.uid,
            password=self.password)
        self.assertIn(
            auth_resp.status_code, normal_response_codes,
            msg=("Auth response expected {0} received {1}".format(
                normal_response_codes, auth_resp.status_code)))
        self.assertIsNotNone(
            auth_resp.entity.token.id,
            msg="Token received {0}".format(auth_resp.entity.token.id))

        validate_token = self.admin_client.validate_token(
            token_id=auth_resp.entity.token.id)
        self._test_token_assertion(auth_resp=auth_resp,
                                   token_obj=validate_token)
        self._test_revoke_token(auth_resp)

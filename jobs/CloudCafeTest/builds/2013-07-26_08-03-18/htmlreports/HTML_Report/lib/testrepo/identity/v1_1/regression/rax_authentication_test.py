from datetime import datetime, timedelta
from dateutil.parser import parse
from re import match
from time import struct_time, mktime

from ccengine.common.decorators import attr
from ccengine.common.tools.datagen import rand_name
from ccengine.common.tools.datagen import random_int
from testrepo.common.testfixtures.identity.v1_1.identity import IdentityFixture


class AuthenticationTest(IdentityFixture):

    @classmethod
    def setUpClass(cls):
        super(AuthenticationTest, cls).setUpClass()
        cls.datetime = datetime
        cls.default_token_length = 32

    @classmethod
    def tearDownClass(cls):
        pass

    @attr('regression', type='positive')
    def test_base_authentication_username_and_key(self):
        normal_response_codes = [200, 203]
        auth_resp = self.client.authenticate_user(
            username=self.config.identity_api.username,
            key=self.config.identity_api.api_key)

        self.assertIn(
            auth_resp.status_code,
            normal_response_codes,
            msg=('Auth response codes expected {0} recieved {1}'
                 .format(normal_response_codes, auth_resp.status_code)))

        self.assertTrue(
            auth_resp.entity.token.id is not None,
            msg=("Token is present returned {0}"
                 .format((auth_resp.entity.token.id is not None))))

        if auth_resp.entity.token.id is not None:
            token_length = len(auth_resp.entity.token.id)
            msg = ('Default token length: {0} length of returned token {1}'
                   .format(self.default_token_length, token_length))
            self.assertEqual(token_length, self.default_token_length, msg)
            regex = ''.join(['^([a-zA-Z0-9]+-?)',
                            '([a-zA-Z0-9]+-?)',
                            '([a-zA-Z0-9]+-?)',
                            '([a-zA-Z0-9]+-?)$'])
            valid_token = match(regex, auth_resp.entity.token.id) is not None
            self.assertTrue(
                valid_token,
                msg=('Token contains only valid chars returned {0}'
                     .format(valid_token)))

        parsed_time = None
        try:
            parsed_time = parse(auth_resp.entity.token.expires)
            ptime = parsed_time.timetuple()
        except ValueError:
            pass

        self.assertIsInstance(
            ptime,
            struct_time,
            msg=('Token expiration - expected: {0}, actual: {1}'
                 .format(struct_time, ptime)))

        current_time = self.datetime.now()
        exp_time = datetime.fromtimestamp(mktime(ptime))

        delta = (exp_time - current_time)

        self.assertGreaterEqual(
            delta,
            timedelta(days=0),
            msg=('Token Expiration >= Current Time returned {0}'
                 .format(delta >= timedelta(days=0))))

    @attr('regression', type='positive')
    def test_token_entropy(self):
        """
        Testing token time to live - here we create a series of tokens
        and make sure that the token time to live for all the created tokens
        is not same and falls within a range (check config file for range)

        """
        normal_response_codes = [200, 203]
        response_code_revoke = [204]
        uid = rand_name("ccusername")
        key = 'asdasdasd-adsasdads-asdasdasd-adsadsasd'
        mossoId = random_int(1000000, 9000000)
        nastId = random_int(1000000, 9000000)
        enabled = True
        create_user = self.admin_client.create_user(
            id=uid,
            key=key,
            enabled=enabled,
            mossoId=mossoId,
            nastId=nastId)
        self.assertEqual(
            create_user.status_code,
            201,
            msg='Create user expected response 201, received {0}'.format(
                create_user.status_code))

        # addCleanup works as stack, First in Last out
        get_user = self.admin_client_vsec.get_user_by_name(name=uid)
        self.addCleanup(self.service_client.delete_user_hard,
                        userId=get_user.entity.id)
        self.addCleanup(self.admin_client.delete_user,
                        userId=create_user.entity.id)

        """
        Token entropy range calculation, the ranges are in seconds
        """
        cloud_token_ttl = self.config.identity_api.cloud_token_ttl
        token_entropy = self.config.identity_api.token_entropy
        token_exp_upper = (float(cloud_token_ttl) *
                           (1 + float(token_entropy) / 100))
        token_exp_low = (float(cloud_token_ttl) *
                         (1 - float(token_entropy) / 100))

        """
        Here entropy_loop is a random number to verify number of tokens ttl
        """
        entropy_loop = 10
        for itr in range(entropy_loop):

            auth_resp = self.client.authenticate_user(
                username=uid,
                key=key)

            self.assertIn(
                auth_resp.status_code,
                normal_response_codes,
                msg='Auth response codes expected {0} recieved {1}'.format(
                    normal_response_codes,
                    auth_resp.status_code))

            self.assertTrue(
                auth_resp.entity.token.id is not None,
                msg="Token is present returned {0}".format(
                    auth_resp.entity.token.id is not None))

            validate_token = self.admin_client.validate_token(
                tokenId=auth_resp.entity.token.id)
            self.assertIn(
                validate_token.status_code,
                normal_response_codes,
                msg='Get base URLs expected {0} received {1}'.format(
                    normal_response_codes,
                    validate_token.status_code))

            delta = self.get_token_ttl_delta(validate_token)

            self.assertTrue(
                token_exp_low <= delta <= token_exp_upper,
                msg="Token is out of Cloud Token Time to live range")

            revoke_token = self.admin_client.revoke_token(
                tokenId=auth_resp.entity.token.id)
            self.assertIn(
                revoke_token.status_code,
                response_code_revoke,
                msg=('Auth response codes expected {0} recieved {1}'
                     .format(response_code_revoke, auth_resp.status_code)))

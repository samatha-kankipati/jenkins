from datetime import datetime, timedelta
from dateutil.parser import parse
from re import match
from time import strptime, struct_time, mktime

from ccengine.common.decorators import attr
from testrepo.common.testfixtures.identity.v1_1.identity import IdentityFixture


class AdminTokenTest(IdentityFixture):

    @classmethod
    def setUpClass(cls):
        super(AdminTokenTest, cls).setUpClass()
        cls.datetime = datetime
        cls.default_token_length = 32

    @classmethod
    def tearDownClass(cls):
        pass

    def _token_response_assertion(self, token_obj, auth_resp):
        normal_response_codes = [200, 203]
        self.assertIn(
            token_obj.status_code,
            normal_response_codes,
            msg='Get base URLs expected {0} received {1}'.format(
                normal_response_codes,
                token_obj.status_code))
        self.assertEquals(
            token_obj.entity.id,
            auth_resp.entity.token.id,
            msg='Tokens match')
        self.assertEquals(
            token_obj.entity.userId,
            self.config.identity_api.username,
            msg='User Ids are identical')
        self.assertEquals(
            token_obj.entity.expires,
            auth_resp.entity.token.expires,
            msg='Expiration dates match')
        self.assertTrue('v1.1/users/{0}'.format(
            self.config.identity_api.username) in token_obj.entity.userURL,
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

    @attr('regression', type='positive')
    def test_mosso_authentication(self):
        normal_response_codes = [200, 203]
        auth_resp = self.admin_client.authenticate_mosso(
            mossoId=self.config.identity_api.mosso_Id,
            key=self.config.identity_api.mosso_key)

        self.assertIn( auth_resp.status_code, normal_response_codes,
                msg= 'Get base URLs expected {0} received {1}'.format(
                    normal_response_codes, 
                    auth_resp.status_code))
        
        self.assertTrue(auth_resp.entity.token.id is not None,
                msg="Token is present returned {0}".format(
                    auth_resp.entity.token.id))
        
        auth_resp.entity.token.id = (auth_resp.entity.token.id).replace('-','')

        if auth_resp.entity.token.id is not None:
            token_length = len(auth_resp.entity.token.id)
            msg = 'Default length: {0} length of returned token {1}'.format(
                self.default_token_length, token_length)
            self.assertEqual(token_length, self.default_token_length, msg)

            regex = ''.join(['^([a-zA-Z0-9]+-?)',
                            '([a-zA-Z0-9]+-?)',
                            '([a-zA-Z0-9]+-?)',
                            '([a-zA-Z0-9]+-?)$'])
            valid_token = match(regex, auth_resp.entity.token.id) is not None
            self.assertTrue(valid_token,
                msg='Token contains only valid chars returned {0}'.format(
                    valid_token))

        parsed_time = None
        try:
            parsed_time = parse(auth_resp.entity.token.expires)
            ptime = parsed_time.timetuple()
        except ValueError:
            pass

        self.assertIsInstance(ptime, struct_time,
                msg='Token expiration time stamp format is correct')

        current_time = self.datetime.now()
        exp_time = datetime.fromtimestamp(mktime(ptime))

        delta = (exp_time - current_time)

        self.assertGreaterEqual(delta, timedelta(days=0),
                msg='Token Expiration >= Current Time returned {0}'.format(
                (delta >= timedelta(days=0))))

    @attr('regression', type='positive')
    def test_nast_authentication(self):
        normal_response_codes = [200, 203]
        auth_resp = self.admin_client.authenticate_nast(
            nastId=self.config.identity_api.nast_Id,
            key=self.config.identity_api.nast_key)

        self.assertIn( auth_resp.status_code, normal_response_codes,
            msg= 'Get base URLs expected {0} received {1}'.format(
                normal_response_codes, 
                auth_resp.status_code))
        
        self.assertTrue(auth_resp.entity.token.id is not None,
            msg="Token is present returned {0}".format(
                auth_resp.entity.token.id))
        
        auth_resp.entity.token.id = (auth_resp.entity.token.id).replace('-','')

        if auth_resp.entity.token.id is not None:
            token_length = len(auth_resp.entity.token.id)
            msg = 'Default length: {0} length of returned token {1}'.format(
                self.default_token_length, token_length)
            self.assertEqual(token_length, self.default_token_length, msg)

            regex = ''.join(['^([a-zA-Z0-9]+-?)',
                            '([a-zA-Z0-9]+-?)',
                            '([a-zA-Z0-9]+-?)',
                            '([a-zA-Z0-9]+-?)$'])
            valid_token = match(regex, auth_resp.entity.token.id) is not None
            self.assertTrue(valid_token,
                msg='Token contains only valid chars returned {0}'.format(
                    valid_token))

        parsed_time = None
        try:
            parsed_time = parse(auth_resp.entity.token.expires)
            ptime = parsed_time.timetuple()
        except ValueError:
            pass

        self.assertIsInstance(ptime, struct_time,
            msg='Token expiration time stamp format is correct')

        current_time = self.datetime.now()
        exp_time = datetime.fromtimestamp(mktime(ptime))

        delta = (exp_time - current_time)

        self.assertGreaterEqual(delta, timedelta(days=0),
            msg='Token Expiration >= Current Time returned {0}'.format(
            (delta >= timedelta(days=0))))

    @attr('regression', type='positive')
    def test_password_authentication(self):
        normal_response_codes = [200, 203]
        auth_resp = self.admin_client.authenticate_password(
            username=self.config.identity_api.username,
            password=self.config.identity_api.password)

        self.assertIn( auth_resp.status_code, normal_response_codes,
            msg= 'Get base URLs expected {0} received {1}'.format(
                normal_response_codes, 
                auth_resp.status_code))
        
        self.assertTrue(auth_resp.entity.token.id is not None,
            msg="Token is present returned {0}".format(
                auth_resp.entity.token.id))
        
        auth_resp.entity.token.id = (auth_resp.entity.token.id).replace('-','')

        if auth_resp.entity.token.id is not None:
            token_length = len(auth_resp.entity.token.id)
            msg = 'Default length: {0} length of returned token {1}'.format(
                self.default_token_length, token_length)
            self.assertEqual(token_length, self.default_token_length, msg)

            regex = ''.join(['^([a-zA-Z0-9]+-?)',
                            '([a-zA-Z0-9]+-?)',
                            '([a-zA-Z0-9]+-?)',
                            '([a-zA-Z0-9]+-?)$'])
            valid_token = match(regex, auth_resp.entity.token.id) is not None
            self.assertTrue(valid_token,
                msg='Token contains only valid chars returned {0}'.format(
                    valid_token))

        parsed_time = None
        try:
            parsed_time = parse(auth_resp.entity.token.expires)
            ptime = parsed_time.timetuple()
        except ValueError:
            pass

        self.assertIsInstance(ptime, struct_time,
                msg='Token expiration time stamp format is correct')

        current_time = self.datetime.now()
        exp_time = datetime.fromtimestamp(mktime(ptime))

        delta = (exp_time - current_time)

        self.assertGreaterEqual(delta, timedelta(days=0),
                msg='Token Expiration >= Current Time returned {0}'.format(
                (delta >= timedelta(days=0))))

    @attr('regression', type='positive')
    def test_get_token(self):
        normal_response_codes = [200, 203]
        auth_resp = self.admin_client.authenticate_password(
            username=self.config.identity_api.username,
            password=self.config.identity_api.password)
        self.assertIn(
            auth_resp.status_code,
            normal_response_codes,
            msg='Get base URLs expected {0} received {1}'.format(
                normal_response_codes,
                auth_resp.status_code))

        get_token = self.admin_client.get_token(
            tokenId=auth_resp.entity.token.id)
        self._token_response_assertion(get_token, auth_resp)

    @attr('regression', type='positive')
    def test_validate_token(self):
        normal_response_codes = [200, 203]
        auth_resp = self.admin_client.authenticate_password(
            username=self.config.identity_api.username,
            password=self.config.identity_api.password)
        self.assertIn(
            auth_resp.status_code,
            normal_response_codes,
            msg='Get base URLs expected {0} received {1}'.format(
                normal_response_codes,
                auth_resp.status_code))

        validate_token = self.admin_client.validate_token(
            tokenId=auth_resp.entity.token.id)
        self._token_response_assertion(validate_token, auth_resp)

    @attr('regression', type='positive')
    def test_revoke_token(self):
        normal_response_codes = [200, 203]
        response_code_revoke = [204]
        auth_resp = self.admin_client.authenticate_password(
            username=self.config.identity_api.username,
            password=self.config.identity_api.password)
        self.assertIn(
            auth_resp.status_code,
            normal_response_codes,
            msg='Get base URLs expected {0} received {1}'.format(
                normal_response_codes,
                auth_resp.status_code))

        revoke_token = self.admin_client.revoke_token(
            tokenId=auth_resp.entity.token.id)
        self.assertIn(
            revoke_token.status_code,
            response_code_revoke,
            msg='Get base URLs expected {0} received {1}'.format(
                response_code_revoke,
                revoke_token.status_code))
        get_token = self.admin_client.get_token(
            tokenId=auth_resp.entity.token.id)
        self.assertEqual(get_token.status_code, 404, msg="Response is 404")
        self.assertTrue('{0} not found'.format('Token') in get_token.content,
                        msg="Token shouldn't be in the system")

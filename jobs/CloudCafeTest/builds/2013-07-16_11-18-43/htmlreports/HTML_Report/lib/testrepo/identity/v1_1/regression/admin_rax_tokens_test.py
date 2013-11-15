from testrepo.common.testfixtures.identity.v1_1.identity import IdentityFixture
from ccengine.common.decorators import attr
from datetime import datetime, timedelta
from time import strptime, struct_time, mktime
from re import match
from dateutil.parser import parse


class AdminTokenTest(IdentityFixture):

    @classmethod
    def setUpClass(cls):
        super(AdminTokenTest, cls).setUpClass()
        cls.datetime = datetime
        cls.default_token_length = 32

    @classmethod
    def tearDownClass(cls):
        pass

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
        self.assertIn( auth_resp.status_code, normal_response_codes,
            msg= 'Get base URLs expected {0} received {1}'.format(
                normal_response_codes, 
                auth_resp.status_code))
        
        get_token = self.admin_client.get_token(
            tokenId=auth_resp.entity.token.id)
        self.assertIn( get_token.status_code, normal_response_codes,
            msg= 'Get base URLs expected {0} received {1}'.format(
                normal_response_codes, 
                get_token.status_code))
        self.assertEquals(get_token.entity.id, 
            auth_resp.entity.token.id,
            msg='Tokens match')
        self.assertEquals(get_token.entity.userId, 
            self.config.identity_api.username,
            msg='User Ids are identical')
        self.assertEquals(get_token.entity.expires, 
            auth_resp.entity.token.expires,
            msg='Expiration dates match')
        self.assertTrue('v1.1/users/{0}'.format(
            self.config.identity_api.username) in 
            get_token.entity.userURL,
            msg="Expecting username in the userURL is correct")
        
        parsed_time_exp = None
        parsed_time_cr = None
        try:
            parsed_time_exp = parse(get_token.entity.expires)
            ptime_exp = parsed_time_exp.timetuple()
            parsed_time_cr = parse(get_token.entity.created)
            ptime_cr = parsed_time_cr.timetuple()
        except ValueError:
            pass

        self.assertIsInstance(ptime_exp, struct_time,
            msg='Token expiration time stamp format is correct')
        self.assertIsInstance(ptime_cr, struct_time,
            msg='Token expiration time stamp format is correct')

        created_time = datetime.fromtimestamp(mktime(ptime_cr))
        exp_time = datetime.fromtimestamp(mktime(ptime_exp))

        delta = (exp_time - created_time)
        oneday = timedelta(days=1)
        self.assertEqual(delta, oneday,
            msg='Token Expiration is 1 day after creation')

    @attr('regression', type='positive')
    def test_validate_token(self):
        normal_response_codes = [200, 203]
        auth_resp = self.admin_client.authenticate_password(
            username=self.config.identity_api.username,
            password=self.config.identity_api.password)
        self.assertIn( auth_resp.status_code, normal_response_codes,
            msg= 'Get base URLs expected {0} received {1}'.format(
                normal_response_codes, 
                auth_resp.status_code))
        
        validate_token = self.admin_client.validate_token(
            tokenId=auth_resp.entity.token.id)
        self.assertIn( validate_token.status_code, normal_response_codes,
            msg= 'Get base URLs expected {0} received {1}'.format(
                normal_response_codes, 
                validate_token.status_code))
        self.assertEquals(validate_token.entity.id, 
            auth_resp.entity.token.id,
            msg='Tokens match')
        self.assertEquals(validate_token.entity.userId, 
            self.config.identity_api.username,
            msg='User Ids are identical')
        self.assertEquals(validate_token.entity.expires, 
            auth_resp.entity.token.expires,
            msg='Expiration dates match')
        self.assertTrue('v1.1/users/{0}'.format(
            self.config.identity_api.username) in 
            validate_token.entity.userURL,
            msg="Expecting username in the userURL is correct")
        
        parsed_time_exp = None
        parsed_time_cr = None
        try:
            parsed_time_exp = parse(validate_token.entity.expires)
            ptime_exp = parsed_time_exp.timetuple()
            parsed_time_cr = parse(validate_token.entity.created)
            ptime_cr = parsed_time_cr.timetuple()
        except ValueError:
            pass

        self.assertIsInstance(ptime_exp, struct_time,
            msg='Token expiration time stamp format is correct')
        self.assertIsInstance(ptime_cr, struct_time,
            msg='Token expiration time stamp format is correct')

        created_time = datetime.fromtimestamp(mktime(ptime_cr))
        exp_time = datetime.fromtimestamp(mktime(ptime_exp))

        delta = (exp_time - created_time)
        oneday = timedelta(days=1)
        self.assertEqual(delta, oneday,
            msg='Token Expiration is 1 day after creation')

    @attr('regression', type='positive')
    def test_revoke_token(self):
        normal_response_codes = [200, 203]
        response_code_revoke = [204]
        auth_resp = self.admin_client.authenticate_password(
            username=self.config.identity_api.username,
            password=self.config.identity_api.password)
        self.assertIn( auth_resp.status_code, normal_response_codes,
            msg= 'Get base URLs expected {0} received {1}'.format(
                normal_response_codes, 
                auth_resp.status_code))
        
        revoke_token = self.admin_client.revoke_token(
            tokenId=auth_resp.entity.token.id)
        self.assertIn( revoke_token.status_code, response_code_revoke,
            msg= 'Get base URLs expected {0} received {1}'.format(
                response_code_revoke, 
                revoke_token.status_code))
        get_token = self.admin_client.get_token(
            tokenId=auth_resp.entity.token.id)
        self.assertEqual(get_token.status_code, 404,
            msg="Response is 404")
        self.assertTrue('{0} not found'.format(
            'Token') in get_token.content,
            msg="Token shouldn't be in the system")

from testrepo.common.testfixtures.identity.v1_1.identity import IdentityFixture
from ccengine.common.decorators import attr
from datetime import datetime, timedelta
from re import match
from time import strptime, struct_time, mktime
from dateutil.parser import parse

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

        self.assertIn(auth_resp.status_code, normal_response_codes,
            msg='Auth response codes expected %s recieved %s' %
            (normal_response_codes, auth_resp.status_code))

        self.assertTrue(auth_resp.entity.token.id is not None,
            msg="Token is present returned %s" % \
            ((auth_resp.entity.token.id is not None)))
        
        if auth_resp.entity.token.id is not None:
            token_length = len(auth_resp.entity.token.id)
            msg = 'Default token length: %s length of returned token %s' % \
                (self.default_token_length, token_length)
            self.assertEqual(token_length, self.default_token_length, msg)
            regex = ''.join(['^([a-zA-Z0-9]+-?)',
                            '([a-zA-Z0-9]+-?)',
                            '([a-zA-Z0-9]+-?)',
                            '([a-zA-Z0-9]+-?)$'])
            valid_token = match(regex, auth_resp.entity.token.id) is not None
            self.assertTrue(valid_token,
                msg='Token contains only valid chars returned %s' % \
                valid_token)
        
        parsed_time = None
        try:                                                               
            parsed_time = parse(auth_resp.entity.token.expires)
            ptime = parsed_time.timetuple()
        except ValueError:
            pass
        
        self.assertIsInstance(ptime, struct_time,
            msg='Token expiration - expected: %s, actual: %s ' % (struct_time,
            ptime))
       
        current_time = self.datetime.now()
        exp_time = datetime.fromtimestamp(mktime(ptime))
        
        delta = (exp_time - current_time)
        
        self.assertGreaterEqual(delta, timedelta(days=0),
            msg='Token Expiration >= Current Time returned %s' %
            (delta >= timedelta(days=0)))

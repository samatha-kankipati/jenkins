from datetime import datetime
from dateutil.parser import parse
from time import mktime

from ccengine.common.decorators import attr
from testrepo.common.testfixtures.identity.v1_0.identity \
    import BaseIdentityFixture


class AuthenticationTest(BaseIdentityFixture):

    @classmethod
    def setUpClass(cls):
        super(AuthenticationTest, cls).setUpClass()
        cls.username = cls.config.identity_api.username
        cls.api_key = cls.config.identity_api.api_key

    @attr('regression', type='positive')
    def test_token_entropy(self):
        """
        Testing token time to live - here we create a series of tokens
        and make sure that the token time to live for all the created tokens
        is not same and falls within a range (check config file for range)

        """
        normal_response_codes = [200, 204]
        response_code_revoke = [204]
        auth_resp = self.client.authenticate(
            x_auth_user=self.username,
            x_auth_key=self.api_key)
        self.assertIn(
            auth_resp.status_code,
            normal_response_codes,
            msg="Get base URLs expected {0} received {1}".format(
                normal_response_codes,
                auth_resp.status_code))
        revoke_token = self.admin_client_v1_1.revoke_token(
            tokenId=auth_resp.entity.x_auth_token)
        self.assertIn(
            revoke_token.status_code,
            response_code_revoke,
            msg='Auth response codes expected {0} recieved {1}'.format(
                response_code_revoke,
                auth_resp.status_code))

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

            auth_resp = self.client.authenticate(
                x_auth_user=self.username,
                x_auth_key=self.api_key)

            self.assertIn(
                auth_resp.status_code,
                normal_response_codes,
                msg="Get base URLs expected {0} received {1}".format(
                    normal_response_codes,
                    auth_resp.status_code))

            validate_token = self.admin_client_v1_1.validate_token(
                tokenId=auth_resp.entity.x_auth_token)
            self.assertIn(
                validate_token.status_code,
                normal_response_codes,
                msg='Get base URLs expected {0} received {1}'.format(
                    normal_response_codes,
                    validate_token.status_code))

            """
            calculates the delta value using token creation and expiration
            time from v1.1 validate token response
            """
            parsed_time_exp = None
            parsed_time_cr = None
            parsed_time_exp = parse(validate_token.entity.expires)
            ptime_exp = parsed_time_exp.timetuple()
            parsed_time_cr = parse(validate_token.entity.created)
            ptime_cr = parsed_time_cr.timetuple()

            created_time = datetime.fromtimestamp(mktime(ptime_cr))
            exp_time = datetime.fromtimestamp(mktime(ptime_exp))
            delta = abs(exp_time - created_time).total_seconds()

            self.assertTrue(
                token_exp_low <= delta <= token_exp_upper,
                msg="Token is out of Cloud Token Time to live range")

            revoke_token = self.admin_client_v1_1.revoke_token(
                tokenId=auth_resp.entity.x_auth_token)
            self.assertIn(
                revoke_token.status_code,
                response_code_revoke,
                msg='Auth response codes expected {0} recieved {1}'.format(
                    response_code_revoke,
                    auth_resp.status_code))

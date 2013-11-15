from dateutil.parser import parse
from dateutil import tz
from datetime import datetime
from time import mktime
import math
import time

from ccengine.common.decorators import attr
from ccengine.common.tools.datagen import rand_name, random_int
from testrepo.common.testfixtures.identity.v1_1.identity \
    import IdentityFixture
from testrepo.common.testfixtures.identity.v2_0.identity \
    import BaseIdentityFixture


class RaxTokenEntropyTest(BaseIdentityFixture, IdentityFixture):

    assert_msg = "Expected response code {0} actual {1}"
    min_expire_in = 100
    imp_racker_token_ttl = 10800
    imp_admin_token_ttl = 40000
    iterations = 3

    @classmethod
    def setUpClass(cls):
        super(RaxTokenEntropyTest, cls).setUpClass()

        cls.apiKey = "1234567890"
        cls.racker_username = cls.config.identity_api.racker_username
        cls.racker_password = cls.config.identity_api.racker_password
        cls.admin_username = cls.config.identity_api.admin_username
        cls.admin_password = cls.config.identity_api.admin_password
        cls.token_entropy = cls.config.identity_api.token_entropy
        cls.cloud_token_ttl = cls.config.identity_api.cloud_token_ttl
        cls.impersonation_token_ttl = cls.config.identity_api. \
            impersonation_token_ttl

        cls.serv_admin_name = cls.config.identity_api.service_username
        cls.serv_admin_password = cls.config.identity_api.service_password
        get_service_info = cls.service_client.get_user_by_name(
            name=cls.serv_admin_name)
        cls.serv_adm_id = get_service_info.entity.id

        cls.auth_iden_adm_resp = cls.admin_client.authenticate_user_password(
            cls.admin_username,
            cls.admin_password)
        cls.admin_client.token = cls.auth_iden_adm_resp.entity.token.id

        domain_id = random_int(10000, 1000000)
        cls.user_admin_username = rand_name("ccuseradmin")
        cls.user_admin_password = "Password1"
        user_admin_email = "{0}@{1}".format(cls.user_admin_username,
                                            "mailtrust.com")
        cls.create_user_admin_resp = cls.admin_client.add_user(
            username=cls.user_admin_username, password=cls.user_admin_password,
            email=user_admin_email, enabled=True, domain_id=domain_id)
        cls.user_adm_id = cls.create_user_admin_resp.entity.id
        cls.auth_user_adm_resp = cls.public_client.authenticate_user_password(
            cls.user_admin_username,
            cls.user_admin_password)

        cls.service_client.update_user_credentials(
            user_id=cls.user_adm_id,
            username=cls.user_admin_username,
            api_key=cls.apiKey)
        cls.to_zone = tz.gettz('America/Chicago')

    @classmethod
    def tearDownClass(cls):
        del cls.auth_user_adm_resp.entity.token.id
        cls.admin_client.delete_user(
            user_id=cls.user_adm_id)
        cls.service_client.delete_user_hard(
            user_id=cls.user_adm_id)

    @attr('regression', type='positive')
    def test_auth_new_token_expiration(self):
        """
        Test to verify the token expiration time varies in the range of 1% of
        total expiry time when authenticate with user name, password and apiKey

        """
        for _ in range(self.iterations):
            '''
            Iterating to verify the expiry time of the token varies
            based on the entropy value
            '''
            identity_admin_token = self._auth_admin_authentication()
            validate_token_v2 = self.admin_client.validate_token(
                token_id=identity_admin_token.token.id)
            validate_token_v1 = self.admin_client_v11.validate_token(
                token_id=identity_admin_token.token.id)
            self.assertEquals(self.auth_iden_adm_resp.status_code,
                              200,
                              self.assert_msg.
                              format(200,
                                     self.auth_iden_adm_resp.status_code))
            self.assertTrue(identity_admin_token.token.expires ==
                            validate_token_v2.entity.token.expires ==
                            validate_token_v1.entity.expires,
                            msg="Token expiry is not same")
            created_times = []

            for _ in range(self.iterations):
                auth_apikey_usr_adm_resp = self.service_client. \
                    authenticate_user_apikey(self.user_admin_username,
                                             self.apiKey)
                validate_token_apikey_v2 = (self.admin_client.validate_token(
                    token_id=auth_apikey_usr_adm_resp.entity.token.id))
                validate_token_apikey_v1 = self.admin_client_v11. \
                    validate_token(
                        token_id=auth_apikey_usr_adm_resp.entity.token.id)
                self.assertEquals(auth_apikey_usr_adm_resp.status_code,
                                  200,
                                  self.assert_msg.format(
                                      200,
                                      auth_apikey_usr_adm_resp.status_code))
                self.assertTrue(
                    auth_apikey_usr_adm_resp.entity.token.expires ==
                    validate_token_apikey_v2.entity.token.expires ==
                    validate_token_apikey_v1.entity.expires,
                    msg="Token expiry is not same")

                user_adm_auth_current_time = datetime.now().replace(
                    tzinfo=self.to_zone)
                token_expire_time = parse(
                    auth_apikey_usr_adm_resp.entity.token.expires)
                self._get_floor_and_ceil_token_ttl_delta(
                    user_adm_auth_current_time,
                    token_expire_time,
                    self.cloud_token_ttl)

                token_exp_upper = (float(self.cloud_token_ttl) *
                                  (1 + float(self.token_entropy) / 100))
                token_exp_low = (float(self.cloud_token_ttl) *
                                (1 - float(self.token_entropy) / 100))
                delta = self.get_token_ttl_delta(validate_token_apikey_v1)
                self.assertTrue(
                    token_exp_low <= delta <= token_exp_upper,
                    msg="Token is out of Cloud Token Time to live range")

            test_values = {self.service_client:
                           [identity_admin_token.token.id,
                            auth_apikey_usr_adm_resp.entity.token.id]}

            self.assertTrue(self._all_same(created_times),
                            msg='All created times are not equal!!')

            client_keys = test_values.keys()
            for client in client_keys:
                token_id_list = test_values[client]
                for token_id in token_id_list:
                    revoke_resp = client.revoke_token(token_id)
                    self.assertEquals(revoke_resp.status_code,
                                      204,
                                      self.assert_msg.
                                      format(204, revoke_resp.status_code))

    @attr('regression', type='positive')
    def test_racker_auth(self):
        """
        Test to verify the token expiration time varies in the range of 1% of
        total expiry time when authenticate a racker
        """
        identity_admin_token = self._auth_admin_authentication()
        self.admin_client.token = identity_admin_token.token.id

        racker_token = self._racker_authentication()
        validate_racker_token = self.admin_client.validate_token(
            token_id=racker_token.token.id)
        self.assertEquals(validate_racker_token.status_code,
                          200,
                          self.assert_msg.
                          format(200, validate_racker_token.status_code))

        revoke_resp = self.service_client.revoke_token(racker_token.token.id)
        self.assertEquals(revoke_resp.status_code,
                          204,
                          self.assert_msg.
                          format(204, revoke_resp.status_code))
        for _ in range(self.iterations):
            racker_token = self._racker_authentication()
            racker_auth_current_time = datetime.now(). \
                replace(tzinfo=self.to_zone)
            racker_auth_expire_time = parse(racker_token.token.expires)
            self._get_floor_and_ceil_token_ttl_delta(
                racker_auth_current_time,
                racker_auth_expire_time,
                self.cloud_token_ttl)

            revoke_resp = self.service_client.revoke_token(
                racker_token.token.id)

    @attr('regression', type='positive')
    def test_racker_impersonation_user_admin(self):
        """
        Test to verify the token expiration time varies in the range of 1% of
        total expiry time when impersonate user admin as a racker
        """
        for _ in range(self.iterations):
            identity_admin_token = self._auth_admin_authentication()
            self.admin_client.token = identity_admin_token.token.id

            racker_token = self._racker_authentication()
            self.racker_client.token = racker_token.token.id

            rac_impersonate_usr_adm = self.racker_client.impersonate_user(
                username=self.config.identity_api.username)
            validate_imp_racker_token_v2 = self.admin_client.validate_token(
                token_id=rac_impersonate_usr_adm.entity.token.id)
            validate_imp_racker_token_v1 = \
                self.admin_client_v11.validate_token(
                    token_id=rac_impersonate_usr_adm.entity.token.id)
            self._verify_token_details(rac_impersonate_usr_adm,
                                       validate_imp_racker_token_v1,
                                       validate_imp_racker_token_v2,
                                       self.impersonation_token_ttl)
            self._revoke_token(rac_impersonate_usr_adm.entity.token.id)

    @attr('regression', type='positive')
    def test_admin_impersonation_user_admin(self):
        """
        Test to verify the token expiration time varies in the range of 1% of
        total expiry time when impersonate useradmin as an admin
        """
        for _ in range(self.iterations):
            adm_impersonate_usr_adm = self.admin_client.impersonate_user(
                username=self.config.identity_api.username)
            validate_imp_admin_token_v2 = self.admin_client.validate_token(
                token_id=adm_impersonate_usr_adm.entity.token.id)
            validate_imp_admin_token_v1 = self.admin_client_v11.validate_token(
                token_id=adm_impersonate_usr_adm.entity.token.id)

            self._verify_token_details(adm_impersonate_usr_adm,
                                       validate_imp_admin_token_v1,
                                       validate_imp_admin_token_v2,
                                       self.impersonation_token_ttl)
            self._revoke_token(adm_impersonate_usr_adm.entity.token.id)

    @attr('regression', type='positive')
    def test_racker_impersonation_user_admin_expire_in(self):
        """
        Test to verify the token expiration time varies in the range 1% of
        total expiry time when impersonate useradmin as a racker with expire in
        """
        for _ in range(self.iterations):
            racker_token = self._racker_authentication()
            self.racker_client.token = racker_token.token.id

            rac_imper_usr_adm_exp_in = self.racker_client. \
                impersonate_user_expire_in(
                    username=self.config.identity_api.username,
                    expire_in_seconds=self.imp_racker_token_ttl)

            validate_imp_racker_token_v2 = self.admin_client.validate_token(
                token_id=rac_imper_usr_adm_exp_in.entity.token.id)
            validate_imp_racker_token_v1 = self.admin_client_v11. \
                validate_token(token_id=
                               rac_imper_usr_adm_exp_in.entity.token.id)
            self._verify_token_details(rac_imper_usr_adm_exp_in,
                                       validate_imp_racker_token_v1,
                                       validate_imp_racker_token_v2,
                                       self.imp_racker_token_ttl)
            self._revoke_token(rac_imper_usr_adm_exp_in.entity.token.id)

    @attr('regression', type='positive')
    def test_admin_impersonation_user_admin_expire_in(self):
        """
        Test to verify the token expiration time varies in the range of 1% of
        total expiry time when impersonate useradmin as an admin with expire in
        """
        for expiry_time in [self.min_expire_in, self.imp_admin_token_ttl]:

            adm_impersonate_usr_adm_exp_in = self.admin_client. \
                impersonate_user_expire_in(
                    username=self.config.identity_api.username,
                    expire_in_seconds=expiry_time)
            validate_imp_admin_token_v2 = self.admin_client.validate_token(
                token_id=adm_impersonate_usr_adm_exp_in.entity.token.id)
            validate_imp_exp_admin_token_v1 = \
                self.admin_client_v11.validate_token(
                    token_id=adm_impersonate_usr_adm_exp_in.entity.token.id)
            self._verify_token_details(adm_impersonate_usr_adm_exp_in,
                                       validate_imp_exp_admin_token_v1,
                                       validate_imp_admin_token_v2,
                                       expiry_time)
            time.sleep(self.min_expire_in + 5)
        self._revoke_token(adm_impersonate_usr_adm_exp_in.entity.token.id)

    def _verify_token_details(self,
                              impersonation_entity,
                              validate_token_v1,
                              validate_token_v2,
                              token_ttl):
        """
        Verifies the response codes of authentication and calls
        _get_floor_and_ceil_token_ttl_delta to calculate the entropy
        @param impersonation_entity: The response of impersonate a user
        @param validate_token_v1: Response of validate token in 1.1
        @param validate_token_v2: Response of validate token in 2.0
        @param token_ttl: Entropy value
        """
        self.assertEqual(impersonation_entity.status_code,
                         200,
                         self.assert_msg.format(
                             200,
                             impersonation_entity.status_code))
        self.assertTrue(
            impersonation_entity.entity.token.expires ==
            validate_token_v2.entity.token.expires ==
            validate_token_v1.entity.expires,
            msg="Token expiry is not same")
        system_time_just_before_authentication = \
            datetime.now().replace(tzinfo=self.to_zone)
        imp_token_expires = parse(impersonation_entity.entity.token.expires)
        self._get_floor_and_ceil_token_ttl_delta(
            system_time_just_before_authentication,
            imp_token_expires,
            token_ttl)

        imp_created_time_v1 = parse(validate_token_v1.entity.created)
        self._get_floor_and_ceil_token_ttl_delta(
            imp_created_time_v1,
            imp_token_expires,
            token_ttl)

    def _revoke_token(self, token_id):
        revoke_resp = self.service_client.revoke_token(token_id)
        self.assertEquals(revoke_resp.status_code,
                          204,
                          self.assert_msg.
                          format(204, revoke_resp.status_code))

    def _get_floor_and_ceil_token_ttl_delta(self,
                                            created_time,
                                            expiry_time,
                                            token_ttl):
        """
        Returns token time to live, calculates the delta value using current
        time, token creation and expiration time from v1.1 validate token
        response
        @param created_time: current time and V1.1 validate token created time
        @param expiry_time: V1.1 validate token expiry time
        @param token_ttl: token entropy value
        """
        created_time_tuple = created_time.utctimetuple()
        created_time_in_seconds = mktime(created_time_tuple)

        expiry_time_tuple = expiry_time.utctimetuple()
        expiry_time_in_seconds = mktime(expiry_time_tuple)

        delta = (expiry_time_in_seconds - created_time_in_seconds) / 3600

        token_expiry_low = math.floor(float(token_ttl) *
                                     (1 - float(self.token_entropy)) / 3600)
        token_expiry_upper = math.ceil(float(token_ttl) *
                                      (1 + float(self.token_entropy)) / 3600)
        self.assertTrue(
            token_expiry_low <= delta <= token_expiry_upper,
            msg="Token is out of Cloud Token Time to live range")

    def _all_same(self, created_times):
        '''
        Determines if all created_times of a list are the same
        '''
        return all(x == created_times[0] for x in created_times)

    def _racker_authentication(self):
        '''
        Authenticate Racker
        '''
        rac_auth_resp = self.racker_client.authenticate_racker(
            self.racker_username,
            self.racker_password)
        self.assertEqual(rac_auth_resp.status_code,
                         200,
                         self.assert_msg.format(200,
                                                rac_auth_resp.status_code))
        return rac_auth_resp.entity

    def _auth_admin_authentication(self):
        '''
        Authenticate Identity Admin
        '''
        self.auth_iden_adm_resp = self.admin_client. \
            authenticate_user_password(self.admin_username,
                                       self.admin_password)
        self.admin_client.token = self.auth_iden_adm_resp.entity.token.id
        self.assertEqual(self.auth_iden_adm_resp.status_code,
                         200,
                         self.assert_msg.format(
                             200,
                             self.auth_iden_adm_resp.status_code))
        return self.auth_iden_adm_resp.entity

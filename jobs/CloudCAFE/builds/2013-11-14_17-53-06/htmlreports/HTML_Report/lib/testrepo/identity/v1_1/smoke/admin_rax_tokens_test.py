from datetime import datetime

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

    @classmethod
    def tearDownClass(cls):
        get_user = cls.admin_client_vsec.get_user_by_name(name=cls.uid)
        cls.admin_client.delete_user(user_id=cls.create_user.entity.id)
        cls.service_client.delete_user_hard(get_user.entity.id)

    @attr('smoke', type='positive')
    def test_mosso_authentication(self):
        """
        Test to verify Authentication with mossoid and key response

        """
        normal_response_codes = [200, 203]
        auth_resp = self.admin_client.authenticate_mosso(
            mosso_id=self.mosso_id,
            key=self.key)
        self.assertIn(
            auth_resp.status_code, normal_response_codes,
            msg=("Auth response expected {0} received {1}".format(
                normal_response_codes, auth_resp.status_code)))

    @attr('smoke', type='positive')
    def test_nast_authentication(self):
        """
        Test to verify Authentication with nastid and key response

        """
        normal_response_codes = [200, 203]
        auth_resp = self.admin_client.authenticate_nast(
            nast_id=self.create_user.entity.nastId,
            key=self.key)
        self.assertIn(
            auth_resp.status_code, normal_response_codes,
            msg=("Auth response expected {0} received {1}".format(
                normal_response_codes, auth_resp.status_code)))

    @attr('smoke', type='positive')
    def test_password_authentication(self):
        """
        Test to verify authentication using password response

        """
        normal_response_codes = [200, 203]
        auth_resp = self.admin_client.authenticate_password(
            username=self.uid,
            password=self.password)
        self.assertIn(
            auth_resp.status_code, normal_response_codes,
            msg=("Auth response expected {0} received {1}".format(
                normal_response_codes, auth_resp.status_code)))

    @attr('smoke', type='positive')
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

        get_token = self.admin_client.get_token(
            token_id=auth_resp.entity.token.id)
        self.assertIn(
            get_token.status_code, normal_response_codes,
            msg="Get token response code expected {0} recieved {1}".format(
                normal_response_codes, auth_resp.status_code))

    @attr('smoke', type='positive')
    def test_validate_token(self):
        """
        Test to verify validate token response

        """
        normal_response_codes = [200, 203]
        auth_resp = self.admin_client.authenticate_password(
            username=self.uid,
            password=self.password)
        self.assertIn(
            auth_resp.status_code, normal_response_codes,
            msg=("Auth response expected {0} received {1}".format(
                normal_response_codes, auth_resp.status_code)))

        validate_token = self.admin_client.validate_token(
            token_id=auth_resp.entity.token.id)
        self.assertIn(
            validate_token.status_code, normal_response_codes,
            msg=("Validate token response expected {0} recieved {1}".format(
                normal_response_codes, auth_resp.status_code)))

    @attr('smoke', type='positive')
    def test_revoke_token(self):
        """
        Test to verify revoke token response

        """
        normal_response_codes = [200, 203]
        response_code_revoke = [204]
        auth_resp = self.admin_client.authenticate_password(
            username=self.uid,
            password=self.password)
        self.assertIn(
            auth_resp.status_code, normal_response_codes,
            msg=("Auth response expected {0} received {1}".format(
                normal_response_codes, auth_resp.status_code)))

        revoke_token = self.admin_client.revoke_token(
            token_id=auth_resp.entity.token.id)
        self.assertIn(
            revoke_token.status_code, response_code_revoke,
            msg=("Revoke response codes expected {0} recieved {1}".format(
                response_code_revoke, auth_resp.status_code)))

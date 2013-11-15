from testrepo.common.testfixtures.identity.v1_1.identity import IdentityFixture
from ccengine.common.decorators import attr
from datetime import datetime, timedelta
from time import strptime, struct_time, mktime

class AdminTokenTest(IdentityFixture):

    @classmethod
    def setUpClass(cls):
        super(AdminTokenTest, cls).setUpClass()
        cls.datetime = datetime

    @classmethod
    def tearDownClass(cls):
        pass

    @attr('smoke', type='positive')
    def test_mosso_authentication(self):
        normal_response_codes = [200, 203]
        auth_resp = self.admin_client.authenticate_mosso(
            mossoId=self.config.identity_api.mosso_Id,
            key=self.config.identity_api.mosso_key)

        self.assertIn(auth_resp.status_code, normal_response_codes,
            msg='Auth response codes expected %s recieved %s' %
            (normal_response_codes, auth_resp.status_code))
    
    @attr('smoke', type='positive')
    def test_nast_authentication(self):
        normal_response_codes = [200, 203]
        auth_resp = self.admin_client.authenticate_nast(
            nastId=self.config.identity_api.nast_Id,
            key=self.config.identity_api.nast_key)

        self.assertIn(auth_resp.status_code, normal_response_codes,
            msg='Auth response codes expected %s recieved %s' %
            (normal_response_codes, auth_resp.status_code))
    
    @attr('smoke', type='positive')
    def test_password_authentication(self):
        normal_response_codes = [200, 203]
        auth_resp = self.admin_client.authenticate_password(
            username=self.config.identity_api.username,
            password=self.config.identity_api.password)

        self.assertIn(auth_resp.status_code, normal_response_codes,
            msg='Auth response codes expected %s recieved %s' %
            (normal_response_codes, auth_resp.status_code))
    
    @attr('smoke', type='positive')
    def test_get_token(self):
        normal_response_codes = [200, 203]
        auth_resp = self.admin_client.authenticate_password(
            username=self.config.identity_api.username,
            password=self.config.identity_api.password)
        self.assertIn(auth_resp.status_code, normal_response_codes,
            msg='Auth response codes expected %s recieved %s' %
            (normal_response_codes, auth_resp.status_code))
        
        get_token = self.admin_client.get_token(
            tokenId=auth_resp.entity.token.id)
        self.assertIn(get_token.status_code, normal_response_codes,
            msg='Auth response codes expected %s recieved %s' %
            (normal_response_codes, auth_resp.status_code))
    
    @attr('smoke', type='positive')
    def test_validate_token(self):
        normal_response_codes = [200, 203]
        auth_resp = self.admin_client.authenticate_password(
            username=self.config.identity_api.username,
            password=self.config.identity_api.password)
        self.assertIn(auth_resp.status_code, normal_response_codes,
            msg='Auth response codes expected %s recieved %s' %
            (normal_response_codes, auth_resp.status_code))
        
        validate_token = self.admin_client.validate_token(
            tokenId=auth_resp.entity.token.id)
        self.assertIn(validate_token.status_code, normal_response_codes,
            msg='Auth response codes expected %s recieved %s' %
            (normal_response_codes, auth_resp.status_code))
    
    @attr('smoke', type='positive')
    def test_revoke_token(self):
        normal_response_codes = [200, 203]
        response_code_revoke = [204]
        auth_resp = self.admin_client.authenticate_password(
            username=self.config.identity_api.username,
            password=self.config.identity_api.password)
        self.assertIn(auth_resp.status_code, normal_response_codes,
            msg='Auth response codes expected %s recieved %s' %
            (normal_response_codes, auth_resp.status_code))
        
        revoke_token = self.admin_client.revoke_token(
            tokenId=auth_resp.entity.token.id)
        self.assertIn(revoke_token.status_code, response_code_revoke,
            msg='Auth response codes expected %s recieved %s' %
            (response_code_revoke, auth_resp.status_code))

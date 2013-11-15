from testrepo.common.testfixtures.rax_signup import RaxSignupAPI_BaseFixture


class RaxSignupAPI_HeartbeatTest(RaxSignupAPI_BaseFixture):

    def test_is_rax_signup_api_responding(self):
        resp = self.client.signup_new_cloud_customer()
        assert resp is not None, "RaxSignUp API is not responding"

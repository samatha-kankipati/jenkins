from testrepo.common.testfixtures.rax_signup import\
        RaxSignupAPI_CloudSignupFixture
from ccengine.common.connectors.rest import RestConnector


class RaxSignupAPI_CloudSignupRequest_PositiveSmoke(
        RaxSignupAPI_CloudSignupFixture):

    def test_cloud_signup_request_default(self):
        '''
        Scenario: Create Account using Cloud SignUp Facade with all necessary
        details
        '''

        metadata = [
            {"key": "cloudSitesPurchased",
            "value": "false"},
            {"key": "cloudFilesPurchased",
            "value": "true"},
            {"key": "cloudServersPurchased",
            "value": "true"},
            {"key": "loadBalancersPurchased",
            "value": "false"},
            {"key": "ipAddress",
            "value": "10.186.932.145"},
            {"key": "rackUID",
            "value": "277298293"},
            {"key": "deviceFingerPrint",
            "value": "134.288-8901"}, ]

        default_order_item = {
            'offering_id': 'CLOUD_SITES',
            'product_id': 'CLOUD_SITES',
            'quantity': '1',
            }

        request_dict = self.get_signup_request_dict(
                metadata=metadata, default_order_item=default_order_item)

        api_response = self.client.signup_new_cloud_customer(**request_dict)
        username = api_response.request.entity.contacts[0].user.username
        password = api_response.request.entity.contacts[0].user.password
        user_id = api_response.entity.id_
        self.assertDefaultResponseOK(api_response)
        
        conn = RestConnector()
        body = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ns="http://cloud.rackspace.com/account/1.0">
                   <soapenv:Header/>
                   <soapenv:Body>
                      <ns:UpdateAccountStatus>
                         <ns:accountId>{0}</ns:accountId>
                         <ns:accountStatus>ACTIVE</ns:accountStatus>
                      </ns:UpdateAccountStatus>
                   </soapenv:Body>
                </soapenv:Envelope>""".format(user_id)
        response = conn.post("http://smix.staging.us.ccp.rackspace.net/account/1.0", body)
        self.assertEqual(200, response.status_code)

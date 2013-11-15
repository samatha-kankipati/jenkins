'''
Created on Mar 14, 2013

@author: vara.chinnappareddy
'''

from testrepo.common.testfixtures.rax_signup import\
        RaxSignupAPI_CloudSignupFixture
from ccengine.common.connectors.rest import RestConnector
from ccengine.providers.identity.identity_v2_0_api import IdentityAPIProvider
from ccengine.domain.configuration import IdentityAPIConfig

import json


class TestMonitor(RaxSignupAPI_CloudSignupFixture):

    def test_monitor(self):
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
        conn.post("http://smix.staging.us.ccp.rackspace.net/account/1.0", body)
        ah_dict = {IdentityAPIConfig.SECTION_NAME: {'username': username,
                                                    'api_key': '',
                                                    'password': password}}
        self.config = self.config.mcp_override(ah_dict)
        self.identity_provider = IdentityAPIProvider(self.config)
        auth_data = self.identity_provider.authenticate().entity
        token_id = self.identity_provider.authenticate().entity.token.id
        self.url1 = """https://staging.monitoring.api.rackspacecloud.com/v1.0/{0}/entities""".format(user_id)
        conn1 = RestConnector()
        entbody = """{
                    "label": "Brand New Entity",
                    "ip_addresses": {
                        "default": "50.56.235.33"
                    },
                   "metadata": {
                                "all": "kinds",
                                "of": "stuff",
                                "can": "go",
                                "here": "null is not a valid value"
                                }
                    }"""
        entityresp = conn1.post(self.url1, entbody,
                                headers={'Content-type': 'application/json',
                                         'X-Auth-Token': token_id})
        self.entityurl = entityresp.headers.get('location') + '/checks'
        checkbody = """{
                        "label": "testVara",
                        "type": "remote.http",
                        "details": {
                        "url": "http://www.foo.com",
                        "method": "GET"
                        },
                     "monitoring_zones_poll": [
                     "mzdfw"
                        ],
                     "timeout": 30,
                     "period": 100,
                     "target_alias": "default"
                    }
                """
        conn1.post(self.entityurl, checkbody,
                   headers={'Content-type': 'application/json',
                            'X-Auth-Token': token_id})
        checkresp = conn1.get(self.entityurl,
                headers={'Content-type': 'application/json',
                         'X-Auth-Token': token_id})
        status = checkresp.status_code
        strtojson = json.loads(checkresp.content)
        checkid = strtojson['values'][0]['id']
        self.assertEqual(200, status, '200 response code returned')
        self.assertIsNotNone(checkid, 'check id is returned')

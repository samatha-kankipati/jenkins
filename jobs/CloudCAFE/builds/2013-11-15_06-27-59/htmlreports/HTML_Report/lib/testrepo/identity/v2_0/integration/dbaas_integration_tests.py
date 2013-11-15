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


class Create_DBInstance(RaxSignupAPI_CloudSignupFixture):

    def test_create_dbinstance(self):
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
        ah_dict = {IdentityAPIConfig.SECTION_NAME: {'username': username,
                            'api_key': '', 'password': password}}
        self.config = self.config.mcp_override(ah_dict)
        self.identity_provider = IdentityAPIProvider(self.config)
        token_id = self.identity_provider.authenticate().entity.token.id
        dbapi_baseurl = 'https://api.staging.ord1.clouddb.rackspace.net/v1.0'
        self.url1 = """{0}/{1}/instances""".format(dbapi_baseurl, user_id)
        entbody = """{
                        "instance": {
                            "databases": [
                                {
                                    "character_set": "utf8",
                                    "collate": "utf8_general_ci",
                                    "name": "sampledb"
                                },
                        {
                            "name": "nextround"
                        }
                                        ],
                        "flavorRef": "https://ord.databases.api.rackspacecloud.com/v1.0/1234/flavors/1",
                        "name": "json_rack_instance3",
                        "users": [
                                {
                                "databases": [
                                    {
                                        "name": "sampledb"
                                    }
                                ],
                                "name": "demouser",
                                "password": "demopassword"
                            }
                        ],
                        "volume": {
                        "size": 2
                            }
                        }
                    }"""
        entity_resp = conn.post(self.url1, entbody,
                                headers={'Content-type': 'application/json',
                                         'Accept': 'application/json',
                                         'X-Auth-Token': token_id})
        str_to_json = json.loads(entity_resp.content)
        instance_id = str_to_json['instance']['id']

        self.assertEquals(entity_resp.status_code, 200,
                          'create response code is 200 OK')
        self.assertTrue(instance_id is not None,
                        'database instance id is created')

        db_inst_url = """{0}/{1}/instances/{2}""".format(dbapi_baseurl, user_id,
                                                str_to_json['instance']['id'])
        status = 'BUILD'
        while (status != 'ACTIVE'):
            db_inst_resp = conn.get(db_inst_url,
                                  headers={'Content-type': 'application/json',
                                           'Accept': 'application/json',
                                           'X-Auth-Token': token_id})
            self.assertEquals(db_inst_resp.status_code, 200,
                              'get response code is 200 OK')
            str_to_json_1 = json.loads(db_inst_resp.content)
            status = str_to_json_1['instance']['status']

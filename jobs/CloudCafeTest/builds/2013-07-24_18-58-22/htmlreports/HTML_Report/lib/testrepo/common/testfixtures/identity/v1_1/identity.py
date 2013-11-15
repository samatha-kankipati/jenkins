'''
@summary: Base Classes for Test Suites (Collections of Test Cases)
@note: Correspondes DIRECTLY TO A unittest.TestCase
@see: http://docs.python.org/library/unittest.html#unittest.TestCase
@copyright: Copyright (c) 2012 Rackspace US, Inc.
'''
from testrepo.common.testfixtures.fixtures import BaseTestFixture
from ccengine.clients.identity.v1_1.rax_auth_api import IdentityClient
from ccengine.clients.identity.v1_1.rax_auth_admin_api \
    import IdentityAdminClient
from ccengine.clients.identity.v2_0.rax_auth_admin_api \
    import IdentityAdminClient as IdentityAdminClientvSec
from ccengine.clients.identity.v2_0.rax_auth_service_api \
    import IdentityServiceClient


class IdentityFixture(BaseTestFixture):
    '''
    @summary: Fixture for an Auth test.
    '''
    @classmethod
    def setUpClass(cls):
        super(IdentityFixture, cls).setUpClass()
        endpoint = cls.config.identity_api.authentication_endpoint
        ser_format = cls.config.misc.serializer
        deser_format = cls.config.misc.deserializer
        cls.client = IdentityClient(authentication_endpoint=endpoint,
            serialize_format=ser_format, deserialize_format=deser_format)
        admin_user = cls.config.identity_api.admin_username
        admin_password = cls.config.identity_api.admin_password
        cls.admin_client = IdentityAdminClient(url=endpoint,
                                               user=admin_user,
                                               password=admin_password,
                                               serialize_format=ser_format)
        'v2_0:Identity:Admin part'
        admin_auth_vsec = cls.admin_client.\
            authenticate_password(username=admin_user,
                                  password=admin_password).entity
        cls.admin_client_vsec = IdentityAdminClientvSec(
                                               url=endpoint,
                                               serialize_format=ser_format)
        cls.admin_client_vsec.token = admin_auth_vsec.token.id
        'v2_0:Service:Admin part'
        service_username = cls.config.identity_api.service_username
        service_password = cls.config.identity_api.service_password
        service_auth = cls.admin_client.\
            authenticate_password(username=service_username,
                                  password=service_password).entity
        cls.service_client = IdentityServiceClient(url=endpoint,
                                                   serialize_format=ser_format)
        cls.service_client.token = service_auth.token.id

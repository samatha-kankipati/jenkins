'''
@summary: Base Classes for Test Suites (Collections of Test Cases)
@note: Correspondes DIRECTLY TO A unittest.TestCase
@see: http://docs.python.org/library/unittest.html#unittest.TestCase
@copyright: Copyright (c) 2012 Rackspace US, Inc.
'''
from datetime import datetime
from dateutil.parser import parse
from time import struct_time, mktime

from ccengine.clients.identity.v1_1.rax_auth_admin_api \
    import IdentityAdminClient
from ccengine.clients.identity.v1_1.rax_auth_api import IdentityClient
from ccengine.clients.identity.v2_0.rax_auth_admin_api \
    import IdentityAdminClient as IdentityAdminClientvSec
from ccengine.clients.identity.v2_0.rax_auth_service_api \
    import IdentityServiceClient
from testrepo.common.testfixtures.fixtures import BaseTestFixture


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

        cls.client = IdentityClient(
            authentication_endpoint=endpoint,
            serialize_format=ser_format,
            deserialize_format=deser_format)

        cls.client = IdentityClient(authentication_endpoint=endpoint,
                                    serialize_format=ser_format,
                                    deserialize_format=deser_format)

        admin_user = cls.config.identity_api.admin_username
        admin_password = cls.config.identity_api.admin_password
        cls.admin_client = IdentityAdminClient(url=endpoint,
                                               user=admin_user,
                                               password=admin_password,
                                               serialize_format=ser_format)
        '''
        Need admin_client_v1 to avoid name conflict in case we inherit \
        both V1 & V2 IdentityClient classes
        '''
        cls.admin_client_v1 = IdentityAdminClient(
            url=endpoint,
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

    def get_token_ttl_delta(self, token_resp):
        """
        Returns token time to live, calculates the delta value using token
        creation and expiration time from v1.1 validate token response
        @param: V1.1 validate token response object
        @returns: delta value in secs

        """
        parsed_time_exp = None
        parsed_time_cr = None
        parsed_time_exp = parse(token_resp.entity.expires)
        ptime_exp = parsed_time_exp.timetuple()
        parsed_time_cr = parse(token_resp.entity.created)
        ptime_cr = parsed_time_cr.timetuple()

        self.assertIsInstance(
            ptime_exp,
            struct_time,
            msg='Token expiration time stamp format is In-correct')
        self.assertIsInstance(
            ptime_cr,
            struct_time,
            msg='Token expiration time stamp format is In-correct')

        created_time = datetime.fromtimestamp(mktime(ptime_cr))
        exp_time = datetime.fromtimestamp(mktime(ptime_exp))
        delta = abs(exp_time - created_time).total_seconds()

        return delta

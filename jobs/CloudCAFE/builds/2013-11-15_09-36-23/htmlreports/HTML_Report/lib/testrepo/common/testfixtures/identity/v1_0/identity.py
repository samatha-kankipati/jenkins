from testrepo.common.testfixtures.fixtures import BaseTestFixture
from ccengine.clients.identity.v1_0.identity_api import IdentityClient
from ccengine.clients.identity.v1_1.rax_auth_admin_api \
    import IdentityAdminClient


class BaseIdentityFixture(BaseTestFixture):

    @classmethod
    def setUpClass(cls):
        super(BaseIdentityFixture, cls).setUpClass()
        url = cls.config.identity_api.authentication_endpoint
        cls.client = IdentityClient(url=url)

        endpoint = cls.config.identity_api.authentication_endpoint
        ser_format = cls.config.misc.serializer
        admin_user = cls.config.identity_api.admin_username
        admin_password = cls.config.identity_api.admin_password
        cls.admin_client_v1_1 = IdentityAdminClient(
                url=endpoint,
                user=admin_user,
                password=admin_password,
                serialize_format=ser_format)

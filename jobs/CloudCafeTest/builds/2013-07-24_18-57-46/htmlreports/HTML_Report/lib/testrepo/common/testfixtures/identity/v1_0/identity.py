from testrepo.common.testfixtures.fixtures import BaseTestFixture
from ccengine.clients.identity.v1_0.identity_api import IdentityClient


class BaseIdentityFixture(BaseTestFixture):

    @classmethod
    def setUpClass(cls):
        super(BaseIdentityFixture, cls).setUpClass()
        url = cls.config.identity_api.authentication_endpoint
        cls.client = IdentityClient(url=url)

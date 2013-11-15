from ccengine.providers.encore.encore_api import EncoreAPIProvider
from ccengine.common.resource_manager.resource_pool import ResourcePool
from testrepo.common.testfixtures.fixtures import BaseTestFixture


class EncoreFixture(BaseTestFixture):
    """@summary: Fixture for an EncoreApi test"""

    @classmethod
    def setUpClass(cls):
        super(EncoreFixture, cls).setUpClass()
        cls.resources = ResourcePool()
        cls.encore_provider = EncoreAPIProvider(cls.config, cls.fixture_log)
        cls.encore_client = cls.encore_provider.encore_client

    @classmethod
    def tearDownClass(cls):
        cls.resources.release()
        super(EncoreFixture, cls).tearDownClass()

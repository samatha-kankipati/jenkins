from ccengine.common.resource_manager.resource_pool import ResourcePool
from ccengine.providers.valkyrie.valkyrie_provider import ValkyrieProvider \
    as _ValkyrieProvider
from testrepo.common.testfixtures.fixtures import BaseTestFixture


class ValkyrieFixture(BaseTestFixture):

    @classmethod
    def setUpClass(cls):
        super(ValkyrieFixture, cls).setUpClass()
        cls.resources = ResourcePool()
        cls.valkyrie_provider = _ValkyrieProvider(cls.config, cls.fixture_log)

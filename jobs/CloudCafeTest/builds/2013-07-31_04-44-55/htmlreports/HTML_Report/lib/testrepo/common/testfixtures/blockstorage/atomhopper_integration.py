#from ccengine.common.tools import datagen
from testrepo.common.testfixtures.blockstorage.volumes_api import \
    VolumesAPI_Fixture
from ccengine.providers.atomhopper import AtomHopperProvider


class AtomhopperIntegrationFixture(VolumesAPI_Fixture):
    @classmethod
    def setUpClass(cls):
        super(AtomhopperIntegrationFixture, cls).setUpClass()
        cls.atomhopper_provider = AtomHopperProvider(
            cls.config.volumes_api.atom_feed_url, cls.config)



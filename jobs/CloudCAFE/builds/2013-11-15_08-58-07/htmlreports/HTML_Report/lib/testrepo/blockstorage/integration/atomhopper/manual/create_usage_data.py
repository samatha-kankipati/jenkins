import pickle
from ccengine.common.tools import datagen
from testrepo.common.testfixtures.blockstorage.atomhopper_integration import \
    AtomhopperIntegrationFixture


class VolumesAPI_Usage_Smoke(AtomhopperIntegrationFixture):

    @classmethod
    def setUpClass(cls):
        super(VolumesAPI_Usage_Smoke, cls).setUpClass()

    def test_create_sata_10g_usage(self):
        vinfo = self.volumes_provider.create_available_volume(
            datagen.random_string(prefix='QEUsageIntegrationTest-'), size=10,
            volume_type='SATA')

        assert vinfo is not None, 'Volume created successfully'
        vinfo_picklename = datagen.timestamp_string('./volumepickle')
        fh = open(vinfo_picklename, 'w+')
        pickle.dump(vinfo, fh)
        fh.close()

    def test_create_ssd_10g_usage(self):
        vinfo = self.volumes_provider.create_available_volume(
            datagen.random_string(prefix='QEUsageIntegrationTest-'), size=10,
            volume_type='SSD')

        assert vinfo is not None, 'Volume created successfully'
        vinfo_picklename = datagen.timestamp_string('./volumepickle')
        fh = open(vinfo_picklename, 'w+')
        pickle.dump(vinfo, fh)
        fh.close()

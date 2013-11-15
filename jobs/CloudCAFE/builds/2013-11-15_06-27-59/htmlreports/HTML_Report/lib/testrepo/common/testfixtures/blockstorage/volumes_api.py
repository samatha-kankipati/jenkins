from ccengine.common.tools import datagen
from ccengine.providers.blockstorage.volumes_api import VolumesAPIProvider
from testrepo.common.testfixtures.blockstorage.common import \
    BlockstorageBaseTestFixture


class VolumesAPI_Fixture(BlockstorageBaseTestFixture):
    @classmethod
    def setUpClass(cls):
        super(VolumesAPI_Fixture, cls).setUpClass()
        cls.volumes_provider = VolumesAPIProvider(cls.config)
        cls.volumes_client = cls.volumes_provider.volumes_client

    def setup_volume(
            self, size=None, volume_type_name='SATA', display_name=None,
            add_cleanup=True):

        self.fixture_log.info('Setting up volume')
        size = size or self.config.volumes_api.min_volume_size

        vname = display_name or datagen.timestamp_string(
            'CBSQE_{0}_TestVolume_'.format(volume_type_name))

        resp = self.volumes_provider.create_available_volume(
            vname, size, volume_type_name)

        assert resp.ok, \
            'Volume create failed in setup_server with a {0}'.format(
                resp.status_code)

        assert resp.entity is not None, \
            ("Volume create failed in setup_server: Could not deserialize "
             "volume create response body")

        if add_cleanup:
            self.fixture_log.info('Adding cleanup task for {0}(id={1})'.format(
                display_name, resp.entity.id))
            self.addCleanup(
                self.volumes_provider.delete_volume_confirmed,
                resp.entity.id)

        return resp.entity

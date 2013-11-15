'''
@summary: Lunr API Volume Smoke Tests - Create, List, Get Info, Update, Delete Volume.
@copyright: Copyright (c) 2012 Rackspace US, Inc.
'''
from testrepo.common.testfixtures.blockstorage.compute_integration import \
    ComputeIntegrationFixture


class VolumeAttachmentsAPISmoke(ComputeIntegrationFixture):

    @classmethod
    def setUpClass(cls):
        super(VolumeAttachmentsAPISmoke, cls).setUpClass()
        cls.test_server = cls.setup_class_server()

    def test_auto_attach_ssd(self):
        volume = self.setup_volume(volume_type_name='ssd')

        #Attach volume to server automatically (with cleanup)
        self.auto_attach_volume_to_server(
            self.test_server.id, volume.id, expected_volume_status="in-use")

    def test_auto_attach_sata(self):
        volume = self.setup_volume(volume_type_name='sata')

        #Attach volume to server automatically (with cleanup)
        self.auto_attach_volume_to_server(
            self.test_server.id, volume.id, expected_volume_status="in-use")

    def test_rapidly_auto_attach_both_volume_types(self):
        sata_volume = self.setup_volume(volume_type_name='sata')
        ssd_volume = self.setup_volume(volume_type_name='ssd')

        self.auto_attach_volume_to_server(
            self.test_server.id, sata_volume.id,
            expected_volume_status=False)

        self.auto_attach_volume_to_server(
            self.test_server.id, ssd_volume.id,
            expected_volume_status=False)

        resp = self.volumes_provider.wait_for_volume_status(
            sata_volume.id, expected_status='in-use')
        assert resp.ok, (
            "After requesting an auto-attach for two volumes,"
            "the SATA volume did not reach the in-use state")

        resp = self.volumes_provider.wait_for_volume_status(
            ssd_volume.id, expected_status='in-use')
        assert resp.ok, (
            "After requesting an auto-attach for two volumes,"
            "the SSD volume did not reach the in-use state")

    def test_explicit_attach_ssd(self):
        volume = self.setup_volume(volume_type_name='ssd')
        volume_device_name = '/dev/xvdg'

        #Attach volume to server automatically (with cleanup)
        self.explicit_attach_volume_to_server(
            self.test_server.id, volume.id, volume_device_name,
            expected_volume_status="in-use", add_cleanup=True)

    def test_explicit_attach_sata(self):
        volume = self.setup_volume(volume_type_name='sata')
        volume_device_name = '/dev/xvdh'

        #Attach volume to server automatically (with cleanup)
        self.explicit_attach_volume_to_server(
            self.test_server.id, volume.id, volume_device_name,
            expected_volume_status="in-use", add_cleanup=True)

    def test_rapidly_explicit_attach_both_volumes_types(self):
        sata_volume = self.setup_volume(volume_type_name='sata')
        ssd_volume = self.setup_volume(volume_type_name='ssd')

        sata_volume_device_name = '/dev/xvdi'
        self.explicit_attach_volume_to_server(
            self.test_server.id, sata_volume.id, sata_volume_device_name,
            expected_volume_status=False, add_cleanup=True)

        ssd_volume_device_name = '/dev/xvdj'
        self.explicit_attach_volume_to_server(
            self.test_server.id, ssd_volume.id, ssd_volume_device_name,
            expected_volume_status=False, add_cleanup=True)

        resp = self.volumes_provider.wait_for_volume_status(
            sata_volume.id, expected_status='in-use')
        assert resp.ok, (
            "After requesting an auto-attach for two volumes,"
            "the SATA volume did not reach the in-use state")

        resp = self.volumes_provider.wait_for_volume_status(
            ssd_volume.id, expected_status='in-use')
        assert resp.ok, (
            "After requesting an auto-attach for two volumes,"
            "the SSD volume did not reach the in-use state")

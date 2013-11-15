'''
@summary: Lunr API Volume Smoke Tests - Create, List, Get Info, Update, Delete Volume.
@copyright: Copyright (c) 2012 Rackspace US, Inc.
'''
import random

from ccengine.common.decorators import attr
from testrepo.common.testfixtures.blockstorage.compute_integration import \
    ComputeIntegrationFixture


class MultipleVolumeAttach(ComputeIntegrationFixture):
    '''
    @summary: Lunr API Volume Smoke Tests - Create, List, Get Info, Update, Delete Volume.
    '''
    @classmethod
    def setUpClass(cls):
        super(MultipleVolumeAttach, cls).setUpClass()

    def setUp(self):
        self.server = self.setup_server()
        self.volumes = []

        for x in range(5):
            volume_type_name = random.choice(['ssd', 'sata'])
            volume = self.setup_volume(volume_type_name=volume_type_name)
            self.volumes.append(volume)

    def tearDown(self):
        self.compute_provider.delete_servers([self.server.id])
        for volume in self.volumes:
            self.volumes_provider.delete_volume_confirmed(volume.id)

    @attr("regression")
    def test_auto_attach_five_mixed_volumes_dont_wait_for_attach(self):
        for volume in self.volumes:
            attachment = self.auto_attach_volume_to_server(
                self.server.id, volume.id, expected_volume_status=False,
                add_cleanup=True)

            assert str(attachment.volume_id) == str(volume.id),\
                'Volume attachment volume_id incorrect'

    @attr("regression")
    def test_auto_attach_five_mixed_volumes_wait_for_attach(self):
        for volume in self.volumes:
            attachment = self.auto_attach_volume_to_server(
                self.server.id, volume.id,
                expected_volume_status='in-use', add_cleanup=True)

            assert str(attachment.volume_id) == str(volume.id),\
                'Volume attachment volume_id incorrect'

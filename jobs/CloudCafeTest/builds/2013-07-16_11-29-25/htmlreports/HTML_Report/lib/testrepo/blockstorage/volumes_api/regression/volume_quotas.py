"""
@summary: happy path tests for Volumes API
@copyright: Copyright (c) 2012 Rackspace US, Inc.
"""
from ccengine.common.tools import datagen
from testrepo.common.testfixtures.blockstorage import VolumesAPIFixture


class VolumesQuotaRegression(VolumesAPIFixture):
    """
    @summary: Test Cloud Block storage Volumes API regressions relating to
    quotas
    """

    @classmethod
    def setUpClass(cls):
        super(VolumesQuotaRegression, cls).setUpClass()
        cls.expected_volumes = []
        cls.volume_types = cls.volumes_client.list_all_volume_types().entity

    @classmethod
    def tearDownClass(cls):
        super(VolumesQuotaRegression, cls).tearDownClass()
        cls.volumes_api_provider.cleanup_volumes(cls.expected_volumes)

    def test_invalid_sata_volume_creates_do_not_affect_quota(self):
        """
        Create 50 invalid volumes (verify they all fail)
        Attempt to create a valid 51'st
        Valid (51st) volume should succeed
        """
        invalid_volume_size = int(
            self.volumes_api_provider.min_volume_size) - 1
        max_allowed_volumes = 50  # Put this value in the config

        for i in range(max_allowed_volumes):
            volume_name = datagen.random_string(
                prefix="InvalidTestVolume{0}".format(i))

            resp = self.volumes_client.create_volume(
                volume_name, invalid_volume_size, "SATA")

            self.assertFalse(
                resp.ok,
                "Volume create should have failed with a 4XX for volume {0},"
                " but suceeded with a {1} instead".format(
                    volume_name, resp.status_code))

        volume_name = datagen.random_string(
            prefix="ValidTestVolume{0}".format(max_allowed_volumes+1))

        #Create a valid volume, expect it to pass
        resp = self.volumes_client.create_volume(
            volume_name, invalid_volume_size, "SATA")

        self.assertTrue(
            resp.ok,
            "Unable to create a valid volume {0} after attempting to create"
            " {1}(quota limit) invalid volumes".format(
                volume_name, max_allowed_volumes))

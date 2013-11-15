"""
@summary: happy path tests for Volumes API
@copyright: Copyright (c) 2012 Rackspace US, Inc.
"""

from unittest2.suite import TestSuite
from ccengine.common.tools import datagen
from testrepo.common.testfixtures.blockstorage.volumes_api import \
    VolumesAPI_Fixture


def load_tests(loader, standard_tests, pattern):
    """In order to run this test, you have to have the runner suppress the
    load_tests method by passing it the -s option.  This is because this
    test should only be run by itself while there is no other activity
    happening on the account
    """
    suite = TestSuite()
    return suite


class VolumesQuotaRegression(VolumesAPI_Fixture):
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
        cls.volumes_provider.cleanup_volumes(cls.expected_volumes)

    def test_invalid_sata_volume_creates_do_not_affect_quota(self):
        """
        Attempt to creat
        Attempt to create a valid 51'st
        Valid (51st) volume should succeed
        """
        invalid_volume_size = int(
            self.volumes_provider.min_volume_size) - 1
        resp = self.volumes_client.list_all_volumes()
        current_volume_count = len(resp.entity or [])
        max_volumes = int(
            int(self.config.volumes_api.volume_quota_limit) -
            current_volume_count)
        max_volumes = 0 if max_volumes < 0 else max_volumes

        print '\nCreating {0} invalid volumes'.format(max_volumes)
        for i in range(max_volumes):
            volume_name = datagen.random_string(
                prefix="InvalidTestVolume{0}".format(i))

            resp = self.volumes_client.create_volume(
                volume_name, invalid_volume_size, "SATA")

            self.assertFalse(
                resp.ok,
                "Invalid volume create should have failed with a 4XX for "
                "volume {0}, but suceeded with a {1} instead".format(
                    volume_name, resp.status_code))

        volume_name = datagen.random_string(
            prefix="ValidTestVolume{0}".format(max_volumes+1))

        #Create a valid volume, expect it to pass
        resp = self.volumes_client.create_volume(
            volume_name, self.volumes_provider.min_volume_size, "SATA")

        self.assertTrue(
            resp.ok,
            "Unable to create a valid volume {0} after attempting to create"
            " {1}(quota limit) invalid volumes".format(
                volume_name, max_volumes))

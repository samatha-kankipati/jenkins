"""
@summary: Volumes API VolumeTypes happy path tests
@copyright: Copyright (c) 2012 Rackspace US, Inc.
"""
from testrepo.common.testfixtures.blockstorage import VolumesAPIFixture


class VolumesAPI_VolumeTypesHappyPathTest(VolumesAPIFixture):
    """
        @summary: List Volume Types and Get Volume Type Info.
    """
    @classmethod
    def setUpClass(cls):
        super(VolumesAPI_VolumeTypesHappyPathTest, cls).setUpClass()

    def test_list_volume_types(self):
        resp = self.volumes_client.list_all_volume_types()
        self.assertTrue(resp.ok, "List Volume Types API call failed")
        vtypes = resp.entity
        for vtype in vtypes:
            self.assertTrue(hasattr(vtype, "id"), "id field not created")
            self.assertTrue(hasattr(vtype, "name"), "name field not created")

    def test_get_volume_type_info(self):
        resp = self.volumes_client.list_all_volume_types()
        self.assertTrue(resp.ok, "List Volume Types API call failed")
        vtypes = resp.entity
        for vtype in vtypes:
            self.assertTrue(
                hasattr(vtype, "id"),
                "id field not present in volume type info recieved from GET "
                "to /types")

            vt_resp = self.volumes_client.get_volume_type_info(vtype.id)
            self.assertTrue(vt_resp.ok, "Unable to get volume type info")
            self.assertIsNotNone(
                vt_resp.entity,
                "Unable to deserialize volume_type info response")

            vt_ent = vt_resp.entity
            self.assertTrue(
                hasattr(vt_ent, "id"),
                "id field not present in volume type info recieved from GET "
                "to /types/{volume_type_id}")

            self.assertTrue(
                hasattr(vt_ent, "name"),
                "name field not present in volume type info recieved from GET "
                "to /types/{volume_type_id}")

    def test_expected_vtypes_exists(self):
        expected_vtypes = ['sata', 'ssd']
        resp = self.volumes_client.list_all_volume_types()
        self.assertTrue(resp.ok, "List Volume Types API call failed")
        vtypes = resp.entity
        for evtype in expected_vtypes:
            type_found = False
            for vtype in vtypes:
                if vtype.name.lower() == evtype:
                    type_found = True
            self.assertTrue(
                type_found,
                'Could not find {0} volume type'.format(evtype))

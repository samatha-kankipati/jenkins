import ccengine.common.tools.datatools as DataTools
from ccengine.common.decorators import attr
from testrepo.common.testfixtures.stacktach_db_compute_integration \
    import STRevertResizeServerFixture
from ccengine.providers.configuration import MasterConfigProvider as _MCP


class StackTachDBResizeServerDownRevertTests(STRevertResizeServerFixture):
    """
    @summary: With Server Resize Down (e.g. from flavor 3 -> 2) then
      Revert (i.e., cancelling the resize so flavor 2 -> 3),
      tests the entries created in StackTach DB.
    """

    @classmethod
    def setUpClass(cls):
        cls.config = _MCP()
        cls.flavor_ref = cls.config.compute_api.flavor_ref
        cls.flavor_ref_alt = cls.config.compute_api.flavor_ref_alt
        if cls.flavor_ref > cls.flavor_ref_alt:
            raise cls.assertClassSetupFailure(
                'flavor_ref should not be greater than flavor_ref_alt. '
                'flavor_ref: {0}  flavor_ref_alt: {1}'.format(
                    cls.flavor_ref, cls.flavor_ref_alt))
        (super(StackTachDBResizeServerDownRevertTests, cls)
         .setUpClass(flavorRef=cls.flavor_ref_alt,
                     resize_flavor=cls.flavor_ref))

    @classmethod
    def tearDownClass(cls):
        super(StackTachDBResizeServerDownRevertTests, cls).tearDownClass()

    @attr(type='positive')
    def test_launch_entry_on_revert_resize_down_server_response(self):
        """
        Verify the Launch parameters are being returned in the
        Server Revert Resize response
        """

        # There should be 3 launch entries for a revert resize.
        self.assertEqual(len(self.st_launch_response.entity), 3,
                         self.msg.format("List of Launch objects",
                                         '3',
                                         len(self.st_launch_response.entity),
                                         self.st_launch_response.reason,
                                         self.st_launch_response.content))
        self.assertTrue(self.st_launch_response.ok,
                        self.msg.format("status_code", 200,
                                        self.st_launch_response.status_code,
                                        self.st_launch_response.reason,
                                        self.st_launch_response.content))
        for launch in self.st_launches:
            self.assertTrue(launch.id,
                            self.msg.format("id",
                                            "Not None or Empty", launch.id,
                                            self.st_launch_response.reason,
                                            self.st_launch_response.content))
            self.assertTrue(launch.request_id,
                            self.msg.format("request_id",
                                            "Not None or Empty",
                                            launch.request_id,
                                            self.st_launch_response.reason,
                                            self.st_launch_response.content))
            self.assertTrue(launch.instance,
                            self.msg.format("instance",
                                            "Not None or Empty",
                                            launch.instance,
                                            self.st_launch_response.reason,
                                            self.st_launch_response.content))
            self.assertTrue(launch.launched_at,
                            self.msg.format("launched_at",
                                            "Not None or Empty",
                                            launch.launched_at,
                                            self.st_launch_response.reason,
                                            self.st_launch_response.content))
            self.assertTrue(launch.instance_type_id,
                            self.msg.format("instance_type_id",
                                            "Not None or Empty",
                                            launch.instance_type_id,
                                            self.st_launch_response.reason,
                                            self.st_launch_response.content))

    @attr(type='positive')
    def test_launch_entry_fields_on_create_server(self):
        """
        Verify that the first Launch entry will have all expected fields
        before a Server Resize
        """

        self.assertEqual(self.created_server.id,
                         self.st_launch_create_server.instance,
                         self.msg.format("instance",
                                         self.created_server.id,
                                         self.st_launch_create_server.instance,
                                         self.st_launch_response.reason,
                                         self.st_launch_response.content))
        self.assertEqual(
            self.created_server.flavor.id,
            self.st_launch_create_server.instance_type_id,
            self.msg.format("instance_type_id",
                            self.created_server.flavor.id,
                            self.st_launch_create_server.instance_type_id,
                            self.st_launch_response.reason,
                            self.st_launch_response.content))
        self.assertEqual(
            self.flavor_ref_alt,
            self.st_launch_create_server.instance_type_id,
            self.msg.format("instance_type_id",
                            self.flavor_ref_alt,
                            self.st_launch_create_server.instance_type_id,
                            self.st_launch_response.reason,
                            self.st_launch_response.content))
        self.assertTrue(DataTools.are_datetimestrings_equal(
            self.launched_at_created_server,
            self.st_launch_create_server.launched_at,
            self.leeway),
            self.msg.format("launched_at",
                            self.launched_at_created_server,
                            self.st_launch_create_server.launched_at,
                            self.st_launch_response.reason,
                            self.st_launch_response.content))

    @attr(type='positive')
    def test_launch_entry_fields_on_resize_down(self):
        """
        Verify that the second Launch entry will have all expected fields
        after a Server Resize and before a Server Revert Resize
        """

        self.assertEqual(self.verified_resized_server.id,
                         self.st_launch_resize_server.instance,
                         self.msg.format("instance",
                                         self.verified_resized_server.id,
                                         self.st_launch_resize_server.instance,
                                         self.st_launch_response.reason,
                                         self.st_launch_response.content))
        self.assertEqual(
            self.verified_resized_server.flavor.id,
            self.st_launch_resize_server.instance_type_id,
            self.msg.format("instance_type_id",
                            self.verified_resized_server.flavor.id,
                            self.st_launch_resize_server.instance_type_id,
                            self.st_launch_response.reason,
                            self.st_launch_response.content))
        self.assertEqual(
            self.flavor_ref,
            self.st_launch_resize_server.instance_type_id,
            self.msg.format("instance_type_id",
                            self.flavor_ref,
                            self.st_launch_resize_server.instance_type_id,
                            self.st_launch_response.reason,
                            self.st_launch_response.content))
        self.assertTrue(DataTools.are_datetimestrings_equal(
            self.launched_at_resized_server,
            self.st_launch_resize_server.launched_at,
            self.leeway),
            self.msg.format("launched_at",
                            self.launched_at_resized_server,
                            self.st_launch_resize_server.launched_at,
                            self.st_launch_response.reason,
                            self.st_launch_response.content))

    @attr(type='positive')
    def test_launch_entry_fields_on_revert_resize_down_server_response(self):
        """
        Verify that the third Launch entry will have all expected fields
        after a Server Revert Resize
        """

        self.assertEqual(self.reverted_server.id,
                         self.st_launch_revert_resize.instance,
                         self.msg.format("instance",
                                         self.reverted_server.id,
                                         self.st_launch_revert_resize.instance,
                                         self.st_launch_response.reason,
                                         self.st_launch_response.content))
        self.assertEqual(
            self.reverted_server.flavor.id,
            self.st_launch_revert_resize.instance_type_id,
            self.msg.format("instance_type_id",
                            self.reverted_server.flavor.id,
                            self.st_launch_revert_resize.instance_type_id,
                            self.st_launch_response.reason,
                            self.st_launch_response.content))
        self.assertEqual(
            self.flavor_ref_alt,
            self.st_launch_revert_resize.instance_type_id,
            self.msg.format("instance_type_id",
                            self.flavor_ref_alt,
                            self.st_launch_revert_resize.instance_type_id,
                            self.st_launch_response.reason,
                            self.st_launch_response.content))
        self.assertTrue(DataTools.are_datetimestrings_equal(
            self.launched_at_revert_resize_server,
            self.st_launch_revert_resize.launched_at,
            self.leeway),
            self.msg.format("launched_at",
                            self.launched_at_revert_resize_server,
                            self.st_launch_revert_resize.launched_at,
                            self.st_launch_response.reason,
                            self.st_launch_response.content))

    @attr(type='positive')
    def test_exist_entry_on_revert_resize_down_server_response(self):
        """
        Verify the Exist parameters are correct after a Server Revert Resize
        """

        # There should be 2 immediate exists entries for a revert resize.
        self.assertEqual(len(self.st_exist_response.entity), 2,
                         self.msg.format("List of Exists objects",
                                         '2',
                                         len(self.st_exist_response.entity),
                                         self.st_exist_response.reason,
                                         self.st_exist_response.content))
        self.assertTrue(self.st_exist_response.ok,
                        self.msg.format("status_code", 200,
                                        self.st_exist_response.status_code,
                                        self.st_exist_response.reason,
                                        self.st_exist_response.content))
        for exist in self.st_exists:
            self.assertTrue(exist.id,
                            self.msg.format("id",
                                            "Not None or Empty", exist.id,
                                            self.st_exist_response.reason,
                                            self.st_exist_response.content))
            self.assertTrue(exist.instance,
                            self.msg.format("instance",
                                            "Not None or Empty",
                                            exist.instance,
                                            self.st_exist_response.reason,
                                            self.st_exist_response.content))
            self.assertTrue(exist.launched_at,
                            self.msg.format("launched_at",
                                            "Not None or Empty",
                                            exist.launched_at,
                                            self.st_exist_response.reason,
                                            self.st_exist_response.content))
            # We do not delete the server so this should be null.
            self.assertTrue(exist.deleted_at is None,
                            self.msg.format("deleted_at",
                                            "None or Empty",
                                            exist.deleted_at,
                                            self.st_exist_response.reason,
                                            self.st_exist_response.content))
            self.assertTrue(exist.message_id,
                            self.msg.format("message_id",
                                            "Not None or Empty",
                                            exist.message_id,
                                            self.st_exist_response.reason,
                                            self.st_exist_response.content))
            self.assertTrue(exist.raw,
                            self.msg.format("raw",
                                            "Not None or Empty",
                                            exist.raw,
                                            self.st_exist_response.reason,
                                            self.st_exist_response.content))
            self.assertTrue(exist.instance_type_id,
                            self.msg.format("instance_type_id",
                                            "Not None or Empty",
                                            exist.instance_type_id,
                                            self.st_exist_response.reason,
                                            self.st_exist_response.content))
            self.assertTrue(exist.status,
                            self.msg.format("status",
                                            "Not None or Empty",
                                            exist.status,
                                            self.st_exist_response.reason,
                                            self.st_exist_response.content))
            self.assertTrue(exist.usage,
                            self.msg.format("usage",
                                            "Not None or Empty", exist.usage,
                                            self.st_exist_response.reason,
                                            self.st_exist_response.content))
            self.assertTrue(self.st_exist.os_distro,
                            self.msg.format("os_distro", "Not None or Empty",
                                            self.st_exist.os_distro,
                                            self.st_exist_response.reason,
                                            self.st_exist_response.content))
            self.assertTrue(self.st_exist.os_version,
                            self.msg.format("os_version", "Not None or Empty",
                                            self.st_exist.os_version,
                                            self.st_exist_response.reason,
                                            self.st_exist_response.content))
            self.assertTrue(self.st_exist.os_architecture,
                            self.msg.format("os_architecture",
                                            "Not None or Empty",
                                            self.st_exist.os_architecture,
                                            self.st_exist_response.reason,
                                            self.st_exist_response.content))
            self.assertTrue(self.st_exist.rax_options,
                            self.msg.format("rax_options", "Not None or Empty",
                                            self.st_exist.rax_options,
                                            self.st_exist_response.reason,
                                            self.st_exist_response.content))
            # We do not delete the server so this should be null.
            self.assertTrue(exist.delete is None,
                            self.msg.format("delete",
                                            "None or Empty", exist.delete,
                                            self.st_exist_response.reason,
                                            self.st_exist_response.content))

    @attr(type='positive')
    def test_exists_entry_fields_on_resize_down(self):
        """
        Verify that the First exists entry will have all expected fields
        on the first Server Resize; before Server Revert Resize
        """

        self.assertEqual(self.created_server.id,
                         self.st_exist_resize_server.instance,
                         self.msg.format("instance",
                                         self.created_server.id,
                                         self.st_exist_resize_server.instance,
                                         self.st_exist_response.reason,
                                         self.st_exist_response.content))
        self.assertTrue(DataTools.are_datetimestrings_equal(
            self.launched_at_created_server,
            self.st_exist_resize_server.launched_at,
            self.leeway),
            self.msg.format("launched_at",
                            self.launched_at_created_server,
                            self.st_exist_resize_server.launched_at,
                            self.st_exist_response.reason,
                            self.st_exist_response.content))
        self.assertEqual(
            self.created_server.flavor.id,
            self.st_exist_resize_server.instance_type_id,
            self.msg.format("instance_type_id",
                            self.created_server.flavor.id,
                            self.st_exist_resize_server.instance_type_id,
                            self.st_exist_response.reason,
                            self.st_exist_response.content))
        self.assertEqual(
            self.flavor_ref_alt,
            self.st_exist_resize_server.instance_type_id,
            self.msg.format("instance_type_id",
                            self.flavor_ref_alt,
                            self.st_exist_resize_server.instance_type_id,
                            self.st_exist_response.reason,
                            self.st_exist_response.content))
        self.assertIn(self.st_exist_resize_server.status,
                      ['pending', 'verified'],
                      self.msg.format("status",
                                      "pending or verified",
                                      self.st_exist_resize_server.status,
                                      self.st_exist_response.reason,
                                      self.st_exist_response.content))
        self.assertIn(self.st_exist.send_status, [0, 201],
                      self.msg.format("send_status",
                                      "Not None, Empty or unexpected value",
                                      self.st_exist.status,
                                      self.st_exist_response.reason,
                                      self.st_exist_response.content))
        self.assertTrue(hasattr(self.st_exist, 'fail_reason'),
                        self.msg.format("fail_reason",
                                        "Should be an attribute of object",
                                        self.st_exist.status,
                                        self.st_exist_response.reason,
                                        self.st_exist_response.content))

    @attr(type='positive')
    def test_exist_launched_at_field_match_on_resize_down(self):
        """
        Verify that the first Exists entry launched_at matches the
        Launch entry launched_at for a Server Resize Down
        """

        self.assertEqual(
            self.st_launch_create_server.launched_at,
            self.st_exist_resize_server.launched_at,
            self.msg.format("launched_at",
                            self.st_launch_create_server.launched_at,
                            self.st_exist_resize_server.launched_at,
                            self.st_exist_response.reason,
                            self.st_exist_response.content))

    @attr(type='positive')
    def test_exists_entry_fields_on_revert_resize_down(self):
        """
        Verify that the Second Exist entry will have all expected fields
        after Server Revert Resize
        """

        self.assertEqual(
            self.verified_resized_server.id,
            self.st_exist_revert_resize_server.instance,
            self.msg.format("instance",
                            self.verified_resized_server.id,
                            self.st_exist_revert_resize_server.instance,
                            self.st_exist_response.reason,
                            self.st_exist_response.content))
        self.assertTrue(DataTools.are_datetimestrings_equal(
            self.launched_at_resized_server,
            self.st_exist_revert_resize_server.launched_at,
            self.leeway),
            self.msg.format("launched_at",
                            self.launched_at_resized_server,
                            self.st_exist_revert_resize_server.launched_at,
                            self.st_exist_response.reason,
                            self.st_exist_response.content))
        self.assertEqual(
            self.verified_resized_server.flavor.id,
            self.st_exist_revert_resize_server.instance_type_id,
            self.msg.format(
                "instance_type_id",
                self.verified_resized_server.flavor.id,
                self.st_exist_revert_resize_server.instance_type_id,
                self.st_exist_response.reason,
                self.st_exist_response.content))
        self.assertEqual(
            self.flavor_ref,
            self.st_exist_revert_resize_server.instance_type_id,
            self.msg.format(
                "instance_type_id",
                self.flavor_ref,
                self.st_exist_revert_resize_server.instance_type_id,
                self.st_exist_response.reason,
                self.st_exist_response.content))
        self.assertEqual(
            self.st_exist_revert_resize_server.status, 'pending',
            self.msg.format("status",
                            "Not None or Empty",
                            self.st_exist_revert_resize_server.status,
                            self.st_exist_response.reason,
                            self.st_exist_response.content))
        self.assertIn(self.st_exist.send_status, [0, 201],
                      self.msg.format("send_status",
                                      "Not None, Empty or unexpected value",
                                      self.st_exist.status,
                                      self.st_exist_response.reason,
                                      self.st_exist_response.content))
        self.assertTrue(hasattr(self.st_exist, 'fail_reason'),
                        self.msg.format("fail_reason",
                                        "Should be an attribute of object",
                                        self.st_exist.status,
                                        self.st_exist_response.reason,
                                        self.st_exist_response.content))

    @attr(type='positive')
    def test_exist_launched_at_field_match_on_revert_resize_down(self):
        """
        Verify that the second Exists entry launched_at matches the
        Launch entry launched_at for a Server Revert Resize Down
        """

        self.assertEqual(
            self.st_launch_resize_server.launched_at,
            self.st_exist_revert_resize_server.launched_at,
            self.msg.format("launched_at",
                            self.st_launch_resize_server.launched_at,
                            self.st_exist_revert_resize_server.launched_at,
                            self.st_exist_response.reason,
                            self.st_exist_response.content))

    @attr(type='positive')
    def test_no_delete_entry_on_revert_resize_down_server_response(self):
        """
        Verify that there is no delete entry after a Server Revert Resize
        """

        self.assertTrue(self.st_delete_response.ok,
                        self.msg.format("status_code",
                                        200,
                                        self.st_delete_response.status_code,
                                        self.st_delete_response.reason,
                                        self.st_delete_response.content))
        self.assertFalse(self.st_delete,
                         self.msg.format("Non-empty List of Delete objects",
                                         "Empty List", self.st_delete,
                                         self.st_delete_response.reason,
                                         self.st_delete_response.content))

import ccengine.common.tools.datatools as DataTools
from ccengine.common.decorators import attr
from testrepo.common.testfixtures.stacktach_db_compute_integration \
        import STRebuildServerFixture


class StackTachDBRebuildServerTests(STRebuildServerFixture):
    '''
    @summary: With Server Rebuild, tests the entries created in StackTach DB.
    '''

    @classmethod
    def setUpClass(cls):
        super(StackTachDBRebuildServerTests, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        super(StackTachDBRebuildServerTests, cls).tearDownClass()

    @attr(type='positive')
    def test_launch_entry_on_rebuild_server_response(self):
        '''
        Verify the Launch parameters are being returned in the
        Server Rebuild response
        '''

        self.assertEqual(len(self.st_launch_response.entity), 2,
                        self.msg.format("List of Launch objects",
                                        '2',
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
        '''
        Verify that the first Launch entry will have all expected fields
        after a Server Rebuild
        '''

        self.assertEqual(self.rebuilt_server.id, self.st_launch_create_server.instance,
                        self.msg.format("instance",
                                        self.rebuilt_server.id,
                                        self.st_launch_create_server.instance,
                                        self.st_launch_response.reason,
                                        self.st_launch_response.content))
        self.assertEqual(self.rebuilt_server.flavor.id,
                         self.st_launch_create_server.instance_type_id,
                         self.msg.format("instance_type_id",
                                         self.rebuilt_server.flavor.id,
                                         self.st_launch_create_server.instance_type_id,
                                         self.st_launch_response.reason,
                                         self.st_launch_response.content))
        self.assertEqual(self.flavor_ref,
                         self.st_launch_create_server.instance_type_id,
                         self.msg.format("instance_type_id",
                                         self.flavor_ref,
                                         self.st_launch_create_server.instance_type_id,
                                         self.st_launch_response.reason,
                                         self.st_launch_response.content))
        self.assertTrue(DataTools
                        .are_datetimestrings_equal(self.launched_at_created_server,
                                                   self.st_launch_create_server.launched_at,
                                                   self.leeway),
                        self.msg.format("launched_at",
                                        self.launched_at_created_server,
                                        self.st_launch_create_server.launched_at,
                                        self.st_launch_response.reason,
                                        self.st_launch_response.content))

    @attr(type='positive')
    def test_launch_entry_fields_on_rebuild(self):
        '''
        Verify that the second Launch entry will have all expected fields
        after a Server Rebuild
        '''

        self.assertEqual(self.rebuilt_server.id, self.st_launch_rebuild_server.instance,
                        self.msg.format("instance",
                                        self.rebuilt_server.id,
                                        self.st_launch_rebuild_server.instance,
                                        self.st_launch_response.reason,
                                        self.st_launch_response.content))
        self.assertEqual(self.rebuilt_server.flavor.id,
                         self.st_launch_rebuild_server.instance_type_id,
                         self.msg.format("instance_type_id",
                                         self.rebuilt_server.flavor.id,
                                         self.st_launch_rebuild_server.instance_type_id,
                                         self.st_launch_response.reason,
                                         self.st_launch_response.content))
        self.assertEqual(self.flavor_ref,
                         self.st_launch_rebuild_server.instance_type_id,
                         self.msg.format("instance_type_id",
                                         self.flavor_ref,
                                         self.st_launch_rebuild_server.instance_type_id,
                                         self.st_launch_response.reason,
                                         self.st_launch_response.content))
        self.assertTrue(DataTools
                        .are_datetimestrings_equal(self.launched_at_rebuilt_server,
                                                   self.st_launch_rebuild_server.launched_at,
                                                   self.leeway),
                        self.msg.format("launched_at",
                                        self.launched_at_rebuilt_server,
                                        self.st_launch_rebuild_server.launched_at,
                                        self.st_launch_response.reason,
                                        self.st_launch_response.content))

    @attr(type='positive')
    def test_exist_entry_on_rebuild(self):
        '''
        Verify the Exist parameters are correct after a Server Rebuild        
        '''

        self.assertEqual(len(self.st_exist_response.entity), 1,
                        self.msg.format("List of Exists objects",
                                        '1',
                                        len(self.st_exist_response.entity),
                                        self.st_exist_response.reason,
                                        self.st_exist_response.content))
        self.assertTrue(self.st_exist_response.ok,
                        self.msg.format("status_code", 200,
                                        self.st_exist_response.status_code,
                                        self.st_exist_response.reason,
                                        self.st_exist_response.content))
        self.assertTrue(self.st_exist.id,
                        self.msg.format("id",
                                        "Not None or Empty", self.st_exist.id,
                                        self.st_exist_response.reason,
                                        self.st_exist_response.content))
        self.assertTrue(self.st_exist.instance,
                        self.msg.format("instance",
                                        "Not None or Empty",
                                        self.st_exist.instance,
                                        self.st_exist_response.reason,
                                        self.st_exist_response.content))
        self.assertTrue(self.st_exist.launched_at,
                        self.msg.format("launched_at",
                                        "Not None or Empty",
                                        self.st_exist.launched_at,
                                        self.st_exist_response.reason,
                                        self.st_exist_response.content))
        # We do not delete the server so this should be null.
        self.assertTrue(self.st_exist.deleted_at is None,
                        self.msg.format("deleted_at",
                                        "None or Empty",
                                        self.st_exist.deleted_at,
                                        self.st_exist_response.reason,
                                        self.st_exist_response.content))
        self.assertTrue(self.st_exist.message_id,
                        self.msg.format("message_id",
                                        "Not None or Empty",
                                        self.st_exist.message_id,
                                        self.st_exist_response.reason,
                                        self.st_exist_response.content))
        self.assertTrue(self.st_exist.raw,
                        self.msg.format("raw",
                                        "Not None or Empty",
                                        self.st_exist.raw,
                                        self.st_exist_response.reason,
                                        self.st_exist_response.content))
        self.assertTrue(self.st_exist.instance_type_id,
                        self.msg.format("instance_type_id",
                                        "Not None or Empty",
                                        self.st_exist.instance_type_id,
                                        self.st_exist_response.reason,
                                        self.st_exist_response.content))
        self.assertTrue(self.st_exist.status,
                        self.msg.format("status",
                                        "Not None or Empty",
                                        self.st_exist.status,
                                        self.st_exist_response.reason,
                                        self.st_exist_response.content))
        self.assertTrue(self.st_exist.usage,
                        self.msg.format("usage",
                                        "Not None or Empty", self.st_exist.usage,
                                        self.st_exist_response.reason,
                                        self.st_exist_response.content))
        # We do not delete the server so this should be null.
        self.assertTrue(self.st_exist.delete is None,
                        self.msg.format("delete",
                                        "None or Empty", self.st_exist.delete,
                                        self.st_exist_response.reason,
                                        self.st_exist_response.content))

    @attr(type='positive')
    def test_exists_entry_fields_on_rebuild_server_response(self):
        '''
        Verify that the Exist entry will have all expected fields 
        after Server Rebuild
        '''

        self.assertEqual(self.rebuilt_server.id, self.st_exist.instance,
                        self.msg.format("instance",
                                        self.rebuilt_server.id,
                                        self.st_exist.instance,
                                        self.st_exist_response.reason,
                                        self.st_exist_response.content))
        self.assertTrue(DataTools
                        .are_datetimestrings_equal(self.launched_at_created_server,
                                                   self.st_exist.launched_at,
                                                   self.leeway),
                        self.msg.format("launched_at",
                                        self.launched_at_created_server,
                                        self.st_exist.launched_at,
                                        self.st_exist_response.reason,
                                        self.st_exist_response.content))
        self.assertEqual(self.rebuilt_server.flavor.id,
                         self.st_exist.instance_type_id,
                         self.msg.format("instance_type_id",
                                         self.rebuilt_server.flavor.id,
                                         self.st_exist.instance_type_id,
                                         self.st_exist_response.reason,
                                         self.st_exist_response.content))
        self.assertEqual(self.flavor_ref,
                         self.st_exist.instance_type_id,
                         self.msg.format("instance_type_id",
                                         self.flavor_ref,
                                         self.st_exist.instance_type_id,
                                         self.st_exist_response.reason,
                                         self.st_exist_response.content))
        self.assertIn(self.st_exist.status, ['pending', 'verified'],
                      self.msg.format("status",
                                      "'pending' or 'verified'",
                                      self.st_exist.status,
                                      self.st_exist_response.reason,
                                      self.st_exist_response.content))

    @attr(type='positive')
    def test_exist_launched_at_field_match_on_rebuild(self):
        '''
        Verify that the Exists entry launched_at matches the
        Launch entry launched_at for a Server Rebuild
        '''

        self.assertEqual(self.st_launch_create_server.launched_at,
                         self.st_exist.launched_at,
                         self.msg.format("launched_at",
                                         self.st_launch_create_server.launched_at,
                                         self.st_exist.launched_at,
                                         self.st_exist_response.reason,
                                         self.st_exist_response.content))

    @attr(type='positive')
    def test_no_delete_entry_on_rebuild_server_response(self):
        '''Verify that there is no delete entry after a Server Rebuild'''

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

from ccengine.common.decorators import attr
import ccengine.common.tools.datatools as DataTools
from testrepo.common.testfixtures.stacktach_db_compute_integration \
        import STDeleteServerFixture


class StackTachDBDeleteServerTests(STDeleteServerFixture):
    '''
    @summary: With Server Delete, tests the entries created in StackTach DB.
    '''

    @classmethod
    def setUpClass(cls):
        super(StackTachDBDeleteServerTests, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        super(StackTachDBDeleteServerTests, cls).tearDownClass()

    @attr(type='positive')
    def test_launch_entry_on_create_server_response(self):
        '''
        Verify the Launch parameters are being returned in the initial response
        of Server Creation
        '''

        self.assertTrue(self.st_launch_response.ok,
                        self.msg.format("status_code", 200,
                                        self.st_launch_response.status_code,
                                        self.st_launch_response.reason,
                                        self.st_launch_response.content))
        self.assertTrue(self.st_launch_create_server.id,
                        self.msg.format("id",
                                        "Not None or Empty",
                                        self.st_launch_create_server.id,
                                        self.st_launch_response.reason,
                                        self.st_launch_response.content))
        self.assertTrue(self.st_launch_create_server.request_id,
                        self.msg.format("request_id",
                                        "Not None or Empty",
                                        self.st_launch_create_server.request_id,
                                        self.st_launch_response.reason,
                                        self.st_launch_response.content))
        self.assertTrue(self.st_launch_create_server.instance,
                        self.msg.format("instance",
                                        "Not None or Empty",
                                        self.st_launch_create_server.instance,
                                        self.st_launch_response.reason,
                                        self.st_launch_response.content))
        self.assertTrue(self.st_launch_create_server.launched_at,
                        self.msg.format("launched_at",
                                        "Not None or Empty",
                                        self.st_launch_create_server.launched_at,
                                        self.st_launch_response.reason,
                                        self.st_launch_response.content))
        self.assertTrue(self.st_launch_create_server.instance_type_id,
                        self.msg.format("instance_type_id",
                                        "Not None or Empty",
                                        self.st_launch_create_server.instance_type_id,
                                        self.st_launch_response.reason,
                                        self.st_launch_response.content))

    @attr(type='positive')
    def test_launch_entry_fields_on_create_server_response(self):
        '''
        Verify that the Launch entry will have all expected fields
        after Server Creation
        '''

        self.assertEqual(self.deleted_server.id, self.st_launch_create_server.instance,
                        self.msg.format("instance",
                                        self.deleted_server.id,
                                        self.st_launch_create_server.instance,
                                        self.st_launch_response.reason,
                                        self.st_launch_response.content))
        self.assertEqual(self.deleted_server.flavor.id,
                         self.st_launch_create_server.instance_type_id,
                         self.msg.format("instance_type_id",
                                         self.deleted_server.flavor.id,
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
    def test_delete_entry_on_delete_server_response(self):
        '''
        Verify the Delete parameters are being returned from the
        StackTach DB on Server Deletion
        '''

        self.assertEqual(len(self.st_delete_response.entity), 1,
                        self.msg.format("List of Delete objects",
                                        '1',
                                        len(self.st_delete_response.entity),
                                        self.st_delete_response.reason,
                                        self.st_delete_response.content))
        self.assertTrue(self.st_delete_response.ok,
                        self.msg.format("status_code", 200,
                                        self.st_delete_response.status_code,
                                        self.st_delete_response.reason,
                                        self.st_delete_response.content))
        self.assertTrue(self.st_delete.id,
                        self.msg.format("id",
                                        "Not None or Empty",
                                        self.st_delete.id,
                                        self.st_delete_response.reason,
                                        self.st_delete_response.content))
        self.assertTrue(self.st_delete.instance,
                        self.msg.format("instance",
                                        "Not None or Empty",
                                        self.st_delete.instance,
                                        self.st_delete_response.reason,
                                        self.st_delete_response.content))
        self.assertTrue(self.st_delete.launched_at,
                        self.msg.format("launched_at",
                                        "Not None or Empty",
                                        self.st_delete.launched_at,
                                        self.st_delete_response.reason,
                                        self.st_delete_response.content))
        self.assertTrue(self.st_delete.deleted_at,
                        self.msg.format("deleted_at",
                                        "Not None or Empty",
                                        self.st_delete.deleted_at,
                                        self.st_delete_response.reason,
                                        self.st_delete_response.content))
        self.assertTrue(self.st_delete.raw,
                        self.msg.format("raw",
                                        "Not None or Empty",
                                        self.st_delete.raw,
                                        self.st_delete_response.reason,
                                        self.st_delete_response.content))

    @attr(type='positive')
    def test_delete_entry_fields_on_delete_server_response(self):
        '''
        Verify that the Delete entry will have all expected fields
        after Server Delete
        '''

        self.assertEqual(self.deleted_server.id, self.st_delete.instance,
                        self.msg.format("instance",
                                        self.deleted_server.id,
                                        self.st_delete.instance,
                                        self.st_delete_response.reason,
                                        self.st_delete_response.content))
        self.assertTrue(DataTools
                        .are_datetimestrings_equal(self.launched_at_created_server,
                                                   self.st_delete.launched_at,
                                                   self.leeway),
                        self.msg.format("launched_at",
                                        self.launched_at_created_server,
                                        self.st_delete.launched_at,
                                        self.st_delete_response.reason,
                                        self.st_delete_response.content))
        self.assertTrue(DataTools
                        .are_datetimestrings_equal(self.deleted_at,
                                                   self.st_delete.deleted_at,
                                                   self.leeway),
                        self.msg.format("deleted_at",
                                        self.deleted_at,
                                        self.st_delete.deleted_at,
                                        self.st_delete_response.reason,
                                        self.st_delete_response.content))

    @attr(type='positive')
    def test_launched_at_field_match_on_delete_server_response(self):
        '''
        Verify that the Delete entry launched_at matches the
        Launch entry launched_at for a deleted server
        '''

        self.assertEqual(self.st_delete.launched_at,
                         self.st_launch_create_server.launched_at,
                         self.msg.format("launched_at",
                                        self.st_delete.launched_at,
                                        self.st_launch_create_server.launched_at,
                                        self.st_delete_response.reason,
                                        self.st_delete_response.content))

    @attr(type='positive')
    def test_launched_earlier_than_deleted_on_delete_server_response(self):
        '''
        Verify that the Delete entry launched_at is earlier than the 
        Delete entry deleted_at for a deleted server
        '''

        self.assertLess(DataTools.string_to_datetime(self.st_delete.launched_at),
                        DataTools.string_to_datetime(self.st_delete.deleted_at),
                        self.msg.format("launched_at",
                                        "launched_at earlier than deleted_at",
                                        ' '.join([self.st_delete.launched_at,
                                                  self.st_delete.deleted_at]),
                                        self.st_delete_response.reason,
                                        self.st_delete_response.content))

    @attr(type='positive')
    def test_instance_field_on_delete_server_response(self):
        '''
        Verify that the Delete entry instance matches the
        Launch entry instance for a deleted server
        '''

        self.assertEqual(self.st_delete.instance,
                         self.st_launch_create_server.instance,
                         self.msg.format("instance",
                                        self.st_delete.instance,
                                        self.st_launch_create_server.instance,
                                        self.st_delete_response.reason,
                                        self.st_delete_response.content))

    @attr(type='positive')
    def test_no_exist_entry_on_delete_server_response(self):
        '''
        Verify that there is no exist entry on a newly deleted server
        where the deletion occurs before the end of audit period
        '''

        self.assertTrue(self.st_exist_response.ok,
                        self.msg.format("status_code",
                                        200,
                                        self.st_exist_response.status_code,
                                        self.st_exist_response.reason,
                                        self.st_exist_response.content))
        self.assertFalse(self.st_exist,
                         self.msg.format("Non-empty List of Exist objects",
                                         "Empty List", self.st_exist,
                                         self.st_exist_response.reason,
                                         self.st_exist_response.content))

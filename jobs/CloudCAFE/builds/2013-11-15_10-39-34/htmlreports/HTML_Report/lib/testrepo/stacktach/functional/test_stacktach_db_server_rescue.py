from ccengine.common.decorators import attr
import ccengine.common.tools.datatools as DataTools
from testrepo.common.testfixtures.stacktach_db_compute_integration \
        import STRescueServerFixture


class ServerRescueTests(STRescueServerFixture):
    '''
    @summary: With Server Rescue, tests the entries created in 
      StackTach DB.
    '''

    @classmethod
    def setUpClass(cls):
        super(ServerRescueTests, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        super(ServerRescueTests, cls).tearDownClass()


    @attr(type='positive')
    def test_launch_entry_on_rescue_server_response(self):
        '''
        Verify that the Launch parameters are being returned from the 
        StackTach DB after peforming a rescue on an instance.
        '''

        self.assertEqual(len(self.st_launch_response.entity), 1,
                        self.msg.format("List of Launch objects",
                                        '1',
                                        len(self.st_launch_response.entity),
                                        self.st_launch_response.reason,
                                        self.st_launch_response.content))
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
    def test_launch_entry_fields_on_rescue_server_response(self):
        '''
        Verify that the Launch entry will have all expected fields from the 
        StackTach DB after peforming a rescue on an instance.
        '''

        self.assertEqual(self.rescue_server.id, self.st_launch_create_server.instance,
                        self.msg.format("instance",
                                        self.rescue_server.id,
                                        self.st_launch_create_server.instance,
                                        self.st_launch_response.reason,
                                        self.st_launch_response.content))
        self.assertEqual(self.rescue_server.flavor.id,
                         self.st_launch_create_server.instance_type_id,
                         self.msg.format("instance_type_id",
                                         self.rescue_server.flavor.id,
                                         self.st_launch_create_server.instance_type_id,
                                         self.st_launch_response.reason,
                                         self.st_launch_response.content))
        self.assertEqual(self.flavor_ref,
                         self.st_launch_create_server.instance_type_id,
                         self.msg.format("instance_type_id",
                                         self.flavor_ref,
                                         self.st_launch_create_server.instance_type_id,
                                         self.st_delete_response.reason,
                                         self.st_delete_response.content))
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
    def test_no_delete_entry_on_rescue_server_response(self):
        '''
        Verify that there is no delete entry after peforming a rescue
        on an instance.
        '''

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

    @attr(type='positive')
    def test_no_exist_entry_on_rescue_server_response(self):
        '''
        Verify that there is no exist entry peforming a rescue
        on an instance.
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

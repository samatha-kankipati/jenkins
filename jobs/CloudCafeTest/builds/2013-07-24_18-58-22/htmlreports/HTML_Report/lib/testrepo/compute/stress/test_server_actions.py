from testrepo.common.testfixtures.compute import ComputeFixture
from ccengine.domain.types import NovaServerStatusTypes, NovaServerRebootTypes
import time
from ccengine.common.tools.datagen import rand_name
from ccengine.common.tools.equality_tools import EqualityTools
from ccengine.common.exceptions.compute import Forbidden
from ccengine.common.decorators import attr
import base64


class ServerActionsBaseTests(ComputeFixture):

    @classmethod
    def setUpClass(cls):
        super(ServerActionsBaseTests, cls).setUpClass()
        response = cls.compute_provider.create_active_server()
        cls.server = response.entity
        cls.remote_instance = cls.compute_provider.get_remote_instance_client(cls.server)
        file_name = rand_name('file') + '.txt'
        file_content = 'This is a test file'
        cls.file_details = cls. remote_instance.create_file(file_name, file_content)
        response = cls.flavors_client.get_flavor_details(cls.flavor_ref)
        cls.flavor = response.entity
        cls.resources.add(cls.server.id, cls.servers_client.delete_server)

    def setup_method(self, method):
        response = self.servers_client.get_server(self.server.id)
        server = response.entity
        # Only create new server if the current server is not active
        if server.status != NovaServerStatusTypes.ACTIVE:
            response = self.compute_provider.create_active_server()
            self.server = response.entity
            remote_instance = self.compute_provider.get_remote_instance_client(self.server)
            file_name = rand_name('file') + '.txt'
            file_content = 'This is a test file'
            self.file_details = remote_instance.create_file(file_name, file_content)
            response = self.flavors_client.get_flavor_details(self.flavor_ref)
            self.flavor = response.entity
            self.resources.add(self.server.id, self.servers_client.delete_server)

    @classmethod
    def tearDownClass(cls):
        super(ServerActionsBaseTests, cls).tearDownClass()

    @attr(type='positive', net='yes')
    def test_rebuild_server(self):
        """The server should be rebuilt using the provided image"""

        # Rebuild the server with the alt image id from config
        rebuilt_response = self.servers_client.rebuild(self.server.id, self.image_ref_alt)
        rebuilt_server = rebuilt_response.entity
        #Verify the properties in the initial response are correct
        self.assertEqual(self.server.id, rebuilt_server.id,
                         msg="Server id changed after rebuild")
        self.assertEqual(self.image_ref_alt, rebuilt_server.image.id,
                         msg="Server's Image ref was not updated to the new image ref")
        self.assertEqual(self.flavor_ref, rebuilt_server.flavor.id,
                         msg="Server's Flavor ref changed after rebuild")

        # Verify the server properties after the rebuild completes
        server_response = self.compute_provider.wait_for_server_status(rebuilt_server.id,
                                                                       NovaServerStatusTypes.ACTIVE)
        rebuilt_server_details = server_response.entity
        self.assertEquals(self.server.addresses, rebuilt_server_details.addresses,
                          msg="Server IP addresses changed after rebuild")
        self.assertEqual(self.server.created, rebuilt_server_details.created,
                         msg="Server Created date changed after rebuild")
        self.assertTrue(self.server.updated != rebuilt_server_details.updated,
                        msg="Server Updated date not changed after rebuild")

        rebuilt_server_details.adminPass = rebuilt_server.adminPass

#        Verify the instance can be accessed
#         Removing SSH call to debug IPv6 SSH issue that is causing tests to hang at this point (Daryl)
        public_address = self.compute_provider.get_public_ip_address(rebuilt_server_details)
        remote_client = self.compute_provider.get_remote_instance_client(rebuilt_server_details,
                                                                         public_address)
        assert remote_client.can_connect_to_public_ip(),\
            "Could not connect to rebuilt server (%s) using admin password %s" % (public_address, password)

        hostname = remote_client.get_hostname()
        self.assertEqual(rebuilt_server_details.name.lower(), hostname.lower(),
                         msg="The hostname was not the same as the server name after rebuild")



    @attr(type='negative', net='yes')
    def test_verify_full_server_resize_server_down(self):
        """B-36431 Problems with resize down on full server"""
        server_response = self.compute_provider.create_active_server(flavor_ref=self.flavor_ref_alt)
        server = server_response.entity
        testvolume_mountpoint = '/tmp'

        # Write 30 gb to disk
        blocksize = 1228800
        count = 25600
        remote_client = self.compute_provider.get_remote_instance_client(server)
        sshresp = remote_client.write_zeroes_data_to_disk(testvolume_mountpoint, 'file', blocksize, count)
        self.assertIsNotNone(sshresp, msg="File added")

        # Resize server
        self.servers_client.resize(server.id, self.flavor_ref)
        self.compute_provider.wait_for_server_status(server.id,
                                                     NovaServerStatusTypes.RESIZE)
        # Verify that we reached ERROR status
        self.compute_provider.wait_for_server_error_status(server.id,
                                                           NovaServerStatusTypes.ERROR)
        # Check for correct error and details
        resized_server_response = self.servers_client.get_server(server.id)
        resized_server = resized_server_response.entity

        # Verify the fault
        self.assertEqual('ProcessExecutionError', str(resized_server.fault.get('message')),
                         msg="Error Description didn't match")
        self.assertEqual(500, resized_server.fault.get('code'),
                         msg="Error code didn't match")


    @attr(type='positive', net='no')
    def test_verify_revert_from_error_mode(self):
        """B-34653 Revert resize from error"""
        server_response = self.compute_provider.create_active_server(flavor_ref=self.flavor_ref_alt)
        server = server_response.entity
        testvolume_mountpoint = '/tmp'

        # Write 30 gb to disk
        blocksize = 1228800
        count = 25600
        remote_client = self.compute_provider.get_remote_instance_client(server)
        sshresp = remote_client.write_zeroes_data_to_disk(testvolume_mountpoint,
                                                          'file', blocksize,
                                                          count)
        self.assertIsNotNone(sshresp, msg="File added")

        # Resize server
        self.servers_client.resize(server.id, self.flavor_ref)
        self.compute_provider.wait_for_server_status(server.id, NovaServerStatusTypes.RESIZE)

        # Verify that we reached ERROR status
        self.compute_provider.wait_for_server_error_status(server.id, NovaServerStatusTypes.ERROR)

        # Try to revert from Error mode
        self.servers_client.revert_resize(server.id)
        reverted_server_response = self.compute_provider.wait_for_server_status_from_error(server.id, NovaServerStatusTypes.ACTIVE)
        reverted_server = reverted_server_response.entity

        # Verify original flavor size
        self.assertEqual(self.flavor_ref_alt, server.flavor.id)


    @attr(type='negative', net='no')
    def test_verify_resize_with_disk_config_manual(self):
        """I-05687 DiskConfig issue with resize"""
        server_response = self.compute_provider.create_active_server(flavor_ref=self.flavor_ref_alt,
                                                                     disk_config='MANUAL')
        server = server_response.entity

        # Resize server and confirm
        with self.assertRaises(Forbidden):
            self.servers_client.resize(server.id, self.flavor_ref)

    @attr(type='positive', net='yes')
    def test_resize_instance_out_of_memory(self):
        """The server should still resize when instance is out of memory"""
        # Move the instance to Out of Memory status
        self.remote_instance.execute_resource_bomb()

        # Resize the instance
        self.servers_client.resize(self.server.id, self.flavor_ref_alt)
        self.compute_provider.wait_for_server_status(self.server.id, NovaServerStatusTypes.VERIFY_RESIZE)
        self.servers_client.confirm_resize(self.server.id)
        self.compute_provider.wait_for_server_status(self.server.id, NovaServerStatusTypes.ACTIVE)

    def _assert_server_details(self, server, expected_name, expected_accessIPv4,
                               expected_accessIPv6, expected_id,
                               expected_image_ref):
        self.assertEqual(expected_accessIPv4, server.accessIPv4,
                         msg="AccessIPv4 did not match")
        self.assertEqual(expected_accessIPv6, server.accessIPv6,
                         msg="AccessIPv6 did not match")
        self.assertEquals(self.config.nova.tenant_id, server.tenant_id,
                          msg="Tenant id did not match")
        self.assertEqual(expected_name, server.name,
                         msg="Server name did not match")
        self.assertTrue(server.host_id is not None,
                        msg="Host id was not set")
        self.assertEqual(expected_image_ref, server.image.id,
                         msg="Image id did not match")
        self.assertEqual(self.flavor_ref, server.flavor.id,
                         msg="Flavor id did not match")
        self.assertEqual(expected_id, server.id, msg="Server id did not match")

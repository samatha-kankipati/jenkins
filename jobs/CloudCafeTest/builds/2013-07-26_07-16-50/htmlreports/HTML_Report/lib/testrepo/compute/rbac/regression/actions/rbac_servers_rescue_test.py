from testrepo.common.testfixtures.compute import RbacComputeFixture
from ccengine.common.decorators import attr
from ccengine.common.tools.datagen import rand_name
from ccengine.domain.configuration import AuthConfig
from ccengine.common.exceptions.compute import Forbidden
from ccengine.domain.types import NovaServerStatusTypes, NovaServerRebootTypes
from ccengine.clients.compute.servers_api import ServerAPIClient
from ccengine.domain.types import NovaImageStatusTypes
from ccengine.domain.types import NovaServerStatusTypes
from ccengine.providers.configuration import MasterConfigProvider as _MCP
from ccengine.providers.compute.compute_api import ComputeAPIProvider \
                                                   as _ComputeAPIProvider


class RBACServerRescueTest(RbacComputeFixture):

    @classmethod
    def setUpClass(cls):
        super(RBACServerRescueTest, cls).setUpClass()
        # Creation of 1 servers needed for the tests
        active_server_response = cls.compute_provider.create_active_server()
        cls.server = active_server_response.entity
        cls.resources.add(cls.server.id,
                          cls.servers_client.delete_server)

    @classmethod
    def tearDownClass(cls):
        super(RBACServerRescueTest, cls).tearDownClass()

    @attr(type='smoke', net='no')
    def test_rescue_server_with_admin_role(self):
        """Rescue server with admin account should work"""
        active_server_response = self.compute_provider.create_active_server()
        server_personal = active_server_response.entity
        self.resources.add(server_personal.id,
                          self.servers_client.delete_server)
        rescue_response = self.servers_client.rescue(server_personal.id)
        changed_password = rescue_response.entity.adminPass
        self.assertEqual(200, rescue_response.status_code)
        self.assertTrue(server_personal.adminPass is not changed_password,
                        msg="The password did not change after Rescue.")
        #Enter rescue mode
        rescue_server_response = self.compute_provider.wait_for_server_status(
            server_personal.id, 
            'RESCUE')
        rescue_server = rescue_server_response.entity
        rescue_server.adminPass = changed_password

        remote_client = self.compute_provider.get_remote_instance_client(rescue_server)

        #Verify if hard drives are attached
        remote_client = self.compute_provider.get_remote_instance_client(rescue_server)
        partitions = remote_client.get_partition_details()
        self.assertEqual(3, len(partitions))
    
    @attr(type='smoke', net='no')
    def test_rescue_server_with_creator_role(self):
        """Rescue server with creator account should fail"""
        with self.assertRaises(Forbidden):
            self.creator_servers_client.rescue(self.server.id)
        self._assert_server_fail_rescue()
    
    @attr(type='smoke', net='no')
    def test_rescue_server_with_observer_role(self):
        """Rescue server with observer account should fail"""
        with self.assertRaises(Forbidden):
            self.observer_servers_client.rescue(self.server.id)
        self._assert_server_fail_rescue()
    
    def _assert_server_fail_rescue(self):
        get_server_response = self.servers_client.get_server(self.server.id)
        get_server = get_server_response.entity
        # Password did not change (Server wasn't rescued)
        remote_client = self.compute_provider.get_remote_instance_client(self.server)
        self.assertTrue(remote_client.can_connect_to_public_ip(),
                        msg="Cannot connect to server using public ip")
        self.assertTrue(get_server.status != 'RESCUE',
                        msg="Server is not in Rescue status")
    
    @attr(type='smoke', net='no')
    def test_unrescue_server_with_admin_role(self):
        """Unrescue server with admin account should work"""
        active_server_response = self.compute_provider.create_active_server()
        server_personal = active_server_response.entity
        self.resources.add(server_personal.id,
            self.servers_client.delete_server)
        rescue_response = self.servers_client.rescue(server_personal.id)
        self.assertEqual(200, rescue_response.status_code)
        rescue_server_response = self.compute_provider.wait_for_server_status(
            server_personal.id, 'RESCUE')
        unrescue_response = self.servers_client.unrescue(server_personal.id)
        self.assertEqual(202, unrescue_response.status_code)
        self.compute_provider.wait_for_server_status(server_personal.id, 'ACTIVE')
        remote_client = self.compute_provider.get_remote_instance_client(server_personal)
        partitions = remote_client.get_partition_details()
        self.assertEqual(2, len(partitions), msg="The number of partitions after unrescue were not two.")
        flavor_response = self.flavors_client.get_flavor_details(self.flavor_ref)
        flavor = flavor_response.entity
        result, message = remote_client.verify_partitions(flavor.disk, flavor.swap, 'active', partitions)
        self.assertTrue(result, msg=message)

    
    @attr(type='smoke', net='no')
    def test_unrescue_server_with_creator_role(self):
        """Unrescue server with creator account should fail"""
        active_server_response = self.compute_provider.create_active_server()
        server_personal = active_server_response.entity
        self.resources.add(server_personal.id,
            self.servers_client.delete_server)
        rescue_response = self.servers_client.rescue(server_personal.id)
        self.assertEqual(200, rescue_response.status_code)
        rescue_server_response = self.compute_provider.wait_for_server_status(
            server_personal.id, 'RESCUE')
        with self.assertRaises(Forbidden):
            self.creator_servers_client.unrescue(self.server.id)
        self._assert_server_fail_unrescue(server_personal)
    
    @attr(type='smoke', net='no')
    def test_unrescue_server_with_observer_role(self):
        """Unrescue server with observer account should fail"""
        active_server_response = self.compute_provider.create_active_server()
        server_personal = active_server_response.entity
        self.resources.add(server_personal.id,
            self.servers_client.delete_server)
        rescue_response = self.servers_client.rescue(server_personal.id)
        self.assertEqual(200, rescue_response.status_code)
        rescue_server_response = self.compute_provider.wait_for_server_status(
            server_personal.id, 'RESCUE')
        with self.assertRaises(Forbidden):
            self.observer_servers_client.unrescue(self.server.id)
        self._assert_server_fail_unrescue(server_personal)

    def _assert_server_fail_unrescue(self, server_personal):
        get_server_response = self.servers_client.get_server(server_personal.id)
        get_server = get_server_response.entity
        self.assertTrue(get_server.status == 'RESCUE',
                        msg="Server has not been rescued status")
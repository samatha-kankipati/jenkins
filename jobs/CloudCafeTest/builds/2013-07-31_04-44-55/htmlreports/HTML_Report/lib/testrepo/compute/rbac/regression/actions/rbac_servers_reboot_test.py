from testrepo.common.testfixtures.compute import RbacComputeFixture
from ccengine.common.decorators import attr
import time
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


class RBACServerRebootTest(RbacComputeFixture):

    @classmethod
    def setUpClass(cls):
        super(RBACServerRebootTest, cls).setUpClass()
        # Creation of 1 servers needed for the tests
        active_server_response = cls.compute_provider.create_active_server()
        cls.server = active_server_response.entity
        cls.resources.add(cls.server.id,
                          cls.servers_client.delete_server)

    @classmethod
    def tearDownClass(cls):
        super(RBACServerRebootTest, cls).tearDownClass()

    @attr(type='smoke', net='no')
    def test_reboot_server_with_admin_role(self):
        """Reboot server with admin account should work"""
        cons = 1
        public_address = self.compute_provider.get_public_ip_address(self.server)
        remote_instance = self.compute_provider.get_remote_instance_client(
            self.server, 
            public_address)
        uptime_start = remote_instance.get_uptime()
        start = time.time()
        
        reboot_type = NovaServerRebootTypes.HARD
        reboot_response = self.servers_client.reboot(self.server.id, 
                                                     reboot_type)
        self.assertEqual(202, reboot_response.status_code)
        
        remote_client = self.compute_provider.get_remote_instance_client(
            self.server, 
            public_address)
        finish = time.time()
        uptime_post_reboot = remote_client.get_uptime()
        self.assertLess(uptime_post_reboot, (uptime_start + (finish - start) + cons))
    
    @attr(type='smoke', net='no')
    def test_reboot_server_with_creator_role(self):
        """Reboot server with creator account should fail"""
        public_address = self.compute_provider.get_public_ip_address(self.server)
        remote_instance = self.compute_provider.get_remote_instance_client(
            self.server, 
            public_address)
        uptime_start = remote_instance.get_uptime()
        start = time.time()
        reboot_type = NovaServerRebootTypes.HARD
        with self.assertRaises(Forbidden):
            self.creator_servers_client.reboot(self.server.id, 
                                               reboot_type)
        self._assert_server_not_rebooted(public_address, uptime_start, start)

    @attr(type='smoke', net='no')
    def test_reboot_server_with_observer_role(self):
        """Reboot server with observer account should fail"""
        public_address = self.compute_provider.get_public_ip_address(self.server)
        remote_instance = self.compute_provider.get_remote_instance_client(
            self.server, 
            public_address)
        uptime_start = remote_instance.get_uptime()
        start = time.time()
        reboot_type = NovaServerRebootTypes.HARD
        with self.assertRaises(Forbidden):
            self.observer_servers_client.reboot(self.server.id, 
                                                reboot_type)
        self._assert_server_not_rebooted(public_address, uptime_start, start)
        
    def _assert_server_not_rebooted(self, public_address, uptime_start, start):
        '''Verify Server not rebooted'''
        remote_client = self.compute_provider.get_remote_instance_client(
            self.server, 
            public_address)
        finish = time.time()
        uptime_post_reboot = remote_client.get_uptime()
        self.assertGreater(uptime_post_reboot, (uptime_start + (finish - start)))
from testrepo.common.testfixtures.compute import ComputeFixture
from ccengine.domain.types import NovaServerStatusTypes, NovaServerRebootTypes
import time
from ccengine.common.tools.datagen import rand_name
from ccengine.common.tools.equality_tools import EqualityTools
from ccengine.common.exceptions.compute import Forbidden
from ccengine.common.decorators import attr
import base64


class RebootServerHardTests(ComputeFixture):

    @classmethod
    def setUpClass(cls):
        super(RebootServerHardTests, cls).setUpClass()
        response = cls.compute_provider.create_active_server()
        cls.server = response.entity
        cls.resources.add(cls.server.id, cls.servers_client.delete_server)

    @classmethod
    def tearDownClass(cls):
        super(RebootServerHardTests, cls).tearDownClass()

    @attr(type='smoke', net='yes')
    def test_reboot_server_hard(self):
        """ The server should be power cycled """
        public_address = self.compute_provider.get_public_ip_address(self.server)
        remote_instance = self.compute_provider.get_remote_instance_client(self.server, public_address)
        uptime_start = remote_instance.get_uptime()
        start = time.time()

        self.compute_provider.reboot_and_await(self.server.id, NovaServerRebootTypes.HARD)
        remote_client = self.compute_provider.get_remote_instance_client(self.server, public_address)
        finish = time.time()
        uptime_post_reboot = remote_client.get_uptime()
        self.assertLess(uptime_post_reboot, (uptime_start + (finish - start)))


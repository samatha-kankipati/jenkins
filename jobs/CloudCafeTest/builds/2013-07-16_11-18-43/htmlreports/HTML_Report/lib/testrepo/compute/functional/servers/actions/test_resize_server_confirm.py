from testrepo.common.testfixtures.compute import ComputeFixture
from ccengine.domain.types import NovaServerStatusTypes, NovaServerRebootTypes
import time
from ccengine.common.tools.datagen import rand_name
from ccengine.common.tools.equality_tools import EqualityTools
from ccengine.common.exceptions.compute import Forbidden
from ccengine.common.decorators import attr
import base64


class ResizeServerUpConfirmTests(ComputeFixture):

    @classmethod
    def setUpClass(cls):
        super(ResizeServerUpConfirmTests, cls).setUpClass()
        server_response = cls.compute_provider.create_active_server()
        server_to_resize = server_response.entity
        cls.resources.add(server_to_resize.id, cls.servers_client.delete_server)

        # resize server and confirm
        cls.servers_client.resize(server_to_resize.id, cls.flavor_ref_alt)
        cls.compute_provider.wait_for_server_status(server_to_resize.id,
                                                    NovaServerStatusTypes.VERIFY_RESIZE)

        cls.servers_client.confirm_resize(server_to_resize.id)
        cls.compute_provider.wait_for_server_status(server_to_resize.id,
                                                    NovaServerStatusTypes.ACTIVE)
        resized_server_response = cls.servers_client.get_server(server_to_resize.id)
        cls.resized_server = resized_server_response.entity
        cls.resized_server.adminPass = server_to_resize.adminPass

    @classmethod
    def tearDownClass(cls):
        super(ResizeServerUpConfirmTests, cls).tearDownClass()

    @attr(type='smoke', net='no')
    def test_verify_confirm_resize_response(self):
        pass

    @attr(type='smoke', net='no')
    def test_server_properties_after_resize(self):
        self.assertEqual(self.flavor_ref_alt, self.resized_server.flavor.id)

    @attr(type='smoke', net='yes')
    def test_ram_and_disk_size_on_resize_up_server_confirm_test(self):
        """
        The server's RAM and disk space should be modified to that of
        the provided flavor
        """

        new_flavor = self.flavors_client.get_flavor_details(self.flavor_ref_alt).entity
        public_address = self.compute_provider.get_public_ip_address(self.resized_server)

        remote_instance = self.compute_provider.get_remote_instance_client(self.resized_server, public_address)

        lower_limit = int(new_flavor.ram) - (int(new_flavor.ram) * .1)
        server_ram_size = int(remote_instance.get_ram_size_in_mb())
        server_swap_size = int(remote_instance.get_swap_size_in_mb())
        self.assertTrue(int(new_flavor.ram) == server_ram_size or lower_limit <= server_ram_size,
                        msg="Ram size after confirm-resize did not match. Expected ram size : %s, Actual ram size : %s" % (new_flavor.ram, server_ram_size))
        self.assertEquals(int(new_flavor.swap), server_swap_size,
                        msg="Swap size after confirm-resize did not match. Expected swap size : %s, Actual swap size : %s" % (new_flavor.swap, server_swap_size))
        self.assertTrue(EqualityTools.are_sizes_equal(new_flavor.disk, remote_instance.get_disk_size_in_gb(self.config.compute_api.instance_disk_path), 0.5),
                        msg="Disk size %s after confirm-resize did not match size %s" % (remote_instance.get_disk_size_in_gb(self.config.compute_api.instance_disk_path), new_flavor.disk))


class ResizeServerDownConfirmTests(ComputeFixture):

    @classmethod
    def setUpClass(cls):
        super(ResizeServerDownConfirmTests, cls).setUpClass()
        server_response = cls.compute_provider.create_active_server(flavor_ref=cls.flavor_ref_alt)
        server_to_resize = server_response.entity
        cls.resources.add(server_to_resize.id, cls.servers_client.delete_server)

        # resize server and confirm
        cls.servers_client.resize(server_to_resize.id, cls.flavor_ref)
        cls.compute_provider.wait_for_server_status(server_to_resize.id,
                                                    NovaServerStatusTypes.VERIFY_RESIZE)

        cls.servers_client.confirm_resize(server_to_resize.id)
        cls.compute_provider.wait_for_server_status(server_to_resize.id,
                                                    NovaServerStatusTypes.ACTIVE)
        resized_server_response = cls.servers_client.get_server(server_to_resize.id)
        cls.resized_server = resized_server_response.entity
        cls.resized_server.adminPass = server_to_resize.adminPass

    @classmethod
    def tearDownClass(cls):
        super(ResizeServerDownConfirmTests, cls).tearDownClass()

    @attr(type='smoke', net='no')
    def test_verify_confirm_resize_response(self):
        pass

    @attr(type='smoke', net='no')
    def test_server_properties_after_resize(self):
        self.assertEqual(self.flavor_ref, self.resized_server.flavor.id)

    @attr(type='smoke', net='yes')
    def test_ram_and_disk_size_on_resize_up_server_confirm_test(self):
        """
        The server's RAM and disk space should be modified to that of
        the provided flavor
        """

        new_flavor = self.flavors_client.get_flavor_details(self.flavor_ref).entity
        public_address = self.compute_provider.get_public_ip_address(self.resized_server)
        remote_instance = self.compute_provider.get_remote_instance_client(self.resized_server, public_address)

        lower_limit = int(new_flavor.ram) - (int(new_flavor.ram) * .1)
        server_ram_size = int(remote_instance.get_ram_size_in_mb())
        server_swap_size = int(remote_instance.get_swap_size_in_mb())
        self.assertTrue(int(new_flavor.ram) == server_ram_size or lower_limit <= server_ram_size,
                        msg="Ram size after confirm-resize did not match. Expected ram size : %s, Actual ram size : %s" % (new_flavor.ram, server_ram_size))
        self.assertEquals(int(new_flavor.swap), server_swap_size,
                        msg="Swap size after confirm-resize did not match. Expected swap size: %s, Actual swap size: %s" % (new_flavor.swap, server_swap_size))
        self.assertTrue(EqualityTools.are_sizes_equal(new_flavor.disk, remote_instance.get_disk_size_in_gb(self.config.compute_api.instance_disk_path), 0.5),
                        msg="Disk size %s after confirm-resize did not match size %s" % (remote_instance.get_disk_size_in_gb(self.config.compute_api.instance_disk_path), new_flavor.disk))

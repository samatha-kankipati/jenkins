from testrepo.common.testfixtures.compute import ComputeFixture
import unittest2 as unittest
import base64
from ccengine.domain.types import NovaServerStatusTypes
from ccengine.common.tools.datagen import rand_name
from ccengine.common.decorators import attr
from datetime import datetime


class CreateServerTest(ComputeFixture):

    @classmethod
    def setUpClass(cls):
        super(CreateServerTest, cls).setUpClass()
        cls.name = rand_name("cctestserver")
        cls.file_contents = 'This is a test file.'
        cls.personality = [{'path': '/root/.csivh', 'contents':
                            base64.b64encode(cls.file_contents)}]
        cls.metadata = {'meta_key_1': 'meta_value_1',
                        'meta_key_2': 'meta_value_2'}
        cls.create_resp = cls.servers_client.create_server(cls.name, cls.image_ref, cls.flavor_ref,
                                                           personality=cls.personality,
                                                           metadata=cls.metadata)
        created_server = cls.create_resp.entity
        wait_response = cls.compute_provider.wait_for_server_status(created_server.id,
                                                                    NovaServerStatusTypes.ACTIVE)
        wait_response.entity.adminPass = created_server.adminPass
        cls.image = cls.images_client.get_image(cls.image_ref).entity
        cls.flavor = cls.flavors_client.get_flavor_details(cls.flavor_ref).entity
        cls.server = wait_response.entity

    @classmethod
    def tearDownClass(cls):
        super(CreateServerTest, cls).tearDownClass()

    @attr(type='smoke', net='no')
    def test_create_server_response(self):
        """Verify the parameters are correct in the initial response"""

        self.assertTrue(self.server.id is not None,
                        msg="Server id was not set in the response")
        self.assertTrue(self.server.adminPass is not None,
                        msg="Admin password was not set in the response")
        self.assertTrue(self.server.links is not None,
                        msg="Server links were not set in the response")

    @attr(type='smoke', net='no')
    def test_created_server_fields(self):
        """Verify that a created server has all expected fields"""
        message = "Expected {0} to be {1}, was {2}."

        self.assertEqual(self.server.progress, 100,
                         msg=message.format('server progress', '100',
                                            self.server.progress))
        self.assertEquals(self.server.tenant_id,
                          str(self.config.compute_api.tenant_id),
                          msg=message.format('tenant id',
                                             str(self.config.compute_api.tenant_id),
                                             self.server.tenant_id))
        self.assertEqual(self.server.name, self.name,
                         msg=message.format('server name', self.server.name,
                                            self.name))
        self.assertTrue(self.server.hostId is not None,
                        msg='Expected host id to be set.')
        self.assertEqual(self.image_ref, self.server.image.id,
                         msg=message.format('image id', self.image_ref,
                                            self.server.image.id))
        self.assertEqual(self.server.flavor.id, self.flavor_ref,
                         msg=message.format('flavor id', self.flavor_ref,
                                            self.server.flavor.id))
        self.assertTrue(self.server.created is not None,
                        msg="Expected server created date to be set, was null.")
        self.assertTrue(self.server.updated is not None,
                        msg="Expected server updated date to be set, was null.")
        self.assertGreaterEqual(self.server.updated, self.server.created,
                                msg="Expected server updated date to be before the created date.")

    @attr(type='smoke', net='no')
    def test_server_access_addresses(self):
        """If the server has public addresses, the access IP addresses should be same as the public addresses"""
        addresses = self.server.addresses
        if addresses.public is not None:
            self.assertTrue(addresses.public.ipv4 is not None,
                            msg="Expected server to have a public IPv4 address set.")
            self.assertTrue(addresses.public.ipv6 is not None,
                            msg="Expected server to have a public IPv6 address set.")
            self.assertTrue(addresses.private.ipv4 is not None,
                            msg="Expected server to have a private IPv4 address set.")
            self.assertEqual(addresses.public.ipv4, self.server.accessIPv4,
                             msg="Expected access IPv4 address to be {0}, was {1}.".format(
                                 addresses.public.ipv4, self.server.accessIPv4))
            self.assertEqual(addresses.public.ipv6, self.server.accessIPv6,
                             msg="Expected access IPv6 address to be {0}, was {1}.".format(
                                 addresses.public.ipv6, self.server.accessIPv6))

    @attr(type='smoke', net='yes')
    def test_created_server_vcpus(self):
        """Verify the number of vCPUs reported matches the amount set by the flavor"""

        remote_client = self.compute_provider.get_remote_instance_client(self.server)
        server_actual_vcpus = remote_client.get_number_of_vcpus()
        self.assertEqual(server_actual_vcpus, self.flavor.vcpus,
                         msg="Expected number of vcpus to be {0}, was {1}.".format(
                             self.flavor.vcpus, server_actual_vcpus))

    @attr(type='smoke', net='yes')
    def test_created_server_disk_size(self):
        """Verify the size of the virtual disk matches the size set by the flavor"""
        remote_client = self.compute_provider.get_remote_instance_client(self.server)
        disk_size = remote_client.get_disk_size_in_gb(self.config.compute_api.instance_disk_path)
        self.assertEqual(disk_size, self.flavor.disk,
                         msg="Expected disk to be {0} GB, was {1} GB".format(
                         self.flavor.disk, disk_size))

    @attr(type='smoke', net='yes')
    def test_created_server_hostname(self):
        """Verify that the hostname of the server is the same as the server name"""
        remote_client = self.compute_provider.get_remote_instance_client(self.server)
        hostname = remote_client.get_hostname()
        self.assertEqual(hostname, self.name,
                         msg="Expected hostname to be {0}, was {1}".format(
                         self.name, hostname))

    @attr(type='smoke', net='yes')
    def test_can_log_into_created_server(self):
        """Tests that we can log into the created server"""
        remote_client = self.compute_provider.get_remote_instance_client(self.server)
        self.assertTrue(remote_client.can_connect_to_public_ip(),
                        msg="Cannot connect to server using public ip")

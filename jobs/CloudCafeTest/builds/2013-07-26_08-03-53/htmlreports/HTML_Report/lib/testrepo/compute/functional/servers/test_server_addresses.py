from testrepo.common.testfixtures.compute import ComputeFixture, \
    CreateServerFixture
from ccengine.common.exceptions.compute import ItemNotFound
from ccengine.domain.types import NovaServerStatusTypes
from ccengine.common.tools.datagen import rand_name
from ccengine.common.decorators import attr


class ServerAddressesTest(CreateServerFixture):

    @classmethod
    def setUpClass(cls):
        cls.name = rand_name("testserver")
        super(ServerAddressesTest, cls).setUpClass(name=cls.name)
        cls.server = cls.server_response.entity

    @classmethod
    def tearDownClass(cls):
        super(ServerAddressesTest, cls).tearDownClass()

    @attr(type='smoke', net='yes')
    def test_list_addresses(self):
        """All public and private addresses for a server should be returned"""
        expected_addresses = self.server.addresses
        self.addr_list = self.servers_client.list_addresses(self.created_server.id)
        actual_addresses = self.addr_list.entity
        self.assertTrue(actual_addresses is not None,
                        "List addresses did not return any addresses")
        self.assertEqual(expected_addresses, actual_addresses,
                         "Addresses returned by List addresses request is not same as the addresses returned in Get server request")
        if len(actual_addresses.public.addresses) > 0:
            remote_client = self.compute_provider.get_remote_instance_client(self.server)
            self.assertTrue(remote_client.can_connect_to_public_ip(),
                            "Cannot connect to server using public ip")
        if len(actual_addresses.private.addresses) > 0:
            self._assert_private_addresses(actual_addresses.private.addresses)

    def _assert_private_addresses(self, private_addresses):
        remote_client = self.compute_provider.get_remote_instance_client(self.server)
        self.assertTrue(remote_client.can_remote_ping_private_ip(private_addresses),
                        "Cannot access the server using private address")

    @attr(type='smoke', net='yes')
    def test_list_addresses_by_network(self):
        """Providing a network type should filter the addresses return by that type"""
        expected_addresses = self.server.addresses
        self.actual_addresses = self.servers_client.list_addresses_by_network(self.created_server.id,
                                                                              'public')
        public_addresses = self.actual_addresses.entity.public
        self.assertEqual(expected_addresses.public, public_addresses,
                         "Addresses returned by List addresses by public type did not match addresses returned by get server")
        if len(public_addresses.addresses) > 0:
            remote_client = self.compute_provider.get_remote_instance_client(self.server)
            self.assertTrue(remote_client.can_ping_public_ip(public_addresses.addresses,
                            self.config.compute_api.ip_address_version_for_ssh),
                            "Cannot connect to server using public ip")

        self.actual_addresses = self.servers_client.list_addresses_by_network(self.created_server.id,
                                                                              'private')
        private_addresses = self.actual_addresses.entity.private
        self.assertEqual(expected_addresses.private, private_addresses,
                         "Addresses returned by List addresses by private type did not match addresses returned by get server")
        if len(private_addresses.addresses) > 0:
            self._assert_private_addresses(private_addresses.addresses)

    @attr(type='positive', net='no')
    def test_list_addresses_by_invalid_network(self):
        """Providing a network type should filter the addresses return by that type"""
        with self.assertRaises(ItemNotFound):
            self.servers_client.list_addresses_by_network(self.server.id, 'voldemort')

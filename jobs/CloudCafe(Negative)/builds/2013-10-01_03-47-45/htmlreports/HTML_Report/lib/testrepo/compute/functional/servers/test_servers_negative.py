from testrepo.common.testfixtures.compute import ComputeFixture
from ccengine.common.exceptions.compute import BadRequest, ItemNotFound
from ccengine.common.tools.datagen import rand_name
from ccengine.common.decorators import attr
import unittest2 as unittest


class ServersNegativeTest(ComputeFixture):

    @classmethod
    def setUpClass(cls):
        super(ServersNegativeTest, cls).setUpClass()
        cls.low_limit_user = cls.low_limit_conf.auth.low_limit_username
        cls.other_api_key = cls.low_limit_conf.auth.low_limit_user_password
        cls.low_limit_tenant_name = cls.compute_provider_for_low_limits_user.tenant_id
        cls.low_limit_user_region = cls.compute_provider_for_low_limits_user.compute_region
        cls.windows_image_ref = cls.low_limit_conf.compute_api.windows_image_ref

    @classmethod
    def tearDownClass(cls):
        """Implemented in Compute Fixture, method present here only for clean structure"""
        super(ServersNegativeTest, cls).tearDownClass()

    @attr(type='negative', net='no')
    def test_server_name_blank(self):
        with self.assertRaises(BadRequest):
                self.servers_client.create_server('', self.image_ref, self.flavor_ref)

    @attr(type='negative', net='no')
    def test_image_min_ram_not_met(self):
        """Server should not get created with an image whose min ram is larger then ram of the flavor used"""
        with self.assertRaises(BadRequest):
            server = self.servers_client.create_server('winserver', self.windows_image_ref, 1)
            self.servers_client.delete_server(server.enity.id)
            self.fail('Image min RAM requirement was not respected')

    @attr(type='negative', net='no')
    def test_personality_file_contents_not_encoded(self):
        """Server should not get created with a personality file whose content is not encoded"""
        file_contents = 'This is a test file.'
        personality = [{'path': '/etc/testfile.txt',
                        'contents': file_contents}]
        with self.assertRaises(BadRequest):
            server = self.servers_client.create_server('blankfile',
                                                       self.image_ref, self.flavor_ref,
                                                       personality=personality)

    @attr(type='negative', net='no')
    def test_invalid_ip_v4_access_address(self):
        """Negative test: Server should not get created with invalid ipv4 address"""
        accessIPv4 = '1.1.1.1.1.1'
        name = rand_name("testserver")
        with self.assertRaises(BadRequest):
            server_response = self.servers_client.create_server(name,
                                                                self.image_ref,
                                                                self.flavor_ref,
                                                                accessIPv4=accessIPv4)

    @attr(type='negative', net='no')
    def test_invalid_ip_v6_access_address(self):
        """Negative test: Server should not get created with invalid ipv6 address"""
        accessIPv6 = '2.2.2.2'
        name = rand_name("testserver")
        with self.assertRaises(BadRequest):
            server_response = self.servers_client.create_server(name,
                                                                self.image_ref,
                                                                self.flavor_ref,
                                                                accessIPv6=accessIPv6)

    @attr(type='negative', net='no')
    def test_server_metadata_item_nonexistent_server(self):
        """Negative test: GET on nonexistent server should not succeed"""
        with self.assertRaises(ItemNotFound):
            self.servers_client.get_server_metadata_item(999, 'test2')

    @attr(type='negative', net='no')
    def test_list_server_metadata_nonexistent_server(self):
        """List metadata on a non existent server should not succeed"""
        with self.assertRaises(ItemNotFound):
                self.servers_client.list_server_metadata(999)

    @attr(type='negative', net='no')
    def test_set_server_metadata_nonexistent_server(self):
        """Set metadata on a non existent server should not succeed"""
        meta = {'meta1': 'data1'}

        with self.assertRaises(ItemNotFound):
            metadata_response = self.servers_client.set_server_metadata(999, meta)

    @attr(type='negative', net='no')
    def test_update_server_metadata_nonexistent_server(self):
        """An update should not happen for a non existent image"""
        meta = {'key1': 'value1', 'key2': 'value2'}
        with self.assertRaises(ItemNotFound):
            self.servers_client.update_server_metadata(999, meta)

    @attr(type='negative', net='no')
    def test_delete_server_metadata_item_nonexistent_server(self):
        """Should not be able to delete metadata item from a non existent server"""
        with self.assertRaises(ItemNotFound):
            self.servers_client.delete_server_metadata_item(999, 'delkey')

    @attr(type='negative', net='no')
    def test_create_server_with_unknown_flavor(self):
        """Server creation with a flavor ID which does not exist, should not be allowed"""
        with self.assertRaises(BadRequest):
            self.servers_client.create_server('testserver', self.image_ref, 999)

    @attr(type='negative', net='no')
    def test_create_server_with_unknown_image(self):
        """Server creation with an image ID which does not exist,should not be allowed"""
        with self.assertRaises(BadRequest):
            self.servers_client.create_server('testserver', 999, self.flavor_ref)

    @attr(type='negative', net='no')
    def test_get_nonexistent_server_fails(self):
        """Making a get request for a server that does not exist should cause a 404"""
        with self.assertRaises(ItemNotFound):
            self.servers_client.get_server(999)

    @attr(type='negative', net='no')
    def test_delete_nonexistent_server_fails(self):
        """Making a delete request for a server that does not exist should cause a 404"""
        with self.assertRaises(ItemNotFound):
            self.servers_client.delete_server(999)

    @attr(type='negative', net='no')
    def test_list_addresses_for_nonexistant_server_fails(self):
        """Making a list address request for a server that does not exist should cause a 404"""
        with self.assertRaises(ItemNotFound):
            self.servers_client.list_addresses(999)

    @attr(type='negative', net='no')
    def test_list_addresses_for_invalid_network_id_fails(self):
        """Making a list address request for a server that does not exist should cause a 404"""
        server_response = self.compute_provider.create_active_server()
        server = server_response.entity
        with self.assertRaises(ItemNotFound):
            self.servers_client.list_addresses_by_network(server.id, 999)

    @attr(type='negative', net='no')
    def test_list_addresses_by_network_for_nonexistant_server_fails(self):
        """Making a list address by network request for a server that does not exist should cause a 404"""
        with self.assertRaises(ItemNotFound):
            self.servers_client.list_addresses_by_network(999, 'public')

    @attr(type='negative', net='no')
    def test_create_server_with_invalid_admin_password(self):
        """
        If an password is invalid - i.e a number or an empty string for Linux then a BadRequest error should be thrown
        """

        if self.config.misc.serializer == "xml":
            raise BadRequest('xml')
        else:
            self.name = rand_name("testserver")
            with self.assertRaises(BadRequest):
                self.servers_client.create_server(self.name, self.image_ref, self.flavor_ref, adminPass=4)

    @attr(type='negative', net='no')
    def test_server_is_not_created_when_access_ips_value_are_blank(self):
        """A 400 Response should be returned when a server is created with blank access ip value"""

        if self.config.misc.serializer == "xml":
            raise BadRequest('xml')

        else:
            self.name = rand_name("testserver")

            with self.assertRaises(BadRequest):
                self.servers_client.create_server(self.name, self.image_ref, self.flavor_ref, accessIPv4='')

            with self.assertRaises(BadRequest):
                self.servers_client.create_server(self.name, self.image_ref, self.flavor_ref, accessIPv6='')

    @attr('negative')
    @attr(type='negative', net='no')
    def test_server_is_not_updated_when_access_ips_value_are_blank(self):
        """A 400 Response should be returned when a server is updated with blank access ip value"""

        if self.config.misc.serializer == "xml":
            raise BadRequest('xml')
        else:
            server_before_update_request = self.compute_provider.create_active_server()

        with self.assertRaises(BadRequest):
            updated_server = self.servers_client.update_server(server_before_update_request.entity.id, accessIPv4='')

        with self.assertRaises(BadRequest):
            updated_server = self.servers_client.update_server(server_before_update_request.entity.id,
                                                               accessIPv6='')
            server_after_update_request = self.servers_client.get_server(server_before_update_request.entity.id)

            self.assertEqual(server_before_update_request.entity.accessIPv4,
                             server_after_update_request.entity.accessIPv4,
                             "The server's accessIPv4 was updated")
            self.assertEqual(server_before_update_request.entity.accessIPv6,
                             server_after_update_request.entity.accessIPv6,
                             "The server's accessIPv6 was updated")

    @attr(type='negative', net='no')
    def test_cannot_get_deleted_server(self):
        """A 400 response should be returned when you get a server which is deleted"""
        server = self.compute_provider.create_active_server()
        delete_resp = self.servers_client.delete_server(server.entity.id)
        self.assertEqual(204, delete_resp.status_code)
        self.compute_provider.wait_for_server_to_be_deleted(server.entity.id)
        with self.assertRaises(ItemNotFound):
            self.servers_client.get_server(server.entity.id)

    @attr(type='negative', net='no')
    def test_create_server_with_invalid_name(self):
        """Server creation with a blank/invalid name should not be allowed"""
        with self.assertRaises(BadRequest):
            self.servers_client.create_server('', self.image_ref, self.flavor_ref)

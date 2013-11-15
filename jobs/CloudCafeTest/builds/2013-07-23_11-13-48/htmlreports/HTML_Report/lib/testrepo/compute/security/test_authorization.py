from testrepo.common.testfixtures.compute import ComputeFixture

from ccengine.common.exceptions.compute import ItemNotFound, Unauthorized
from ccengine.common.decorators import attr
from ccengine.domain.configuration import AuthConfig
from ccengine.clients.compute.servers_api import ServerAPIClient
from ccengine.providers.configuration import MasterConfigProvider as _MCP
from ccengine.providers.compute.compute_api import ComputeAPIProvider \
                                                   as _ComputeAPIProvider
import unittest2 as unittest


class AuthorizationTest(ComputeFixture):

    @classmethod
    def setUpClass(cls):
        super(AuthorizationTest, cls).setUpClass()
        cls.server = cls.compute_provider.create_active_server()
        cls.resources.add(cls.server.entity.id, cls.servers_client.delete_server)

        # Initialize compute provider for other user
        config = _MCP()
        other_user_auth = {AuthConfig.SECTION_NAME: {'username': config.auth.low_limit_username, 'api_key': config.auth.low_limit_user_password}}
        other_user_conf = config.mcp_override(other_user_auth)
        cls.compute_provider_for_other_user = _ComputeAPIProvider(other_user_conf)
        cls.compute_provider_for_other_user.compute_public_url = cls.compute_provider.compute_public_url
        cls.compute_provider_for_other_user.tenant_id = cls.compute_provider.tenant_id
        other_user_server_client = ServerAPIClient(url=cls.compute_provider_for_other_user.compute_public_url,
                                                   tenant_id=cls.compute_provider_for_other_user.tenant_id,
                                                   auth_token=cls.compute_provider_for_other_user.auth_token)
        cls.compute_provider_for_other_user.servers_client = other_user_server_client

    @classmethod
    def tearDownClass(cls):
        super(AuthorizationTest, cls).tearDownClass()

    @attr(type='negative', net='no')
    def test_get_server_for_other_account_fails(self):
        """A get request for a server on another user's account should fail"""
        with self.assertRaises(ItemNotFound):
            self.compute_provider_for_low_limits_user.servers_client.get_server(self.server.entity.id)

    @attr(type='negative', net='no')
    def test_delete_server_for_other_account_fails(self):
        """A delete request for a server on another user's account should fail"""
        with self.assertRaises(ItemNotFound):
            self.compute_provider_for_low_limits_user.servers_client.delete_server(self.server.entity.id)

    @attr(type='negative', net='no')
    @unittest.skip('Bug: D-03818')
    def test_update_server_for_other_account_fails(self):
        """An update server request for a server on another user's account should fail"""
        with self.assertRaises(Unauthorized):
            self.compute_provider_for_low_limits_user.servers_client.update_server(self.server.entity.id, name='test_auth_server')

    @attr(type='negative', net='no')
    def test_list_server_addresses_for_other_account_fails(self):
        """A list addresses request for a server on another user's account should fail"""
        with self.assertRaises(ItemNotFound):
            self.compute_provider_for_low_limits_user.servers_client.list_addresses(self.server.entity.id)

    @attr(type='negative', net='no')
    def test_list_server_addresses_by_network_for_other_account_fails(self):
        """A list addresses by network request for a server on another user's account should fail"""
        with self.assertRaises(ItemNotFound):
            self.compute_provider_for_low_limits_user.servers_client.list_addresses_by_network(self.server.entity.id, 'public')

    @attr(type='negative', net='no')
    def test_change_password_for_other_account_fails(self):
        """A change password request for a server on another user's account should fail"""
        with self.assertRaises(ItemNotFound):
            self.compute_provider_for_low_limits_user.servers_client.change_password(self.server.entity.id, 'newpass')

    @attr(type='negative', net='no')
    def test_reboot_server_for_other_account_fails(self):
        """A reboot request for a server on another user's account should fail"""
        with self.assertRaises(ItemNotFound):
            self.compute_provider_for_low_limits_user.servers_client.reboot(self.server.entity.id, 'HARD')

    @attr(type='negative', net='no')
    def test_rebuild_server_for_other_account_fails(self):
        """A rebuild request for a server on another user's account should fail"""
        with self.assertRaises(ItemNotFound):
            self.compute_provider_for_low_limits_user.servers_client.rebuild(self.server.entity.id, self.image_ref_alt)

    @attr(type='negative', net='no')
    def test_resize_server_for_other_account_fails(self):
        """A resize request for a server on another user's account should fail"""
        with self.assertRaises(ItemNotFound):
            self.compute_provider_for_low_limits_user.servers_client.resize(self.server.entity.id, self.flavor_ref_alt)

    @attr(type='negative', net='no')
    def test_create_image_for_other_account_fails(self):
        """A create image request for a server on another user's account should fail"""
        with self.assertRaises(ItemNotFound):
            self.compute_provider_for_low_limits_user.servers_client.create_image(self.server.entity.id, 'testImage')

    @attr(type='negative', net='no')
    def test_server_creation_fails_when_tenant_is_incorrect(self):
        """Creation of server with wrong tenant ID should fail"""
        with self.assertRaises(Unauthorized):
            self.compute_provider_for_other_user.create_active_server()

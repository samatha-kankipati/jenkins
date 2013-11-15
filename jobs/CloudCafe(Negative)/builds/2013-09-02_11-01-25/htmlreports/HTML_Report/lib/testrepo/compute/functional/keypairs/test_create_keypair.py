from ccengine.common.decorators import attr
from ccengine.common.tools.datagen import rand_name
from ccengine.common.exceptions.compute import ActionInProgress

from testrepo.common.testfixtures.compute import ComputeFixture


class CreateKeypairTest(ComputeFixture):

    @classmethod
    def setUpClass(cls):
        super(CreateKeypairTest, cls).setUpClass()
        cls.name = rand_name("key")
        cls.create_resp = cls.keypairs_client.create_keypair(cls.name)
        cls.keypair = cls.keypairs_client.get_keypair(cls.name).entity
        cls.resources.add(cls.name,
                          cls.keypairs_client.delete_keypair)

    @attr(type='positive', net='no')
    def test_create_keypair_response(self):
        """Verify the response code and contents are correct"""

        # Get the keypair from the original response
        keypair = self.create_resp.entity

        self.assertEqual(self.create_resp.status_code, 200)
        self.assertEqual(keypair.name, self.name)
        self.assertIsNotNone(keypair.public_key)
        self.assertIsNotNone(keypair.fingerprint)

    @attr(type='positive', net='no')
    def test_created_keypair_listed(self):
        """Verify the new key appears in list of keypairs"""

        keypairs_list = self.keypairs_client.list_keypairs().entity

        # Format of keypairs in list differs from the normal keypair model
        # Just check for a keypair by name
        self.assertTrue(any([key for key in keypairs_list
                             if key.name == self.keypair.name]))

    @attr(type='negative', net='no')
    def test_cannot_create_duplicate_keypair(self):
        """Verify a duplicate keypair cannot be created"""
        with self.assertRaises(ActionInProgress):
            self.keypairs_client.create_keypair(self.name)

    @attr(type='positive', net='yes')
    def test_created_server_has_new_keypair(self):
        """Verify the key is injected into a built server"""
        server = self.compute_provider.create_active_server(
            key_name=self.name).entity
        self.resources.add(server.id, self.servers_client.delete_server)

        # Verify the authorized_keys file was generated
        remote_client = self.compute_provider.get_remote_instance_client(
            server)
        self.assertTrue(remote_client.is_file_present(
            '~/.ssh/authorized_keys'))

        # Verify the file contains the expected key
        file_contents = remote_client.get_file_details(
            '~/.ssh/authorized_keys')
        self.assertIn(self.keypair.public_key, file_contents.content)

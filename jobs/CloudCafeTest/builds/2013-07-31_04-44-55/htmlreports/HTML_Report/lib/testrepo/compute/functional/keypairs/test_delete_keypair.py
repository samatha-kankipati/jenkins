from ccengine.common.decorators import attr
from ccengine.common.tools.datagen import rand_name
from ccengine.common.exceptions.compute import ItemNotFound

from testrepo.common.testfixtures.compute import ComputeFixture


class DeleteKeypairTest(ComputeFixture):

    @classmethod
    def setUpClass(cls):
        super(DeleteKeypairTest, cls).setUpClass()
        cls.name = rand_name("key")
        cls.keypair = cls.keypairs_client.create_keypair(cls.name).entity
        cls.delete_resp = cls.keypairs_client.delete_keypair(cls.name)

    @attr(type='positive', net='no')
    def test_delete_keypair_response(self):
        self.assertEqual(self.delete_resp.status_code, 202)

    @attr(type='positive', net='no')
    def test_deleted_keypair_not_listed(self):
        keypairs_list = self.keypairs_client.list_keypairs().entity
        self.assertNotIn(self.keypair, keypairs_list)

    @attr(type='negative', net='no')
    def test_get_deleted_keypair_fails(self):
        with self.assertRaises(ItemNotFound):
            self.keypairs_client.get_keypair(self.name)

    @attr(type='negative', net='no')
    def test_delete_deleted_keypair_fails(self):
        with self.assertRaises(ItemNotFound):
            self.keypairs_client.delete_keypair(self.name)

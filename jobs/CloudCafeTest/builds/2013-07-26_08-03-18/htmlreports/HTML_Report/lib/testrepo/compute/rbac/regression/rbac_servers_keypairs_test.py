from ccengine.common.decorators import attr
from ccengine.common.tools.datagen import rand_name
from ccengine.common.exceptions.compute import Forbidden
from testrepo.common.testfixtures.compute import RbacComputeFixture


class RbacKeypairTest(RbacComputeFixture):

    @classmethod
    def setUpClass(cls):
        super(RbacKeypairTest, cls).setUpClass()
        # Common for Gets verification
        # Insert here
    
    @attr(type='positive', net='no')
    def test_create_keypair_admin_user(self):
        """Verify the response code and contents are correct for Admin"""
        self._test_create_keypair(role_for_keypair='admin')
    
    @attr(type='positive', net='no')
    def test_create_keypair_creator_user(self):
        """Verify the response code and contents are correct for Creator"""
        self._test_create_keypair(role_for_keypair='creator')
    
    @attr(type='positive', net='no')
    def test_create_keypair_observer_user(self):
        """Verify the response code and contents are correct for Observer"""
        self._test_create_keypair(role_for_keypair='observer')
        
    def _test_create_keypair(self, role_for_keypair):
        name = rand_name("key")
        if role_for_keypair.lower() == 'admin':
            create_resp = self.keypairs_client.create_keypair(name)
            self.assertEqual(create_resp.status_code, 200)
            self.resources.add(name,
                          self.keypairs_client.delete_keypair)
        if role_for_keypair.lower() == 'creator':
            create_resp = self.creator_keypairs_client.create_keypair(name)
            self.assertEqual(create_resp.status_code, 200)
            self.resources.add(name,
                          self.keypairs_client.delete_keypair)
        elif role_for_keypair.lower() == 'observer':
            with self.assertRaises(Forbidden):
                create_resp = self.observer_keypairs_client.create_keypair(name)
        return create_resp
    
    def _test_verify_keypair(self, keypair, original_name):
        self.assertEqual(keypair.name, original_name)
        self.assertIsNotNone(keypair.public_key)
        self.assertIsNotNone(keypair.fingerprint)
    
    @attr(type='positive', net='no')
    def test_get_keypair_admin_user(self):
        """Verify the response code and contents are correct for Admin"""
        keypair = self._test_create_keypair(role_for_keypair='admin').entity
        self._test_get_keypair(role_for_keypair='admin', name=keypair.name)
    
    @attr(type='positive', net='no')
    def test_get_keypair_creator_user(self):
        """Verify the response code and contents are correct for Creator"""
        keypair = self._test_create_keypair(role_for_keypair='creator').entity
        self._test_get_keypair(role_for_keypair='creator', name=keypair.name)
    
    @attr(type='positive', net='no')
    def test_get_keypair_observer_user(self):
        """Verify the response code and contents are correct for Observer"""
        keypair = self._test_create_keypair(role_for_keypair='admin').entity
        self._test_get_keypair(role_for_keypair='observer', name=keypair.name)
    
    def _test_get_keypair(self, role_for_keypair, name):
        if role_for_keypair.lower() == 'admin':
            get_resp = self.keypairs_client.get_keypair(name)
            self.assertEqual(get_resp.status_code, 200)
        if role_for_keypair.lower() == 'creator':
            get_resp = self.creator_keypairs_client.get_keypair(name)
            self.assertEqual(get_resp.status_code, 200)
        elif role_for_keypair.lower() == 'observer':
            with self.assertRaises(Forbidden):
                get_resp = self.observer_keypairs_client.get_keypair(name)
        keypair = get_resp.entity
        return keypair
    
    @attr(type='positive', net='no')
    def test_delete_keypair_admin_user(self):
        """Verify the response code and contents are correct for Admin"""
        keypair = self._test_create_keypair(role_for_keypair='admin').entity
        self._test_delete_keypair(role_for_keypair='admin', name=keypair.name)
    
    @attr(type='positive', net='no')
    def test_delete_keypair_creator_user(self):
        """Verify the response code and contents are correct for Creator"""
        keypair = self._test_create_keypair(role_for_keypair='creator').entity
        self._test_delete_keypair(role_for_keypair='creator', name=keypair.name)
    
    @attr(type='positive', net='no')
    def test_delete_keypair_observer_user(self):
        """Verify the response code and contents are correct for Observer"""
        keypair = self._test_create_keypair(role_for_keypair='admin').entity
        self._test_delete_keypair(role_for_keypair='observer', name=keypair.name)


    def _test_delete_keypair(self, role_for_keypair, name):
        if role_for_keypair.lower() == 'admin':
            delete_resp = self.keypairs_client.delete_keypair(name)
            self.assertEqual(delete_resp.status_code, 202)
        if role_for_keypair.lower() == 'creator':
            delete_resp = self.creator_keypairs_client.delete_keypair(name)
            self.assertEqual(delete_resp.status_code, 202)
        elif role_for_keypair.lower() == 'observer':
            with self.assertRaises(Forbidden):
                delete_resp = self.observer_keypairs_client.delete_keypair(name)
        return delete_resp
import unittest
from ccengine.common.tools.datagen import rand_name
from ccengine.common.tools.datagen import random_int
from testrepo.common.testfixtures.identity.v1_1.identity \
    import IdentityFixture
from ccengine.common.decorators import attr


class AdminUsersTest(IdentityFixture):

    @classmethod
    def setUpClass(cls):
        super(AdminUsersTest, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        pass

    @attr('smoke', type='positive')
    def test_admin_create_user(self):
        normal_response_codes = [200, 203]   
        uid = rand_name("ccusername")
        key = 'asdasdasd-adsasdads-asdasdasd-adsadsasd'
        mossoId = random_int(1000000, 9000000)
        nastId = random_int(1000000, 9000000)
        enabled=True
        create_user = self.admin_client.create_user(
                id=uid,
                key=key,
                enabled=enabled,
                mossoId=mossoId,
                nastId=nastId)
        self.assertEqual(create_user.status_code, 201,
                msg="Create user expected response 201" + \
                        " received %s" %
                create_user.status_code)
        
        get_user = self.admin_client_vsec.get_user_by_name(name=uid)
        delete_user = self.admin_client.delete_user(userId=uid)
        self.assertEqual(delete_user.status_code, 204,
                msg="Create user expected response 204" + \
                        " received %s" %
                delete_user.status_code)
        self.addCleanup(self.service_client.delete_user_hard,
                        userId=get_user.entity.id)

    @attr('smoke', type='positive')
    def test_admin_list_get_user(self):
        normal_response_codes = [200, 203]   
        uid = rand_name("ccusername")
        key = 'asdasdasd-adsasdads-asdasdasd-adsadsasd'
        mossoId = random_int(1000000, 9000000)
        nastId = random_int(1000000, 9000000)
        enabled=True
        create_user = self.admin_client.create_user(
                id=uid,
                key=key,
                enabled=enabled,
                mossoId=mossoId,
                nastId=nastId)
        self.assertEqual(create_user.status_code, 201,
                msg="Create user expected response 201" + \
                        " received %s" %
                create_user.status_code)
        
        get_user_vone = self.admin_client.get_user(userId=uid)
        self.assertIn(get_user_vone.status_code, normal_response_codes,
                msg='Admin list users expected %s recieved %s' %
                (normal_response_codes, get_user_vone.status_code))

        get_user = self.admin_client_vsec.get_user_by_name(name=uid)
        delete_user = self.admin_client.delete_user(userId=uid)
        self.assertEqual(delete_user.status_code, 204,
                msg="Create user expected response 204" + \
                        " received %s" %
                delete_user.status_code)
        self.addCleanup(self.service_client.delete_user_hard,
                        userId=get_user.entity.id)
        
    @attr('smoke', type='positive')
    def test_admin_list_get_user_enabled(self):
        normal_response_codes = [200, 203]   
        uid = rand_name("ccusername")
        key = 'asdasdasd-adsasdads-asdasdasd-adsadsasd'
        mossoId = random_int(1000000, 9000000)
        nastId = random_int(1000000, 9000000)
        enabled=True
        create_user = self.admin_client.create_user(
                id=uid,
                key=key,
                enabled=enabled,
                mossoId=mossoId,
                nastId=nastId)
        self.assertEqual(create_user.status_code, 201,
                msg="Create user expected response 201" + \
                        " received %s" %
                create_user.status_code)
        
        get_user_vone = self.admin_client.get_user_enabled(userId=uid)
        self.assertIn(get_user_vone.status_code, normal_response_codes,
                msg='Admin list users expected %s recieved %s' %
                (normal_response_codes, get_user_vone.status_code))

        get_user = self.admin_client_vsec.get_user_by_name(name=uid)
        delete_user = self.admin_client.delete_user(userId=uid)
        self.assertEqual(delete_user.status_code, 204,
                msg="Create user expected response 204" + \
                        " received %s" %
                delete_user.status_code)
        self.addCleanup(self.service_client.delete_user_hard,
                        userId=get_user.entity.id)
        
    @attr('smoke', type='positive')
    def test_admin_list_get_user_groups(self):
        normal_response_codes = [200, 203]   
        uid = rand_name("ccusername")
        key = 'asdasdasd-adsasdads-asdasdasd-adsadsasd'
        mossoId = random_int(1000000, 9000000)
        nastId = random_int(1000000, 9000000)
        enabled=True
        create_user = self.admin_client.create_user(
                id=uid,
                key=key,
                enabled=enabled,
                mossoId=mossoId,
                nastId=nastId)
        self.assertEqual(create_user.status_code, 201,
                msg="Create user expected response 201" + \
                        " received %s" %
                create_user.status_code)
        
        get_user_vone = self.admin_client.get_user_groups(userId=uid)
        self.assertIn(get_user_vone.status_code, normal_response_codes,
                msg='Admin list users expected %s recieved %s' %
                (normal_response_codes, get_user_vone.status_code))

        get_user = self.admin_client_vsec.get_user_by_name(name=uid)
        delete_user = self.admin_client.delete_user(userId=uid)
        self.assertEqual(delete_user.status_code, 204,
                msg="Create user expected response 204" + \
                        " received %s" %
                delete_user.status_code)
        self.addCleanup(self.service_client.delete_user_hard,
                        userId=get_user.entity.id)
        
    @attr('smoke', type='positive')
    def test_admin_list_get_user_catalog(self):
        normal_response_codes = [200, 203]   
        uid = rand_name("ccusername")
        key = 'asdasdasd-adsasdads-asdasdasd-adsadsasd'
        mossoId = random_int(1000000, 9000000)
        nastId = random_int(1000000, 9000000)
        enabled=True
        create_user = self.admin_client.create_user(
                id=uid,
                key=key,
                enabled=enabled,
                mossoId=mossoId,
                nastId=nastId)
        self.assertEqual(create_user.status_code, 201,
                msg="Create user expected response 201" + \
                        " received %s" %
                create_user.status_code)
        
        get_user_vone = self.admin_client.get_user_service_catalog(userId=uid)
        self.assertIn(get_user_vone.status_code, normal_response_codes,
                msg='Admin list users expected %s recieved %s' %
                (normal_response_codes, get_user_vone.status_code))

        get_user = self.admin_client_vsec.get_user_by_name(name=uid)
        delete_user = self.admin_client.delete_user(userId=uid)
        self.assertEqual(delete_user.status_code, 204,
                msg="Create user expected response 204" + \
                        " received %s" %
                delete_user.status_code)
        self.addCleanup(self.service_client.delete_user_hard,
                        userId=get_user.entity.id)
    
    @attr('smoke', type='positive')
    def test_admin_update_user(self):
        normal_response_codes = [200, 203]   
        uid = rand_name("ccusername")
        key = 'asdasdasd-adsasdads-asdasdasd-adsadsasd'
        upd_key = 'asda3dfsd-ad5asdads-as7ajhgsd-adsadseee'
        mossoId = random_int(1000000, 9000000)
        nastId = random_int(1000000, 9000000)
        enabled=True
        create_user = self.admin_client.create_user(
                id=uid,
                key=key,
                enabled=enabled,
                mossoId=mossoId,
                nastId=nastId)
        self.assertEqual(create_user.status_code, 201,
                msg="Create user expected response 201" + \
                        " received %s" %
                create_user.status_code)
        
        update_user = self.admin_client.update_user(userId=uid, id=uid,
                                                    key=upd_key,
                                                    enabled=enabled,
                                                    mossoId=mossoId,
                                                    nastId=nastId)
        self.assertIn(update_user.status_code, normal_response_codes,
                msg='Admin list users expected %s recieved %s' %
                (normal_response_codes, update_user.status_code))

        get_user = self.admin_client_vsec.get_user_by_name(name=uid)
        delete_user = self.admin_client.delete_user(userId=uid)
        self.assertEqual(delete_user.status_code, 204,
                msg="Create user expected response 204" + \
                        " received %s" %
                delete_user.status_code)
        self.addCleanup(self.service_client.delete_user_hard,
                        userId=get_user.entity.id)
        
    @attr('smoke', type='positive')
    def test_admin_update_user_enabled(self):
        normal_response_codes = [200, 203]   
        uid = rand_name("ccusername")
        key = 'asdasdasd-adsasdads-asdasdasd-adsadsasd'
        mossoId = random_int(1000000, 9000000)
        nastId = random_int(1000000, 9000000)
        enabled=False
        upd_enabled=True
        create_user = self.admin_client.create_user(
                id=uid,
                key=key,
                enabled=enabled,
                mossoId=mossoId,
                nastId=nastId)
        self.assertEqual(create_user.status_code, 201,
                msg="Create user expected response 201" + \
                        " received %s" %
                create_user.status_code)
        
        update_user = self.admin_client.update_user_enabled(
                                                    userId=uid,
                                                    enabled=upd_enabled)
        self.assertIn(update_user.status_code, normal_response_codes,
                msg='Admin list users expected %s recieved %s' %
                (normal_response_codes, update_user.status_code))

        get_user = self.admin_client_vsec.get_user_by_name(name=uid)
        delete_user = self.admin_client.delete_user(userId=uid)
        self.assertEqual(delete_user.status_code, 204,
                msg="Create user expected response 204" + \
                        " received %s" %
                delete_user.status_code)
        self.addCleanup(self.service_client.delete_user_hard,
                        userId=get_user.entity.id)
        
    @attr('smoke', type='positive')
    def test_admin_list_get_user_key(self):
        normal_response_codes = [200, 203]   
        uid = rand_name("ccusername")
        key = 'asdasdasd-adsasdads-asdasdasd-adsadsasd'
        mossoId = random_int(1000000, 9000000)
        nastId = random_int(1000000, 9000000)
        enabled=True
        create_user = self.admin_client.create_user(
                id=uid,
                key=key,
                enabled=enabled,
                mossoId=mossoId,
                nastId=nastId)
        self.assertEqual(create_user.status_code, 201,
                msg="Create user expected response 201" + \
                        " received %s" %
                create_user.status_code)
        
        get_user_vone = self.admin_client.get_user_key(userId=uid)
        self.assertIn(get_user_vone.status_code, normal_response_codes,
                msg='Admin list users expected %s recieved %s' %
                (normal_response_codes, get_user_vone.status_code))

        get_user = self.admin_client_vsec.get_user_by_name(name=uid)
        delete_user = self.admin_client.delete_user(userId=uid)
        self.assertEqual(delete_user.status_code, 204,
                msg="Create user expected response 204" + \
                        " received %s" %
                delete_user.status_code)
        self.addCleanup(self.service_client.delete_user_hard,
                        userId=get_user.entity.id)
        
    @attr('smoke', type='positive')
    def test_admin_list_set_user_key(self):
        normal_response_codes = [200, 203]   
        uid = rand_name("ccusername")
        key = 'asdasdasd-adsasdads-asdasdasd-adsadsasd'
        upd_key = '12da5dasd-adsas6ad9-asda7dasd-a456ds8sd'
        mossoId = random_int(1000000, 9000000)
        nastId = random_int(1000000, 9000000)
        enabled=True
        create_user = self.admin_client.create_user(
                id=uid,
                key=key,
                enabled=enabled,
                mossoId=mossoId,
                nastId=nastId)
        self.assertEqual(create_user.status_code, 201,
                msg="Create user expected response 201" + \
                        " received %s" %
                create_user.status_code)
        
        get_user_vone = self.admin_client.set_user_key(userId=uid,
                                                       key=upd_key)
        self.assertIn(get_user_vone.status_code, normal_response_codes,
                msg='Admin list users expected %s recieved %s' %
                (normal_response_codes, get_user_vone.status_code))

        get_user = self.admin_client_vsec.get_user_by_name(name=uid)
        delete_user = self.admin_client.delete_user(userId=uid)
        self.assertEqual(delete_user.status_code, 204,
                msg="Create user expected response 204" + \
                        " received %s" %
                delete_user.status_code)
        self.addCleanup(self.service_client.delete_user_hard,
                        userId=get_user.entity.id)
        
    @attr('smoke', type='positive')
    def test_admin_list_get_alternate_nast(self):
        normal_response_codes = [200, 203]   
        uid = rand_name("ccusername")
        key = 'asdasdasd-adsasdads-asdasdasd-adsadsasd'
        mossoId = random_int(1000000, 9000000)
        nastId = random_int(1000000, 9000000)
        enabled=True
        create_user = self.admin_client.create_user(
                id=uid,
                key=key,
                enabled=enabled,
                mossoId=mossoId,
                nastId=nastId)
        self.assertEqual(create_user.status_code, 201,
                msg="Create user expected response 201" + \
                        " received %s" %
                create_user.status_code)
        
        get_user_vone = self.admin_client.get_user_by_nast_id(
                nastId=create_user.entity.nastId,
                requestslib_kwargs={'allow_redirects': False})
        self.assertEquals(
                get_user_vone.status_code, 301, "Expected 301, "
                "recieved {0}".format(get_user_vone.status_code))

        self.assertEquals(get_user_vone.headers.get('location'),
                "/v1.1/users/{0}".format(uid),
                "Expected valid location header")

        get_user = self.admin_client_vsec.get_user_by_name(name=uid)
        delete_user = self.admin_client.delete_user(userId=uid)
        self.assertEqual(delete_user.status_code, 204,
                msg="Create user expected response 204" + \
                        " received %s" %
                delete_user.status_code)
        self.addCleanup(self.service_client.delete_user_hard,
                        userId=get_user.entity.id)
        
    @attr('smoke', type='positive')
    def test_admin_list_get_alternate_mosso(self):
        normal_response_codes = [200, 203]   
        uid = rand_name("ccusername")
        key = 'asdasdasd-adsasdads-asdasdasd-adsadsasd'
        mossoId = random_int(1000000, 9000000)
        nastId = random_int(1000000, 9000000)
        enabled=True
        create_user = self.admin_client.create_user(
                id=uid,
                key=key,
                enabled=enabled,
                mossoId=mossoId,
                nastId=nastId)
        self.assertEqual(create_user.status_code, 201,
                msg="Create user expected response 201" + \
                        " received %s" %
                create_user.status_code)

        get_user_vone = self.admin_client.get_user_by_mosso_id(mossoId=mossoId,
                requestslib_kwargs={'allow_redirects': False})
        self.assertEquals(
                get_user_vone.status_code, 301, "Expected 301, "
                "recieved {0}".format(get_user_vone.status_code))

        self.assertEquals(get_user_vone.headers.get('location'),
                "/v1.1/users/{0}".format(uid),
                "Expected valid location header")

        get_user = self.admin_client_vsec.get_user_by_name(name=uid)
        delete_user = self.admin_client.delete_user(userId=uid)
        self.assertEqual(delete_user.status_code, 204,
                msg="Create user expected response 204" + \
                        " received %s" %
                delete_user.status_code)
        self.addCleanup(self.service_client.delete_user_hard,
                        userId=get_user.entity.id)


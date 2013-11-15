import unittest
from ccengine.common.tools.datagen import rand_name
from ccengine.common.tools.datagen import random_int
from testrepo.common.testfixtures.identity.v1_1.identity \
    import IdentityFixture
from ccengine.common.decorators import attr
import types


class AdminBaseurlTest(IdentityFixture):

    @classmethod
    def setUpClass(cls):
        super(AdminBaseurlTest, cls).setUpClass()
        cls.service_name = 'cloudFiles'

    @classmethod
    def tearDownClass(cls):
        pass

    @attr('regression', type='positive')
    def test_admin_get_base_urls_enabled(self):
        normal_response_codes = [200, 203]   
        get_base_urls_enbled = self.admin_client.list_base_urls_enabled()
        self.assertIn(get_base_urls_enbled.status_code, normal_response_codes,
                msg= 'Get base URLs expected {0} received {1}'.format(
                    normal_response_codes, 
                    get_base_urls_enbled.status_code))
        
        self.assertIsInstance(get_base_urls_enbled.entity, types.ListType,
            msg="Expecting get url format is correct")
        self.assertTrue(get_base_urls_enbled.entity[0].id is not None,
            msg="Expecting id is not None")
        self.assertTrue(get_base_urls_enbled.entity[0].userType is not None,
            msg="Expecting userType is not None")
        self.assertTrue(get_base_urls_enbled.entity[0].region is not None,
            msg="Expecting region is not None")
        self.assertTrue(get_base_urls_enbled.entity[0].default is not None,
            msg="Expecting default state is not None")
        self.assertTrue(get_base_urls_enbled.entity[0].serviceName is not None,
            msg="Expecting serviceName is not None")
        self.assertTrue(get_base_urls_enbled.entity[0].publicURL is not None,
            msg="Expecting publicURL is not None")
        self.assertTrue(get_base_urls_enbled.entity[0].internalURL is not None,
            msg="Expecting internal URL is not None")
        self.assertTrue(get_base_urls_enbled.entity[0].enabled is not None,
            msg="Expecting default enabled is not None")
        
        
    @attr('regression', type='positive')
    def test_admin_get_base_urls(self):
        normal_response_codes = [200, 203]   
        get_base_url = self.admin_client.list_base_urls()
        self.assertIn(get_base_url.status_code, normal_response_codes,
                msg= 'Get base URL expected {0} received {1}'.format(
                    normal_response_codes, 
                    get_base_url.status_code))
        
        self.assertIsInstance(get_base_url.entity, types.ListType,
            msg="Expecting get url format is correct")
        self.assertTrue(get_base_url.entity[0].id is not None,
            msg="Expecting id is not None")
        self.assertTrue(get_base_url.entity[0].userType is not None,
            msg="Expecting userType is not None")
        self.assertTrue(get_base_url.entity[0].region is not None,
            msg="Expecting region is not None")
        self.assertTrue(get_base_url.entity[0].default is not None,
            msg="Expecting default state is not None")
        self.assertTrue(get_base_url.entity[0].serviceName is not None,
            msg="Expecting serviceName is not None")
        self.assertTrue(get_base_url.entity[0].publicURL is not None,
            msg="Expecting publicURL is not None")
        self.assertTrue(get_base_url.entity[0].internalURL is not None,
            msg="Expecting internal URL is not None")
        self.assertTrue(get_base_url.entity[0].enabled is not None,
            msg="Expecting default enabled is not None")
        
    @attr('regression', type='positive')
    def test_admin_get_base_urls_service_name(self):
        normal_response_codes = [200, 203]   
        get_base_url = self.admin_client.list_base_urls(
                serviceName=self.service_name)
        self.assertIn(get_base_url.status_code, normal_response_codes,
                msg= 'Get base URL by service expected {0} received {1}'.format(
                    normal_response_codes, 
                    get_base_url.status_code))
        self.assertTrue(get_base_url.entity[0].id is not None,
            msg="Expecting id is not None")
        self.assertTrue(get_base_url.entity[0].userType is not None,
            msg="Expecting userType is not None")
        self.assertTrue(get_base_url.entity[0].region is not None,
            msg="Expecting region is not None")
        self.assertTrue(get_base_url.entity[0].default is not None,
            msg="Expecting default state is not None")
        self.assertTrue(get_base_url.entity[0].serviceName is not None,
            msg="Expecting serviceName is not None")
        self.assertTrue(get_base_url.entity[0].publicURL is not None,
            msg="Expecting publicURL is not None")
        self.assertTrue(get_base_url.entity[0].internalURL is not None,
            msg="Expecting internal URL is not None")
        self.assertTrue(get_base_url.entity[0].enabled is not None,
            msg="Expecting default enabled is not None")
        
    @attr('regression', type='positive')
    def test_admin_get_base_urls_enabled_service_name(self):
        normal_response_codes = [200, 203]   
        get_base_urls_enabled = self.admin_client.list_base_urls_enabled(
                serviceName=self.service_name)
        self.assertIn(get_base_urls_enabled.status_code, normal_response_codes,
                msg= 'Get enabled URL by serv expected {0} received {1}'.format(
                    normal_response_codes, 
                    get_base_urls_enabled.status_code))
        self.assertTrue(get_base_urls_enabled.entity[0].id is not None,
            msg="Expecting id is not None")
        self.assertTrue(get_base_urls_enabled.entity[0].userType is not None,
            msg="Expecting userType is not None")
        self.assertTrue(get_base_urls_enabled.entity[0].region is not None,
            msg="Expecting region is not None")
        self.assertTrue(get_base_urls_enabled.entity[0].default is not None,
            msg="Expecting default state is not None")
        self.assertTrue(get_base_urls_enabled.entity[0].serviceName is not None,
            msg="Expecting serviceName is not None")
        self.assertTrue(get_base_urls_enabled.entity[0].publicURL is not None,
            msg="Expecting publicURL is not None")
        self.assertTrue(get_base_urls_enabled.entity[0].internalURL is not None,
            msg="Expecting internal URL is not None")
        self.assertTrue(get_base_urls_enabled.entity[0].enabled is not None,
            msg="Expecting default enabled is not None")
        
    @attr('regression', type='positive')
    def test_admin_get_base_url(self):
        normal_response_codes = [200, 203]
        get_url_id = self.admin_client.list_base_urls_enabled(
                serviceName=self.service_name)   
        get_base_url = self.admin_client.get_base_url(
                baseURLId=get_url_id.entity[0].id)
        self.assertIn(get_base_url.status_code, normal_response_codes,
                msg= 'Get base URL expected {0} received {1}'.format(
                    normal_response_codes, 
                    get_base_url.status_code))
        
    @attr('regression', type='positive')
    def test_admin_get_base_url_user(self):
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
                msg= 'Create user exp. response 201 received {0}'.format(
                    create_user.status_code))
        
        get_base_url = self.admin_client.get_user_base_urls(
                userId=uid)
        self.assertIn(get_base_url.status_code, normal_response_codes,
                msg= 'Get base URLs expected {0} received {1}'.format(
                    normal_response_codes, 
                    get_base_url.status_code))
        
        
        get_user = self.admin_client_vsec.get_user_by_name(name=uid)
        delete_user = self.admin_client.delete_user(userId=uid)
        self.assertEqual(delete_user.status_code, 204,
                msg= 'Delete user exp. response 201 received {0}'.format(
                    delete_user.status_code))
        self.addCleanup(self.service_client.delete_user_hard,
                        userId=get_user.entity.id)
    
    @attr('regression', type='positive')
    def test_admin_remove_base_url_user(self):
        normal_response_codes = [204]   
        uid = rand_name("ccusername")
        key = 'asdasdasd-adsasdads-asdasdasd-adsadsasd'
        mossoId = random_int(1000000, 9000000)
        nastId = random_int(1000000, 9000000)
        enabled=True
        v1Default=True
        create_user = self.admin_client.create_user(
                id=uid,
                key=key,
                enabled=enabled,
                mossoId=mossoId,
                nastId=nastId)
        self.assertEqual(create_user.status_code, 201,
                msg= 'Create user exp. response 201 received {0}'.format(
                    create_user.status_code))
        get_url_id = self.admin_client.list_base_urls_enabled(
                serviceName=self.service_name)        
        add_base_url = self.admin_client.add_user_base_url(
                id='133',
                v1Default=v1Default,
                userId=uid)
        self.assertEqual(add_base_url.status_code, 201,
                msg= '{0}{1}'.format('Add base URL response 201 received ',
                    add_base_url.status_code))
        
        remove_base_url = self.admin_client.delete_user_base_url(
                baseURLId='133',
                userId=uid)
        self.assertIn(remove_base_url.status_code, normal_response_codes,
                msg= 'Remove base URLs expected {0} received {1}'.format(
                    normal_response_codes, 
                    remove_base_url.status_code))
        
        add_base_url_sec = self.admin_client.add_user_base_url(
                id='133',
                v1Default=v1Default,
                userId=uid)
        self.assertEqual(add_base_url_sec.status_code, 201,
                msg= '{0}{1}'.format('Add base URL response 201 received ',
                    add_base_url_sec.status_code))
        get_user = self.admin_client_vsec.get_user_by_name(name=uid)
        delete_user = self.admin_client.delete_user(userId=uid)
        self.assertEqual(delete_user.status_code, 204,
                msg= 'Delete user exp. response 201 received {0}'.format(
                    delete_user.status_code))
        self.addCleanup(self.service_client.delete_user_hard,
                        userId=get_user.entity.id)
    
    @attr('regression', type='positive')
    def test_admin_add_base_url_user(self):
        normal_response_codes = [201]   
        uid = rand_name("ccusername")
        key = 'asdasdasd-adsasdads-asdasdasd-adsadsasd'
        mossoId = random_int(1000000, 9000000)
        nastId = random_int(1000000, 9000000)
        enabled=True
        v1Default=True
        create_user = self.admin_client.create_user(
                id=uid,
                key=key,
                enabled=enabled,
                mossoId=mossoId,
                nastId=nastId)
        self.assertEqual(create_user.status_code, 201,
                msg= 'Create user exp. response 201 received {0}'.format(
                    create_user.status_code))
        get_url_id = self.admin_client.list_base_urls_enabled(
                serviceName=self.service_name)        
        add_base_url = self.admin_client.add_user_base_url(
                id='133',
                v1Default=v1Default,
                userId=uid)
        self.assertIn(add_base_url.status_code, normal_response_codes,
                msg= 'Add base URLs expected {0} received {1}'.format(
                    normal_response_codes, 
                    add_base_url.status_code))
        
        remove_base_url = self.admin_client.delete_user_base_url(
                baseURLId='133',
                userId=uid)
        self.assertEqual(remove_base_url.status_code, 204,
                msg= '{0}{1}'.format('Remove user exp. response 201 received ',
                    remove_base_url.status_code))
        
        get_user = self.admin_client_vsec.get_user_by_name(name=uid)
        delete_user = self.admin_client.delete_user(userId=uid)
        self.assertEqual(delete_user.status_code, 204,
                msg= 'Delete user exp. response 201 received {0}'.format(
                    delete_user.status_code))
        self.addCleanup(self.service_client.delete_user_hard,
                        userId=get_user.entity.id)
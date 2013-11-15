import unittest
from ccengine.common.tools.datagen import rand_name
from ccengine.common.tools.datagen import random_int
from testrepo.common.testfixtures.identity.v1_1.identity \
    import IdentityFixture
from ccengine.common.decorators import attr
import types
from time import strptime, struct_time, mktime
from datetime import datetime, timedelta
from dateutil.parser import parse


class AdminUsersTest(IdentityFixture):

    @classmethod
    def setUpClass(cls):
        super(AdminUsersTest, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        pass

    @attr('regression', type='positive')
    def test_admin_create_user(self):
        '''Docs: nastId should be provided and processed by identity,
        but identity doesn't process it in present behaviour'''
        normal_response_codes = [201, 203]   
        uid = rand_name("ccusername")
        key = 'asdasdasd-adsasdads-asdasdasd-adsadsasd'
        mossoId = random_int(1000000, 9000000)
        #nastId = random_int(1000000, 9000000) - present in the api doc
        enabled=True
        create_user = self.admin_client.create_user(
            id=uid,
            key=key,
            enabled=enabled,
            mossoId=mossoId,
            #nastId=nastId - present in the api doc
            )
        self.assertIn(create_user.status_code, normal_response_codes,
            msg= 'Get base URLs expected {0} received {1}'.format(
                normal_response_codes, 
                create_user.status_code))
        
        self.assertEquals(create_user.entity.id, uid,
            msg='User Uid expected {0} but received {1}'.format(
            uid, create_user.entity.id))
        self.assertEquals(create_user.entity.key, key,
            msg='User key expected {0} but received {1}'.format(
            key, create_user.entity.key))
        self.assertEquals(create_user.entity.mossoId, mossoId,
            msg='User mossoId expected {0} but received {1}'.format(
            mossoId, create_user.entity.mossoId))
        self.assertEquals(create_user.entity.enabled, enabled,
            msg='User mossoId expected {0} but received {1}'.format(
            enabled, create_user.entity.enabled))
        self.assertTrue(create_user.entity.nastId is not None,
            msg="Expecting nastId is not None")
        self.assertIsInstance(create_user.entity.baseURLRefs, types.ListType,
            msg="Expecting username in the userURL is correct")
        self.assertTrue(create_user.entity.baseURLRefs[0].id is not None,
            msg="Expecting username in the userURL is correct")
        self.assertTrue(create_user.entity.baseURLRefs[0].href is not None,
            msg="Expecting username in the userURL is correct")
        self.assertTrue(create_user.entity.baseURLRefs[0].v1Default is not None,
            msg="Expecting username in the userURL is correct")
        
        get_user = self.admin_client_vsec.get_user_by_name(name=uid)
        delete_user = self.admin_client.delete_user(userId=uid)
        self.assertEqual(delete_user.status_code, 204,
                msg='Create user expected response 204, received {0}'.format(
                delete_user.status_code))
        self.addCleanup(self.service_client.delete_user_hard,
                        userId=get_user.entity.id)

    @attr('regression', type='positive')
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
                msg='Create user expected response 201, received {0}'.format(
                create_user.status_code))
        
        get_user_vone = self.admin_client.get_user(userId=uid)
        self.assertIn(get_user_vone.status_code, normal_response_codes,
            msg= 'Get base URLs expected {0} received {1}'.format(
                normal_response_codes, 
                get_user_vone.status_code))
        
        self.assertEquals(get_user_vone.entity.id, uid,
            msg='User Uid expected {0} but received {1}'.format(
            uid, get_user_vone.entity.id))
        self.assertEquals(get_user_vone.entity.key, key,
            msg='User key expected {0} but received {1}'.format(
            key, get_user_vone.entity.key))
        self.assertEquals(get_user_vone.entity.mossoId, mossoId,
            msg='User mossoId expected {0} but received {1}'.format(
            mossoId, get_user_vone.entity.mossoId))
        self.assertEquals(get_user_vone.entity.enabled, enabled,
            msg='User mossoId expected {0} but received {1}'.format(
            enabled, get_user_vone.entity.enabled))
        self.assertTrue(get_user_vone.entity.nastId is not None,
            msg="Expecting nastId is not None")
        self.assertIsInstance(get_user_vone.entity.baseURLRefs, types.ListType,
            msg="Expecting username in the userURL is correct")
        self.assertTrue(get_user_vone.entity.baseURLRefs[0].id is not None,
            msg="Expecting username in the userURL is correct")
        self.assertTrue(get_user_vone.entity.baseURLRefs[0].href is not None,
            msg="Expecting username in the userURL is correct")
        self.assertTrue(get_user_vone.entity.baseURLRefs[0].v1Default is not None,
            msg="Expecting username in the userURL is correct")
        
        parsed_time_cr = None
        parsed_time_up = None
        try:
            parsed_time_cr = parse(get_user_vone.entity.created)
            ptime_cr = parsed_time_cr.timetuple()
            parsed_time_up = parse(get_user_vone.entity.updated)
            ptime_up = parsed_time_up.timetuple()
        except ValueError:
            pass

        self.assertIsInstance(ptime_cr, struct_time,
                msg='Date format is correct')
        self.assertIsInstance(ptime_up, struct_time,
                msg='Date format is correct')
        cr_time = datetime.fromtimestamp(mktime(ptime_cr))
        up_time = datetime.fromtimestamp(mktime(ptime_up))
        delta = (cr_time - up_time)
        self.assertLessEqual(delta, timedelta(days=0, hours=0, minutes=0),
                msg='User hasnt been updated')
        
        get_user = self.admin_client_vsec.get_user_by_name(name=uid)
        delete_user = self.admin_client.delete_user(userId=uid)
        self.assertEqual(delete_user.status_code, 204,
                msg='Create user expected response 204, received {0}'.format(
                delete_user.status_code))
        self.addCleanup(self.service_client.delete_user_hard,
                        userId=get_user.entity.id)
        
    @attr('regression', type='positive')
    def test_admin_list_get_user_enabled(self):
        '''Docs: Only enabled should be in response'''
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
                msg='Create user expected response 201, received {0}'.format(
                create_user.status_code))
        
        get_user_vone = self.admin_client.get_user_enabled(userId=uid)
        self.assertIn(get_user_vone.status_code, normal_response_codes,
                msg= 'Get base URLs expected {0} received {1}'.format(
                normal_response_codes, 
                get_user_vone.status_code))
        
        self.assertEquals(get_user_vone.entity.enabled, enabled,
            msg='User enabled state expected {0} but received {1}'.format(
            enabled, create_user.entity.enabled))

        get_user = self.admin_client_vsec.get_user_by_name(name=uid)
        delete_user = self.admin_client.delete_user(userId=uid)
        self.assertEqual(delete_user.status_code, 204,
                msg='Create user expected response 204, received {0}'.format(
                delete_user.status_code))
        self.addCleanup(self.service_client.delete_user_hard,
                userId=get_user.entity.id)
        
    @attr('regression', type='positive')
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
                msg='Create user expected response 201, received {0}'.format(
                create_user.status_code))
        
        get_user_vone = self.admin_client.get_user_groups(userId=uid)
        self.assertIn(get_user_vone.status_code, normal_response_codes,
                msg= 'Get base URLs expected {0} received {1}'.format(
                normal_response_codes, 
                get_user_vone.status_code))
        
        self.assertTrue(get_user_vone.entity[0].id is not None,
            msg="Expecting nastId is not None")
        self.assertTrue(get_user_vone.entity[0].description is not None,
            msg="Expecting nastId is not None")

        get_user = self.admin_client_vsec.get_user_by_name(name=uid)
        delete_user = self.admin_client.delete_user(userId=uid)
        self.assertEqual(delete_user.status_code, 204,
                msg='Create user expected response 204, received {0}'.format(
                delete_user.status_code))
        self.addCleanup(self.service_client.delete_user_hard,
                userId=get_user.entity.id)
        
    @attr('regression', type='positive')
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
                msg='Create user expected response 201, received {0}'.format(
                create_user.status_code))
        
        get_user_vone = self.admin_client.get_user_service_catalog(userId=uid)
        self.assertIn(get_user_vone.status_code, normal_response_codes,
                msg= 'Get base URLs expected {0} received {1}'.format(
                normal_response_codes, 
                get_user_vone.status_code))
        
        self.assertTrue(get_user_vone.entity[0].endpoints[0].region is not None,
                msg="Expecting region is not None")
        self.assertTrue(get_user_vone.entity[2].endpoints[0].publicURL is not None,
                msg="Expecting publicURL is not None")
        self.assertTrue(get_user_vone.entity[3].endpoints[0].internalURL is not None,
                msg="Expecting internalURL is not None")
        self.assertTrue(get_user_vone.entity[8].endpoints[0].v1Default is not None,
                msg="Expecting v1Default is not None")

        get_user = self.admin_client_vsec.get_user_by_name(name=uid)
        delete_user = self.admin_client.delete_user(userId=uid)
        self.assertEqual(delete_user.status_code, 204,
                msg='Create user expected response 204, received {0}'.format(
                delete_user.status_code))
        self.addCleanup(self.service_client.delete_user_hard,
                        userId=get_user.entity.id)
    
    @attr('regression', type='positive')
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
                msg='Create user expected response 201, received {0}'.format(
                create_user.status_code))
        
        update_user = self.admin_client.update_user(userId=uid, id=uid,
                                                    key=upd_key,
                                                    enabled=enabled,
                                                    mossoId=mossoId,
                                                    nastId=nastId)
        self.assertIn(update_user.status_code, normal_response_codes,
                msg= 'Get base URLs expected {0} received {1}'.format(
                normal_response_codes, 
                update_user.status_code))
        
        self.assertEquals(update_user.entity.id, uid,
            msg='User Uid expected {0} but received {1}'.format(
            uid, update_user.entity.id))
        self.assertEquals(update_user.entity.key, key,
            msg='User key expected {0} but received {1}'.format(
            key, update_user.entity.key))
        self.assertEquals(update_user.entity.mossoId, mossoId,
            msg='User mossoId expected {0} but received {1}'.format(
            mossoId, update_user.entity.mossoId))
        self.assertEquals(update_user.entity.enabled, enabled,
            msg='User mossoId expected {0} but received {1}'.format(
            enabled, update_user.entity.enabled))
        self.assertTrue(update_user.entity.nastId is not None,
            msg="Expecting nastId is not None")
        self.assertIsInstance(update_user.entity.baseURLRefs, types.ListType,
            msg="Expecting username in the userURL is correct")
        self.assertTrue(update_user.entity.baseURLRefs[0].id is not None,
            msg="Expecting username in the userURL is correct")
        self.assertTrue(update_user.entity.baseURLRefs[0].href is not None,
            msg="Expecting username in the userURL is correct")
        self.assertTrue(update_user.entity.baseURLRefs[0].v1Default is not None,
            msg="Expecting username in the userURL is correct")
        
        parsed_time_cr = None
        parsed_time_up = None
        try:
            parsed_time_cr = parse(update_user.entity.created)
            ptime_cr = parsed_time_cr.timetuple()
            parsed_time_up = parse(update_user.entity.updated)
            ptime_up = parsed_time_up.timetuple()
        except ValueError:
            pass

        self.assertIsInstance(ptime_cr, struct_time,
                msg='Date format is correct')
        self.assertIsInstance(ptime_up, struct_time,
                msg='Date format is correct')
        cr_time = datetime.fromtimestamp(mktime(ptime_cr))
        up_time = datetime.fromtimestamp(mktime(ptime_up))
        delta = (cr_time - up_time)
        self.assertLessEqual(delta, timedelta(days=0, hours=0, minutes=0),
                msg='Expected delta {0} but received {1}'.format(
                timedelta(days=0, hours=0, minutes=0), delta))

        get_user = self.admin_client_vsec.get_user_by_name(name=uid)
        delete_user = self.admin_client.delete_user(userId=uid)
        self.assertEqual(delete_user.status_code, 204,
                msg='Create user expected response 204, received {0}'.format(
                delete_user.status_code))
        self.addCleanup(self.service_client.delete_user_hard,
                        userId=get_user.entity.id)
        
    @attr('regression', type='positive')
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
                msg='Create user expected response 201, received {0}'.format(
                create_user.status_code))
        
        update_user = self.admin_client.update_user_enabled(
                userId=uid,
                enabled=upd_enabled)
        self.assertIn(update_user.status_code, normal_response_codes,
                msg= 'Get base URLs expected {0} received {1}'.format(
                normal_response_codes, 
                update_user.status_code))
        
        self.assertEquals(update_user.entity.enabled, upd_enabled,
                msg='Enabled state expected {0} but received {1}'.format(
                upd_enabled, update_user.entity.enabled))

        get_user = self.admin_client_vsec.get_user_by_name(name=uid)
        delete_user = self.admin_client.delete_user(userId=uid)
        self.assertEqual(delete_user.status_code, 204,
                msg='Create user expected response 204, received {0}'.format(
                delete_user.status_code))
        self.addCleanup(self.service_client.delete_user_hard,
                userId=get_user.entity.id)
        
    @attr('regression', type='positive')
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
                msg='Create user expected response 201, received {0}'.format(
                create_user.status_code))
        
        get_user_vone = self.admin_client.get_user_key(userId=uid)
        self.assertIn(get_user_vone.status_code, normal_response_codes,
                msg= 'Get base URLs expected {0} received {1}'.format(
                normal_response_codes, 
                get_user_vone.status_code))
        
        self.assertEquals(get_user_vone.entity.key, key,
            msg='User key expected {0} but received {1}'.format(
            key, get_user_vone.entity.key))

        get_user = self.admin_client_vsec.get_user_by_name(name=uid)
        delete_user = self.admin_client.delete_user(userId=uid)
        self.assertEqual(delete_user.status_code, 204,
                msg='Create user expected response 204, received {0}'.format(
                delete_user.status_code))
        self.addCleanup(self.service_client.delete_user_hard,
                        userId=get_user.entity.id)
        
    @attr('regression', type='positive')
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
                msg='Create user expected response 201, received {0}'.format(
                create_user.status_code))
        
        get_user_vone = self.admin_client.set_user_key(userId=uid,
                                                       key=upd_key)
        self.assertIn(get_user_vone.status_code, normal_response_codes,
                msg= 'Get base URLs expected {0} received {1}'.format(
                normal_response_codes, 
                get_user_vone.status_code))
        
        self.assertEquals(get_user_vone.entity.key, upd_key,
            msg='User key expected {0} but received {1}'.format(
            upd_key, get_user_vone.entity.key))

        get_user = self.admin_client_vsec.get_user_by_name(name=uid)
        delete_user = self.admin_client.delete_user(userId=uid)
        self.assertEqual(delete_user.status_code, 204,
                msg='Create user expected response 204, received {0}'.format(
                delete_user.status_code))
        self.addCleanup(self.service_client.delete_user_hard,
                        userId=get_user.entity.id)
        
    @attr('regression', type='positive')
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
                msg='Create user expected response 201, received {0}'.format(
                create_user.status_code))
        
        get_user_vone = self.admin_client.get_user_by_nast_id(
                nastId=create_user.entity.nastId,
                requestslib_kwargs={'allow_redirects': False})

        self.assertEquals(
                get_user_vone.status_code, 301, "Expected 301, "
                "recieved {0}".format(get_user_vone.status_code))

        self.assertEquals(get_user_vone.headers.get('location'),
                "/v1.1/users/{0}".format(uid),
                "Expected valid location header")

        get_user = self.admin_client.get_user(userId=uid)

        self.assertEquals(get_user.entity.id, uid,
            msg='User Uid expected {0} but received {1}'.format(
            uid, get_user.entity.id))
        self.assertEquals(get_user.entity.key, key,
            msg='User key expected {0} but received {1}'.format(
            key, get_user.entity.key))
        self.assertEquals(get_user.entity.mossoId, mossoId,
            msg='User mossoId expected {0} but received {1}'.format(
            mossoId, get_user.entity.mossoId))
        self.assertEquals(get_user.entity.enabled, enabled,
            msg='User mossoId expected {0} but received {1}'.format(
            enabled, get_user.entity.enabled))
        self.assertTrue(get_user.entity.nastId is not None,
            msg="Expecting nastId is not None")
        self.assertIsInstance(get_user.entity.baseURLRefs, types.ListType,
            msg="Expecting username in the userURL is correct")
        self.assertTrue(get_user.entity.baseURLRefs[0].id is not None,
            msg="Expecting username in the userURL is correct")
        self.assertTrue(get_user.entity.baseURLRefs[0].href is not None,
            msg="Expecting username in the userURL is correct")
        self.assertTrue(get_user.entity.baseURLRefs[0].v1Default is not None,
            msg="Expecting username in the userURL is correct")

        delete_user = self.admin_client.delete_user(userId=uid)
        self.assertEqual(delete_user.status_code, 204,
                msg='Create user expected response 204, received {0}'.format(
                delete_user.status_code))
        self.addCleanup(self.service_client.delete_user_hard,
                        userId=get_user.entity.id)
        
    @attr('regression', type='positive')
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
                msg='Create user expected response 201, received {0}'.format(
                create_user.status_code))
        
        get_user_vone = self.admin_client.get_user_by_mosso_id(
                mossoId=mossoId,requestslib_kwargs={'allow_redirects': False})

        self.assertEquals(
                get_user_vone.status_code, 301, "Expected 301, "
                "recieved {0}".format(get_user_vone.status_code))

        self.assertEquals(get_user_vone.headers.get('location'),
                "/v1.1/users/{0}".format(uid),
                "Expected valid location header")

        get_user = self.admin_client.get_user(userId=uid)

        self.assertEquals(get_user.entity.id, uid,
            msg='User Uid expected {0} but received {1}'.format(
            uid, get_user.entity.id))
        self.assertEquals(get_user.entity.key, key,
            msg='User key expected {0} but received {1}'.format(
            key, get_user.entity.key))
        self.assertEquals(get_user.entity.mossoId, mossoId,
            msg='User mossoId expected {0} but received {1}'.format(
            mossoId, get_user.entity.mossoId))
        self.assertEquals(get_user.entity.enabled, enabled,
            msg='User mossoId expected {0} but received {1}'.format(
            enabled, get_user.entity.enabled))
        self.assertTrue(get_user.entity.nastId is not None,
            msg="Expecting nastId is not None")
        self.assertIsInstance(get_user.entity.baseURLRefs, types.ListType,
            msg="Expecting username in the userURL is correct")
        self.assertTrue(get_user.entity.baseURLRefs[0].id is not None,
            msg="Expecting username in the userURL is correct")
        self.assertTrue(get_user.entity.baseURLRefs[0].href is not None,
            msg="Expecting username in the userURL is correct")
        self.assertTrue(get_user.entity.baseURLRefs[0].v1Default is not None,
            msg="Expecting username in the userURL is correct")

        delete_user = self.admin_client.delete_user(userId=uid)
        self.assertEqual(delete_user.status_code, 204,
                msg='Create user expected response 204, received {0}'.format(
                delete_user.status_code))
        self.addCleanup(self.service_client.delete_user_hard,
                        userId=get_user.entity.id)

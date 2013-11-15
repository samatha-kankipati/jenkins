from datetime import datetime, timedelta
from time import struct_time, mktime
import types

from dateutil.parser import parse
from ccengine.common.decorators import attr
from ccengine.common.tools.datagen import rand_name
from ccengine.common.tools.datagen import random_int
from testrepo.common.testfixtures.identity.v1_1.identity \
    import IdentityFixture


class AdminUsersTest(IdentityFixture):
    @classmethod
    def setUpClass(cls):
        """
        Function to create test bed for all the test. Execute once at the
        beginning of class
        @param cls: class

        """
        super(AdminUsersTest, cls).setUpClass()
        cls.uid = rand_name("ccusername")
        cls.key = 'asdasdasd-adsasdads-asdasdasd-adsadsasd'
        cls.mosso_id = random_int(1000000, 9000000)
        cls.nast_id = random_int(1000000, 9000000)
        cls.enabled = True
        cls.create_user = cls.admin_client.create_user(
            id=cls.uid,
            key=cls.key,
            enabled=cls.enabled,
            mosso_id=cls.mosso_id,
            nast_id=cls.nast_id)
        cls.v1_default_mosso = cls.config.identity_api.v1_default_mosso
        cls.v1_default_nast = cls.config.identity_api.v1_default_nast
        cls.v1_default_cfg = cls.v1_default_mosso + cls.v1_default_nast

    @classmethod
    def tearDownClass(cls):
        """
        Function to clean up the data after execution of all the tests
        completed. Execute once at the end of all the tests.
        @param cls: class

        """
        get_user = cls.admin_client_vsec.get_user_by_name(name=cls.uid)
        cls.admin_client.delete_user(user_id=cls.create_user.entity.id)
        cls.service_client.delete_user_hard(get_user.entity.id)

    def _user_entity_assertion(self, user, uid=None, mosso_id=None):
        """
        Common assertion for the user

        """
        uid = uid or self.uid
        mosso_id = mosso_id or self.mosso_id
        self.assertEquals(
            user.entity.id, uid,
            msg=('User Uid expected {0} but received {1}'.format(
                uid, user.entity.id)))
        self.assertEquals(
            user.entity.key, self.key,
            msg=('User key expected {0} but received {1}'.format(
                self.key, user.entity.key)))
        self.assertEquals(
            user.entity.mossoId, mosso_id,
            msg=('User mossoId expected {0} but received {1}'.format(
                mosso_id, user.entity.mossoId)))
        self.assertEquals(
            user.entity.enabled, self.enabled,
            msg=('User status expected {0} but received {1}'.format(
                self.enabled, user.entity.enabled)))
        self.assertTrue(
            user.entity.nastId is not None,
            msg="Expecting nastId is not None")
        self.assertIsInstance(
            user.entity.baseURLRefs, types.ListType,
            msg="Expecting username in the userURL is correct")
        base_url_refs_len = len(user.entity.baseURLRefs)
        for base_url_ref_index in range(base_url_refs_len):
            self.assertTrue(
                user.entity.baseURLRefs[base_url_ref_index].id is not None,
                msg="Expecting username in the userURL is correct")
            self.assertTrue(
                user.entity.baseURLRefs[base_url_ref_index].href is not None,
                msg="Expecting username in the userURL is correct")
            if (user.entity.baseURLRefs[base_url_ref_index].id in
                    self.v1_default_cfg):
                self.assertTrue(
                    user.entity.baseURLRefs[base_url_ref_index].v1Default,
                    msg=("v1Default is not True for {0}".format(
                        user.entity.baseURLRefs[base_url_ref_index].id)))
            else:
                self.assertFalse(
                    user.entity.baseURLRefs[base_url_ref_index].v1Default,
                    msg=("v1Default is not False for {0}".format(
                        user.entity.baseURLRefs[base_url_ref_index].id)))

    def _get_user_modified_delta(self, user):
        """
        Get the user object and return delta value between created and
        update time of the user.

        """
        parsed_time_cr = None
        parsed_time_up = None
        parsed_time_cr = parse(user.entity.created)
        ptime_cr = parsed_time_cr.timetuple()
        parsed_time_up = parse(user.entity.updated)
        ptime_up = parsed_time_up.timetuple()

        self.assertIsInstance(
            ptime_cr, struct_time,
            msg='Date format is correct')
        self.assertIsInstance(
            ptime_up, struct_time,
            msg='Date format is correct')
        cr_time = datetime.fromtimestamp(mktime(ptime_cr))
        up_time = datetime.fromtimestamp(mktime(ptime_up))
        delta = (cr_time - up_time)
        return delta

    @attr('regression', type='positive')
    def test_admin_create_and_delete_user(self):
        """
        Test Create and Delete user response

        """
        user_id = rand_name("ccuseradmin")
        key = "asdasdasd-adsasdads-asdasdasd-adsadsasd"
        mosso_id = random_int(1000000, 9000000)
        enabled = True
        create_user = self.admin_client.create_user(
            id=user_id,
            key=key,
            enabled=enabled,
            mosso_id=mosso_id)
        self._user_entity_assertion(
            create_user, uid=user_id, mosso_id=mosso_id)

        get_user = self.admin_client_vsec.get_user_by_name(name=user_id)
        delete_user = self.admin_client.delete_user(user_id=user_id)
        self.assertEqual(delete_user.status_code, 204,
                         msg="Response for delete user is not 204.")
        self.addCleanup(self.service_client.delete_user_hard,
                        user_id=get_user.entity.id)

    @attr('regression', type='positive')
    def test_admin_list_get_user(self):
        """
        Test get user response

        """
        normal_response_codes = [200, 203]

        get_user_vone = self.admin_client.get_user(user_id=self.uid)
        self.assertIn(
            get_user_vone.status_code, normal_response_codes,
            msg=('Get base URLs expected {0} received {1}'.format(
                normal_response_codes,
                get_user_vone.status_code)))

        self._user_entity_assertion(get_user_vone)
        delta = self._get_user_modified_delta(get_user_vone)
        self.assertLessEqual(
            delta,
            timedelta(days=0, hours=0, minutes=0),
            msg='User hasnt been updated')

    @attr('regression', type='positive')
    def test_admin_list_get_user_enabled(self):
        """
        Docs: Only enabled should be in response
        Verifying get user enable call

        """
        normal_response_codes = [200, 203]

        get_user_vone = self.admin_client.get_user_enabled(user_id=self.uid)
        self.assertIn(
            get_user_vone.status_code,
            normal_response_codes,
            msg=('Get base URLs expected {0} received {1}'.format(
                normal_response_codes,
                get_user_vone.status_code)))
        self.assertEquals(
            get_user_vone.entity.enabled,
            self.enabled,
            msg=('User enabled state expected {0} but received {1}'.format(
                self.enabled,
                self.create_user.entity.enabled)))

    @attr('regression', type='positive')
    def test_admin_list_get_user_groups(self):
        """
        Test to verify get user groups

        """
        normal_response_codes = [200, 203]

        get_user_vone = self.admin_client.get_user_groups(user_id=self.uid)
        self.assertIn(
            get_user_vone.status_code,
            normal_response_codes,
            msg=('Get base URLs expected {0} received {1}'.format(
                normal_response_codes,
                get_user_vone.status_code)))

        self.assertTrue(
            get_user_vone.entity[0].id is not None,
            msg="Expecting nastId is not None")
        self.assertTrue(
            get_user_vone.entity[0].description is not None,
            msg="Expecting nastId is not None")

    @attr('regression', type='positive')
    def test_admin_list_get_user_catalog(self):
        """
        Test to verify get user service catalog response, verifying
        v1Default and publicURL.  Need to verify regions, internalURL once
        the data issue is resolved in environment.

        """
        normal_response_codes = [200, 203]

        get_user_vone = self.admin_client.get_user_service_catalog(
            user_id=self.uid)
        self.assertIn(
            get_user_vone.status_code,
            normal_response_codes,
            msg=('Get base URLs expected {0} received {1}'
                 .format(normal_response_codes, get_user_vone.status_code)))
        self.validate_service_catalog(get_user_vone)

    @attr('regression', type='positive')
    def test_admin_update_user(self):
        """
        Test to verify the update user call

        """
        normal_response_codes = [200, 203]
        uid = rand_name("ccusername")
        key = 'asdasdasd-adsasdads-asdasdasd-adsadsasd'
        upd_key = '12da5dasd-adsas6ad9-asda7dasd-a456ds8sd'
        mosso_id = random_int(1000000, 9000000)
        nast_id = random_int(1000000, 9000000)
        create_user = self.admin_client.create_user(
            id=uid,
            key=key,
            enabled=self.enabled,
            mosso_id=mosso_id,
            nast_id=nast_id)
        self.assertEqual(
            create_user.status_code,
            201,
            msg=('Create user expected response 201, received {0}'.format(
                create_user.status_code)))

        self.assertEqual(
            create_user.status_code,
            201,
            msg=('Create user expected response 201, received {0}'
                 .format(create_user.status_code)))
        self.assertIsNotNone(
            create_user.entity.id,
            msg='Create user returned id as None')

        get_user = self.admin_client_vsec.get_user_by_name(name=uid)
        self.addCleanup(self.service_client.delete_user_hard,
                        user_id=get_user.entity.id)
        self.addCleanup(self.admin_client.delete_user,
                        user_id=create_user.entity.id)

        update_user = self.admin_client.update_user(
            user_id=uid,
            id=uid,
            key=upd_key,
            enabled=self.enabled,
            mosso_id=mosso_id,
            nast_id=nast_id)
        self.assertIn(
            update_user.status_code,
            normal_response_codes,
            msg=('Get base URLs expected {0} received {1}'.format(
                normal_response_codes,
                update_user.status_code)))

        self._user_entity_assertion(update_user, uid=uid, mosso_id=mosso_id)
        delta = self._get_user_modified_delta(update_user)

        self.assertLessEqual(
            delta, timedelta(days=0, hours=0, minutes=0),
            msg=('Expected delta {0} but received {1}'
                 .format(timedelta(days=0, hours=0, minutes=0), delta)))

    @attr('regression', type='positive')
    def test_admin_update_user_enabled(self):
        """
        Test to verify update user enable call

        """
        normal_response_codes = [200, 203]
        uid = rand_name("ccusername")
        key = 'asdasdasd-adsasdads-asdasdasd-adsadsasd'
        mosso_id = random_int(1000000, 9000000)
        nast_id = random_int(1000000, 9000000)
        enabled = False
        upd_enabled = True
        create_user = self.admin_client.create_user(
            id=uid,
            key=key,
            enabled=enabled,
            mosso_id=mosso_id,
            nast_id=nast_id)
        self.assertEqual(
            create_user.status_code,
            201,
            msg=('Create user expected response 201, received {0}'.format(
                create_user.status_code)))
        self.assertIsNotNone(
            create_user.entity.id,
            msg='Create user returned id as None')

        get_user = self.admin_client_vsec.get_user_by_name(name=uid)
        self.addCleanup(self.service_client.delete_user_hard,
                        user_id=get_user.entity.id)
        self.addCleanup(self.admin_client.delete_user,
                        user_id=create_user.entity.id)

        update_user = self.admin_client.update_user_enabled(
            user_id=uid,
            enabled=upd_enabled)
        self.assertIn(
            update_user.status_code,
            normal_response_codes,
            msg=('Get base URLs expected {0} received {1}'.format(
                normal_response_codes,
                update_user.status_code)))
        self.assertEquals(
            update_user.entity.enabled,
            upd_enabled,
            msg=('Enabled state expected {0} but received {1}'.format(
                upd_enabled,
                update_user.entity.enabled)))

    @attr('regression', type='positive')
    def test_admin_list_get_user_key(self):
        """
        Test to verify get user key call

        """
        normal_response_codes = [200, 203]

        get_user_vone = self.admin_client.get_user_key(user_id=self.uid)
        self.assertIn(
            get_user_vone.status_code,
            normal_response_codes,
            msg=('Get base URLs expected {0} received {1}'.format(
                normal_response_codes,
                get_user_vone.status_code)))

        self.assertEquals(
            get_user_vone.entity.key,
            self.key,
            msg=('User key expected {0} but received {1}'
                 .format(self.key, get_user_vone.entity.key)))

    @attr('regression', type='positive')
    def test_admin_list_set_user_key(self):
        """
        Test to verify set user key call

        """
        normal_response_codes = [200, 203]
        uid = rand_name("ccusername")
        key = 'asdasdasd-adsasdads-asdasdasd-adsadsasd'
        upd_key = '12da5dasd-adsas6ad9-asda7dasd-a456ds8sd'
        mosso_id = random_int(1000000, 9000000)
        nast_id = random_int(1000000, 9000000)
        create_user = self.admin_client.create_user(
            id=uid,
            key=key,
            enabled=self.enabled,
            mosso_id=mosso_id,
            nast_id=nast_id)
        self.assertEqual(
            create_user.status_code,
            201,
            msg=('Create user expected response 201, received {0}'
                 .format(create_user.status_code)))
        self.assertIsNotNone(
            create_user.entity.id,
            msg='Create user returned id as None')

        get_user = self.admin_client_vsec.get_user_by_name(name=uid)
        self.addCleanup(self.service_client.delete_user_hard,
                        user_id=get_user.entity.id)
        self.addCleanup(self.admin_client.delete_user,
                        user_id=create_user.entity.id)

        get_user_vone = self.admin_client.set_user_key(user_id=uid,
                                                       key=upd_key)
        self.assertIn(
            get_user_vone.status_code, normal_response_codes,
            msg=('Get base URLs expected {0} received {1}'.format(
                normal_response_codes,
                get_user_vone.status_code)))

        self.assertEquals(
            get_user_vone.entity.key, upd_key,
            msg=('User key expected {0} but received {1}'.format(
                upd_key, get_user_vone.entity.key)))

    @attr('regression', type='positive')
    def test_admin_get_user_by_nast_id(self):
        """
        Verifies that identity admin can get the user by nast id

        """
        get_user_vone = self.admin_client.get_user_by_nast_id(
            nast_id=self.create_user.entity.nastId,
            requestslib_kwargs={'allow_redirects': False})

        self.assertEquals(get_user_vone.status_code, 301,
                          "Expected 301, recieved {0}"
                          .format(get_user_vone.status_code))
        self.assertEquals(
            get_user_vone.headers.get('location'),
            "/v1.1/users/{0}".format(self.uid),
            "Expected valid location header")

        get_user = self.admin_client.get_user(user_id=self.uid)
        self._user_entity_assertion(get_user)

    @attr('regression', type='positive')
    def test_admin_get_user_by_mosso_id(self):
        """
        Verifies that identity admin can get the user by mosso id

        """
        get_user_vone = self.admin_client.get_user_by_mosso_id(
            mosso_id=self.mosso_id,
            requestslib_kwargs={'allow_redirects': False})

        self.assertEquals(
            get_user_vone.status_code, 301,
            "Expected 301, recieved {0}".format(get_user_vone.status_code))
        self.assertEquals(
            get_user_vone.headers.get('location'),
            "/v1.1/users/{0}".format(self.uid),
            "Expected valid location header")

        get_user = self.admin_client.get_user(user_id=self.uid)
        self._user_entity_assertion(get_user)

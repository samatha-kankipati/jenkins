from datetime import datetime, timedelta
from dateutil.parser import parse
from time import struct_time, mktime
import types

from ccengine.common.decorators import attr
from ccengine.common.tools.datagen import rand_name
from ccengine.common.tools.datagen import random_int
from testrepo.common.testfixtures.identity.ldap.ldap_fixture \
    import LDAPFixture
from testrepo.common.testfixtures.identity.v1_1.identity import IdentityFixture


class AdminTokenTest(LDAPFixture, IdentityFixture):

    @classmethod
    def setUpClass(cls):
        super(AdminTokenTest, cls).setUpClass()
        cls.password = 'CCPassword1'
        cls.key = 'asdasdasd-adsasdads-asdasdasd-adsadsasd'
        cls.enabled = True
        cls.uid = rand_name("ccusername")
        cls.mossoId = random_int(1000000, 9000000)
        nastId_gen = random_int(1000000, 9000000)

        create_user = cls.admin_client.create_user(
            id=cls.uid,
            key=cls.key,
            enabled=cls.enabled,
            mossoId=cls.mossoId,
            nastId=nastId_gen)
        cls.nastId = create_user.entity.nastId
        get_user = cls.admin_client_vsec.get_user_by_name(name=cls.uid)
        cls.admin_client_vsec.add_user_credentials(
            userId=get_user.entity.id,
            username=get_user.entity.username,
            password=cls.password)

        auth_resp = cls.admin_client.authenticate_password(
            username=cls.uid,
            password=cls.password)

        cls.admin_client.revoke_token(tokenId=auth_resp.entity.token.id)
        cls.admin_client.get_token(tokenId=auth_resp.entity.token.id)

        #Deleting token for the user in ldap
        user = cls.ldap_client.get_users('uid={user_id}'.format(
            user_id=cls.uid))
        cls.token_dn = str(user[1][0])
        cls.ldap_client.delete_entry(cls.token_dn)

    @classmethod
    def tearDownClass(cls):
        get_user = cls.admin_client_vsec.get_user_by_name(name=cls.uid)
        cls.admin_client.delete_user(userId=cls.uid)
        cls.service_client.delete_user_hard(userId=get_user.entity.id)

    @attr('regression', type='negative')
    def test_admin_get_user(self):
        """
        Test Admin get user call for a user, after deleting the user token
        in ldap

        """
        normal_response_codes = [200, 203]
        get_user_vone = self.admin_client.get_user(userId=self.uid)
        self.assertIn(
            get_user_vone.status_code,
            normal_response_codes,
            msg=('Get base URLs expected {0} received {1}'
                 .format(normal_response_codes, get_user_vone.status_code)))

        self.assertEquals(
            get_user_vone.entity.id,
            self.uid,
            msg=('User Uid expected {0} but received {1}'
                 .format(self.uid, get_user_vone.entity.id)))
        self.assertEquals(
            get_user_vone.entity.key,
            self.key,
            msg=('User key expected {0} but received {1}'
                 .format(self.key, get_user_vone.entity.key)))
        self.assertEquals(
            get_user_vone.entity.mossoId,
            self.mossoId,
            msg=('User mossoId expected {0} but received {1}'
                 .format(self.mossoId, get_user_vone.entity.mossoId)))
        self.assertEquals(
            get_user_vone.entity.enabled,
            self.enabled,
            msg=('User Status expected {0} but received {1}'
                 .format(self.enabled, get_user_vone.entity.enabled)))
        self.assertIsNotNone(
            get_user_vone.entity.nastId,
            msg=('Nast Id expected but received {0}'
                 .format(get_user_vone.entity.nastId)))
        self.assertIsInstance(
            get_user_vone.entity.baseURLRefs,
            types.ListType,
            msg="Expecting username in the userURL is correct")
        self.assertIsNotNone(
            get_user_vone.entity.baseURLRefs[0].id,
            msg=('Expecting Id in baseURLRef but received {0}'
                 .format(get_user_vone.entity.baseURLRefs[0].id)))
        self.assertIsNotNone(
            get_user_vone.entity.baseURLRefs[0].href,
            msg=('Expecting href in baseURLRef but received {0}'
                 .format(get_user_vone.entity.baseURLRefs[0].href)))
        self.assertIsNotNone(
            get_user_vone.entity.baseURLRefs[0].v1Default,
            msg=('Expecting v1Default in baseURLRef but received {0}'
                 .format(get_user_vone.entity.baseURLRefs[0].v1Default)))

        parsed_time_cr = None
        parsed_time_up = None

        parsed_time_cr = parse(get_user_vone.entity.created)
        ptime_cr = parsed_time_cr.timetuple()
        parsed_time_up = parse(get_user_vone.entity.updated)
        ptime_up = parsed_time_up.timetuple()

        self.assertIsInstance(
            ptime_cr,
            struct_time,
            msg='Date format is correct')
        self.assertIsInstance(
            ptime_up,
            struct_time,
            msg='Date format is correct')
        cr_time = datetime.fromtimestamp(mktime(ptime_cr))
        up_time = datetime.fromtimestamp(mktime(ptime_up))
        delta = (cr_time - up_time)
        self.assertLessEqual(
            delta,
            timedelta(days=0, hours=0, minutes=0),
            msg='User hasnt been updated')

    @attr('regression', type='negative')
    def test_admin_get_user_enabled(self):
        """
        Test Admin get user enabled call for a user, after deleting the
        user token in ldap

        """
        normal_response_codes = [200, 203]

        get_user_vone = self.admin_client.get_user_enabled(userId=self.uid)
        self.assertIn(
            get_user_vone.status_code,
            normal_response_codes,
            msg=('Get user enabled expected {0} received {1}'
                 .format(normal_response_codes, get_user_vone.status_code)))

        self.assertEquals(
            get_user_vone.entity.enabled,
            self.enabled,
            msg=('User enabled state expected {0} but received {1}'
                 .format(self.enabled, get_user_vone.entity.enabled)))

    @attr('regression', type='negative')
    def test_admin_get_user_groups(self):
        """
        Test Admin get user groups call for a user, after deleting the
        user token in ldap

        """
        normal_response_codes = [200, 203]

        get_user_vone = self.admin_client.get_user_groups(userId=self.uid)
        self.assertIn(
            get_user_vone.status_code,
            normal_response_codes,
            msg=('Get user groups expected {0} received {1}'
                 .format(normal_response_codes, get_user_vone.status_code)))

        self.assertIsNotNone(
            get_user_vone.entity[0].id,
            msg=('Group Id expected but received {0}'
                 .format(get_user_vone.entity[0].id)))
        self.assertIsNotNone(
            get_user_vone.entity[0].description,
            msg=('Group Description expected but received {0}'
                 .format(get_user_vone.entity[0].description)))

    @attr('regression', type='negative')
    def test_admin_get_user_catalog(self):
        """
        Test Admin get user service catalog call for a user, after deleting
        the user token in ldap

        """
        normal_response_codes = [200, 203]

        get_user_vone = self.admin_client.get_user_service_catalog(
            userId=self.uid)
        self.assertIn(
            get_user_vone.status_code,
            normal_response_codes,
            msg=('Get Service Catalog expected {0} received {1}'
                 .format(normal_response_codes, get_user_vone.status_code)))
        self.assertIsNotNone(
            get_user_vone.entity[0].endpoints[0].region,
            msg=('In Service Cataglog, region expected but received {0}'
                 .format(get_user_vone.entity[0].endpoints[0].region)))
        self.assertIsNotNone(
            get_user_vone.entity[2].endpoints[0].publicURL,
            msg=('In Service Cataglog, publicURL expected but received {0}'
                 .format(get_user_vone.entity[2].endpoints[0].publicURL)))
        self.assertIsNotNone(
            get_user_vone.entity[3].endpoints[0].internalURL,
            msg=('In Service Cataglog, internalURL expected but received {0}'
                 .format(get_user_vone.entity[3].endpoints[0].internalURL)))
        self.assertIsNotNone(
            get_user_vone.entity[8].endpoints[0].v1Default,
            msg=('In Service Cataglog, v1Default expected but received {0}'
                 .format(get_user_vone.entity[8].endpoints[0].v1Default)))

    @attr('regression', type='negative')
    def test_admin_get_user_key(self):
        """
        Test Admin get user key call for a user, after deleting the
        user token in ldap

        """
        normal_response_codes = [200, 203]

        get_user_vone = self.admin_client.get_user_key(userId=self.uid)
        self.assertIn(
            get_user_vone.status_code,
            normal_response_codes,
            msg=('Get base URLs expected {0} received {1}'
                 .format(normal_response_codes, get_user_vone.status_code)))

        self.assertEquals(
            get_user_vone.entity.key,
            self.key,
            msg=('Get user key expected {0} but received {1}'
                 .format(self.key, get_user_vone.entity.key)))

    @attr('regression', type='negative')
    def test_admin_get_alternate_nast(self):
        """
        Test Admin get user by nast Id call for a user, after deleting the
        user token in ldap

        """
        get_user_vone = self.admin_client.get_user_by_nast_id(
            nastId=self.nastId,
            requestslib_kwargs={'allow_redirects': False})

        self.assertEquals(
            get_user_vone.status_code,
            301,
            "Expected 301, recieved {0}".format(get_user_vone.status_code))

        self.assertEquals(
            get_user_vone.headers.get('location'),
            "/v1.1/users/{0}".format(self.uid),
            "Expected valid location header")

        get_user = self.admin_client.get_user(userId=self.uid)

        self.assertEquals(
            get_user.entity.id,
            self.uid,
            msg=('User Uid expected {0} but received {1}'
                 .format(self.uid, get_user.entity.id)))
        self.assertEquals(
            get_user.entity.key,
            self.key,
            msg=('User key expected {0} but received {1}'
                 .format(self.key, get_user.entity.key)))
        self.assertEquals(
            get_user.entity.mossoId,
            self.mossoId,
            msg=('User mossoId expected {0} but received {1}'
                 .format(self.mossoId, get_user.entity.mossoId)))
        self.assertEquals(
            get_user.entity.enabled,
            self.enabled,
            msg=('User mossoId expected {0} but received {1}'
                 .format(self.enabled, get_user.entity.enabled)))
        self.assertIsNotNone(
            get_user.entity.nastId,
            msg=('Nast Id expected but received {0}'
                 .format(get_user.entity.nastId)))
        self.assertIsInstance(
            get_user.entity.baseURLRefs,
            types.ListType,
            msg="Expecting username in the userURL is correct")
        self.assertIsNotNone(
            get_user.entity.baseURLRefs[0].id,
            msg=('Expecting Id in baseURLRef but received {0}'
                 .format(get_user.entity.baseURLRefs[0].id)))
        self.assertIsNotNone(
            get_user.entity.baseURLRefs[0].href,
            msg=('Expecting href in baseURLRef but received {0}'
                 .format(get_user.entity.baseURLRefs[0].href)))
        self.assertIsNotNone(
            get_user.entity.baseURLRefs[0].v1Default,
            msg=('Expecting v1Default in baseURLRef but received {0}'
                 .format(get_user.entity.baseURLRefs[0].v1Default)))

    @attr('regression', type='negative')
    def test_admin_get_alternate_mosso(self):
        """
        Test Admin get user mosso id call for a user, after deleting the
        user token in ldap

        """
        get_user_vone = self.admin_client.get_user_by_mosso_id(
            mossoId=self.mossoId,
            requestslib_kwargs={'allow_redirects': False})

        self.assertEquals(
            get_user_vone.status_code,
            301,
            "Expected 301, recieved {0}".format(get_user_vone.status_code))
        self.assertEquals(
            get_user_vone.headers.get('location'),
            "/v1.1/users/{0}".format(self.uid),
            "Expected valid location header")

        get_user = self.admin_client.get_user(userId=self.uid)
        self.assertEquals(
            get_user.entity.id,
            self.uid,
            msg=('User Uid expected {0} but received {1}'
                 .format(self.uid, get_user.entity.id)))
        self.assertEquals(
            get_user.entity.key,
            self.key,
            msg=('User key expected {0} but received {1}'
                 .format(self.key, get_user.entity.key)))
        self.assertEquals(
            get_user.entity.mossoId,
            self.mossoId,
            msg=('User mossoId expected {0} but received {1}'
                 .format(self.mossoId, get_user.entity.mossoId)))
        self.assertEquals(
            get_user.entity.enabled,
            self.enabled,
            msg=('User mossoId expected {0} but received {1}'
                 .format(self.enabled, get_user.entity.enabled)))
        self.assertIsNotNone(
            get_user.entity.nastId,
            msg=('Nast Id expected but received {0}'
                 .format(get_user.entity.nastId)))
        self.assertIsInstance(
            get_user.entity.baseURLRefs,
            types.ListType,
            msg="Expecting username in the userURL is correct")
        self.assertIsNotNone(
            get_user.entity.baseURLRefs[0].id,
            msg=('Expecting Id in baseURLRef but received {0}'
                 .format(get_user.entity.baseURLRefs[0].id)))
        self.assertIsNotNone(
            get_user.entity.baseURLRefs[0].href,
            msg=('Expecting href in baseURLRef but received {0}'
                 .format(get_user.entity.baseURLRefs[0].href)))
        self.assertIsNotNone(
            get_user.entity.baseURLRefs[0].v1Default,
            msg=('Expecting v1Default in baseURLRef but received {0}'
                 .format(get_user.entity.baseURLRefs[0].v1Default)))

from ccengine.common.decorators import attr
from ccengine.common.tools.datagen import rand_name
from ccengine.common.tools.datagen import random_int
from testrepo.common.testfixtures.identity.ldap.ldap_fixture \
    import LDAPFixture
from testrepo.common.testfixtures.identity.v1_1.identity \
    import IdentityFixture
from testrepo.common.testfixtures.identity.v2_0.identity \
    import IdentityAdminFixture


class LdapTest(LDAPFixture, IdentityFixture, IdentityAdminFixture):

    @classmethod
    def setUpClass(cls):
        super(LdapTest, cls).setUpClass()
        cls.ldap_client = cls.ldap_client

        cls.uid = rand_name("ccusername")
        key = 'asdasdasd-adsasdads-asdasdasd-adsadsasd'
        mossoId = random_int(1000000, 9000000)
        enabled = True
        cls.create_user = cls.admin_client.create_user(
            id=cls.uid,
            key=key,
            enabled=enabled,
            mossoId=mossoId,
            )
        cls.get_user = cls.admin_client_vsec.get_user_by_name(name=cls.uid)
        cls.user_id = cls.get_user.entity.id

    @classmethod
    def tearDownClass(cls):
        cls.admin_client.delete_user(cls.user_id)
        cls.service_client.delete_user_hard(
            cls.user_id)

    @attr('smoke', type='positive')
    def test_admin_create_user(self):
        '''
        Create user in v1.1
        '''
        normal_response_codes = [201]
        self.assertIn(self.create_user.status_code, normal_response_codes,
            msg='Create user response code expected {0} received {1}'.format(
                normal_response_codes,
                self.create_user.status_code))

    @attr('smoke', type='positive')
    def test_find_user_uid(self):
        '''
        Search for the user in the directory
        '''
        user = self.ldap_client.get_users('uid=' + self.uid)
        username = user[0][1]['uid'][0]
        self.token_dn = str(user[1][0])
        self.token_dn1 = str(user[2][0])
        self.ldap_client.delete_entry(self.token_dn)
        self.ldap_client.delete_entry(self.token_dn1)
        user = self.ldap_client.get_users('uid=' + self.uid)
        self.assertIn(username,
                      [self.uid],
                      msg="did not get expected user ID")

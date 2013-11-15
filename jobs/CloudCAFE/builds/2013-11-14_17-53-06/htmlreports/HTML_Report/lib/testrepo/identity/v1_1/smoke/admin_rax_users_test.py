from ccengine.common.tools.datagen import rand_name
from ccengine.common.tools.datagen import random_int
from testrepo.common.testfixtures.identity.v1_1.identity \
    import IdentityFixture
from ccengine.common.decorators import attr


class AdminUsersTest(IdentityFixture):
    @classmethod
    def setUpClass(cls):
        """
        Function to create test bed for all the test. Execute once at the
        beginning of class
        @param cls: instance of class
        """
        super(AdminUsersTest, cls).setUpClass()
        cls.user_id = rand_name("ccuseradmin")
        cls.key = "asdasdasd-zxcvbnmqw-123456789-adsadsasd"
        cls.mosso_id = random_int(1000000, 9000000)
        cls.enabled = True
        cls.create_user = cls.admin_client.create_user(id=cls.user_id,
                                                       key=cls.key,
                                                       enabled=cls.enabled,
                                                       mosso_id=cls.mosso_id)
        cls.id = cls.admin_client_vsec.get_user_by_name(
            name=cls.user_id).entity.id
        cls.nast_id = cls.create_user.entity.nastId

    @classmethod
    def tearDownClass(cls):
        """
        Function to clean up the data after execution of all the tests
        completed. Execute once at the end of all the tests.
        @param cls: class
        """
        cls.admin_client.delete_user(user_id=cls.user_id)
        cls.service_client.delete_user_hard(user_id=cls.id)

    @attr('smoke', type='positive')
    def test_admin_create_and_delete_user(self):
        """
        Verifies that identity admin can create and delete user admin
        """
        user_id = rand_name("ccusername")
        key = "asdasdasd-adsasdads-asdasdasd-adsadsasd"
        mosso_id = random_int(1000000, 9000000)
        create_user = self.admin_client.create_user(id=user_id,
                                                    key=key,
                                                    enabled=True,
                                                    mosso_id=mosso_id)
        self.assertEqual(create_user.status_code, 201,
                         msg="Response for create user is not 201.")
        get_user = self.admin_client_vsec.get_user_by_name(name=user_id)
        delete_user = self.admin_client.delete_user(user_id=user_id)
        self.assertEqual(delete_user.status_code, 204,
                         msg="Response for delete user is not 204.")
        self.addCleanup(self.service_client.delete_user_hard,
                        user_id=get_user.entity.id)

    @attr('smoke', type='positive')
    def test_admin_list_get_user(self):
        """
        Verifies that identity admin can get user admin by username
        """
        normal_response_codes = [200, 203]
        get_user_vone = self.admin_client.get_user(user_id=self.user_id)
        self.assertIn(get_user_vone.status_code, normal_response_codes,
                      msg="Response for get user is not in {0}"
                      .format(normal_response_codes))

    @attr('smoke', type='positive')
    def test_admin_list_get_user_enabled(self):
        """
        Verifies that identity admin can get enabled user admin
        """
        normal_response_codes = [200, 203]
        get_user_vone = self.admin_client.get_user_enabled(
            user_id=self.user_id)
        self.assertIn(get_user_vone.status_code, normal_response_codes,
                      msg="Response fot get enabled user is not in {0}"
                      .format(normal_response_codes))

    @attr('smoke', type='positive')
    def test_admin_list_get_user_groups(self):
        """
        Verifies that identity admin can get groups for user admin
        """
        normal_response_codes = [200, 203]
        get_user_vone = self.admin_client.get_user_groups(user_id=self.user_id)
        self.assertIn(get_user_vone.status_code, normal_response_codes,
                      msg="Response fot get groups for user is not in {0}"
                      .format(normal_response_codes))

    @attr('smoke', type='positive')
    def test_admin_list_get_user_catalog(self):
        """
        Verifies that identity admin can get catalog for user admin
        """
        normal_response_codes = [200, 203]
        get_user_vone = self.admin_client.get_user_service_catalog(
            user_id=self.user_id)
        self.assertIn(get_user_vone.status_code, normal_response_codes,
                      msg="Response fot get catalog for user is not in {0}"
                      .format(normal_response_codes))

    @attr('smoke', type='positive')
    def test_admin_update_user(self):
        """
        Verifies that identity admin can update user admin
        """
        normal_response_codes = [200, 203]
        user_id = rand_name("ccusername")
        key = 'asdasdasd-adsasdads-asdasdasd-adsadsasd'
        upd_key = 'asda3dfsd-ad5asdads-as7ajhgsd-adsadseee'
        mosso_id = random_int(1000000, 9000000)
        enabled = True
        create_user = self.admin_client.create_user(id=user_id,
                                                    key=key,
                                                    enabled=enabled,
                                                    mosso_id=mosso_id)
        self.assertEqual(create_user.status_code, 201,
                         msg="Response for create user is not 201.")
        # delete user after test completion
        get_user = self.admin_client_vsec.get_user_by_name(name=user_id)
        self.addCleanup(self.admin_client.delete_user, user_id=user_id)
        self.addCleanup(self.service_client.delete_user_hard,
                        user_id=get_user.entity.id)

        update_user = self.admin_client.update_user(user_id=user_id,
                                                    id=user_id,
                                                    key=upd_key,
                                                    enabled=enabled,
                                                    mosso_id=mosso_id)
        self.assertIn(update_user.status_code, normal_response_codes,
                      msg="Response for update user is not in {0}"
                      .format(normal_response_codes))

    @attr('smoke', type='positive')
    def test_admin_update_user_enabled(self):
        """
        Verifies that identity admin can enable or disable user admin
        """
        normal_response_codes = [200, 203]
        user_id = rand_name("ccusername")
        key = 'asdasdasd-adsasdads-asdasdasd-adsadsasd'
        mosso_id = random_int(1000000, 9000000)
        enabled = False
        upd_enabled = True
        create_user = self.admin_client.create_user(id=user_id,
                                                    key=key,
                                                    enabled=enabled,
                                                    mosso_id=mosso_id)
        self.assertEqual(create_user.status_code, 201,
                         msg="Response for create user is not 201.")
        # delete user after test completion
        get_user = self.admin_client_vsec.get_user_by_name(name=user_id)
        self.addCleanup(self.admin_client.delete_user, user_id=user_id)
        self.addCleanup(self.service_client.delete_user_hard,
                        user_id=get_user.entity.id)

        update_user = self.admin_client.update_user_enabled(
            user_id=user_id,
            enabled=upd_enabled)
        self.assertIn(update_user.status_code, normal_response_codes,
                      msg="Response for enable user is not in {0}"
                      .format(normal_response_codes))

    @attr('smoke', type='positive')
    def test_admin_list_get_user_key(self):
        """
        Verifies that identity admin can get key for user admin
        """
        normal_response_codes = [200, 203]
        get_user_vone = self.admin_client.get_user_key(user_id=self.user_id)
        self.assertIn(get_user_vone.status_code, normal_response_codes,
                      msg="Response for get user key is not in {0}"
                      .format(normal_response_codes))

    @attr('smoke', type='positive')
    def test_admin_list_set_user_key(self):
        """
        Verifies that identity admin can set key for user admin
        """
        normal_response_codes = [200, 203]
        upd_key = '12da5dasd-adsas6ad9-asda7dasd-a456ds8sd'
        get_user_vone = self.admin_client.set_user_key(user_id=self.user_id,
                                                       key=upd_key)
        self.assertIn(get_user_vone.status_code, normal_response_codes,
                      msg="Response for set user key is not in {0}"
                      .format(normal_response_codes))

    @attr('smoke', type='positive')
    def test_admin_get_user_by_nast_id(self):
        """
        Verifies that identity admin can get user by nast_id
        """
        user_vone = self.admin_client.get_user_by_nast_id(
            nast_id=self.nast_id,
            requestslib_kwargs={'allow_redirects': False})
        self.assertEquals(user_vone.status_code, 301,
                          msg="Response for get user by nast ID is not 301.")

    @attr('smoke', type='positive')
    def test_admin_get_user_by_mosso_id(self):
        """
        Verifies that identity admin can get the user by mosso id
        """
        user_vone = self.admin_client.get_user_by_mosso_id(
            mosso_id=self.mosso_id,
            requestslib_kwargs={'allow_redirects': False})
        self.assertEquals(user_vone.status_code, 301,
                          msg="Response to get a user by mosso_id is not 301.")

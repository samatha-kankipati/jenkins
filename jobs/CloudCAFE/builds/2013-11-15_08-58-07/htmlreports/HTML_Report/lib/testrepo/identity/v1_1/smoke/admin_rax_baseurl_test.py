from ccengine.common.decorators import attr
from ccengine.common.tools.datagen import rand_name, random_int
from testrepo.common.testfixtures.identity.v1_1.identity \
    import IdentityFixture


class AdminBaseurlTest(IdentityFixture):
    @classmethod
    def setUpClass(cls):
        super(AdminBaseurlTest, cls).setUpClass()
        cls.service_name = 'cloudFiles'

        type_mosso = cls.config.identity_api.type_mosso
        default_region = cls.config.identity_api.default_region
        public_url = cls.config.identity_api.public_url
        internal_url = cls.config.identity_api.internal_url
        admin_url = cls.config.identity_api.admin_url
        endpoint_template_id = random_int(10000, 1000000000)
        endpoint_template_name = rand_name("ccTestEndpoint")
        cls.add_endpoint_template_resp = \
            cls.admin_client_vsec.add_endpoint_template(
                id=endpoint_template_id,
                name=endpoint_template_name,
                type=type_mosso,
                region=default_region,
                enabled=True,
                public_url=public_url,
                internal_url=internal_url,
                admin_url=admin_url)

        cls.admin_client_vsec.get_endpoint_template(
            cls.add_endpoint_template_resp.entity.id)

    @classmethod
    def tearDownClass(cls):
        cls.admin_client_vsec.delete_endpoint_template(
            endpoint_template_id=cls.add_endpoint_template_resp.entity.id)

    @attr('smoke', type='positive')
    def test_admin_get_base_urls_enabled(self):
        """
        @summary: Retrieves all the baseUrls that are enabled
        """
        normal_response_codes = [200, 203]
        get_base_urls_enbled = self.admin_client.list_base_urls_enabled()
        self.assertIn(
            get_base_urls_enbled.status_code, normal_response_codes,
            msg='Get base URLs expected {0} received {1}'
            .format(normal_response_codes, get_base_urls_enbled.status_code))

    @attr('smoke', type='positive')
    def test_admin_get_base_urls(self):
        """
        @summary: Retrieves all the baseUrls
        """
        normal_response_codes = [200, 203]
        get_base_url = self.admin_client.list_base_urls()
        self.assertIn(
            get_base_url.status_code, normal_response_codes,
            msg='Get base URL expected {0} received {1}'
            .format(normal_response_codes, get_base_url.status_code))

    @attr('smoke', type='positive')
    def test_admin_get_base_urls_service_name(self):
        """
        @summary: Retrieves baseUrls with the specified service name
        """
        normal_response_codes = [200, 203]
        get_base_url = self.admin_client.list_base_urls(
            service_name=self.service_name)
        self.assertIn(get_base_url.status_code, normal_response_codes,
                      msg='Get base URL by service expected {0} received {1}'
                      .format(normal_response_codes,
                              get_base_url.status_code))

    @attr('smoke', type='positive')
    def test_admin_get_base_urls_enabled_service_name(self):
        """
        @summary: Retrieves all baseUrls that are enabled with the specified
        service name
        """
        normal_response_codes = [200, 203]
        get_base_urls_enbled = self.admin_client.list_base_urls_enabled(
            service_name=self.service_name)
        self.assertIn(get_base_urls_enbled.status_code, normal_response_codes,
                      msg='Get enabled URL by serv expected {0} received {1}'
                      .format(normal_response_codes,
                              get_base_urls_enbled.status_code))

    @attr('smoke', type='positive')
    def test_admin_get_base_url(self):
        """
        @summary: Retrieves the specified baseUrl
        """
        normal_response_codes = [200, 203]
        get_url_id = self.admin_client.list_base_urls_enabled(
            service_name=self.service_name)
        get_base_url = self.admin_client.get_base_url(
            base_url_id=get_url_id.entity[0].id)
        self.assertIn(get_base_url.status_code, normal_response_codes,
                      msg='Get base URL expected {0} received {1}'.format(
                          normal_response_codes,
                          get_base_url.status_code))

    @attr('smoke', type='positive')
    def test_admin_get_base_url_user(self):
        """
        @summary: Retrieves baseUrl for the user
        """
        normal_response_codes = [200, 203]
        uid = rand_name("ccusername")
        key = 'asdasdasd-adsasdads-asdasdasd-adsadsasd'
        mosso_id = random_int(1000000, 9000000)
        nast_id = random_int(1000000, 9000000)
        enabled = True
        create_user = self.admin_client.create_user(
            id=uid,
            key=key,
            enabled=enabled,
            mosso_id=mosso_id,
            nast_id=nast_id)
        self.assertEqual(create_user.status_code, 201,
                         msg='Create user exp. response 201 received {0}'
                         .format(create_user.status_code))

        get_base_url = self.admin_client.get_user_base_urls(
            user_id=uid)
        self.assertIn(get_base_url.status_code, normal_response_codes,
                      msg='Get base URLs expected {0} received {1}'
                      .format(normal_response_codes,
                              get_base_url.status_code))

        get_user = self.admin_client_vsec.get_user_by_name(name=uid)
        delete_user = self.admin_client.delete_user(user_id=uid)
        self.assertEqual(delete_user.status_code, 204,
                         msg='Delete user exp. response 201 received {0}'
                         .format(delete_user.status_code))
        self.addCleanup(self.service_client.delete_user_hard,
                        user_id=get_user.entity.id)

    @attr('smoke', type='positive')
    def test_admin_remove_base_url_user(self):
        """
        @summary: Removes baseUrl from the user
        """
        normal_response_codes = [204]
        uid = rand_name("ccusername")
        key = 'asdasdasd-adsasdads-asdasdasd-adsadsasd'
        mosso_id = random_int(1000000, 9000000)
        nast_id = random_int(1000000, 9000000)
        enabled = True
        v1_default = True
        create_user = self.admin_client.create_user(
            id=uid,
            key=key,
            enabled=enabled,
            mosso_id=mosso_id,
            nast_id=nast_id)
        self.assertEqual(create_user.status_code, 201,
                         msg='Create user exp. response 201 received {0}'
                         .format(create_user.status_code))
        get_url_id = self.admin_client.list_base_urls_enabled(
            service_name=self.service_name)
        add_base_url = self.admin_client.add_user_base_url(
            id='133',
            v1_default=v1_default,
            user_id=uid)
        self.assertEqual(add_base_url.status_code, 201,
                         msg='{0}{1}'.format(
                             'Add base URL response 201 received ',
                             add_base_url.status_code))

        remove_base_url = self.admin_client.delete_user_base_url(
            base_url_id='133',
            user_id=uid)
        self.assertIn(remove_base_url.status_code, normal_response_codes,
                      msg='Remove base URLs expected {0} received {1}'
                      .format(normal_response_codes,
                              remove_base_url.status_code))

        add_base_url_sec = self.admin_client.add_user_base_url(
            id='133',
            v1_default=v1_default,
            user_id=uid)
        self.assertEqual(add_base_url_sec.status_code, 201,
                         msg='{0}{1}'.format(
                             'Add base URL response 201 received ',
                             add_base_url_sec.status_code))
        get_user = self.admin_client_vsec.get_user_by_name(name=uid)
        delete_user = self.admin_client.delete_user(user_id=uid)
        self.assertEqual(delete_user.status_code, 204,
                         msg='Delete user exp. response 201 received {0}'
                         .format(delete_user.status_code))
        self.addCleanup(self.service_client.delete_user_hard,
                        user_id=get_user.entity.id)

    @attr('smoke', type='positive')
    def test_admin_add_base_url_user(self):
        """
        @summary: Add baseUrl to the user
        """
        normal_response_codes = [201]
        uid = rand_name("ccusername")
        key = 'asdasdasd-adsasdads-asdasdasd-adsadsasd'
        mosso_id = random_int(1000000, 9000000)
        nast_id = random_int(1000000, 9000000)
        enabled = True
        v1_default = True
        create_user = self.admin_client.create_user(
            id=uid,
            key=key,
            enabled=enabled,
            mosso_id=mosso_id,
            nast_id=nast_id)
        self.assertEqual(create_user.status_code, 201,
                         msg='Create user exp. response 201 received {0}'
                         .format(create_user.status_code))
        get_url_id = self.admin_client.list_base_urls_enabled(
            service_name=self.service_name)
        add_base_url = self.admin_client.add_user_base_url(
            id='133',
            v1_default=v1_default,
            user_id=uid)
        self.assertIn(add_base_url.status_code, normal_response_codes,
                      msg='Add base URLs expected {0} received {1}'.format(
                          normal_response_codes,
                          add_base_url.status_code))

        remove_base_url = self.admin_client.delete_user_base_url(
            base_url_id='133',
            user_id=uid)
        self.assertEqual(remove_base_url.status_code, 204,
                         msg='{0}{1}'.format(
                             'Remove user exp. response 201 received ',
                             remove_base_url.status_code))

        get_user = self.admin_client_vsec.get_user_by_name(name=uid)
        delete_user = self.admin_client.delete_user(user_id=uid)
        self.assertEqual(delete_user.status_code, 204,
                         msg='Delete user exp. response 201 received {0}'
                         .format(delete_user.status_code))
        self.addCleanup(self.service_client.delete_user_hard,
                        user_id=get_user.entity.id)

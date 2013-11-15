from testrepo.common.testfixtures.identity.v2_0.identity \
    import IdentityAdminFixture
from ccengine.common.decorators import attr


class AdminExtensionsTest(IdentityAdminFixture):
    @classmethod
    def setUpClass(cls):
        super(AdminExtensionsTest, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        pass

    @attr('smoke', type='positive')
    def test_admin_get_extension(self):
        normal_response_codes = [200, 203]
        get_extensions = self.admin_client.list_extensions()
        self.assertIn(
            get_extensions.status_code, normal_response_codes,
            msg='Get Extensions expected {0} received {1}'.format(
                normal_response_codes, get_extensions.status_code))

    @attr('smoke', type='positive')
    def test_get_extension_by_alias(self):
        normal_response_codes = [200, 203]
        get_extensions = self.admin_client.list_extensions()
        self.assertIn(
            get_extensions.status_code, normal_response_codes,
            msg='Get Extensions expected {0} received {1}'.format(
                normal_response_codes, get_extensions.status_code))
        get_extensions_alias = self.admin_client.get_extension_by_alias(
            alias=get_extensions.entity[0].alias)
        self.assertIn(
            get_extensions_alias.status_code, normal_response_codes,
            msg='Get Extensions alias expected {0} received {1}'.format(
                normal_response_codes, get_extensions_alias.status_code))

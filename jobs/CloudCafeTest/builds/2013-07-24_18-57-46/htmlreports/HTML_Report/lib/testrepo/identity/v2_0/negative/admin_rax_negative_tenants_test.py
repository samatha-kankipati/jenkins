from testrepo.common.testfixtures.identity.v2_0.identity \
    import IdentityAdminFixture
from ccengine.common.decorators import attr


class AdminNegativeTenantsTest(IdentityAdminFixture):

    @classmethod
    def setUpClass(cls):
        super(AdminNegativeTenantsTest, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        pass

    @attr('regression', type='negative')
    def test_get_tenants(self):
        '''TODO: add negative tenants tests'''
        pass

    @attr('regression', type='negative')
    def test_get_tenants_by_name(self):
        '''TODO: add negative tenants tests'''
        pass

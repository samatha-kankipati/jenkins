from testrepo.common.testfixtures.identity.v2_0.identity \
    import UserAdminFixture
from ccengine.common.decorators import attr


class TenantsTest(UserAdminFixture):

    @classmethod
    def setUpClass(cls):
        super(TenantsTest, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        pass

    @attr('regression', type='negative')
    def test_get_tenants(self):
        '''TODO: add negative tenant tests'''
        pass

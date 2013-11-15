from ccengine.common.tools.datagen import rand_name
from testrepo.common.testfixtures.identity.v2_0.identity \
    import IdentityAdminFixture
from ccengine.common.decorators import attr


class AdminNegativeRolesTest(IdentityAdminFixture):

    @classmethod
    def setUpClass(cls):
        super(AdminNegativeRolesTest, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        pass

    @attr('regression', type='negative')
    def test_list_identity_admin_roles_with_user_admin_token(self):
        '''TODO: add negative roles tests'''
        pass

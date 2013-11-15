from ccengine.common.tools.datagen import rand_name
from testrepo.common.testfixtures.identity.v2_0.identity \
    import IdentityAdminFixture
from ccengine.common.decorators import attr


class AdminGroupsTest(IdentityAdminFixture):

    @classmethod
    def setUpClass(cls):
        super(AdminGroupsTest, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        pass

    @attr('regression', type='positive')
    def test_get_groups(self):
        '''TODO:>>> add admin groups tests'''
        pass

    @attr('regression', type='positive')
    def test_get_group_details(self):
        '''TODO:>>> add admin groups tests'''
        pass

    @attr('regression', type='positive')
    def test_add_group(self):
        '''TODO:>>> add admin groups tests'''
        pass

    @attr('regression', type='positive')
    def test_delete_group(self):
        '''TODO:>>> add admin groups tests'''
        pass

    @attr('regression', type='positive')
    def test_update_group(self):
        '''TODO:>>> add admin groups tests'''
        pass

    @attr('regression', type='positive')
    def test_list_groups_for_user(self):
        '''TODO:>>> add admin groups tests'''
        pass

    @attr('regression', type='positive')
    def test_add_user_to_group(self):
        '''TODO:>>> add admin groups tests'''
        pass

    @attr('regression', type='positive')
    def test_get_user_for_group(self):
        '''TODO:>>> add admin groups tests'''
        pass

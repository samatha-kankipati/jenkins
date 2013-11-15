from testrepo.common.testfixtures.identity.v2_0.identity \
    import IdentityAdminFixture
from ccengine.common.decorators import attr
from datetime import datetime, timedelta
from time import strptime, struct_time, mktime


class AdminNegativeTokenTest(IdentityAdminFixture):

    @classmethod
    def setUpClass(cls):
        super(AdminNegativeTokenTest, cls).setUpClass()
        cls.datetime = datetime
        cls.default_token_length = 32

    @classmethod
    def tearDownClass(cls):
        pass

    @attr('regression', type='negative')
    def test_validate_token(self):
        '''TODO: add negative token tests'''
        pass

    @attr('regression', type='negative')
    def test_validate_token_user_part(self):
        '''TODO: add negative token tests'''
        pass

    @attr('regression', type='negative')
    def test_check_token(self):
        '''TODO: add negative token tests'''
        pass

    @attr('regression', type='negative')
    def test_list_endpoints_for_token(self):
        '''TODO: add negative token tests'''
        pass


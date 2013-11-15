from ccengine.common.decorators import attr
from ccengine.common.constants.compute_constants import VncConsoleTypes
from ccengine.common.exceptions.compute import Forbidden
from testrepo.common.testfixtures.compute import RbacComputeFixture


class LimitsTest(RbacComputeFixture):

    @classmethod
    def setUpClass(cls):
        super(LimitsTest, cls).setUpClass()
    
    @attr(type='positive', net='no')
    def test_get_limits_admin_user(self):
        """Verify the response code and contents are correct for Admin"""
        self._test_get_limits(role_for_limits='admin')
    
    @attr(type='positive', net='no')
    def test_create_limits_creator_user(self):
        """Verify the response code and contents are correct for Creator"""
        self._test_get_limits(role_for_limits='creator')
    
    @attr(type='positive', net='no')
    def test_create_limits_observer_user(self):
        """Verify the response code and contents are correct for Observer"""
        self._test_get_limits(role_for_limits='observer')
        
    def _test_get_limits(self, role_for_limits):
        if role_for_limits.lower() == 'admin':
            limits_resp = self.limits_client.get_limits()
        if role_for_limits.lower() == 'creator':
            limits_resp = self.creator_limits_client.get_limits()
        elif role_for_limits.lower() == 'observer':
            limits_resp = self.observer_limits_client.get_limits()
        self.assertEqual(limits_resp.status_code, 200)
        return limits_resp

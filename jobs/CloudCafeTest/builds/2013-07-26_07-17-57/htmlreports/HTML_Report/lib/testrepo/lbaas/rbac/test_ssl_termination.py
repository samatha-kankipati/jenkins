from testrepo.common.testfixtures.load_balancers \
    import LoadBalancersRBACFixture
from ccengine.common.decorators import attr
from ccengine.common.constants.lbaas import SSLConstants


class TestSslTerminationRBAC(LoadBalancersRBACFixture):

    @attr('rbac')
    def test_rbac_get_ssl_termination(self):
        '''View ssl termination with observer and creator roles.'''
        secure_port = 443
        enabled = True
        secure_traffic_only = False
        self.user_admin.update_ssl_termination(
            self.rbac_lb.id, securePort=secure_port, enabled=enabled,
            secureTrafficOnly=secure_traffic_only,
            privatekey=SSLConstants.privatekey,
            certificate=SSLConstants.certificate)
        observer_resp = self.observer.get_ssl_termination(self.rbac_lb.id)
        self.assertEquals(observer_resp.status_code, 200, 'Observer should '
                          'be allowed to view ssl termination.')
        creator_resp = self.creator.get_ssl_termination(self.rbac_lb.id)
        self.assertEquals(creator_resp.status_code, 200, 'Creator should '
                          'be allowed to view ssl termination.')

    @attr('rbac')
    def test_rbac_update_ssl_termination(self):
        '''Update ssl termination with observer and creator roles.'''
        secure_port = 443
        enabled = True
        secure_traffic_only = False
        observer_resp = self.observer.update_ssl_termination(
            self.rbac_lb.id, securePort=secure_port, enabled=enabled,
            secureTrafficOnly=secure_traffic_only,
            privatekey=SSLConstants.privatekey,
            certificate=SSLConstants.certificate)
        self.assertEquals(observer_resp.status_code, 405, 'Observer should '
                          'not be allowed to update ssl termination.')
        creator_resp = self.creator.update_ssl_termination(
            self.rbac_lb.id, securePort=secure_port, enabled=enabled,
            secureTrafficOnly=secure_traffic_only,
            privatekey=SSLConstants.privatekey,
            certificate=SSLConstants.certificate)
        self.assertEquals(creator_resp.status_code, 202, 'Creator should '
                          'be allowed to update ssl termination.')

    @attr('rbac')
    def test_rbac_delete_ssl_termination(self):
        '''Delete ssl termination with observer and creator roles.'''
        secure_port = 443
        enabled = True
        secure_traffic_only = False
        self.user_admin.update_ssl_termination(
            self.rbac_lb.id, securePort=secure_port, enabled=enabled,
            secureTrafficOnly=secure_traffic_only,
            privatekey=SSLConstants.privatekey,
            certificate=SSLConstants.certificate)
        observer_resp = self.observer.delete_ssl_termination(
            self.rbac_lb.id)
        self.assertEquals(observer_resp.status_code, 405, 'Observer should '
                          'not be allowed to update ssl termination.')
        creator_resp = self.creator.delete_ssl_termination(
            self.rbac_lb.id)
        self.assertEquals(creator_resp.status_code, 405, 'Creator should '
                          'not be allowed to update ssl termination.')

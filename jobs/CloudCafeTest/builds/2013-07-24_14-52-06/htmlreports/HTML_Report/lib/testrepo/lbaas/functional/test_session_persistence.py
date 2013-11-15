from testrepo.common.testfixtures.load_balancers \
    import LoadBalancersSmokeFixture, LoadBalancersZeusFixture
from ccengine.common.decorators import attr
from ccengine.domain.types import LoadBalancerStatusTypes as LBStatus


class SessionPersistenceTests(LoadBalancersSmokeFixture):

    _SP_TYPES = ['HTTP_COOKIE', 'SOURCE_IP']

    @attr('smoke', 'positive')
    def test_functional_session_persistence(self):
        """Testing session persistence CRUD operations"""
        persistenceType = self._SP_TYPES[0]
        r = self.client.update_session_persistence(self.lb.id, persistenceType)
        self.assertEquals(r.status_code, 202)
        self.lbaas_provider.wait_for_status(self.lb.id)
        r = self.client.get_session_persistence(self.lb.id)
        created_sp = r.entity
        self.assertEquals(r.status_code, 200)
        self.assertEquals(persistenceType, created_sp.persistenceType)
        r = self.client.delete_session_persistence(self.lb.id)
        self.assertEquals(r.status_code, 202)
        self.lbaas_provider.wait_for_status(self.lb.id)
        r = self.client.get_session_persistence(self.lb.id)
        self.assertEquals(r.status_code, 200)
        self.assertIsNone(r.entity.persistenceType)

    @attr('smoke', 'positive')
    def test_update_lb_after_cookie_session_persistence(self):
        """Testing cookie based session persistence load balancer."""
        persistenceType = self._SP_TYPES[0]
        r = self.client.update_session_persistence(self.lb.id, persistenceType)
        self.assertEquals(r.status_code, 202)
        self.lbaas_provider.wait_for_status(self.lb.id)
        r = self.client.get_session_persistence(self.lb.id)
        created_sp = r.entity
        self.assertEquals(r.status_code, 200)
        self.assertEquals(persistenceType, created_sp.persistenceType)
        protocol = 'FTP'
        r = self.client.update_load_balancer(self.lb.id, protocol=protocol)
        self.assertEquals(r.status_code, 202)
        self.lbaas_provider.wait_for_status(self.lb.id)
        r = self.client.get_session_persistence(self.lb.id)
        self.assertEquals(r.status_code, 200)
        self.assertIsNone(r.entity.persistenceType)


class SessionPersistenceTests(LoadBalancersZeusFixture):

    _SP_TYPES = ['HTTP_COOKIE', 'SOURCE_IP']

    @classmethod
    def setUpClass(cls):
        super(SessionPersistenceTests, cls).setUpClass()
        cls.lb = cls.lbaas_provider.create_active_load_balancer().entity
        cls.lbs_to_delete.append(cls.lb.id)

    @attr('positive')
    def test_non_http_load_balancer_ip_session_persistence(self):
        """Verify IP based session persistence on a non HTTP load balancer"""
        lb = self.lbaas_provider.\
            create_active_load_balancer(protocol='FTP').entity
        pt = self._SP_TYPES[1]
        r = self.client.update_session_persistence(lb.id,
                                                   persistenceType=pt)
        self.assertEquals(r.status_code, 202)
        self.lbaas_provider.wait_for_status(lb.id)
        r = self.client.get_session_persistence(lb.id)
        created_sp = r.entity
        self.assertEquals(r.status_code, 200)
        self.assertEquals(pt, created_sp.persistenceType)
        r = self.client.delete_session_persistence(lb.id)
        self.assertEquals(r.status_code, 202)
        self.lbaas_provider.wait_for_status(lb.id)
        r = self.client.get_session_persistence(lb.id)
        self.assertEquals(r.status_code, 200)
        self.assertIsNone(r.entity.persistenceType)

    @attr('positive')
    def test_delete_session_persistence_status(self):
        '''Verify after session persistence is deleted LB is PENDING_UPDATE'''
        persistenceType = self._SP_TYPES[0]
        r = self.client.update_session_persistence(self.lb.id, persistenceType)
        self.assertEquals(r.status_code, 202)
        r = self.client.get_load_balancer(self.lb.id)
        self.assertEquals(r.entity.status, LBStatus.PENDING_UPDATE)

import time
from testrepo.common.testfixtures.load_balancers \
    import LoadBalancersSmokeFixture, LoadBalancersZeusFixture
from ccengine.common.decorators import attr
from ccengine.domain.types import LoadBalancerStatusTypes as LBStatus


class ErrorPageSmokeTests(LoadBalancersSmokeFixture):

    _ERROR_PAGE_CONTENT = '<html><body>ERROR PAGE</body></html>'

    def setUp(self):
        super(ErrorPageSmokeTests, self).setUp()
        self.client.delete_error_page(self.lb.id)
        self.lbaas_provider.wait_for_status(self.lb.id)

    @attr('smoke', 'positive')
    def test_functional_error_page(self):
        """Testing error page update, delete, and get operations"""
        content = self._ERROR_PAGE_CONTENT
        r = self.client.update_error_page(self.lb.id, content=content)
        self.assertEquals(r.status_code, 202)
        self.lbaas_provider.wait_for_status(self.lb.id)
        r = self.client.get_error_page(self.lb.id)
        created_ep = r.entity
        self.assertEquals(r.status_code, 200)
        self.assertEquals(content, created_ep.content)
        content = '<html><body>DIFFERENT ERROR PAGE</body></html>'
        r = self.client.update_error_page(self.lb.id, content=content)
        self.assertEquals(r.status_code, 202)
        self.lbaas_provider.wait_for_status(self.lb.id)
        r = self.client.get_error_page(self.lb.id)
        updated_ep = r.entity
        self.assertEquals(r.status_code, 200)
        self.assertEquals(content, updated_ep.content)
        r = self.client.delete_error_page(self.lb.id)
        self.assertEquals(r.status_code, 202)
        self.lbaas_provider.wait_for_status(self.lb.id)
        r = self.client.get_error_page(self.lb.id)
        self.assertEquals(r.status_code, 200)
        self.assertNotEqual(updated_ep.content, r.entity.content)

    @attr('smoke', 'positive')
    def test_toggle_error_page_from_custom(self):
        """Toggling between custom and default error page"""
        r = self.client.get_error_page(self.lb.id)
        default_ep = r.entity
        self.assertEquals(r.status_code, 200)
        content = self._ERROR_PAGE_CONTENT
        r = self.client.update_error_page(self.lb.id, content=content)
        self.assertEquals(r.status_code, 202)
        self.lbaas_provider.wait_for_status(self.lb.id)
        r = self.client.get_error_page(self.lb.id)
        created_ep = r.entity
        self.assertEquals(r.status_code, 200)
        self.assertEquals(content, created_ep.content)
        r = self.client.delete_error_page(self.lb.id)
        self.assertEquals(r.status_code, 202)
        self.lbaas_provider.wait_for_status(self.lb.id)
        r = self.client.get_error_page(self.lb.id)
        deleted_ep = r.entity
        self.assertEquals(r.status_code, 200)
        self.assertNotEqual(created_ep.content, deleted_ep.content)
        self.assertEquals(default_ep.content, deleted_ep.content)


class ErrorPageTests(LoadBalancersZeusFixture):

    _ERROR_PAGE_CONTENT = '<html><body>ERROR PAGE</body></html>'
    _DEFAULT_ERROR_PAGE_NAME = 'Default'

    @classmethod
    def setUpClass(cls):
        super(ErrorPageTests, cls).setUpClass()
        cls.lb = cls.lbaas_provider.create_active_load_balancer().entity
        cls.lbs_to_delete.append(cls.lb.id)
        cls.zeus_vs_name = '{0}_{1}'.format(cls.tenant_id, cls.lb.id)

    def setUp(self):
        super(ErrorPageTests, self).setUp()
        self.lbaas_provider.wait_for_status(self.lb.id)
        self.client.delete_error_page(self.lb.id)
        self.lbaas_provider.wait_for_status(self.lb.id)

    @attr('positive', 'test')
    def test_custom_error_page_sync_persistence(self):
        """Verify a custom error page persists after sync."""
        self.lbaas_provider.wait_for_status(self.lb.id)
        content = '<html><body>SYNC ERROR PAGE TEST</body></html>'
        r = self.client.update_error_page(self.lb.id, content=content)
        self.assertEquals(r.status_code, 202)
        self.lbaas_provider.wait_for_status(self.lb.id)
        ep = self.client.get_error_page(self.lb.id).entity
        self.assertEquals(ep.content, content)
        r = self.mgmt_client.sync_load_balancer(self.lb.id)
        self.assertEquals(r.status_code, 202)
        self.lbaas_provider.wait_for_status(self.lb.id)
        r = self.client.get_error_page(self.lb.id)
        self.assertEquals(r.status_code, 200)
        ep = r.entity
        self.assertEquals(ep.content, content)

    @attr('positive', 'test')
    def test_custom_error_page_verify_zeus(self):
        """Verify EP gets set correctly in Zeus.  EXPECTED FAILURE when run with multiple EP tests."""
        r = self.client.get_error_page(self.lb.id)
        self.assertIsNotNone(r.entity.content)
        default_content = r.entity.content
        content = '<html><body>DIFFERENT ERROR PAGE</body></html>'
        r = self.client.update_error_page(self.lb.id, content=content)
        self.assertEquals(r.status_code, 202)
        r = self.client.get_load_balancer(self.lb.id)
        self.assertEquals(r.entity.status, LBStatus.PENDING_UPDATE)
        self.lbaas_provider.wait_for_status(self.lb.id)
        r = self.client.get_error_page(self.lb.id)
        self.assertEquals(r.entity.content, content)
        time.sleep(self.config.lbaas_api.zeus_replication_time)
        zeus_resp = self.zeus_vs.getErrorFile([self.zeus_vs_name])
        error_file_name = '{0}_error.html'.format(self.zeus_vs_name)
        self.assertEquals(zeus_resp[1][0], error_file_name)
        r = self.client.delete_error_page(self.lb.id)
        self.assertEquals(r.status_code, 202)
        r = self.client.get_load_balancer(self.lb.id)
        self.assertEquals(r.entity.status, LBStatus.PENDING_UPDATE)
        self.lbaas_provider.wait_for_status(self.lb.id)
        r = self.client.get_error_page(self.lb.id)
        self.assertEquals(r.entity.content, default_content)
        zeus_resp = self.zeus_vs.getErrorFile([self.zeus_vs_name])
        self.assertEquals(zeus_resp[1][0],
                          ErrorPageTests._DEFAULT_ERROR_PAGE_NAME)

    @attr('positive')
    def test_add_delete_add_error_page(self):
        """Add EP, Delete EP, Add EP."""
        ep_lb = self.lbaas_provider.create_active_load_balancer().entity
        self.lbs_to_delete.append(ep_lb.id)
        ep_lb_zeus_vs_name = '{0}_{1}'.format(self.tenant_id, ep_lb.id)
        error_file_name = '{0}_error.html'.format(ep_lb_zeus_vs_name)
        content = '<html><body>ADD DELETE ADD ERROR PAGE</body></html>'
        r = self.client.update_error_page(ep_lb.id, content=content)
        self.assertEquals(r.status_code, 202)
        self.lbaas_provider.wait_for_status(ep_lb.id)
        r = self.client.delete_error_page(ep_lb.id)
        self.assertEquals(r.status_code, 202)
        self.lbaas_provider.wait_for_status(ep_lb.id)
        zeus_resp = self.zeus_vs.getErrorFile([ep_lb_zeus_vs_name])
        self.assertEquals(zeus_resp[1][0],
                          ErrorPageTests._DEFAULT_ERROR_PAGE_NAME)
        r = self.client.update_error_page(ep_lb.id, content=content)
        self.assertEquals(r.status_code, 202)
        self.lbaas_provider.wait_for_status(ep_lb.id)
        zeus_resp = self.zeus_vs.getErrorFile([ep_lb_zeus_vs_name])
        self.assertEquals(zeus_resp[1][0], error_file_name, 'Zeus error page '
                          'filename does not match what was sent to API.')

    @attr('positive')
    def test_add_sync_delete_add_error_page(self):
        """Add EP, sync LB, delete EP, add EP. EXPECTED FAILURE!!!"""
        ep_lb = self.lbaas_provider.create_active_load_balancer(
            name='add_sync_delete_add_ep').entity
        self.lbs_to_delete.append(ep_lb.id)
        ep_lb_zeus_vs_name = '{0}_{1}'.format(self.tenant_id, ep_lb.id)
        error_file_name = '{0}_error.html'.format(ep_lb_zeus_vs_name)
        content = '<html><body>ADD SYNC DELETE ADD ERROR PAGE</body></html>'
        r = self.client.update_error_page(ep_lb.id, content=content)
        self.assertEquals(r.status_code, 202)
        self.lbaas_provider.wait_for_status(ep_lb.id)
        self.mgmt_client.sync_load_balancer(ep_lb.id)
        self.lbaas_provider.wait_for_status(ep_lb.id)
        r = self.client.delete_error_page(ep_lb.id)
        self.assertEquals(r.status_code, 202)
        self.lbaas_provider.wait_for_status(ep_lb.id)
        zeus_resp = self.zeus_vs.getErrorFile([ep_lb_zeus_vs_name])
        self.assertEquals(zeus_resp[1][0],
                          ErrorPageTests._DEFAULT_ERROR_PAGE_NAME)
        r = self.client.update_error_page(ep_lb.id, content=content)
        self.assertEquals(r.status_code, 202)
        self.lbaas_provider.wait_for_status(ep_lb.id)
        time.sleep(self.config.lbaas_api.zeus_replication_time)
        zeus_resp = self.zeus_vs.getErrorFile([ep_lb_zeus_vs_name])
        self.assertEquals(zeus_resp[1][0], error_file_name, 'Zeus error page '
                          'filename does not match what was sent to API.')

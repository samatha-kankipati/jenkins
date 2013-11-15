from testrepo.common.testfixtures.load_balancers \
    import LoadBalancersSmokeFixture, LoadBalancersZeusFixture
from ccengine.domain.types import LoadBalancerStatusTypes as LBStatus
from ccengine.common.decorators import attr


class ListsSmokeTests(LoadBalancersSmokeFixture):

    @attr('smoke', 'positive')
    def test_list_load_balancers(self):
        '''Verify list of load balancers returns properly.'''
        r = self.client.list_load_balancers()
        lb_list = r.entity
        self.assertEqual(r.status_code, 200)
        matches = [lb for lb in lb_list if self.lb.id == lb.id]
        self.assertEquals(len(matches), 1)

    @attr('smoke', 'positive')
    def test_list_protocols(self):
        '''Verify list of protocols returns properly.'''
        r = self.client.list_protocols()
        self.assertEqual(r.status_code, 200)

    @attr('smoke', 'positive')
    def test_list_algorithms(self):
        '''Verify list of algorithms returns properly.'''
        r = self.client.list_algorithms()
        self.assertEqual(r.status_code, 200)

    @attr('smoke', 'positive')
    def test_list_absolute_limits(self):
        '''Verify list of absolute limits exists.'''
        r = self.client.list_absolute_limits()
        self.assertEqual(r.status_code, 200)

    @attr('smoke', 'positive')
    def test_list_rate_limits(self):
        '''Verify list of rate limits exists.'''
        r = self.client.list_rate_limits()
        self.assertEqual(r.status_code, 200)

    @attr('smoke', 'positive')
    def test_allowed_domains_list(self):
        '''Verify list of allowed domains exists.'''
        r = self.client.list_allowed_domains()
        self.assertEquals(r.status_code, 200)


class ListsTests(LoadBalancersZeusFixture):

    @classmethod
    def setUpClass(cls):
        super(ListsTests, cls).setUpClass()
        cls.lb = cls.lbaas_provider.create_active_load_balancer().entity
        cls.lbs_to_delete.append(cls.lb.id)

    @attr('positive')
    def test_list_load_balancers_extra_lb(self):
        '''Verify list of load balancers returns properly.'''
        r = self.client.list_load_balancers()
        lb_list = r.entity
        self.assertEqual(r.status_code, 200)
        matches = [lb for lb in lb_list if self.lb.id == lb.id]
        self.assertEquals(len(matches), 1)
        new_lb = self.lbaas_provider.create_active_load_balancer().entity
        self.lbs_to_delete.append(new_lb.id)
        r = self.client.list_load_balancers()
        lb_list = r.entity
        self.assertEqual(r.status_code, 200)
        matches = [lb for lb in lb_list
                   if self.lb.id == lb.id or new_lb.id == lb.id]
        self.assertEquals(len(matches), 2)

    @attr('positive')
    def test_protocols_in_list(self):
        '''Verify protocols in protocol list.'''
        r = self.client.list_protocols()
        prot_list = r.entity
        self.assertTrue(prot_list.contains('DNS_TCP', 53))
        self.assertTrue(prot_list.contains('DNS_UDP', 53))
        self.assertTrue(prot_list.contains('TCP_CLIENT_FIRST', 0))
        self.assertTrue(prot_list.contains('UDP', 0))
        self.assertTrue(prot_list.contains('UDP_STREAM', 0))
        self.assertTrue(prot_list.contains('MYSQL', 3306))
        self.assertTrue(prot_list.contains('SFTP', 22))
        self.assertTrue(prot_list.contains('FTP', 21))
        self.assertTrue(prot_list.contains('HTTP', 80))
        self.assertTrue(prot_list.contains('HTTPS', 443))
        self.assertTrue(prot_list.contains('IMAPS', 993))
        self.assertTrue(prot_list.contains('IMAPv2', 143))
        self.assertTrue(prot_list.contains('IMAPv3', 220))
        self.assertTrue(prot_list.contains('IMAPv4', 143))
        self.assertTrue(prot_list.contains('LDAP', 389))
        self.assertTrue(prot_list.contains('LDAPS', 636))
        self.assertTrue(prot_list.contains('POP3', 110))
        self.assertTrue(prot_list.contains('POP3S', 995))
        self.assertTrue(prot_list.contains('SMTP', 25))

    @attr('positive')
    def test_list_load_balancers_by_node_address(self):
        '''List load balancers by node address'''
        new_lb = self.lbaas_provider.create_active_load_balancer().entity
        self.lbs_to_delete.append(new_lb.id)
        node1_addr = self.lb.nodes[0].address
        node2_addr = new_lb.nodes[1].address
        r = self.client.list_load_balancers(nodeaddress=node1_addr)
        self.assertEquals(r.status_code, 200)
        self.assertIsNotNone(r.entity.get_by_id(self.lb.id))
        r = self.client.list_load_balancers(nodeaddress=node2_addr)
        self.assertEquals(r.status_code, 200)
        self.assertIsNotNone(r.entity.get_by_id(new_lb.id))
        self.client.delete_load_balancer(new_lb.id)
        r = self.client.list_load_balancers(nodeaddress=node2_addr)
        self.assertEquals(r.status_code, 200)
        new_lb_by_node = r.entity.get_by_id(new_lb.id)
        self.assertIsNone(new_lb_by_node)
        self.lbaas_provider.wait_for_status(new_lb.id, LBStatus.DELETED)
        r = self.client.list_load_balancers(nodeaddress=node2_addr)
        self.assertEquals(r.status_code, 200)
        new_lb_by_node = r.entity.get_by_id(new_lb.id)
        self.assertIsNone(new_lb_by_node)

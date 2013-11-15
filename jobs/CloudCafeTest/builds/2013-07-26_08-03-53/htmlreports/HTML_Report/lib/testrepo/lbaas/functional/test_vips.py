from testrepo.common.testfixtures.load_balancers \
    import LoadBalancersSmokeFixture, LoadBalancersZeusFixture
from ccengine.common.decorators import attr
from ccengine.domain.types import LoadBalancerVirtualIpTypes as LBVipTypes, \
    LoadBalancerVirtualIpVersions as LBVipVersions, \
    LoadBalancerStatusTypes as LBStatus


class VIPSmokeTests(LoadBalancersSmokeFixture):

    @attr('smoke', 'positive')
    def test_add_remove_vip(self):
        """Add and remove a VIP - Only IPV6"""
        #API does not allow adding IPV6 Servicenet Virtual IP
        if self.lb.virtualIps[0].type == LBVipTypes.SERVICENET:
            return
        r = self.client.list_virtual_ips(self.lb.id)
        vip_list = r.entity
        self.assertEquals(r.status_code, 200)
        self.assertEquals(vip_list[0].type, self.lb.virtualIps[0].type)
        self.assertEquals(vip_list[0].ipVersion,
                          self.lb.virtualIps[0].ipVersion)
        vip1_type = self.lb.virtualIps[0].type
        vip1_ipVersion = LBVipVersions.IPV6
        r = self.client.add_virtual_ip(self.lb.id, vip1_type, vip1_ipVersion)
        ret_vip = r.entity
        self.assertEquals(r.status_code, 202)
        self.assertEquals(vip1_type, ret_vip.type)
        self.assertEquals(vip1_ipVersion, ret_vip.ipVersion)
        self.lbaas_provider.wait_for_status(self.lb.id)
        r = self.client.list_virtual_ips(self.lb.id)
        vip_list = r.entity
        self.assertEquals(r.status_code, 200)
        self.assertEquals(len(vip_list), 3)
        r = self.client.delete_virtual_ip(self.lb.id, ret_vip.id)
        self.assertEqual(r.status_code, 202)
        self.lbaas_provider.wait_for_status(self.lb.id)
        r = self.client.list_virtual_ips(self.lb.id)
        vip_list = r.entity
        self.assertEquals(r.status_code, 200)
        self.assertEquals(len(vip_list), 2)


class VIPTests(LoadBalancersZeusFixture):

    @classmethod
    def setUpClass(cls):
        super(VIPTests, cls).setUpClass()
        cls.lb = cls.lbaas_provider.create_active_load_balancer().entity
        cls.lbs_to_delete.append(cls.lb.id)

    @attr('positive')
    def test_add_remove_vip(self):
        """Add and remove a VIP - Only IPV6"""
        self.lb = self.lbaas_provider.create_active_load_balancer().entity
        self.lbs_to_delete.append(self.lb.id)
        #API does not allow adding IPV6 Servicenet Virtual IP
        if self.lb.virtualIps[0].type == LBVipTypes.SERVICENET:
            return
        r = self.client.list_virtual_ips(self.lb.id)
        vip_list = r.entity
        self.assertEquals(r.status_code, 200)
        self.assertEquals(vip_list[0].type, self.lb.virtualIps[0].type)
        self.assertEquals(vip_list[0].ipVersion,
                          self.lb.virtualIps[0].ipVersion)
        vip1_type = self.lb.virtualIps[0].type
        vip1_ipVersion = LBVipVersions.IPV6
        r = self.client.add_virtual_ip(self.lb.id, vip1_type, vip1_ipVersion)
        ret_vip = r.entity
        self.assertEquals(r.status_code, 202)
        self.assertEquals(vip1_type, ret_vip.type)
        self.assertEquals(vip1_ipVersion, ret_vip.ipVersion)
        self.lbaas_provider.wait_for_status(self.lb.id)
        r = self.client.list_virtual_ips(self.lb.id)
        vip_list = r.entity
        self.assertEquals(r.status_code, 200)
        self.assertEquals(len(vip_list), 3)
        r = self.client.delete_virtual_ip(self.lb.id, ret_vip.id)
        self.assertEqual(r.status_code, 202)
        self.lbaas_provider.wait_for_status(self.lb.id)
        r = self.client.list_virtual_ips(self.lb.id)
        vip_list = r.entity
        self.assertEquals(r.status_code, 200)
        self.assertEquals(len(vip_list), 2)

    @attr('positive')
    def test_shared_vip_different_protocols(self):
        """Share vip between 2 lbs with different protocols on the same port"""
        virtualIps = [{'type': 'SERVICENET'}]
        nodes = [{'address': '100.1.1.1', 'condition': 'ENABLED', 'port': 80}]
        lb1 = self.client.create_load_balancer(name='cc_share_vips_port',
                                               virtualIps=virtualIps,
                                               nodes=nodes,
                                               protocol='TCP',
                                               port=66).entity
        self.lbs_to_delete.append(lb1.id)
        lb1 = self.lbaas_provider.wait_for_status(lb1.id).entity
        vip_id = lb1.virtualIps.get_ipv4_vips()[0].id
        virtualIps = [{'id': vip_id}]
        nodes = [{'address': '100.1.1.1', 'condition': 'ENABLED', 'port': 80}]
        r = self.client.create_load_balancer(name='cc_share_vips_port2',
                                             virtualIps=virtualIps,
                                             nodes=nodes,
                                             protocol='UDP',
                                             port=66)
        self.assertEqual(r.status_code, 202)
        lb2 = r.entity
        self.lbs_to_delete.append(lb2.id)
        lb2 = self.lbaas_provider.wait_for_status(lb2.id).entity
        self.assertEquals(lb2.status, LBStatus.ACTIVE)

    @attr('positive')
    def test_share_vip_on_inactive_cluster(self):
        '''Share a vip even if the cluster is inactive'''
        r = self.mgmt_client.get_clusters()
        self.assertEquals(r.status_code, 200)
        #TODO: Figure out a way to get the cluster set to inactive.
        pass

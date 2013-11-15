from testrepo.common.testfixtures.load_balancers\
    import BaseLoadBalancersFixture
from ccengine.common.decorators import attr
from ccengine.domain.lbaas.mgmt.virtual_ip_block import VirtualIpBlock, \
    VirtualIpBlockList
from ccengine.domain.types import LoadBalancerStatusTypes as LBStatus
from ccengine.domain.lbaas.mgmt.ticket import Ticket


class VirtualIpTests(BaseLoadBalancersFixture):

    @classmethod
    def setUpClass(cls):
        super(VirtualIpTests, cls).setUpClass()

    @attr('positive')
    def test_get_virtual_ips(self):
        '''Test get calls for management vips.'''
        r = self.mgmt_client.get_region_vips()
        self.assertEquals(r.status_code, 200)
        self.assertTrue(len(r.entity) > 0)
        r = self.mgmt_client.get_clusters()
        self.assertEquals(r.status_code, 200)
        cluster_id = r.entity[0].id
        r = self.mgmt_client.get_vips_on_cluster(cluster_id)
        self.assertEquals(r.status_code, 200)
        self.assertTrue(len(r.entity) > 0)
        vip_id = r.entity[0].id
        r = self.mgmt_client.get_load_balancers_with_vip(vip_id)
        self.assertEquals(r.status_code, 200)
        # lb_id = r.entity[0].id
        # r = self.mgmt_client.get_vips_on_loadbalancer(lb_id)
        # self.assertEquals(r.status_code, 200)
        # self.assertTrue(len(r.entity) > 0)

    @attr('positive')
    def test_add_vip_blocks_delete_vip(self):
        '''Test adding vip blocks and deleting a vip from a cluster'''
        self.lb = self.lbaas_provider.create_active_load_balancer().entity
        self.lbs_to_delete.append(self.lb.id)
        vip = self.lb.virtualIps.get_ipv4_vips()[0]
        r = self.client.delete_load_balancer(self.lb.id)
        self.assertEquals(r.status_code, 202)
        self.lbaas_provider.wait_for_status(self.lb.id, LBStatus.DELETED)
        r = self.mgmt_client.delete_virtual_ip(vip.id)
        self.assertEquals(r.status_code, 200)
        r = self.mgmt_client.get_clusters()
        self.assertEquals(r.status_code, 200)
        cluster_id = r.entity[0].id
        r = self.mgmt_client.add_vip_block(cluster_id, type=vip.type,
                                           firstIp=vip.address,
                                           lastIp=vip.address)
        self.assertEquals(r.status_code, 200)

    @attr('positive')
    def test_add_vip_to_load_balancer(self):
        '''Test adding a vip to a load balancer'''
        lb = self.lbaas_provider.create_active_load_balancer().entity
        vip_type = lb.virtualIps[0].type
        lb_id = lb.id
        r = self.mgmt_client.add_virtual_ip(lb_id, vip_type, Ticket(
            comment="Test ticket for adding a vip.", ticketId=12345)
            ._auto_to_dict().get(Ticket.ROOT_TAG))
        self.assertEquals(r.status_code, 202)
        self.assertEquals(r.entity.type, vip_type)
        self.assertTrue(r.entity.address is not None)

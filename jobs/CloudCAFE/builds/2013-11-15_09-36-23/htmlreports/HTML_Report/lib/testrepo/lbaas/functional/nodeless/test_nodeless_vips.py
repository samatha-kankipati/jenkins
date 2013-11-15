import requests

from ccengine.common.decorators import attr
from ccengine.domain.types import LoadBalancerVirtualIpTypes as LBVipTypes, \
    LoadBalancerVirtualIpVersions as LBVipVersions, \
    LoadBalancerStatusTypes as LBStatus
import testrepo.lbaas.functional.test_vips as LBVips


class NodelessVIPTests(LBVips.VIPTests):
    @attr('nodeless')
    def test_add_remove_vip_nodeless(self):
        """Add and remove a VIP - Only IPV6"""
        self.lb = self.lbaas_provider.create_active_load_balancer(
            nodeless=True).entity
        self.lbs_to_delete.append(self.lb.id)

        # API does not allow adding IPV6 Servicenet Virtual IP
        if self.lb.virtualIps[0].type == LBVipTypes.SERVICENET:
            return

        vip_response = self.client.list_virtual_ips(self.lb.id)
        vip_list = vip_response.entity

        self.assertEqual(vip_response.status_code, requests.codes.ok)
        self.assertEqual(vip_list[0].type, self.lb.virtualIps[0].type)
        self.assertEqual(vip_list[0].ipVersion,
                         self.lb.virtualIps[0].ipVersion)

        vip1_type = self.lb.virtualIps[0].type
        vip_response = self.client.add_virtual_ip(
            self.lb.id, vip1_type, LBVipVersions.IPV6)

        ret_vip = vip_response.entity
        self.assertEqual(vip_response.status_code, requests.codes.accepted)
        self.assertEqual(vip1_type, ret_vip.type)
        self.assertEqual(LBVipVersions.IPV6, ret_vip.ipVersion)

        self.lbaas_provider.wait_for_status(self.lb.id)
        vip_response = self.client.list_virtual_ips(self.lb.id)
        self.assertEqual(vip_response.status_code, requests.codes.ok)
        self.assertEqual(len(vip_response.entity), 3)

        vip_response = self.client.delete_virtual_ip(self.lb.id, ret_vip.id)
        self.assertEqual(vip_response.status_code, requests.codes.accepted)
        self.lbaas_provider.wait_for_status(self.lb.id)

        vip_response = self.client.list_virtual_ips(self.lb.id)
        self.assertEqual(vip_response.status_code, requests.codes.ok)
        self.assertEqual(len(vip_response.entity), 2)

    @attr('nodeless')
    def test_shared_vip_different_protocols_nodeless(self):
        """Share vip between 2 lbs with different protocols on the same port"""

        lb_1_args = dict(virtualIps=[{'type': 'SERVICENET'}],
                         name='cc_share_vips_port', protocol='TCP', port=66,
                         nodes=[dict(address='100.1.1.1',
                                     condition='ENABLED',
                                     port=80)])

        lb_2_args = dict(virtualIps=[{'type': 'SERVICENET'}],
                         name='cc_share_vips_port2', protocol='UDP', port=66,
                         nodes=[])

        lb_1 = self.client.create_load_balancer(**lb_1_args).entity
        self.lbs_to_delete.append(lb_1.id)
        lb_1 = self.lbaas_provider.wait_for_status(lb_1.id).entity

        vip_id = lb_1.virtualIps.get_ipv4_vips()[0].id
        lb_2_args['virtualIps'] = [{'id': vip_id}]
        response = self.client.create_load_balancer(**lb_2_args)
        self.assertEqual(response.status_code, requests.codes.accepted)
        self.lbs_to_delete.append(response.entity.id)

        lb2 = self.lbaas_provider.wait_for_status(response.entity.id).entity
        self.assertEqual(lb2.status, LBStatus.ACTIVE)

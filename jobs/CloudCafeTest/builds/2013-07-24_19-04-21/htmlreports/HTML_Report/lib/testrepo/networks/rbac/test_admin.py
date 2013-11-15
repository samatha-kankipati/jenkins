'''
@summary: Test Module for Networks Role Based Access Control
@copyright: Copyright (c) 2013 Rackspace US, Inc.
@author: leon0944
'''
import aiclib
from ccengine.common.constants.networks_constants import HTTPResponseCodes
from ccengine.common.decorators import attr
from ccengine.common.tools import datagen
from testrepo.common.testfixtures.networks import NetworksRBACFixture


class TestAdminRBAC(NetworksRBACFixture):
    """Testing Networks Admin RBAC"""

    @attr('rbac', 'positive')
    def test_create_ipv4_network(self):
        """Testing IPv4 network create with RBAC Admin role"""
        # Creating test data and asserting IP version
        network_name = datagen.rand_name('test_admin_net_create')
        prefix = '172.*.*.0'
        suffix = '24'
        cidr = datagen.random_cidr(ip_pattern=prefix, mask=suffix)
        self.admin_helper.assert_ip_version(ips=cidr, version=4)

        # Networks create call and response assertions
        resp = self.admin_networks_provider.client.create_network(cidr=cidr,
            label=network_name)
        self.assertEqual(resp.status_code, HTTPResponseCodes.CREATE_NETWORK,
                         self.create_msg.format('admin', resp.status_code,
                                                resp.reason, resp.content))
        network = resp.entity
        self.admin_networks_to_delete.append(network.id)
        self.assertEqual(network.label, network_name, self.uname_msg.format(
            network.label, network_name))
        self.assertEqual(network.cidr, cidr, self.ucidr_msg.format(
            network.cidr, cidr))

        # Check the switch in NVP is created for the Network
        if self.run_nvp:
            try:
                nvp_switch = self.admin_nvp_provider.aic_client.get_lswitch(
                    network.id)
            except aiclib.nvp.ResourceNotFound:
                self.fail(self.nvp_msg.format(network.id))
            self.assertEqual(nvp_switch['display_name'], network.label,
                             self.unvp_msg.format(nvp_switch['display_name'],
                                                  network.label))

    @attr('rbac', 'positive')
    def test_create_ipv6_network(self):
        """Testing IPv6 network create with RBAC Admin role"""
        # Creating test data and asserting IP version
        network_name = datagen.rand_name('test_admin_create_ipv6_net')
        cidr = '2001:7f8::/29'
        self.admin_helper.assert_ip_version(ips=cidr, version=6)
        resp = self.admin_networks_provider.client.create_network(cidr=cidr,
            label=network_name)
        self.assertEqual(resp.status_code, HTTPResponseCodes.CREATE_NETWORK,
            self.create_msg.format('admin IPv6', resp.status_code, resp.reason,
                             resp.content))
        self.admin_networks_to_delete.append(resp.entity.id)
        network = resp.entity

        self.assertEqual(network.label, network_name, self.uname_msg.format(
            network.label, network_name))
        self.assertEqual(network.cidr, cidr, self.ucidr_msg.format(
            network.cidr, cidr))

        # Check the switch in NVP is created for the Network
        if self.run_nvp:
            try:
                nvp_switch = self.admin_nvp_provider.aic_client.get_lswitch(
                    network.id)
            except aiclib.nvp.ResourceNotFound:
                self.fail(self.nvp_msg.format(network.id))
            self.assertEqual(nvp_switch['display_name'], network.label,
                             self.unvp_msg.format(nvp_switch['display_name'],
                                                  network.label))

    @attr('rbac', 'positive')
    def test_list_networks(self):
        """Testing network list with RBAC Admin role"""
        # Networks list call and response assertions
        network = self.admin_network
        network2 = self.admin_ipv6_network
        resp = self.admin_networks_provider.client.list_networks()
        network_list = resp.entity
        self.assertEqual(resp.status_code, HTTPResponseCodes.LIST_NETWORKS,
                         self.list_msg.format(resp.status_code, resp.reason,
                                     resp.content))
        self.assertIn(network, network_list, self.ulist_msg.format(
            network.id, ''))

        self.assertIn(network2, network_list, self.ulist_msg.format(
            network2.id, ''))

        # TODO - add checks for creator networks once bug 778 is fixed

    @attr('rbac', 'positive')
    def test_show_admin_ipv4_network(self):
        """Testing IPv4 admin network show with RBAC Admin role"""
        # Networks get call and response assertions
        network = self.admin_network
        resp = self.admin_networks_provider.client.get_network(network.id)
        network_get = resp.entity
        self.assertEqual(resp.status_code, HTTPResponseCodes.GET_NETWORK,
                         self.get_msg.format(resp.status_code, resp.reason,
                                             resp.content))
        self.assertEqual(network_get.label, network.label,
            self.uname_msg.format(network_get.label, network.label))
        self.assertEqual(network_get.cidr, network.cidr, self.ucidr_msg.format(
            network_get.cidr, network.cidr))

    @attr('rbac', 'positive')
    def test_show_admin_ipv6_network(self):
        """Testing IPv6 admin network show with RBAC Admin role"""
        # Networks get call and response assertions
        network = self.admin_ipv6_network
        resp = self.admin_networks_provider.client.get_network(network.id)
        network_get = resp.entity
        self.assertEqual(resp.status_code, HTTPResponseCodes.GET_NETWORK,
                         self.get_msg.format(resp.status_code, resp.reason,
                                             resp.content))
        self.assertEqual(network_get.label, network.label,
            self.uname_msg.format(network_get.label, network.label))
        self.assertEqual(network_get.cidr, network.cidr, self.ucidr_msg.format(
            network_get.cidr, network.cidr))

    # TODO: show ipv4 and ipv6 creator networks (need bug fix 778)

    @attr('rbac', 'positive')
    def test_delete_admin_ipv4_network(self):
        """Testing IPv4 admin network delete with RBAC Admin role"""
        # Creating test data
        network_name = datagen.rand_name('test_admin_net_delete')
        prefix = '172.*.*.0'
        suffix = '24'
        cidr = datagen.random_cidr(ip_pattern=prefix, mask=suffix)
        self.admin_helper.assert_ip_version(ips=cidr, version=4)

        # Networks create call and response assertions
        resp = self.admin_networks_provider.client.create_network(cidr=cidr,
            label=network_name)
        self.assertEqual(resp.status_code, HTTPResponseCodes.CREATE_NETWORK,
                         self.create_msg.format('admin IPv4', resp.status_code,
                                                 resp.reason, resp.content))
        network = resp.entity

        # Check the switch in NVP is created for the Network
        if self.run_nvp:
            try:
                nvp_switch = self.admin_nvp_provider.aic_client.get_lswitch(
                    network.id)
            except aiclib.nvp.ResourceNotFound:
                self.fail(self.nvp_msg.format(network.id))
            self.assertEqual(nvp_switch['display_name'], network.label,
                             self.unvp_msg.format(nvp_switch['display_name'],
                                                  network.label))

        # Networks delete call and response assertions
        resp = self.admin_networks_provider.client.delete_network(network.id)
        self.assertEqual(resp.status_code, HTTPResponseCodes.DELETE_NETWORK,
                         self.delete_msg.format(network.id, resp.status_code,
                         resp.reason, resp.content))

        # Double check network delete
        resp = self.admin_networks_provider.client.list_networks()
        network_list = resp.entity
        self.assertEqual(resp.status_code, HTTPResponseCodes.LIST_NETWORKS,
                         self.list_msg.format(resp.status_code, resp.reason,
                                              resp.content))
        self.assertNotIn(network, network_list, self.ulist_msg.format(
            network.id, 'NOT'))
        resp = self.admin_networks_provider.client.get_network(network.id)
        self.assertEqual(resp.status_code, HTTPResponseCodes.NOT_FOUND,
                         self.udelete_msg.format(resp.status_code,
                                                resp.reason, resp.content))

        # Check the switch in NVP is deleted for the Network
        if self.run_nvp:
            try:
                nvp_switch = self.admin_nvp_provider.aic_client.get_lswitch(
                    network.id)
                self.fail(self.nvpf_msg.format(network.id))
            except aiclib.nvp.ResourceNotFound:
                pass

    @attr('rbac', 'positive')
    def test_delete_admin_ipv6_network(self):
        """Testing IPv6 admin network delete with RBAC Admin role"""
        # Creating test data and asserting IP version
        network_name = datagen.rand_name('test_admin_create_ipv6_net')
        cidr = '2000:7f8::/29'
        self.admin_helper.assert_ip_version(ips=cidr, version=6)
        resp = self.admin_networks_provider.client.create_network(cidr=cidr,
            label=network_name)
        self.assertEqual(resp.status_code, HTTPResponseCodes.CREATE_NETWORK,
            self.create_msg.format('admin IPv6', resp.status_code, resp.reason,
                             resp.content))
        self.admin_networks_to_delete.append(resp.entity.id)
        network = resp.entity

        # Check the switch in NVP is created for the Network
        if self.run_nvp:
            try:
                nvp_switch = self.admin_nvp_provider.aic_client.get_lswitch(
                    network.id)
            except aiclib.nvp.ResourceNotFound:
                self.fail(self.nvp_msg.format(network.id))
            self.assertEqual(nvp_switch['display_name'], network.label,
                             self.unvp_msg.format(nvp_switch['display_name'],
                                                  network.label))

        # Networks delete call and response assertions
        resp = self.admin_networks_provider.client.delete_network(network.id)
        self.assertEqual(resp.status_code, HTTPResponseCodes.DELETE_NETWORK,
                         self.delete_msg.format(network.id, resp.status_code,
                                                resp.reason, resp.content))

        # Double check network delete
        resp = self.admin_networks_provider.client.list_networks()
        network_list = resp.entity
        self.assertEqual(resp.status_code, HTTPResponseCodes.LIST_NETWORKS,
                         self.list_msg.format(resp.status_code, resp.reason,
                                         resp.content))
        self.assertNotIn(network, network_list, self.ulist_msg.format(
            network.id, 'NOT'))
        resp = self.admin_networks_provider.client.get_network(network.id)
        self.assertEqual(resp.status_code, HTTPResponseCodes.NOT_FOUND,
                         self.udelete_msg.format(resp.status_code, resp.reason,
                                                 resp.content))

        # Check the switch in NVP is deleted for the Network
        if self.run_nvp:
            try:
                nvp_switch = self.admin_nvp_provider.aic_client.get_lswitch(
                    network.id)
                self.fail(self.nvpf.format(network.id))
            except aiclib.nvp.ResourceNotFound:
                pass

    # TODO: delete ipv4 and ipv6 creator networks (need bug fix 778)

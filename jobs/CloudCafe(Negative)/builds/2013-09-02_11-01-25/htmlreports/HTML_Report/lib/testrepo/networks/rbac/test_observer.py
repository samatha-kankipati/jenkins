'''
@summary: Test Module for Networks Role Based Access Control
@copyright: Copyright (c) 2013 Rackspace US, Inc.
@author: leon0944
'''
import unittest2
import aiclib
from ccengine.common.constants.networks_constants import HTTPResponseCodes
from ccengine.common.decorators import attr
from ccengine.common.tools import datagen
from testrepo.common.testfixtures.networks import NetworksRBACFixture


class TestObserverRBAC(NetworksRBACFixture):
    """Testing Networks Observer RBAC"""

    @attr('rbac', 'negative')
    def test_create_ipv4_network_w_observer(self):
        """Testing IPv4 network create is forbidden with RBAC Observer"""
        # Creating test data and asserting IP version
        network_name = datagen.rand_name('test_observer_create')
        prefix = '172.*.*.0'
        suffix = '24'
        cidr = datagen.random_cidr(ip_pattern=prefix, mask=suffix)
        self.observer_helper.assert_ip_version(ips=cidr, version=4)

        # Networks create call forbidden with observer and response assertions
        resp = self.observer_networks_provider.client.create_network(cidr=cidr,
            label=network_name)
        self.assertEqual(resp.status_code, self.unallowed_status,
                         self.ucreate_msg.format('observer', resp.status_code,
                                                resp.reason, resp.content))

    @attr('rbac', 'negative')
    def test_create_ipv6_network_w_observer(self):
        """Testing IPv6 network create is forbidden with RBAC Observer"""
        # Creating test data and asserting IP version
        network_name = datagen.rand_name('test_observer_create_ipv6_net')
        cidr = '2001:7f8::/29'
        self.observer_helper.assert_ip_version(ips=cidr, version=6)
        resp = self.observer_networks_provider.client.create_network(cidr=cidr,
            label=network_name)
        self.assertEqual(resp.status_code, self.unallowed_status,
            self.ucreate_msg.format('observer IPv6', resp.status_code,
                                    resp.reason, resp.content))

    @attr('rbac', 'positive')
    def test_list_networks_w_observer(self):
        """Testing network list with RBAC Observer role"""
        # Networks list call and response assertions
        network = self.admin_network
        network2 = self.admin_ipv6_network
        resp = self.observer_networks_provider.client.list_networks()
        network_list = resp.entity
        self.assertEqual(resp.status_code, HTTPResponseCodes.LIST_NETWORKS,
                         self.list_msg.format(resp.status_code, resp.reason,
                                              resp.content))
        self.assertIn(network, network_list, self.ulist_msg.format(
            network.id, ''))

        self.assertIn(network2, network_list, self.ulist_msg.format(
            network2.id, ''))

        # TODO - add checks for creator networks once bug 778 is fixed

    @unittest2.skip('Skip - fails due to bug 860')
    @attr('rbac', 'positive')
    def test_show_admin_ipv4_network_w_observer(self):
        """Testing IPv4 admin network show with RBAC Observer role"""
        # Networks get call and response assertions
        network = self.admin_network
        resp = self.observer_networks_provider.client.get_network(network.id)
        network_get = resp.entity
        self.assertEqual(resp.status_code, HTTPResponseCodes.GET_NETWORK,
                         self.get_msg.format(resp.status_code, resp.reason,
                                             resp.content))
        self.assertEqual(network_get.label, network.label,
            self.uname_msg.format(network_get.label, network.label))
        self.assertEqual(network_get.cidr, network.cidr, self.ucidr_msg.format(
            network_get.cidr, network.cidr))

    @unittest2.skip('Skip - fails due to bug 860')
    @attr('rbac', 'positive')
    def test_show_admin_ipv6_network_w_observer(self):
        """Testing IPv6 admin network show with RBAC Observer role"""
        # Networks get call and response assertions
        network = self.admin_ipv6_network
        resp = self.observer_networks_provider.client.get_network(network.id)
        network_get = resp.entity
        self.assertEqual(resp.status_code, HTTPResponseCodes.GET_NETWORK,
                         self.get_msg.format(resp.status_code, resp.reason,
                                             resp.content))
        self.assertEqual(network_get.label, network.label,
            self.uname_msg.format(network_get.label, network.label))
        self.assertEqual(network_get.cidr, network.cidr, self.ucidr_msg.format(
            network_get.cidr, network.cidr))

    # TODO: show ipv4 and ipv6 creator networks (need bug fix 778)

    @attr('rbac', 'negative')
    def test_delete_admin_ipv4_network_w_observer(self):
        """Testing IPv4 admin network delete is forbidden with Observer"""
        # Creating test data
        network_name = datagen.rand_name('test_observer_net_delete')
        prefix = '172.*.*.0'
        suffix = '24'
        cidr = datagen.random_cidr(ip_pattern=prefix, mask=suffix)
        self.creator_helper.assert_ip_version(ips=cidr, version=4)

        # Networks create call and response assertions
        resp = self.admin_networks_provider.client.create_network(cidr=cidr,
            label=network_name)
        self.assertEqual(resp.status_code, HTTPResponseCodes.CREATE_NETWORK,
                         self.create_msg.format('admin IPv4', resp.status_code,
                                                 resp.reason, resp.content))
        network = resp.entity
        self.admin_networks_to_delete.append(network.id)

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

        # Networks delete call forbidden with observer and response assertions
        resp = self.observer_networks_provider.client.delete_network(
            network.id)
        self.assertEqual(resp.status_code, self.unallowed_status,
                         self.uadelete_msg.format(network.id, resp.status_code,
                                                  resp.reason, resp.content))

        # Double check the network was not deleted
        resp = self.admin_networks_provider.client.list_networks()
        network_list = resp.entity
        self.assertEqual(resp.status_code, HTTPResponseCodes.LIST_NETWORKS,
                         self.list_msg.format(resp.status_code, resp.reason,
                                              resp.content))
        self.assertIn(network, network_list, self.ulist_msg.format(
            network.id, ''))
        resp = self.admin_networks_provider.client.get_network(network.id)
        self.assertEqual(resp.status_code, HTTPResponseCodes.GET_NETWORK,
                         self.get_msg.format(resp.status_code, resp.reason,
                                             resp.content))

        # Check the switch in NVP is still there
        if self.run_nvp:
            try:
                nvp_switch = self.admin_nvp_provider.aic_client.get_lswitch(
                    network.id)
            except aiclib.nvp.ResourceNotFound:
                self.fail(self.nvp_msg.format(network.id))
            self.assertEqual(nvp_switch['display_name'], network.label,
                             self.unvp_msg.format(nvp_switch['display_name'],
                                                  network.label))

    @attr('rbac', 'negative')
    def test_delete_admin_ipv6_network_w_observer(self):
        """Testing IPv6 admin network delete is forbidden with Observer"""
        # Creating test data and asserting IP version
        network_name = datagen.rand_name('test_observer_delete_ipv6_net')
        cidr = '2000:7f8::/29'
        self.admin_helper.assert_ip_version(ips=cidr, version=6)
        resp = self.admin_networks_provider.client.create_network(cidr=cidr,
            label=network_name)
        self.assertEqual(resp.status_code, HTTPResponseCodes.CREATE_NETWORK,
            self.create_msg.format('admin IPv6', resp.status_code, resp.reason,
                                   resp.content))
        network = resp.entity
        self.admin_networks_to_delete.append(resp.entity.id)

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

        # Networks delete call forbidden with observer and response assertions
        resp = self.observer_networks_provider.client.delete_network(
            network.id)
        self.assertEqual(resp.status_code, self.unallowed_status,
                         self.uadelete_msg.format(network.id, resp.status_code,
                                                  resp.reason, resp.content))

        # Double check the network was not deleted
        resp = self.admin_networks_provider.client.list_networks()
        network_list = resp.entity
        self.assertEqual(resp.status_code, HTTPResponseCodes.LIST_NETWORKS,
                         self.list_msg.format(resp.status_code, resp.reason,
                                              resp.content))
        self.assertIn(network, network_list, self.ulist_msg.format(
            network.id, ''))
        resp = self.admin_networks_provider.client.get_network(network.id)
        self.assertEqual(resp.status_code, HTTPResponseCodes.GET_NETWORK,
                         self.get_msg.format(resp.status_code, resp.reason,
                                             resp.content))

        # Check the switch in NVP is still there
        if self.run_nvp:
            try:
                nvp_switch = self.admin_nvp_provider.aic_client.get_lswitch(
                    network.id)
            except aiclib.nvp.ResourceNotFound:
                self.fail(self.nvp_msg.format(network.id))
            self.assertEqual(nvp_switch['display_name'], network.label,
                             self.unvp_msg.format(nvp_switch['display_name'],
                                                  network.label))

    # TODO: delete ipv4 and ipv6 creator networks (need bug fix 778)

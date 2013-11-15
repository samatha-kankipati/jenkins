from testrepo.common.testfixtures.load_balancers\
    import BaseLoadBalancersFixture
from ccengine.domain.lbaas.mgmt.subnet_mapping import HostSubnetList, \
    HostSubnet, NetInterfaceList, NetInterface, CidrList, Cidr
from ccengine.common.decorators import attr


class SubnetMappingTests(BaseLoadBalancersFixture):

    @classmethod
    def setUpClass(cls):
        super(SubnetMappingTests, cls).setUpClass()

    @attr('positive')
    def test_functional_subnetmapping_operations(self):
        '''Testing host subnet mapping calls'''
        # use subnet 10.1.1.0/24 for deletion/addition
        r = self.mgmt_client.get_hosts()
        self.assertEquals(r.status_code, 200)
        host_id = r.entity[0].id
        r = self.mgmt_client.get_subnet_mappings(host_id)
        self.assertEquals(r.status_code, 200)
        subnets = r.entity
        self.assertTrue(len(subnets) > 0)
        netInterfaces = subnets[0].netInterfaces
        self.assertTrue(len(netInterfaces) > 0)
        cidrs = netInterfaces[0].cidrs
        self.assertTrue(len(cidrs) > 0)
        subnetList = [{'name': netInterfaces[0].name,
                       'cidrs':[{'block': '10.1.1.0/24'}]}]
        r = self.mgmt_client.delete_subnet_mappings(host_id, subnetList)
        self.assertEquals(r.status_code, 200)
        r = self.mgmt_client.add_subnet_mappings(host_id, subnetList)
        self.assertEquals(r.status_code, 200)

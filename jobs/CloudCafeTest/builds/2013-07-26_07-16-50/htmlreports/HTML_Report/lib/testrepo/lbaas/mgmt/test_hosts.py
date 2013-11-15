from testrepo.common.testfixtures.load_balancers\
    import BaseLoadBalancersFixture
from ccengine.common.decorators import attr
from ccengine.domain.lbaas.mgmt.host import Host


class HostTests(BaseLoadBalancersFixture):

    @classmethod
    def setUpClass(cls):
        super(HostTests, cls).setUpClass()

    @attr('positive')
    def test_get_hosts_host(self):
        '''Test get calls for hosts and singular host.'''
        r = self.mgmt_client.get_hosts()
        self.assertEquals(r.status_code, 200)
        self.assertTrue(len(r.entity) > 0)
        host = r.entity[0]
        r = self.mgmt_client.get_host(host.id)
        self.assertEquals(r.status_code, 200)
        self.assertEqual(r.entity.id, host.id)

    @attr('positive')
    def test_create_update_host(self):
        '''Test post and put on host.'''
        r = self.mgmt_client.get_hosts()
        self.assertEquals(r.status_code, 200)
        for host in r.entity:
            if host.name == "DeleteMe" or host.name == "DeleteMe2":
                r2 = self.mgmt_client.delete_host(host.id)
                self.assertEquals(r2.status_code, 202)
        r = self.mgmt_client.get_hosts()
        self.assertEquals(r.status_code, 200)
        name = "DeleteMe"
        clusterId = 1
        coreDeviceId = "SomeCoreDevice"
        zone = "B"
        managementIp = "12.34.56.78"
        managementSoapInterface = "http://SomeSoapNode.com:9090"
        maxConcurrentConnections = 5
        trafficManagerName = "zeus01.blah.blah"
        type = "FAILOVER"
        soapEndpointActive = "true"
        ipv4Servicenet = "10.2.2.80"
        ipv4Public = "172.11.11.110"
        r = self.mgmt_client.add_host(
            name=name, clusterId=clusterId, zone=zone, ipv4Public=ipv4Public,
            managementIp=managementIp, coreDeviceId=coreDeviceId, type=type,
            managementSoapInterface=managementSoapInterface,
            maxConcurrentConnections=maxConcurrentConnections,
            trafficManagerName=trafficManagerName,
            soapEndpointActive=soapEndpointActive,
            ipv4Servicenet=ipv4Servicenet)
        self.assertEquals(r.status_code, 202)
        self.assertTrue(r.entity.id is not None)
        host_id = r.entity.id
        name = "DeleteMe2"
        r = self.mgmt_client.update_host(
            host_id, ipv4Public=ipv4Public, managementIp=managementIp,
            coreDeviceId=coreDeviceId, ipv4Servicenet=ipv4Servicenet,
            managementSoapInterface=managementSoapInterface, name=name,
            maxConcurrentConnections=maxConcurrentConnections,
            trafficManagerName=trafficManagerName,
            soapEndpointActive=soapEndpointActive)
        self.assertEquals(r.status_code, 200)
        r = self.mgmt_client.get_host(host_id)
        self.assertEquals(r.status_code, 200)
        self.assertTrue(r.entity.name == name)
        r = self.mgmt_client.delete_host(host_id)
        self.assertEquals(r.status_code, 202)
        r = self.mgmt_client.get_hosts()
        self.assertEquals(r.status_code, 200)
        self.assertTrue(len(r.entity) == 4)

    @attr('positive')
    def test_active_host_endpoint_calls(self):
        '''Test active SOAP endpoint host calls'''
        r = self.mgmt_client.get_clusters()
        self.assertEquals(r.status_code, 200)
        cluster = r.entity[0]
        r = self.mgmt_client.get_host_endpoint(cluster.id)
        self.assertEquals(r.status_code, 200)
        self.assertEquals(cluster.id, r.entity.clusterId)
        # set a different endpoint
        r = self.mgmt_client.get_hosts()
        self.assertEquals(r.status_code, 200)
        host = r.entity[0]
        if host.soapEndpointActive == "true":
            r2 = self.mgmt_client.update_host_endpoint_disable(host.id)
            self.assertEquals(r2.status_code, 200)
        else:
            r2 = self.mgmt_client.update_host_endpoint_enable(host.id)
            self.assertEquals(r2.status_code, 200)
        r = self.mgmt_client.get_hosts()
        self.assertEquals(r.status_code, 200)
        host = r.entity[0]
        if host.soapEndpointActive == "true":
            r2 = self.mgmt_client.update_host_endpoint_disable(host.id)
            self.assertEquals(r2.status_code, 200)
        r = self.mgmt_client.call_host_endpoint_poller()
        self.assertEquals(r.status_code, 200)
        r = self.mgmt_client.get_host(host.id)
        self.assertEquals(r.status_code, 200)
        self.assertEquals(r.entity.soapEndpointActive, True)

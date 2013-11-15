from requests import codes as resp_codes

from ccengine.common.decorators import attr
from testrepo.common.testfixtures.load_balancers\
    import BaseLoadBalancersFixture


class HostTests(BaseLoadBalancersFixture):

    @attr('positive')
    def test_get_hosts_host(self):
        """Test get calls for hosts and singular host."""

        status_err = "{msg} - Expected: {expected}  Actual: {actual}"

        # Get list of nodes
        host_response = self.mgmt_client.get_hosts()
        actual_response = host_response.status_code
        expected_response = resp_codes.ok
        self.assertEquals(expected_response, actual_response,
                          status_err.format(msg='List of hosts',
                                            actual=actual_response,
                                            expected=expected_response))

        self.assertGreater(len(host_response.entity), 0,
                           'No hosts were returned in list of hosts')
        host = host_response.entity[0]

        # Get node by id
        host_response = self.mgmt_client.get_host(host.id)
        actual_response = host_response.status_code
        expected_response = resp_codes.ok
        self.assertEquals(expected_response, actual_response,
                          status_err.format(msg='Get hosts by id',
                                            actual=actual_response,
                                            expected=expected_response))

        actual_id = host_response.entity.id
        expected_id = host.id
        self.assertEquals(expected_response, actual_response,
                          status_err.format(msg='Host values are different',
                                            actual=actual_id,
                                            expected=expected_id))

    @attr('positive')
    def test_create_update_host(self):
        """Test post and put on host."""

        status_err = "{msg} - Expected: {expected}  Actual: {actual}"
        host_names = ['DeleteMe', 'DeleteMe2']

        # Get list of nodes defined on the device
        host_response = self.mgmt_client.get_hosts()
        actual_response = host_response.status_code
        expected_response = resp_codes.ok
        self.assertEquals(expected_response, actual_response,
                          status_err.format(msg='List of defined nodes',
                                            actual=actual_response,
                                            expected=expected_response))

        # Remove specific nodes if they exist, and store number of nodes
        # defined on the device
        num_hosts = len(host_response.entity)
        for host in host_response.entity:
            if host.name in host_names:
                num_hosts -= 1
                del_response = self.mgmt_client.delete_host(host.id)
                actual_response = del_response.status_code
                expected_response = resp_codes.accepted
                self.assertEquals(actual_response, expected_response,
                                  status_err.format(msg='delete_host',
                                                    expected=expected_response,
                                                    actual=actual_response))

        # Add new node
        add_host_args = {'name': "DeleteMe",
                         'clusterId': 1,
                         'coreDeviceId': "SomeCoreDevice",
                         'zone': "B",
                         'managementIp': "12.34.56.78",
                         'managementSoapInterface':
                             "http://SomeSoapNode.com:9090",
                         'maxConcurrentConnections': 5,
                         'trafficManagerName': "zeus01.blah.blah",
                         'type': "FAILOVER",
                         'soapEndpointActive': "true",
                         'ipv4Servicenet': "10.2.2.80",
                         'ipv4Public': "172.11.11.110"}

        add_response = self.mgmt_client.add_host(**add_host_args)
        actual_response = add_response.status_code
        expected_response = resp_codes.accepted
        self.assertEquals(expected_response, actual_response,
                          status_err.format(msg='add_host',
                                            actual=actual_response,
                                            expected=expected_response))
        self.assertIsNotNone(add_response.entity.id,
                             'Add response id was None')
        host_id = add_response.entity.id

        # Update argument list for updating host
        add_host_args['name'] = "DeleteMe2"
        remove_args = ['zone', 'type', 'clusterId']
        for arg in remove_args:
            del add_host_args[arg]

        # Update node
        update_response = self.mgmt_client.update_host(hostId=host_id,
                                                       **add_host_args)
        actual_response = update_response.status_code
        expected_response = resp_codes.ok
        self.assertEquals(expected_response, actual_response,
                          status_err.format(msg='update_host',
                                            actual=actual_response,
                                            expected=expected_response))

        # Verify node exists
        host_response = self.mgmt_client.get_host(host_id)
        actual_response = host_response.status_code
        expected_response = resp_codes.ok
        self.assertEquals(expected_response, actual_response,
                          status_err.format(msg='get host by ID',
                                            actual=actual_response,
                                            expected=expected_response))

        actual_name = host_response.entity.name
        expected_name = add_host_args['name']
        self.assertEquals(actual_name, expected_name,
                          status_err.format(msg='Host names do not match',
                                            actual=actual_name,
                                            expected=expected_name))

        # Delete node
        delete_response = self.mgmt_client.delete_host(host_id)
        actual_response = delete_response.status_code
        expected_response = resp_codes.accepted
        self.assertEquals(expected_response, actual_response,
                          status_err.format(msg='delete_host',
                                            actual=actual_response,
                                            expected=expected_response))

        # Verify node was deleted
        host_response = self.mgmt_client.get_hosts()
        actual_response = host_response.status_code
        expected_response = resp_codes.ok
        self.assertEquals(expected_response, actual_response,
                          status_err.format(msg='get hosts',
                                            actual=actual_response,
                                            expected=expected_response))

        self.assertEquals(len(host_response.entity), num_hosts,
                          "Expected {0} hosts, found {1}".format(
                              num_hosts, len(host_response.entity)))

    @attr('positive')
    def test_active_host_endpoint_calls(self):
        """Test active SOAP endpoint host calls"""

        VAL_TRUE = 'true'
        status_err = "{msg} - Expected: {expected}  Actual: {actual}"

        # Get the ZEUS cluster servicing the load balancer
        cluster_response = self.mgmt_client.get_clusters()
        actual_response = cluster_response.status_code
        expected_response = resp_codes.ok
        self.assertEquals(actual_response, expected_response,
                          status_err.format(msg='Get Zeus Cluster',
                                            expected=expected_response,
                                            actual=actual_response))
        cluster = cluster_response.entity[0]

        # Get the endpoint for ZEUS
        endpt_response = self.mgmt_client.get_host_endpoint(cluster.id)
        actual_response = endpt_response.status_code
        expected_response = resp_codes.ok
        self.assertEquals(actual_response, expected_response,
                          status_err.format(msg='Get Zeus Endpoint',
                                            expected=expected_response,
                                            actual=actual_response))

        self.assertEquals(cluster.id, endpt_response.entity.clusterId,
                          status_err.format(msg='Validate endpoint IDs',
                                            expected=cluster.id,
                                            actual=endpt_response.entity.
                                                clusterId))

        # Disable/Enable the endpoint
        host_response = self.mgmt_client.get_hosts()
        self.assertEquals(host_response.status_code, resp_codes.ok)
        host = host_response.entity[0]
        if host.soapEndpointActive == VAL_TRUE:
            response = self.mgmt_client.update_host_endpoint_disable(host.id)
            self.assertEquals(response.status_code, resp_codes.ok,
                              "Unable to disable endpoint")
        else:
            response = self.mgmt_client.update_host_endpoint_enable(host.id)
            self.assertEquals(response.status_code, resp_codes.ok,
                              "Unable to enable endpoint")

        # Get host and verify SOAP endpoint is active
        host_response = self.mgmt_client.get_hosts()
        self.assertEquals(host_response.status_code, resp_codes.ok)
        host = host_response.entity[0]
        if host.soapEndpointActive == VAL_TRUE:
            response = self.mgmt_client.update_host_endpoint_disable(host.id)
            self.assertEquals(response.status_code, resp_codes.ok,
                              "Unable to disable endpoint")

        # Verify Poller is still responding
        poller_response = self.mgmt_client.call_host_endpoint_poller()
        actual_response = poller_response.status_code
        expected_response = resp_codes.ok
        self.assertEquals(actual_response, expected_response,
                          status_err.format(msg='Verify poller response',
                                            actual=actual_response,
                                            expected=expected_response))

        host_response = self.mgmt_client.get_host(host.id)
        actual_response = host_response.status_code
        expected_response = resp_codes.ok
        self.assertEquals(actual_response, expected_response,
                          status_err.format(msg='Get host by ID',
                                            actual=actual_response,
                                            expected=expected_response))
        self.assertTrue(host_response.entity.soapEndpointActive,
                        "SoapEndpoint is NOT active")

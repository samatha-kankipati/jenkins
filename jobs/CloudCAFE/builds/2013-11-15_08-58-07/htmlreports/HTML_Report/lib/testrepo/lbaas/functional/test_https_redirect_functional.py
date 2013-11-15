from requests import codes as HttpCodes

from ccengine.common.constants.lbaas import SSLConstants
from ccengine.common.decorators import attr
from ccengine.common.tools.datagen import random_string
from ccengine.domain.types import LoadBalancerStatusTypes as LBStatus, \
    LoadBalancerVirtualIpTypes as LBVipTypes
from testrepo.common.testfixtures.load_balancers \
    import BaseLoadBalancersFixture


class TestHTTPRedirectFunctional(BaseLoadBalancersFixture):
    TRAFFIC_SSL = 'SSL'
    TRAFFIC_STD = 'STD'
    SSL_SECURE_PORT = '443'
    HTTPS = 'HTTPS'
    HTTP = 'HTTP'
    TRAFFIC_SRC = '/medium.iso'
    MEGABYTE = 1024 * 1024

    # Hack due to issues with port forwarding in the Rackspace Internal Network
    ENABLE_TRAFFIC_VALIDATION = True

    # SSL not configured on the backend servers
    # So a successful response is a specific web page error, hence min_bytes
    MIN_BYTES = 450

    traffic_stats = ('\n\nVIP: {vip}\n\t{traf_type} Bytes In: {bytes_in} '
                     'bytes\n\t{traf_type} Bytes Out: {bytes_out} bytes\n\n')

    @attr('functional', 'redirect', 'smoke')
    def test_http_lb_with_traffic_and_https_redirect(self):
        """ Test using a HTTP LB, pass traffic with/without HTTPS Redirect """
        protocol = self.HTTP

        lb_id = self.create_load_balancer(
            protocol=protocol, redirect_enabled=False, use_public_vip=True)
        vip = self.get_vip(lb_id=lb_id)

        for redirect_enabled in [False, True]:

            # Enable/Disable http redirects
            # (enable should fail, disabling should be successful)
            self.configure_http_redirect(lb_id=lb_id, enabled=redirect_enabled,
                                         success=not redirect_enabled)

            self.generate_and_validate_traffic(
                vip=vip, traffic_type=self.TRAFFIC_STD, successful=True)
            self.generate_and_validate_traffic(
                vip=vip, traffic_type=self.TRAFFIC_SSL, successful=False)

        self.delete_load_balancer(lb_id=lb_id)

    @attr('functional', 'redirect')
    def test_https_lb_with_traffic_and_https_redirect(self):
        """ Test using a HTTPS LB, pass traffic with/without HTTPS Redirect """
        protocol = self.HTTPS

        lb_id = self.create_load_balancer(
            protocol=protocol, redirect_enabled=False, use_public_vip=True,
            node_port=self.SSL_SECURE_PORT, port=self.SSL_SECURE_PORT)
        vip = self.get_vip(lb_id=lb_id)

        self.generate_and_validate_traffic(
            vip=vip, traffic_type=self.TRAFFIC_STD, successful=False,
            lb_id=lb_id)
        self.generate_and_validate_traffic(
            vip=vip, traffic_type=self.TRAFFIC_SSL, successful=True,
            lb_id=lb_id)

        for enabled_state in [True, False]:
            self.configure_http_redirect(lb_id=lb_id, enabled=enabled_state,
                                         success=True)

            # Standard traffic should work if the redirect is enabled
            self.generate_and_validate_traffic(
                vip=vip, lb_id=lb_id, traffic_type=self.TRAFFIC_STD,
                successful=enabled_state)

            # SSL traffic should always work
            self.generate_and_validate_traffic(
                vip=vip, traffic_type=self.TRAFFIC_SSL, successful=True,
                lb_id=lb_id)

        self.delete_load_balancer(lb_id=lb_id)

    @attr('functional', 'redirect')
    def test_http_lb_with_ssl_term_and_https_redirect(self):
        """ Test using a HTTP LB with SSL Term traffic with/out HTTPS Redirects
        """
        protocol = self.HTTP

        lb_id = self.create_load_balancer(
            protocol=protocol, redirect_enabled=False, use_public_vip=True)
        vip = self.get_vip(lb_id=lb_id)

        # Enable SSL Termination
        response = self.client.update_ssl_termination(
            lb_id, enabled=True, securePort=self.SSL_SECURE_PORT,
            privatekey=SSLConstants.privatekey, secureTrafficOnly=True,
            certificate=SSLConstants.certificate)

        self.assertEqual(response.status_code, HttpCodes.accepted)
        self.lbaas_provider.wait_for_status(lb_id, LBStatus.ACTIVE)

        for enabled_state in [True, False]:
            self.configure_http_redirect(
                lb_id=lb_id, enabled=enabled_state, success=True)

            self.generate_and_validate_traffic(
                vip=vip, lb_id=lb_id, traffic_type=self.TRAFFIC_STD,
                successful=enabled_state)

            # SSL traffic should always work
            self.generate_and_validate_traffic(
                vip=vip, lb_id=lb_id, traffic_type=self.TRAFFIC_SSL,
                successful=True)

        self.delete_load_balancer(lb_id=lb_id)

    # ------- NON-TEST ROUTINES ---------

    def get_vip(self, lb_id):
        """ Get the VIP defined on the LB """
        vip_list = self.client.list_virtual_ips(load_balancer_id=lb_id).entity
        vip = vip_list[0].address
        return vip

    def generate_and_validate_traffic(
            self, vip, traffic_type, successful=False, lb_id=None):
        """ Generate a specific type of traffic, and validate if the LB
        response to the traffic was correct.

        @param: vip = VIP to make request against
        @param: traffic_type = Type of traffic to generate (STD or SSL)
        @param: successful = Should the traffic be load balanced or rejected
        @param: lb_id = Load balancer ID (for debugging purposes only)

        Return: None
        """

        traffic_routine = 'generate_ssl_bandwidth_out' if \
            traffic_type == self.TRAFFIC_SSL else 'generate_bandwidth_out'

        traf_gen = getattr(self.lbaas_provider, traffic_routine)

        bytes_in, bytes_out, socket_out = traf_gen(
            ip=vip, path=self.TRAFFIC_SRC, output=True)

        self.fixture_log.info(self.traffic_stats.format(
            vip=vip, bytes_in=bytes_in, bytes_out=bytes_out,
            traf_type=traffic_type))

        # Due to an issue in RS internal networks,
        if not self.ENABLE_TRAFFIC_VALIDATION:
            return True

        if successful:
            num_bytes = self.MEGABYTE if traffic_type == self.TRAFFIC_STD \
                else self.MIN_BYTES

            # Didn't get a large response, check for redirect mesg
            msg = '{type_} Traffic was not passed to the LB.\nOutput:\n{out}'
            if bytes_out < num_bytes:
                if ("301 moved permanently" in socket_out.lower() and
                        "location: https" in socket_out.lower()):
                    self.fixture_log.info(
                        "\n\t*** Received redirect as expected. ***\n")
                else:
                    self.assertGreater(
                        bytes_out, num_bytes,
                        msg.format(type_=traffic_type, out=socket_out))

        else:
            num_bytes = self.MEGABYTE if traffic_type == self.TRAFFIC_STD \
                else self.MIN_BYTES

            # DEBUG for network issue
            if lb_id is not None:
                debug_str = ('\n\nTRAFFIC TYPE: {type_}\n'
                             'TRAFFIC ROUTINE: {routine}\n'
                             'BYTES IN: {bytes_in}\n'
                             'BYTES OUT: {bytes_out}\n\n')

                self.fixture_log.debug(debug_str.format(
                    type_=traffic_type, routine=traffic_routine,
                    bytes_in=bytes_in, bytes_out=bytes_out))
                response = self.lbaas_provider.wait_for_status(
                    lb_id, LBStatus.ACTIVE)

                self.fixture_log.debug(
                    "RESPONSE:\n{response}".format(response=response.entity))

            self.assertLess(bytes_out, num_bytes,
                            '{type_} Traffic was passed '
                            'to the LB'.format(type_=traffic_type))

    def create_load_balancer(
            self, protocol='HTTP', node_port='80', redirect_enabled=False,
            use_public_vip=False, **kwargs):
        """
        Create a load balancer for the redirect tests
        @param: protocol - Protocol to load balance
        @param: node_port - The backend server port to forward to
        @param: redirect_enabled - (Boolean) - Enable http redirect?
        @param: use_public_vip - (Boolean) - Use public vip (vs default)

        Return: (str) Load Balancer ID
        """

        name = random_string('cc_lb')
        nodes = [{'address': self.config.lbaas_api.live_node1,
                  'port': str(node_port), 'condition': 'ENABLED'},
                 {'address': self.config.lbaas_api.live_node2,
                  'port': str(node_port), 'condition': 'ENABLED'}]

        virtual_ips = [{'type': LBVipTypes.PUBLIC}] if use_public_vip else \
            [{'type': self.default_vip_type}]

        response = self.client.create_load_balancer(
            name=name, nodes=nodes, protocol=protocol, virtualIps=virtual_ips,
            httpsRedirect=redirect_enabled, **kwargs)
        self.assertEqual(response.status_code, HttpCodes.accepted)

        load_balancer = response.entity

        response = self.lbaas_provider.wait_for_status(
            load_balancer.id, LBStatus.ACTIVE)
        self.assertEqual(response.status_code, HttpCodes.ok)
        if redirect_enabled:
            self.assertTrue(load_balancer.httpsRedirect)

        self.lbs_to_delete.append(load_balancer.id)
        return load_balancer.id

    def configure_http_redirect(self, lb_id, enabled, success):
        """
        Configure the HTTP redirect functionality on the LB and validate
        that Zeus correctly reflects the configuration

        @param: lb_id = Load balancer id
        @param: enabled = Boolean - Enable(T)/Disable(F) redirect

        Return: None
        """
        expected_status_code = HttpCodes.accepted if success else HttpCodes.bad

        # Determine the current state of httpsRedirect
        response = self.lbaas_provider.wait_for_status(lb_id, LBStatus.ACTIVE)
        current_state = response.entity.httpsRedirect

        # Try to update the load balancer
        response = self.client.update_load_balancer(
            lb_id, httpsRedirect=enabled)
        self.assertEqual(response.status_code, expected_status_code)

        # Wait for the LB to become ACTIVE
        response = self.lbaas_provider.wait_for_status(lb_id)
        self.assertEqual(response.status_code, HttpCodes.ok)
        self.assertEqual(response.entity.status, LBStatus.ACTIVE)

        # Determine the expected state of httpsRedirect
        expected_state = not current_state if \
            (success and enabled != current_state) else current_state
        self.assertEqual(response.entity.httpsRedirect, expected_state)

    def delete_load_balancer(self, lb_id):
        """
        Delete Load Balancer, and verify the virtual servers were deleted
        accordingly

        @param: lb_id - Load Balancer ID
        @param: lb_name - Original Load Balancer name
        @param: lb_redirect_name - Name of LB supporting redirect
        @param: lb_ssl_name - Name of SSL load balancer supporting redirect
        @param: ssl_enabled - Boolean indicating if SSL was enabled on LBs

        Return: None
        """

        response = self.client.delete_load_balancer(lb_id)
        self.assertEqual(response.status_code, HttpCodes.accepted)
        response = self.client.get_load_balancer(lb_id)
        self.assertEqual(response.status_code, HttpCodes.ok)
        self.assertEqual(response.entity.status, LBStatus.PENDING_DELETE)

        response = self.lbaas_provider.wait_for_status(lb_id, LBStatus.DELETED)
        self.assertEqual(response.status_code, HttpCodes.ok)
        self.assertEqual(response.entity.status, LBStatus.DELETED)

        response = self.client.list_load_balancers()
        lb_id_list = [l_bal.id for l_bal in response.entity]
        self.assertNotIn(lb_id, lb_id_list,
                         "DELETED Load balancer in load balancers list.")

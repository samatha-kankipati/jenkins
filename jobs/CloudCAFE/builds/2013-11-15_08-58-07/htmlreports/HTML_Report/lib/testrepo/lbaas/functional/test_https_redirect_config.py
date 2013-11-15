from ccengine.common.constants.lbaas import SSLConstants
from ccengine.common.decorators import attr
from ccengine.common.tools import datagen
from ccengine.domain.types import LoadBalancerStatusTypes as LBStatus, \
    LoadBalancerVirtualIpTypes as LBVipTypes
from testrepo.common.testfixtures.load_balancers \
    import LoadBalancersZeusFixture


class TestHTTPSRedirectConfig(LoadBalancersZeusFixture):

    SSL_SECURE_PORT = '443'
    HTTPS = 'HTTPS'
    HTTP = 'HTTP'

    @attr('positive', 'redirect')
    def test_https_lb_with_https_redirect(self):
        """Test CRUD with an HTTPS LB with HTTPS Redirect enabled """
        name = 'https_with_redirect'
        protocol = self.HTTPS
        lb_id, lb_name, lb_redirect_name = self.create_load_balancer(
            name=name, protocol=protocol, redirect_enabled=True,
            node_port=self.SSL_SECURE_PORT)

        response = self.client.list_load_balancers()
        lb_id_list = [l_bal.id for l_bal in response.entity]
        self.assertIn(lb_id, lb_id_list,
                      'NON-DELETED Load balancer not in load balancers list.')

        vs_names = self.zeus_vs.getVirtualServerNames()[1]
        self.assertIn(lb_name, vs_names,
                      "Primary HTTPS Virtual Server does not exist.")
        self.assertIn(lb_redirect_name, vs_names,
                      "Redirection Virtual Server does not exist.")

        new_algorithm = 'RANDOM'
        response = self.client.update_load_balancer(lb_id,
                                                    algorithm=new_algorithm)
        self.assertEqual(response.status_code, 202)

        response = self.client.get_load_balancer(lb_id)
        self.assertEqual(response.entity.status, LBStatus.PENDING_UPDATE)
        self.assertEqual(response.entity.algorithm, new_algorithm)

        response = self.lbaas_provider.wait_for_status(lb_id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.entity.status, LBStatus.ACTIVE)

        self.delete_load_balancer(lb_id=lb_id, lb_name=lb_name,
                                  lb_redirect_name=lb_redirect_name)

    @attr('positive', 'redirect', 'smoke')
    def test_https_lb_add_remove_redirect(self):
        """Test creating a HTTPS LB, add and remove HTTPS Redirect """
        name = 'https_without_redirect'
        protocol = self.HTTPS
        lb_id, lb_name, lb_redirect_name = self.create_load_balancer(
            name=name, protocol=protocol, redirect_enabled=False)

        # Toggle Redirect Functionality
        for enabled in [True, False, True, False]:
            self.configure_http_redirect(
                lb_id=lb_id, enabled=enabled, lb_name=lb_name,
                lb_redirect_name=lb_redirect_name)

        # Delete LB
        self.delete_load_balancer(lb_id=lb_id, lb_name=lb_name,
                                  lb_redirect_name=lb_redirect_name)

    @attr('positive', 'redirect', 'smoke')
    def test_ssl_lb_with_https_redirect(self):
        """Test add HTTPS Redirect to a LB with SSL Termination enabled """
        name = 'ssl_with_redirect'
        protocol = "HTTP"
        lb_id, lb_name, lb_redirect_name, lb_ssl_name = \
            self.create_load_balancer(
                name=name, protocol=protocol, redirect_enabled=False, ssl=True,
                node_port=self.SSL_SECURE_PORT)

        # Add SSL termination
        response = self.client.update_ssl_termination(
            lb_id, securePort=self.SSL_SECURE_PORT, enabled=True,
            privatekey=SSLConstants.privatekey,
            certificate=SSLConstants.certificate,
            secureTrafficOnly=True)

        self.assertEqual(response.status_code, 202)
        self.lbaas_provider.wait_for_status(lb_id)

        response = self.client.get_ssl_termination(lb_id)
        self.assertEqual(response.status_code, 200)

        vs_names = self.zeus_vs.getVirtualServerNames()[1]
        self.assertIn(lb_name, vs_names,
                      "Non-SSL Virtual Server does not exist.")
        self.assertIn(lb_ssl_name, vs_names,
                      "Primary SSL Virtual Server does not exist.")

        # Turn on Redirect
        self.configure_http_redirect(
            lb_id=lb_id, enabled=True, lb_name=lb_name,
            lb_redirect_name=lb_redirect_name, lb_ssl_name=lb_ssl_name)

        # Delete LB
        self.delete_load_balancer(lb_id=lb_id, lb_name=lb_name,
                                  lb_redirect_name=lb_redirect_name,
                                  lb_ssl_name=lb_ssl_name)

    @attr('negative', 'redirect')
    def test_ssl_lb_with_https_redirect_invalid_operations(self):
        """Test invalid ops on a LB w/SSL Term and HTTPS Redirect enabled """
        name = 'ssl_with_redirect'
        protocol = self.HTTP
        lb_id, lb_name, lb_redirect_name, lb_ssl_name = \
            self.create_load_balancer(
                name=name, protocol=protocol, redirect_enabled=False, ssl=True,
                node_port=self.SSL_SECURE_PORT)

        # Add SSL term
        ssl_enabled = True
        ssl_secure_traffic_only = True
        response = self.client.update_ssl_termination(
            lb_id, enabled=ssl_enabled, securePort=self.SSL_SECURE_PORT,
            privatekey=SSLConstants.privatekey,
            certificate=SSLConstants.certificate,
            secureTrafficOnly=ssl_secure_traffic_only)

        self.assertEqual(response.status_code, 202)
        self.lbaas_provider.wait_for_status(lb_id)

        response = self.client.get_ssl_termination(lb_id)
        self.assertEqual(response.status_code, 200)

        vs_names = self.zeus_vs.getVirtualServerNames()[1]
        self.assertIn(lb_name, vs_names,
                      "Non-SSL Virtual Server does not exist.")
        self.assertIn(lb_ssl_name, vs_names,
                      "Primary SSL Virtual Server does not exist.")

        # Turn on Redirect
        self.configure_http_redirect(
            lb_id=lb_id, enabled=True, lb_name=lb_name,
            lb_ssl_name=lb_ssl_name, lb_redirect_name=lb_redirect_name)

        # Attempt to modify functionality that is NOT ALLOWED to change
        response = self.client.update_load_balancer(lb_id, port=500)
        self.assertEqual(response.status_code, 400)

        response = self.client.update_ssl_termination(lb_id,
                                                      secureTrafficOnly=False)
        self.assertEqual(response.status_code, 400)

        response = self.client.update_ssl_termination(lb_id, securePort=550)
        self.assertEqual(response.status_code, 400)

        # Turn off Redirect
        self.configure_http_redirect(
            lb_id=lb_id, enabled=False, lb_name=lb_name,
            lb_redirect_name=lb_redirect_name)

        #Attempt modify functionality this IS ALLOWED to change
        response = self.client.update_ssl_termination(lb_id,
                                                      secureTrafficOnly=False)
        self.assertEqual(response.status_code, 202)

        response = self.lbaas_provider.wait_for_status(lb_id)
        self.assertEqual(response.status_code, 200)

        # Attempt to turn on Redirect
        response = self.client.update_load_balancer(lb_id, httpsRedirect=True)
        self.assertEqual(response.status_code, 400)

        # Attempt to modify additional functionality NOW ALLOWED to change
        response = self.client.update_load_balancer(lb_id, port=500)
        self.assertEqual(response.status_code, 202)
        response = self.lbaas_provider.wait_for_status(lb_id)
        self.assertEqual(response.status_code, 200)
        response = self.client.update_ssl_termination(lb_id, securePort=550)
        self.assertEqual(response.status_code, 202)
        response = self.lbaas_provider.wait_for_status(lb_id)
        self.assertEqual(response.status_code, 200)

        # Delete LB
        self.delete_load_balancer(
            lb_id=lb_id, lb_name=lb_name, lb_redirect_name=lb_redirect_name,
            lb_ssl_name=lb_ssl_name, ssl_enabled=ssl_enabled)

    @attr('negative', 'redirect')
    def test_https_lb_with_https_redirect_invalid_operations(self):
        """Test attempt invalid ops on a SSL LB w/HTTPS Redirect enabled """

        name = 'ssl_with_redirect'
        protocol = self.HTTPS

        lb_id, lb_name, lb_redirect_name = self.create_load_balancer(
            name=name, protocol=protocol, redirect_enabled=True,
            node_port=self.SSL_SECURE_PORT)

        # Attempt to add SSL termination
        ssl_enabled = True
        ssl_secure_traffic_only = True
        response = self.client.update_ssl_termination(
            lb_id, securePort=self.SSL_SECURE_PORT, enabled=ssl_enabled,
            privatekey=SSLConstants.privatekey,
            certificate=SSLConstants.certificate,
            secureTrafficOnly=ssl_secure_traffic_only)
        self.assertEqual(response.status_code, 400)

        # Attempt to modify functionality that is NOT ALLOWED to change
        response = self.client.update_load_balancer(lb_id, port=500)
        self.assertEqual(response.status_code, 400)

        # Delete LB
        self.delete_load_balancer(
            lb_id=lb_id, lb_name=lb_name, lb_redirect_name=lb_redirect_name,
            ssl_enabled=ssl_enabled)

    @attr('redirect', 'smoke')
    def test_non_https_lb_add_https_redirect(self):
        """Verify HTTPS Redirect can be added to HTTPS load balancers only."""
        name = 'http_load_balancer'
        protocol = self.HTTP
        lb_id, lb_name, lb_redirect_name = self.create_load_balancer(
            name=name, protocol=protocol, redirect_enabled=False,
            node_port='80')

        # Attempt to turn on Redirect
        redirect = True
        response = self.client.update_load_balancer(lb_id,
                                                    httpsRedirect=redirect)
        self.assertEqual(response.status_code, 400)

        # Try every protocol except HTTPS (and HTTP, which we already tried)
        protocol_list = [item for item in self.client.list_protocols().entity
                         if item.name not in ('HTTP', 'HTTPS')]

        for protocol in protocol_list:
            lb_port = protocol.port
            if int(protocol.port) == 0:
                lb_port = datagen.random_int(1, 1000)
            response = self.client.update_load_balancer(lb_id, port=lb_port,
                                                        protocol=protocol.name)
            self.assertEqual(response.status_code, 202)
            response = self.lbaas_provider.wait_for_status(lb_id)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.entity.status, LBStatus.ACTIVE)

            # Attempt to turn on Redirect
            response = self.client.update_load_balancer(lb_id,
                                                        httpsRedirect=redirect)
            self.assertEqual(response.status_code, 400)

        # Switch to HTTPS with invalid port for redirect
        protocol = self.HTTPS
        lb_port = '500'
        ssl_enabled = True
        response = self.client.update_load_balancer(lb_id, protocol=protocol,
                                                    port=lb_port)
        self.assertEqual(response.status_code, 202)
        response = self.lbaas_provider.wait_for_status(lb_id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.entity.status, LBStatus.ACTIVE)

        # Attempt to turn on Redirect
        response = self.client.update_load_balancer(lb_id,
                                                    httpsRedirect=redirect)
        self.assertEqual(response.status_code, 400)

        # Switch to valid port for redirect
        lb_port = self.SSL_SECURE_PORT
        response = self.client.update_load_balancer(lb_id, port=lb_port)
        self.assertEqual(response.status_code, 202)
        response = self.lbaas_provider.wait_for_status(lb_id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.entity.status, LBStatus.ACTIVE)

        # Attempt to turn on Redirect
        response = self.client.update_load_balancer(lb_id,
                                                    httpsRedirect=redirect)
        self.assertEqual(response.status_code, 202)
        response = self.lbaas_provider.wait_for_status(lb_id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.entity.status, LBStatus.ACTIVE)

        # Delete LB
        self.delete_load_balancer(lb_id=lb_id, lb_name=lb_name,
                                  lb_redirect_name=lb_redirect_name,
                                  ssl_enabled=ssl_enabled)

    def create_load_balancer(
            self, name, protocol='HTTP', node_port='80', ssl=False,
            redirect_enabled=False, use_public_vip=False):

        """
        Create a load balancer for the redirect tests
        @param: name - Name of the load balancer to create
        @param: protocol - Protocol to load balance
        @param: node_port - The backend server port to forward to
        @param: redirect_enabled - (Boolean) - Enable http redirect?
        @param: ssl - (Boolean) Load balancer will have SSL enabled?
        @param: use_public_vip - (Boolean) - Use public vip (vs default)
        """

        nodes = [{'address': self.config.lbaas_api.live_node1,
                  'port': str(node_port), 'condition': 'ENABLED'},
                 {'address': self.config.lbaas_api.live_node2,
                  'port': str(node_port), 'condition': 'ENABLED'}]

        if use_public_vip:
            virtual_ips = [{'type': LBVipTypes.PUBLIC}]
        else:
            virtual_ips = [{'type': self.default_vip_type}]

        response = self.client.create_load_balancer(
            name=name, nodes=nodes, protocol=protocol, virtualIps=virtual_ips,
            httpsRedirect=redirect_enabled)
        self.assertEqual(response.status_code, 202)

        load_balancer = response.entity
        lb_name = '{0}_{1}'.format(self.tenant_id, load_balancer.id)
        lb_redirect_name = '{0}_{1}_R'.format(self.tenant_id, load_balancer.id)
        lb_ssl_name = '{0}_{1}_S'.format(self.tenant_id, load_balancer.id)

        response = self.lbaas_provider.wait_for_status(
            load_balancer.id, LBStatus.ACTIVE)
        self.assertEqual(response.status_code, 200)
        if redirect_enabled:
            self.assertTrue(load_balancer.httpsRedirect)

        self.lbs_to_delete.append(load_balancer.id)

        ret_vals = [load_balancer.id, lb_name, lb_redirect_name]
        if ssl:
            ret_vals.append(lb_ssl_name)
        return ret_vals

    def configure_http_redirect(self, lb_id, enabled, lb_name,
                                lb_redirect_name, lb_ssl_name=None):
        """
        Configure the HTTP redirect functionality on the LB and validate
        that Zeus correctly reflects the configuration

        @param: lb_id = Load balancer id
        @param: enabled = Boolean - Enable(T)/Disable(F) redirect
        @param: lb_name = Name of load balancer
        @param: lb_redirect_name = Name of load balancer supporting redirects
        @param: lb_ssl_name = Name of load balancer with SSL configured
        """

        response = self.client.update_load_balancer(
            lb_id, httpsRedirect=enabled)
        self.assertEqual(response.status_code, 202)

        response = self.client.get_load_balancer(lb_id)
        self.assertEqual(response.entity.status, LBStatus.PENDING_UPDATE)

        response = self.lbaas_provider.wait_for_status(lb_id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.entity.status, LBStatus.ACTIVE)
        self.assertEqual(response.entity.httpsRedirect, enabled)

        if self.lbaas_provider is None:
            vs_names = self.zeus_vs.getVirtualServerNames()[1]
            if lb_ssl_name is None:
                self.assertIn(lb_name, vs_names,
                              "Primary HTTPS Virtual Server does not exist.")
            else:
                self.assertNotIn(lb_name, vs_names,
                                 "Original non-SSL Virtual Server was not "
                                 "renamed correctly.")

            if enabled:
                if lb_ssl_name is None:
                    self.assertIn(lb_redirect_name, vs_names,
                                  "Redirection Virtual Server does not exist.")
                else:
                    self.assertIn(lb_redirect_name, vs_names,
                                  "Original non-SSL Virtual Server was not "
                                  "renamed correctly.")
                    self.assertIn(lb_ssl_name, vs_names,
                                  "Primary SSL Virtual Server does not exist.")

            else:
                if lb_ssl_name is None:
                    self.assertNotIn(lb_redirect_name, vs_names,
                                     "Redirection Virtual Server "
                                     "still exists.")
                else:
                    self.assertNotIn(lb_ssl_name, vs_names,
                                     "Primary SSL Virtual Server "
                                     "still exists.")

    def delete_load_balancer(self, lb_id, lb_name, lb_redirect_name,
                             lb_ssl_name=None, ssl_enabled=False):
        """
        Delete Load Balancer, and verify the virtual servers were deleted
        accordingly

        @param: lb_id - Load Balancer ID
        @param: lb_name - Original Load Balancer name
        @param: lb_redirect_name - Name of LB supporting redirect
        @param: lb_ssl_name - Name of SSL load balancer supporting redirect
        @param: ssl_enabled - Boolean indicating if SSL was enabled on LBs
        """

        response = self.client.delete_load_balancer(lb_id)
        self.assertEqual(response.status_code, 202)
        response = self.client.get_load_balancer(lb_id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.entity.status, LBStatus.PENDING_DELETE)

        response = self.lbaas_provider.wait_for_status(lb_id, LBStatus.DELETED)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.entity.status, LBStatus.DELETED)

        response = self.client.list_load_balancers()
        lb_id_list = [l_bal.id for l_bal in response.entity]
        self.assertNotIn(lb_id, lb_id_list,
                         "DELETED Load balancer in load balancers list.")

        # Validation for tests defined in this class
        if isinstance(self, LoadBalancersZeusFixture):
            vs_names = self.zeus_vs.getVirtualServerNames()[1]
            if lb_ssl_name is None and not ssl_enabled:
                self.assertNotIn(lb_name, vs_names,
                                 "Primary HTTPS Virtual Server still exists "
                                 "after LB deletion.")
                self.assertNotIn(lb_redirect_name, vs_names,
                                 "Redirection Virtual Server still exists "
                                 "after LB deletion.")
            else:
                self.assertNotIn(lb_name, vs_names,
                                 "Original non-SSL Virtual Server still exists"
                                 " after LB deletion.")
                self.assertNotIn(lb_redirect_name, vs_names,
                                 "HTTPS Redirect Virtual Server still exists "
                                 "after LB deletion.")
                if lb_ssl_name is not None:
                    self.assertNotIn(lb_ssl_name, vs_names,
                                     "Primary SSL Virtual Server still exists "
                                     "after LB deletion.")

            # Remove LB from list of LBs to delete
            self.lbs_to_delete = [id_ for id_ in self.lbs_to_delete
                                  if id_ != lb_id]

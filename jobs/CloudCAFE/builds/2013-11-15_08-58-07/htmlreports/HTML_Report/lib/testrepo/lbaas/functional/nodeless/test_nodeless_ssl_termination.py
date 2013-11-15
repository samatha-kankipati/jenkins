import requests

from ccengine.common.decorators import attr
from ccengine.common.constants.lbaas import SSLConstants
import testrepo.lbaas.functional.test_ssl_termination as TestSSL

try:
    import M2Crypto
except:
    pass

class NodelessSSLTerminationSmokeTests(TestSSL.SSLTerminationSmokeTests):

    @classmethod
    def setUpClass(cls):
        super(NodelessSSLTerminationSmokeTests, cls).setUpClass()
        cls.orig_lb = cls.lb

        # Set up nodeless load balancer for smoke tests
        cls.lb = cls.lbaas_provider.create_active_load_balancer(
            nodeless=True).entity
        cls.lbs_to_delete.append(cls.lb.id)

    @attr('nodeless')
    def test_nodeless_ssl_term_crud(self):
        return self.test_ssl_term_crud()


class NodelessSSLTerminationTests(TestSSL.SSLTerminationTests):

    @classmethod
    def setUpClass(cls):
        """ Setting up class. Create SSL load balancer. """
        super(NodelessSSLTerminationTests, cls).setUpClass()
        cls.orig_ssl_lb = cls.ssl_lb

        node_less_ssl_lb = cls.lbaas_provider.create_active_load_balancer(
            protocol='HTTP', port=80, nodeless=True)
        assert node_less_ssl_lb.status_code == 200, \
                'Received {status}'.format(
                    status=str(node_less_ssl_lb.status_code))

        cls.ssl_lb = node_less_ssl_lb.entity
        cls.lbs_to_delete.append(cls.ssl_lb.id)

        cls.zeus_vs_name = '{tenant!s}_{lb_id!s}_S'.format(
            tenant=cls.tenant_id, lb_id=cls.ssl_lb.id)

    @classmethod
    def tearDown(cls):
        for lb_id in [cls.orig_ssl_lb.id, cls.ssl_lb.id]:
            cls.lbaas_provider.wait_for_status(lb_id)
            cls.client.delete_ssl_termination(lb_id)
            cls.lbaas_provider.wait_for_status(lb_id)

    @attr('nodeless')
    def test_nodeless_ssl_termination_cert_validation(self):
        """ SSL Cert validation - rsaEncryption PEM format """
        return self.test_ssl_termination_cert_validation()

    @attr('nodeless')
    def test_nodeless_ssl_termination_pkcs8_key_format(self):
        """ Nodeless - SSL Cert validation - pkcs8 format """
        return self.test_ssl_termination_pkcs8_key_format()

    @attr('nodeless')
    def test_nodeless_ssl_termination_pkcs1_key_format(self):
        """ Nodeless SSL Cert validation - pkcs1 format"""
        return self.test_ssl_termination_pkcs1_key_format()

    @attr('nodeless')
    def test_add_ssl_termination_to_nodeless_lb_on_ssl_port(self):
        """ Add SSL termination to a nodeless LB on the SSL port """
        std_port = 80
        ssl_port = 443

        lb = self.lbaas_provider.create_active_load_balancer(
            port=std_port, nodeless=True).entity
        self.lbs_to_delete.append(lb.id)

        response = self.client.update_load_balancer(lb.id, port=ssl_port)
        self.assertEqual(response.status_code, requests.codes.accepted)

        response = self.client.get_load_balancer(lb.id)
        self.assertEqual(response.status_code, requests.codes.ok)
        self.assertEqual(int(response.entity.port), int(ssl_port))

        response = self.client.update_ssl_termination(
            lb.id, securePort=ssl_port, certificate=SSLConstants.certificate,
            privatekey=SSLConstants.privatekey)
        self.assertEqual(response.status_code, requests.codes.bad)

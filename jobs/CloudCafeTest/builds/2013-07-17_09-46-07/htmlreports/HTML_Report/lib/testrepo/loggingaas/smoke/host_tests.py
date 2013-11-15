import os
from ccengine.common.tools.datagen import rand_name
from testrepo.common.testfixtures.loggingaas import HostFixture
from ccengine.providers.loggingaas.logging_provider import \
    LoggingProducerProvider, LoggingProfileProvider


class HostTests(HostFixture):

    @classmethod
    def setUpClass(cls):
        super(HostTests, cls).setUpClass()
        cls.tenant_provider.create_tenant()

    def setUp(self):
        super(HostTests, self).setUp()
        self.hosts_created = []

        self.producer_provider = LoggingProducerProvider(self.config)
        self.profile_provider = LoggingProfileProvider(self.config)

        response = self.producer_provider.create_producer(producer_name='boom',
                                                          create_depend=False)
        self.producer_id = self.get_id(response)

        response = self.profile_provider.create_profile(
            producer_ids=[self.producer_id],
            create_depend=False)
        self.profile_id = self.get_id(response)

    def tearDown(self):
        for host_id in self.hosts_created:
            self._delete_host(host_id, False)

        self.hosts_created = []

        self.profile_provider.delete_profile(self.profile_id)
        self.producer_provider.delete_producer(self.producer_id)

    def get_id(self, request):
        """
        Helper function to extract the host id from location header
        """
        assert request.status_code == 201
        location = request.headers.get('location')
        ret_id = int(os.path.split(location)[1])
        return ret_id

    def _delete_host(self, host_id, remove_from_array=True):
        response = self.provider.delete_host(host_id)
        self.assertEqual(200, response.status_code,
                         'Delete response code should have returned 200 OK.')

        if remove_from_array:
            self.hosts_created.remove(host_id)

        return response

    def _create_new_host(self, hostname, ip_v4=None, ip_v6=None,
                         profile_id=None):

        host_req = self.provider.create_host(hostname=hostname,
                                             ip_v4=ip_v4,
                                             ip_v6=ip_v6,
                                             profile_id=profile_id,
                                             create_depend=False)
        self.assertEqual(201, host_req.status_code,
                         'Status code should have been 201 Created. ')

        location = host_req.headers.get('location')
        host_id = int(os.path.split(location)[1])

        bad_loc_msg = ('Headers should have returned a location in the '
                       'headers after creation')
        self.assertIsNotNone(location, bad_loc_msg)
        self.assertGreater(host_id, 0, "Invalid producer ID")

        self.hosts_created.append(host_id)

        return {
            'request': host_req,
            'location': location,
            'host_id': host_id
        }

    def test_create_host(self):
        cfg = self.provider.config.loggingaas
        self._create_new_host(hostname=cfg.hostname,
                              ip_v4=cfg.ip_address_v4,
                              ip_v6=cfg.ip_address_v6,
                              profile_id=self.profile_id)

    def test_get_host(self):
        cfg = self.provider.config.loggingaas
        host_result = self._create_new_host(hostname=cfg.hostname,
                                            ip_v4=cfg.ip_address_v4,
                                            ip_v6=cfg.ip_address_v6,
                                            profile_id=self.profile_id)
        host_id = host_result['host_id']

        host_response = self.provider.get_host(host_id)
        host = host_response.entity

        self.assertEqual(200, host_response.status_code,
                         'Status code should have been 200 OK')
        self.assertIsNotNone(host)
        self.assertEqual('testhost', host.hostname, 'Incorrect hostname')
        self.assertEqual('::1', host.ip_address_v6, 'Incorrect ipv6 address')
        self.assertEqual('127.0.0.1', host.ip_address_v4,
                         'Incorrect ipv4 address')
        self.assertEqual(host_id, host.id, 'Unexpected host id')

    def test_get_all_hosts(self):
        second_host_name = rand_name()

        cfg = self.provider.config.loggingaas
        host1_result = self._create_new_host(hostname=cfg.hostname,
                                             ip_v4=cfg.ip_address_v4,
                                             ip_v6=cfg.ip_address_v6,
                                             profile_id=self.profile_id)
        host2_result = self._create_new_host(hostname=second_host_name,
                                             ip_v4='10.10.1.1',
                                             ip_v6=cfg.ip_address_v6,
                                             profile_id=self.profile_id)

        host1_id = host1_result['host_id']
        host2_id = host2_result['host_id']

        hosts_resp = self.provider.get_all_hosts()

        self.assertEqual(200, hosts_resp.status_code)

        for host in hosts_resp.entity:
            if host.id == host1_id:
                self.assertEqual(cfg.hostname, host.hostname)
                self.assertEqual(cfg.ip_address_v4, host.ip_address_v4)
            elif host.id == host2_id:
                self.assertEqual(second_host_name, host.hostname)
                self.assertEqual('10.10.1.1', host.ip_address_v4)
            else:
                self.fail("Unexpected host id:{}".format(host.id))

    def test_update_host(self):
        cfg = self.provider.config.loggingaas
        host_result = self._create_new_host(hostname=cfg.hostname,
                                            ip_v4=cfg.ip_address_v4,
                                            ip_v6=cfg.ip_address_v6,
                                            profile_id=self.profile_id)

        # We currently have to set all values on the update due to an issue
        # when profile_id is equal to None.
        host_id = host_result['host_id']
        self.provider.update_host(host_id=host_id,
                                  hostname="new_hostname",
                                  ip_v4="10.10.1.2",
                                  ip_v6='::1',
                                  profile_id=self.profile_id)

        host_response = self.provider.get_host(host_id)
        host = host_response.entity

        self.assertEqual(200, host_response.status_code,
                         'Status code should have been 200 OK')
        self.assertEqual('new_hostname', host.hostname, 'Incorrect hostname')

    def test_delete_host(self):
        temp_hostname = self.config.loggingaas.hostname
        host_results = self._create_new_host(hostname=temp_hostname)

        # Assertion is in the helper method
        self._delete_host(host_results['host_id'])

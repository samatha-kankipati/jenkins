from testrepo.common.testfixtures.compute import ComputeFixture
import base64
from ccengine.domain.types import NovaServerStatusTypes
from ccengine.common.tools.datagen import rand_name
from ccengine.common.constants.compute_constants import Constants
from ccengine.common.decorators import attr
import unittest2
from random import choice


@unittest2.skip
class HostsTest(ComputeFixture):

    @classmethod
    def setUpClass(cls):
        super(HostsTest, cls).setUpClass()
        all_hosts_response = cls.hosts_client.list_hosts()
        all_hosts = all_hosts_response.entity
        cls.host_details = choice(all_hosts)

    @classmethod
    def tearDownClass(cls):
        super(HostsTest, cls).tearDownClass()

    @attr(type='positive', net='no')
    def test_verify_hosts_list(self):
        hosts_response = self.hosts_client.list_hosts()
        hosts = hosts_response.entity
        self.assertTrue(len(hosts) > 0)

    @attr(type='positive', net='no')
    def test_verify_hosts_describe(self):
        host_response = self.hosts_client.describe_host(hostname=self.host_details.host_name)
        host = host_response.entity
        self.assertTrue(len(host) > 0)

"""Basic Positive Tests for Rax Auth Service APIs"""
import unittest

from ccengine.common.decorators import attr
from testrepo.common.testfixtures.identity.v2_0.identity \
    import IdentityAdminFixture


class ServiceAPIsTest(IdentityAdminFixture):
    """Basic Smoke Tests - Check HTTP Resoponses Service APIs Admin"""

    @classmethod
    def setUpClass(cls):
        super(ServiceAPIsTest, cls).setUpClass()
        cls.type = 'compute'
        cls.version = '2'
        cls.cap = [{"id": "get_servers",
                    "name": "get_servers",
                    "action": "GET",
                    "url": "/servers"},
                   {"id": "get_server",
                    "name": "get_server",
                    "action": "GET",
                    "url": "/servers/{serverId}"}]

    @classmethod
    def tearDownClass(cls):
        pass

    @unittest.skip("Contract change - Need to re-implement this")
    @attr('smoke', type='positive', net='no')
    def test_get_service_apis(self):
        get_serv_apis = self.admin_client.get_service_apis()
        self.assertEqual(get_serv_apis.status_code, 200,
                         msg="Expected response 200 received %s" %
                             get_serv_apis.status_code)

    @unittest.skip("Contract change - Need to re-implement this")
    @attr('smoke', type='positive', net='no')
    def test_get_capabilities(self):
        get_cap = self.admin_client.get_capabilities(
            type=self.type,
            version=self.version)
        self.assertEqual(get_cap.status_code, 200,
                         msg="Expected response 200 received %s" %
                             get_cap.status_code)

    @unittest.skip("Contract change - Need to re-implement this")
    @attr('smoke', type='positive', net='no')
    def test_update_capabilities(self):
        update_cap = self.admin_client.update_capabilities(
            type=self.type,
            version=self.version,
            capabilities=self.cap)
        self.assertEqual(update_cap.status_code, 204,
                         msg="Expected response 204 received %s" %
                             update_cap.status_code)

    @unittest.skip("Contract change - Need to re-implement this")
    @attr('smoke', type='positive', net='no')
    def test_remove_capabilities(self):
        remove_cap = self.admin_client.remove_capabilities(
            type=self.type,
            version=self.version)
        self.assertEqual(remove_cap.status_code, 204,
                         msg="Expected response 204 received %s" %
                             remove_cap.status_code)

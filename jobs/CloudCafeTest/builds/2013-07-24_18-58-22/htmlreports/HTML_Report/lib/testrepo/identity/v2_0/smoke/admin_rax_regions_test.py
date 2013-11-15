from testrepo.common.testfixtures.identity.v2_0.identity \
    import IdentityAdminFixture
from ccengine.common.decorators import attr


class AdminRegionTest(IdentityAdminFixture):

    @classmethod
    def setUpClass(cls):
        super(AdminRegionTest, cls).setUpClass()
        cls.srv = ['cloudFiles']

    @classmethod
    def tearDownClass(cls):
        pass

    @attr('smoke', type='positive')
    def test_get_default_region_services(self):
        get_services = self.admin_client.get_default_region_services()

        self.assertEqual(get_services.status_code, 200,
                msg="Admin get default region services expected response 200 "
                "received %s" % get_services.status_code)

    @attr('smoke', type='positive')
    def test_set_default_region_services(self):
        set_services = self.admin_client.set_default_region_services(
                defaultRegionServices=self.srv)
        self.assertEqual(set_services.status_code, 204,
                msg="Admin set default region services expected response 204 "
                "received %s" % set_services.status_code)

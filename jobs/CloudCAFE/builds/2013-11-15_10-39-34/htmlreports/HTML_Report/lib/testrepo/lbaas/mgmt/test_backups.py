from testrepo.common.testfixtures.load_balancers\
    import BaseLoadBalancersFixture
from ccengine.common.decorators import attr


class BackupTests(BaseLoadBalancersFixture):

    @classmethod
    def setUpClass(cls):
        super(BackupTests, cls).setUpClass()

    @attr('positive')
    def test_backups(self):
        """Testing host backups"""
        r = self.mgmt_client.get_hosts()
        self.assertEquals(r.status_code, 200)
        host_id = r.entity[0].id
        r = self.mgmt_client.get_host_backups(host_id)
        self.assertEquals(r.status_code, 200)
        self.assertIsNotNone(r.entity)

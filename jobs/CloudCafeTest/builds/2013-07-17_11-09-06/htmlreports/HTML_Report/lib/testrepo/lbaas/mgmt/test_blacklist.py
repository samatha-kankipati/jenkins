from testrepo.common.testfixtures.load_balancers \
    import BaseLoadBalancersFixture
from ccengine.common.decorators import attr


class BlacklistTests(BaseLoadBalancersFixture):

    @classmethod
    def setUpClass(cls):
        super(BlacklistTests, cls).setUpClass()

    @attr('positive')
    def test_blacklist_calls(self):
        '''Test the functional blacklist calls'''
        r = self.mgmt_client.get_blacklist()
        self.assertEquals(r.status_code, 200)
        self.assertTrue(len(r.entity) > 0)
        r = self.mgmt_client.add_blacklist_item(cidr_block="127.0.0.1/32",
                                                ip_version="IPV4",
                                                type="NODE")
        self.assertEquals(r.status_code, 202)
        self.assertTrue(r.entity is None)
        r = self.mgmt_client.get_blacklist()
        self.assertEquals(r.status_code, 200)
        item_id = -1
        for item in r.entity:
            if item.cidrBlock == "127.0.0.1/32":
                item_id = item.id
                break
        self.assertTrue(item_id != -1)
        r = self.mgmt_client.delete_blacklist_item(item_id=item_id)
        self.assertEquals(r.status_code, 202)
        r = self.mgmt_client.get_blacklist()
        self.assertEquals(r.status_code, 200)
        for item in r.entity:
            if item.cidrBlock == "127.0.0.1/32":
                item_id = -1
                break
        self.assertTrue(item_id != -1)

from testrepo.common.testfixtures.load_balancers \
    import BaseLoadBalancersFixture
from ccengine.common.decorators import attr


class ClusterTests(BaseLoadBalancersFixture):

    @classmethod
    def setUpClass(cls):
        super(ClusterTests, cls).setUpClass()

    @attr('positive')
    def test_get_clusters_cluster(self):
        '''Test get calls for clusters and singular cluster.'''
        r = self.mgmt_client.get_clusters()
        self.assertEquals(r.status_code, 200)
        self.assertTrue(len(r.entity) > 0)
        cluster = r.entity[0]
        r = self.mgmt_client.get_cluster(cluster.id)
        self.assertEquals(r.status_code, 200)
        self.assertEquals(r.entity.id, cluster.id)

    @attr('positive')
    def test_get_hosts_on_cluster(self):
        '''Retrieve the hosts on a cluster.'''
        r = self.mgmt_client.get_clusters()
        self.assertEquals(r.status_code, 200)
        cluster = r.entity[0]
        r = self.mgmt_client.get_hosts_on_cluster(cluster.id)
        self.assertEquals(r.status_code, 200)
        self.assertTrue(len(r.entity) > 0)

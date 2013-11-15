from testrepo.common.testfixtures.load_balancers \
    import BaseLoadBalancersFixture
from ccengine.domain.lbaas.mgmt.customers import CustomersById, \
    CustomersByName
from ccengine.common.decorators import attr


class CustomerTests(BaseLoadBalancersFixture):

    @classmethod
    def setUpClass(cls):
        super(CustomerTests, cls).setUpClass()

    @attr('positive')
    def test_customer_list_calls(self):
        """Testing customer list generation and customer count calls"""
        r = self.mgmt_client.get_hosts()
        self.assertEquals(r.status_code, 200)
        host_id = r.entity[0].id
        host_name = r.entity[0].name
        r = self.mgmt_client.get_clusters()
        self.assertEquals(r.status_code, 200)
        cluster_id = r.entity[0].id
        cluster_name = r.entity[0].name
        r = self.mgmt_client.get_hosts_customers(CustomersById(host_id))
        self.assertEquals(r.status_code, 200)
        self.assertTrue(len(r.entity.customers) > 0)
        r = self.mgmt_client.get_clusters_customers(CustomersById(cluster_id))
        self.assertEquals(r.status_code, 200)
        self.assertTrue(len(r.entity.customers) > 0)
        r = self.mgmt_client.get_hosts_customers(CustomersByName(host_name))
        self.assertEquals(r.status_code, 200)
        self.assertTrue(len(r.entity.customers) > 0)
        r = self.mgmt_client.get_clusters_customers(
            CustomersByName(cluster_name))
        self.assertEquals(r.status_code, 200)
        self.assertTrue(len(r.entity.customers) > 0)
        r = self.mgmt_client.get_customer_count_on_cluster(cluster_id)
        self.assertEquals(r.status_code, 200)
        self.assertTrue(len(r.entity) > 0)
        r = self.mgmt_client.get_customer_count_on_host(host_id)
        self.assertEquals(r.status_code, 200)
        self.assertTrue(len(r.entity) > 0)

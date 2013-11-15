from testrepo.common.testfixtures.load_balancers \
    import LoadBalancersSmokeFixture
from ccengine.common.decorators import attr
from ccengine.domain.types import LoadBalancerStatusTypes as LBStatus
import ccengine.common.tools.datagen as datagen


class ConnectionThrottleSmokeTests(LoadBalancersSmokeFixture):

    @attr('smoke', 'positive')
    def test_functional_connection_throttling(self):
        """Testing connection throttle update, delete, and get operations"""
        minConnections = datagen.random_int(1, 1000)
        maxConnectionRate = datagen.random_int(1, 100000)
        maxConnections = datagen.random_int(1001, 100000)
        rateInterval = datagen.random_int(1, 3600)
        r = self.client.update_connection_throttle(self.lb.id,
                                                   maxConnectionRate,
                                                   maxConnections,
                                                   minConnections,
                                                   rateInterval)
        self.assertEquals(r.status_code, 202)
        self.lbaas_provider.wait_for_status(self.lb.id)
        r = self.client.get_connection_throttle(self.lb.id)
        created_ct = r.entity
        self.assertEquals(r.status_code, 200)
        self.assertEquals(minConnections, created_ct.minConnections)
        self.assertEquals(maxConnections, created_ct.maxConnections)
        self.assertEquals(maxConnectionRate, created_ct.maxConnectionRate)
        self.assertEquals(rateInterval, created_ct.rateInterval)
        minConnections = datagen.random_int(1, 1000)
        maxConnectionRate = datagen.random_int(1, 100000)
        maxConnections = datagen.random_int(1001, 100000)
        rateInterval = datagen.random_int(1, 3600)
        r = self.client.update_connection_throttle(self.lb.id,
                                                   maxConnectionRate,
                                                   maxConnections,
                                                   minConnections,
                                                   rateInterval)
        self.assertEquals(r.status_code, 202)
        self.lbaas_provider.wait_for_status(self.lb.id)
        r = self.client.get_connection_throttle(self.lb.id)
        updated_ct = r.entity
        self.assertEquals(r.status_code, 200)
        self.assertEquals(minConnections, updated_ct.minConnections)
        self.assertEquals(maxConnections, updated_ct.maxConnections)
        self.assertEquals(maxConnectionRate, updated_ct.maxConnectionRate)
        self.assertEquals(rateInterval, updated_ct.rateInterval)
        r = self.client.delete_connection_throttle(self.lb.id)
        self.assertEquals(r.status_code, 202)
        self.lbaas_provider.wait_for_status(self.lb.id)
        r = self.client.get_connection_throttle(self.lb.id)
        deleted_ct = r.entity
        self.assertEquals(r.status_code, 200)
        self.assertIsNone(deleted_ct.maxConnectionRate)
        self.assertIsNone(deleted_ct.maxConnections)
        self.assertIsNone(deleted_ct.minConnections)
        self.assertIsNone(deleted_ct.rateInterval)

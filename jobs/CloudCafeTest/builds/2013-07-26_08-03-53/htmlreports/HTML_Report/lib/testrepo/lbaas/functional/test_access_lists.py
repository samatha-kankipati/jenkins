from testrepo.common.testfixtures.load_balancers \
    import LoadBalancersSmokeFixture, LoadBalancersZeusFixture
from ccengine.common.decorators import attr
from ccengine.domain.types import LoadBalancerAccessListTypes as LBALT
import ccengine.common.tools.datagen as datagen


class AccessListsSmokeTests(LoadBalancersSmokeFixture):

    @attr('smoke', 'positive')
    def test_add_remove_access_list(self):
        """CRUD operations and batch delete access lists."""
        al_count = 0
        r = self.client.get_access_list(self.lb.id)
        self.assertEquals(r.status_code, 200)
        self.assertEquals(len(r.entity), 0)
        al_address = datagen.random_ip()
        al_type = datagen.random_item_in_list(['ALLOW', 'DENY'])
        r = self.client.create_access_list(self.lb.id,
                                           address=al_address,
                                           type=al_type)
        self.assertEquals(r.status_code, 202)
        al_count += 1
        self.lbaas_provider.wait_for_status(self.lb.id)
        r = self.client.get_access_list(self.lb.id)
        self.assertEquals(r.status_code, 200)
        self.assertEquals(r.entity[0].address, al_address)
        self.assertEquals(r.entity[0].type, al_type)
        network_item1 = r.entity[0]
        al_address_list = []
        al_type_list = []
        for _ in range(0, 5):
            al_temp_address = datagen.random_ip()
            al_temp_type = datagen.random_item_in_list(['ALLOW', 'DENY'])
            for addr in al_address_list:
                while al_temp_address == addr:
                    al_temp_address = datagen.random_ip()
            al_address_list.append(al_temp_address)
            al_type_list.append(al_temp_type)
            al_count += 1
        r = self.client.create_access_list(self.lb.id,
                                           address=al_address_list,
                                           type=al_type_list)
        self.assertEquals(r.status_code, 202)
        self.lbaas_provider.wait_for_status(self.lb.id)
        r = self.client.get_access_list(self.lb.id)
        al = r.entity
        self.assertEquals(r.status_code, 200)
        self.assertEquals(len(al), al_count)
        r = self.client.delete_access_list_item(self.lb.id,
                                                network_item1.id)
        self.assertEquals(r.status_code, 202)
        self.lbaas_provider.wait_for_status(self.lb.id)
        al_count -= 1
        r = self.client.get_access_list(self.lb.id)
        al = r.entity
        self.assertEquals(r.status_code, 200)
        self.assertEquals(len(al), al_count)
        al_id_list = []
        for item in al:
            self.assertFalse(item.id == network_item1.id)
            al_id_list.append(item.id)
            al_count -= 1
        al_id1 = al_id_list.pop()
        al_count += 1
        al_id2 = al_id_list.pop()
        al_count += 1
        r = self.client.batch_delete_access_list_items(self.lb.id, al_id_list)
        self.assertEquals(r.status_code, 202)
        self.lbaas_provider.wait_for_status(self.lb.id)
        r = self.client.get_access_list(self.lb.id)
        al = r.entity
        self.assertEquals(r.status_code, 200)
        self.assertEquals(len(al), al_count)
        for item in al:
            self.assertTrue(item.id == al_id1 or item.id == al_id2)
        r = self.client.delete_access_list(self.lb.id)
        self.assertEquals(r.status_code, 202)
        self.lbaas_provider.wait_for_status(self.lb.id)
        r = self.client.get_access_list(self.lb.id)
        al = r.entity
        self.assertEquals(r.status_code, 200)
        self.assertEquals(len(al), 0)


class AccessListsTests(LoadBalancersZeusFixture):

    @classmethod
    def setUpClass(cls):
        super(AccessListsTests, cls).setUpClass()
        cls.lb = cls.lbaas_provider.create_active_load_balancer().entity
        cls.lbs_to_delete.append(cls.lb.id)
        cls.zeus_vs_name = '_'.join([str(cls.tenant_id), str(cls.lb.id)])

    def setUp(self):
        super(AccessListsTests, self).setUp()
        self.lbaas_provider.wait_for_status(self.lb.id)
        self.client.delete_access_list(self.lb.id)
        self.lbaas_provider.wait_for_status(self.lb.id)

    @attr('positive')
    def test_batch_delete_access_list(self):
        r = self.client.get_access_list(self.lb.id)
        self.assertEquals(len(r.entity), 0)
        r = self.client.create_access_list(self.lb.id,
                                           address=['11.1.1.1', '11.1.1.2'],
                                           type=[LBALT.ALLOW, LBALT.DENY])
        self.assertEquals(r.status_code, 202)
        self.lbaas_provider.wait_for_status(self.lb.id)
        r = self.client.get_access_list(self.lb.id)
        access_list = r.entity
        self.assertEquals(len(access_list), 2)
        resp = self.zeus_protection.getAllowedAddresses([self.zeus_vs_name])
        self.assertEquals(len(resp[1][0]), 1)
        self.assertEquals(resp[1][0][0], '11.1.1.1')
        resp = self.zeus_protection.getBannedAddresses([self.zeus_vs_name])
        self.assertEquals(len(resp[1][0]), 1)
        self.assertEquals(resp[1][0][0], '11.1.1.2')
        al_ids = [item.id for item in access_list]
        r = self.client.batch_delete_access_list_items(
            self.lb.id,
            network_item_id_list=al_ids)
        self.assertEquals(r.status_code, 202)
        self.lbaas_provider.wait_for_status(self.lb.id)
        resp = self.zeus_protection.getAllowedAddresses([self.zeus_vs_name])
        self.assertEquals(len(resp[1][0]), 0)
        resp = self.zeus_protection.getBannedAddresses([self.zeus_vs_name])
        self.assertEquals(len(resp[1][0]), 0)

from testrepo.common.testfixtures.load_balancers \
    import LoadBalancersSmokeFixture
from ccengine.common.decorators import attr
import ccengine.common.tools.datagen as datagen


class MetadataSmokeTests(LoadBalancersSmokeFixture):

    @attr('smoke', 'positive')
    def test_metadata_crud(self):
        '''Metadata CRUD operations'''
        md_key = 'testkey1'
        md2_key = 'testkey2'
        md3_key = 'testkey3'
        metadata = [{'key': md_key, 'value': 'testvalue1'},
                    {'key': md2_key, 'value': 'testvalue2'},
                    {'key': md3_key, 'value': 'testvalue3'}]
        r = self.client.add_load_balancer_metadata(self.lb.id, metadata)
        md_created_list = r.entity
        self.assertEquals(r.status_code, 200)
        for meta in metadata:
            self.assertIsNotNone(md_created_list.get(meta['key']))
        md1 = md_created_list.get_meta(md_key)
        md2 = md_created_list.get_meta(md2_key)
        md3 = md_created_list.get_meta(md3_key)
        r = self.client.list_load_balancer_metadata(self.lb.id)
        md_list = r.entity
        for meta in metadata:
            self.assertIsNotNone(md_list.get(meta['key']))
        r = self.client.get_load_balancer_meta_item(self.lb.id, md1.id)
        md_item = r.entity
        self.assertEquals(r.status_code, 200)
        self.assertEquals(md_item.key, md1.key)
        self.assertEquals(md_item.value, md1.value)
        value = 'new_value'
        r = self.client.update_load_balancer_meta_item(self.lb.id, md1.id,
                                                       value)
        self.assertEquals(r.status_code, 200)
        r = self.client.get_load_balancer_meta_item(self.lb.id, md1.id)
        md_item = r.entity
        self.assertEquals(r.status_code, 200)
        self.assertEquals(md_item.key, md1.key)
        self.assertEquals(md_item.value, value)
        r = self.client.delete_load_balancer_meta_item(self.lb.id, md1.id)
        self.assertEquals(r.status_code, 200)
        r = self.client.batch_delete_load_balancer_meta_items(self.lb.id,
                                                              [md2.id, md3.id])
        self.assertEquals(r.status_code, 200)
        r = self.client.list_load_balancer_metadata(self.lb.id)
        md_list = r.entity
        self.assertIsNone(md_list.get(md1.key))
        self.assertIsNone(md_list.get(md2.key))
        self.assertIsNone(md_list.get(md3.key))

    @attr('smoke', 'positive')
    def test_node_metadata_crud(self):
        '''Node Metadata CRUD operations'''
        md_key = 'testkey1'
        md2_key = 'testkey2'
        md3_key = 'testkey3'
        metadata = [{'key': md_key, 'value': 'testvalue1'},
                    {'key': md2_key, 'value': 'testvalue2'},
                    {'key': md3_key, 'value': 'testvalue3'}]
        r = self.client.add_node_metadata(self.lb.id, self.lb.nodes[0].id,
                                          metadata)
        md_created_list = r.entity
        self.assertEquals(r.status_code, 200)
        for meta in metadata:
            self.assertIsNotNone(md_created_list.get(meta['key']))
        md1 = md_created_list.get_meta(md_key)
        md2 = md_created_list.get_meta(md2_key)
        md3 = md_created_list.get_meta(md3_key)
        r = self.client.list_node_metadata(self.lb.id, self.lb.nodes[0].id)
        md_list = r.entity
        for meta in metadata:
            self.assertIsNotNone(md_list.get(meta['key']))
        r = self.client.get_node_meta_item(self.lb.id, self.lb.nodes[0].id,
                                           md1.id)
        md_item = r.entity
        self.assertEquals(r.status_code, 200)
        self.assertEquals(md_item.key, md1.key)
        self.assertEquals(md_item.value, md1.value)
        value = 'new_value'
        r = self.client.update_node_meta_item(self.lb.id, self.lb.nodes[0].id,
                                              md1.id, value)
        self.assertEquals(r.status_code, 200)
        r = self.client.get_node_meta_item(self.lb.id, self.lb.nodes[0].id,
                                           md1.id)
        md_item = r.entity
        self.assertEquals(r.status_code, 200)
        self.assertEquals(md_item.key, md1.key)
        self.assertEquals(md_item.value, value)
        r = self.client.delete_node_meta_item(self.lb.id, self.lb.nodes[0].id,
                                              md1.id)
        self.assertEquals(r.status_code, 200)
        r = self.client.batch_delete_node_meta_items(self.lb.id,
                                                     self.lb.nodes[0].id,
                                                     [md2.id, md3.id])
        self.assertEquals(r.status_code, 200)
        r = self.client.list_node_metadata(self.lb.id, self.lb.nodes[0].id)
        md_list = r.entity
        self.assertIsNone(md_list.get(md1.key))
        self.assertIsNone(md_list.get(md2.key))
        self.assertIsNone(md_list.get(md3.key))

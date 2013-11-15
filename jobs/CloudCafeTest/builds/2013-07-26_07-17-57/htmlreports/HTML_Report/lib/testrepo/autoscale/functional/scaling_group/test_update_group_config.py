from testrepo.common.testfixtures.autoscale import AutoscaleFixture
from ccengine.common.tools.datagen import rand_name


class UpdateGroupConfigTest(AutoscaleFixture):

    @classmethod
    def setUpClass(cls):
        super(UpdateGroupConfigTest, cls).setUpClass()
        create_resp = cls.autoscale_provider.create_scaling_group_min()
        cls.group = create_resp.entity
        cls.resources.add(cls.group.id,
                          cls.autoscale_client.delete_scaling_group)
        cls.gc_name = rand_name("updgroupconfig")
        cls.gc_min_entities = cls.group.groupConfiguration.minEntities
        cls.gc_cooldown = 800
        cls.gc_max_entities = 25
        cls.gc_metadata = {"upd_key1": "upd_value1"}
        cls.update_group_response = cls.autoscale_client.update_group_config(
            group_id=cls.group.id,
            name=cls.gc_name,
            cooldown=cls.gc_cooldown,
            min_entities=cls.gc_min_entities,
            max_entities=cls.gc_max_entities,
            metadata=cls.gc_metadata)
        cls.update_group = cls.update_group_response.entity

    @classmethod
    def tearDownClass(cls):
        super(UpdateGroupConfigTest, cls).tearDownClass()

    def test_list_group_config_response(self):
        group_config_response = self.autoscale_client.view_scaling_group_config(self.group.id)
        updated_config = group_config_response.entity
        self.assertEquals(self.update_group_response.status_code, 204,
                          msg="Update group config failed with %s"
                          % self.update_group_response.status_code)
        self.assertTrue(self.update_group_response.headers is not None,
                        msg="The headers are not as expected")
        self.validate_headers(self.update_group_response.headers)
        self.assertEquals(updated_config.minEntities, self.gc_min_entities,
                          msg="Min entities in the Group config did not update")
        self.assertEquals(updated_config.cooldown, self.gc_cooldown,
                          msg="Cooldown time in the Group config did not update")
        self.assertEquals(updated_config.name, self.gc_name,
                          msg="Name in the Group config did not update")
        self.assertEquals(updated_config.maxEntities, self.gc_max_entities,
                          msg="Max entities in the Group config did not update")
        self.assertEquals(self.autoscale_provider.to_data(updated_config.metadata),
                          self.gc_metadata,
                          msg="Metadata in the Group config did not update")

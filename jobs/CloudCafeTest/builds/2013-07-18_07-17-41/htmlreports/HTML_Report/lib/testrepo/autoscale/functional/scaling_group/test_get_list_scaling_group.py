from testrepo.common.testfixtures.autoscale import AutoscaleFixture


class ScalingGroupListTest(AutoscaleFixture):

    @classmethod
    def setUpClass(cls):
        super(ScalingGroupListTest, cls).setUpClass()
        """ Create 3 scaling groups """
        first_group = cls.autoscale_provider.create_scaling_group_min()
        cls.first_scaling_group = first_group.entity
        second_group = cls.autoscale_provider.create_scaling_group_min()
        cls.second_scaling_group = second_group.entity
        third_group = cls.autoscale_provider.create_scaling_group_min()
        cls.third_scaling_group = third_group.entity
        ''' Adding groups to the resource repository'''
        cls.resources.add(cls.first_scaling_group.id,
                          cls.autoscale_client.delete_scaling_group)
        cls.resources.add(cls.second_scaling_group.id,
                          cls.autoscale_client.delete_scaling_group)
        cls.resources.add(cls.third_scaling_group.id,
                          cls.autoscale_client.delete_scaling_group)

    @classmethod
    def teardown(cls):
        super(ScalingGroupListTest, cls).tearDownClass()

    def test_get_scaling_group(self):
        """ return a view of the manifest config for a scaling group """
        group_info_response = self.autoscale_client.\
            view_manifest_config_for_scaling_group(group_id=self.first_scaling_group.id)
        group_info = group_info_response.entity
        self.assertEqual(200, group_info_response.status_code,
                         msg="The get scaling group call failed with %s"
                         % group_info_response.status_code)
        self.assertTrue(group_info_response.headers,
                        msg="The headers are not as expected, %s"
                        % group_info_response.headers)
        self.validate_headers(group_info_response.headers)
        self.assertEqual(group_info.id, self.first_scaling_group.id,
                         msg="Group id did not match")
        self.assertEqual(group_info.groupConfiguration.name,
                         self.first_scaling_group.groupConfiguration.name,
                         msg="Group name did not match")
        self.assertEqual(group_info.groupConfiguration.minEntities,
                         self.first_scaling_group.groupConfiguration.minEntities,
                         msg="Group's minimum entities did not match")
        self.assertEqual(group_info.launchConfiguration,
                         self.first_scaling_group.launchConfiguration,
                         msg="Group's launch configurations did not match")

    def test_list_scaling_group(self):
        """ All scaling groups should be returned """
        list_groups_response = self.autoscale_client.list_scaling_groups()
        list_groups = list_groups_response.entity
        self.assertEqual(200, list_groups_response.status_code,
                         msg="The list scaling group call failed with: %s"
                         % list_groups_response.content)
        self.validate_headers(list_groups_response.headers)
        self.assertTrue(self.first_scaling_group.min_details() in
                        list_groups, msg="Group with id %s was not found in the list %s"
                        % (self.first_scaling_group.id, list_groups))
        self.assertTrue(self.second_scaling_group.min_details() in
                        list_groups, msg="Group with id %s was not found in the list"
                        % self.second_scaling_group.id)
        self.assertTrue(self.third_scaling_group.min_details() in
                        list_groups, msg="Group with id %s was not found in the list"
                        % self.third_scaling_group.id)

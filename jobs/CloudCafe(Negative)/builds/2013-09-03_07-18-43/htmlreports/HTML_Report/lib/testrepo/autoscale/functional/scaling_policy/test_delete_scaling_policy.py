from testrepo.common.testfixtures.autoscale import AutoscaleFixture


class DeleteScalingPolicy(AutoscaleFixture):

    @classmethod
    def setUpClass(cls):
        super(DeleteScalingPolicy, cls).setUpClass()
        create_resp = cls.autoscale_provider.create_scaling_group_min()
        cls.group = create_resp.entity
        cls.resources.add(cls.group.id,
                          cls.autoscale_client.delete_scaling_group)
        cls.policy_response = cls.autoscale_client.create_policy(
            group_id=cls.group.id,
            name=cls.sp_name,
            cooldown=cls.sp_cooldown,
            change=cls.sp_change)
        cls.policy = cls.policy_response.entity

    @classmethod
    def tearDownClass(cls):
        super(DeleteScalingPolicy, cls).tearDownClass()

    def test_delete_scaling_policy(self):
        self.assertEquals(self.policy_response.status_code, 201,
                          msg="Create scaling policy failed with %s"
                          % self.policy_response.status_code)
        policy = self.autoscale_provider.get_policy_properties(self.policy)
        delete_policy = self.autoscale_client.delete_scaling_policy(
            group_id=self.group.id,
            policy_id=policy["id"])
        self.assertEquals(delete_policy.status_code, 204,
                          msg="Delete scaling policy failed with %s"
                          % delete_policy.status_code)
        self.assertTrue(delete_policy.headers is not None,
                          msg="The headers are not as expected")
        self.validate_headers(delete_policy.headers)

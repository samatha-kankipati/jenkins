from testrepo.common.testfixtures.autoscale import AutoscaleFixture


class UpdateScalingPolicy(AutoscaleFixture):

    @classmethod
    def setUpClass(cls):
        super(UpdateScalingPolicy, cls).setUpClass()
        create_resp = cls.autoscale_provider.create_scaling_group_min()
        cls.group = create_resp.entity
        cls.resources.add(cls.group.id,
                          cls.autoscale_client.delete_scaling_group)
        policy_response = cls.autoscale_client.create_policy(group_id=cls.group.id,
                                                             name=cls.sp_name,
                                                             cooldown=cls.sp_cooldown,
                                                             change=cls.sp_change)
        cls.policy = policy_response.entity
        cls.policy_details = cls.autoscale_provider.get_policy_properties(cls.policy)
        cls.update_policy_response = cls.autoscale_client.update_policy(
            group_id=cls.group.id,
            policy_id=cls.policy_details["id"],
            name=cls.policy_details["name"],
            cooldown=cls.policy_details["cooldown"],
            change=cls.upd_sp_change)
        cls.update_policy = cls.update_policy_response.entity

    @classmethod
    def tearDownClass(cls):
        super(UpdateScalingPolicy, cls).tearDownClass()

    def test_update_scaling_policy(self):
        policy_response = self.autoscale_client.get_policy_details(self.group.id, self.policy_details["id"])
        updated_policy = policy_response.entity
        self.assertEquals(self.update_policy_response.status_code, 204,
                          msg="Update scaling policy failed with %s"
                          % self.update_policy_response.status_code)
        self.assertTrue(self.update_policy_response.headers is not None,
                          msg="The headers are not as expected")
        self.validate_headers(self.update_policy_response.headers)
        self.assertEquals(updated_policy.id, self.policy_details["id"],
                        msg="Policy Id is not as expected after update")
        self.assertEquals(updated_policy.links, self.policy_details["links"],
                        msg="Links for the scaling policy is none after the update")
        self.assertEquals(updated_policy.name, self.policy_details["name"],
                          msg="Name of the policy is None after update")
        self.assertEquals(updated_policy.cooldown, self.policy_details["cooldown"],
                          msg="Cooldown of the policy in null after an update")
        self.assertEquals(updated_policy.change, self.upd_sp_change,
                          msg="Change in the policy did not update")

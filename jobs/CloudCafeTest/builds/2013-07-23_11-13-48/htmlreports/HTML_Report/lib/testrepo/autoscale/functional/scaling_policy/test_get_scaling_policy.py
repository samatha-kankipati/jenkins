from testrepo.common.testfixtures.autoscale import AutoscaleFixture


class GetScalingPolicy(AutoscaleFixture):

    @classmethod
    def setUpClass(cls):
        super(GetScalingPolicy, cls).setUpClass()
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
        cls.policy_id = cls.policy_details["id"]
        cls.get_policy_response = cls.autoscale_client.get_policy_details(cls.group.id, cls.policy_id)
        cls.get_policy = cls.get_policy_response.entity

    @classmethod
    def tearDownClass(cls):
        super(GetScalingPolicy, cls).tearDownClass()

    def test_get_scaling_policy(self):
        self.assertEquals(self.get_policy_response.status_code, 200,
                          msg="Get scaling policy failed with %s"
                          % self.get_policy_response.status_code)
        self.assertTrue(self.get_policy_response.headers is not None,
                          msg="The headers are not as expected")
        self.validate_headers(self.get_policy_response.headers)
        self.assertEquals(self.get_policy.id, self.policy_details["id"],
                        msg="Policy Id is none upon creation")
        self.assertEquals(self.get_policy.links, self.policy_details["links"],
                        msg="Links for the scaling policy is none")
        self.assertEquals(self.get_policy.name, self.sp_name,
                          msg="Name of the policy did not match")
        self.assertEquals(self.get_policy.cooldown, self.sp_cooldown,
                          msg="Cooldown time in the policy did not match")
        self.assertEquals(self.get_policy.change, self.sp_change,
                          msg="Change in the policy did not match")

from testrepo.common.testfixtures.autoscale import AutoscaleFixture
import sys


class CreateScalingPolicy(AutoscaleFixture):

    @classmethod
    def setUpClass(cls):
        super(CreateScalingPolicy, cls).setUpClass()
        create_resp = cls.autoscale_provider.create_scaling_group_min()
        cls.group = create_resp.entity
        cls.resources.add(cls.group.id,
                          cls.autoscale_client.delete_scaling_group)
        #cls.sp_name = rand_name(cls.sp_name)
        cls.create_policy_response = cls.autoscale_client.create_policy(group_id=cls.group.id,
                                                                        name=cls.sp_name,
                                                                        cooldown=cls.sp_cooldown,
                                                                        change=cls.sp_change)
        cls.create_policy = cls.create_policy_response.entity

    @classmethod
    def tearDownClass(cls):
        super(CreateScalingPolicy, cls).tearDownClass()

    def test_create_scaling_policy(self):
        self.assertEquals(self.create_policy_response.status_code, 201,
                          msg="Create scaling policy failed with %s"
                          % self.create_policy_response.status_code)
        self.assertTrue(self.create_policy_response.headers is not None,
                        msg="The headers are not as expected")
        self.validate_headers(self.create_policy_response.headers)
        policy = self.autoscale_provider.get_policy_properties(self.create_policy)
        self.assertTrue(policy["id"] is not None,
                        msg="Scaling policy id is None")
        self.assertTrue(policy["links"] is not None,
                        msg="Newly created scaling policy's links are null")
        self.assertEquals(policy["cooldown"], self.sp_cooldown,
                          msg="scaling policy's cooldown time does not match")
        self.assertEquals(policy["change"], self.sp_change,
                          msg="Scaling policy's change does not match")
        self.assertEquals(policy["name"], self.sp_name,
                          msg="Scaling policy's name does not match")
        self.assertEquals(policy["count"], 1,
                          msg="More scaling policies listed than created")

    def test_scaling_policy_maxint_cooldown_change(self):
        '''
        Negative Test: Test scaling policy when change and cooldown are maxint
        '''
        cooldown = change = sys.maxint
        create_resp = self.autoscale_client.create_policy(group_id=self.group.id,
                                                                name=self.sp_name,
                                                                cooldown=cooldown,
                                                                change=change)
        policy = create_resp.entity
        self.assertEquals(create_resp.status_code, 201,
                          msg="Create scaling policy failed with maxint as cooldown & change: %s"
                          % create_resp.status_code)
        self.assertTrue(policy is not None,
                        msg="Create scaling policy failed: %s"
                        % policy)

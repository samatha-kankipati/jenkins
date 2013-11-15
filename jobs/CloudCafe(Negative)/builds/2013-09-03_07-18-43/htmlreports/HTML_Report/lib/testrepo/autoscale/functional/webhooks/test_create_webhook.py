from testrepo.common.testfixtures.autoscale import AutoscaleFixture


class CreateWebhook(AutoscaleFixture):

    @classmethod
    def setUpClass(cls):
        super(CreateWebhook, cls).setUpClass()
        create_resp = cls.autoscale_provider.create_scaling_group_min()
        cls.group = create_resp.entity
        create_policy = cls.autoscale_provider.create_policy_min(group_id=cls.group.id)
        cls.policy = create_policy.entity
        cls.policy_details = cls.autoscale_provider.get_policy_properties(cls.policy)
        cls.resources.add(cls.group.id,
                          cls.autoscale_client.delete_scaling_group)
        cls.wb_metadata = {"meta": "key"}
        cls.create_webhook_response = cls.autoscale_client.create_webhook(
            group_id=cls.group.id,
            policy_id=cls.policy_details["id"],
            name=cls.wb_name,
            metadata=cls.wb_metadata)
        cls.create_webhook = cls.create_webhook_response.entity
        cls.webhook = cls.autoscale_provider.get_webhooks_properties(cls.create_webhook)

    @classmethod
    def tearDownClass(cls):
        super(CreateWebhook, cls).tearDownClass()

    def test_create_webhook(self):
        self.assertEquals(self.create_webhook_response.status_code, 201,
                          msg="Create webhook for a policy failed with %s"
                          % self.create_webhook_response.status_code)
        self.validate_headers(self.create_webhook_response.headers)
        self.assertTrue(self.webhook["id"] is not None,
                        msg="Webhook id is None")
        self.assertTrue(self.webhook["links"] is not None,
                        msg="Newly created Webhook's links are null")
        self.assertEquals(self.webhook["name"], self.wb_name,
                          msg="Webhook's name does not match")
        self.assertEquals(self.autoscale_provider.to_data(self.webhook["metadata"]),
                          self.wb_metadata,
                          msg="Webhook's metadata does not match %s" % self.wb_metadata)

from testrepo.common.testfixtures.autoscale import AutoscaleFixture


class GetWebhook(AutoscaleFixture):

    @classmethod
    def setUpClass(cls):
        super(GetWebhook, cls).setUpClass()
        create_resp = cls.autoscale_provider.create_scaling_group_min()
        cls.group = create_resp.entity
        cls.resources.add(cls.group.id,
                          cls.autoscale_client.delete_scaling_group)
        policy_response = cls.autoscale_provider.create_policy_min(group_id=cls.group.id)
        cls.policy = policy_response.entity
        cls.policy_details = cls.autoscale_provider.get_policy_properties(cls.policy)
        cls.wb_metadata = {"wb_key": "wb_value"}
        cls.webhook_response = cls.autoscale_client.create_webhook(
            group_id=cls.group.id,
            policy_id=cls.policy_details["id"],
            name=cls.wb_name,
            metadata=cls.wb_metadata)
        cls.create_webhook = cls.webhook_response.entity
        cls.webhook = cls.autoscale_provider.get_webhooks_properties(cls.create_webhook)
        cls.get_webhook_response = cls.autoscale_client.get_webhook(cls.group.id,
                                                                    cls.policy_details["id"],
                                                                    cls.webhook["id"])
        cls.get_webhook = cls.get_webhook_response.entity

    @classmethod
    def tearDownClass(cls):
        super(GetWebhook, cls).tearDownClass()

    def test_get_webhook(self):
        self.assertEquals(self.get_webhook_response.status_code, 200,
                          msg="Get webhook failed with %s"
                          % self.get_webhook_response.status_code)
        self.validate_headers(self.get_webhook_response.headers)
        self.assertEquals(self.get_webhook.id, self.webhook["id"],
                          msg="Webhook Id is null")
        self.assertEquals(self.get_webhook.links, self.webhook["links"],
                          msg="Links for the webhook is null")
        self.assertEquals(self.get_webhook.name, self.wb_name,
                          msg="Name of the webhook did not match")
        self.assertEquals(self.autoscale_provider.to_data(self.get_webhook.metadata), self.wb_metadata,
                          msg="Metadata of the webhook did not match")

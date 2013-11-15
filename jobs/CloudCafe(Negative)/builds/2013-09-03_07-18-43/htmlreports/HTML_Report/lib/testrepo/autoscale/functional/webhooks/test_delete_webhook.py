from testrepo.common.testfixtures.autoscale import AutoscaleFixture


class DeleteWebhook(AutoscaleFixture):

    @classmethod
    def setUpClass(cls):
        super(DeleteWebhook, cls).setUpClass()
        create_resp = cls.autoscale_provider.create_scaling_group_min()
        cls.group = create_resp.entity
        cls.resources.add(cls.group.id,
                          cls.autoscale_client.delete_scaling_group)
        cls.policy_response = cls.autoscale_provider.create_policy_min(group_id=cls.group.id)
        cls.policy = cls.policy_response.entity
        cls.policy_details = cls.autoscale_provider.get_policy_properties(cls.policy)
        cls.webhook_response = cls.autoscale_client.create_webhook(
            group_id=cls.group.id,
            policy_id=cls.policy_details["id"],
            name=cls.wb_name)
        cls.create_webhook = cls.webhook_response.entity
        cls.webhook = cls.autoscale_provider.get_webhooks_properties(cls.create_webhook)

    @classmethod
    def tearDownClass(cls):
        super(DeleteWebhook, cls).tearDownClass()

    def test_delete_webhook(self):
        self.assertEquals(self.webhook_response.status_code, 201,
                          msg="Create webhook failed with %s"
                          % self.webhook_response.status_code)
        delete_webhook_resp = self.autoscale_client.delete_webhook(
            group_id=self.group.id,
            policy_id=self.policy_details["id"],
            webhook_id=self.webhook["id"])
        self.assertEquals(delete_webhook_resp.status_code, 204,
                          msg="Delete webhook failed with %s"
                          % delete_webhook_resp.status_code)
        self.validate_headers(delete_webhook_resp.headers)

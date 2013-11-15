from testrepo.common.testfixtures.autoscale import AutoscaleFixture


class UpdateWebhook(AutoscaleFixture):

    @classmethod
    def setUpClass(cls):
        super(UpdateWebhook, cls).setUpClass()
        create_resp = cls.autoscale_provider.create_scaling_group_min()
        cls.group = create_resp.entity
        cls.resources.add(cls.group.id,
                          cls.autoscale_client.delete_scaling_group)
        policy_response = cls.autoscale_provider.create_policy_min(group_id=cls.group.id)
        cls.policy_details = policy_response.entity
        cls.policy = cls.autoscale_provider.get_policy_properties(cls.policy_details)
        webhook_response = cls.autoscale_client.create_webhook(
            group_id=cls.group.id,
            policy_id=cls.policy["id"],
            name=cls.wb_name)
        cls.create_webhook = webhook_response.entity
        cls.webhook = cls.autoscale_provider.get_webhooks_properties(cls.create_webhook)
        cls.upd_wb_name = "updated_wb_name"
        cls.update_webhook_response = cls.autoscale_client.update_webhook(
            group_id=cls.group.id,
            policy_id=cls.policy["id"],
            webhook_id=cls.webhook["id"],
            name=cls.upd_wb_name
        )
        cls.update_webhook = cls.update_webhook_response.entity

    @classmethod
    def tearDownClass(cls):
        super(UpdateWebhook, cls).tearDownClass()

    def test_update_webhook(self):
        get_webhook_response = self.autoscale_client.get_webhook(self.group.id,
                                                                 self.policy["id"],
                                                                 self.webhook["id"])
        updated_webhook = get_webhook_response.entity
        self.assertEquals(self.update_webhook_response.status_code, 204,
                          msg="Update webhook failed with %s"
                          % self.update_webhook_response.status_code)
        self.assertTrue(self.update_webhook_response.headers is not None,
                        msg="The headers are not as expected")
        self.validate_headers(self.update_webhook_response.headers)
        self.assertEquals(updated_webhook.id, self.webhook["id"],
                          msg="Webhook Id is not as expected after the update")
        self.assertEquals(updated_webhook.links, self.webhook["links"],
                          msg="Links for the webhook is not as expected after the update")
        self.assertEquals(updated_webhook.name, self.upd_wb_name,
                          msg="Name of the webhook did not update")

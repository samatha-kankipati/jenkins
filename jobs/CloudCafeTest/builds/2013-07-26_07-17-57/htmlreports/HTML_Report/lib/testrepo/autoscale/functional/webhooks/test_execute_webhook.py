from testrepo.common.testfixtures.autoscale import AutoscaleFixture
import os


class GetWebhook(AutoscaleFixture):

    @classmethod
    def setUpClass(cls):
        super(GetWebhook, cls).setUpClass()
        create_resp = cls.autoscale_provider.create_scaling_group_min()
        cls.group = create_resp.entity
        cls.resources.add(cls.group.id,
                          cls.autoscale_client.delete_scaling_group)
        policy_response = cls.autoscale_provider.create_policy_min(group_id=cls.group.id)
        cls.policy = cls.autoscale_provider.get_policy_properties(policy_response.entity)
        cls.wb_metadata = {"wb_key": "wb_value"}
        webhook_response = cls.autoscale_client.create_webhook(
            group_id=cls.group.id,
            policy_id=cls.policy["id"],
            name=cls.wb_name,
            metadata=cls.wb_metadata)
        cls.webhook = cls.autoscale_provider.get_webhooks_properties(webhook_response.entity)
        cls.get_webhook_response = cls.autoscale_client.get_webhook(cls.group.id,
                                                                    cls.policy["id"],
                                                                    cls.webhook["id"])
        cls.get_webhook = cls.get_webhook_response.entity

    @classmethod
    def tearDownClass(cls):
        super(GetWebhook, cls).tearDownClass()

    def test_execute_webhook(self):
        cap_url = self.get_webhook.links.capability
        env = os.environ['CLOUDCAFE_TEST_CONFIG']
        if "dev" in env.lower():
            cap_url = (str(cap_url))[:16] + ':9000' +\
                (str(cap_url))[16:]
        execute_wb_resp = self.autoscale_client.execute_webhook(cap_url)
        self.assertEquals(execute_wb_resp.status_code, 202,
                          msg="Execute webhook failed with %s"
                          % execute_wb_resp.status_code)
        self.validate_headers(execute_wb_resp.headers)

    def test_execute_webhook_after_update(self):
        cap_url_before_update = self.get_webhook.links.capability
        env = os.environ['CLOUDCAFE_TEST_CONFIG']
        if "dev" in env.lower():
            cap_url_before_update = (str(cap_url_before_update))[:16] + ':9000' +\
                (str(cap_url_before_update))[16:]
        update_webhook_resp = self.autoscale_client.update_webhook(group_id=self.group.id,
                                                                   policy_id=self.policy["id"],
                                                                   webhook_id=self.webhook["id"],
                                                                   name='update_execute_webhook')
        self.assertEquals(update_webhook_resp.status_code, 204,
                          msg="Update webhook failed with %s"
                          % update_webhook_resp.status_code)
        updated_webhook_response = self.autoscale_client.get_webhook(self.group.id,
                                                                     self.policy["id"],
                                                                     self.webhook["id"])
        updated_webhook = updated_webhook_response.entity
        cap_url_after_update = updated_webhook.links.capability
        env = os.environ['CLOUDCAFE_TEST_CONFIG']
        if "dev" in env.lower():
            cap_url_after_update = (str(cap_url_after_update))[:16] + ':9000' +\
                (str(cap_url_after_update))[16:]
        self.assertEquals(cap_url_before_update, cap_url_after_update,
                          msg='Capability URL changed upon update to webhook name')
        execute_wb_resp = self.autoscale_client.execute_webhook(cap_url_after_update)
        self.assertEquals(execute_wb_resp.status_code, 202,
                          msg="Execute webhook failed with %s"
                          % execute_wb_resp.status_code)
        self.validate_headers(execute_wb_resp.headers)

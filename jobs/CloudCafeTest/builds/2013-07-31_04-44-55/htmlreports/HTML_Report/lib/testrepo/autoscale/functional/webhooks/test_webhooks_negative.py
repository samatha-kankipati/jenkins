from testrepo.common.testfixtures.autoscale import AutoscaleFixture
from ccengine.domain.status_codes import HttpStatusCodes
import unittest2 as unittest
import os


class ScalingWebhooksNegative(AutoscaleFixture):
    @classmethod
    def setUpClass(cls):
        super(ScalingWebhooksNegative, cls).setUpClass()
        create_resp = cls.autoscale_provider.create_scaling_group_min()
        cls.group = create_resp.entity
        cls.resources.add(cls.group.id,
                          cls.autoscale_client.delete_scaling_group)
        policy_resp = cls.autoscale_provider.create_policy_min(cls.group.id)
        cls.policy = cls.autoscale_provider.get_policy_properties(policy_resp.entity)

    @classmethod
    def tearDownClass(cls):
        super(ScalingWebhooksNegative, cls).tearDownClass()

    @unittest.skip('invalid when tests are running in parallel')
    def test_webhooks_nonexistant(self):
        list_webhooks_resp = self.autoscale_client.list_webhooks(self.group.id, self.policy["id"])
        list_webhooks = list_webhooks_resp.entity
        self.assertEquals(list_webhooks_resp.status_code, 200,
                          msg="List webhooks failed with %s"
                          % list_webhooks_resp.status_code)
        self.validate_headers(list_webhooks_resp.headers)
        self.assertEquals(list_webhooks, [],
                          msg="Some webhooks already exist on the scaling policy")

    def test_webhook_name_blank(self):
        '''
        Negative Test: Webhooks should not get created with an empty
        name
        '''
        expected_status_code = HttpStatusCodes.BAD_REQUEST
        error_create_resp = self.autoscale_client.create_webhook(group_id=self.group.id,
                                                                 policy_id=self.policy["id"],
                                                                 name='')
        create_error = error_create_resp.entity
        self.assertEquals(error_create_resp.status_code, expected_status_code,
                          msg="Create webhooks succeeded with invalid request: %s"
                          % error_create_resp.status_code)
        self.assertTrue(create_error is None,
                        msg="Create webhooks with invalid request returned: %s"
                        % create_error)

    def test_webhooks_name_whitespace(self):
        '''
        Negative Test: Webhooks should not get created with
        name as whitespace
        '''
        expected_status_code = HttpStatusCodes.BAD_REQUEST
        error_create_resp = self.autoscale_client.create_webhook(group_id=self.group.id,
                                                                 policy_id=self.policy["id"],
                                                                 name='')
        create_error = error_create_resp.entity
        self.assertEquals(error_create_resp.status_code, expected_status_code,
                          msg="Create webhooks succeeded with invalid request: %s"
                          % error_create_resp.status_code)
        self.assertTrue(create_error is None,
                        msg="Create webhooks with invalid request returned: %s"
                        % create_error)

    def test_get_invalid_webhook_id(self):
        '''
        Negative Test: Get Webhooks with invalid webhook id should fail with
        resource not found 404
        '''
        webhook = 13344
        expected_status_code = HttpStatusCodes.NOT_FOUND
        error_create_resp = self.autoscale_client.get_webhook(group_id=self.group.id,
                                                              policy_id=self.policy["id"],
                                                              webhook_id=webhook)
        create_error = error_create_resp.entity
        self.assertEquals(error_create_resp.status_code, expected_status_code,
                          msg="Create webhooks succeeded with invalid request: %s"
                          % error_create_resp.status_code)
        self.assertTrue(create_error is None,
                        msg="Create webhooks with invalid request returned: %s"
                        % create_error)

    def test_update_invalid_webhook_id(self):
        '''
        Negative Test: Update Webhooks with invalid webhook id should fail with
        resource not found 404
        '''
        webhook = 13344
        expected_status_code = HttpStatusCodes.NOT_FOUND
        error_create_resp = self.autoscale_client.update_webhook(group_id=self.group.id,
                                                                 policy_id=self.policy["id"],
                                                                 webhook_id=webhook,
                                                                 name=self.wb_name)
        create_error = error_create_resp.entity
        self.assertEquals(error_create_resp.status_code, expected_status_code,
                          msg="Create webhooks succeeded with invalid request: %s"
                          % error_create_resp.status_code)
        self.assertTrue(create_error is None,
                        msg="Create webhooks with invalid request returned: %s"
                        % create_error)

    def test_get_webhook_after_deletion(self):
        '''
        Negative Test: Get webhook when webhook is deleted should fail with
        resource not found 404
        '''
        create_resp = self.autoscale_client.create_webhook(group_id=self.group.id,
                                                           policy_id=self.policy["id"], name=self.wb_name)
        webhook = self.autoscale_provider.get_webhooks_properties(create_resp.entity)
        del_resp = self.autoscale_client.delete_webhook(group_id=self.group.id,
                                                        policy_id=self.policy["id"], webhook_id=webhook["id"])
        self.assertEquals(create_resp.status_code, 201, msg="create webhook failed")
        self.assertEquals(del_resp.status_code, 204, msg="Delete webhook failed")
        expected_status_code = HttpStatusCodes.NOT_FOUND
        error_create_resp = self.autoscale_client.get_webhook(group_id=self.group.id,
                                                              policy_id=self.policy["id"],
                                                              webhook_id=webhook["id"])
        create_error = error_create_resp.entity
        self.assertEquals(error_create_resp.status_code, expected_status_code,
                          msg="Create webhooks succeeded with invalid request: %s"
                          % error_create_resp.status_code)
        self.assertTrue(create_error is None,
                        msg="Create webhooks with invalid request returned: %s"
                        % create_error)

    def test_update_webhook_after_deletion(self):
        '''
        Negative Test: Update webhook when webhook is deleted should fail with
        resource not found 404
        '''
        create_resp = self.autoscale_client.create_webhook(group_id=self.group.id,
                                                           policy_id=self.policy["id"], name=self.wb_name)
        webhook = self.autoscale_provider.get_webhooks_properties(create_resp.entity)
        del_resp = self.autoscale_client.delete_webhook(group_id=self.group.id,
                                                        policy_id=self.policy["id"], webhook_id=webhook["id"])
        self.assertEquals(create_resp.status_code, 201, msg="create webhook failed")
        self.assertEquals(del_resp.status_code, 204, msg="Delete webhook failed")
        expected_status_code = HttpStatusCodes.NOT_FOUND
        error_create_resp = self.autoscale_client.update_webhook(group_id=self.group.id,
                                                                 policy_id=self.policy["id"],
                                                                 webhook_id=webhook["id"],
                                                                 name=self.wb_name)
        create_error = error_create_resp.entity
        self.assertEquals(error_create_resp.status_code, expected_status_code,
                          msg="Create webhooks succeeded with invalid request: %s"
                          % error_create_resp.status_code)
        self.assertTrue(create_error is None,
                        msg="Create webhooks with invalid request returned: %s"
                        % create_error)

    def test_execute_invalid_version_webhook(self):

        create_resp = self.autoscale_client.create_webhook(group_id=self.group.id,
                                                           policy_id=self.policy["id"],
                                                           name=self.wb_name)
        webhook = self.autoscale_provider.get_webhooks_properties(create_resp.entity)
        self.assertEquals(create_resp.status_code, 201, msg="create webhook failed")
        cap_url = webhook['links'].capability
        env = os.environ['CLOUDCAFE_TEST_CONFIG']
        if "dev" in env.lower():
            cap_url = (str(cap_url))[:16] + ':9000' +\
                (str(cap_url))[16:]
            invalid_cap_url = (str(cap_url))[:35] + '10' +\
                (str(cap_url))[35:]
        else:
            invalid_cap_url = (str(cap_url))[:30] + '10' +\
                (str(cap_url))[30:]
        execute_wb_resp = self.autoscale_client.execute_webhook(invalid_cap_url)
        self.assertEquals(execute_wb_resp.status_code, 202,
                          msg="Execute webhook did not fail. Response: %s"
                          % execute_wb_resp.status_code)

    def test_execute_nonexistant_webhook(self):
        create_resp = self.autoscale_client.create_webhook(group_id=self.group.id,
                                                           policy_id=self.policy["id"],
                                                           name=self.wb_name)
        webhook = self.autoscale_provider.get_webhooks_properties(create_resp.entity)
        self.assertEquals(create_resp.status_code, 201, msg="create webhook failed")
        cap_url = webhook['links'].capability
        env = os.environ['CLOUDCAFE_TEST_CONFIG']
        if "dev" in env.lower():
            cap_url = (str(cap_url))[:16] + ':9000' +\
                (str(cap_url))[16:]
        invalid_cap_url = (str(cap_url))[:45] + 'INVALIDATE' +\
            (str(cap_url))[45:]
        execute_wb_resp = self.autoscale_client.execute_webhook(invalid_cap_url)
        self.assertEquals(execute_wb_resp.status_code, 202,
                          msg="Execute webhook did not fail. Response: %s"
                              % execute_wb_resp.status_code)

    def test_execute_webhook_after_deletion(self):
        create_resp = self.autoscale_client.create_webhook(group_id=self.group.id,
                                                           policy_id=self.policy["id"],
                                                           name=self.wb_name)
        webhook = self.autoscale_provider.get_webhooks_properties(create_resp.entity)
        cap_url = webhook['links'].capability
        env = os.environ['CLOUDCAFE_TEST_CONFIG']
        if "dev" in env.lower():
            cap_url = (str(cap_url))[:16] + ':9000' +\
                (str(cap_url))[16:]
        del_resp = self.autoscale_client.delete_webhook(group_id=self.group.id,
                                                        policy_id=self.policy["id"],
                                                        webhook_id=webhook["id"])
        self.assertEquals(create_resp.status_code, 201, msg="create webhook failed")
        self.assertEquals(del_resp.status_code, 204, msg="Delete webhook failed")
        execute_wb_resp = self.autoscale_client.execute_webhook(cap_url)
        self.assertEquals(execute_wb_resp.status_code, 202,
                          msg="Execute webhook failed with %s"
                          % execute_wb_resp.status_code)

import re, os, unittest2 as unittest
from urlparse import urlparse

from testrepo.common.testfixtures.autoscale import AutoscaleFixture


class AutoscalingLinksTest(AutoscaleFixture):
    # Has set the port to 9000 in the links if the environment is 'dev'

    @classmethod
    def setUpClass(cls):
        super(AutoscalingLinksTest, cls).setUpClass()
        create_resp = cls.autoscale_provider.create_scaling_group_min()
        cls.group = create_resp.entity
        cls.resources.add(cls.group.id,
                          cls.autoscale_client.delete_scaling_group)
        cls.policy_resp = cls.autoscale_provider.create_policy_min(cls.group.id)
        cls.policy = cls.autoscale_provider.get_policy_properties(
            cls.policy_resp.entity)
        cls.webhook_resp = cls.autoscale_client.create_webhook(
            group_id=cls.group.id,
            policy_id=cls.policy["id"],
            name=cls.wb_name)
        cls.webhook = cls.autoscale_provider.get_webhooks_properties(
            cls.webhook_resp.entity)

    @classmethod
    def tearDownClass(cls):
        super(AutoscalingLinksTest, cls).tearDownClass()

    def test_scaling_group_links(self):
        '''
        Verify that scaling groups has links for self and bookmark
        '''
        self.assertTrue(self.group.links is not None,
                        msg="No links returned upon scaling group creation")
        #Issue AUTO-209
        # self.assertTrue(self.group.id in self.group.links.bookmark,
        #                 msg="The Group ID does not exit in the Links")
        self.assertTrue(self.group.id in self.group.links.self,
                        msg="The Group ID does not exit in the Links")

    @unittest.skip('view manifest not implemented yet')
    def test_scaling_group_self_link(self):
        '''
        Verify that scaling groups self link is a full url with a version
        '''
        group_self_link = self.group.links.self
        self.assertTrue(self._has_version(group_self_link))
        env = os.environ['CLOUDCAFE_TEST_CONFIG']
        if "dev" in env.lower():
            group_self_link = (str(group_self_link))[:16] + ':9000' +\
                (str(group_self_link))[16:]
        get_group_resp = self.autoscale_client.\
            view_manifest_config_for_scaling_group(group_self_link)
        self.assertEqual(self.group.id, get_group_resp.entity.id)

    def test_scaling_policy_links(self):
        '''
        Verify that scaling policy has links for self and bookmark
        '''
        policy_links = self.policy['links']
        self.assertTrue(self.policy['links'] is not None,
                        msg="No links returned upon scaling policy creation")
        #Issue AUTO-209
        # self.assertTrue(self.policy['id'] in policy_links.bookmark,
        #                 msg="The Policy ID does not exit in the Links")
        self.assertTrue(self.policy['id'] in policy_links.self,
                        msg="The Policy ID does not exit in the Links")

    def test_scaling_policy_self_link(self):
        '''
        Verify that scaling policy self link is a full url with a version
        '''
        policy_self_link = self.policy['links'].self
        self.assertTrue(self._has_version(policy_self_link))
        env = os.environ['CLOUDCAFE_TEST_CONFIG']
        if "dev" in env.lower():
            policy_self_link = (str(policy_self_link))[:16] + ':9000' +\
                (str(policy_self_link))[16:]
        get_policy_resp = self.autoscale_client.get_policy_details(
            self.group.id, policy_self_link)
        self.assertEqual(self.policy["id"], (get_policy_resp.entity).id)

    def test_webhook_links(self):
        '''
        Verify that webhook has links for self and bookmark
        '''
        webhook_links = self.webhook['links']
        self.assertTrue(self.webhook['links'] is not None,
                        msg="No links returned upon webhook creation")
        #Issue AUTO-209
        # self.assertTrue(self.webhook['id'] in webhook_links.bookmark,
        #                 msg="The webhook ID does not exit in the Links")
        self.assertTrue(self.webhook['id'] in webhook_links.self,
                        msg="The webhook ID does not exit in the Links")

    def test_webhook_self_link(self):
        '''
        Verify that webhooks self link is a full url with a version
        '''
        webhook_self_link = self.webhook['links'].self
        self.assertTrue(self._has_version(webhook_self_link))
        env = os.environ['CLOUDCAFE_TEST_CONFIG']
        if "dev" in env.lower():
            webhook_self_link = (str(webhook_self_link))[:16] + ':9000' +\
                (str(webhook_self_link))[16:]
        get_webhook_resp = self.autoscale_client.get_webhook(
            self.group.id, self.policy["id"], webhook_self_link)
        self.assertEqual(self.webhook["id"], (get_webhook_resp.entity).id)

    def test_webhook_capability_link(self):
        '''
        Verify that webhooks capability link is a full url with a version
        '''
        webhook_capability_link = self.webhook['links'].capability
        self.assertTrue(self._has_version(webhook_capability_link))

    def _has_version(self, link):
        return re.search('^/v+\d', urlparse(link).path) is not None

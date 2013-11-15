from testrepo.common.testfixtures.identity.v2_0.identity \
    import IdentityAdminFixture
from ccengine.common.decorators import attr
from ccengine.common.tools.datagen import rand_name
from unittest2 import skip


class AdminPoliciesTest(IdentityAdminFixture):
    @classmethod
    def setUpClass(cls):
        super(AdminPoliciesTest, cls).setUpClass()
        cls.blob = ('{context_is_admin: [[role:admin]],admin_or_owner:'
                    '[[is_admin:True], [project_id:%(project_id)s]],default: '
                    '[[rule:admin_or_owner]]}')
        cls.enabled = True
        cls.description = 'Static descr policy'
        cls.policy_name = rand_name("ccpolname")
        cls.global_ = False
        cls.type = 'nova-json-policy-format'
        cls.upd_name = rand_name("ccpolnameupd")
        cls.upd_enabled = False

    @classmethod
    def tearDownClass(cls):
        pass

    @attr('smoke', type='positive')
    def test_get_all_policies(self):
        get_policies = self.admin_client.get_policies()

        self.assertEqual(get_policies.status_code, 200,
                         msg="Admin get all policies expected response "
                             "200 received %s" % get_policies.status_code)

    @attr('smoke', type='positive')
    def test_create_policy(self):
        create_policy = self.admin_client.create_policy(
            name=self.policy_name,
            description=self.description,
            blob=self.blob,
            enabled=self.enabled,
            global_=self.global_,
            type=self.type)

        self.assertEqual(create_policy.status_code, 201,
                         msg="Admin create policy expected response "
                             "201 received %s" % create_policy.status_code)

        policy_id = create_policy.headers['location'].split('/')[-1]

        self.addCleanup(self.admin_client.delete_policy, policy_id=policy_id)

    @attr('smoke', type='positive')
    def test_get_a_policy(self):
        create_policy = self.admin_client.create_policy(
            name=self.policy_name,
            description=self.description,
            blob=self.blob,
            enabled=self.enabled,
            global_=self.global_,
            type=self.type)

        policy_id = create_policy.headers['location'].split('/')[-1]

        get_policies = self.admin_client.get_policies()

        self.assertEqual(get_policies.status_code, 200,
                         msg="Admin get policies expected response 200 "
                             "received %s" % get_policies.status_code)

        get_policy = self.admin_client.get_policy(
            policy_id=get_policies.entity[0].id)

        self.assertEqual(get_policy.status_code, 200,
                         msg="Admin get policy expected response 200 "
                             "received %s" % get_policy.status_code)

        self.addCleanup(self.admin_client.delete_policy, policy_id=policy_id)

    @attr('smoke', type='positive')
    def test_update_policy(self):
        create_policy = self.admin_client.create_policy(
            name=self.policy_name,
            description=self.description,
            blob=self.blob,
            enabled=self.enabled,
            global_=self.global_,
            type=self.type)

        self.assertEqual(create_policy.status_code, 201,
                         msg="Admin create policy expected response 201 "
                             "received %s" % create_policy.status_code)

        policy_id = create_policy.headers['location'].split('/')[-1]

        update_policy = self.admin_client.update_policy(
            policy_id=policy_id,
            name=self.upd_name,
            description=self.description,
            blob=self.blob,
            enabled=self.upd_enabled,
            global_=self.global_,
            type=self.type)

        self.assertEqual(update_policy.status_code, 204,
                         msg="Admin update policy expected response 204 "
                             "received %s" % update_policy.status_code)

        self.addCleanup(self.admin_client.delete_policy, policy_id=policy_id)

    @attr('smoke', type='positive')
    def test_delete_policy(self):
        create_policy = self.admin_client.create_policy(
            name=self.policy_name,
            description=self.description,
            blob=self.blob,
            enabled=self.enabled,
            global_=self.global_,
            type=self.type)

        self.assertEqual(create_policy.status_code, 201,
                         msg="Admin create policy expected response 201 "
                             "received %s" % create_policy.status_code)

        policy_id = create_policy.headers['location'].split('/')[-1]

        delete_policy = self.admin_client.delete_policy(
            policy_id=policy_id)

        self.assertEqual(delete_policy.status_code, 204,
                         msg="Admin delete policy expected response 204 "
                             "received %s" % delete_policy.status_code)

    @skip("WIP:>>> G.A. is still working on this method")
    @attr('smoke', type='positive')
    def test_get_detailed_policy_content(self):
        get_policies = self.admin_client.get_policies()

        self.assertEqual(get_policies.status_code, 200,
                         msg="Admin get policies expected response 200 "
                             "received %s" % get_policies.status_code)

        policy_detail = self.admin_client.get_detailed_policy_content(
            policy_id=get_policies.entity[-1].id)

        self.assertEqual(policy_detail.status_code, 200,
                         msg="Admin get detailed policy content expected "
                             "response 200 received %s" %
                             policy_detail.status_code)

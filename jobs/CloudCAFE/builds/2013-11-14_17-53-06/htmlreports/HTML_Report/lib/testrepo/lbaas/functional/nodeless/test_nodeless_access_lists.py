from ccengine.common.decorators import attr
import testrepo.lbaas.functional.test_access_lists as lbaas_acl


class NodelessAccessSmokeTests(lbaas_acl.AccessListsSmokeTests):
    @classmethod
    def setUpClass(cls):
        super(NodelessAccessSmokeTests, cls).setUpClass()
        cls.original_lb = cls.lb
        cls.lb = cls.lbaas_provider.create_active_load_balancer(
            nodeless=True).entity
        cls.lbs_to_delete.append(cls.lb.id)

    @attr('positive', 'nodeless')
    def test_nodeless_add_remove_access_lists(self):
        return self.test_add_remove_access_list()


class NodelessAccessListsTests(lbaas_acl.AccessListsTests):
    @classmethod
    def setUpClass(cls):
        super(NodelessAccessListsTests, cls).setUpClass()
        cls.original_lb = cls.lb
        cls.lb = cls.lbaas_provider.create_active_load_balancer(
            nodeless=True).entity
        cls.zeus_vs_name = '_'.join([str(cls.tenant_id), str(cls.lb.id)])
        cls.lbs_to_delete.append(cls.lb.id)

    @attr('nodeless')
    def test_nodeless_batch_delete_access_list(self):
        return self.test_batch_delete_access_list()

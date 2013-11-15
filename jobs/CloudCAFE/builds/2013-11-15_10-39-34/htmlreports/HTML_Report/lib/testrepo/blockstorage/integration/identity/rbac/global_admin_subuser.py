from ccengine.common.decorators import attr
from testrepo.common.testfixtures.blockstorage import identity_integration as \
    rbac_fixtures


class RBAC_CBS_SubUser_GlobalAdminRole(
        rbac_fixtures.RBAC_CBS_SubUserTestFixture):
    @classmethod
    def setUpClass(cls):
        super(RBAC_CBS_SubUser_GlobalAdminRole, cls).setUpClass()

        #Role Setup
        role_under_test = cls.get_role(
            cls.main_test_user.client,
            cls.actual_test_user.id,
            cls.GLOBAL_ADMIN)

        cls.add_role_to_sub_user(
            cls.main_test_user.client,
            cls.actual_test_user,
            role_under_test.id)

        default_result = cls.ExpectedResult(expected_status_code_range=200)

        cls.EXPECTED_RESULTS = {
            "volume_extension:types_manage": default_result,
            "volume_extension:types_extra_specs": default_result,
            "volume_extension:quotas:update_for_project": default_result,
            "volume_extension:volume_admin_actions:reset_status":
            default_result,
            "volume_extension:snapshot_admin_actions:reset_status":
            default_result,
            "volume_extension:volume_admin_actions:force_delete":
            default_result,
            "volume_extension:snapshot_admin_actions:force_delete":
            default_result,
            "volume_extension:volume_host_attribute": default_result,
            "volume_extension:volume_tenant_attribute": default_result,
            "volume_extension:extended_snapshot_attributes": default_result,
            "volume_extension:quotas:show": default_result,
            "volume_extension:quotas:update_for_user": default_result,
            "volume_extension:quota_classes": default_result,
            "volume:delete": default_result,
            "volume:update": default_result,
            "volume:check_detach": default_result,
            "volume:unreserve_volume": default_result,
            "volume:begin_detaching": default_result,
            "volume:roll_detaching": default_result,
            "volume:detach": default_result,
            "volume:terminate_connection": default_result,
            "volume:delete_snapshot": default_result,
            "volume:update_snapshot": default_result,
            "volume:delete_volume_metadata": default_result,
            "volume:update_volume_metadata": default_result,

            "volume:create": default_result,
            "volume:check_attach": default_result,
            "volume:reserve_volume": default_result,
            "volume:attach": default_result,
            "volume:initialize_connection": default_result,
            "volume:create_snapshot": default_result,
            "volume:copy_volume_to_image": default_result,

            "volume:get": default_result,
            "volume:get_all": default_result,
            "volume:get_snapshot": default_result,
            "volume:get_volume": default_result,
            "volume:get_all_snapshots": default_result,
            "volume:get_volume_metadata": default_result,
            "volume:get_volume_image_metadata": default_result}

    @attr('smoke')
    def test_actual_test_user_is_global_admin(self):
        self.assert_actual_test_user_has_role(self.GLOBAL_ADMIN)

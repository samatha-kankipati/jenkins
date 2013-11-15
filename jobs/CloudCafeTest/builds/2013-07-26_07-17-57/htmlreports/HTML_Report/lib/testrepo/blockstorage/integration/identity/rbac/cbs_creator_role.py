from ccengine.common.decorators import attr
from testrepo.common.testfixtures.blockstorage import identity_integration as \
    rbac_fixtures


class RBAC_CBS_SubUser_CBSCreatorRole(
        rbac_fixtures.RBAC_CBS_SubUserTestFixture):
    @classmethod
    def setUpClass(cls):
        super(RBAC_CBS_SubUser_CBSCreatorRole, cls).setUpClass()

        #Role Setup
        role_under_test = cls.get_role(
            cls.main_test_user.client,
            cls.actual_test_user.id,
            cls.CBS_CREATOR)

        cls.add_role_to_sub_user(
            cls.main_test_user.client,
            cls.actual_test_user,
            role_under_test.id)

        default_result = cls.ExpectedResult(expected_status_code_range=200)
        negative_result = cls.ExpectedResult(expected_status_code=403)

        cls.EXPECTED_RESULTS = {
            "volume_extension:types_manage": negative_result,
            "volume_extension:types_extra_specs": negative_result,
            "volume_extension:quotas:update_for_project": negative_result,
            "volume_extension:volume_admin_actions:reset_status":
            negative_result,
            "volume_extension:snapshot_admin_actions:reset_status":
            negative_result,
            "volume_extension:volume_admin_actions:force_delete":
            negative_result,
            "volume_extension:snapshot_admin_actions:force_delete":
            negative_result,
            "volume_extension:volume_host_attribute": negative_result,
            "volume_extension:volume_tenant_attribute": negative_result,
            "volume_extension:extended_snapshot_attributes": negative_result,
            "volume_extension:quotas:show": negative_result,
            "volume_extension:quotas:update_for_user": negative_result,
            "volume_extension:quota_classes": negative_result,
            "volume:delete": negative_result,
            "volume:update": negative_result,
            "volume:check_detach": negative_result,
            "volume:unreserve_volume": negative_result,
            "volume:begin_detaching": negative_result,
            "volume:roll_detaching": negative_result,
            "volume:detach": negative_result,
            "volume:terminate_connection": negative_result,
            "volume:delete_snapshot": negative_result,
            "volume:update_snapshot": negative_result,
            "volume:delete_volume_metadata": negative_result,
            "volume:update_volume_metadata": negative_result,

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
    def test_actual_test_user_is_cbs_creator(self):
        self.assert_actual_test_user_has_role(self.CBS_CREATOR)

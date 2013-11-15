from ccengine.common.decorators import attr
from testrepo.common.testfixtures.blockstorage import identity_integration as \
    rbac_fixtures


class RBAC_CBS_SubUser_IdentityDefaultRole(
        rbac_fixtures.RBAC_CBS_SubUserTestFixture):
    IDENTITY_DEFAULT = "identity:default"

    @classmethod
    def setUpClass(cls):
        super(RBAC_CBS_SubUser_IdentityDefaultRole, cls).setUpClass()

        ##Role Setup
        #Don't add any roles to the user

        #default_result = cls.ExpectedResult(expected_status_code_range=200)
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

            "volume:create": negative_result,
            "volume:check_attach": negative_result,
            "volume:reserve_volume": negative_result,
            "volume:attach": negative_result,
            "volume:initialize_connection": negative_result,
            "volume:create_snapshot": negative_result,
            "volume:copy_volume_to_image": negative_result,

            "volume:get": negative_result,
            "volume:get_all": negative_result,
            "volume:get_snapshot": negative_result,
            "volume:get_volume": negative_result,
            "volume:get_all_snapshots": negative_result,
            "volume:get_volume_metadata": negative_result,
            "volume:get_volume_image_metadata": negative_result}

    @attr('smoke')
    def test_actual_test_user_is_identity_default_role(self):
        self.assert_actual_test_user_has_role(self.IDENTITY_DEFAULT)

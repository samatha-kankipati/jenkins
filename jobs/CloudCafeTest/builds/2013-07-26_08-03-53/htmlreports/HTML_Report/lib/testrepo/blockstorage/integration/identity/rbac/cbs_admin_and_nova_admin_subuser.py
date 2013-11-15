from ccengine.common.decorators import attr
from ccengine.providers.blockstorage.volumes_api import VolumesAPIProvider
from ccengine.providers.blockstorage.lunr_api import LunrAPIProvider
from ccengine.providers.compute.volume_attachments_api import \
    VolumeAttachmentsAPIProvider
from ccengine.providers.compute.compute_api import ComputeAPIProvider
from testrepo.common.testfixtures.blockstorage import identity_integration as \
    rbac_fixtures


class RBAC_CBS_SubUser_CBSAdmin_and_NovaAdminRoles(
        rbac_fixtures.RBAC_CBS_SubUserTestFixture):
    NOVA_ADMIN = 'nova:admin'

    @classmethod
    def setUpClass(cls):
        super(RBAC_CBS_SubUser_CBSAdmin_and_NovaAdminRoles, cls).setUpClass()

        #Setup main user providers using actual user credentials
        #Allow the user under test to preform its own setup.
        main_test_user_config_override ={
            "identity": {
                "username": cls.actual_test_user.username,
                "password": cls.actual_test_user.password}}

        main_test_user_mcp = cls.config.mcp_override(
            main_test_user_config_override)

        cls.main_test_user_volumes_provider = VolumesAPIProvider(
            main_test_user_mcp)

        cls.main_test_user_lunr_provider = LunrAPIProvider(
            main_test_user_mcp.lunr_api)

        cls.main_test_user_vol_attach_provider = VolumeAttachmentsAPIProvider(
            main_test_user_mcp)

        cls.main_test_user_compute_provider = ComputeAPIProvider(
            main_test_user_mcp)

        #Role Setup
        nova_role_under_test = cls.get_role(
            cls.main_test_user.client,
            cls.actual_test_user.id,
            cls.NOVA_ADMIN)

        cbs_role_under_test = cls.get_role(
            cls.main_test_user.client,
            cls.actual_test_user.id,
            cls.CBS_ADMIN)

        cls.add_role_to_sub_user(
            cls.main_test_user.client,
            cls.actual_test_user,
            nova_role_under_test.id)

        cls.add_role_to_sub_user(
            cls.main_test_user.client,
            cls.actual_test_user,
            cbs_role_under_test.id)

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
    def test_actual_test_user_is_cbs_admin(self):
        self.assert_actual_test_user_has_role(self.CBS_ADMIN)

    @attr('smoke')
    def test_actual_test_user_is_nova_admin(self):
        self.assert_actual_test_user_has_role(self.NOVA_ADMIN)

    @attr('compute')
    def test_volume_attach(self):
        api_action_name = "volume:attach"
        server = self.setup_a_test_server(
            compute_provider=self.actual_test_user_compute_provider)

        volume = self.setup_a_test_volume(
            volumes_provider=self.actual_test_user_volumes_provider)

        resp = (self.actual_test_user_vol_attach_provider.client.attach_volume(
            server.id, volume.id))

        self.assert_result(api_action_name, resp)

        attachment = resp.entity

        #Add cleanup
        self.addCleanup(
            self.actual_test_user_vol_attach_provider.detach_volume_confirmed,
            attachment.id, server.id)

        #Add additional cleanup using main user in case test user role
        #disallowes detaching
        self.addCleanup(
            self.main_test_user_vol_attach_provider.detach_volume_confirmed,
            attachment.id, server.id)

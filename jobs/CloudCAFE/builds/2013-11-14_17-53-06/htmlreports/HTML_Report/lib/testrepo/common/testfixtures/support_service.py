from ccengine.domain.configuration import AuthConfig
from ccengine.domain.types import HttpResponse
from ccengine.providers.configuration import MasterConfigProvider as _MCP
from ccengine.providers.support_services.support_service_api import\
    SupportServicesAPIProvider as _SupportServicesAPIProvider
from testrepo.common.testfixtures.fixtures import BaseParameterizedTestFixture


class SupportServicesFixture(BaseParameterizedTestFixture):

    @classmethod
    def setUpClass(cls):
        super(SupportServicesFixture, cls).setUpClass()
        mcp = _MCP()
        customer_auth_dict = {AuthConfig.SECTION_NAME: {
            'base_url': cls.config.auth.alt_url,
            'username': cls.config.auth.alt_username,
            'password': cls.config.auth.alt_password,
            'version': cls.config.auth.alt_version}}

        customer_config = cls.config.mcp_override(customer_auth_dict)

        cls.support_services_groups_provider = \
            _SupportServicesAPIProvider(cls.config, cls.fixture_log)

        cls.support_services_cutomer_provider = \
            _SupportServicesAPIProvider(customer_config, cls.fixture_log)

        cls.user = cls.config.auth.username

        cls.NOT_FOUND = HttpResponse.NOT_FOUND
        cls.OK_CODE = HttpResponse.OK
        cls.BAD_REQ_CODE = HttpResponse.BAD_REQUEST
        cls.UNAUTHORIZED_CODE = HttpResponse.UNAUTHORIZED
        cls.FORBIDDEN = HttpResponse.FORBIDDEN

        cls.account_number = cls.config.support_service.account_number
        cls.service_level = cls.config.support_service.service_level
        cls.account_info_racker = ["account_badges", "service_level",
                                   "roles", "teams"]
        cls.account_info_roles_attributes = ['user_id', 'user_badges', 'role',
                                             'user_sso', 'user_name']
        cls.account_info_teams_attributes = ['team_badges', 'team_id',
                                             'team_name', 'team_type']
        cls.account_info_badges_attributes = ['badge_description', 'badge_url',
                                              'badge_name']
        cls.linked_account = cls.config.support_service.linked_account
        cls.account_name = cls.config.support_service.account_name
        cls.team_id = cls.config.support_service.team_id
        cls.group_with_users = cls.config.support_service.group_with_users
        cls.user_id = cls.config.support_service.user_id
        cls.user_email = cls.config.support_service.user_email
        cls.user_name = cls.config.support_service.user_name
        cls.user_sso = cls.config.support_service.user_sso
        cls.user_tags = cls.config.support_service.user_tags

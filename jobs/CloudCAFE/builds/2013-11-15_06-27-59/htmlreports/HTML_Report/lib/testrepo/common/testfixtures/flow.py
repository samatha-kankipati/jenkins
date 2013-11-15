from ccengine.domain.configuration import AuthConfig
from ccengine.providers.flow.flow_api import FlowAPIProvider \
    as _FlowAPIProvider
from ccengine.providers.zendesk.zendesk_api import ZendeskAPIProvider \
    as _ZDProvider
from testrepo.common.testfixtures.fixtures import BaseTestFixture


class FlowFixture(BaseTestFixture):

    @classmethod
    def setUpClass(cls):
        super(FlowFixture, cls).setUpClass()
        cls.flow_provider = _FlowAPIProvider(cls.config)
        zd_dict = {AuthConfig.SECTION_NAME:
                   {'username': cls.config.auth.zendesk_user_name,
                    'password': cls.config.auth.zendesk_password,
                    'zendesk_ticket_url': cls.config.auth.
                    zendesk_ticket_url}}
        zd_config = cls.config.mcp_override(zd_dict)
        cls.zendesk_provider = _ZDProvider(zd_config)

        # Config values
        cls.testuser4_zd_id = cls.config.flow.testuser4_zd_id
        cls.zd_hybrid_int_smb_id = cls.config.flow.zd_hybrid_int_smb_id
        cls.flow_hybrid_int_smb_id = cls.config.flow.flow_hybrid_int_smb_id
        cls.testuser4_user_name = cls.config.flow.testuser4_user_name
        cls.testuser4_sso = cls.config.flow.testuser4_sso
        cls.wait_for_tickets = cls.config.flow.wait_for_tickets

    @classmethod
    def tearDownClass(cls):
        super(FlowFixture, cls).tearDownClass()


class TicketConst(object):

    severity_level_1 = 1
    zd_severity_urgent = 'urgent'
    core_severity_emergency = 'emergency'

    severity_level_2 = 2
    zd_severity_high = 'high'
    core_sevrity_urgent = 'urgent'

    severity_level_3 = 3
    zd_severity_normal = 'normal'
    core_severity_standard = 'standard'

    severity_level_4 = 4
    zd_severity_low = 'low'

    flow_state_active = 'active'
    zd_status_open = 'open'

    flow_state_pending = 'pending'
    zd_status_pending = 'pending'

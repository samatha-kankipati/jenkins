from testrepo.common.testfixtures.fixtures import BaseTestFixture
from ccengine.providers.tq_search.gate_api import GateAPIProvider \
    as _GateAPIProvider
from ccengine.providers.core.core_api import CoreAPIProvider \
    as _CoreAPIProvider
from ccengine.domain.configuration import AuthConfig
from ccengine.domain.configuration import TQSearchConfig
from ccengine.providers.tq_search.gate_api import AccountServicesProvider \
    as _AccountServicesProvider
from ccengine.providers.tq_search.gate_api import EasticSearchProvider \
    as _EasticSearchProvider
from ccengine.domain.configuration import MiscConfig


class TQSearchFixture(BaseTestFixture):

    @classmethod
    def setUpClass(cls):
        super(TQSearchFixture, cls).setUpClass()
        cls.start_time = cls.config.tq_search.start_time
        cls.end_time = cls.config.tq_search.end_time
        cls.end_time_1 = cls.config.tq_search.end_time_1
        cls.status_1 = cls.config.tq_search.status_1
        cls.status_2 = cls.config.tq_search.status_2
        cls.status_3 = cls.config.tq_search.status_3
        cls.status_type = cls.config.tq_search.status_type
        cls.priority_1 = cls.config.tq_search.priority_1
        cls.priority_3 = cls.config.tq_search.priority_3
        cls.account_number_1 = cls.config.tq_search.account_number_1
        cls.account_number_2 = cls.config.tq_search.account_number_2
        cls.account_number_3 = cls.config.tq_search.account_number_3
        cls.account_number_4 = cls.config.tq_search.account_number_4
        cls.queue_name = cls.config.tq_search.queue_name
        cls.utc_date_constant = cls.config.tq_search.utc_date_constant
        cls.content_type = cls.config.tq_search.content_type
        cls.utc_start_time = cls.config.tq_search.utc_start_time
        cls.utc_start_time_2 = cls.config.tq_search.utc_start_time_2
        cls.utc_end_time = cls.config.tq_search.utc_end_time
        cls.utc_end_time_1 = cls.config.tq_search.utc_end_time_1
        cls.tq_search_account_number_1 = cls.config.tq_search.tq_search_account_number_1
        cls.tq_search_account_number_2 = cls.config.tq_search.tq_search_account_number_2
        cls.tq_search_priority_1 = cls.config.tq_search.tq_search_priority_1
        cls.tq_search_priority_2 = cls.config.tq_search.tq_search_priority_2
        cls.start_time_1 = cls.config.tq_search.start_time_1
        cls.utc_start_time_2 = cls.config.tq_search.utc_start_time_2
        cls.utc_start_time_1 = cls.config.tq_search.utc_start_time_1
        cls.start_time_1 = cls.config.tq_search.start_time_1
        cls.start_time_2 = cls.config.tq_search.start_time_2
        cls.status_4 = cls.config.tq_search.status_4
        cls.queue_name_1 = cls.config.tq_search.queue_name_1
        cls.utc_start_time_1 = cls.config.tq_search.utc_start_time_1
        cls.elastic_search_url = cls.config.tq_search.elastic_search_url
        cls.account_type_1 = cls.config.tq_search.account_type_1
        cls.account_type_2 = cls.config.tq_search.account_type_2
        cls.team_name = cls.config.tq_search.team_name
        cls.sync_queue_id = cls.config.tq_search.sync_queue_id
        cls.sync_sub_category = cls.config.tq_search.sync_sub_category
        cls.sync_account_id = cls.config.tq_search.sync_account_id
        cls.sync_ticket_text = cls.config.tq_search.sync_ticket_text
        cls.sync_ticket_list = cls.config.tq_search.sync_ticket_list
        cls.sync_ticket_subject = cls.config.tq_search.sync_ticket_subject
        cls.sync_ticket_subject2 = cls.config.tq_search.sync_ticket_subject2
        cls.sync_source = cls.config.tq_search.sync_source
        cls.sync_severity = cls.config.tq_search.sync_severity
        cls.sync_account_id = cls.config.tq_search.sync_account_id
        cls.gate_provider = _GateAPIProvider(cls.config, cls.fixture_log)
        cls.core_attributes = ["number", "last_public_response_date",
                               "status.name", "created",
                               "modified", "priority.name", "category.name",
                               "queue.name", "queue.id",
                               "subject", "has_linux_servers",
                               "has_windows_servers", "subcategory.name",
                               "difficulty", "severity.name", "account.number",
                               "account.service_level_name",
                               "account.support_team.support_territory.code",
                               "assignee.name", "assignee.employee_userid",
                               "status.types.name"]
        cls.result_map = {
            "number": "number", "subject": "subject",
            "last_public_response_date": "last_public_response_date",
            "created": "created", "priority": "priority.id",
            "status.name": "status.name", "modified": "modified",
            "category.name": "category.name", "queue.name": "queue.name",
            "account.number": "account.number",
            "assignee.name": "assignee.name"}
        core_dict = {AuthConfig.SECTION_NAME: {'base_url':
                     cls.config.auth.core_auth_url, 'username':
                     cls.config.auth.core_username, 'password':
                     cls.config.auth.core_password, 'version':
                     cls.config.auth.core_version}}

        core_config = cls.config.mcp_override(core_dict)
        cls.core_provider = _CoreAPIProvider(config=core_config)
        as_dict = {MiscConfig.SECTION_NAME: {'serializer': 'xml',
                                             'deserializer': 'xml'}}
        as_config = cls.config.mcp_override(as_dict)
        cls.account_services_provider =\
            _AccountServicesProvider(as_config, cls.fixture_log)
        cls.elastic_search_provider =\
            _EasticSearchProvider(cls.config, cls.fixture_log)

    @classmethod
    def tearDownClass(cls):
        super(TQSearchFixture, cls).tearDownClass()

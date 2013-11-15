from ccengine.common.exception_handler.exception_handler import \
    ExceptionHandler
from ccengine.common.resource_manager.resource_pool import ResourcePool
from testrepo.common.testfixtures.fixtures import BaseTestFixture
from ccengine.common.tools.datagen import rand_name
from ccengine.domain.configuration import AuthConfig
from ccengine.providers.lefty.lefty_api import LeftyAPIProvider \
    as _LeftyAPIProvider


class LeftyFixture(BaseTestFixture):

    @classmethod
    def setUpClass(cls):
        super(LeftyFixture, cls).setUpClass()
        cls.resources = ResourcePool()
        cls.lefty_ticket_provider = _LeftyAPIProvider(cls.config,
                                                      cls.fixture_log)
        cls.user = cls.config.auth.username
        cls.account_id = cls.config.lefty.account_id

        cls.NOT_FOUND = ["404", "Not Found"]
        cls.OK_CODE = ["200", "OK"]
        cls.BAD_REQ_CODE = ["400", "Bad Request"]
        cls.attribute_list_on_events = ["on", "by", "ticket_id"]
        cls.attribute_list_on_pub_sub_events = ["by", "ticket_id"]        
        cls.expected_event_feed_keys = ["on", "by", "ticket_id", "category",
                                        "sub_category_id", "description",
                                        "subject", "sub_category",
                                        "category_id", "account_id"]

    @classmethod
    def tearDownClass(cls):
        super(LeftyFixture, cls).tearDownClass()

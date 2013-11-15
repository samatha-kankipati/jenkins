'''
@summary: Base Classes for Core Test Suites (Collections of Test Cases)
@note: Correspondes DIRECTLY TO A unittest.TestCase
@see: http://docs.python.org/library/unittest.html#unittest.TestCase
@copyright: Copyright (c) 2012 Rackspace US, Inc.
'''
from testrepo.common.testfixtures.fixtures import BaseTestFixture
from ccengine.providers.core.core_api import CoreAPIProvider \
                                                   as _CoreAPIProvider
from ccengine.common.resource_manager.resource_pool import ResourcePool


class CoreFixture(BaseTestFixture):
    '''
    @summary: Fixture for a CORE API test.
    '''
    @classmethod
    def setUpClass(cls):
        super(CoreFixture, cls).setUpClass()
        cls.resources = ResourcePool()
        cls.core_provider = _CoreAPIProvider(cls.config, cls.fixture_log)
        cls.ticket_client = cls.core_provider.ticket_client
        cls.queue_client = cls.core_provider.queue_client
        cls.core_client = cls.core_provider.core_client
        cls.contact_client = cls.core_provider.contact_client
        cls.account_client = cls.core_provider.account_client
        cls.contract_client = cls.core_provider.contract_client
        cls.computer_client = cls.core_provider.computer_client

    @classmethod
    def tearDownClass(cls):
        cls.resources.release()
        super(CoreFixture, cls).tearDownClass()

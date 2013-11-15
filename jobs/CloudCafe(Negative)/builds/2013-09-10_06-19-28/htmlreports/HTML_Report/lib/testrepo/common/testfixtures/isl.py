'''
@summary: Base Classes for Compute Test Suites (Collections of Test Cases)
@note: Correspondes DIRECTLY TO A unittest.TestCase
@see: http://docs.python.org/library/unittest.html#unittest.TestCase
@copyright: Copyright (c) 2012 Rackspace US, Inc.
'''
from testrepo.common.testfixtures.fixtures import BaseTestFixture
from ccengine.providers.isl.incident_api import IncidentAPIProvider \
                                                   as _IncidentAPIProvider
from ccengine.common.resource_manager.resource_pool import ResourcePool
from ccengine.domain.configuration import AuthConfig
from ccengine.common.tools.datagen import rand_name
from ccengine.common.exception_handler.exception_handler import ExceptionHandler

class ISLFixture(BaseTestFixture):
    '''
    @summary: Fixture for an ISL test.
    '''

    @classmethod
    def setUpClass(cls):
        super(ISLFixture, cls).setUpClass()
        cls.resources = ResourcePool()
        cls.incident_provider = _IncidentAPIProvider(cls.config, cls.fixture_log)

    @classmethod
    def tearDownClass(cls):
        super(ISLFixture, cls).tearDownClass()
        cls.resources.release()

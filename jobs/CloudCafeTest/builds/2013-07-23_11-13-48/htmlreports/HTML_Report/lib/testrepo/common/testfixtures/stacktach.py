'''
@summary: Base Classes for Test Suites (Collections of Test Cases)
@note: Correspondes DIRECTLY TO A unittest.TestCase
@see: http://docs.python.org/library/unittest.html#unittest.TestCase
@copyright: Copyright (c) 2013 Rackspace US, Inc.
'''
from testrepo.common.testfixtures.fixtures import BaseTestFixture
from ccengine.providers.stacktach.stacktach_provider import \
        StackTachProvider as _StackTachProvider
from ccengine.providers.stacktach.stacktachdb_provider import \
        StackTachDBProvider as _StackTachDBProvider
from ccengine.common.constants.stacktach_constants import Constants


class StackTachFixture(BaseTestFixture):
    '''
    @summary: Fixture for any StackTach test.
    '''
    @classmethod
    def setUpClass(cls):
        super(StackTachFixture, cls).setUpClass()
        #init providers
        cls.stacktach_provider = _StackTachProvider(cls.config,
                                                    cls.fixture_log)
        cls.event_id = str(cls.config.stacktach.event_id)
        cls.days_passed = int(cls.config.stacktach.days_passed)
        cls.msg = Constants.MESSAGE

    @classmethod
    def tearDownClass(cls):
        super(StackTachFixture, cls).tearDownClass()


class StackTachDBFixture(BaseTestFixture):
    '''
    @summary: Fixture for any StackTachDB test.
    '''
    @classmethod
    def setUpClass(cls):
        super(StackTachDBFixture, cls).setUpClass()
        #init providers
        cls.stacktachdb_provider = _StackTachDBProvider(cls.config,
                                                        cls.fixture_log)
        cls.event_id = str(cls.config.stacktach.event_id)
        cls.days_passed = int(cls.config.stacktach.days_passed)
        cls.msg = Constants.MESSAGE

    @classmethod
    def tearDownClass(cls):
        super(StackTachDBFixture, cls).tearDownClass()

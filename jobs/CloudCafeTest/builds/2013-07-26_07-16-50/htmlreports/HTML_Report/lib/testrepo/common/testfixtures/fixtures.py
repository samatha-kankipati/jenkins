'''
@summary: Base Classes for Test Suites (Collections of Test Cases)
@note: Correspondes DIRECTLY TO A unittest.TestCase
@see: http://docs.python.org/library/unittest.html#unittest.TestCase
@copyright: Copyright (c) 2012 Rackspace US, Inc.
'''
import unittest2 as unittest
from datetime import datetime

from ccengine.providers.configuration import MasterConfigProvider as _MCP
from ccengine.common.tools import logging_tools


class BaseTestFixture(unittest.TestCase):
    '''
    @summary: Foundation for TestRepo Test Fixture.
    @note: This is the base class for ALL test cases in TestRepo. Add new
           functionality carefully.
    @see: http://docs.python.org/library/unittest.html#unittest.TestCase
    '''
    @classmethod
    def assertClassSetupFailure(cls, message):
        '''
        @summary: Use this if you need to fail from a Test Fixture's
                  setUpClass() method
        '''
        cls.fixture_log.error("FATAL: %s:%s" % (cls.__name__, message))
        raise AssertionError("FATAL: %s:%s" % (cls.__name__, message))

    @classmethod
    def assertClassTeardownFailure(cls, message):
        '''
        @summary: Use this if you need to fail from a Test Fixture's
                  tearUpClass() method
        '''
        cls.fixture_log.error("FATAL: %s:%s" % (cls.__name__, message))
        raise AssertionError("FATAL: %s:%s" % (cls.__name__, message))

    @classmethod
    def setUpClass(cls):
        super(BaseTestFixture, cls).setUpClass()

        #Master Config Provider
        cls.config = _MCP()

        #Setup root log handler only if the root logger doesn't already haves
        if logging_tools.getLogger('').handlers == []:
            logging_tools.getLogger('').addHandler(
                    logging_tools.setup_new_cchandler('cc.master'))

        #Setup fixture log, which is really just a copy of the master log
        #for the duration of this test fixture
        cls.fixture_log = logging_tools.getLogger('')
        cls._fixture_log_handler = logging_tools.setup_new_cchandler(
                logging_tools.get_object_namespace(cls))
        cls.fixture_log.addHandler(cls._fixture_log_handler)

        #Init Log Test
        cls.fixture_log.debug("\n{0}\n{1} {2} at {3}\n{0}".format('=' * 56,
            'SETTING UP', str(logging_tools.get_object_namespace(cls)),
            datetime.now()))

    @classmethod
    def tearDownClass(cls):
        cls.fixture_log.debug("\n{0}\n{1} {2} at {3}\n{0}".format(
                '=' * 56, 'TEARING DOWN', cls.__name__, datetime.now()))

        #Remove the fixture log handler from the fixture log
        cls.fixture_log.removeHandler(cls._fixture_log_handler)

        #Call super teardown after we've finished out additions to teardown
        super(BaseTestFixture, cls).tearDownClass()

    def setUp(self):
        self.fixture_log.debug("\n{0}\n{1} {2} at {3}\n{0}".format(
                '=' * 56, self._testMethodName, 'STARTING', datetime.now()))
        unittest.TestCase.setUp(self)

    def tearDown(self):
        unittest.TestCase.tearDown(self)
        self.fixture_log.debug("\n{0}\n{1} {2} at {3}\n{0}".format(
                '=' * 56, self._testMethodName, 'COMPLETED', datetime.now()))


class BaseParameterizedTestFixture(BaseTestFixture):
    """ TestCase classes that want to be parametrized should
        inherit from this class.
    """
    def __copy__(self):
        new_copy = self.__class__(self._testMethodName)
        for key in self.__dict__.keys():
            new_copy.key = self.__dict__[key]
        return new_copy

    def setUp(self):
        self.fixture_log.debug("\n{0}\n{1} {2} at {3}\n{0}".format(
                '=' * 56, self.__dict__, 'STARTING', datetime.now()))
        unittest.TestCase.setUp(self)

    def tearDown(self):
        unittest.TestCase.tearDown(self)
        self.fixture_log.debug("\n{0}\n{1} {2} at {3}\n{0}".format(
                '=' * 56, self.__dict__, 'COMPLETED', datetime.now()))

    def __str__(self):
        if "test_record" in self.__dict__:
            return self._testMethodName + " " + str(self.test_record)
        else:
            return super(BaseParameterizedTestFixture, self).__str__()

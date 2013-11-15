'''
@summary: Base Classes for Test Suites (Collections of Test Cases)
@note: Correspondes DIRECTLY TO A unittest.TestCase
@see: http://docs.python.org/library/unittest.html#unittest.TestCase
@copyright: Copyright (c) 2012 Rackspace US, Inc.
'''
from testrepo.common.testfixtures.fixtures import BaseTestFixture
from ccengine.providers.checkmate.checkmate_api import CheckamteProvider \
                                                    as _CheckMateProvider

class CheckmateFixture(BaseTestFixture):
    '''
    @summary: Fixture for any Isolated Networks test..
    '''
    @classmethod
    def setUpClass(cls):
        super(CheckmateFixture, cls).setUpClass()
        #init providers
        cls.checkmate_provider = _CheckMateProvider(cls.config, cls.fixture_log)

    @classmethod
    def tearDownClass(cls):
        super(CheckmateFixture, cls).tearDownClass()

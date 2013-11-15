'''
@summary: Types that could used by all test case infrastructures
@copyright: Copyright (c) 2012 Rackspace US, Inc.
'''

class TestResultTypes():
    '''
    @summary: Types dictating an individual Test Case result
    @cvar PASSED: Test has passed
    @type PASSED: C{str}
    @cvar FAILED: Test has failed
    @type FAILED: C{str}
    @cvar ABORTED: Test was stopped or crashed
    @type ABORTED: C{str}
    @cvar TIMEDOUT: Test exceeded pre-defined execution time limit   
    @type TIMEDOUT: C{str}
    @note: This is essentially an Enumerated Type
    '''
    PASSED = "Passed"
    FAILED = "Failed"
    ABORTED = "Aborted"
    TIMEDOUT = "Timedout"
    UNKNOWN = "UNKNOWN"

'''
@summary: Lunr API Nodes Smoke Test - List Nodes.
@copyright: Copyright (c) 2012 Rackspace US, Inc.
'''
from testrepo.common.testfixtures.blockstorage import LunrAPIFixture
from unittest2.suite import TestSuite
import json

class LunrNodesAdminAPISmokeTest(LunrAPIFixture):
    '''
        @summary: Lunr API Nodes Smoke Test - List Nodes.
    '''
    def test_list_nodes(self):
        api_response = self.admin_client.Nodes.list()
        self.assertTrue(api_response.ok, "List Nodes API call failed: '%s'" % json.loads(api_response.content))

def load_tests(loader, standard_tests, pattern):
    suite = TestSuite()
    suite.addTest(LunrNodesAdminAPISmokeTest("test_list_nodes"))
    '''@TODO Should we add test for get_info()? It is not in the legacy smoke test, but it
    is in the test strategy and should not harm QE or PreProd environments'''
    return suite

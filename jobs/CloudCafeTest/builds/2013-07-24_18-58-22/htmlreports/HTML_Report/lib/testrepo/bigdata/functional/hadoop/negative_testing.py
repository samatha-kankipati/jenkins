
from testrepo.common.testfixtures.fixtures import BaseParameterizedTestFixture
from ccengine.clients.bigdata.lava_api_client import LavaAPIClient
from testrepo.bigdata.functional.lava_base_fixture import LavaBaseFixture
from ccengine.providers.bigdata.lava_api import LavaAPIProvider as _LavaAPIProvider

from unittest2.suite import TestSuite

class ErrorMessageTest(LavaBaseFixture):
    def test_job_tracker_page():
        '''
        @todo..
        Different set of valid credentials
        '''
        self.master_node = self.lava_provider.get_node_with_role(self.cluster,
                                                                 "NAMENODE")
        jbt_url = "http://%s:50030/master-1/jobtracker.jsp" % self.master_node.ip
        if self.username == "" and self.password == "":
            jbt_response = rest.get(jbt_url)
        else:
            jbt_response = rest.get(jbt_url,auth = (self.username,
                                                    self.password))
        result = jbt_response.ok
        jobt_string = "Hadoop Map/Reduce Administration"
        self.assertTrue(jbt_response.content.find(jobt_string) == -1,
                        "%s" % self.error_message)
        
    def test_task_tracker_page():
        self.master_node = self.lava_provider.get_node_with_role(self.cluster,
                                                                 "NAMENODE")
        for node in self.lava_provider.get:
            if node.role == "slave":
                i = i + 1  
                if(node.id == slave.id):
                    slave_name = "slave-%s" %i
        m_ip = self.master_node.ip
        tt_url = 'http://%s:50060/%s/tasktracker.jsp'%(m_ip,slave_name)
        if self.username == "" and self.password == "":
            tt_response = rest.get(tt_url)
        else:
            tt_response = rest.get(tt_url,auth = (self.username,
                                                  self.password))
        self.assertTrue(tt_response.content.find("Running tasks") == -1,
                        "%s" % self.error_message)
           
    def test_dfs_health_check():
        self.master_node = self.lava_provider.get_node_with_role(cluster,
                                                                 "NAMENODE")
        dfs_url = 'http://%s:50070/master-1/dfshealth.jsp' % self.master_node.ip
        if self.username == "" and self.password == "":
            dfs_response = rest.get(dfs_url)
        else:
            dfs_response = rest.get(dfs_url,auth = (self.username,
                                                    self.password))
        self.assertTrue(dfs_response.content.find("Cluster Summary") == -1,
                        "%s" % self.error_message)
        
    
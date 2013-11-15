'''
@summary: Tests using hutil to run pig jobs on Master Nodes
@copyright: Copyright (c) 2012 Rackspace US, Inc.
'''
from ccengine.providers.bigdata.lava_api import LavaAPIProvider as _LavaAPIProvider
from ccengine.domain.types import LavaJobStatusTypes as _LavaJobStatusTypes
from ccengine.common.connectors.ftp import FTPConnector
from ccengine.providers.bigdata.hutil_provider import HutilProvider
from testrepo.bigdata.functional.lava_base_fixture import LavaBaseFixture

class LavaHutilPigJobTest(LavaBaseFixture):

    def test_pig_job_on_master_node(self):
        '''
        @todo: Currently doesnt work for HBASE.
        @summary: Runs pig job on Master Node. Should work for Hadoop and HBase.
        '''

        master_node = self.lava_provider.get_node_with_role(self.cluster,
                                                            "NAMENODE")
        self.assertIsNotNone(master_node, "Cluster %s does not contain master node"
                                          % self.cluster)
        pig_job_file = self.config.lava_api.TEST_DATA_PATH+'fs_ops1.pig'
        FILENAME = pig_job_file.split('/')[-1]
        JOB_TYPE = 'Pig'

        self.fixture_log.info("Run pig job on box '%s'" % master_node.ip)
        hutil_provider = HutilProvider(self.config, master_node)
        hutil_client = hutil_provider.hutil_client
        response = hutil_client.run_query(JOB_TYPE, FILENAME)
        self.assertIsNotNone(response, 
                             "SSH call could not convert response to JSON")
        self.assertTrue(response.has_key('handle'), 
                        "Response returned without dictionary key handle: '%s'" 
                        %(response))
        job_handle = response['handle']

        self.fixture_log.info("Check if job is tracked as 'running' ...")
        current_status = hutil_provider.wait_for_handle_status(job_handle, 
                                                               _LavaJobStatusTypes.RUNNING)
        self.assertEqual(current_status, _LavaJobStatusTypes.RUNNING, 
                         "Handle %s never went into running status" 
                         %(job_handle))

        '''TODO: Uncomment this when new states (wait/error) are implemented.'''
        #        response_dictionary = hutil_client.list_all_jobs()
        #        self.assertNotEquals(response_dictionary['running'], [], "Running pig job is not shown for listalljobs: '%s'"
        #                                            % response_dictionary)

        self.fixture_log.info("Check if job is tracked as 'finished' ...")
        current_status = hutil_provider.wait_for_handle_status(job_handle, 
                                                               _LavaJobStatusTypes.FINISHED)
        self.assertEqual(current_status, 
                         _LavaJobStatusTypes.FINISHED, 
                         "Handle %s never finished" 
                         %(job_handle))
        response_dictionary = hutil_client.list_all_jobs()
        self.assertNotEquals(response_dictionary['finished'], 
                             [], 
                             "There are no finished jobs: '%s'"
                              %(response_dictionary))
        ftp_connector = FTPConnector(master_node.ip,
            self.config.lava_api.USER_NAME,
            self.config.lava_api.PASSWORD,
            port=9021)
        directory_contents = ftp_connector.browse()
        self.assertIn(self.job_results, directory_contents, 
                      "File '%s' is not in the HDFS" 
                      % self.job_results)
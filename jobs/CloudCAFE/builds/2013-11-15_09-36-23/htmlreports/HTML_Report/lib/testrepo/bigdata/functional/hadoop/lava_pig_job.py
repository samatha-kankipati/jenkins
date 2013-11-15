'''
@summary: Pig Job test for Cluster Nodes
@copyright: Copyright (c) 2012 Rackspace US, Inc.
'''
from ccengine.providers.bigdata.lava_api import LavaAPIProvider as _LavaAPIProvider
from ccengine.providers.bigdata.pig_provider import PigProvider
from ccengine.common.connectors.ftp import FTPConnector
from ccengine.providers.bigdata.hutil_provider import HutilProvider
from ccengine.clients.bigdata.hadoop_client import HadoopClient
from ccengine.clients.bigdata.swiftly_client import SwiftlyClient
from ccengine.domain.types import LavaJobStatusTypes as _LavaJobStatusTypes
from testrepo.common.testfixtures.fixtures import BaseParameterizedTestFixture
from testrepo.bigdata.functional.lava_base_fixture import LavaBaseFixture


class LavaPigJobTest(LavaBaseFixture):

    def setUp(self):
        super(LavaPigJobTest, self).setUp()
        # Copy data files from cloud files onto hdfs
        self.gateway_node = self.lava_provider.get_node_with_role(self.cluster,
                                                                  "GATEWAY")
        self.ssh_connector = self.lava_provider.create_ssh_connector\
            (self.gateway_node)
        self.swiftly_client = SwiftlyClient\
            (self.config.lava_api.USER_NAME,
             self.config.lava_api.PASSWORD,
             self.config.lava_api.SWIFTLY_AUTH_URL,
             self.config.lava_api.SWIFTLY_AUTH_USER,
             self.config.lava_api.SWIFTLY_AUTH_KEY,
             self.gateway_node.ip)
        self.hadoop_client = HadoopClient(self.config.lava_api.USER_NAME,
                                          self.config.lava_api.PASSWORD,
                                          self.gateway_node.ip)

    def test_run_pig_job_on_cluster(self):
        self.swiftly_client.get_file("cfsmall/1xaa.gz", "1xaa.gz")
        self.hadoop_client.filesystem.mkdir("cfsmall")
        self.hadoop_client.filesystem.put("1xaa.gz", "cfsmall/1xaa.gz")
        file_path = self.config.lava_api.TEST_DATA_PATH + 'fs_ops1.pig'
        self.ssh_connector.upload_a_file('fs_ops1.pig', file_path)
        pig_provider = PigProvider(self.config, self.gateway_node)
        response = pig_provider.run_pig_job('fs_ops1.pig')
        self.assertIn("Success!",
                      response,
                      "Pig Job did not run successfully: %s"
                      % response)
        # undo the job to run it again
        self.hadoop_client.filesystem.rmr("/user/%s/result8/"
                                          % (self.config.lava_api.USER_NAME))

    def test_run_pig_job_with_swift_plugin_on_cluster(self):
        file_path = "%sfs_ops1_swift.pig" \
            % self.config.lava_api.TEST_DATA_PATH
        self.ssh_connector.upload_a_file('fs_ops1_swift.pig', file_path)
        pig_provider = PigProvider(self.config, self.gateway_node)
        response = pig_provider.run_pig_job('fs_ops1_swift.pig')
        self.assertIn("Success!",
                      response,
                      "Pig Job did not run successfully: %s"
                      % response)
        # undo the job to run it again
        self.hadoop_client.filesystem.rmr("/user/%s/result9/"
                                          % (self.config.lava_api.USER_NAME))

    def test_pig_job_on_gateway_node_using_hutil(self):
        '''
        @todo: Currently doesnt work for HBASE.
        @summary: Runs pig job on Master Node. Should work for Hadoop and HBase.
        '''

        gateway_node = self.lava_provider.get_node_with_role(self.cluster,
                                                             "GATEWAY")
        self.assertIsNotNone(gateway_node, "Cluster %s does not contain master node"
                             % self.cluster)
        pig_job_file = self.config.lava_api.TEST_DATA_PATH + 'fs_ops1.pig'
        FILENAME = pig_job_file.split('/')[-1]
        JOB_TYPE = 'Pig'
        ssh_connector = self.lava_provider.create_ssh_connector(gateway_node)
        ssh_connector.upload_a_file(FILENAME, pig_job_file)
        self.fixture_log.info("Run pig job on box '%s'" % gateway_node.ip)
        hutil_provider = HutilProvider(self.config, gateway_node)
        hutil_client = hutil_provider.hutil_client
        response = hutil_client.run_query(JOB_TYPE, FILENAME)
        self.assertIsNotNone(response,
                             "SSH call could not convert response to JSON")
        self.assertTrue('handle' in response,
                        "Response returned without dictionary key handle: '%s'"
                        % (response))
        job_handle = response['handle']

        self.fixture_log.info("Check if job is tracked as 'running' ...")
        current_status = hutil_provider.wait_for_handle_status(job_handle,
                                                               _LavaJobStatusTypes.RUNNING)
        self.assertEqual(current_status, _LavaJobStatusTypes.RUNNING,
                         "Handle %s never went into running status"
                         % (job_handle))
        self.fixture_log.info("Check if job is tracked as 'finished' ...")
        current_status = hutil_provider.wait_for_handle_status(job_handle,
                                                               _LavaJobStatusTypes.FINISHED)
        self.assertEqual(current_status,
                         _LavaJobStatusTypes.FINISHED,
                         "Handle %s never finished"
                         % (job_handle))
        response_dictionary = hutil_client.list_all_jobs()
        self.assertNotEquals(response_dictionary['finished'],
                             [],
                             "There are no finished jobs: '%s'"
                             % (response_dictionary))
        ftp_connector = FTPConnector(gateway_node.ip,
                                     self.config.lava_api.USER_NAME,
                                     self.config.lava_api.PASSWORD,
                                     port=9021)
        directory_contents = ftp_connector.browse()
        self.assertIn("result8", directory_contents,
                      "File results8 is not in the HDFS")
        # undo the job to run it again
        self.hadoop_client.filesystem.rmr("/user/%s/result8/"
                                          % (self.config.lava_api.USER_NAME))

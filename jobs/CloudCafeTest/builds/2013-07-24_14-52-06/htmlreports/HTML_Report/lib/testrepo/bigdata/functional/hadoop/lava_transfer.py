'''
@summary: Parameterized Functional test for Lava Transfer functionality using hadoop, FTP, and SFTP
@copyright: Copyright (c) 2012 Rackspace US, Inc.
'''
from ccengine.providers.bigdata.lava_api import LavaAPIProvider as _LavaAPIProvider
from ccengine.providers.bigdata.hadoop_provider import HadoopProvider as _HadoopProvider
from ccengine.common.connectors.ftp import FTPConnector
from ccengine.clients.bigdata.hadoop_client import HadoopClient as _HadoopClient
from testrepo.common.testfixtures.fixtures import BaseParameterizedTestFixture
from testrepo.bigdata.functional.lava_base_fixture import LavaBaseFixture
from ccengine.clients.remote_instance.linux.linux_instance_client import LinuxClient
import ccengine.common.tools.filetools as file_tools

import random


class LavaHadoopTransferTest(LavaBaseFixture):

    def setUp(self):
        super(LavaHadoopTransferTest, self).setUp()
        if not 'scalar_size' in self.__dict__:
            self.scalar_size = 1
        if not 'multiplier' in self.__dict__:
            self.multiplier = "mega"
        if not "filename" in self.__dict__:
            self.filename = self._testMethodName + "_temp" + \
                str(random.randint(1, 1000))
        self.test_file = file_tools.get_testfile(file_name=self.filename,
                                                 multiplier=self.multiplier,
                                                 scalar_size=self.scalar_size)

    def tearDown(self):
        gateway_node = self.lava_provider.get_node_with_role(self.cluster,
                                                             "GATEWAY")
        ssh_client = self.lava_provider.create_ssh_connector(gateway_node)
        ssh_client.exec_command("rm -f %s" % (self.filename))

    def test_copy_between_node_and_hdfs(self):
        '''
        @summary: Parameterized Test uses hadoop to copy a
        specified file on the node cluster
        file system to the Hadoop File System.
        @ivar test_record['cluster_name']: The cluster that the node belongs to
        @ivar test_record['test_file']: The file to be copied.
        '''
        gateway_node = self.lava_provider.get_node_with_role(self.cluster,
                                                             "GATEWAY")
        ssh_client = self.lava_provider.create_ssh_connector(gateway_node)
        filepath = self.test_file
        filename = filepath.split('/')[-1]
        # upload the file
        response = ssh_client.upload_a_file(filename, filepath)
        self.assertTrue(response, "File '%s' Upload FAILED" % filename)
        # make sure the file doesnt get picked up by hdfs
        hadoop_client = _HadoopClient(self.config.lava_api.USER_NAME,
                                      self.config.lava_api.PASSWORD,
                                      gateway_node.ip)
        hadoop_provider = _HadoopProvider(self.config, self.cluster)
        file_found = hadoop_provider.verify_file_in_folder(filename)
        self.assertFalse(file_found, "File: %s picked up by hdfs"
                         % filename)
        # put the file inside hdfs
        hadoop_client.filesystem.put(filename)
        file_found = hadoop_provider.verify_file_in_folder(filename)
        self.assertTrue(file_found, "File: %s was not copied onto hdfs"
                        % filename)
        # delete the file on the box
        response = ssh_client.exec_command("rm -f '%s'\n" % filename)
        response = ssh_client.exec_command("ls '%s'\n" % filename)
        self.assertNotIn(filename, response, "File '%s' was not created: '%s'"
                         % (filename, response))
        # Get the file from hdfs to the node again
        hadoop_client.filesystem.get(filename)
        response = ssh_client.exec_command("ls '%s'\n" % filename)
        self.assertIn(filename, response, "File '%s' was not created: '%s'"
                      % (filename, response))

    def test_ftp_upload_to_hdfs(self):
        '''
        @summary: Parameterized Test uses FTP to UPLOAD
                  a specified file to the Hadoop File System
        @ivar test_record['cluster_name']: The cluster that the node belongs to
        @ivar test_record['test_file']: The file to be copied.
        '''
        file_name = self.dest_file_path.split("/")[-1]
        gateway_node = self.lava_provider.get_node_with_role(self.cluster,
                                                             "GATEWAY")
        ssh_client = self.lava_provider.create_ssh_connector(gateway_node,
                                                             port=9022)
        # upload the file
        response = ssh_client.upload_a_file(
            self.dest_file_path, self.test_file)
        self.assertTrue(response,
                        "scp failed to upload file: %s to server: %s"
                        % (self.test_file, response))
        hadoop_provider = _HadoopProvider(self.config, self.cluster)
        file_found_in_hdfs = hadoop_provider.verify_file_in_folder(file_name)
        self.assertTrue(file_found_in_hdfs,
                        "Files: %s not found in hdfs"
                        % (file_name))

    def disableFTPServiceTest(self):
        gateway_node = self.lava_provider.get_node_with_role(self.cluster,
                                                             "GATEWAY")
        ftp_connector = FTPConnector(gateway_node.ip,
                                     self.config.lava_api.USER_NAME,
                                     self.config.lava_api.PASSWORD,
                                     port=9021)
        ftp_connector.disableService(self.cluster.type)
        ftp_transfer_successful = ftp_connector.upload_a_file(self.test_file)
        self.assertFalse(ftp_transfer_successful,
                         "File Upload sucesful for cluster: %s"
                         % (self.cluster_name))

    def stopFTPServiceUntilRestart(self):
        gateway_node = self.lava_provider.get_node_with_role(self.cluster,
                                                             "GATEWAY")
        ftp_connector = FTPConnector(gateway_node.ip,
                                     self.config.lava_api.USER_NAME,
                                     self.config.lava_api.PASSWORD,
                                     port=9021)
        ftp_connector.stopService()
        ftp_transfer_successful = ftp_connector.upload_a_file(self.test_file)
        self.assertFalse(ftp_transfer_successful,
                         "File Upload sucesful for cluster: %s"
                         % (self.cluster_name))
        linux_client = LinuxClient(ip_address=gateway_node.ip,
                                   server_id=gateway_node.server_id,
                                   os_distro="",
                                   username=self.config.lava_api.USER_NAME,
                                   password=self.config.lava_api.PASSWORD)
        self.assertTrue(linux_client.reboot(), "%s did not reboot"
                        % (gateway_node.ip))
        ftp_transfer_successful = ftp_connector.upload_a_file(self.test_file)
        self.assertTrue(ftp_transfer_successful,
                        "FTP failed to upload file: %s to HDFS"
                        % (self.test_file))
        hadoop_provider = _HadoopProvider(self.config, gateway_node)
        filename = self.test_file.split('/')[-1]
        file_found_in_hdfs = hadoop_provider.verify_file_in_folder(filename)
        self.assertTrue(file_found_in_hdfs,
                        "Files: %s not found in hdfs"
                        % (self.test_file))

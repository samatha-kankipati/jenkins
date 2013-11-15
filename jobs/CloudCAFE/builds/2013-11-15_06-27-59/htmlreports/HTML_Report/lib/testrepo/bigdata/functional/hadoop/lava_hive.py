'''
@summary: Hive Job test for Cluster Nodes
@copyright: Copyright (c) 2012 Rackspace US, Inc.
'''
from ccengine.providers.bigdata.lava_api import LavaAPIProvider as _LavaAPIProvider
from testrepo.bigdata.functional.lava_base_fixture import LavaBaseFixture

import csv
import os.path
import random


class LavaHiveJob(LavaBaseFixture):
    def test_hive_script(self):
        gateway_node = self.lava_provider.get_node_with_role(self.cluster,
                                                             "GATEWAY")
        ssh_connector = self.lava_provider.create_ssh_connector(gateway_node)
        # FTP file (hive job) onto cluster file system
        hive_path = self.config.lava_api.TEST_DATA_PATH + 'hive_script.q'
        result = ssh_connector.upload_a_file("hive_script.q", hive_path)
        self.assertTrue(result, "Hive script upload failed")
        '''
        Generating the csv file inside the test for now.
        But need to push it up and make it more re-usable
        '''
        # Check if the file exists and if not create it
        hive_data_file_name = "hive_data.csv"
        hive_data_file_path = "/tmp/hive_data.csv"
        if not os.path.isfile(hive_data_file_path):
            data_file = open(hive_data_file_path, "wb")
            writer = csv.writer(data_file)
            for i in xrange(1000):
                year = random.randint(1998, 2007)
                temp = random.randint(78, 89)
                quality = random.randint(0, 10)
                writer.writerow((year, temp, quality))
            data_file.close()
        result = ssh_connector.upload_a_file(hive_data_file_name,
                                             hive_data_file_path)
        self.assertTrue(result, "Data file upload failed")
        response, prompt = ssh_connector.exec_shell_command_wait_for_prompt\
            ("hive -f hive_script.q", "%s@GATEWAY"
             % (self.config.lava_api.USER_NAME))
        self.assertIn("SUCCESS",
                      response,
                      "Hive Job did not run successfully: %s" % response)

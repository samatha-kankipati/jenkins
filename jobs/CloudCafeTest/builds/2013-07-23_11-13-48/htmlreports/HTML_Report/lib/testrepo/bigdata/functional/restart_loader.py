from datetime import datetime
from testrepo.bigdata.smoke.lava_api import LavaAPITest as _SmokeLavaAPITest
from testrepo.bigdata.functional.hadoop.lava_transfer import \
    LavaHadoopTransferTest
from testrepo.bigdata.functional.swiftly.lava_swiftly import LavaSwiftlyTest
from testrepo.bigdata.functional.hadoop.lava_pig_job import LavaPigJobTest
from ccengine.common.loaders.base_parameterized_loader import \
    BaseParameterizedLoader
from ccengine.common.data_generators.bigdata.lava_data_generator import \
    LavaAPIDataGenerator, SCPTransfer
from testrepo.bigdata.functional.hadoop.lava_hive import LavaHiveJob

from unittest2.suite import TestSuite


def load_tests(loader, standard_tests, pattern):
    lava_api_data_generator = LavaAPIDataGenerator()
    cluster_loader = BaseParameterizedLoader(lava_api_data_generator)
    cluster_loader.addTest(_SmokeLavaAPITest("test_add_cluster"))
    cluster_loader.addTest(_SmokeLavaAPITest("test_restart_all_nodes"))
    cluster_loader.addTest(LavaHiveJob("test_hive_script"))
    cluster_loader.addTest(LavaPigJobTest("test_run_pig_job_on_cluster"))
    cluster_loader.addTest(LavaHadoopTransferTest(
        "test_copy_between_node_and_hdfs"))
    cluster_loader.addTest(LavaHadoopTransferTest("test_ftp_upload_to_hdfs"),
                           SCPTransfer())
    cluster_loader.addTest(LavaSwiftlyTest("test_swiftly_node_to_cloud_files"))
    cluster_loader.addTest(LavaSwiftlyTest("test_swiftly_cloud_files_to_hdfs"))
    cluster_loader.addTest(_SmokeLavaAPITest("test_delete_cluster"))
    return cluster_loader.getSuite()

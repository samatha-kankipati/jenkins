from datetime import datetime
from testrepo.bigdata.smoke.lava_api import LavaAPITest
from testrepo.bigdata.functional.lava_api.negative_testing import \
    ErrorMessageTest
from testrepo.bigdata.functional.hadoop.lava_transfer import \
    LavaHadoopTransferTest as _LHTT
from testrepo.bigdata.functional.swiftly.lava_swiftly import \
    LavaSwiftlyTest
from testrepo.bigdata.functional.hadoop.lava_pig_job import \
    LavaPigJobTest as _LPJT
from testrepo.bigdata.functional.hadoop.lava_hive import LavaHiveJob
from ccengine.common.loaders.base_parameterized_loader import \
    BaseParameterizedLoader
from ccengine.common.data_generators.bigdata.lava_data_generator \
    import LavaAPIDataGenerator, SCPTransfer

from unittest2.suite import TestSuite


def load_tests(loader, standard_tests, pattern):
    lava_api_data_generator = LavaAPIDataGenerator()
    cluster_loader = BaseParameterizedLoader(lava_api_data_generator)
    cluster_loader.addTest(LavaAPITest("test_add_cluster"))
    cluster_loader.addTest(LavaHiveJob("test_hive_script"))
    cluster_loader.addTest(_LPJT("test_run_pig_job_on_cluster"))
    cluster_loader.addTest(_LHTT("test_copy_between_node_and_hdfs"))
    cluster_loader.addTest(_LHTT("test_ftp_upload_to_hdfs"),
                           SCPTransfer())
    cluster_loader.addTest(LavaSwiftlyTest("test_swiftly_node_to_cloud_files"))
    cluster_loader.addTest(LavaSwiftlyTest("test_swiftly_cloud_files_to_hdfs"))
    cluster_loader.addTest(LavaAPITest("test_delete_cluster"))
    return cluster_loader.getSuite()

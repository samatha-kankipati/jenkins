from ccengine.common.loaders.base_parameterized_loader import BaseParameterizedLoader
from ccengine.common.data_generators.bigdata.lava_data_generator import LavaMiscFTPFileDataGenerator
from testrepo.bigdata.functional.hadoop.lava_transfer import LavaHadoopTransferTest
from testrepo.bigdata.smoke.lava_api import LavaAPITest

from unittest2.suite import TestSuite

def load_tests(loader, standard_tests, pattern):
    suite = TestSuite()
    ftp_data_generator = LavaMiscFTPFileDataGenerator()
    cluster_data = ftp_data_generator.ClusterData()
    ftp_data = ftp_data_generator.FTPMiscRunner()
    cluster_loader = BaseParameterizedLoader(cluster_data)
    cluster_loader.addTest(LavaAPITest("test_add_cluster"))
    suite.addTest(cluster_loader.getSuite())
    
    cluster_loader = BaseParameterizedLoader(ftp_data)
    cluster_loader.addTest(LavaHadoopTransferTest("test_ftp_upload_to_hdfs"))
    cluster_loader.addTest(LavaHadoopTransferTest("test_copy_from_node_to_hdfs"))
    cluster_loader.addTest(LavaHadoopTransferTest("test_sftp_upload_to_node"))
    cluster_loader.addTest(LavaHadoopTransferTest("test_copy_from_hdfs_to_node"))
    suite.addTest(cluster_loader.getSuite())
    
    cluster_loader = BaseParameterizedLoader(cluster_data)
    cluster_loader.addTest(LavaAPITest("test_delete_cluster"))
    suite.addTest(cluster_loader.getSuite())
    return suite

        

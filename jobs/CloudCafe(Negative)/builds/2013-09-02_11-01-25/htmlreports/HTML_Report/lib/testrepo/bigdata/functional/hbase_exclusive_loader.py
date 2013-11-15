from datetime import datetime

from testrepo.bigdata.functional.hbase.hbase_shell import HbaseShellTest
from ccengine.common.loaders.base_parameterized_loader import BaseParameterizedLoader
from ccengine.data_generators.bigdata.lava_data_generator import LavaHbaseDataGenerator
from testrepo.bigdata.smoke.lava_api import LavaAPITest
from unittest2.suite import TestSuite

def load_tests(loader, standard_tests, pattern):
    hbase_data = LavaHbaseDataGenerator()
    cluster_loader = BaseParameterizedLoader(hbase_data)
    cluster_loader.addTest(LavaAPITest("test_add_cluster"))
    cluster_loader.addTest(HbaseShellTest("test_hbase_shell"))
    cluster_loader.addTest(LavaAPITest("test_delete_cluster"))
    return cluster_loader.getSuite()
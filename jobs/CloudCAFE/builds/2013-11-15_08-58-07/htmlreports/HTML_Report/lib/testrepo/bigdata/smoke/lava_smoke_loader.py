from datetime import datetime
from testrepo.bigdata.smoke.lava_api import LavaAPITest

from ccengine.common.loaders.base_parameterized_loader import \
    BaseParameterizedLoader
from ccengine.common.data_generators.bigdata.lava_data_generator \
    import LavaAPIDataGenerator

from unittest2.suite import TestSuite


def load_tests(loader, standard_tests, pattern):
    suite = TestSuite()
    suite.addTest(LavaAPITest("test_update_profile"))
    smoke_data_gen = LavaAPIDataGenerator()
    custom_loader = BaseParameterizedLoader(smoke_data_gen)
    custom_loader.addTest(LavaAPITest("test_add_cluster"))
    custom_loader.addTest(LavaAPITest("test_cluster_nodes"))
    custom_loader.addTest(LavaAPITest("test_manual_ssh_key_addition"))
    custom_loader.addTest(LavaAPITest("test_node_web_pages"))
    custom_loader.addTest(LavaAPITest("test_list_clusters"))
    custom_loader.addTest(LavaAPITest("test_get_cluster_info"))
    custom_loader.addTest(LavaAPITest("test_get_node"))
    custom_loader.addTest(LavaAPITest("test_resize_cluster"))
    custom_loader.addTest(LavaAPITest("test_delete_cluster"))
    suite.addTest(custom_loader.getSuite())
    return suite

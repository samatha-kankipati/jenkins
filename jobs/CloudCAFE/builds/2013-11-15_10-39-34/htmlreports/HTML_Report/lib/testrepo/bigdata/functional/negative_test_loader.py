from datetime import datetime
from testrepo.bigdata.smoke.lava_api import LavaAPITest as _SmokeLavaAPITest
from testrepo.bigdata.functional.lava_api.negative_testing \
    import ErrorMessageTest
from ccengine.common.loaders.base_parameterized_loader \
    import BaseParameterizedLoader
from ccengine.common.data_generators.bigdata.negative_data_generator \
    import ResizeDataErrors, InvalidProfilePassword, ClusterCreateErrors
from ccengine.common.data_generators.bigdata.lava_data_generator \
    import LavaAPIDataGenerator

from unittest2.suite import TestSuite


def load_tests(loader, standard_tests, pattern):
    suite = TestSuite()
    suite.addTest(
        ErrorMessageTest("test_no_profile_for_cluster_create"))
    suite.addTest(
        ErrorMessageTest("test_default_repl_count_for_profile"))
    suite.addTest(
        ErrorMessageTest("test_invalid_cluster_id"))
    suite.addTest(
        ErrorMessageTest("test_unauthorized_calls_admin_api"))
    lava_api_data_generator = LavaAPIDataGenerator()
    cluster_loader = BaseParameterizedLoader(
        lava_api_data_generator)
    cluster_loader.addTest(
        _SmokeLavaAPITest("test_add_cluster"))
    cluster_loader.addTest(
        ErrorMessageTest("test_no_proxy_node_web_pages"))
    cluster_loader.addTest(
        ErrorMessageTest("test_invalid_password"),
        InvalidProfilePassword())
    cluster_loader.addTest(
        ErrorMessageTest("test_error_messages_for_cluster_create"),
        ClusterCreateErrors())
    cluster_loader.addTest(
        ErrorMessageTest("test_unauthorized_calls"))
    cluster_loader.addTest(
        ErrorMessageTest("test_error_messages_for_resize_cluster"),
        ResizeDataErrors())
    cluster_loader.addTest(_SmokeLavaAPITest("test_delete_cluster"))
    suite.addTest(cluster_loader.getSuite())
    return suite

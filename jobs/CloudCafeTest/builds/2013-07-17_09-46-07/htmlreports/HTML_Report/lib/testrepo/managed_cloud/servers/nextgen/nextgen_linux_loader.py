from testrepo.managed_cloud.servers. \
    nextgen.test_parameterized_linux_nextgen_servers \
    import ManagedLinuxNextGenServersTest
from ccengine.common.loaders.base_parameterized_loader \
    import BaseParameterizedLoader
from ccengine.common.data_generators.managed_cloud. \
    nextgen_linux_generator import ManagedCloudLinuxNextGenDataGenerator
from unittest2.suite import TestSuite


def load_tests(loader, standard_tests, pattern):
    suite = TestSuite()
    smoke_data_gen = ManagedCloudLinuxNextGenDataGenerator()
    custom_loader = BaseParameterizedLoader(smoke_data_gen)
    custom_loader.addTest(ManagedLinuxNextGenServersTest(
        "test_managed_server_active"))
    custom_loader.addTest(ManagedLinuxNextGenServersTest(
        "test_managed_automation_process_started"))
    custom_loader.addTest(ManagedLinuxNextGenServersTest(
        "test_managed_automation_complete"))
    custom_loader.addTest(ManagedLinuxNextGenServersTest(
        "test_rack_account_password_from_valkyrie"))
    custom_loader.addTest(ManagedLinuxNextGenServersTest(
        "test_can_authenticate"))
    custom_loader.addTest(ManagedLinuxNextGenServersTest(
        "test_rackspace_monitoring_agent_file"))
    custom_loader.addTest(ManagedLinuxNextGenServersTest(
        "test_rackspace_monitoring_agent_running"))
    custom_loader.addTest(ManagedLinuxNextGenServersTest(
        "test_mckick_complete"))
    custom_loader.addTest(ManagedLinuxNextGenServersTest(
        "test_monitoring_entity_is_registered"))
    # TODO[Siva] need to figure out pagination in monitoring api calls.
    # custom_loader.addTest(ManagedLinuxNextGenServersTest(
    #    "test_monitoring_agent_is_registered"))
    # custom_loader.addTest(ManagedLinuxNextGenServersTest(
    #    "test_monitoring_agents_list"))
    custom_loader.addTest(ManagedLinuxNextGenServersTest(
        "test_create_server_image"))
    custom_loader.addTest(ManagedLinuxNextGenServersTest(
        "test_delete_server"))
    suite.addTest(custom_loader.getSuite())
    return suite

from ccengine.common.loaders.base_parameterized_loader \
    import BaseParameterizedLoader
from ccengine.common.data_generators.managed_cloud.legacy_windows_generator \
    import ManagedCloudLegacyWindowsDataGenerator
from testrepo.managed_cloud.servers.legacy. \
    test_parameterized_windows_legacy_servers \
    import ManagedWindowsFirstGenServersTest
from unittest2.suite import TestSuite


def load_tests(loader, standard_tests, pattern):
    suite = TestSuite()
    smoke_data_gen = ManagedCloudLegacyWindowsDataGenerator()
    custom_loader = BaseParameterizedLoader(smoke_data_gen)
    custom_loader.addTest(ManagedWindowsFirstGenServersTest(
        "test_legacy_server_active"))
    custom_loader.addTest(ManagedWindowsFirstGenServersTest(
        "test_rack_account_password_from_valkyrie"))
    custom_loader.addTest(ManagedWindowsFirstGenServersTest(
        "test_monitoring_entity_is_registered"))
    custom_loader.addTest(ManagedWindowsFirstGenServersTest(
        "test_monitoring_agent_is_registered"))
    custom_loader.addTest(ManagedWindowsFirstGenServersTest(
        "test_monitoring_agents_list"))
    custom_loader.addTest(ManagedWindowsFirstGenServersTest(
        "test_backup_enabled"))
    custom_loader.addTest(ManagedWindowsFirstGenServersTest(
        "test_backup_config"))
    suite.addTest(custom_loader.getSuite())
    return suite

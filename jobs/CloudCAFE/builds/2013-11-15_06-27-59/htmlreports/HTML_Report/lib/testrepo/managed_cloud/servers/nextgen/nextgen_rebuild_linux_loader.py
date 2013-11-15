from testrepo.managed_cloud.servers.nextgen. \
    test_parameterized_linux_nextgen_servers \
    import ManagedLinuxNextGenServersTest
from ccengine.common.loaders.base_parameterized_loader \
    import BaseParameterizedLoader
from ccengine.common.data_generators.managed_cloud. \
    nextgen_rebuild_linux_servers_generator \
    import ManagedCloudLinuxNextGenRebuildDataGenerator
from unittest2.suite import TestSuite


def load_tests(loader, standard_tests, pattern):
    suite = TestSuite()
    smoke_data_gen = ManagedCloudLinuxNextGenRebuildDataGenerator()
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
    custom_loader.addTest(ManagedLinuxNextGenServersTest(
        "test_postfix_config_file"))
    custom_loader.addTest(ManagedLinuxNextGenServersTest(
        "test_sendmail_file"))
    custom_loader.addTest(ManagedLinuxNextGenServersTest(
        "test_mailgun_configured"))
    custom_loader.addTest(ManagedLinuxNextGenServersTest(
        "test_mailgun_sendmail"))
    custom_loader.addTest(ManagedLinuxNextGenServersTest(
        "test_listen_port_25"))
    custom_loader.addTest(ManagedLinuxNextGenServersTest(
        "test_listen_port_587"))
    custom_loader.addTest(ManagedLinuxNextGenServersTest(
        "test_listen_port_465"))
    custom_loader.addTest(ManagedLinuxNextGenServersTest(
        "test_backup_enabled"))
    custom_loader.addTest(ManagedLinuxNextGenServersTest(
        "test_backup_config"))
    custom_loader.addTest(ManagedLinuxNextGenServersTest(
        "test_yumcron_file"))
    custom_loader.addTest(ManagedLinuxNextGenServersTest(
        "test_yumcron_activated"))
    #[Deepak] removing test_delete_server from suite as we'll be cleaning up
    #test servers via Cleanup script scheduled to run in Jenkins
    suite.addTest(custom_loader.getSuite())
    return suite

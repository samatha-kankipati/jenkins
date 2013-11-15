from testrepo.managed_cloud.servers.nextgen. \
    test_parameterized_linux_nextgen_servers \
    import ManagedLinuxNextGenServersTest
from ccengine.common.loaders.base_parameterized_loader \
    import BaseParameterizedLoader
from ccengine.common.data_generators.managed_cloud. \
    nextgen_snapshot_lamp_servers_generator \
    import ManagedCloudLampNextGenSnapshotDataGenerator
from unittest2.suite import TestSuite


def load_tests(loader, standard_tests, pattern):
    suite = TestSuite()
    smoke_data_gen = ManagedCloudLampNextGenSnapshotDataGenerator()
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
        "test_apache_open_port_80"))
    custom_loader.addTest(ManagedLinuxNextGenServersTest(
        "test_apache_open_port_443"))
    custom_loader.addTest(ManagedLinuxNextGenServersTest(
        "test_listen_port_80"))
    custom_loader.addTest(ManagedLinuxNextGenServersTest(
        "test_listen_port_443"))
    custom_loader.addTest(ManagedLinuxNextGenServersTest(
        "test_apache_http_200"))
    custom_loader.addTest(ManagedLinuxNextGenServersTest(
        "test_apache_http_404"))
    custom_loader.addTest(ManagedLinuxNextGenServersTest(
        "test_php_apc"))
    custom_loader.addTest(ManagedLinuxNextGenServersTest(
        "test_fail2ban_firewall"))
    custom_loader.addTest(ManagedLinuxNextGenServersTest(
        "test_fail2ban_running"))
    custom_loader.addTest(ManagedLinuxNextGenServersTest(
        "test_listen_port_3306"))
    custom_loader.addTest(ManagedLinuxNextGenServersTest(
        "test_open_port_3306"))
    custom_loader.addTest(ManagedLinuxNextGenServersTest(
        "test_show_processlist"))
    custom_loader.addTest(ManagedLinuxNextGenServersTest(
        "test_phpmyadmin"))
    custom_loader.addTest(ManagedLinuxNextGenServersTest(
        "test_localhost_in_hosts"))
    custom_loader.addTest(ManagedLinuxNextGenServersTest(
        "test_rhn_check"))
    custom_loader.addTest(ManagedLinuxNextGenServersTest(
        "test_root_statuspass"))
    custom_loader.addTest(ManagedLinuxNextGenServersTest(
        "test_root_muninpass"))
    custom_loader.addTest(ManagedLinuxNextGenServersTest(
        "test_root_phpmyadminpass"))
    custom_loader.addTest(ManagedLinuxNextGenServersTest(
        "test_driveclient_installed"))
    custom_loader.addTest(ManagedLinuxNextGenServersTest(
        "test_driveclient_bootstrap"))
    custom_loader.addTest(ManagedLinuxNextGenServersTest(
        "test_driveclient_running"))
    custom_loader.addTest(ManagedLinuxNextGenServersTest(
        "test_munin_running"))
    custom_loader.addTest(ManagedLinuxNextGenServersTest(
        "test_swap_exists"))
    custom_loader.addTest(ManagedLinuxNextGenServersTest(
        "test_rack_user_exists"))
    custom_loader.addTest(ManagedLinuxNextGenServersTest(
        "test_monitoring_agent_running"))
    custom_loader.addTest(ManagedLinuxNextGenServersTest(
        "test_monitoring_agent_configured"))
    custom_loader.addTest(ManagedLinuxNextGenServersTest(
        "test_create_lamp_server_image"))
    custom_loader.addTest(ManagedLinuxNextGenServersTest(
        "test_delete_server"))
    suite.addTest(custom_loader.getSuite())
    return suite

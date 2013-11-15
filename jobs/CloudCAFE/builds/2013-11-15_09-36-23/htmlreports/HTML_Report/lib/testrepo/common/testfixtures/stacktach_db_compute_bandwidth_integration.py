'''
@summary: Dervied Classes for StackTach Test Suites (Collections of Test Cases)
@note: Correspondes DIRECTLY TO A unittest.TestCase
@see: http://docs.python.org/library/unittest.html#unittest.TestCase
@copyright: Copyright (c) 2012-2013 Rackspace US, Inc.
'''
from testrepo.common.testfixtures.stacktach_db_compute_integration \
    import CreateServerFixture
from ccengine.providers.compute.bandwidth_compute_api \
    import BandwidthComputeAPIProvider as _ComputeAPIProvider
from ccengine.providers.configuration import MasterConfigProvider as _MCP


class BwComputeFixture(CreateServerFixture):
    '''
    @summary: Fixture for a StackTach DB and Compute Bandwidth test.
    @note:  This class performs integration tests between the Compute API
      and the StackTach DB API .
    @attention: This class MULTIPLE INHERITS methods and attributes from both
     ComputeFixture and StackTachDBFixture to provide some readability
     with the intention of later refactoring towards an integration-type
     fixture.
    '''

    @classmethod
    def setUpClass(cls, flavorRef=None):
        cls.config = _MCP()
        cls.flavor_ref = cls.config.compute_api.flavor_ref
        cls.flavor_ref_alt = cls.config.compute_api.flavor_ref_alt
        if cls.flavor_ref > cls.flavor_ref_alt:
            raise cls.assertClassSetupFailure(
                'flavor_ref should not be greater than flavor_ref_alt. '
                'flavor_ref: {0}  flavor_ref_alt: {1}'.format(
                    cls.flavor_ref, cls.flavor_ref_alt))
        super(BwComputeFixture, cls).setUpClass(flavorRef=flavorRef)
        cls.compute_provider = _ComputeAPIProvider(cls.config, cls.fixture_log)
        cls.gb_file_size = cls.config.compute_api.gb_file_size
        cls.test_type = cls.config.compute_api.test_type
        cls.new_password = "abc123"
        cls.expected_audit_period_ending = None
        cls.launched_at_rebuilt_server = None
        cls.launched_at_resized_server = None
        cls.rebooted_server = None
        cls.changed_pw_server = None
        cls.rebuilt_server = None
        cls.resized_server = None


class BwCreateServerFixture(BwComputeFixture):
    '''
    @summary: Creates a server, waits for active state. Transfers some
        bandwidth.
    @todo: Check all immediate exists events in AH
    '''

    @classmethod
    def setUpClass(cls):
        # create server
        super(BwCreateServerFixture, cls).setUpClass()
        try:
            # generate bandwidth
            (cls.compute_provider
             .do_bandwidth_server_to_client(cls.created_server,
                                            cls.gb_file_size))
        except Exception as exception:
            cls.fixture_log.critical('Exception occured while transferring '
                                     'bandwidth from server to local client.')
            raise cls.assertClassSetupFailure(exception)


class NoBwCreateServerFixture(BwComputeFixture):
    '''
    @summary: Creates a server, waits for active state. Does not
        transfer any bandwidth.
    @todo: Check all immediate exists events in AH
    '''

    @classmethod
    def setUpClass(cls):
        # create server
        super(NoBwCreateServerFixture, cls).setUpClass()


class BwBeforeChangePasswordServerFixture(BwComputeFixture):
    '''
    @summary: Creates a server, waits for active state.
        Transfers some bandwidth.  Then changes the password
        of the server.
    '''

    @classmethod
    def setUpClass(cls):
        # create server
        super(BwBeforeChangePasswordServerFixture, cls).setUpClass()
        try:
            # generate bandwidth
            (cls.compute_provider
             .do_bandwidth_server_to_client(cls.created_server,
                                            cls.gb_file_size))
        except Exception as exception:
            cls.fixture_log.critical('Exception occured while transferring '
                                     'bandwidth from server to local client.')
            raise cls.assertClassSetupFailure(exception)
        try:
            # do change password
            cls.changed_pw_server = \
                (cls.compute_provider
                 .change_password_and_await(cls.created_server.id,
                                            cls.new_password))
        except Exception as exception:
            cls.fixture_log.critical('Exception occured while performing '
                                     'a CHANGE PASSWORD on the server.')
            raise cls.assertClassSetupFailure(exception)


class BwAfterChangePasswordServerFixture(BwComputeFixture):
    '''
    @summary: Creates a server, waits for active state.
        Then changes the password of the server.  Transfers bandwidth.
    '''

    @classmethod
    def setUpClass(cls):
        # create server
        super(BwAfterChangePasswordServerFixture, cls).setUpClass()
        try:
            # do change password
            cls.changed_pw_server = \
                (cls.compute_provider
                 .change_password_and_await(cls.created_server.id,
                                            cls.new_password))
        except Exception as exception:
            cls.fixture_log.critical('Exception occured while performing '
                                     'a CHANGE PASSWORD on the server.')
            raise cls.assertClassSetupFailure(exception)
        cls.created_server.adminPass = cls.new_password
        try:
            # generate bandwidth
            (cls.compute_provider
             .do_bandwidth_server_to_client(cls.created_server,
                                            cls.gb_file_size))
        except Exception as exception:
            cls.fixture_log.critical('Exception occured while transferring '
                                     'bandwidth from server to local client.')
            raise cls.assertClassSetupFailure(exception)


class BwBeforeAndAfterChangePasswordServerFixture(BwComputeFixture):
    '''
    @summary: Creates a server, waits for active state.
        Transfers bandwidth. Then changes the password of the server.
        Transfers bandwidth again.
    '''

    @classmethod
    def setUpClass(cls):
        # create server
        super(BwBeforeAndAfterChangePasswordServerFixture, cls).setUpClass()
        try:
            # generate bandwidth
            (cls.compute_provider
             .do_bandwidth_server_to_client(cls.created_server,
                                            cls.gb_file_size))
        except Exception as exception:
            cls.fixture_log.critical('Exception occured while transferring '
                                     'bandwidth from server to local client.')
            raise cls.assertClassSetupFailure(exception)
        try:
            # do change password
            cls.changed_pw_server = \
                (cls.compute_provider
                 .change_password_and_await(cls.created_server.id,
                                            cls.new_password))
        except Exception as exception:
            cls.fixture_log.critical('Exception occured while performing '
                                     'a CHANGE PASSWORD on the server.')
            raise cls.assertClassSetupFailure(exception)
        cls.created_server.adminPass = cls.new_password
        try:
            # generate bandwidth
            (cls.compute_provider
             .do_bandwidth_server_to_client(cls.created_server,
                                            cls.gb_file_size))
        except Exception as exception:
            cls.fixture_log.critical('Exception occured while transferring '
                                     'bandwidth from server to local client.')
            raise cls.assertClassSetupFailure(exception)


class NoBwChangePasswordServerFixture(BwComputeFixture):
    '''
    @summary: Creates a server, waits for active state.
        Then changes the password of the server.
        Does not transfer any bandwidth.
    '''

    @classmethod
    def setUpClass(cls):
        # create server
        super(NoBwChangePasswordServerFixture, cls).setUpClass()
        try:
            # do change password
            cls.changed_pw_server = \
                (cls.compute_provider
                 .change_password_and_await(cls.created_server.id,
                                            cls.new_password))
        except Exception as exception:
            cls.fixture_log.critical('Exception occured while performing '
                                     'a CHANGE PASSWORD on the server.')
            raise cls.assertClassSetupFailure(exception)


class BwBeforeRescueServerFixture(BwComputeFixture):
    '''
    @summary: Creates a server, waits for active state.
        Transfers some bandwidth.  Then rescues and unrescues the server.
    '''

    @classmethod
    def setUpClass(cls):
        # create server
        super(BwBeforeRescueServerFixture, cls).setUpClass()
        try:
            # generate bandwidth
            (cls.compute_provider
             .do_bandwidth_server_to_client(cls.created_server,
                                            cls.gb_file_size))
        except Exception as exception:
            cls.fixture_log.critical('Exception occured while transferring '
                                     'bandwidth from server to local client.')
            raise cls.assertClassSetupFailure(exception)
        try:
            # do rescue and unrescue
            (cls.unrescued_server,
             cls.expected_audit_period_ending,
             cls.launched_at_unrescued_server) = \
                cls.compute_provider.rescue_and_unrescue(
                    server_id=cls.created_server.id)
        except Exception as exception:
            cls.fixture_log.critical('Exception occured while performing '
                                     'a RESCUE on the server.')
            raise cls.assertClassSetupFailure(exception)


class BwAfterRescueServerFixture(BwComputeFixture):
    '''
    @summary: Creates a server, waits for active state.
        Then rescues  and unrescues the server.  Transfers bandwidth.
    '''

    @classmethod
    def setUpClass(cls):
        # create server
        super(BwAfterRescueServerFixture, cls).setUpClass()
        try:
            # do rescue and unrescue
            (cls.unrescued_server,
             cls.expected_audit_period_ending,
             cls.launched_at_unrescued_server) = \
                cls.compute_provider.rescue_and_unrescue(
                    server_id=cls.created_server.id)
        except Exception as exception:
            cls.fixture_log.critical('Exception occured while performing '
                                     'a RESCUE on the server.')
            raise cls.assertClassSetupFailure(exception)
        try:
            # generate bandwidth
            (cls.compute_provider
             .do_bandwidth_server_to_client(cls.created_server,
                                            cls.gb_file_size))
        except Exception as exception:
            cls.fixture_log.critical('Exception occured while transferring '
                                     'bandwidth from server to local client.')
            raise cls.assertClassSetupFailure(exception)


class BwBeforeAndAfterRescueServerFixture(BwComputeFixture):
    '''
    @summary: Creates a server, waits for active state.
        Transfers bandwidth. Then rescues and unrescues the server.
        Transfers bandwidth again.
    '''

    @classmethod
    def setUpClass(cls):
        # create server
        super(BwBeforeAndAfterRescueServerFixture, cls).setUpClass()
        try:
            # generate bandwidth
            (cls.compute_provider
             .do_bandwidth_server_to_client(cls.created_server,
                                            cls.gb_file_size))
        except Exception as exception:
            cls.fixture_log.critical('Exception occured while transferring '
                                     'bandwidth from server to local client.')
            raise cls.assertClassSetupFailure(exception)
        try:
            # do rescue and unrescue
            (cls.unrescued_server,
             cls.expected_audit_period_ending,
             cls.launched_at_unrescued_server) = \
                cls.compute_provider.rescue_and_unrescue(
                    server_id=cls.created_server.id)
        except Exception as exception:
            cls.fixture_log.critical('Exception occured while performing '
                                     'a RESCUE on the server.')
            raise cls.assertClassSetupFailure(exception)
        try:
            # generate bandwidth
            (cls.compute_provider
             .do_bandwidth_server_to_client(cls.created_server,
                                            cls.gb_file_size))
        except Exception as exception:
            cls.fixture_log.critical('Exception occured while transferring '
                                     'bandwidth from server to local client.')
            raise cls.assertClassSetupFailure(exception)


class NoBwRescueServerFixture(BwComputeFixture):
    '''
    @summary: Creates a server, waits for active state.
        Then rescues and unrescues the server.
        Does not transfers any bandwidth.
    '''

    @classmethod
    def setUpClass(cls):
        # create server
        super(NoBwRescueServerFixture, cls).setUpClass()
        try:
            # do rescue and unrescue
            (cls.unrescued_server,
             cls.expected_audit_period_ending,
             cls.launched_at_unrescued_server) = \
                cls.compute_provider.rescue_and_unrescue(
                    server_id=cls.created_server.id)
        except Exception as exception:
            cls.fixture_log.critical('Exception occured while performing '
                                     'a RESCUE on the server.')
            raise cls.assertClassSetupFailure(exception)


class BwBeforeSoftRebootServerFixture(BwComputeFixture):
    '''
    @summary: Creates a server, waits for active state.
        Transfers some bandwidth.  Then soft reboots the server.
    '''

    @classmethod
    def setUpClass(cls):
        # create server
        super(BwBeforeSoftRebootServerFixture, cls).setUpClass()
        try:
            # generate bandwidth
            (cls.compute_provider
             .do_bandwidth_server_to_client(cls.created_server,
                                            cls.gb_file_size))
        except Exception as exception:
            cls.fixture_log.critical('Exception occured while transferring '
                                     'bandwidth from server to local client.')
            raise cls.assertClassSetupFailure(exception)
        try:
            # do soft reboot
            cls.rebooted_server = \
                (cls.compute_provider
                 .reboot_and_await(server_id=cls.created_server.id,
                                   reboot_type="SOFT"))
        except Exception as exception:
            cls.fixture_log.critical('Exception occured while performing '
                                     'a SOFT REBOOT on the server.')
            raise cls.assertClassSetupFailure(exception)


class BwAfterSoftRebootServerFixture(BwComputeFixture):
    '''
    @summary: Creates a server, waits for active state.
        Then soft reboots the server.  Transfers bandwidth.
    '''

    @classmethod
    def setUpClass(cls):
        # create server
        super(BwAfterSoftRebootServerFixture, cls).setUpClass()
        try:
            # do soft reboot
            cls.rebooted_server = \
                (cls.compute_provider
                 .reboot_and_await(server_id=cls.created_server.id,
                                   reboot_type="SOFT"))
        except Exception as exception:
            cls.fixture_log.critical('Exception occured while performing '
                                     'a SOFT REBOOT on the server.')
            raise cls.assertClassSetupFailure(exception)
        try:
            # generate bandwidth
            (cls.compute_provider
             .do_bandwidth_server_to_client(cls.created_server,
                                            cls.gb_file_size))
        except Exception as exception:
            cls.fixture_log.critical('Exception occured while transferring '
                                     'bandwidth from server to local client.')
            raise cls.assertClassSetupFailure(exception)


class BwBeforeAndAfterSoftRebootServerFixture(BwComputeFixture):
    '''
    @summary: Creates a server, waits for active state.
        Transfers bandwidth. Then soft reboots the server.
        Transfers bandwidth again.
    '''

    @classmethod
    def setUpClass(cls):
        # create server
        super(BwBeforeAndAfterSoftRebootServerFixture, cls).setUpClass()
        try:
            # generate bandwidth
            (cls.compute_provider
             .do_bandwidth_server_to_client(cls.created_server,
                                            cls.gb_file_size))
        except Exception as exception:
            cls.fixture_log.critical('Exception occured while transferring '
                                     'bandwidth from server to local client.')
            raise cls.assertClassSetupFailure(exception)
        try:
            # do soft reboot
            cls.rebooted_server = \
                (cls.compute_provider
                 .reboot_and_await(server_id=cls.created_server.id,
                                   reboot_type="SOFT"))
        except Exception as exception:
            cls.fixture_log.critical('Exception occured while performing '
                                     'a SOFT REBOOT on the server.')
            raise cls.assertClassSetupFailure(exception)
        try:
            # generate bandwidth
            (cls.compute_provider
             .do_bandwidth_server_to_client(cls.created_server,
                                            cls.gb_file_size))
        except Exception as exception:
            cls.fixture_log.critical('Exception occured while transferring '
                                     'bandwidth from server to local client.')
            raise cls.assertClassSetupFailure(exception)


class NoBwSoftRebootServerFixture(BwComputeFixture):
    '''
    @summary: Creates a server, waits for active state.
        Then soft reboots the server. Does not transfers any bandwidth.
    '''

    @classmethod
    def setUpClass(cls):
        # create server
        super(NoBwSoftRebootServerFixture, cls).setUpClass()
        try:
            # do soft reboot
            cls.rebooted_server = \
                (cls.compute_provider
                 .reboot_and_await(server_id=cls.created_server.id,
                                   reboot_type="SOFT"))
        except Exception as exception:
            cls.fixture_log.critical('Exception occured while performing '
                                     'a SOFT REBOOT on the server.')
            raise cls.assertClassSetupFailure(exception)


class BwBeforeHardRebootServerFixture(BwComputeFixture):
    '''
    @summary: Creates a server, waits for active state.
        Transfers some bandwidth.  Then reboots the server.
    @todo: Check all immediate exists events in AH
    '''

    @classmethod
    def setUpClass(cls):
        # create server
        super(BwBeforeHardRebootServerFixture, cls).setUpClass()
        try:
            # generate bandwidth
            (cls.compute_provider
             .do_bandwidth_server_to_client(cls.created_server,
                                            cls.gb_file_size))
        except Exception as exception:
            cls.fixture_log.critical('Exception occured while transferring '
                                     'bandwidth from server to local client.')
            raise cls.assertClassSetupFailure(exception)
        try:
            # do hard reboot
            cls.rebooted_server = \
                (cls.compute_provider
                 .reboot_and_await(server_id=cls.created_server.id,
                                   reboot_type="HARD"))
        except Exception as exception:
            cls.fixture_log.critical('Exception occured while performing '
                                     'a HARD REBOOT on the server.')
            raise cls.assertClassSetupFailure(exception)


class BwAfterHardRebootServerFixture(BwComputeFixture):
    '''
    @summary: Creates a server, waits for active state.
        Then reboots the server.  Transfers bandwidth.
    @todo: Check all immediate exists events in AH
    '''

    @classmethod
    def setUpClass(cls):
        # create server
        super(BwAfterHardRebootServerFixture, cls).setUpClass()
        try:
            # do hard reboot
            cls.rebooted_server = \
                (cls.compute_provider
                 .reboot_and_await(server_id=cls.created_server.id,
                                   reboot_type="HARD"))
        except Exception as exception:
            cls.fixture_log.critical('Exception occured while performing '
                                     'a HARD REBOOT on the server.')
            raise cls.assertClassSetupFailure(exception)
        try:
            # generate bandwidth
            (cls.compute_provider
             .do_bandwidth_server_to_client(cls.created_server,
                                            cls.gb_file_size))
        except Exception as exception:
            cls.fixture_log.critical('Exception occured while transferring '
                                     'bandwidth from server to local client.')
            raise cls.assertClassSetupFailure(exception)


class BwBeforeAndAfterHardRebootServerFixture(BwComputeFixture):
    '''
    @summary: Creates a server, waits for active state.
        Transfers bandwidth. Then reboots the server.
        Transfers bandwidth again.
    @todo: Check all immediate exists events in AH
    '''

    @classmethod
    def setUpClass(cls):
        # create server
        super(BwBeforeAndAfterHardRebootServerFixture, cls).setUpClass()
        try:
            # generate bandwidth
            (cls.compute_provider
             .do_bandwidth_server_to_client(cls.created_server,
                                            cls.gb_file_size))
        except Exception as exception:
            cls.fixture_log.critical('Exception occured while transferring '
                                     'bandwidth from server to local client.')
            raise cls.assertClassSetupFailure(exception)
        try:
            # do hard reboot
            cls.rebooted_server = \
                (cls.compute_provider
                 .reboot_and_await(server_id=cls.created_server.id,
                                   reboot_type="HARD"))
        except Exception as exception:
            cls.fixture_log.critical('Exception occured while performing '
                                     'a HARD REBOOT on the server.')
            raise cls.assertClassSetupFailure(exception)
        try:
            # generate bandwidth
            (cls.compute_provider
             .do_bandwidth_server_to_client(cls.created_server,
                                            cls.gb_file_size))
        except Exception as exception:
            cls.fixture_log.critical('Exception occured while transferring '
                                     'bandwidth from server to local client.')
            raise cls.assertClassSetupFailure(exception)


class NoBwHardRebootServerFixture(BwComputeFixture):
    '''
    @summary: Creates a server, waits for active state.
        Then reboots the server. Does not transfers any bandwidth.
    @todo: Check all immediate exists events in AH
    '''

    @classmethod
    def setUpClass(cls):
        # create server
        super(NoBwHardRebootServerFixture, cls).setUpClass()
        try:
            # do hard reboot
            cls.rebooted_server = \
                (cls.compute_provider
                 .reboot_and_await(server_id=cls.created_server.id,
                                   reboot_type="HARD"))
        except Exception as exception:
            cls.fixture_log.critical('Exception occured while performing '
                                     'a HARD REBOOT on the server.')
            raise cls.assertClassSetupFailure(exception)


class BwBeforeRebuildServerFixture(BwComputeFixture):
    '''
    @summary: Creates a server, waits for active state. Transfers some
        bandwidth. Then rebuilds the server.
    @todo: Check all immediate exists events in AH
    @note: audit period ending is when we made the request to rebuild
        or the start time of the wait response
    '''

    @classmethod
    def setUpClass(cls):
        # create server
        super(BwBeforeRebuildServerFixture, cls).setUpClass()
        try:
            # generate bandwidth
            (cls.compute_provider
             .do_bandwidth_server_to_client(cls.created_server,
                                            cls.gb_file_size))
        except Exception as exception:
            cls.fixture_log.critical('Exception occured while transferring '
                                     'bandwidth from server to local client.')
            raise cls.assertClassSetupFailure(exception)
        try:
            # do rebuild
            (cls.rebuilt_server,
             cls.expected_audit_period_ending,
             cls.launched_at_rebuilt_server) = (cls.compute_provider
                .rebuild_and_await(server_id=cls.created_server.id,
                                   image_ref=cls.image_ref_alt))
        except Exception as exception:
            cls.fixture_log.critical('Exception occured while performing '
                                     'a REBUILD on the server.\n'
                                     'instance uuid: {0} \n'
                                     'original image: {1} \n'
                                     'rebuild image: {2} \n'
                                     .format(cls.created_server.id,
                                             cls.image_ref,
                                             cls.image_ref_alt))
            raise cls.assertClassSetupFailure(exception)


class BwAfterRebuildServerFixture(BwComputeFixture):
    '''
    @summary: Creates a server, waits for active state. Rebuilds the
        server. Then, transfers some bandwidth.
    @todo: Check all immediate exists events in AH
    @note: audit period ending is when we made the request to rebuild
        or the start time of the wait response
    '''

    @classmethod
    def setUpClass(cls):
        # create server
        super(BwAfterRebuildServerFixture, cls).setUpClass()
        try:
            # do rebuild
            (cls.rebuilt_server,
             cls.expected_audit_period_ending,
             cls.launched_at_rebuilt_server) = (cls.compute_provider
                .rebuild_and_await(server_id=cls.created_server.id,
                                   image_ref=cls.image_ref_alt,
                                   admin_pass=cls.new_password))
        except Exception as exception:
            cls.fixture_log.critical('Exception occured while performing '
                                     'a REBUILD on the server.\n'
                                     'instance uuid: {0} \n'
                                     'original image: {1} \n'
                                     'rebuild image: {2} \n'
                                     .format(cls.created_server.id,
                                             cls.image_ref,
                                             cls.image_ref_alt))
            raise cls.assertClassSetupFailure(exception)
        cls.created_server.adminPass = cls.new_password
        try:
            # generate bandwidth
            (cls.compute_provider
             .do_bandwidth_server_to_client(cls.created_server,
                                            cls.gb_file_size))
        except Exception as exception:
            cls.fixture_log.critical('Exception occured while transferring '
                                     'bandwidth from server to local client.')
            raise cls.assertClassSetupFailure(exception)


class BwBeforeAndAfterRebuildServerFixture(BwComputeFixture):
    '''
    @summary: Creates a server, waits for active state. Transfers
        some bandwidth. Rebuilds the server. Finally, transfers
        some bandwidth.
    @todo: Check all immediate exists events in AH
    @note: audit period ending is when we made the request to rebuild
        or the start time of the wait response
    '''

    @classmethod
    def setUpClass(cls):
        # create server
        super(BwBeforeAndAfterRebuildServerFixture, cls).setUpClass()
        try:
            # generate bandwidth
            (cls.compute_provider
             .do_bandwidth_server_to_client(cls.created_server,
                                            cls.gb_file_size))
        except Exception as exception:
            cls.fixture_log.critical('Exception occured while transferring '
                                     'bandwidth from server to local client.')
            raise cls.assertClassSetupFailure(exception)
        try:
            # do rebuild
            (cls.rebuilt_server,
             cls.expected_audit_period_ending,
             cls.launched_at_rebuilt_server) = (cls.compute_provider
                .rebuild_and_await(server_id=cls.created_server.id,
                                   image_ref=cls.image_ref_alt,
                                   admin_pass=cls.new_password))
        except Exception as exception:
            cls.fixture_log.critical('Exception occured while performing '
                                     'a REBUILD on the server.\n'
                                     'instance uuid: {0} \n'
                                     'original image: {1} \n'
                                     'rebuild image: {2} \n'
                                     .format(cls.created_server.id,
                                             cls.image_ref,
                                             cls.image_ref_alt))
            raise cls.assertClassSetupFailure(exception)
        cls.created_server.adminPass = cls.new_password
        try:
            # generate bandwidth
            (cls.compute_provider
             .do_bandwidth_server_to_client(cls.created_server,
                                            cls.gb_file_size))
        except Exception as exception:
            cls.fixture_log.critical('Exception occured while transferring '
                                     'bandwidth from server to local client.')
            raise cls.assertClassSetupFailure(exception)


class NoBwRebuildServerFixture(BwComputeFixture):
    '''
    @summary: Creates a server, waits for active state. Then rebuilds
        the server.  Does not transfers any bandwidth.
    @todo: Check all immediate exists events in AH
    @note: audit period ending is when we made the request to rebuild
        or the start time of the wait response
    '''

    @classmethod
    def setUpClass(cls):
        # create server
        super(NoBwRebuildServerFixture, cls).setUpClass()
        try:
            # do rebuild
            (cls.rebuilt_server,
             cls.expected_audit_period_ending,
             cls.launched_at_rebuilt_server) = (cls.compute_provider
                .rebuild_and_await(server_id=cls.created_server.id,
                                   image_ref=cls.image_ref_alt))
        except Exception as exception:
            cls.fixture_log.critical('Exception occured while performing '
                                     'a REBUILD on the server.\n'
                                     'instance uuid: {0} \n'
                                     'original image: {1} \n'
                                     'rebuild image: {2} \n'
                                     .format(cls.created_server.id,
                                             cls.image_ref,
                                             cls.image_ref_alt))
            raise cls.assertClassSetupFailure(exception)


class BwBeforeResizeDownNoConfirmServerFixture(BwComputeFixture):
    '''
    @summary: Creates a server, waits for active state. Transfers some
        bandwidth. Then resizes the server down. Does not confirm resize.
    @note: audit period ending is when we made the request to resize
        or the start time of the wait response
    '''

    @classmethod
    def setUpClass(cls):
        cls.config = _MCP()
        cls.flavor_ref_alt = cls.config.compute_api.flavor_ref_alt
        # create server
        (super(BwBeforeResizeDownNoConfirmServerFixture, cls)
         .setUpClass(flavorRef=cls.flavor_ref_alt))
        try:
            # generate bandwidth
            (cls.compute_provider
             .do_bandwidth_server_to_client(cls.created_server,
                                            cls.gb_file_size))
        except Exception as exception:
            cls.fixture_log.critical('Exception occured while transferring '
                                     'bandwidth from server to local client.')
            raise cls.assertClassSetupFailure(exception)
        try:
            # do resize down
            (cls.resized_server,
             cls.expected_audit_period_ending,
             cls.launched_at_resized_server) = (cls.compute_provider
                .resize_and_await(server_id=cls.created_server.id,
                                  new_flavor=cls.flavor_ref))
        except Exception as exception:
            cls.fixture_log.critical('Exception occured while performing a '
                                     'RESIZE DOWN NO CONFIRM on the server.\n'
                                     'instance uuid: {0} \n'
                                     'original flavor: {1} \n'
                                     'resize flavor: {2} \n'
                                     .format(cls.created_server.id,
                                             cls.flavor_ref_alt,
                                             cls.flavor_ref))
            raise cls.assertClassSetupFailure(exception)


class BwAfterResizeDownNoConfirmServerFixture(BwComputeFixture):
    '''
    @summary: Creates a server, waits for active state. Then,
        resizes the server down. Does not confirm resize. Finally,
        transfers some bandwidth.
    @note: audit period ending is when we made the request to resize
        or the start time of the wait response
    '''

    @classmethod
    def setUpClass(cls):
        cls.config = _MCP()
        cls.flavor_ref_alt = cls.config.compute_api.flavor_ref_alt
        # create server
        (super(BwAfterResizeDownNoConfirmServerFixture, cls)
         .setUpClass(flavorRef=cls.flavor_ref_alt))
        try:
            # do resize down
            (cls.resized_server,
             cls.expected_audit_period_ending,
             cls.launched_at_resized_server) = (cls.compute_provider
                .resize_and_await(server_id=cls.created_server.id,
                                  new_flavor=cls.flavor_ref))
        except Exception as exception:
            cls.fixture_log.critical('Exception occured while performing a '
                                     'RESIZE DOWN NO CONFIRM on the server.\n'
                                     'instance uuid: {0} \n'
                                     'original flavor: {1} \n'
                                     'resize flavor: {2} \n'
                                     .format(cls.created_server.id,
                                             cls.flavor_ref_alt,
                                             cls.flavor_ref))
            raise cls.assertClassSetupFailure(exception)
        try:
            # generate bandwidth
            (cls.compute_provider
             .do_bandwidth_server_to_client(cls.created_server,
                                            cls.gb_file_size))
        except Exception as exception:
            cls.fixture_log.critical('Exception occured while transferring '
                                     'bandwidth from server to local client.')
            raise cls.assertClassSetupFailure(exception)


class BwBeforeAndAfterResizeDownNoConfirmServerFixture(BwComputeFixture):
    '''
    @summary: Creates a server, waits for active state. Transfers
        some bandwidth. Then, resizes the server down. Does not confirm resize.
        Finally, transfers some bandwidth.
    @note: audit period ending is when we made the request to resize
        or the start time of the wait response
    '''

    @classmethod
    def setUpClass(cls):
        cls.config = _MCP()
        cls.flavor_ref_alt = cls.config.compute_api.flavor_ref_alt
        # create server
        (super(BwBeforeAndAfterResizeDownNoConfirmServerFixture, cls)
         .setUpClass(flavorRef=cls.flavor_ref_alt))
        try:
            # generate bandwidth
            (cls.compute_provider
             .do_bandwidth_server_to_client(cls.created_server,
                                            cls.gb_file_size))
        except Exception as exception:
            cls.fixture_log.critical('Exception occured while transferring '
                                     'bandwidth from server to local client.')
            raise cls.assertClassSetupFailure(exception)
        try:
            # do resize down
            (cls.resized_server,
             cls.expected_audit_period_ending,
             cls.launched_at_resized_server) = (cls.compute_provider
                .resize_and_await(server_id=cls.created_server.id,
                                  new_flavor=cls.flavor_ref))
        except Exception as exception:
            cls.fixture_log.critical('Exception occured while performing a '
                                     'RESIZE DOWN NO CONFIRM on the server.\n'
                                     'instance uuid: {0} \n'
                                     'original flavor: {1} \n'
                                     'resize flavor: {2} \n'
                                     .format(cls.created_server.id,
                                             cls.flavor_ref_alt,
                                             cls.flavor_ref))
            raise cls.assertClassSetupFailure(exception)
        try:
            # generate bandwidth
            (cls.compute_provider
             .do_bandwidth_server_to_client(cls.created_server,
                                            cls.gb_file_size))
        except Exception as exception:
            cls.fixture_log.critical('Exception occured while transferring '
                                     'bandwidth from server to local client.')
            raise cls.assertClassSetupFailure(exception)


class NoBwResizeDownNoConfirmServerFixture(BwComputeFixture):
    '''
    @summary: Creates a server, waits for active state. Then,
        resizes the server down. Does not confirm resize.
        Does not transfers any bandwidth.
    @note: audit period ending is when we made the request to resize
        or the start time of the wait response
    '''

    @classmethod
    def setUpClass(cls):
        cls.config = _MCP()
        cls.flavor_ref_alt = cls.config.compute_api.flavor_ref_alt
        # create server
        (super(NoBwResizeDownNoConfirmServerFixture, cls)
         .setUpClass(flavorRef=cls.flavor_ref_alt))
        try:
            # do resize down
            (cls.resized_server,
             cls.expected_audit_period_ending,
             cls.launched_at_resized_server) = (cls.compute_provider
                .resize_and_await(server_id=cls.created_server.id,
                                  new_flavor=cls.flavor_ref))
        except Exception as exception:
            cls.fixture_log.critical('Exception occured while performing a '
                                     'RESIZE DOWN NO CONFIRM on the server.\n'
                                     'instance uuid: {0} \n'
                                     'original flavor: {1} \n'
                                     'resize flavor: {2} \n'
                                     .format(cls.created_server.id,
                                             cls.flavor_ref_alt,
                                             cls.flavor_ref))
            raise cls.assertClassSetupFailure(exception)


class BwBeforeResizeDownConfirmServerFixture(BwComputeFixture):
    '''
    @summary: Creates a server, waits for active state. Transfers some
        bandwidth. Then resizes the server down. Confirms resize.
    @note: audit period ending is when we made the request to resize
        or the start time of the wait response
    '''

    @classmethod
    def setUpClass(cls):
        cls.config = _MCP()
        cls.flavor_ref_alt = cls.config.compute_api.flavor_ref_alt
        # create server
        (super(BwBeforeResizeDownConfirmServerFixture, cls)
         .setUpClass(flavorRef=cls.flavor_ref_alt))
        try:
            # generate bandwidth
            (cls.compute_provider
             .do_bandwidth_server_to_client(cls.created_server,
                                            cls.gb_file_size))
        except Exception as exception:
            cls.fixture_log.critical('Exception occured while transferring '
                                     'bandwidth from server to local client.')
            raise cls.assertClassSetupFailure(exception)
        try:
            # do resize down and confirm
            (cls.resized_server,
             cls.expected_audit_period_ending,
             cls.launched_at_resized_server) = (cls.compute_provider
                .resize_and_confirm(server_id=cls.created_server.id,
                                    new_flavor=cls.flavor_ref))
        except Exception as exception:
            cls.fixture_log.critical('Exception occured while performing a '
                                     'RESIZE DOWN CONFIRM on the server.\n'
                                     'instance uuid: {0} \n'
                                     'original flavor: {1} \n'
                                     'resize flavor: {2} \n'
                                     .format(cls.created_server.id,
                                             cls.flavor_ref_alt,
                                             cls.flavor_ref))
            raise cls.assertClassSetupFailure(exception)


class BwAfterResizeDownConfirmServerFixture(BwComputeFixture):
    '''
    @summary: Creates a server, waits for active state. Then,
        resizes the server down. Confirms resize. Finally,
        transfers some bandwidth.
    @note: audit period ending is when we made the request to resize
        or the start time of the wait response
    '''

    @classmethod
    def setUpClass(cls):
        cls.config = _MCP()
        cls.flavor_ref_alt = cls.config.compute_api.flavor_ref_alt
        # create server
        (super(BwAfterResizeDownConfirmServerFixture, cls)
         .setUpClass(flavorRef=cls.flavor_ref_alt))
        try:
            # do resize down and confirm
            (cls.resized_server,
             cls.expected_audit_period_ending,
             cls.launched_at_resized_server) = (cls.compute_provider
                .resize_and_confirm(server_id=cls.created_server.id,
                                    new_flavor=cls.flavor_ref))
        except Exception as exception:
            cls.fixture_log.critical('Exception occured while performing a '
                                     'RESIZE DOWN CONFIRM on the server.\n'
                                     'instance uuid: {0} \n'
                                     'original flavor: {1} \n'
                                     'resize flavor: {2} \n'
                                     .format(cls.created_server.id,
                                             cls.flavor_ref_alt,
                                             cls.flavor_ref))
            raise cls.assertClassSetupFailure(exception)
        try:
            # generate bandwidth
            (cls.compute_provider
             .do_bandwidth_server_to_client(cls.created_server,
                                            cls.gb_file_size))
        except Exception as exception:
            cls.fixture_log.critical('Exception occured while transferring '
                                     'bandwidth from server to local client.')
            raise cls.assertClassSetupFailure(exception)


class BwBeforeAndAfterResizeDownConfirmServerFixture(BwComputeFixture):
    '''
    @summary: Creates a server, waits for active state. Transfers
        some bandwidth. Then, resizes the server down. Confirms resize.
        Finally, transfers some bandwidth.
    @note: audit period ending is when we made the request to resize
        or the start time of the wait response
    '''

    @classmethod
    def setUpClass(cls):
        cls.config = _MCP()
        cls.flavor_ref_alt = cls.config.compute_api.flavor_ref_alt
        # create server
        (super(BwBeforeAndAfterResizeDownConfirmServerFixture, cls)
         .setUpClass(flavorRef=cls.flavor_ref_alt))
        try:
            # generate bandwidth
            (cls.compute_provider
             .do_bandwidth_server_to_client(cls.created_server,
                                            cls.gb_file_size))
        except Exception as exception:
            cls.fixture_log.critical('Exception occured while transferring '
                                     'bandwidth from server to local client.')
            raise cls.assertClassSetupFailure(exception)
        try:
            # do resize down and confirm
            (cls.resized_server,
             cls.expected_audit_period_ending,
             cls.launched_at_resized_server) = (cls.compute_provider
                .resize_and_confirm(server_id=cls.created_server.id,
                                    new_flavor=cls.flavor_ref))
        except Exception as exception:
            cls.fixture_log.critical('Exception occured while performing a '
                                     'RESIZE DOWN CONFIRM on the server.\n'
                                     'instance uuid: {0} \n'
                                     'original flavor: {1} \n'
                                     'resize flavor: {2} \n'
                                     .format(cls.created_server.id,
                                             cls.flavor_ref_alt,
                                             cls.flavor_ref))
            raise cls.assertClassSetupFailure(exception)
        try:
            # generate bandwidth
            (cls.compute_provider
             .do_bandwidth_server_to_client(cls.created_server,
                                            cls.gb_file_size))
        except Exception as exception:
            cls.fixture_log.critical('Exception occured while transferring '
                                     'bandwidth from server to local client.')
            raise cls.assertClassSetupFailure(exception)


class NoBwResizeDownConfirmServerFixture(BwComputeFixture):
    '''
    @summary: Creates a server, waits for active state. Then,
        resizes the server down. Confirms resize.
        Does not transfers any bandwidth.
    @note: audit period ending is when we made the request to resize
        or the start time of the wait response
    '''

    @classmethod
    def setUpClass(cls):
        cls.config = _MCP()
        cls.flavor_ref_alt = cls.config.compute_api.flavor_ref_alt
        # create server
        (super(NoBwResizeDownConfirmServerFixture, cls)
         .setUpClass(flavorRef=cls.flavor_ref_alt))
        try:
            # do resize down and confirm
            (cls.resized_server,
             cls.expected_audit_period_ending,
             cls.launched_at_resized_server) = (cls.compute_provider
                .resize_and_confirm(server_id=cls.created_server.id,
                                    new_flavor=cls.flavor_ref))
        except Exception as exception:
            cls.fixture_log.critical('Exception occured while performing a '
                                     'RESIZE DOWN CONFIRM on the server.\n'
                                     'instance uuid: {0} \n'
                                     'original flavor: {1} \n'
                                     'resize flavor: {2} \n'
                                     .format(cls.created_server.id,
                                             cls.flavor_ref_alt,
                                             cls.flavor_ref))
            raise cls.assertClassSetupFailure(exception)


class BwBeforeResizeUpNoConfirmServerFixture(BwComputeFixture):
    '''
    @summary: Creates a server, waits for active state. Transfers some
        bandwidth. Then resizes the server up. Does not confirm resize.
    @note: audit period ending is when we made the request to resize
        or the start time of the wait response
    '''

    @classmethod
    def setUpClass(cls):
        # create server
        super(BwBeforeResizeUpNoConfirmServerFixture, cls).setUpClass()
        try:
            # generate bandwidth
            (cls.compute_provider
             .do_bandwidth_server_to_client(cls.created_server,
                                            cls.gb_file_size))
        except Exception as exception:
            cls.fixture_log.critical('Exception occured while transferring '
                                     'bandwidth from server to local client.')
            raise cls.assertClassSetupFailure(exception)
        try:
            # do resize up
            (cls.resized_server,
             cls.expected_audit_period_ending,
             cls.launched_at_resized_server) = (cls.compute_provider
                .resize_and_await(server_id=cls.created_server.id,
                                  new_flavor=cls.flavor_ref_alt))
        except Exception as exception:
            cls.fixture_log.critical('Exception occured while performing a '
                                     'RESIZE UP NO CONFIRM on the server.\n'
                                     'instance uuid: {0} \n'
                                     'original flavor: {1} \n'
                                     'resize flavor: {2} \n'
                                     .format(cls.created_server.id,
                                             cls.flavor_ref,
                                             cls.flavor_ref_alt))
            raise cls.assertClassSetupFailure(exception)


class BwAfterResizeUpNoConfirmServerFixture(BwComputeFixture):
    '''
    @summary: Creates a server, waits for active state. Then,
        resizes the server up. Does not confirm resize. Finally,
        transfers some bandwidth.
    @note: audit period ending is when we made the request to resize
        or the start time of the wait response
    '''

    @classmethod
    def setUpClass(cls):
        # create server
        super(BwAfterResizeUpNoConfirmServerFixture, cls).setUpClass()
        try:
            # do resize up
            (cls.resized_server,
             cls.expected_audit_period_ending,
             cls.launched_at_resized_server) = (cls.compute_provider
                .resize_and_await(server_id=cls.created_server.id,
                                  new_flavor=cls.flavor_ref_alt))
        except Exception as exception:
            cls.fixture_log.critical('Exception occured while performing a '
                                     'RESIZE UP NO CONFIRM on the server.\n'
                                     'instance uuid: {0} \n'
                                     'original flavor: {1} \n'
                                     'resize flavor: {2} \n'
                                     .format(cls.created_server.id,
                                             cls.flavor_ref,
                                             cls.flavor_ref_alt))
            raise cls.assertClassSetupFailure(exception)
        try:
            # generate bandwidth
            (cls.compute_provider
             .do_bandwidth_server_to_client(cls.created_server,
                                            cls.gb_file_size))
        except Exception as exception:
            cls.fixture_log.critical('Exception occured while transferring '
                                     'bandwidth from server to local client.')
            raise cls.assertClassSetupFailure(exception)


class BwBeforeAndAfterResizeUpNoConfirmServerFixture(BwComputeFixture):
    '''
    @summary: Creates a server, waits for active state. Transfers
        some bandwidth. Then, resizes the server up. Does not confirm resize.
        Finally, transfers some bandwidth.
    @note: audit period ending is when we made the request to resize
        or the start time of the wait response
    '''

    @classmethod
    def setUpClass(cls):
        # create server
        super(BwBeforeAndAfterResizeUpNoConfirmServerFixture, cls).setUpClass()
        try:
            # generate bandwidth
            (cls.compute_provider
             .do_bandwidth_server_to_client(cls.created_server,
                                            cls.gb_file_size))
        except Exception as exception:
            cls.fixture_log.critical('Exception occured while transferring '
                                     'bandwidth from server to local client.')
            raise cls.assertClassSetupFailure(exception)
        try:
            # do resize up
            (cls.resized_server,
             cls.expected_audit_period_ending,
             cls.launched_at_resized_server) = (cls.compute_provider
                .resize_and_await(server_id=cls.created_server.id,
                                  new_flavor=cls.flavor_ref_alt))
        except Exception as exception:
            cls.fixture_log.critical('Exception occured while performing a '
                                     'RESIZE UP NO CONFIRM on the server.\n'
                                     'instance uuid: {0} \n'
                                     'original flavor: {1} \n'
                                     'resize flavor: {2} \n'
                                     .format(cls.created_server.id,
                                             cls.flavor_ref,
                                             cls.flavor_ref_alt))
            raise cls.assertClassSetupFailure(exception)
        try:
            # generate bandwidth
            (cls.compute_provider
             .do_bandwidth_server_to_client(cls.created_server,
                                            cls.gb_file_size))
        except Exception as exception:
            cls.fixture_log.critical('Exception occured while transferring '
                                     'bandwidth from server to local client.')
            raise cls.assertClassSetupFailure(exception)


class NoBwResizeUpNoConfirmServerFixture(BwComputeFixture):
    '''
    @summary: Creates a server, waits for active state. Then,
        resizes the server up. Does not confirm resize.
        Does not transfers any bandwidth.
    @note: audit period ending is when we made the request to resize
        or the start time of the wait response
    '''

    @classmethod
    def setUpClass(cls):
        # create server
        super(NoBwResizeUpNoConfirmServerFixture, cls).setUpClass()
        try:
            # do resize up
            (cls.resized_server,
             cls.expected_audit_period_ending,
             cls.launched_at_resized_server) = (cls.compute_provider
                .resize_and_await(server_id=cls.created_server.id,
                                  new_flavor=cls.flavor_ref_alt))
        except Exception as exception:
            cls.fixture_log.critical('Exception occured while performing a '
                                     'RESIZE UP NO CONFIRM on the server.\n'
                                     'instance uuid: {0} \n'
                                     'original flavor: {1} \n'
                                     'resize flavor: {2} \n'
                                     .format(cls.created_server.id,
                                             cls.flavor_ref,
                                             cls.flavor_ref_alt))
            raise cls.assertClassSetupFailure(exception)


class BwBeforeResizeUpConfirmServerFixture(BwComputeFixture):
    '''
    @summary: Creates a server, waits for active state. Transfers some
        bandwidth. Then resizes the server up.  Confirms resize.
    @note: audit period ending is when we made the request to resize
        or the start time of the wait response
    '''

    @classmethod
    def setUpClass(cls):
        # create server
        super(BwBeforeResizeUpConfirmServerFixture, cls).setUpClass()
        try:
            # generate bandwidth
            (cls.compute_provider
             .do_bandwidth_server_to_client(cls.created_server,
                                            cls.gb_file_size))
        except Exception as exception:
            cls.fixture_log.critical('Exception occured while transferring '
                                     'bandwidth from server to local client.')
            raise cls.assertClassSetupFailure(exception)
        try:
            # do resize up and confirm
            (cls.resized_server,
             cls.expected_audit_period_ending,
             cls.launched_at_resized_server) = (cls.compute_provider
                .resize_and_confirm(server_id=cls.created_server.id,
                                    new_flavor=cls.flavor_ref_alt))
        except Exception as exception:
            cls.fixture_log.critical('Exception occured while performing a '
                                     'RESIZE UP CONFIRM on the server.\n'
                                     'instance uuid: {0} \n'
                                     'original flavor: {1} \n'
                                     'resize flavor: {2} \n'
                                     .format(cls.created_server.id,
                                             cls.flavor_ref,
                                             cls.flavor_ref_alt))
            raise cls.assertClassSetupFailure(exception)


class BwAfterResizeUpConfirmServerFixture(BwComputeFixture):
    '''
    @summary: Creates a server, waits for active state. Then,
        resizes the server up. Confirms resize. Finally,
        transfers some bandwidth.
    @note: audit period ending is when we made the request to resize
        or the start time of the wait response
    '''

    @classmethod
    def setUpClass(cls):
        # create server
        super(BwAfterResizeUpConfirmServerFixture, cls).setUpClass()
        try:
            # do resize up and confirm
            (cls.resized_server,
             cls.expected_audit_period_ending,
             cls.launched_at_resized_server) = (cls.compute_provider
                .resize_and_confirm(server_id=cls.created_server.id,
                                    new_flavor=cls.flavor_ref_alt))
        except Exception as exception:
            cls.fixture_log.critical('Exception occured while performing a '
                                     'RESIZE UP CONFIRM on the server.\n'
                                     'instance uuid: {0} \n'
                                     'original flavor: {1} \n'
                                     'resize flavor: {2} \n'
                                     .format(cls.created_server.id,
                                             cls.flavor_ref,
                                             cls.flavor_ref_alt))
            raise cls.assertClassSetupFailure(exception)
        try:
            # generate bandwidth
            (cls.compute_provider
             .do_bandwidth_server_to_client(cls.created_server,
                                            cls.gb_file_size))
        except Exception as exception:
            cls.fixture_log.critical('Exception occured while transferring '
                                     'bandwidth from server to local client.')
            raise cls.assertClassSetupFailure(exception)


class BwBeforeAndAfterResizeUpConfirmServerFixture(BwComputeFixture):
    '''
    @summary: Creates a server, waits for active state. Transfers
        some bandwidth. Then, resizes the server up. Confirms resize.
        Finally, transfers some bandwidth.
    @note: audit period ending is when we made the request to resize
        or the start time of the wait response
    '''

    @classmethod
    def setUpClass(cls):
        # create server
        super(BwBeforeAndAfterResizeUpConfirmServerFixture, cls).setUpClass()
        try:
            # generate bandwidth
            (cls.compute_provider
             .do_bandwidth_server_to_client(cls.created_server,
                                            cls.gb_file_size))
        except Exception as exception:
            cls.fixture_log.critical('Exception occured while transferring '
                                     'bandwidth from server to local client.')
            raise cls.assertClassSetupFailure(exception)
        try:
            # do resize up and confirm
            (cls.resized_server,
             cls.expected_audit_period_ending,
             cls.launched_at_resized_server) = (cls.compute_provider
                .resize_and_confirm(server_id=cls.created_server.id,
                                    new_flavor=cls.flavor_ref_alt))
        except Exception as exception:
            cls.fixture_log.critical('Exception occured while performing a '
                                     'RESIZE UP CONFIRM on the server.\n'
                                     'instance uuid: {0} \n'
                                     'original flavor: {1} \n'
                                     'resize flavor: {2} \n'
                                     .format(cls.created_server.id,
                                             cls.flavor_ref,
                                             cls.flavor_ref_alt))
            raise cls.assertClassSetupFailure(exception)
        try:
            # generate bandwidth
            (cls.compute_provider
             .do_bandwidth_server_to_client(cls.created_server,
                                            cls.gb_file_size))
        except Exception as exception:
            cls.fixture_log.critical('Exception occured while transferring '
                                     'bandwidth from server to local client.')
            raise cls.assertClassSetupFailure(exception)


class NoBwResizeUpConfirmServerFixture(BwComputeFixture):
    '''
    @summary: Creates a server, waits for active state. Then,
        resizes the server up. Confirms resize.
        Does not transfer any bandwidth.
    @note: audit period ending is when we made the request to resize
        or the start time of the wait response
    '''

    @classmethod
    def setUpClass(cls):
        # create server
        super(NoBwResizeUpConfirmServerFixture, cls).setUpClass()
        try:
            # do resize up and confirm
            (cls.resized_server,
             cls.expected_audit_period_ending,
             cls.launched_at_resized_server) = (cls.compute_provider
                .resize_and_confirm(server_id=cls.created_server.id,
                                    new_flavor=cls.flavor_ref_alt))
        except Exception as exception:
            cls.fixture_log.critical('Exception occured while performing a '
                                     'RESIZE UP CONFIRM on the server.\n'
                                     'instance uuid: {0} \n'
                                     'original flavor: {1} \n'
                                     'resize flavor: {2} \n'
                                     .format(cls.created_server.id,
                                             cls.flavor_ref,
                                             cls.flavor_ref_alt))
            raise cls.assertClassSetupFailure(exception)


class BwBeforeResizeDownRevertServerFixture(BwComputeFixture):
    '''
    @summary: Creates a server, waits for active state. Transfers some
        bandwidth. Then resizes the server down. Reverts the resize back
        to the original flavor.
    @note: audit period ending is when we made the request to resize
        or the start time of the wait response
    '''

    @classmethod
    def setUpClass(cls):
        cls.config = _MCP()
        cls.flavor_ref_alt = cls.config.compute_api.flavor_ref_alt
        # create server
        (super(BwBeforeResizeDownRevertServerFixture, cls)
         .setUpClass(flavorRef=cls.flavor_ref_alt))
        try:
            # generate bandwidth
            (cls.compute_provider
             .do_bandwidth_server_to_client(cls.created_server,
                                            cls.gb_file_size))
        except Exception as exception:
            cls.fixture_log.critical('Exception occured while transferring '
                                     'bandwidth from server to local client.')
            raise cls.assertClassSetupFailure(exception)
        try:
            # do resize down and revert
            (cls.resized_server,
             cls.expected_audit_period_ending,
             cls.launched_at_resized_server,
             cls.reverted_resized_server,
             cls.reverted_expected_audit_period_ending,
             cls.launched_at_reverted_resized_server) = (cls.compute_provider
                .resize_and_revert(server_id=cls.created_server.id,
                                   new_flavor=cls.flavor_ref))
        except Exception as exception:
            cls.fixture_log.critical('Exception occured while performing a '
                                     'RESIZE DOWN REVERT on the server.\n'
                                     'instance uuid: {0} \n'
                                     'original flavor: {1} \n'
                                     'resize flavor: {2} \n'
                                     .format(cls.created_server.id,
                                             cls.flavor_ref_alt,
                                             cls.flavor_ref))
            raise cls.assertClassSetupFailure(exception)


class BwAfterResizeDownRevertServerFixture(BwComputeFixture):
    '''
    @summary: Creates a server, waits for active state. Then,
        resizes the server down. Reverts the resize back to the original
        flavor. Finally, transfers some bandwidth.
    @note: audit period ending is when we made the request to resize
        or the start time of the wait response
    '''

    @classmethod
    def setUpClass(cls):
        cls.config = _MCP()
        cls.flavor_ref_alt = cls.config.compute_api.flavor_ref_alt
        # create server
        (super(BwAfterResizeDownRevertServerFixture, cls)
         .setUpClass(flavorRef=cls.flavor_ref_alt))
        try:
            # do resize down and revert
            (cls.resized_server,
             cls.expected_audit_period_ending,
             cls.launched_at_resized_server,
             cls.reverted_resized_server,
             cls.reverted_expected_audit_period_ending,
             cls.launched_at_reverted_resized_server) = (cls.compute_provider
                .resize_and_revert(server_id=cls.created_server.id,
                                   new_flavor=cls.flavor_ref))
        except Exception as exception:
            cls.fixture_log.critical('Exception occured while performing a '
                                     'RESIZE DOWN REVERT on the server.\n'
                                     'instance uuid: {0} \n'
                                     'original flavor: {1} \n'
                                     'resize flavor: {2} \n'
                                     .format(cls.created_server.id,
                                             cls.flavor_ref_alt,
                                             cls.flavor_ref))
            raise cls.assertClassSetupFailure(exception)
        try:
            # generate bandwidth
            (cls.compute_provider
             .do_bandwidth_server_to_client(cls.created_server,
                                            cls.gb_file_size))
        except Exception as exception:
            cls.fixture_log.critical('Exception occured while transferring '
                                     'bandwidth from server to local client.')
            raise cls.assertClassSetupFailure(exception)


class BwBeforeAndAfterResizeDownRevertServerFixture(BwComputeFixture):
    '''
    @summary: Creates a server, waits for active state. Transfers
        some bandwidth. Then, resizes the server down.  Reverts the resize
        back to the original flavor. Finally, transfers some bandwidth.
    @note: audit period ending is when we made the request to resize
        or the start time of the wait response
    '''

    @classmethod
    def setUpClass(cls):
        cls.config = _MCP()
        cls.flavor_ref_alt = cls.config.compute_api.flavor_ref_alt
        # create server
        (super(BwBeforeAndAfterResizeDownRevertServerFixture, cls)
         .setUpClass(flavorRef=cls.flavor_ref_alt))
        try:
            # generate bandwidth
            (cls.compute_provider
             .do_bandwidth_server_to_client(cls.created_server,
                                            cls.gb_file_size))
        except Exception as exception:
            cls.fixture_log.critical('Exception occured while transferring '
                                     'bandwidth from server to local client.')
            raise cls.assertClassSetupFailure(exception)
        try:
            # do resize down and revert
            (cls.resized_server,
             cls.expected_audit_period_ending,
             cls.launched_at_resized_server,
             cls.reverted_resized_server,
             cls.reverted_expected_audit_period_ending,
             cls.launched_at_reverted_resized_server) = (cls.compute_provider
                .resize_and_revert(server_id=cls.created_server.id,
                                   new_flavor=cls.flavor_ref))
        except Exception as exception:
            cls.fixture_log.critical('Exception occured while performing a '
                                     'RESIZE DOWN REVERT on the server.\n'
                                     'instance uuid: {0} \n'
                                     'original flavor: {1} \n'
                                     'resize flavor: {2} \n'
                                     .format(cls.created_server.id,
                                             cls.flavor_ref_alt,
                                             cls.flavor_ref))
            raise cls.assertClassSetupFailure(exception)
        try:
            # generate bandwidth
            (cls.compute_provider
             .do_bandwidth_server_to_client(cls.created_server,
                                            cls.gb_file_size))
        except Exception as exception:
            cls.fixture_log.critical('Exception occured while transferring '
                                     'bandwidth from server to local client.')
            raise cls.assertClassSetupFailure(exception)


class NoBwResizeDownRevertServerFixture(BwComputeFixture):
    '''
    @summary: Creates a server, waits for active state. Then,
        resizes the server down. Reverts the resize back the the original
        flavor. Does not transfers any bandwidth.
    @note: audit period ending is when we made the request to resize
        or the start time of the wait response
    '''

    @classmethod
    def setUpClass(cls):
        cls.config = _MCP()
        cls.flavor_ref_alt = cls.config.compute_api.flavor_ref_alt
        # create server
        (super(NoBwResizeDownRevertServerFixture, cls)
         .setUpClass(flavorRef=cls.flavor_ref_alt))
        try:
            # do resize down and revert
            (cls.resized_server,
             cls.expected_audit_period_ending,
             cls.launched_at_resized_server,
             cls.reverted_resized_server,
             cls.reverted_expected_audit_period_ending,
             cls.launched_at_reverted_resized_server) = (cls.compute_provider
                .resize_and_revert(server_id=cls.created_server.id,
                                   new_flavor=cls.flavor_ref))
        except Exception as exception:
            cls.fixture_log.critical('Exception occured while performing a '
                                     'RESIZE DOWN REVERT on the server.\n'
                                     'instance uuid: {0} \n'
                                     'original flavor: {1} \n'
                                     'resize flavor: {2} \n'
                                     .format(cls.created_server.id,
                                             cls.flavor_ref_alt,
                                             cls.flavor_ref))
            raise cls.assertClassSetupFailure(exception)


class BwBeforeResizeUpRevertServerFixture(BwComputeFixture):
    '''
    @summary: Creates a server, waits for active state. Transfers some
        bandwidth. Then resizes the server up. Reverts the resize back
        to the original flavor.
    @note: audit period ending is when we made the request to resize
        or the start time of the wait response
    '''

    @classmethod
    def setUpClass(cls):
        # create server
        (super(BwBeforeResizeUpRevertServerFixture, cls).setUpClass())
        try:
            # generate bandwidth
            (cls.compute_provider
             .do_bandwidth_server_to_client(cls.created_server,
                                            cls.gb_file_size))
        except Exception as exception:
            cls.fixture_log.critical('Exception occured while transferring '
                                     'bandwidth from server to local client.')
            raise cls.assertClassSetupFailure(exception)
        try:
            # do resize up and revert
            (cls.resized_server,
             cls.expected_audit_period_ending,
             cls.launched_at_resized_server,
             cls.reverted_resized_server,
             cls.reverted_expected_audit_period_ending,
             cls.launched_at_reverted_resized_server) = (cls.compute_provider
                .resize_and_revert(server_id=cls.created_server.id,
                                   new_flavor=cls.flavor_ref_alt))
        except Exception as exception:
            cls.fixture_log.critical('Exception occured while performing a '
                                     'RESIZE UP REVERT on the server.\n'
                                     'instance uuid: {0} \n'
                                     'original flavor: {1} \n'
                                     'resize flavor: {2} \n'
                                     .format(cls.created_server.id,
                                             cls.flavor_ref,
                                             cls.flavor_ref_alt))
            raise cls.assertClassSetupFailure(exception)


class BwAfterResizeUpRevertServerFixture(BwComputeFixture):
    '''
    @summary: Creates a server, waits for active state. Then,
        resizes the server up. Reverts the resize back to the original
        flavor. Finally, transfers some bandwidth.
    @note: audit period ending is when we made the request to resize
        or the start time of the wait response
    '''

    @classmethod
    def setUpClass(cls):
        # create server
        super(BwAfterResizeUpRevertServerFixture, cls).setUpClass()
        try:
            # do resize up and revert
            (cls.resized_server,
             cls.expected_audit_period_ending,
             cls.launched_at_resized_server,
             cls.reverted_resized_server,
             cls.reverted_expected_audit_period_ending,
             cls.launched_at_reverted_resized_server) = (cls.compute_provider
                .resize_and_revert(server_id=cls.created_server.id,
                                   new_flavor=cls.flavor_ref_alt))
        except Exception as exception:
            cls.fixture_log.critical('Exception occured while performing a '
                                     'RESIZE UP REVERT on the server.\n'
                                     'instance uuid: {0} \n'
                                     'original flavor: {1} \n'
                                     'resize flavor: {2} \n'
                                     .format(cls.created_server.id,
                                             cls.flavor_ref,
                                             cls.flavor_ref_alt))
            raise cls.assertClassSetupFailure(exception)
        try:
            # generate bandwidth
            (cls.compute_provider
             .do_bandwidth_server_to_client(cls.created_server,
                                            cls.gb_file_size))
        except Exception as exception:
            cls.fixture_log.critical('Exception occured while transferring '
                                     'bandwidth from server to local client.')
            raise cls.assertClassSetupFailure(exception)


class BwBeforeAndAfterResizeUpRevertServerFixture(BwComputeFixture):
    '''
    @summary: Creates a server, waits for active state. Transfers
        some bandwidth. Then, resizes the server up.  Reverts the resize
        back to the original flavor. Finally, transfers some bandwidth.
    @note: audit period ending is when we made the request to resize
        or the start time of the wait response
    '''

    @classmethod
    def setUpClass(cls):
        # create server
        super(BwBeforeAndAfterResizeUpRevertServerFixture, cls).setUpClass()
        try:
            # generate bandwidth
            (cls.compute_provider
             .do_bandwidth_server_to_client(cls.created_server,
                                            cls.gb_file_size))
        except Exception as exception:
            cls.fixture_log.critical('Exception occured while transferring '
                                     'bandwidth from server to local client.')
            raise cls.assertClassSetupFailure(exception)
        try:
            # do resize up and revert
            (cls.resized_server,
             cls.expected_audit_period_ending,
             cls.launched_at_resized_server,
             cls.reverted_resized_server,
             cls.reverted_expected_audit_period_ending,
             cls.launched_at_reverted_resized_server) = (cls.compute_provider
                .resize_and_revert(server_id=cls.created_server.id,
                                   new_flavor=cls.flavor_ref_alt))
        except Exception as exception:
            cls.fixture_log.critical('Exception occured while performing a '
                                     'RESIZE UP REVERT on the server.\n'
                                     'instance uuid: {0} \n'
                                     'original flavor: {1} \n'
                                     'resize flavor: {2} \n'
                                     .format(cls.created_server.id,
                                             cls.flavor_ref,
                                             cls.flavor_ref_alt))
            raise cls.assertClassSetupFailure(exception)
        try:
            # generate bandwidth
            (cls.compute_provider
             .do_bandwidth_server_to_client(cls.created_server,
                                            cls.gb_file_size))
        except Exception as exception:
            cls.fixture_log.critical('Exception occured while transferring '
                                     'bandwidth from server to local client.')
            raise cls.assertClassSetupFailure(exception)


class NoBwResizeUpRevertServerFixture(BwComputeFixture):
    '''
    @summary: Creates a server, waits for active state. Then,
        resizes the server up. Reverts the resize back the the original
        flavor. Does not transfers any bandwidth.
    @note: audit period ending is when we made the request to resize
        or the start time of the wait response
    '''

    @classmethod
    def setUpClass(cls):
        # create server
        super(NoBwResizeUpRevertServerFixture, cls).setUpClass()
        try:
            # do resize up and revert
            (cls.resized_server,
             cls.expected_audit_period_ending,
             cls.launched_at_resized_server,
             cls.reverted_resized_server,
             cls.reverted_expected_audit_period_ending,
             cls.launched_at_reverted_resized_server) = (cls.compute_provider
                .resize_and_revert(server_id=cls.created_server.id,
                                   new_flavor=cls.flavor_ref_alt))
        except Exception as exception:
            cls.fixture_log.critical('Exception occured while performing a '
                                     'RESIZE UP REVERT on the server.\n'
                                     'instance uuid: {0} \n'
                                     'original flavor: {1} \n'
                                     'resize flavor: {2} \n'
                                     .format(cls.created_server.id,
                                             cls.flavor_ref,
                                             cls.flavor_ref_alt))
            raise cls.assertClassSetupFailure(exception)

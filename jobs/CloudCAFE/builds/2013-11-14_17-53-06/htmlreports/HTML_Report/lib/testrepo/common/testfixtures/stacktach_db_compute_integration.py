'''
@summary: Dervied Classes for StackTach Test Suites (Collections of Test Cases)
@note: Correspondes DIRECTLY TO A unittest.TestCase
@see: http://docs.python.org/library/unittest.html#unittest.TestCase
@copyright: Copyright (c) 2012-2013 Rackspace US, Inc.
'''

from datetime import datetime, timedelta

from testrepo.common.testfixtures.compute import ComputeFixture
from testrepo.common.testfixtures.stacktach import StackTachDBFixture
from ccengine.common.tools.datagen import rand_name
from ccengine.domain.types import NovaServerStatusTypes as status
from ccengine.domain.types import NovaServerRebootTypes as reboot
from ccengine.common.exceptions.compute \
        import TimeoutException, BuildErrorException
from ccengine.common.constants.compute_constants \
        import Constants as ComputeConstants
from ccengine.common.constants.stacktach_constants \
        import Constants as StackTachConstants


class StackTachDBComputeFixture(ComputeFixture, StackTachDBFixture):
    '''
    @summary: Fixture for a StackTach DB and Compute Integration test.
    @note:  This class performs integration tests between the Compute API
      and the StackTach DB API .
    @attention: This class MULTIPLE INHERITS methods and attributes from both
     ComputeFixture and StackTachDBFixture to provide some readability
     with the intention of later refactoring towards an integration-type
     fixture.
    '''

    @classmethod
    def setUpClass(cls):
        super(StackTachDBComputeFixture, cls).setUpClass()
        cls.leeway = cls.config.compute_api.build_interval * 3
        cls.msg = StackTachConstants.MESSAGE

    @classmethod
    def tearDownClass(cls):
        super(StackTachDBComputeFixture, cls).tearDownClass()


class CreateServerFixture(StackTachDBComputeFixture):
    '''
    @summary: Creates a server using defaults from the test data,
        waits for active state.
    @param name: The name of the server.
    @type name: String
    @param image_ref: The reference to the image used to build the server.
    @type image_ref: String
    @param flavor_ref: The flavor used to build the server.
    @type flavor_ref: String
    @param meta: A dictionary of values to be used as metadata.
    @type meta: Dictionary. The limit is 5 key/values.
    @param personality: A list of dictionaries for files to be injected
        into the server.
    @type personality: List
    @param disk_config: MANUAL/AUTO/None
    @type disk_config: String
    @param networks:The networks to which you want to attach the server.
    @type networks: String
    @note: Overrides CreateServerFixture in ComputeFixture.
    '''

    @classmethod
    def setUpClass(cls, name=None,
                   imageRef=None, flavorRef=None,
                   personality=None, metadata=None,
                   disk_config=None, networks=None):

        # Compute
        super(CreateServerFixture, cls).setUpClass()
        if name is None:
            name = rand_name('testservercc')
        if imageRef is None:
            imageRef = cls.image_ref
        if flavorRef is None:
            flavorRef = cls.flavor_ref
        create_response = (cls.servers_client
                           .create_server(name,
                                          imageRef,
                                          flavorRef,
                                          personality=personality,
                                          metadata=metadata,
                                          disk_config=disk_config,
                                          networks=networks))
        cls.expected_audit_period_beginning = \
            datetime.utcnow().strftime(ComputeConstants
                                       .DATETIME_0AM_FORMAT)
        cls.expected_audit_period_ending = \
            ((datetime.utcnow() + timedelta(days=1))
             .strftime(ComputeConstants.DATETIME_0AM_FORMAT))
        cls.created_server = create_response.entity
        try:
            wait_response = (cls.compute_provider
                             .wait_for_server_status(cls.created_server.id,
                                                     status.ACTIVE))
            wait_response.entity.adminPass = cls.created_server.adminPass
            cls.launched_at_created_server = (datetime.utcnow()
                                             .strftime(ComputeConstants
                                                       .DATETIME_FORMAT))
            _ = (cls.stacktachdb_provider
                 .wait_for_launched_at(cls.created_server.id,
                                       interval_time=cls.config.compute_api
                                       .build_interval,
                                       timeout=cls.config.compute_api
                                       .server_status_timeout))
        except TimeoutException as exception:
            cls.assertClassSetupFailure(exception.message)
        except BuildErrorException as exception:
            cls.assertClassSetupFailure(exception.message)
        finally:
            cls.resources.add(cls.created_server.id,
                              cls.servers_client.delete_server)
        cls.server_response = wait_response
        if cls.server_response.entity.status != status.ACTIVE:
            cls.assertClassSetupFailure("Server {0} did not reach active state"
                                        .format(cls.created_server.id))
        cls.created_server = cls.server_response.entity
        cls.resources.add(cls.created_server.id,
                          cls.servers_client.delete_server)

    @classmethod
    def tearDownClass(cls):
        super(CreateServerFixture, cls).tearDownClass()


class STCreateServerFixture(CreateServerFixture):
    '''
    @summary: Creates a server using defaults from the test data,
        waits for active state. Connects to StackTach DB to obtain
        revelant validation data.
    '''

    @classmethod
    def setUpClass(cls):

        super(STCreateServerFixture, cls).setUpClass()

        # StackTach
        cls.st_launch_response = \
                (cls.stacktachdb_provider.client
                 .list_launches_for_uuid(instance=cls.created_server.id))
        cls.st_launch_create_server = cls.st_launch_response.entity[0]
        cls.st_delete_response = \
                (cls.stacktachdb_provider.client
                 .list_deletes_for_uuid(instance=cls.created_server.id))
        cls.st_delete = cls.st_delete_response.entity
        cls.st_exist_response = \
                (cls.stacktachdb_provider.client
                 .list_exists_for_uuid(instance=cls.created_server.id))
        cls.st_exist = cls.st_exist_response.entity

    @classmethod
    def tearDownClass(cls):
        super(STCreateServerFixture, cls).tearDownClass()


class ResizeServerFixture(CreateServerFixture):
    '''
    @summary: Create an active server, resizes it and waits for
        verify_resize state.
    @param name: The name of the server.
    @type name: String
    @param image_ref: The reference to the image used to build the server.
    @type image_ref: String
    @param flavor_ref: The flavor used to build the server.
    @type flavor_ref: String
    @param meta: A dictionary of values to be used as metadata.
    @type meta: Dictionary. The limit is 5 key/values.
    @param personality: A list of dictionaries for files to be
        injected into the server.
    @type personality: List
    @param disk_config: MANUAL/AUTO/None
    @type disk_config: String
    @param networks:The networks to which you want to attach the server.
    @type networks: String
    @param resize_flavor: Flavor to which Server needs to be resized.
    @type resize_flavor: String
    @note: Overrides ResizeServerFixture in ComputeFixture.
    '''

    @classmethod
    def setUpClass(cls, name=None, imageRef=None,
                   flavorRef=None, personality=None,
                   metadata=None, disk_config=None,
                   networks=None, resize_flavor=None):

        # Compute
        super(ResizeServerFixture, cls).setUpClass(name=name,
                                                   imageRef=imageRef,
                                                   flavorRef=flavorRef,
                                                   personality=personality,
                                                   metadata=metadata,
                                                   disk_config=disk_config,
                                                   networks=networks)
        if resize_flavor != None:
            cls.resize_flavor = resize_flavor
        else:
            cls.resize_flavor = cls.flavor_ref_alt

        try:
            cls.servers_client.resize(cls.created_server.id,
                                      cls.resize_flavor)
            cls.start_time_wait_resp_at_resize = \
                datetime.utcnow().strftime(ComputeConstants.DATETIME_FORMAT)
            wait_response = (cls.compute_provider
                             .wait_for_server_status(cls.created_server.id,
                                                     status.VERIFY_RESIZE))
            cls.launched_at_resized_server = (datetime.utcnow()
                                              .strftime(ComputeConstants
                                                        .DATETIME_FORMAT))
            _ = (cls.stacktachdb_provider
                 .wait_for_launched_at(cls.created_server.id,
                                       interval_time=cls.config.compute_api
                                       .build_interval,
                                       timeout=cls.config.compute_api
                                       .server_status_timeout))
        except TimeoutException as exception:
            cls.assertClassSetupFailure(exception.message)
        except BuildErrorException as exception:
            cls.assertClassSetupFailure(exception.message)
        cls.verified_resized_server = wait_response.entity
        if cls.verified_resized_server.status != status.VERIFY_RESIZE:
            cls.assertClassSetupFailure("Server {0} did not reach VerifyResize"
                                        .format(cls
                                                .verified_resized_server.id))

    @classmethod
    def tearDownClass(cls):
        super(ResizeServerFixture, cls).tearDownClass()


class ConfirmResizeServerFixture(ResizeServerFixture):
    '''
    @summary: Create an active server, resizes it and confirms resize.
        Connects to StackTach DB to obtain revelant validation data.
    @param name: The name of the server.
    @type name: String
    @param image_ref: The reference to the image used to build the server.
    @type image_ref: String
    @param flavor_ref: The flavor used to build the server.
    @type flavor_ref: String
    @param meta: A dictionary of values to be used as metadata.
    @type meta: Dictionary. The limit is 5 key/values.
    @param personality: A list of dictionaries for files to be
        injected into the server.
    @type personality: List
    @param disk_config: MANUAL/AUTO/None
    @type disk_config: String
    @param networks:The networks to which you want to attach the server.
    @type networks: String
    @param resize_flavor: Flavor to which Server needs to be resized.
    @type resize_flavor: String
    @note: Overides ConfirmResizeServerFixture in ComputeFixture
    '''

    @classmethod
    def setUpClass(cls, name=None, imageRef=None,
                   flavorRef=None, personality=None,
                   metadata=None, disk_config=None,
                   networks=None, resize_flavor=None):

        # Compute
        (super(ConfirmResizeServerFixture, cls)
         .setUpClass(name=name,
                     imageRef=imageRef,
                     flavorRef=flavorRef,
                     personality=personality,
                     metadata=metadata,
                     disk_config=disk_config,
                     networks=networks,
                     resize_flavor=resize_flavor))
        try:
            cls.servers_client.confirm_resize(cls.created_server.id)
            wait_response = (cls.compute_provider
                             .wait_for_server_status(cls.created_server.id,
                                                     status.ACTIVE))
            _ = (cls.stacktachdb_provider
                 .wait_for_launched_at(cls.created_server.id,
                                       interval_time=cls.config.compute_api
                                       .build_interval,
                                       timeout=cls.config.compute_api
                                       .server_status_timeout))
        except TimeoutException as exception:
            cls.assertClassSetupFailure(exception.message)
        except BuildErrorException as exception:
            cls.assertClassSetupFailure(exception.message)
        cls.confirmed_resized_server = wait_response.entity
        if cls.confirmed_resized_server.status != status.ACTIVE:
            cls.assertClassSetupFailure("Server {0} did not reach Active state"
                                        .format(cls
                                                .confirmed_resized_server.id))

    @classmethod
    def tearDownClass(cls):
        super(ConfirmResizeServerFixture, cls).tearDownClass()


class STConfirmResizeServerFixture(ConfirmResizeServerFixture):
    '''
    @summary: Creates a server using defaults from the test data,
        waits for active state. Then Resizes and Confirms the
        Resize of the server. Connects to StackTach DB to obtain
        revelant validation data.
    '''

    @classmethod
    def setUpClass(cls, flavorRef=None, resize_flavor=None):

        (super(STConfirmResizeServerFixture, cls)
         .setUpClass(flavorRef=flavorRef,
                     resize_flavor=resize_flavor))

        # StackTach
        cls.st_launch_response = \
                (cls.stacktachdb_provider.client
                 .list_launches_for_uuid(instance=cls.
                                         confirmed_resized_server.id))
        cls.st_launches = sorted(cls.st_launch_response.entity,
                                 key=lambda launch: launch.id)
        cls.st_launch_create_server = cls.st_launches[0]
        cls.st_launch_resize_server = cls.st_launches[1]
        cls.st_exist_response = \
                (cls.stacktachdb_provider.client
                 .list_exists_for_uuid(instance=cls
                                       .confirmed_resized_server.id))
        cls.st_exist = cls.st_exist_response.entity[0]
        cls.st_delete_response = \
                (cls.stacktachdb_provider.client
                 .list_deletes_for_uuid(instance=cls
                                        .confirmed_resized_server.id))
        cls.st_delete = cls.st_delete_response.entity

    @classmethod
    def tearDownClass(cls):
        super(STConfirmResizeServerFixture, cls).tearDownClass()


class RevertResizeServerFixture(ResizeServerFixture):
    '''
    @summary: Creates a server, resizes the server, reverts the resize and
        waits for active state.  Connects to StackTach DB to obtain revelant
        validation data.
    @param name: The name of the server.
    @type name: String
    @param image_ref: The reference to the image used to build the server.
    @type image_ref: String
    @param flavor_ref: The flavor used to build the server.
    @type flavor_ref: String
    @param meta: A dictionary of values to be used as metadata.
    @type meta: Dictionary. The limit is 5 key/values.
    @param personality: A list of dictionaries for files to be
        injected into the server.
    @type personality: List
    @param disk_config: MANUAL/AUTO/None
    @type disk_config: String
    @param networks:The networks to which you want to attach the server.
    @type networks: String
    @param resize_flavor: Flavor to which Server needs to be resized.
    @type resize_flavor: String
    @note: Overrides RevertResizeFixture in ComputeFixture.
    '''

    @classmethod
    def setUpClass(cls, name=None, imageRef=None,
                   flavorRef=None, personality=None,
                   metadata=None, disk_config=None,
                   networks=None, resize_flavor=None):

        # Compute
        (super(RevertResizeServerFixture, cls)
         .setUpClass(name=name,
                     imageRef=imageRef,
                     flavorRef=flavorRef,
                     personality=personality,
                     metadata=metadata,
                     disk_config=disk_config,
                     networks=networks,
                     resize_flavor=resize_flavor))
        try:
            cls.servers_client.revert_resize(cls.created_server.id)
            wait_response = cls.compute_provider.wait_for_server_status(
                                                   cls.created_server.id,
                                                   status.ACTIVE)
            cls.launched_at_revert_resize_server = \
                    (datetime.utcnow().strftime(ComputeConstants
                                                .DATETIME_FORMAT))
            _ = (cls.stacktachdb_provider
                 .wait_for_launched_at(cls.created_server.id,
                                       interval_time=cls.config.compute_api
                                       .build_interval,
                                       timeout=cls.config.compute_api
                                       .server_status_timeout))
        except TimeoutException as exception:
            cls.assertClassSetupFailure(exception.message)
        except BuildErrorException as exception:
            cls.assertClassSetupFailure(exception.message)
        cls.reverted_server = wait_response.entity
        if cls.reverted_server.status != status.ACTIVE:
            cls.assertClassSetupFailure("Server {0} did not reach Active state"
                                        .format(cls.reverted_server.id))

    @classmethod
    def tearDownClass(cls):
        super(RevertResizeServerFixture, cls).tearDownClass()


class STRevertResizeServerFixture(RevertResizeServerFixture):
    '''
    @summary: Creates a server using defaults from the test data,
        waits for active state. Then resizes the server and revert
        resizes the server. Connects to StackTach DB to obtain
        revelant validation data.
    '''

    @classmethod
    def setUpClass(cls, flavorRef=None, resize_flavor=None):

        (super(STRevertResizeServerFixture, cls)
         .setUpClass(flavorRef=flavorRef,
                     resize_flavor=resize_flavor))

        # StackTach
        cls.st_launch_response = \
                (cls.stacktachdb_provider.client
                 .list_launches_for_uuid(instance=cls.reverted_server.id))
        cls.st_launches = sorted(cls.st_launch_response.entity,
                                 key=lambda launch: launch.id)
        cls.st_launch_create_server = cls.st_launches[0]
        cls.st_launch_resize_server = cls.st_launches[1]
        cls.st_launch_revert_resize = cls.st_launches[2]
        cls.st_exist_response = (cls.stacktachdb_provider.client
                                 .list_exists_for_uuid(instance=cls
                                                       .reverted_server.id))
        cls.st_exists = sorted(cls.st_exist_response.entity,
                               key=lambda exist: exist.id)
        cls.st_exist_resize_server = cls.st_exists[0]
        cls.st_exist_revert_resize_server = cls.st_exists[1]
        cls.st_delete_response = \
                (cls.stacktachdb_provider.client
                 .list_deletes_for_uuid(instance=cls.reverted_server.id))
        cls.st_delete = cls.st_delete_response.entity

    @classmethod
    def tearDownClass(cls):
        super(STRevertResizeServerFixture, cls).tearDownClass()


class RescueServerFixture(CreateServerFixture):
    '''
    @summary: Makes a rescue request for the server and waits for the rescued
        state. Connects to StackTach DB to obtain revelant validation data.
    @param name: The name of the server.
    @type name: String
    @param image_ref: The reference to the image used to build the server.
    @type image_ref: String
    @param flavor_ref: The flavor used to build the server.
    @type flavor_ref: String
    @param meta: A dictionary of values to be used as metadata.
    @type meta: Dictionary. The limit is 5 key/values.
    @param personality: A list of dictionaries for files to be
        injected into the server.
    @type personality: List
    @param disk_config: MANUAL/AUTO/None
    @type disk_config: String
    @param networks:The networks to which you want to attach the server.
    @type networks: String
    @note: Overrides RescueServerFixture in ComputeFixture.
    '''

    @classmethod
    def setUpClass(cls, name=None, imageRef=None,
                   flavorRef=None, personality=None,
                   metadata=None, disk_config=None,
                   networks=None):

        # Compute
        super(RescueServerFixture, cls).setUpClass(name=None,
                                                   imageRef=None,
                                                   flavorRef=None,
                                                   personality=None,
                                                   metadata=None,
                                                   disk_config=None,
                                                   networks=None)
        try:
            cls.servers_client.rescue(cls.created_server.id)
            wait_response = (cls.compute_provider
                             .wait_for_server_status(cls.created_server.id,
                                                     status.RESCUE))
        except TimeoutException as exception:
            cls.assertClassSetupFailure(exception.message)
        except BuildErrorException as exception:
            cls.assertClassSetupFailure(exception.message)
        cls.rescue_server = wait_response.entity
        if cls.rescue_server.status != status.RESCUE:
            cls.assertClassSetupFailure("Server {0} did not reach Rescue state"
                                        .format(cls.rescue_server.id))

    @classmethod
    def tearDownClass(cls):
        super(RescueServerFixture, cls).tearDownClass()


class STRescueServerFixture(RescueServerFixture):
    '''
    @summary: Creates a server using defaults from the test data,
        waits for active state. Then rescues the server.
        Connects to StackTach DB to obtain revelant validation data.
    '''

    @classmethod
    def setUpClass(cls):

        super(STRescueServerFixture, cls).setUpClass()

        # StackTach
        cls.st_launch_response = \
                (cls.stacktachdb_provider.client
                 .list_launches_for_uuid(instance=cls.rescue_server.id))
        cls.st_launch_create_server = cls.st_launch_response.entity[0]
        cls.st_delete_response = \
                (cls.stacktachdb_provider.client
                 .list_deletes_for_uuid(instance=cls.rescue_server.id))
        cls.st_delete = cls.st_delete_response.entity
        cls.st_exist_response = \
                (cls.stacktachdb_provider.client
                 .list_exists_for_uuid(instance=cls.rescue_server.id))
        cls.st_exist = cls.st_exist_response.entity

    @classmethod
    def tearDownClass(cls):
        super(STRescueServerFixture, cls).tearDownClass()


class RebuildServerFixture(CreateServerFixture):
    '''
    @summary: Creates an Active server, Rebuilds the server using the
        configured secondary image and waits for the active state.
        Connects to StackTach DB to obtain revelant validation data.
    @param name: The name of the server.
    @type name: String
    @param image_ref: The reference to the image used to build the server.
    @type image_ref: String
    @param flavor_ref: The flavor used to build the server.
    @type flavor_ref: String
    @param meta: A dictionary of values to be used as metadata.
    @type meta: Dictionary. The limit is 5 key/values.
    @param personality: A list of dictionaries for files to be
        injected into the server.
    @type personality: List
    @param disk_config: MANUAL/AUTO/None
    @type disk_config: String
    @param networks:The networks to which you want to attach the server.
    @type networks: String
    @note: Overrides RebuildServerFixture in ComputeFixture
    '''

    @classmethod
    def setUpClass(cls, name=None, imageRef=None,
                   flavorRef=None, personality=None,
                   metadata=None, disk_config=None,
                   networks=None, rebuild_image_ref=None):

        # Compute
        super(RebuildServerFixture, cls).setUpClass(name=None,
                                                    imageRef=None,
                                                    flavorRef=None,
                                                    personality=None,
                                                    metadata=None,
                                                    disk_config=None,
                                                    networks=None,)
        if rebuild_image_ref == None:
            cls.rebuild_image_ref = cls.image_ref_alt
        else:
            cls.rebuild_image_ref = rebuild_image_ref
        try:
            cls.servers_client.rebuild(cls.created_server.id,
                                       cls.rebuild_image_ref)
            wait_response = (cls.compute_provider
                             .wait_for_server_status(cls.created_server.id,
                                                     status.ACTIVE))
            cls.launched_at_rebuilt_server = (datetime.utcnow()
                                              .strftime(ComputeConstants
                                                        .DATETIME_FORMAT))
            _ = (cls.stacktachdb_provider
                 .wait_for_launched_at(cls.created_server.id,
                                       interval_time=cls.config.compute_api
                                       .build_interval,
                                       timeout=cls.config.compute_api
                                       .server_status_timeout))
        except TimeoutException as exception:
            cls.assertClassSetupFailure(exception.message)
        except BuildErrorException as exception:
            cls.assertClassSetupFailure(exception.message)
        cls.rebuilt_server = wait_response.entity
        if cls.rebuilt_server.status != status.ACTIVE:
            cls.assertClassSetupFailure("Server {0} did not reach Active state"
                                        .format(cls.rebuilt_server.id))

    @classmethod
    def tearDownClass(cls):
        super(RebuildServerFixture, cls).tearDownClass()


class STRebuildServerFixture(RebuildServerFixture):
    '''
    @summary: Creates a server using defaults from the test data,
        waits for active state. Then rebuilds the server.
        Connects to StackTach DB to obtain revelant validation data.
    '''

    @classmethod
    def setUpClass(cls):

        super(STRebuildServerFixture, cls).setUpClass()

        # StackTach
        cls.st_launch_response = \
                (cls.stacktachdb_provider.client
                 .list_launches_for_uuid(instance=cls.rebuilt_server.id))
        cls.st_launches = sorted(cls.st_launch_response.entity,
                                 key=lambda launch: launch.id)
        cls.st_launch_create_server = cls.st_launches[0]
        cls.st_launch_rebuild_server = cls.st_launches[1]
        cls.st_exist_response = \
                (cls.stacktachdb_provider.client
                 .list_exists_for_uuid(instance=cls.rebuilt_server.id))
        cls.st_exist = cls.st_exist_response.entity[0]
        cls.st_delete_response = \
                (cls.stacktachdb_provider.client
                 .list_deletes_for_uuid(instance=cls.rebuilt_server.id))
        cls.st_delete = cls.st_delete_response.entity

    @classmethod
    def tearDownClass(cls):
        super(STRebuildServerFixture, cls).tearDownClass()


class RebootServerHardFixture(CreateServerFixture):
    '''
    @summary: Performs a hard reboot on the created server and waits for the
        active state. Connects to StackTach DB to obtain revelant
        validation data.
    @param name: The name of the server.
    @type name: String
    @param image_ref: The reference to the image used to build the server.
    @type image_ref: String
    @param flavor_ref: The flavor used to build the server.
    @type flavor_ref: String
    @param meta: A dictionary of values to be used as metadata.
    @type meta: Dictionary. The limit is 5 key/values.
    @param personality: A list of dictionaries for files to be
        injected into the server.
    @type personality: List
    @param disk_config: MANUAL/AUTO/None
    @type disk_config: String
    @param networks:The networks to which you want to attach the server.
    @type networks: String
    @note: Overrides RebootServerHardFixture in ComputeFixture
    '''

    @classmethod
    def setUpClass(cls, name=None, imageRef=None,
                   flavorRef=None, personality=None,
                   metadata=None, disk_config=None,
                   networks=None):

        # Compute
        super(RebootServerHardFixture, cls).setUpClass(name=None,
                                                       imageRef=None,
                                                       flavorRef=None,
                                                       personality=None,
                                                       metadata=None,
                                                       disk_config=None,
                                                       networks=None)
        try:
            cls.servers_client.reboot(cls.created_server.id, reboot.HARD)
            wait_response = (cls.compute_provider
                             .wait_for_server_status(cls.created_server.id,
                                                     status.ACTIVE))
            cls.reboot_response = wait_response
        except TimeoutException as exception:
            cls.assertClassSetupFailure(exception.message)
        except BuildErrorException as exception:
            cls.assertClassSetupFailure(exception.message)
        cls.hard_rebooted_server = wait_response.entity
        if wait_response.entity.status != status.ACTIVE:
            cls.assertClassSetupFailure("Server {0} did not reach Active state"
                                        .format(cls.hard_rebooted_server.id))

    @classmethod
    def tearDownClass(cls):
        super(RebootServerHardFixture, cls).tearDownClass()
        cls.resources.release()


class STRebootServerHardFixture(RebootServerHardFixture):
    '''
    @summary: Creates a server using defaults from the test data,
        waits for active state. Then hard reboots the server.
        Connects to StackTach DB to obtain revelant validation data.
    '''

    @classmethod
    def setUpClass(cls):

        super(STRebootServerHardFixture, cls).setUpClass()

        # StackTach
        cls.st_launch_response = \
                (cls.stacktachdb_provider.client
                 .list_launches_for_uuid(instance=cls.hard_rebooted_server.id))
        cls.st_launch_create_server = cls.st_launch_response.entity[0]
        cls.st_delete_response = \
                (cls.stacktachdb_provider.client
                 .list_deletes_for_uuid(instance=cls.hard_rebooted_server.id))
        cls.st_delete = cls.st_delete_response.entity
        cls.st_exist_response = \
                (cls.stacktachdb_provider.client
                 .list_exists_for_uuid(instance=cls.hard_rebooted_server.id))
        cls.st_exist = cls.st_exist_response.entity

    @classmethod
    def tearDownClass(cls):
        super(STRebootServerHardFixture, cls).tearDownClass()


class RebootServerSoftFixture(CreateServerFixture):
    '''
    @summary: Performs a soft reboot on the created server and waits for
        the active state. Connects to StackTach DB to obtain
        revelant validation data.
    @param name: The name of the server.
    @type name: String
    @param image_ref: The reference to the image used to build the server.
    @type image_ref: String
    @param flavor_ref: The flavor used to build the server.
    @type flavor_ref: String
    @param meta: A dictionary of values to be used as metadata.
    @type meta: Dictionary. The limit is 5 key/values.
    @param personality: A list of dictionaries for files to be
        injected into the server.
    @type personality: List
    @param disk_config: MANUAL/AUTO/None
    @type disk_config: String
    @param networks:The networks to which you want to attach the server.
    @type networks: String
    @note: Overrides RebootServerSoftFixture in ComputeFixture
    '''

    @classmethod
    def setUpClass(cls, name=None, imageRef=None,
                   flavorRef=None, personality=None,
                   metadata=None, disk_config=None,
                   networks=None):

        # Compute
        super(RebootServerSoftFixture, cls).setUpClass(name=None,
                                                       imageRef=None,
                                                       flavorRef=None,
                                                       personality=None,
                                                       metadata=None,
                                                       disk_config=None,
                                                       networks=None)
        try:
            cls.servers_client.reboot(cls.created_server.id, reboot.SOFT)
            wait_response = (cls.compute_provider
                             .wait_for_server_status(cls.created_server.id,
                                                     status.ACTIVE))
            cls.reboot_response = wait_response
        except TimeoutException as exception:
            cls.assertClassSetupFailure(exception.message)
        except BuildErrorException as exception:
            cls.assertClassSetupFailure(exception.message)
        cls.soft_rebooted_server = wait_response.entity
        if wait_response.entity.status != status.ACTIVE:
            cls.assertClassSetupFailure("Server {0} did not reach Active state"
                                        .format(cls.soft_rebooted_server.id))

    @classmethod
    def tearDownClass(cls):
        super(RebootServerSoftFixture, cls).tearDownClass()
        cls.resources.release()


class STRebootServerSoftFixture(RebootServerSoftFixture):
    '''
    @summary: Creates a server using defaults from the test data,
        waits for active state. Then soft reboots the server.
        Connects to StackTach DB to obtain revelant validation data.
    '''

    @classmethod
    def setUpClass(cls):

        super(STRebootServerSoftFixture, cls).setUpClass()

        # StackTach
        cls.st_launch_response = \
                (cls.stacktachdb_provider.client
                 .list_launches_for_uuid(instance=cls.soft_rebooted_server.id))
        cls.st_launch_create_server = cls.st_launch_response.entity[0]
        cls.st_delete_response = \
                (cls.stacktachdb_provider.client
                 .list_deletes_for_uuid(instance=cls.soft_rebooted_server.id))
        cls.st_delete = cls.st_delete_response.entity
        cls.st_exist_response = \
                (cls.stacktachdb_provider.client
                 .list_exists_for_uuid(instance=cls.soft_rebooted_server.id))
        cls.st_exist = cls.st_exist_response.entity

    @classmethod
    def tearDownClass(cls):
        super(STRebootServerSoftFixture, cls).tearDownClass()


class ChangePasswordServerFixture(CreateServerFixture):
    '''
    @summary: Performs a change password on the created server and waits for
        the active state. Connects to StackTach DB to obtain
        revelant validation data.
    @param name: The name of the server.
    @type name: String
    @param image_ref: The reference to the image used to build the server.
    @type image_ref: String
    @param flavor_ref: The flavor used to build the server.
    @type flavor_ref: String
    @param meta: A dictionary of values to be used as metadata.
    @type meta: Dictionary. The limit is 5 key/values.
    @param personality: A list of dictionaries for files to be
        injected into the server.
    @type personality: List
    @param disk_config: MANUAL/AUTO/None
    @type disk_config: String
    @param networks:The networks to which you want to attach the server.
    @type networks: String
    @note: Overrides ChangePasswordServerFixture in ComputeFixture
    '''

    @classmethod
    def setUpClass(cls, name=None, imageRef=None,
                   flavorRef=None, personality=None,
                   metadata=None, disk_config=None,
                   networks=None):

        # Compute
        super(ChangePasswordServerFixture, cls).setUpClass(name=None,
                                                           imageRef=None,
                                                           flavorRef=None,
                                                           personality=None,
                                                           metadata=None,
                                                           disk_config=None,
                                                           networks=None)
        try:
            # Change Password
            cls.new_password = "newslice129690TuG72Bgj2"
            cls.response = (cls.servers_client
                            .change_password(cls.created_server.id,
                                             cls.new_password))
            wait_response = (cls.compute_provider
                             .wait_for_server_status(cls.created_server.id,
                                                     status.ACTIVE))
        except TimeoutException as exception:
            cls.assertClassSetupFailure(exception.message)
        except BuildErrorException as exception:
            cls.assertClassSetupFailure(exception.message)
        cls.changed_password_server = wait_response.entity
        if wait_response.entity.status != status.ACTIVE:
            cls.assertClassSetupFailure("Server {0} did not reach Active state"
                                        .format(cls
                                                .changed_password_server.id))

    @classmethod
    def tearDownClass(cls):
        super(ChangePasswordServerFixture, cls).tearDownClass()
        cls.resources.release()


class STChangePasswordServerFixture(ChangePasswordServerFixture):
    '''
    @summary: Creates a server using defaults from the test data,
        waits for active state. Changes password on server.
        Connects to StackTach DB to obtain revelant validation data.
    '''

    @classmethod
    def setUpClass(cls):

        super(STChangePasswordServerFixture, cls).setUpClass()

        # StackTach
        cls.st_launch_response = \
                (cls.stacktachdb_provider.client
                 .list_launches_for_uuid(
                    instance=cls.changed_password_server.id))
        cls.st_launch_create_server = cls.st_launch_response.entity[0]
        cls.st_delete_response = \
                (cls.stacktachdb_provider.client
                 .list_deletes_for_uuid(
                    instance=cls.changed_password_server.id))
        cls.st_delete = cls.st_delete_response.entity
        cls.st_exist_response = \
                (cls.stacktachdb_provider.client
                 .list_exists_for_uuid(
                    instance=cls.changed_password_server.id))
        cls.st_exist = cls.st_exist_response.entity

    @classmethod
    def tearDownClass(cls):
        super(STChangePasswordServerFixture, cls).tearDownClass()


class DeleteServerFixture(CreateServerFixture):
    '''
    @summary: Performs a delete on the created server and waits for
        the deleted state. Connects to StackTach DB to obtain
        revelant validation data.
    @param name: The name of the server.
    @type name: String
    @param image_ref: The reference to the image used to build the server.
    @type image_ref: String
    @param flavor_ref: The flavor used to build the server.
    @type flavor_ref: String
    @param meta: A dictionary of values to be used as metadata.
    @type meta: Dictionary. The limit is 5 key/values.
    @param personality: A list of dictionaries for files to be
        injected into the server.
    @type personality: List
    @param disk_config: MANUAL/AUTO/None
    @type disk_config: String
    @param networks: The networks to which you want to attach the server.
    @type networks: String
    @note: Overrides DeleteServerFixture in ComputeFixture
    '''

    @classmethod
    def setUpClass(cls, name=None, imageRef=None,
                   flavorRef=None, personality=None,
                   metadata=None, disk_config=None,
                   networks=None):

        # Compute
        super(DeleteServerFixture, cls).setUpClass(name=None,
                                                   imageRef=None,
                                                   flavorRef=None,
                                                   personality=None,
                                                   metadata=None,
                                                   disk_config=None,
                                                   networks=None)
        try:
            wait_response = (cls.servers_client
                             .get_server(cls.created_server.id))
            cls.servers_client.delete_server(cls.created_server.id)
            (cls.compute_provider
             .wait_for_server_to_be_deleted(cls.created_server.id))
            cls.deleted_at = (datetime.utcnow()
                              .strftime(ComputeConstants.DATETIME_FORMAT))
        except TimeoutException as exception:
            cls.assertClassSetupFailure(exception.message)
        except BuildErrorException as exception:
            cls.assertClassSetupFailure(exception.message)
        cls.deleted_server = wait_response.entity

    @classmethod
    def tearDownClass(cls):
        super(DeleteServerFixture, cls).tearDownClass()
        cls.resources.release()


class STDeleteServerFixture(DeleteServerFixture):
    '''
    @summary: Creates a server using defaults from the test data,
        waits for active state. Then deletes the server.
        Connects to StackTach DB to obtain revelant validation data.
    '''

    @classmethod
    def setUpClass(cls):

        super(STDeleteServerFixture, cls).setUpClass()

        # StackTach
        cls.st_launch_response = \
                (cls.stacktachdb_provider.client
                 .list_launches_for_uuid(instance=cls.deleted_server.id))
        cls.st_launch_create_server = cls.st_launch_response.entity[0]
        cls.st_delete_response = \
                (cls.stacktachdb_provider.client
                 .list_deletes_for_uuid(instance=cls.deleted_server.id))
        cls.st_delete = cls.st_delete_response.entity[0]
        cls.st_exist_response = \
                (cls.stacktachdb_provider.client
                 .list_exists_for_uuid(instance=cls.deleted_server.id))
        cls.st_exist = cls.st_exist_response.entity

    @classmethod
    def tearDownClass(cls):
        super(STDeleteServerFixture, cls).tearDownClass()

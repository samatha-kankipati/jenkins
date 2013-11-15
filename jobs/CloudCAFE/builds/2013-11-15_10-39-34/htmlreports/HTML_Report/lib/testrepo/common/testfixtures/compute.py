'''
@summary: Base Classes for Compute Test Suites (Collections of Test Cases)
@note: Correspondes DIRECTLY TO A unittest.TestCase
@see: http://docs.python.org/library/unittest.html#unittest.TestCase
@copyright: Copyright (c) 2012 Rackspace US, Inc.
'''
from testrepo.common.testfixtures.fixtures import BaseTestFixture, \
                                            BaseParameterizedTestFixture
from ccengine.providers.compute.compute_api import ComputeAPIProvider \
                                                   as _ComputeAPIProvider
from ccengine.providers.atomhopper import AtomHopperProvider
from ccengine.common.resource_manager.resource_pool import ResourcePool
from ccengine.domain.configuration import AuthConfig, MiscConfig
from ccengine.common.tools.datagen import rand_name
from ccengine.providers.dnsaas.ptr_api import PtrProvider as _PtrProvider
from ccengine.providers.rackconnect.rcc_api import RackconnectProvider as \
                                                   _RackconnectProvider
from ccengine.clients.compute.servers_api import ServerAPIClient
from ccengine.clients.compute.flavors_api import FlavorsApiClient
from ccengine.clients.compute.images_api import ImagesAPIClient
from ccengine.clients.compute.keypairs_api import KeypairsClient
from ccengine.clients.compute.vnc_console_api import VncConsoleClient
from ccengine.clients.compute.limits_api import LimitsApiClient
from ccengine.providers.configuration import MasterConfigProvider as _MCP
from ccengine.common.exception_handler.exception_handler import ExceptionHandler
from ccengine.domain.types import NovaServerStatusTypes as status
from ccengine.domain.types import NovaServerRebootTypes as reboot
from ccengine.common.exceptions.compute import TimeoutException, \
    BuildErrorException


class ComputeFixture(BaseTestFixture):
    '''
    @summary: Fixture for an Compute test.
    '''

    @classmethod
    def setUpClass(cls):
        super(ComputeFixture, cls).setUpClass()
        cls.resources = ResourcePool()
        cls.compute_provider = _ComputeAPIProvider(cls.config, cls.fixture_log)
        cls.atomhopper_provider = AtomHopperProvider(cls.config.compute_api.atom_hopper_url, cls.config)
        ah_dict = {MiscConfig.SECTION_NAME: {'serializer': 'xml', 'deserializer': 'xml'}}
        ah_config = cls.config.mcp_override(ah_dict)
        nova_atom_hopper_url = ah_config.compute_api.atom_hopper_url + '/nova/events'
        glance_atom_hopper_url = ah_config.compute_api.atom_hopper_url + '/glance/events'
        cls.nova_atomhopper_provider = AtomHopperProvider(nova_atom_hopper_url, ah_config)
        cls.glance_atomhopper_provider = AtomHopperProvider(glance_atom_hopper_url, ah_config)
        cls._set_clients_from_provider()
        cls.flavor_ref = cls.config.compute_api.flavor_ref
        cls.image_ref = cls.config.compute_api.image_ref
        cls.image_ref_alt = cls.config.compute_api.image_ref_alt
        cls.flavor_ref_alt = cls.config.compute_api.flavor_ref_alt
        low_limit_user_auth = {AuthConfig.SECTION_NAME:
                          {'username': cls.config.auth.low_limit_username,
                           'api_key': cls.config.auth.low_limit_user_password}}
        cls.low_limit_conf = cls.config.mcp_override(low_limit_user_auth)
        cls.compute_provider_for_low_limits_user = _ComputeAPIProvider(
                                                            cls.low_limit_conf,
                                                            cls.fixture_log)

    @classmethod
    def tearDownClass(cls):
        super(ComputeFixture, cls).tearDownClass()
        cls.resources.release()
        cls.flavors_client.delete_exception_handler(ExceptionHandler())

    @classmethod
    def _set_clients_from_provider(cls, provider=None):
        if provider is None:
            provider = cls.compute_provider
            ah_provider = cls.atomhopper_provider
            cls.flavors_client = provider.flavors_client
            cls.flavors_client.add_exception_handler(ExceptionHandler())
            cls.servers_client = provider.servers_client
            cls.images_client = provider.images_client
            cls.limits_client = provider.limits_client
            cls.hosts_client = provider.hosts_client
            cls.atomhopper_client = ah_provider.client
            cls.vnc_client = provider.vnc_client
            cls.keypairs_client = provider.keypairs_client

    @classmethod
    def parse_image_id(self, image_response):
        """
        @summary: Extract Image Id from Image response
        @param image_response: Image response
        @type image_ref: string
        @return: Image id
        @rtype: string
        """
        image_ref = image_response.headers['location']
        return image_ref.rsplit('/')[-1]

    def verify_server_event_details(self, server, image, flavor, event):
        '''
        @summary: Verifies the common attributes for all compute events
        @param event: Contains event details (actual data) to be verified.
        @type event: Dictionary
        '''
        failure = 'Expected {0} field in event to be {1}, was {2}'
        image_id = event.payload.image_ref_url.rsplit('/')[-1]

        self.assertEqual(server.tenant_id, event.payload.tenant_id,
                         msg=failure.format('tenant id', server.tenant_id,
                                            event.payload.tenant_id))
        self.assertEqual(event.payload.user_id, server.user_id,
                         msg=failure.format('user id', server.user_id,
                                            event.payload.user_id))
        self.assertEqual(event.payload.instance_type_id, int(server.flavor.id),
                         msg=failure.format('flavor id', server.flavor.id,
                                            event.payload.instance_type_id))
        self.assertEqual(event.payload.instance_type, flavor.name,
                         msg=failure.format('flavor name', flavor.name,
                                            event.payload.instance_type))
        self.assertEqual(event.payload.memory_mb, flavor.ram,
                         msg=failure.format('RAM size', flavor.ram,
                                            event.payload.memory_mb))
        self.assertEqual(event.payload.disk_gb, flavor.disk,
                         msg=failure.format('disk size', flavor.disk,
                                            event.payload.disk_gb))
        self.assertEqual(event.payload.instance_id, server.id,
                         msg=failure.format('server id', server.id,
                                            event.payload.instance_id))
        self.assertEqual(event.payload.display_name, server.name,
                         msg=failure.format('server name', server.name,
                                            event.payload.display_name))
        self.assertEqual(image_id, server.image.id,
                         msg=failure.format('image id', server.image.id,
                                            image_id))


class RbacComputeFixture(ComputeFixture):
    '''
    @summary: Creates Creator and Observer Users with RBAC specific roles
    '''

    @classmethod
    def setUpClass(cls):
        super(RbacComputeFixture, cls).setUpClass()
        # Initialize compute provider for Creator user
        config = _MCP()
        creator_user_auth = {AuthConfig.SECTION_NAME: 
            {'username': config.auth.creator, 
            'api_key': config.auth.creator_key}}
        creator_user_conf = config.mcp_override(creator_user_auth)
        cls.compute_provider_for_creator_user = _ComputeAPIProvider(
            creator_user_conf)
        cls.compute_provider_for_creator_user.compute_public_url = (
            cls.compute_provider.compute_public_url)
        cls.compute_provider_for_creator_user.tenant_id = (
            cls.compute_provider.tenant_id)
        creator_user_server_client = ServerAPIClient(
            url=cls.compute_provider_for_creator_user.compute_public_url,
            auth_token=cls.compute_provider_for_creator_user.auth_token)
        cls.creator_servers_client = creator_user_server_client
        creator_user_flavor_client = FlavorsApiClient(
            url=cls.compute_provider_for_creator_user.compute_public_url,
            auth_token=cls.compute_provider_for_creator_user.auth_token)
        cls.creator_flavors_client = creator_user_flavor_client
        creator_user_image_client = ImagesAPIClient(
            url=cls.compute_provider_for_creator_user.compute_public_url,
            auth_token=cls.compute_provider_for_creator_user.auth_token,
            serialize_format=cls.config.misc.serializer,
            deserialize_format=cls.config.misc.deserializer)
        cls.creator_images_client = creator_user_image_client
        creator_user_keypairs_client = KeypairsClient(
            url=cls.compute_provider_for_creator_user.compute_public_url,
            auth_token=cls.compute_provider_for_creator_user.auth_token,
            serialize_format=cls.config.misc.serializer,
            deserialize_format=cls.config.misc.deserializer)
        cls.creator_keypairs_client = creator_user_keypairs_client
        creator_user_vnc_client = VncConsoleClient(
            url=cls.compute_provider_for_creator_user.compute_public_url,
            auth_token=cls.compute_provider_for_creator_user.auth_token,
            serialize_format=cls.config.misc.serializer,
            deserialize_format=cls.config.misc.deserializer)
        cls.creator_vnc_client = creator_user_vnc_client
        creator_user_limits_client = LimitsApiClient(
            url=cls.compute_provider_for_creator_user.compute_public_url,
            auth_token=cls.compute_provider_for_creator_user.auth_token,
            serialize_format=cls.config.misc.serializer,
            deserialize_format=cls.config.misc.deserializer)
        cls.creator_limits_client = creator_user_limits_client

        # Initialize compute provider for Observer user
        observer_user_auth = {AuthConfig.SECTION_NAME: 
            {'username': config.auth.observer, 
            'api_key': config.auth.observer_key}}
        observer_user_conf = config.mcp_override(observer_user_auth)
        cls.compute_provider_for_observer_user = _ComputeAPIProvider(
            observer_user_conf)
        cls.compute_provider_for_observer_user.compute_public_url = (
            cls.compute_provider.compute_public_url)
        cls.compute_provider_for_observer_user.tenant_id = (
            cls.compute_provider.tenant_id)
        observer_user_server_client = ServerAPIClient(
            url=cls.compute_provider_for_observer_user.compute_public_url,
            auth_token=cls.compute_provider_for_observer_user.auth_token)
        cls.observer_servers_client = observer_user_server_client
        observer_user_flavor_client = FlavorsApiClient(
            url=cls.compute_provider_for_observer_user.compute_public_url,
            auth_token=cls.compute_provider_for_observer_user.auth_token)
        cls.observer_flavors_client = observer_user_flavor_client
        observer_user_image_client = ImagesAPIClient(
            url=cls.compute_provider_for_observer_user.compute_public_url,
            auth_token=cls.compute_provider_for_observer_user.auth_token,
            serialize_format=cls.config.misc.serializer,
            deserialize_format=cls.config.misc.deserializer)
        cls.observer_images_client = observer_user_image_client
        observer_user_keypairs_client = KeypairsClient(
            url=cls.compute_provider_for_observer_user.compute_public_url,
            auth_token=cls.compute_provider_for_observer_user.auth_token,
            serialize_format=cls.config.misc.serializer,
            deserialize_format=cls.config.misc.deserializer)
        cls.observer_keypairs_client = observer_user_keypairs_client
        observer_user_vnc_client = VncConsoleClient(
            url=cls.compute_provider_for_observer_user.compute_public_url,
            auth_token=cls.compute_provider_for_observer_user.auth_token,
            serialize_format=cls.config.misc.serializer,
            deserialize_format=cls.config.misc.deserializer)
        cls.observer_vnc_client = observer_user_vnc_client
        observer_user_limits_client = LimitsApiClient(
            url=cls.compute_provider_for_observer_user.compute_public_url,
            auth_token=cls.compute_provider_for_observer_user.auth_token,
            serialize_format=cls.config.misc.serializer,
            deserialize_format=cls.config.misc.deserializer)
        cls.observer_limits_client = observer_user_limits_client


class DnsaasIntegrationFixture(ComputeFixture):
    '''
    @summary: Addes DNS as a Service functionality
    '''

    @classmethod
    def setUpClass(cls):
        super(DnsaasIntegrationFixture, cls).setUpClass()
        # Auth to Identity Standartization between projects
        cls.config.identity_api = cls.config.auth
        base_url = cls.config.auth.base_url
        cls.config.identity_api.authentication_endpoint = base_url
        # Initialize DNSAAS providers       
        cls.ptr_provider = _PtrProvider(cls.config, cls.fixture_log)


class RackconnectIntegrationFixture(ComputeFixture):
    '''
    @summary: Adds Rackconnect functionality
    '''

    @classmethod
    def setUpClass(cls):
        super(RackconnectIntegrationFixture, cls).setUpClass()
        # Auth Rackconnect Initialization
        cls.config.identity_api = cls.config.auth
        base_url = cls.config.auth.base_url
        cls.config.identity_api.authentication_endpoint = base_url
        # Initialize RackConnect providers       
        cls.rcc_provider = _RackconnectProvider(cls.config, cls.fixture_log)


class CreateServerFixture(ComputeFixture):
    '''
    @summary: Creates a server using defaults from the test data,
                         waits for active state.
    '''

    @classmethod
    def setUpClass(cls, name=None,
                   imageRef=None, flavorRef=None,
                   personality=None, metadata=None,
                   diskConfig=None, networks=None):

        '''
        @summary:Creates a server and waits for server to reach active status
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
        @param networks:The networks to which you want to attach the server
        @type networks: String
        '''

        super(CreateServerFixture, cls).setUpClass()
        if name is None:
            name = rand_name('testservercc')
        if imageRef is None:
            imageRef = cls.image_ref
        if flavorRef is None:
            flavorRef = cls.flavor_ref
        cls.flavor_ref = flavorRef
        cls.image_ref = imageRef
        create_response = cls.servers_client.\
                            create_server(
                                          name, imageRef,
                                          flavorRef,
                                          personality=personality,
                                          metadata=metadata,
                                          disk_config=diskConfig,
                                          networks=networks)
        cls.created_server = create_response.entity
        try:
            wait_response = cls.compute_provider.wait_for_server_status(
                                                       cls.created_server.id,
                                                       status.ACTIVE)
            wait_response.entity.adminPass = cls.created_server.adminPass
        except TimeoutException as exception:
            cls.assertClassSetupFailure(exception.message)
        except BuildErrorException as exception:
            cls.assertClassSetupFailure(exception.message)
        finally:
            cls.resources.add(cls.created_server.id,
                              cls.servers_client.delete_server)
        cls.server_response = wait_response
        if cls.server_response.entity.status != status.ACTIVE:
            cls.assertClassSetupFailure('Server %s did not reach active state',
                                         cls.created_server.id)

    @classmethod
    def tearDownClass(cls):
        super(CreateServerFixture, cls).tearDownClass()


class ResizeServerFixture(CreateServerFixture):
    '''
    @Summary: Create an active server, resizes it and waits for
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
    @param networks:The networks to which you want to attach the server
    @type networks: String
    @param resize_flavor: Flavor to which Server needs to be resized
    @type resize_flavor: String
    '''

    @classmethod
    def setUpClass(cls, name=None, imageRef=None, flavorRef=None,
                   personality=None, metadata=None, diskConfig=None,
                   networks=None, resize_flavor=None):

        super(ResizeServerFixture, cls).setUpClass(name=None,
                                                   imageRef=None,
                                                   flavorRef=None,
                                                   personality=None,
                                                   metadata=None,
                                                   diskConfig=None,
                                                   networks=None)

        if resize_flavor != None:
            cls.resize_flavor = resize_flavor
        else:
            cls.resize_flavor = cls.flavor_ref_alt

        try:
            cls.servers_client.resize(cls.created_server.id,
                                      cls.resize_flavor)
            wait_response = cls.compute_provider.\
                            wait_for_server_status(cls.created_server.id,
                                                   status.VERIFY_RESIZE)
        except TimeoutException as exception:
            cls.assertClassSetupFailure(exception.message)
        except BuildErrorException as exception:
            cls.assertClassSetupFailure(exception.message)
        cls.resize_server = wait_response.entity
        if cls.resize_server.status != status.VERIFY_RESIZE:
            cls.assertClassSetupFailure('Server %s did not reach VerifyResize',
                                        cls.resize_server.id)

    @classmethod
    def tearDownClass(cls):
        super(ResizeServerFixture, cls).tearDownClass()


class ConfirmResizeFixture(ResizeServerFixture):
    '''
    @Summary: Create an active server, resizes it and confirms resize.
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
    @param networks:The networks to which you want to attach the server
    @type networks: String
    @param resize_flavor: Flavor to which Server needs to be resized
    @type resize_flavor: String
    '''

    @classmethod
    def setUpClass(cls, name=None, imageRef=None, flavorRef=None,
                   personality=None, metadata=None, diskConfig=None,
                   networks=None, resize_flavor=None):

        super(ConfirmResizeFixture, cls).setUpClass(name=None,
                                                    imageRef=None,
                                                    flavorRef=None,
                                                    personality=None,
                                                    metadata=None,
                                                    diskConfig=None,
                                                    networks=None,
                                                    resize_flavor=None)

        try:
            cls.servers_client.confirm_resize(cls.created_server.id)
            wait_response = cls.compute_provider. \
                            wait_for_server_status(cls.created_server.id,
                                                    status.ACTIVE)
        except TimeoutException as exception:
            cls.assertClassSetupFailure(exception.message)
        except BuildErrorException as exception:
            cls.assertClassSetupFailure(exception.message)
        cls.confirm_resize_server = wait_response.entity
        if cls.confirm_resize_server.status != status.ACTIVE:
            cls.assertClassSetupFailure('Server %s did not reach Active state',
                                        cls.confirm_resize_server.id)

    @classmethod
    def tearDownClass(cls):
        super(ConfirmResizeFixture, cls).tearDownClass()


class RevertResizeFixture(ResizeServerFixture):
    '''
    @Summary: Creates a server, resizes the server,
    reverts the resize and waits for active state.
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
    @param networks:The networks to which you want to attach the server
    @type networks: String
    @param resize_flavor: Flavor to which Server needs to be resized
    @type resize_flavor: String
    '''

    @classmethod
    def setUpClass(cls, name=None, imageRef=None, flavorRef=None,
                   personality=None, metadata=None, diskConfig=None,
                   networks=None, resize_flavor=None):
        super(RevertResizeFixture, cls).setUpClass(
                                                   name=None,
                                                   imageRef=None,
                                                   flavorRef=None,
                                                   personality=None,
                                                   metadata=None,
                                                   diskConfig=None,
                                                   networks=None,
                                                   resize_flavor=None)
        try:
            cls.servers_client.revert_resize(cls.created_server.id)
            wait_response = cls.compute_provider.wait_for_server_status(
                                                   cls.created_server.id,
                                                   status.ACTIVE)
        except TimeoutException as exception:
            cls.assertClassSetupFailure(exception.message)
        except BuildErrorException as exception:
            cls.assertClassSetupFailure(exception.message)
        cls.revert_resize_server = wait_response.entity
        if cls.revert_resize_server.status != status.ACTIVE:
            cls.assertClassSetupFailure('Server %s did not reach Active state',
                                        cls.revert_resize_server.id)

    @classmethod
    def tearDownClass(cls):
        super(RevertResizeFixture, cls).tearDownClass()


class RescueServerFixture(CreateServerFixture):
    '''
    @Summary: Makes a rescue request for the server
                 and waits for the rescued state.
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
    @param networks:The networks to which you want to attach the server
    @type networks: String
    '''

    @classmethod
    def setUpClass(cls, name=None, imageRef=None,
                   flavorRef=None, personality=None,
                   metadata=None, diskConfig=None,
                   networks=None):
        super(RescueServerFixture, cls).setUpClass(name=None,
                                              imageRef=None,
                                              flavorRef=None,
                                              personality=None,
                                              metadata=None,
                                              diskConfig=None,
                                              networks=None)
        try:
            cls.servers_client.rescue(cls.created_server.id)
            wait_response = cls.compute_provider.\
                            wait_for_server_status(cls.created_server.id,
                                                   status.RESCUE)
        except TimeoutException as exception:
            cls.assertClassSetupFailure(exception.message)
        except BuildErrorException as exception:
            cls.assertClassSetupFailure(exception.message)
        cls.rescue_server = wait_response.entity
        if cls.rescue_server.status != status.RESCUE:
            cls.assertClassSetupFailure('Server %s did not reach Rescue state',
                                        cls.rescue_server.id)

    @classmethod
    def tearDownClass(cls):
        super(RescueServerFixture, cls).tearDownClass()


class RebuildServerFixture(CreateServerFixture):
    '''
    @Summary: Creates an Active server, Rebuilds the server using the
            configured secondary image and waits for the active state.
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
    @param networks:The networks to which you want to attach the server
    @type networks: String
    '''

    @classmethod
    def setUpClass(cls, name=None, imageRef=None,
                   flavorRef=None, personality=None,
                   metadata=None, diskConfig=None,
                   networks=None, rebuild_image_ref=None):
        super(RebuildServerFixture, cls).setUpClass(
                                                    name=None,
                                                    imageRef=None,
                                                    flavorRef=None,
                                                    personality=None,
                                                    metadata=None,
                                                    diskConfig=None,
                                                    networks=None,)
        if rebuild_image_ref == None:
            cls.rebuild_image_ref = cls.image_ref_alt
        else:
            cls.rebuild_image_ref = rebuild_image_ref
        try:
            cls.servers_client.rebuild(cls.created_server.id,
                                       cls.rebuild_image_ref)
            wait_response = cls.compute_provider.\
                            wait_for_server_status(cls.created_server.id,
                                                   status.ACTIVE)
        except TimeoutException as exception:
            cls.assertClassSetupFailure(exception.message)
        except BuildErrorException as exception:
            cls.assertClassSetupFailure(exception.message)

        cls.rebuild_server = wait_response.entity
        if cls.rebuild_server.status != status.ACTIVE:
            cls.assertClassSetupFailure('Server %s did not reach Active state',
                                        cls.rebuild_server.id)

    @classmethod
    def tearDownClass(cls):
        super(RebuildServerFixture, cls).tearDownClass()


class RebootServerHardFixture(CreateServerFixture):
    '''
    @Summary: Performs a hard reboot on the created server
                 and waits for the active state.
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
    @param networks:The networks to which you want to attach the server
    @type networks: String
    '''

    @classmethod
    def setUpClass(cls, name=None, imageRef=None,
                   flavorRef=None, personality=None,
                   metadata=None, diskConfig=None,
                   networks=None):
        super(RebootServerHardFixture, cls).\
            setUpClass(
                       name=None,
                       imageRef=None,
                       flavorRef=None,
                       personality=None,
                       metadata=None,
                       diskConfig=None,
                       networks=None)
        try:
            cls.servers_client.reboot(cls.created_server.id, reboot.HARD)
            wait_response = cls.compute_provider.\
                    wait_for_server_status(cls.created_server.id,
                                           status.ACTIVE)
            cls.reboot_response = wait_response
        except TimeoutException as exception:
            cls.assertClassSetupFailure(exception.message)
        except BuildErrorException as exception:
            cls.assertClassSetupFailure(exception.message)
        if wait_response.entity.status != status.ACTIVE:
            cls.assertClassSetupFailure('Server %s did not reach Active state',
                                        cls.created_server.id)

    @classmethod
    def tearDownClass(cls):
        super(RebootServerHardFixture, cls).tearDownClass()
        cls.resources.release()


class RebootServerSoftFixture(CreateServerFixture):
    '''
    @Summary: Performs a soft reboot on the created server
                and waits for the active state.
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
    @param networks:The networks to which you want to attach the server
    @type networks: String
    '''

    @classmethod
    def setUpClass(cls, name=None, imageRef=None,
                   flavorRef=None, personality=None,
                   metadata=None, diskConfig=None,
                   networks=None):
        super(RebootServerSoftFixture, cls).\
            setUpClass(
                       name=None,
                       imageRef=None,
                       flavorRef=None,
                       personality=None,
                       metadata=None,
                       diskConfig=None,
                       networks=None)
        try:
            cls.servers_client.reboot(cls.created_server.id, reboot.SOFT)
            wait_response = cls.compute_provider.\
                wait_for_server_status(cls.created_server.id, status.ACTIVE)
            cls.reboot_response = wait_response
        except TimeoutException as exception:
            cls.assertClassSetupFailure(exception.message)
        except BuildErrorException as exception:
            cls.assertClassSetupFailure(exception.message)
        if cls.wait_response.entity.status != status.ACTIVE:
            cls.assertClassSetupFailure('Server %s did not reach Active state',
                                        cls.created_server.id)

    @classmethod
    def tearDownClass(cls):
        super(RebootServerSoftFixture, cls).tearDownClass()
        cls.resources.release()


class ComputeFixtureParameterized(BaseParameterizedTestFixture):
    '''
    @summary: Fixture for an Parameterized Compute test.
    '''

    @classmethod
    def setUpClass(cls):
        super(ComputeFixtureParameterized, cls).setUpClass()
        cls.resources = ResourcePool()
        cls.compute_provider = _ComputeAPIProvider(cls.config, cls.fixture_log)
        cls.atomhopper_provider = AtomHopperProvider(
                     cls.config.compute_api.atom_hopper_url, cls.config)
        cls._set_clients_from_provider()
        cls.flavor_ref = cls.config.compute_api.flavor_ref
        cls.image_ref = cls.config.compute_api.image_ref
        cls.image_ref_alt = cls.config.compute_api.image_ref_alt
        cls.flavor_ref_alt = cls.config.compute_api.flavor_ref_alt
        low_limit_user_auth = {AuthConfig.SECTION_NAME:
                          {'username': cls.config.auth.low_limit_username,
                           'api_key': cls.config.auth.low_limit_user_password}}
        cls.low_limit_conf = cls.config.mcp_override(low_limit_user_auth)
        cls.compute_provider_for_low_limits_user = _ComputeAPIProvider(
                                                            cls.low_limit_conf,
                                                            cls.fixture_log)

    @classmethod
    def tearDownClass(cls):
        super(ComputeFixtureParameterized, cls).tearDownClass()
        cls.resources.release()
        cls.flavors_client.delete_exception_handler(ExceptionHandler())

    @classmethod
    def _set_clients_from_provider(cls, provider=None):
        if provider is None:
            provider = cls.compute_provider
            ah_provider = cls.atomhopper_provider
            cls.flavors_client = provider.flavors_client
            cls.flavors_client.add_exception_handler(ExceptionHandler())
            cls.servers_client = provider.servers_client
            cls.images_client = provider.images_client
            cls.limits_client = provider.limits_client
            cls.hosts_client = provider.hosts_client
            cls.atomhopper_client = ah_provider.client

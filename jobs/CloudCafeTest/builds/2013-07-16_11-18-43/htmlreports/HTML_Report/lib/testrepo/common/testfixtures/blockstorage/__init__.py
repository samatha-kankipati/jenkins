'''
@summary: Base Classes for Test Suites (Collections of Test Cases) for Cloud Block Storage
@note: Correspondes DIRECTLY TO A unittest.TestCase
@see: http://docs.python.org/library/unittest.html#unittest.TestCase
@copyright: Copyright (c) 2012 Rackspace US, Inc.
'''
import os
from ccengine.common.tools import datagen

from testrepo.common.testfixtures.fixtures import\
        BaseTestFixture  as _BaseTestFixture,\
        BaseParameterizedTestFixture as _BaseParameterizedTestFixture
from ccengine.providers.blockstorage.lunr_api import LunrAPIProvider as\
        _LunrAPIProvider
from ccengine.providers.blockstorage.storage_node_api import\
        StorageNodeAPIProvider as _StorageNodeAPIProvider
from ccengine.providers.blockstorage.volumes_api import VolumesAPIProvider as\
        _VolumesAPIProvider
from ccengine.providers.atomhopper import AtomHopperProvider as\
        _AtomHopperProvider
from ccengine.providers.compute.compute_api import ComputeAPIProvider as\
        _ComputeAPIProvider
from ccengine.providers.compute.volume_attachments_api import\
        VolumeAttachmentsAPIProvider as _VolumeAttachmentsAPIProvider
from ccengine.clients.remote_instance.linux.base_client import\
        BasePersistentLinuxClient as _LinuxClient


class VolumesAPIFixture(_BaseTestFixture):
    '''
    @summary: Foundation for any Cinder API Test.
              Creates instance of VolumesAPIProvider and reference its
              volumes_client.
    @cvar volumes_api_provider: Provider instance for the Volumes API
    @type volumes_api_provider: L{VolumesAPIProvider}
    @cvar volumes_client: Client instance for the Volumes API
    @type volumes_client: L{VolumesAPIProvider}
    '''
    @classmethod
    def setUpClass(cls):
        super(VolumesAPIFixture, cls).setUpClass()
        cls.volumes_api_provider = _VolumesAPIProvider(cls.config)
        cls.volumes_client = cls.volumes_api_provider.volumes_client


class LunrAPIFixture(_BaseTestFixture):
    '''
    @summary: Foundation for any Lunr API Test.
    '''
    @classmethod
    def setUpClass(cls):
        super(LunrAPIFixture, cls).setUpClass()
        #init providers
        cls.LunrAPIProvider = _LunrAPIProvider(cls.config.lunr_api)

        #Breakout Lunr clients
        cls.user_client = cls.LunrAPIProvider.lunr_api_client
        cls.admin_client = cls.LunrAPIProvider.lunr_api_admin_client


class StorageNodeAPIFixture(LunrAPIFixture):
    '''
    @summary: Foundation for any Storage Node API Test.
              Includes lunr_api provider, user and admin clients
    '''
    @classmethod
    def setUpClass(cls):
        super(StorageNodeAPIFixture, cls).setUpClass()
        cls.StorageNodeAPIProvider = _StorageNodeAPIProvider(cls.config)

        #List storage nodes
        storage_node_list = cls.LunrAPIProvider.list_storage_nodes()

        #Create SNAPI Clients
        cls.snapi_clients = []
        for node in storage_node_list:
            cls.snapi_clients.append(
                cls.StorageNodeAPIProvider.create_snapi_client(node))

        #Volumes cleanup dict
        cls.expected_volumes = {}


class CloudBlockStorage_IntegrationFixture(_BaseTestFixture):
    '''
    @summary: Foundation for any Cloud Block Storage test integration all
              API's relevant to the CloudBlockStorage product.  Instantiates:
              Volumes API Provider
              Compute API Provider
              Volume Attachments API Provider
              Atomhopper Provider
    '''
    @classmethod
    def setUpClass(cls):
        super(CloudBlockStorage_IntegrationFixture, cls).setUpClass()
        cls.volumes_api_provider = _VolumesAPIProvider(cls.config)
        cls.compute_api_provider = _ComputeAPIProvider(cls.config)
        cls.volume_attachments_api_provider = _VolumeAttachmentsAPIProvider(
            cls.config)
        cls.atomhopper_provider = _AtomHopperProvider(
            cls.config.volumes_api.atom_feed_url, config=cls.config)


class CloudBlockStorage_ComputeIntegrationFixture(
        CloudBlockStorage_IntegrationFixture):
    '''
    @summary: Foundation for any Cloud Block Storage test requiring a server
              to be built and access to all api's.
    '''
    @classmethod
    def setUpClass(cls):
        super(CloudBlockStorage_ComputeIntegrationFixture, cls).setUpClass()

        #Create test server
        cls.fixture_log.info('Creating test server')
        image = cls.config.compute_api.image_ref
        flavor = cls.config.compute_api.flavor_ref
        cls.server_name = datagen.timestamp_string(
            'CinderAPI_ServerIntegration_')
        cls.create_server_response = cls.compute_api_provider.\
            create_active_server(
                image_ref=image, flavor_ref=flavor, name=cls.server_name)

        if not cls.create_server_response.ok:
            cls.assertClassSetupFailure('Server Create Failed in setup')

        cls.testserver = cls.create_server_response.entity
        if cls.testserver.status == 'ERROR':
            cls.assertClassSetupFailure(
                'Server Create Failed in setup, server is in Error state')

        cls.fixture_log.debug('{0}'.format(cls.testserver))
        cls.server_id = cls.testserver.id
        cls.public_ipv4 = cls.testserver.addresses.public.ipv4
        cls.admin_pass = cls.testserver.adminPass

        #Comment out the stuff above first, then paste the new stuff in below
        #this comment, but before the prints
        cls.fixture_log.debug("#Copy this into the test for debug testing")
        cls.fixture_log.debug("cls.server_id = '{0}'".format(cls.server_id))
        cls.fixture_log.debug(
            "cls.testserver = cls.compute_api_provider. "
            "servers_client.get_server(cls.server_id)")
        cls.fixture_log.debug("cls.server_name = '{0}'".format(cls.server_name))
        cls.fixture_log.debug("cls.public_ipv4 = '{0}'".format(cls.public_ipv4))
        cls.fixture_log.debug("cls.admin_pass = '{0}'".format(cls.admin_pass))

    @classmethod
    def tearDownClass(cls):
        #delete server
        par = cls.compute_api_provider.servers_client.delete_server(
            cls.server_id)
        if not par.ok:
            cls.assertClassTeardownFailure(
                'Unable to delete server in teardown')

        #Finish local teardown class before doing parent teardown class
        super(CloudBlockStorage_ComputeIntegrationFixture, cls).tearDownClass()


class CloudBlockStorage_LinuxIntegrationFixture(
        CloudBlockStorage_ComputeIntegrationFixture):

    @classmethod
    def setUpClass(cls):
        super(CloudBlockStorage_LinuxIntegrationFixture, cls).setUpClass()
        #Create active volume
        cls.fixture_log.info('Creating an active volume')
        vname = datagen.timestamp_string('VolumesWriteTest')
        cls.testvolume_size = cls.volumes_api_provider.min_volume_size
        cls.testvolume_type = 'ssd'
        r = cls.volumes_api_provider.create_available_volume(
            vname, cls.testvolume_size, cls.testvolume_type)
        if not r.ok:
            cls.assertClassSetupFailure(
                'Available volume create failed in setup')
        cls.testvolume = r.entity
        cls.fixture_log.debug('{0}'.format(cls.testvolume))

        #Attach volume to server
        cls.fixture_log.info('Attaching Volume to the server')
        cls.testvolume_device_name = '/dev/xvde'
        cls.testvolume_fstype = 'ext3'
        cls.volume_file_name = datagen.random_string()
        cls.testvolume_mountpoint = datagen.timestamp_string(
            prefix='/mnt/cbsvolume-')
        cls.volume_file_path = os.path.join(
            cls.testvolume_mountpoint, cls.volume_file_name)

        resp = cls.volume_attachments_api_provider.client.attach_volume(
            cls.server_id, cls.testvolume.id, cls.testvolume_device_name)
        if not resp.ok:
            cls.assertClassSetupFailure('Active volume successfully created')

        cls.testvolume_attachment = r.entity
        if resp.entity is None:
            cls.assertClassSetupFailure('VolumeAttachment object is None')

        #Create ssh connection
        cls.initialize_ssh_connection()

        #Format device
        cls.fixture_log.info('Formatting attached volume on test server')
        sshresp = cls.remote_server.format_disk_device(
            cls.testvolume_device_name, cls.testvolume_fstype)
        cls.fixture_log.info(str(sshresp))

        #Mount disk
        cls.fixture_log.info('Mounting formatted volume on test server')
        sshresp = cls.remote_server.mount_disk_device(
            cls.testvolume_device_name, cls.testvolume_mountpoint,
            cls.testvolume_fstype)
        cls.fixture_log.info(str(sshresp))

    @classmethod
    def tearDownClass(cls):
        #Unmount volume
        #Returns nothing, therefore unable to verify
        cls.fixture_log.info('Unmounting volume on remote server in teardown')
        cls.remote_server.unmount_disk_device(cls.testvolume_mountpoint)

        #detach volume
        par = cls.volume_attachments_api_provider.detach_volume_confirmed(
            cls.testvolume_attachment.volume_id, cls.server_id)
        if not par.ok:
            cls.assertClassTeardownFailure('Volume Detach Failed in teardown')

        #Wait for status 'available'
        #If this happens, then we know the volume unmounted correctly :\
        par = cls.volumes_api_provider.wait_for_volume_status(
            cls.testvolume.id, 'available')
        if not par.ok:
            cls.assertClassTeardownFailure(
                'Volume never became available after detaching, in teardown')

        #delete volume
        par = cls.volumes_api_provider.delete_volume_confirmed(
            cls.testvolume.id)
        if not par.ok:
            cls.assertClassTeardownFailure(
                'Unable to verify that volume deleted properly in teardown')

        #finish local teardown class before doing parent teardown class
        super(CloudBlockStorage_ComputeIntegrationFixture, cls).tearDownClass()

    @classmethod
    def initialize_ssh_connection(cls):
        #Create ssh connection
        cls.fixture_log.info('Creating SSH Session to test server')
        cls.remote_server = _LinuxClient(
            cls.public_ipv4, 'root', cls.admin_pass)


class VolumesAPI_ParameterizedFixture(_BaseParameterizedTestFixture):
    '''
    @summary: Foundation for any Paramaterized Cinder API Tests.
              Creates instance of VolumesAPIProvider and reference its
              volumes_client.
    @cvar volumes_api_provider: Provider instance for the Volumes API
    @type volumes_api_provider: L{VolumesAPIProvider}
    @cvar volumes_client: Client instance for the Volumes API
    @type volumes_client: L{VolumesAPIProvider}
    '''
    @classmethod
    def setUpClass(cls):
        super(VolumesAPI_ParameterizedFixture, cls).setUpClass()
        cls.volumes_api_provider = _VolumesAPIProvider(cls.config)
        cls.volumes_client = cls.volumes_api_provider.volumes_client

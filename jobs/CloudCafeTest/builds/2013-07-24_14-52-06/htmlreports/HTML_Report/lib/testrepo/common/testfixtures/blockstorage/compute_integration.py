from ccengine.common.tools import datagen
from ccengine.providers.compute.compute_api import ComputeAPIProvider
from ccengine.providers.blockstorage.volumes_api import VolumesAPIProvider
from ccengine.providers.compute.volume_attachments_api import \
    VolumeAttachmentsAPIProvider
from ccengine.clients.remote_instance.linux.base_client import \
    BasePersistentLinuxClient
from testrepo.common.testfixtures.fixtures import BaseTestFixture


class ComputeIntegrationFixture(BaseTestFixture):
    @classmethod
    def setUpClass(cls):
        super(ComputeIntegrationFixture, cls).setUpClass()
        cls._class_teardown_tasks = []
        cls.volumes_provider = VolumesAPIProvider(cls.config)
        cls.compute_provider = ComputeAPIProvider(cls.config)
        cls.volume_attachments_provider = VolumeAttachmentsAPIProvider(
            cls.config)

    @classmethod
    def tearDownClass(cls):
        #TODO: Figure out a way to make this run independently of tearDownClass
        cls._do_class_teardown_tasks()
        super(ComputeIntegrationFixture, cls).tearDownClass()

    @classmethod
    def _do_class_teardown_tasks(cls):
        for func, args, kwargs in reversed(cls._class_teardown_tasks):
            cls.fixture_log.error(
                "Running teardown task: {0}({1}, {2})".format(
                    func.__name__,
                    ", ".join([str(arg) for arg in args]),
                    ", ".join(["{0}={1}".format(
                        str(k), str(kwargs[k])) for k in kwargs])))
            try:
                func(*args, **kwargs)
            except Exception as exception:
                #Pretty prints method signature in the following format:
                #"classTearDown failure: Unable to execute FnName(a, b, c=42)"
                cls.fixture_log.exception(exception)
                cls.fixture_log.error(
                    "classTearDown failure: Exception occured while trying to"
                    " execute class teardown task: {0}({1}, {2})".format(
                        func.__name__,
                        ", ".join([str(arg) for arg in args]),
                        ", ".join(["{0}={1}".format(
                            str(k), str(kwargs[k])) for k in kwargs])))

    @classmethod
    def addTearDownClassTask(cls, function, *args, **kwargs):
        """Named to match unittest's addCleanup"""
        cls._class_teardown_tasks.append((function, args or [], kwargs or {}))

    @classmethod
    def setup_class_server(
            cls, server_name=None, add_cleanup=True, image=None, flavor=None):
        #TODO: Once this can be run from setUpClass, any classmethod, or
        #any instance method without sacrificing cleanup, it'll be the only
        #version required, and won't have to have 'class' in it's name ;)

        cls.fixture_log.info('Setting up server')
        server_name = server_name or datagen.timestamp_string(
            'CBSQE_TestServer_')

        #Create test server
        image = image or cls.config.compute_api.image_ref
        flavor = flavor or cls.config.compute_api.flavor_ref
        resp = cls.compute_provider.create_active_server(
            image_ref=image, flavor_ref=flavor, name=server_name)

        assert resp.ok, \
            'Server create failed in setup_server with a {0}'.format(
                resp.status_code)

        assert resp.entity is not None, \
            ("Server create failed in setup_server: Could not deserialize "
             "server create response body")

        assert resp.entity.status != 'ERROR', \
            "Server create failed in setup_server: server is in Error state"

        if add_cleanup:
            cls.fixture_log.info(
                'Adding class cleanup task for {0}(id={1})'.format(
                    server_name, resp.entity.id))
            cls.addTearDownClassTask(
                cls.compute_provider.servers_client.delete_server,
                resp.entity.id)

        return resp.entity

    def setup_server(
            self, server_name=None, add_cleanup=True, image=None, flavor=None):
        #TODO: Make addClassCleanup work like a singleton (registry?), and then
        #there won't be a need for an instance-method version of setup_server.

        self.fixture_log.info('Setting up server')
        server_name = server_name or datagen.timestamp_string(
            'CBSQE_TestServer_')

        #Create test server
        image = image or self.config.compute_api.image_ref
        flavor = flavor or self.config.compute_api.flavor_ref
        resp = self.compute_provider.create_active_server(
            image_ref=image, flavor_ref=flavor, name=server_name)

        assert resp.ok, (
            'Server create failed in setup_server with a {0}'.format(
                resp.status_code))

        assert resp.entity is not None, (
            "Server create failed in setup_server: Recieved unexpected "
            "reponse / could not deserialize response body")

        assert resp.entity.status != 'ERROR', (
            "Server create failed in setup_server: server is in Error state")

        if add_cleanup:
            self.fixture_log.info('Adding cleanup task for {0}(id={1})'.format(
                server_name, resp.entity.id))
            self.addCleanup(
                self.compute_provider.servers_client.delete_server,
                resp.entity.id)

        return resp.entity

    def setup_volume(
            self, size=None, volume_type_name='SATA', display_name=None,
            add_cleanup=True):

        self.fixture_log.info('Setting up volume')
        size = size or self.config.volumes_api.min_volume_size

        vname = display_name or datagen.timestamp_string(
            'CBSQE_{0}_TestVolume_'.format(volume_type_name))

        resp = self.volumes_provider.create_available_volume(
            vname, size, volume_type_name)

        assert resp.ok, \
            'Volume create failed in setup_server with a {0}'.format(
                resp.status_code)

        assert resp.entity is not None, \
            ("Volume create failed in setup_server: Could not deserialize "
             "volume create response body")

        if add_cleanup:
            self.fixture_log.info('Adding cleanup task for {0}(id={1})'.format(
                display_name, resp.entity.id))
            self.addCleanup(
                self.volumes_provider.delete_volume_confirmed,
                resp.entity.id)

        return resp.entity

    def auto_attach_volume_to_server(
            self, server_id, volume_id, expected_volume_status=None,
            add_cleanup=True):
        """Returns a VolumeAttachment object"""

        self.fixture_log.info('Auto attaching volume to server')

        resp = self.volume_attachments_provider.client.attach_volume(
            server_id, volume_id)

        assert resp.ok, \
            ("Volume attachment failed in auto_attach_volume_to_server with a "
             "{0}".format(resp.status_code))

        assert resp.entity is not None, \
            ("Volume attachment failed in auto_attach_volume_to_server: "
             "Could not deserialize volume attachment response body")

        assert str(resp.entity.volume_id) == str(volume_id), \
            ("Volume attachment failed in auto_attach_volume_to_server: "
             "Volume attachment volume_id did not match expected volume_id")

        if add_cleanup:
            args = [resp.entity.id, server_id]
            self.addCleanup(
                self.volume_attachments_provider.detach_volume_confirmed,
                *args)

        if expected_volume_status is not False:
            expected_volume_status = expected_volume_status or 'in-use'
            prov_resp = self.volumes_provider.wait_for_volume_status(
                volume_id, expected_volume_status, timeout=500)

            assert prov_resp.ok, \
                ("Volume failed to attain '{0}' status within allotted "
                 "timeout.".format(resp.status_code))

        return resp.entity

    def explicit_attach_volume_to_server(
            self, server_id, volume_id, volume_device_name,
            expected_volume_status=None, add_cleanup=True):
        """Attaches a volume to a server as volume_device_name
        Returns a VolumeAttachment object"""

        self.fixture_log.info('Attaching volume to server as {0}'.format(
            volume_device_name))

        resp = self.volume_attachments_provider.client.attach_volume(
            server_id, volume_id, volume_device_name)

        assert resp.ok, \
            ("Volume attachment failed in auto_attach_volume_to_server with a "
             "{0}".format(resp.status_code))

        assert resp.entity is not None, \
            ("Volume attachment failed in auto_attach_volume_to_server: "
             "Could not deserialize volume attachment response body")

        assert str(resp.entity.volume_id) == str(volume_id), \
            ("Volume attachment failed in auto_attach_volume_to_server: "
             "Volume attachment volume_id did not match expected volume_id")

        if add_cleanup:
            args = [resp.entity.id, server_id]
            self.addCleanup(
                self.volume_attachments_provider.detach_volume_confirmed,
                *args)

        if expected_volume_status is not False:
            expected_volume_status = expected_volume_status or 'in-use'
            prov_resp = self.volumes_provider.wait_for_volume_status(
                volume_id, expected_volume_status, timeout=500)

            assert prov_resp.ok, \
                ("Volume failed to attain '{0}' status within allotted "
                 "timeout.".format(resp.status_code))

        return resp.entity

    def detach_and_delete_volume(
            self, server_id, volume_id, volume_attachment_id,
            assert_success=False):

        resp = self.volume_attachments_provider.detach_volume_confirmed(
            volume_attachment_id, server_id)

        if assert_success:
            assert resp.ok, \
                ("Volume dettachment failed in detach_and_delete_volume with a"
                 " {0}".format(resp.status_code))

            resp = self.volumes_provider.delete_volume_confirmed(volume_id)
            assert resp.ok, \
                ("Volume dettachment failed in detach_and_delete_volume with a"
                 " {0}".format(resp.status_code))


class LinuxIntegrationMixin(object):

    @staticmethod
    def setup_ssh_connection(
            server_ipv4_address, server_user, server_user_password):

        ssh_conn = BasePersistentLinuxClient(
            ip_address=server_ipv4_address, username=server_user,
            password=server_user_password)

        return ssh_conn

    @staticmethod
    def mount_and_format_attached_volume(
            ssh_conn, device_name, filesystem_type, mountpoint):
        """Mounts and formats an already-attached volume on a server.
        initialize_ssh_connection() must have already been called for this
        method to work"""

        #Format device
        ssh_conn.format_disk_device(device_name, filesystem_type)

        #Mount disk
        ssh_conn.mount_disk_device(device_name, mountpoint, filesystem_type)

    @staticmethod
    def verify_remote_file_size(
            ssh_conn, expected_file_size_in_bytes, full_path_to_file):

        ssh_resp = ssh_conn.get_file_size_bytes(full_path_to_file)

        assert ssh_resp is not None, \
            'wc -c of file on mounted volume over ssh failed to return'

        ssh_resp_data = ssh_resp.split(' ')[0]

        fail_msg = (
            "Unable to verify remote file size. Expected {0} bytes but "
            "observed {1} bytes".format(
                int(expected_file_size_in_bytes), int(ssh_resp_data)))

        assert int(expected_file_size_in_bytes) == int(ssh_resp_data), fail_msg


class BlockStorageLinuxIntegrationFixture(
        ComputeIntegrationFixture, LinuxIntegrationMixin):

    class LinuxBlockStorageTestEnv(object):
        def __init__(
                self, server=None, volume=None, attachment=None, ssh_conn=None,
                device_name=None, file_system_type=None, mount_point=None):
            self.server = server
            self.volume = volume
            self.attachment = attachment
            self.ssh_conn = ssh_conn
            self.device_name = device_name
            self.file_system_type = file_system_type
            self.mount_point = mount_point

        def connect(self):
            """Provided for convenience when the connection needs to be
            re-initialized with the same info."""

            self.ssh_conn = LinuxIntegrationMixin.setup_ssh_connection(
                server_ipv4_address=self.server.addresses.public.ipv4,
                server_user='root', server_user_password=self.server.adminPass)

    def setup_server_with_volume_attached(self, server=None, volume=None):
        """
        Sets up a server and attached volume.  Optionally initializes an ssh
        connection as root to the server.
        Returns a LinuxBlockStorageTestEnv object with server, volume,
        attachment, and optionally ssh_conn setup.

        """

        server = server or self.setup_server()
        volume = volume or self.setup_volume()
        attachment = self.auto_attach_volume_to_server(
            server.id, volume.id)

        testenv = BlockStorageLinuxIntegrationFixture.LinuxBlockStorageTestEnv(
            server=server, volume=volume, attachment=attachment)

        return testenv

    def setup_mounted_and_formatted_volume_on_server(
            self, device_name=None, file_system_type=None, mount_point=None,
            server_domain_object=None, volume_domain_object=None,
            attachment_domain_object=None, ssh_conn=None):

        """
        Sets up server with volume attached, mounted and formatted

        Returns a LinuxBlockStorageTestEnv object, which contains all
        information about the server, volume, and linux environment relevant to
        Blockstorage testing.  Optionally allows for specifiying none, any, or
        all components of the LinuxBlockStorageTestEnv.

        """

        device_name = device_name or '/dev/xvde'
        file_system_type = file_system_type or 'ext3'
        server = server_domain_object or self.setup_server()
        volume = volume_domain_object or self.setup_volume()

        attachment = attachment_domain_object or \
            self.explicit_attach_volume_to_server(
                server.id, volume.id, device_name)

        mount_point = datagen.timestamp_string(prefix='/mnt/cbsvolume-')

        testenv = BlockStorageLinuxIntegrationFixture.LinuxBlockStorageTestEnv(
            server=server, volume=volume, attachment=attachment,
            ssh_conn=ssh_conn, device_name=device_name,
            file_system_type=file_system_type, mount_point=mount_point)

        if ssh_conn is None:
            testenv.connect()

        self.mount_and_format_attached_volume(
            testenv.ssh_conn, device_name, file_system_type, mount_point)

        return testenv

    def write_and_verify_data_on_mounted_volume(
            self, ssh_conn, mount_point, file_name=None, file_block_size=None,
            file_block_count=None):

        # Setup
        file_name = file_name or datagen.timestamp_string("cbs_write_test_")
        full_path_to_file = "{0}/{1}".format(mount_point, file_name)
        file_block_size = file_block_size or 4096
        file_block_count = file_block_count or 25600
        expected_file_size = file_block_size * file_block_count

        # Issue write command
        ssh_conn.write_random_data_to_disk(
            mount_point, file_name, file_block_size, file_block_count)

        # Verify written file size
        self.verify_remote_file_size(
            ssh_conn, expected_file_size, full_path_to_file)

        #TODO:  Add md5 hash verification, make verification a separate
        #method so that it can be called independently.


class BlockStorageWindowsIntegrationFixture(ComputeIntegrationFixture):

    class WindowsBlockStorageTestEnv(object):
        def __init__(
                self, server=None, volume=None, attachment=None):
            self.server = server
            self.volume = volume
            self.attachment = attachment

    @classmethod
    def setup_class_server(
            cls, server_name=None, add_cleanup=True, image=None, flavor=None):
        """overrides default image to windows."""

        image = image or cls.config.compute_api.windows_image_ref

        super(BlockStorageWindowsIntegrationFixture, cls).setup_class_server(
            server_name=server_name, add_cleanup=add_cleanup, image=image,
            flavor=flavor)

    def setup_server(
            self, server_name=None, add_cleanup=True, image=None, flavor=None):
        """overrides default image to windows."""

        image = image or self.config.compute_api.windows_image_ref

        super(BlockStorageWindowsIntegrationFixture, self).setup_server(
            server_name=server_name, add_cleanup=add_cleanup, image=image,
            flavor=flavor)

import time

from ccengine.providers.base_provider import BaseProvider
from ccengine.providers.auth.auth_api import AuthProvider as _AuthProvider
from ccengine.providers.identity.v2_0.identity_api import\
    IdentityAPIProvider as _IdentityAPIProvider
from ccengine.providers.atomhopper import AtomHopperProvider
from ccengine.clients.compute.servers_api import ServerAPIClient
from ccengine.clients.compute.images_api import ImagesAPIClient
from ccengine.clients.compute.flavors_api import FlavorsApiClient
from ccengine.clients.compute.hosts_api import HostsAPIClient
from ccengine.clients.compute.vnc_console_api import VncConsoleClient
from ccengine.clients.compute.keypairs_api import KeypairsClient
from ccengine.clients.atomhopper import AtomHopperClient
from ccengine.clients.compute.limits_api import LimitsApiClient
from ccengine.clients.remote_instance.instance_client import \
    InstanceClientFactory
from ccengine.domain.types import NovaServerStatusTypes as ServerStatus
from ccengine.domain.types import NovaImageStatusTypes as ImageStatus
from ccengine.domain.types import NovaManagedMetaStatusTypes as ManagedStatus
from ccengine.common.tools.datagen import rand_name
from ccengine.common.tools.reports_ohthree_helper import ReportsOhThreeHelper
from ccengine.common.constants.compute_constants import HTTPResponseCodes
from ccengine.common.exceptions.compute import ItemNotFound, DeleteException, \
    TimeoutException, BuildErrorException


class ComputeAPIProvider(BaseProvider):
    '''
    @summary: Provider Module for the Compute REST API
    @note: Should be the primary interface to a test case or external tool.
    @copyright: Copyright (c) 2012 Rackspace US, Inc.
    '''

    def __init__(self, config, logger=None):
        super(ComputeAPIProvider, self).__init__()
        if config is None:
            self.provider_log.warning('empty (=None) config recieved in init')
            # Load configuration from default.conf
            self.config = _AuthProvider
        else:
            self.config = config

        #Configure auth/identity
        if (config.identity_api.api_key is not None or
                config.identity_api.password is not None):
            self.identity_api_provider = _IdentityAPIProvider(self.config)
            self.identity_data = self.identity_api_provider.authenticate()
            self.auth_token = self.identity_data.response.entity.token.id
            compute_service = (self.identity_data.response.entity
                               .serviceCatalog
                               .get_service(self.config.compute_api
                                            .identity_service_name))
        else:
            self.auth_provider = _AuthProvider(self.config)
            self.auth_data = self.auth_provider.authenticate()
            self.auth_token = self.auth_data.token.id
            compute_service = (self.auth_data
                               .get_service(self.config.compute_api.
                                            identity_service_name))

        # Load compute config data
        self.compute_region = self.config.compute_api.region
        if (config.identity_api.api_key is not None or
                config.identity_api.password is not None):
            self.compute_public_url = compute_service. \
                get_endpoint(self.compute_region).publicURL
            self.tenant_id = compute_service. \
                get_endpoint(self.compute_region).tenantId

        else:
            self.compute_public_url = compute_service. \
                get_endpoint_by_region(self.compute_region).publicURL
            self.tenant_id = compute_service. \
                get_endpoint_by_region(self.compute_region).tenantId

        # Initialize compute api clients
        self.flavors_client = FlavorsApiClient(self.compute_public_url,
                                               self.auth_token,
                                               self.config.misc.serializer,
                                               self.config.misc.deserializer)
        self.servers_client = ServerAPIClient(self.compute_public_url,
                                              self.auth_token,
                                              self.config.misc.serializer,
                                              self.config.misc.deserializer)
        self.images_client = ImagesAPIClient(self.compute_public_url,
                                             self.auth_token,
                                             self.config.misc.serializer,
                                             self.config.misc.deserializer)
        self.limits_client = LimitsApiClient(self.compute_public_url,
                                             self.auth_token,
                                             self.config.misc.serializer,
                                             self.config.misc.deserializer)
        self.hosts_client = HostsAPIClient(self.compute_public_url,
                                           self.auth_token,
                                           self.config.misc.serializer,
                                           self.config.misc.deserializer)
        self.vnc_client = VncConsoleClient(self.compute_public_url,
                                           self.auth_token,
                                           self.config.misc.serializer,
                                           self.config.misc.deserializer)
        self.keypairs_client = KeypairsClient(self.compute_public_url,
                                              self.auth_token,
                                              self.config.misc.serializer,
                                              self.config.misc.deserializer)

    def create_active_server(self, name=None, image_ref=None, flavor_ref=None,
                             personality=None, metadata=None, accessIPv4=None,
                             accessIPv6=None, disk_config=None, networks=None,
                             key_name=None):
        '''
        @summary:Creates a server and waits for server to reach active status
        @param name: The name of the server.
        @type name: String
        @param image_ref: The reference to the image used to build the server.
        @type image_ref: String
        @param flavor_ref: The flavor used to build the server.
        @type flavor_ref: String
        @param metadata: A dictionary of values to be used as metadata.
        @type metadata: Dictionary. The limit is 5 key/values.
        @param personality: A list of dictionaries for files to be
         injected into the server.
        @type personality: List
        @param accessIPv4: IPv4 address for the server.
        @type accessIPv4: String
        @param accessIPv6: IPv6 address for the server.
        @type accessIPv6: String
        @param disk_config: MANUAL/AUTO/None
        @type disk_config: String
        @return: Response Object containing response code and
         the server domain object
        @rtype: Request Response Object
        '''

        if name is None:
            name = rand_name('testserver')
        if image_ref is None:
            image_ref = self.config.compute_api.image_ref
        if flavor_ref is None:
            flavor_ref = self.config.compute_api.flavor_ref

        create_response = (self.servers_client
                           .create_server(name, image_ref, flavor_ref,
                                          personality=personality,
                                          metadata=metadata,
                                          accessIPv4=accessIPv4,
                                          accessIPv6=accessIPv6,
                                          disk_config=disk_config,
                                          networks=networks,
                                          key_name=key_name))
        assert create_response.status_code == HTTPResponseCodes.CREATE_SERVER,\
            ('Unexpected create server response with status code {0}, '
               'reason: {1}, content: {2}. Expected status code {3}.'.format(
                create_response.status_code, create_response.reason,
                create_response.content, HTTPResponseCodes.CREATE_SERVER))
        server_obj = create_response.entity
        wait_response = self.wait_for_server_status(server_obj.id,
                                                    ServerStatus.ACTIVE)
        # Add the admin pass from the create command
        # into the final wait response
        wait_response.entity.adminPass = server_obj.adminPass
        # assert wait_response.status_code == 200
        return wait_response

    def rebuild_and_await(self, server_id, image_ref, name=None,
                          personality=None, metadata=None,
                          accessIPv4=None, accessIPv6=None, disk_config=None,
                          networks=None, admin_password=None):
        '''
        @summary:  Rebuild instance and wait for server status ACTIVE
        @return:  Rebuilt server entity object

        '''
        resp = self.servers_client.rebuild(server_id, image_ref, name=name,
                                           metadata=metadata,
                                           disk_config=disk_config,
                                           accessIPv4=accessIPv4,
                                           accessIPv6=accessIPv6,
                                           personality=personality,
                                           admin_pass=admin_password,
                                           networks=networks)
        assert resp.status_code is 202
        rebuilt_server = self.wait_for_server_status(server_id,
                                                     ServerStatus.ACTIVE)
        return rebuilt_server.entity

    def resize_and_await(self, server_id, new_flavor):
        '''
        @summary:  Resize instance and wait for server status VERIFY RESIZE
        @return:  Resized server entity object

        '''

        resp = self.servers_client.resize(server_id, new_flavor)
        assert resp.status_code is 202
        resized_server = self.wait_for_server_status(server_id,
                                                     ServerStatus
                                                     .VERIFY_RESIZE)
        return resized_server.entity

    def resize_and_confirm(self, server_id, new_flavor):
        '''
        @summary:  Resize instance then confirm resize.
            Wait for server status ACTIVE
        @return:  (Confirmed) Resized server entity object

        '''

        self.resize_and_await(server_id, new_flavor)
        resp = self.servers_client.confirm_resize(server_id)
        assert resp.status_code is 204
        resized_server = self.wait_for_server_status(server_id,
                                                     ServerStatus.ACTIVE)
        return resized_server.entity

    def resize_and_revert(self, server_id, new_flavor):
        '''
        @summary:  Resize instance then revert resize.
            Wait for server status ACTIVE
        @return:  (Reverted) Resized server entity object

        '''
        self.resize_and_await(server_id, new_flavor)
        resp = self.servers_client.revert_resize(server_id)
        assert resp.status_code is 202
        resized_server = self.wait_for_server_status(server_id,
                                                     ServerStatus.ACTIVE)
        return resized_server.entity

    def reboot_and_await(self, server_id, reboot_type):
        '''
        @summary:  Reboot instance then wait for server status ACTIVE
        @return:  Rebooted server entity object

        '''
        resp = self.servers_client.reboot(server_id, reboot_type)
        assert resp.status_code is 202
        rebooted_server = self.wait_for_server_status(server_id,
                                                      ServerStatus.ACTIVE)
        return rebooted_server.entity

    def change_password_and_await(self, server_id, new_password):
        '''
        @summary:  Change password on instance then
            wait for server status ACTIVE
        @return:  Server entity object of server where password was changed

        '''
        resp = self.servers_client.change_password(server_id, new_password)
        assert resp.status_code is 202
        changed_pw_server = self.wait_for_server_status(server_id,
                                                        ServerStatus.ACTIVE)
        return changed_pw_server.entity

    def rescue_and_await(self, server_id):
        '''
        @summary:  Rescue instance and waits for server status RESCUE.
        @return:  Server entity object

        '''
        resp = self.servers_client.rescue(server_id)
        assert resp.status_code is 200
        rescued_server = self.wait_for_server_status(server_id,
                                                     ServerStatus.RESCUE)
        return rescued_server.entity

    def unrescue_and_await(self, server_id):
        '''
        @summary:  Unrescues instance and waits for server status ACTIVE.
        @return:  Server entity object
        @note: It is assumed that the ServerStatus of the server being
            passed in is in a RESCUE state.

        '''
        resp = self.servers_client.unrescue(server_id)
        assert resp.status_code is 202
        rescued_server = self.wait_for_server_status(server_id,
                                                     ServerStatus.ACTIVE)
        return rescued_server.entity

    def rescue_and_unrescue(self, server_id):
        '''
        @summary:  Rescue instance and waits for server status RESCUE.
            Then unrescues the instance and waits for server status ACTIVE.
        @return:  Server entity object

        '''
        self.rescue_and_await(server_id)
        unrescued_server = self.unrescue_and_await(server_id)
        return unrescued_server

    def create_server_no_wait(self, name=None, imageRef=None, flavorRef=None,
                              networks=None):
        '''
        @summary: Creates a server with defaults if they are not provided as
            parameters. Does not wait for a status.
        '''
        if name is None:
            name = rand_name('testserver')
        else:
            name = rand_name(str(name))
        if imageRef is None:
            imageRef = self.config.compute_api.image_ref
        if flavorRef is None:
            flavorRef = self.config.compute_api.flavor_ref
        create_response = self.servers_client.create_server(name, imageRef,
                                                            flavorRef,
                                                            networks=networks)
        return create_response

    def wait_for_server_status(self, server_id, status_to_wait_for,
                               timeout=None):
        '''
        @summary: Polls server server_id details
            until status_to_wait_for is met.

        '''
        if status_to_wait_for == ServerStatus.DELETED:
            return self.wait_for_server_to_be_deleted(server_id)
        server_response = self.servers_client.get_server(server_id)
        server_obj = server_response.entity
        time_waited = 0
        interval_time = self.config.compute_api.build_interval
        timeout = timeout or self.config.compute_api.server_status_timeout
        while (server_obj.status.lower() != status_to_wait_for.lower() and
               server_obj.status.lower() != ServerStatus.ERROR.lower() and
               time_waited <= timeout):
            server_response = self.servers_client.get_server(server_id)
            server_obj = server_response.entity
            time.sleep(interval_time)
            time_waited += interval_time
        if time_waited > timeout:
            raise TimeoutException('Request timed out waiting on Server: '
                                   'uuid: {0}\n'
                                   'timeout: {1}\n'
                                   'status_to_wait_for: {2}\n'
                                   .format(server_id,
                                           timeout,
                                           status_to_wait_for))
        if server_obj.status.lower() == ServerStatus.ERROR.lower():
            server_build_error = ""
            try:
                server_build_error = \
                    (ReportsOhThreeHelper(self.config.compute_api.env_name)
                     .get_server_build_error(server_obj.id))
                server_build_error = "****" + server_build_error
            except:
                pass
            raise BuildErrorException('Build failed. Server with uuid {0} '
                                      'entered ERROR status.\n Reason : \n{1}'
                                      .format(server_id, server_build_error))

        return server_response

    def wait_for_server_error_status(self, server_id, status_to_wait_for,
                                     timeout=None):
        '''
        @summary: Polls server server_id details
            until status_to_wait_for is met.

        '''

        if status_to_wait_for == ServerStatus.DELETED:
            return self.wait_for_server_to_be_deleted(server_id)
        server_response = self.servers_client.get_server(server_id)
        server_obj = server_response.entity
        time_waited = 0
        interval_time = self.config.compute_api.build_interval
        timeout = timeout or self.config.compute_api.server_status_timeout
        while (server_obj.status.lower() != status_to_wait_for.lower() and
               time_waited <= timeout * 10):
            server_response = self.servers_client.get_server(server_id)
            server_obj = server_response.entity
            time.sleep(interval_time)
            time_waited += interval_time
        return server_response

    def wait_for_server_status_from_error(self, server_id, status_to_wait_for,
                                          timeout=None):
        '''
        @summary: Polls server server_id details
            until status_to_wait_for is met.

        '''
        if status_to_wait_for == ServerStatus.DELETED:
            return self.wait_for_server_to_be_deleted(server_id)
        server_response = self.servers_client.get_server(server_id)
        server_obj = server_response.entity
        time_waited = 0
        interval_time = self.config.compute_api.build_interval
        timeout = timeout or self.config.compute_api.server_status_timeout
        while (server_obj.status.lower() != status_to_wait_for.lower() and
               time_waited <= timeout):
            server_response = self.servers_client.get_server(server_id)
            server_obj = server_response.entity
            time.sleep(interval_time)
            time_waited += interval_time
        if time_waited > timeout:
            raise TimeoutException(server_obj.status, server_obj.status,
                                   id=server_obj.id)
        return server_response

    def wait_for_image_status(self, image_id, status_to_wait_for):
        '''
        @summary: Polls image image_id details
            until status_to_wait_for is met.

        '''
        image_response = self.images_client.get_image(image_id)
        image_obj = image_response.entity
        time_waited = 0
        interval_time = self.config.compute_api.build_interval
        while (image_obj.status.lower() != status_to_wait_for.lower() and
               time_waited < self.config.compute_api.server_status_timeout):
            image_response = self.images_client.get_image(image_id)
            image_obj = image_response.entity

            if image_obj.status.lower() is ImageStatus.ERROR.lower():
                message = 'Snapshot failed. ' \
                          'Image with uuid {0} entered ERROR status.'
                raise BuildErrorException(message.format(image_id))

            time.sleep(interval_time)
            time_waited += interval_time
        return image_response

    def wait_for_image_resp_code(self, image_id, code_to_wait_for):
        '''
        @summary: Polls image resp for the specified status code.

        '''
        image_response = self.images_client.get_image(image_id)
        image_obj = image_response.entity
        time_waited = 0
        interval_time = self.config.compute_api.build_interval
        while (image_response.status_code != code_to_wait_for and
               image_obj.status.lower() != ImageStatus.ERROR.lower() and
               time_waited < self.config.compute_api.image_status_timeout):
            image_response = self.images_client.get_image(image_id)
            image_obj = image_response.entity
            time.sleep(interval_time)
            time_waited += interval_time
        return image_response

    def wait_for_image_to_be_deleted(self, image_id):
        '''
        @summary: Waits for the image to be deleted.

        '''

        image_response = self.images_client.delete_image(image_id)
        image_obj = image_response.entity
        time_waited = 0
        interval_time = self.config.compute_api.build_interval

        try:
            while (True):
                image_response = self.images_client.get_image(image_id)
                image_obj = image_response.entity
                if time_waited > self.config.compute_api.server_status_timeout:
                    raise TimeoutException("Timed out while deleting " \
                                           "image id: {0}".format(image_id))
                if image_obj.status.lower() == ImageStatus.DELETED.lower():
                    return
                if image_obj.status.lower() != ImageStatus.ERROR.lower():
                    raise BuildErrorException("Image entered Error state " \
                                              "while deleting, Image id : {0}"
                                              .format(image_id))
                time.sleep(interval_time)
                time_waited += interval_time
        except ItemNotFound:
            pass

    def wait_for_server_to_be_deleted_response_code(self, server_id):
        """
        @summary: Waits for server to be deleted based on response code.
        """
        interval_time = self.config.compute_api.min_polling_interval
        timeout = time.time() + self.config.compute_api.max_delete_wait
        while time.time() < timeout:
            try:
                resp = self.servers_client.get_server(server_id)
                if resp.status_code == HTTPResponseCodes.NOT_FOUND:
                    return
            except ItemNotFound:
                pass
            finally:
                time.sleep(interval_time)

    def wait_for_server_to_be_deleted(self, server_id):
        '''
        @summary: Waits for the server to be deleted.

        '''
        time_waited = 0
        interval_time = self.config.compute_api.build_interval
        try:
            while (True):
                server_response = self.servers_client.get_server(server_id)
                server_obj = server_response.entity
                if time_waited > self.config.compute_api.server_status_timeout:
                    raise TimeoutException("Timed out while deleting " \
                                           "server id: {0}".format(server_id))
                if server_obj.status.lower() != ServerStatus.ERROR.lower():
                    time.sleep(interval_time)
                    time_waited += interval_time
                    continue
                    if server_obj.status.lower() != ServerStatus.ERROR.lower():
                        raise BuildErrorException("Server entered Error " \
                                                  "state while deleting, " \
                                                  "server id : {0}"
                                                  .format(server_id))
                time.sleep(interval_time)
                time_waited += interval_time
        except ItemNotFound:
            pass

    def wait_for_server_metadata(self, server_id, metadata_to_wait_for,
                                 timeout=300):
        '''
        @summary: Polls server server_id
            until status_to_wait_for is set on the server.

        '''
        metadata_response = self.servers_client.list_server_metadata(server_id)
        metadata = metadata_response.entity
        time_waited = 0
        interval_time = self.config.compute_api.build_interval
        timeout = timeout or self.config.compute_api.server_metadata_timeout
        while (metadata_to_wait_for not in metadata.__dict__.keys() and
               time_waited <= timeout):
            metadata_response = self.servers_client.list_server_metadata(
                server_id)
            metadata = metadata_response.entity
            time.sleep(interval_time)
            time_waited += interval_time
            if time_waited > timeout:
                raise TimeoutException
        return metadata_response

    def wait_for_server_metadata_status(
            self, server_id, metadata_key, metadata_value, timeout=300):
        '''
       @summary: Polls server server_id
           until metadata  is set on the server with the value
           metadata_status.
       '''
        metadata_response = self.servers_client.list_server_metadata(server_id)
        metadata = metadata_response.entity
        time_waited = 0
        interval_time = self.config.compute_api.build_interval
        timeout = timeout or self.config.compute_api.server_metadata_timeout
        while (getattr(metadata, metadata_key) != metadata_value and
                       time_waited <= timeout):
            metadata_response = self.servers_client.list_server_metadata(
                server_id)
            metadata = metadata_response.entity
            time.sleep(interval_time)
            time_waited += interval_time
            if time_waited > timeout:
                raise TimeoutException
        return metadata_response

    def delete_servers(self, server_list, timeout=None):
        '''
        @summary: Deletes the servers from a server id list.
            Will log and return undeleted servers ids,
            no exceptions will be raised

        '''
        timeout = timeout or self.config.compute_api.server_delete_timeout
        for server_id in server_list:
            self.servers_client.delete_server(server_id)
        not_deleted = []
        for server_id in server_list:
            time_count = 0
            while True:
                try:
                    r = self.servers_client.get_server(server_id)
                    if r.status_code == HTTPResponseCodes.NOT_FOUND:
                        #server deleted
                        break
                    if time_count > timeout:
                        #server not deleted within expected timeout
                        msg = 'Unable to delete server %s' % (server_id)
                        self.provider_log.debug(msg)
                        not_deleted.append(server_id)
                        break
                except ItemNotFound:
                    break
                finally:
                    time.sleep(1)
                    time_count += 1
        return not_deleted

    def delete_servers_with_status(self, status):
        '''
        @summary: Deletes servers by status

        '''
        servers = self.servers_client.list_servers(status=status)
        delete_list = []
        for server in servers.entity:
            delete_list.append(server.id)
        not_deleted = self.delete_servers(delete_list)
        return not_deleted

    def get_remote_instance_client(self, server, ip_address=None,
                                   username=None, password=None):
        '''
        @summary: Gets an client of the server
        @param server: Instance uuid id of the server
        @type server: String
        @param ip_address: IPv4 address of the server
        @type ip_address: String
        @param username: Valid user of the server
        @type username: String
        @param password: Valid user password of the server
        @type password: String
        @return: Either IPv4 or IPv6 address of instance
        @rtype: String

        '''
        image = server.image
        image_response = self.images_client.get_image(image.id)
        image = image_response.entity
        image_metadata = image.metadata

        os_distro = (image_metadata.os_distro if
                     hasattr(image_metadata, "os_distro") else None)
        os_type = (image_metadata.os_type if
                   hasattr(image_metadata, "os_type") else None)
        if password is None:
            password = server.adminPass

        ''' Either os_distro is None or os_distro is not in the available
            client list then set os_distro to os_type and instantiate client
            for os_type'''
        if (os_distro is None or
            os_distro not in InstanceClientFactory.clientList):
            if os_type is None:
                os_type = self.config.compute_api.os_type
            os_distro = os_type

        if ip_address is None:
            ip_address = self.get_public_ip_address(server)

        return InstanceClientFactory.get_instance_client(ip_address=ip_address,
                                                         username=username,
                                                         password=password,
                                                         os_distro=os_distro,
                                                         server_id=server.id)

    def get_public_ip_address(self, server):
        '''
        @summary: Gets the public ip address of instance
        @param server: Instance uuid id of the server
        @type server: String
        @return: Either IPv4 or IPv6 address of instance
        @rtype: String

        '''
        if self.config.compute_api.ip_address_version_for_ssh == '4':
            return server.addresses.public.ipv4
        else:
            return server.addresses.public.ipv6

    def wait_for_managed_status(self, server, status_to_wait_for):
        '''
        @summary: Polls service level automation metadata
            until status_to_wait_for is met

        '''
        remote_client = self.get_remote_instance_client(server)
        server_xenstore_meta_resp = remote_client.get_xen_user_metadata()
        while ('rax_service_level_automation' not in server_xenstore_meta_resp.keys()):
            server_xenstore_meta_resp = remote_client.get_xen_user_metadata()
        rax_serv_automation = server_xenstore_meta_resp['rax_service_level_automation']
        time_waited = 0
        interval_time = self.config.compute_api.build_interval
        while (rax_serv_automation.lower() != status_to_wait_for.lower() and
               time_waited < self.config.compute_api.managed_timeout):
            server_xenstore_meta_resp = remote_client.get_xen_user_metadata()
            rax_serv_automation = server_xenstore_meta_resp['rax_service_level_automation']
            if str(rax_serv_automation.lower()) == str(ManagedStatus.ERROR.lower()):
                message = 'Managed process failed. ' \
                          'Server with uuid {0} entered ERROR status.'
                raise BuildErrorException(message.format(server.id))

            time.sleep(interval_time)
            time_waited += interval_time
        return rax_serv_automation

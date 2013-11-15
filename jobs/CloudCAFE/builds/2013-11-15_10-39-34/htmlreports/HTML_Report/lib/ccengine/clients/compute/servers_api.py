from ccengine.clients.base_client import BaseMarshallingClient
from ccengine.domain.compute.response.server import Server
from ccengine.domain.compute.response.server import Addresses
from ccengine.domain.compute.request.server_requests import Rebuild, \
            CreateImage, RevertResize, CreateServer, RescueMode, \
            ExitRescueMode, AddFixedIP, RemoveFixedIP
from ccengine.domain.compute.request.server_requests import ChangePassword, \
                                                ConfirmResize, Resize, Reboot, \
                                                MigrateServer, ConfirmServerMigration, \
                                                Lock, Unlock, Start, Stop, Suspend, \
                                                Resume, Pause, Unpause, UpdateServer
from ccengine.domain.compute.metadata import MetadataItem, Metadata
from ccengine.common.tools.datagen import rand_name
from ccengine.domain.compute.response.rescue import Rescue
from urlparse import urlparse


class ServerAPIClient(BaseMarshallingClient):

    def __init__(self, url, auth_token, serialize_format=None,
                 deserialize_format=None):
        '''
        @param logger: PBLogger instance to use,
         Generates private logger if None
        @type logger: L{PBLogger}
        '''
        super(ServerAPIClient, self).__init__(serialize_format,
                                            deserialize_format)
        self.auth_token = auth_token
        self.default_headers['X-Auth-Token'] = auth_token
        ct = ''.join(['application/', self.serialize_format])
        accept = ''.join(['application/', self.deserialize_format])
        self.default_headers['Content-Type'] = ct
        self.default_headers['Accept'] = accept
        self.url = url

    def list_servers(self, name=None, image=None, flavor=None,
                     status=None, marker=None, limit=None, changes_since=None,
                     image_schedule=None, body=None, requestslib_kwargs=None):
        '''
        @summary: Lists IDs, names, and links for all servers filtered
         by optional query params
        @param image: The image id
        @type image: String
        @param flavor: The flavor id
        @type flavor: String
        @param name: The server name
        @type name: String
        @param status: The server status
        @type status: String
        @param marker: The ID of the last item in the previous list
        @type marker: String
        @param limit: The page size
        @type limit: Int
        @param changes-since: The changes-since time. The list contains servers
         that have been deleted since the changes-since time
        @type changes-since: dateTime
        @return: Response Object containing response code and body with details
         of servers filtered by the params
        @rtype: Response Object
        '''

        '''
            GET
            v2/{tenant_id}/servers?{params}
        '''
        params = {'image': image, 'flavor': flavor, 'name': name,
                  'status': status, 'marker': marker,
                  'limit': limit, 'changes-since': changes_since,
                  'RAX-SI:image_schedule': image_schedule}
        url = '%s/servers' % self.url
        server_response = self.request('GET', url, params=params,
                                       response_entity_type=Server,
                                       request_entity=body,
                                       requestslib_kwargs=requestslib_kwargs)
        return server_response

    def list_servers_including_body(self, **kwargs):

        body = CreateImage("fake_name", {})

        return self.list_servers(body=body, **kwargs)

    def list_servers_with_detail(self, image=None, flavor=None, name=None,
                                 status=None, marker=None,
                                 limit=None, changes_since=None,
                                 image_schedule=None, requestslib_kwargs=None,
                                 body=None, all_tenants=None):

        '''
        @summary: Gets all the server details filtered by
         the optional query params
        @param image: The image id
        @type image: String
        @param flavor: The flavor id
        @type flavor: String
        @param name: The server name
        @type name: String
        @param status: The server status
        @type status: String
        @param marker: The ID of the last item in the previous list
        @type marker: String
        @param limit: The page size
        @type limit: Int
        @param changes-since: The changes-since time. The list contains servers
         that have been deleted since the changes-since time
        @type changes-since: dateTime
        @return: Response Object containing response code and body with details
         of servers filtered by the params
        @rtype: Response Object
        '''

        '''
            GET
            v2/{tenant_id}/servers/detail?{params}
        '''
        params = {'image': image, 'flavor': flavor, 'name': name,
                  'status': status, 'marker': marker, 'limit': limit,
                  'changes-since': changes_since,
                  'RAX-SI:image_schedule': image_schedule,
                  'all_tenants' : all_tenants}
        url = '%s/servers/detail' % (self.url)
        server_response = self.request('GET', url, params=params,
                                       response_entity_type=Server,
                                       request_entity=body,
                                       requestslib_kwargs=requestslib_kwargs)
        return server_response

    def list_servers_with_detail_including_body(self, **kwargs):

        body = CreateImage("fake_name", {})

        return self.list_servers_with_detail(body=body, **kwargs)

    def get_server(self, server_id, body=None, requestslib_kwargs=None):
        '''
        @summary: Gets the server details.
        @param server_id: The id of an existing server.
        @type server_id: String
        @return: Response Object containing response code and
         body with details of server
        @rtype: Response Object
        '''

        '''
            GET
            v2/{tenant_id}/servers/id
        '''
        self.server_id = server_id
        url_new = str(server_id)
        url_scheme = urlparse(url_new).scheme
        url = url_new if url_scheme else '%s/servers/%s' % (self.url,
                                                            self.server_id)
        server_response = self.request('GET', url,
                                       response_entity_type=Server,
                                       requestslib_kwargs=requestslib_kwargs)
        return server_response

    def get_server_diagnostics(self, server_id, requestslib_kwargs=None):
        self.server_id = server_id
        url_new = str(server_id)
        url_scheme = urlparse(url_new).scheme
        url = url_new if url_scheme else '%s/servers/%s/diagnostics' % (self.url,
                                                                        self.server_id)
        server_response = self.request('GET', url,
                                       response_entity_type=Server,
                                       requestslib_kwargs=requestslib_kwargs)
        return server_response

    def get_server_including_body(self, server_id, **kwargs):

        body = CreateImage("fake_name", {})

        return self.get_server(server_id, body=body, **kwargs)

    def delete_server(self, server_id, requestslib_kwargs=None):
        '''
        @summary: Deletes the server.
        @param server_id: The id of an existing server.
        @type server_id: String
        @return: Response Object containing response code 204
         on success and empty body
        @rtype: Response Object
        '''

        '''
            DELETE
            v2/{tenant_id}/servers/id
        '''
        self.server_id = server_id
        url = '%s/servers/%s' % (self.url, self.server_id)
        server_response = self.request('DELETE', url,
                                       requestslib_kwargs=requestslib_kwargs)
        return server_response

    def create_server(self, name, image_ref, flavor_ref, personality=None,
                      metadata=None, accessIPv4=None,
                      accessIPv6=None, disk_config=None, networks=None,
                      adminPass=None, key_name=None, requestslib_kwargs=None):

        '''
        @summary: Creates an instance of a server.
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
        @rtype: Response Object
        '''

        '''
            POST
            v2/{tenant_id}/servers
        '''
        server_request_object = CreateServer(name=name, flavorRef=flavor_ref,
                                             imageRef=image_ref,
                                             personality=personality,
                                             metadata=metadata,
                                             accessIPv4=accessIPv4,
                                             accessIPv6=accessIPv6,
                                             diskConfig=disk_config,
                                             networks=networks,
                                             adminPass=adminPass,
                                             key_name=key_name)

        url = '%s/servers' % self.url
        server_response = self.request('POST', url,
                                       response_entity_type=Server,
                                       request_entity=server_request_object,
                                       requestslib_kwargs=requestslib_kwargs)
        return server_response

    def change_password(self, server_id, password, requestslib_kwargs=None):
        '''
        @summary: Changes the root password for the server.
        @param server_id: The id of an existing server.
        @type server_id: String
        @param password: The new password.
        @type password: String.
        @return: Response Object containing response code and the empty
         body on success
        @rtype: Response Object
        '''

        '''
            POST
            v2/{tenant_id}/servers/id/action
        '''
        self.server_id = server_id
        url = '%s/servers/%s/action' % (self.url, self.server_id)
        server_action_response = self.request('POST', url,
                                              request_entity=ChangePassword(password),
                                              requestslib_kwargs=requestslib_kwargs)
        return server_action_response

    def reboot(self, server_id, reboot_type, requestslib_kwargs=None):
        '''
        @summary: Reboots the server - soft/hard based on reboot_type.
        @param server_id: The id of an existing server.
        @type server_id: String
        @param reboot_type: Soft or Hard.
        @type reboot_type: String.
        @return: Response Object containing response code and the empty body
        after the server reboot is applied
        @rtype: Response Object
        '''

        '''
            POST
            v2/{tenant_id}/servers/id/action
        '''
        self.server_id = server_id
        url = '%s/servers/%s/action' % (self.url, self.server_id)
        server_action_response = self.request('POST', url,
                                              request_entity=Reboot(reboot_type),
                                              requestslib_kwargs=requestslib_kwargs)
        return server_action_response

    def rebuild(self, server_id, image_ref, name=None,
                flavor_ref=None, admin_pass=None,
                disk_config=None, metadata=None,
                personality=None, accessIPv4=None, accessIPv6=None,
                requestslib_kwargs=None):
        '''
        @summary: Rebuilds the server
        @param server_id: The id of an existing server.
        @type server_id: String
        @param name: The new name for the server
        @type name: String
        @param image_ref:The image ID.
        @type image_ref: String
        @param flavor_ref:The flavor ID.
        @type flavor_ref: String
        @param admin_pass:The administrator password
        @type admin_pass: String
        @param disk_config:The disk configuration value, which is AUTO or MANUAL
        @type disk_config: String(AUTO/MANUAL)
        @param metadata:A metadata key and value pair.
        @type metadata: Dictionary
        @param personality:The file path and file contents
        @type personality: String
        @param accessIPv4:The IP version 4 address.
        @type accessIPv4: String
        @param accessIPv6:The IP version 6 address
        @type accessIPv6: String
        @return: Response Object containing response code and
         the server domain object
        @rtype: Response Object
        '''

        '''
            POST
            v2/{tenant_id}/servers/id/action
        '''
        self.server_id = server_id
        url = '%s/servers/%s/action' % (self.url, self.server_id)
        rebuild_request_object = Rebuild(name=name, imageRef=image_ref,
                                         flavorRef=flavor_ref,
                                         adminPass=admin_pass,
                                         diskConfig=disk_config,
                                         metadata=metadata,
                                         personality=personality,
                                         accessIPv4=accessIPv4,
                                         accessIPv6=accessIPv6)

        server_action_response = self.request('POST', url,
                                                    response_entity_type=Server,
                                                    request_entity=rebuild_request_object,
                                                    requestslib_kwargs=requestslib_kwargs)
        return server_action_response

    def resize(self, server_id, flavor_ref, disk_config=None,
               requestslib_kwargs=None):
        '''
        @summary: Resizes the server to specified flavor_ref.
        @param server_id: The id of an existing server.
        @type server_id: String
        @param flavor_ref: The flavor id.
        @type flavor_ref: String.
        @return: Response Object containing response code and
         the empty body after the server resize is applied
        @rtype: Response Object
        '''

        '''
            POST
            v2/{tenant_id}/servers/id/action
        '''
        self.server_id = server_id
        url = '%s/servers/%s/action' % (self.url, self.server_id)
        resize_request_object = Resize(flavor_ref, disk_config)

        server_action_response = self.request('POST', url,
                                              request_entity=resize_request_object,
                                              requestslib_kwargs=requestslib_kwargs)
        return server_action_response

    def confirm_resize(self, server_id, requestslib_kwargs=None):
        '''
        @summary: Confirms resize of server
        @param server_id: The id of an existing server.
        @type server_id: String
        @return: Response Object containing response code and the empty
         body after the server resize is applied
        @rtype: Response Object
        '''

        '''
            POST
            v2/{tenant_id}/servers/id/action
        '''
        self.server_id = server_id
        url = '%s/servers/%s/action' % (self.url, self.server_id)
        confirm_resize_request_object = ConfirmResize()
        server_action_response = self.request('POST', url,
                                              request_entity=confirm_resize_request_object,
                                              requestslib_kwargs=requestslib_kwargs)
        return server_action_response

    def revert_resize(self, server_id, requestslib_kwargs=None):
        '''
        @summary: Reverts resize of the server
        @param server_id: The id of an existing server.
        @type server_id: String
        @return: Response Object containing response code and the empty body
         after the server resize is applied
        @rtype: Response Object
        '''

        '''
            POST
            v2/{tenant_id}/servers/id/action
        '''
        self.server_id = server_id
        url = '%s/servers/%s/action' % (self.url, self.server_id)
        server_action_response = self.request('POST', url,
                                              request_entity=RevertResize(),
                                              requestslib_kwargs=requestslib_kwargs)
        return server_action_response

    def migrate_server(self, server_id, requestslib_kwargs=None):
        self.server_id = server_id
        url = '%s/servers/%s/action' % (self.url, self.server_id)
        resp = self.request('POST', url,
                            request_entity=MigrateServer(),
                            requestslib_kwargs=requestslib_kwargs)
        return resp

    def live_migrate_server(self, server_id, requestslib_kwargs=None):
        self.server_id = server_id
        url = '%s/servers/%s/action' % (self.url, self.server_id)
        resp = self.request('POST', url,
                            request_entity=MigrateServer(),
                            requestslib_kwargs=requestslib_kwargs)
        return resp

    def lock_server(self, server_id, requestslib_kwargs=None):
        self.server_id = server_id
        url = '%s/servers/%s/action' % (self.url, self.server_id)
        resp = self.request('POST', url,
                            request_entity=Lock(),
                            requestslib_kwargs=requestslib_kwargs)
        return resp

    def unlock_server(self, server_id, requestslib_kwargs=None):
        self.server_id = server_id
        url = '%s/servers/%s/action' % (self.url, self.server_id)
        resp = self.request('POST', url,
                            request_entity=Unlock(),
                            requestslib_kwargs=requestslib_kwargs)
        return resp

    def stop_server(self, server_id, requestslib_kwargs=None):
        self.server_id = server_id
        url = '%s/servers/%s/action' % (self.url, self.server_id)
        resp = self.request('POST', url,
                            request_entity=Stop(),
                            requestslib_kwargs=requestslib_kwargs)
        return resp

    def start_server(self, server_id, requestslib_kwargs=None):
        self.server_id = server_id
        url = '%s/servers/%s/action' % (self.url, self.server_id)
        resp = self.request('POST', url,
                            request_entity=Start(),
                            requestslib_kwargs=requestslib_kwargs)
        return resp

    def suspend_server(self, server_id, requestslib_kwargs=None):
        self.server_id = server_id
        url = '%s/servers/%s/action' % (self.url, self.server_id)
        resp = self.request('POST', url,
                            request_entity=Suspend(),
                            requestslib_kwargs=requestslib_kwargs)
        return resp

    def resume_server(self, server_id, requestslib_kwargs=None):
        self.server_id = server_id
        url = '%s/servers/%s/action' % (self.url, self.server_id)
        resp = self.request('POST', url,
                            request_entity=Resume(),
                            requestslib_kwargs=requestslib_kwargs)
        return resp

    def pause_server(self, server_id, requestslib_kwargs=None):
        self.server_id = server_id
        url = '%s/servers/%s/action' % (self.url, self.server_id)
        resp = self.request('POST', url,
                            request_entity=Pause(),
                            requestslib_kwargs=requestslib_kwargs)
        return resp

    def unpause_server(self, server_id, requestslib_kwargs=None):
        self.server_id = server_id
        url = '%s/servers/%s/action' % (self.url, self.server_id)
        resp = self.request('POST', url,
                            request_entity=Unpause(),
                            requestslib_kwargs=requestslib_kwargs)
        return resp

    def reset_state(self, server_id, reset_state='error',
                    requestslib_kwargs=None):
        self.server_id = server_id
        url = '%s/servers/%s/action' % (self.url, self.server_id)
        resp = self.request('POST', url,
                            request_entity=MigrateServer(),
                            requestslib_kwargs=requestslib_kwargs)
        return resp

    def rescue(self, server_id, requestslib_kwargs=None):
        '''
        @summary: Enters the server into rescue mode.
        @param server_id: The id of an existing server.
        @type server_id: String
        @return: Response Object containing response code and
         ServerRescueMode domain object
        @rtype: Response Object
        '''

        '''
            POST
            v2/{tenant_id}/servers/id/action
        '''
        self.server_id = server_id
        url = '%s/servers/%s/action' % (self.url, self.server_id)
        rescue_request_object = RescueMode()
        server_action_response = \
            self.request('POST', url,
                         response_entity_type=Rescue,
                         request_entity=rescue_request_object,
                         requestslib_kwargs=requestslib_kwargs)
        return server_action_response

    def unrescue(self, server_id, requestslib_kwargs=None):
        '''
        @summary: Exits rescue mode the specified server is in.
        @param server_id: The id of an existing server.
        @type server_id: String
        @return: Response Object containing response code and
         the Server domain object
        @rtype: Response Object
        '''

        '''
            POST
            v2/{tenant_id}/servers/id/action
        '''
        self.server_id = server_id
        url = '%s/servers/%s/action' % (self.url, self.server_id)
        unrescue_request_object = ExitRescueMode()
        #DOCS say that this call should return a server object,
        #but it currently does not
        server_action_response = \
            self.request('POST', url,
                         response_entity_type=Server,
                         request_entity=unrescue_request_object,
                         requestslib_kwargs=requestslib_kwargs)
        return server_action_response

    def create_image(self, server_id, name=None, metadata=None,
                     requestslib_kwargs=None):
        '''
        @summary: Creates snapshot of the server
        @param server_id: The id of an existing server.
        @type server_id: String
        @param: metadata: A metadata key and value pair.
        @type: Metadata Object
        @return: Response Object containing response code and the empty body
         after the server resize is applied
        @rtype: Response Object
        '''

        '''
            POST
            v2/{tenant_id}/servers/id/action
        '''
        if name is None:
            name = 'new_image'
        self.server_id = server_id
        if name is None:
            name = rand_name("TestImage")
        url = '%s/servers/%s/action' % (self.url, self.server_id)
        create_image_request_object = CreateImage(name, metadata)
        server_action_response = self.request('POST', url,
                                              request_entity=create_image_request_object,
                                              requestslib_kwargs=requestslib_kwargs)

        return server_action_response

    def add_fixed_ip(self, server_id, networkId=None, requestslib_kwargs=None):
        '''
        @summary: Adds additional IP of a network to a server
        @param server_id: The id of an existing server.
        @type server_id: String
        @param: networkId: uuid of the network to get IP on
        @type: String
        @return: Response Object containing response code and the empty body
         after the server resize is applied
        @rtype: Response Object
        '''
        url = '%s/servers/%s/action' % (self.url, self.server_id)
        add_ip = AddFixedIP(networkId=networkId)
        server_action_response = self.request('POST', url,
                                              request_entity=add_ip,
                                              requestslib_kwargs=requestslib_kwargs)
        return server_action_response

    def remove_fixed_ip(self, server_id, ip_address=None,
                        requestslib_kwargs=None):
        '''
        @summary: Removes IP of a network to a server
        @param server_id: The id of an existing server.
        @type server_id: String
        @param: ip_address: IP Address to remove
        @type: String
        @return: Response Object containing response code and the empty body
         after the server resize is applied
        @rtype: Response Object
        '''
        url = '%s/servers/%s/action' % (self.url, self.server_id)
        remove_ip = RemoveFixedIP(ip_address=ip_address)
        server_action_response = self.request('POST', url,
                                              request_entity=remove_ip,
                                              requestslib_kwargs=requestslib_kwargs)
        return server_action_response

    def update_server(self, server_id, name=None, metadata=None,
                      accessIPv4=None, accessIPv6=None,
                      requestslib_kwargs=None):
        """
        @summary: Updates the properties of an existing server.
        @param server_id: The id of an existing server.
        @type server_id: String
        @param name: The name of the server.
        @type name: String
        @param meta: A dictionary of values to be used as metadata.
        @type meta: Dictionary. The limit is 5 key/values.
        @param ipv4: IPv4 address for the server.
        @type ipv4: String
        @param ipv6: IPv6 address for the server.
        @type ipv6: String
        @return: The response code and the updated Server .
        @rtype: Integer(Response code) and Object(Server)
        """
        '''
            PUT
             v2/{tenant_id}/servers/id
        '''
        self.server_id = server_id
        url = '%s/servers/%s' % (self.url, self.server_id)
        request = UpdateServer(name=name, metadata=metadata,
                               accessIPv4=accessIPv4, accessIPv6=accessIPv6)
        server_action_response = self.request('PUT', url,
                                              response_entity_type=Server,
                                              request_entity=request,
                                              requestslib_kwargs=requestslib_kwargs)
        return server_action_response

    def list_addresses(self, server_id, requestslib_kwargs=None):
        """
        @summary: Lists all addresses for a server.
        @param server_id: The id of an existing server.
        @type server_id: String
        @return: Response code and the Addresses
        @rtype: Integer(Response code) and Object(Addresses)
        """
        '''
            GET
             v2/{tenant_id}/servers/id/ips
        '''
        self.server_id = server_id
        url = '%s/servers/%s/ips' % (self.url, self.server_id)
        addresses_response = self.request('GET', url,
                                          response_entity_type=Addresses,
                                          requestslib_kwargs=requestslib_kwargs)
        return addresses_response

    def list_addresses_by_network(self, server_id, network_id,
                                  requestslib_kwargs=None):
        """
        @summary: Lists all addresses of a specific network type for a server.
        @param server_id: The id of an existing server.
        @type server_id: String
        @param network_id: The ID of a network.
        @type network_id: String
        @return: Response code and the Addresses by network.
        @rtype: Integer(Response code) and Object(Addresses)
        """
        '''
            GET
             v2/{tenant_id}/servers/id/ips
        '''
        self.server_id = server_id
        self.network_id = network_id
        url = '%s/servers/%s/ips/%s' % (self.url, self.server_id,
                                        self.network_id)
        server_response = self.request('GET', url,
                                       response_entity_type=Addresses,
                                       requestslib_kwargs=requestslib_kwargs)
        return server_response

    def list_server_metadata(self, server_id, requestslib_kwargs=None):
        '''
        @summary: Returns metadata associated with an server
        @param server_id: server ID
        @type server_id:String
        @return: Metadata associated with an server on success
        @rtype: Response object with metadata dictionary as entity
        '''

        '''
            GET
            v2/{tenant_id}/servers/{server_id}/metadata
        '''
        url = '%s/servers/%s/metadata' % (self.url, server_id)
        server_response = self.request('GET', url,
                                       response_entity_type=Metadata,
                                       requestslib_kwargs=requestslib_kwargs)
        return server_response

    def set_server_metadata(self, server_id, metadata, requestslib_kwargs=None):
        '''
        @summary: Sets metadata for the specified server
        @param server_id: server ID
        @type server_id:String
        @param metadata: Metadata to be set for an server
        @type metadata: dictionary
        @return: Metadata associated with an server on success
        @rtype:  Response object with metadata dictionary as entity
        '''

        '''
            PUT
            v2/{tenant_id}/servers/{server_id}/metadata
        '''
        url = '%s/servers/%s/metadata' % (self.url, server_id)
        request_metadata_object = Metadata(metadata)
        server_response = self.request('PUT', url,
                                       response_entity_type=Metadata,
                                       request_entity=request_metadata_object,
                                       requestslib_kwargs=requestslib_kwargs)
        return server_response

    def update_server_metadata(self, server_id, metadata,
                               requestslib_kwargs=None):
        '''
        @summary: Updates metadata items for the specified server
        @param server_id: server ID
        @type server_id:String
        @param metadata: Metadata to be updated for an server
        @type metadata: dictionary
        @return: Metadata associated with an server on success
        @rtype:  Response object with metadata dictionary as entity
        '''

        '''
            POST
            v2/{tenant_id}/servers/{server_id}/metadata
        '''
        url = '%s/servers/%s/metadata' % (self.url, server_id)
        request_metadata_object = Metadata(metadata)
        server_response = self.request('POST', url,
                                       response_entity_type=Metadata,
                                       request_entity=request_metadata_object,
                                       requestslib_kwargs=requestslib_kwargs)
        return server_response

    def get_server_metadata_item(self, server_id, key, requestslib_kwargs=None):
        '''
        @summary: Retrieves a single metadata item by key
        @param server_id: server ID
        @type server_id:String
        @param key: Key for which metadata item needs to be retrieved
        @type key: String
        @return: Metadata Item for a key on success
        @rtype:  Response object with metadata dictionary as entity
        '''

        '''
            GET
            v2/{tenant_id}/servers/{server_id}/metadata/{key}
        '''
        url = '%s/servers/%s/metadata/%s' % (self.url, server_id, key)
        server_response = self.request('GET', url,
                                       response_entity_type=MetadataItem,
                                       requestslib_kwargs=requestslib_kwargs)
        return server_response

    def set_server_metadata_item(self, server_id, key, value,
                                 requestslib_kwargs=None):
        '''
        @summary: Sets a metadata item for a specified server
        @param server_id: server ID
        @type server_id:String
        @param key: Key for which metadata item needs to be set
        @type key: String
        @return: Metadata Item for the key on success
        @rtype:  Response object with metadata dictionary as entity
        '''

        '''
            PUT
            v2/{tenant_id}/servers/{server_id}/metadata/{key}
        '''
        url = '%s/servers/%s/metadata/%s' % (self.url, server_id, key)
        metadata_item_request = MetadataItem({key: value})
        server_response = self.request('PUT', url,
                                       response_entity_type=MetadataItem,
                                       request_entity=metadata_item_request,
                                       requestslib_kwargs=requestslib_kwargs)
        return server_response

    def delete_server_metadata_item(self, server_id, key,
                                    requestslib_kwargs=None):
        '''
        @summary: Sets a metadata item for a specified server
        @param server_id: server ID
        @type server_id:String
        @param key: Key for which metadata item needs to be set
        @type key: String
        @return: Metadata Item for the key on success
        @rtype:  Response object with metadata dictionary as entity
        '''

        '''
            DELETE
            v2/{tenant_id}/servers/{server_id}/metadata/{key}
        '''
        url = '%s/servers/%s/metadata/%s' % (self.url, server_id, key)
        server_response = self.request('DELETE', url,
                                       requestslib_kwargs=requestslib_kwargs)
        return server_response

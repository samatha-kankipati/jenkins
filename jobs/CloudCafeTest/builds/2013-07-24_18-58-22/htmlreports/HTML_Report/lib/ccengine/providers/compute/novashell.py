'''
@summary: Specifically provides access to Compute (nova) Clients/Helpers
@note: Should be the primary interface to a test case or external tool.
@attention: This is a port of the old provider in the compute module. When the old
smoke test is phased out, this should be moved or renamed appropriately.
@copyright: Copyright (c) 2012 Rackspace US, Inc.
'''
from _socket import inet_aton
import random
import re
import time
import sys

from ccengine.providers.base_provider import BaseProvider
from ccengine.clients.compute.novashell import NovaShellClient
from ccengine.domain.compute.novashell import\
    VolumeTypeDomainObject,\
    ImageDomainObject,\
    FlavorDomainObject,\
    ServerDomainObject

from ccengine.domain.types import\
    NovaServerStatusTypes,\
    NovaVolumeStatusTypes,\
    NovaVolumeSnapshotStatusTypes


class NovaShellProvider(BaseProvider):
    def __init__(self, config):
        super(NovaShellProvider, self).__init__()
        self.config = config
        self.nova_shell_config = self.config.nova_shell
        novaclient_osenv_dict = {}
        empty_vars = {}
        if self.nova_shell_config is None:
            self.provider_log.warning("Empty config recieved in init, the"
                                      "client will use whatever OS ENV's are"
                                      "currently set for the environment")
        else:
            env_vars = dir(self.nova_shell_config)
            for env_var in env_vars:
                e_value = None
                '''
                @TODO: Having these magic strings here is bad.  We need
                       to define a constant that we put in front of ALL
                       env vars so we can have them all automagically
                       added.  Replace OS_ and NOVA with something like
                       CC_AUTOENV_ or something.
                '''
                if re.search('^OS_', env_var) or (re.search('^NOVA', env_var)):
                    e_value = getattr(self.nova_shell_config, str(env_var))
                else:
                    continue

                if e_value is None:
                    empty_vars[env_var] = e_value
                else:
                    novaclient_osenv_dict[env_var] = e_value

        #Log config vars = None
        for key, value in empty_vars.items():
            self.provider_log.warning('Not Configured: {0}={1}. Most '
                'likely it is not defined in the current config file.'
                .format(key, value))

        #Log config vars being sent to client
        for key, value in novaclient_osenv_dict.items():
            self.provider_log.debug('Found: {0}={1}'.format(key, value))

        #Init novaclient
        self.NovaShellClient = NovaShellClient(novaclient_osenv_dict)

    def select_random_image(self):
        '''
        @summary: Returns a random image
        @return: Valid image record
        @rtype: L{ImageDomainObject}
        '''
        self.provider_log.info("Selecting a RANDOM Image . . .")

        nova_response = self.NovaShellClient.image_list()
        if nova_response.IsEmpty == False and nova_response.IsError == False:
            random_image = random.randrange(0, len(nova_response.rows))
            image = ImageDomainObject(**nova_response.find_row('ID', random_image))
            self.provider_log.info("Selected RANDOM Image %s" % image)
        elif nova_response.IsError:
            self.provider_log.info("Image list is invalid, nova returned:\n%s" % nova_response)
        else:
            self.provider_log.info("No Image found.")

        return image

    def select_image(self, image_id):
        '''
        @summary: Returns a hardcoded image
        @return: Valid image record
        @rtype: L{ImageDomainObject}
        '''
        self.provider_log.info("Selecting a Image . . .")
        image = None
        nova_response = self.NovaShellClient.image_list()
        if nova_response.IsEmpty == False and nova_response.IsError == False:
            image = ImageDomainObject(**nova_response.find_row('ID', image_id))
            self.provider_log.info("Selected Image %s" % image)
        elif nova_response.IsError:
            self.provider_log.info("Image list is invalid, nova returned:\n%s" % nova_response)
        else:
            self.provider_log.info("No Image found.")

        return image

    def select_random_flavor(self):
        '''
        @summary: Returns a specific smoke test valid flavor
        @return: Valid flavor record
        @rtype: L{FlavorDomainObject}
        '''
        self.provider_log.info("Selecting RANOM Flavor . . .")
        nova_response = self.NovaShellClient.flavor_list()

        if nova_response.IsEmpty == False and nova_response.IsError == False:
            random_flavor = random.randrange(0, len(nova_response.rows))
            flavor = FlavorDomainObject(**nova_response.get_row(random_flavor))
            self.provider_log.info("Selected RANDOM Flavor %s" % flavor)
        elif nova_response.IsError:
            self.provider_log.info("Flavor list is invalid, nova returned:\n%s" % nova_response)
        else:
            self.provider_log.info("No Flavor found.")
        return flavor

    def select_flavor(self, flavor_id):
        '''
        @summary: Returns a specific smoke test valid flavor
        @return: Valid flavor record
        @rtype: L{FlavorDomainObject}
        '''
        flavor = None
        self.provider_log.info("Selecting a Flavor . . .")
        nova_response = self.NovaShellClient.flavor_list()

        if nova_response.IsEmpty is False and nova_response.IsError is False:
            flavor = FlavorDomainObject(**nova_response.find_row('ID', flavor_id))
            self.provider_log.info("Selected Flavor {0}".format(flavor))
        elif nova_response.IsError:
            self.provider_log.info(
                "Flavor list is invalid, nova returned:\n"
                "{0}".format(nova_response))
        else:
            self.provider_log.info("No Flavor found.")
        return flavor

    def create_random_server(self, server_name):
        '''
        @summary: Creates a server from a RANDOM Image and Flavor that are compatible.
        @return: Valid server on success, or None if boot_server returns a Nova Exception other than ERROR_MESSAGE
        '''
        ERROR_MESSAGE="ERROR: Instance type's memory is too small for requested image"
        nova_exception = "NOVA EXCEPTION"
        BAD_COMBO = True

        try:
            while BAD_COMBO:
                image = self.select_random_image()
                flavor = self.select_random_flavor()
                self.provider_log.info("Creating RANDOM Server Instance - %s with flavor: %s and image: %s" % (server_name, flavor.ID, image.ID))
                nova_response = self.NovaShellClient.boot_server(server_name, flavor.ID, image.ID)

                if nova_response.fields.count(nova_exception) == 1:
                    exception_message = nova_response.get_row(0)[nova_exception]
                    if ERROR_MESSAGE in exception_message:
                        self.provider_log.info(ERROR_MESSAGE + " Trying again.")
                    else:
                        self.provider_log.info(exception_message + " Returning None")
                        return None
                else:
                    BAD_COMBO = False

        except Exception, boot_exception:
            self.provider_log.info("Exception booting server_domain_object: %s: %s" % (server_name, boot_exception))

        return nova_response

    def create_active_server(self, server_name, flavor_id, image_id, timeout=700):
        '''
        @summary: Creates a server from an Image and Flavor
        @return: Valid server on success, or None if boot_server returns a Nova Exception other than ERROR_MESSAGE
        '''

        server_domain_object = None
        try:
            self.provider_log.info("Creating VALID Server Instance - %s with flavor: %s and image: %s" % (server_name, flavor_id, image_id))
            nova_response = self.NovaShellClient.boot_server(server_name, flavor_id, image_id)
        except Exception, boot_exception:
            self.provider_log.info("Exception booting server_domain_object: %s: %s" % (server_name, boot_exception))
            return None

        if nova_response.IsEmpty == False and nova_response.IsError == False:
            self.provider_log.info("Server %s created, waiting for server_domain_object to become active . . ." % server_name)
            admin_password = nova_response.find_row('Property', 'adminPass')['Value']
            (is_status_found, is_error, server_domain_object) = self.wait_for_server_status(server_name, NovaServerStatusTypes.ACTIVE, timeout, True)
            if is_status_found:
                self.provider_log.info("Server Instance: %s created and available." % server_domain_object)
                server_domain_object.admin_pass = admin_password
                return server_domain_object
            else:
                if is_error:
                    self.provider_log.info("Server %s was created but entered an error state before becoming active. Last Status was: %s" % (server_name, server_domain_object.Status))
                elif server_domain_object is not None:
                    self.provider_log.info("Server %s was created but timed-out before becoming active. Last Status was: %s" % (server_name, server_domain_object.Status))
                else:
                    self.provider_log.info("Server %s was created but never found in the system" % server_name)
        else:
            self.provider_log.info("Boot server_domain_object failed, nova returned:\n%s" % nova_response)
        return server_domain_object

    def create_server(self, server_name, timeout=600):
        '''
        @summary: Boot a new server, wait for it to return and report result
        @param server_name: server_name for the new server
        @type server_name: C{str}
        @param timeout: Wait time in seconds before time-out
        @type timeout: C{int}
        @return: Valid record on success
        @rtype: L{ServerDomainObject}
        '''

        server_domain_object = None
        nova_response = self.create_random_server(server_name)
        if nova_response.IsEmpty == False and nova_response.IsError == False:
            self.provider_log.info("Server %s created, waiting for server_domain_object to become active . . ." % server_name)
            (is_status_found, is_error, server_domain_object) = self.wait_for_server_status(server_name, NovaServerStatusTypes.ACTIVE, timeout, True)
            if is_status_found:
                self.provider_log.info("Server Instance: %s created and available." % server_domain_object)
                return server_domain_object
            else:
                if is_error:
                    self.provider_log.info("Server %s was created but entered an error state before becoming active. Last Status was: %s" % (server_name, server_domain_object.Status))
                elif server_domain_object is not None:
                    self.provider_log.info("Server %s was created but timed-out before becoming active. Last Status was: %s" % (server_name, server_domain_object.Status))
                else:
                    self.provider_log.info("Server %s was created but never found in the system" % server_name)
        else:
            self.provider_log.info("Boot server_domain_object failed, nova returned:\n%s" % nova_response)
        return server_domain_object

    def get_server(self, server_name=""):
        '''
        @summary: Returns the specified server
        @param server_name: Name of the server
        @type server_name: C{str}
        @return: Valid record on success
        @rtype: L{ServerDomainObject}
        '''
        server_domain_object = None
        if server_name != "":
            try:
                nova_response = self.NovaShellClient.list_server(server_name)
                if nova_response.IsEmpty == False and nova_response.IsError == False:
                    server_domain_object = ServerDomainObject(**nova_response.get_row(0))
                elif nova_response.IsError:
                    self.provider_log.info("Error retrieving server, nova returned:\n%s" % nova_response)
                else:
                    self.provider_log.info("Server Not Found.")
            except Exception, server_exception:
                self.provider_log.info("Exception searching for server: %s: %s" % (server_name, server_exception))
        return server_domain_object

    def delete_server(self, server_name, timeout=480):
        '''
        @summary: Delete a server, wait for it to delete and report result
        @param server_name: Display Name of the server to delete. (see 'nova server-list').
        @type server_name: C{str}
        @param timeout: Wait time in seconds before time-out
        @type timeout: C{int}
        @return: True if deleted and removed.
        @rtype: C{bool}
        '''
        was_deleted = False

        try:
            ''' Delete Server requires the ID of the server passed in, look it up first '''
            self.provider_log.info("Loading Server %s . . ." % server_name)
            server = self.get_server(server_name)
        except Exception, search_exception:
            server = None
            self.provider_log.info("Exception loading server: %s: %s" % (server_name, search_exception))

        if server:
            try:
                self.provider_log.info("Deleting Server %s . . ." % server_name)
                novaResponse = self.NovaShellClient.delete_server(server_name)
            except Exception, delete_exception:
                self.provider_log.info("Exception deleting server: %s from server: %s: %s" % (server_name, delete_exception))

            if novaResponse.IsEmpty == True and novaResponse.IsError == False:
                self.provider_log.info("Server %s deleted, waiting for server to be removed . . ." % server_name)
                (is_status_found, is_error, server) = self.wait_for_server_status(server_name, NovaServerStatusTypes.DELETING, timeout, True)
                if is_status_found:
                    ''' Status was found within timeout '''
                    ''' @todo: add back in the final check for deleted '''
                    was_deleted = True
                    self.provider_log.info("Server %s was deleted." % server_name)
                else:
                    if is_error:
                        self.provider_log.info("Server %s was deleted but entered an error state before being removed. Last Status was: %s" % (server_name, server.Status))
                    elif server is not None:
                        self.provider_log.info("Server %s was deleted but timed-out before being removed. Last Status was: %s" % (server_name, server.Status))
                    else:
                        '''
                        The server actually vanished before/during the wait for status call,
                        It's acceptable to assume that the delete was successful
                        '''
                        was_deleted = True
                        self.provider_log.info("Server %s was deleted." % server_name)
            else:
                self.provider_log.info("Delete server failed, nova returned:\n%s" % novaResponse)
        else:
            self.provider_log.info("Un-able to locate server: %s" % server_name)
        return was_deleted

    def wait_for_server_status(self, server_name, status, timeout=480, stop_on_error=False):
        '''
        @summary: Waits for a server to enter a specific status
        @param server_name: Name of the server
        @type server_name: C{str}
        @param staus: Server status to expect
        @type status: L{NovaServerStatusTypes}
        @param timeout: Wait time in seconds before time-out
        @type timeout: C{int}
        @param stop_on_error: Stops if server enters error status (Only if not waiting on error)
        @type stop_on_error: C{bool}
        @return: Tuple with True/False for status found, error found and the ServerDomainObject or None if server is not found
        @rtype: C{Tuple} [True/False, True/False, L{ServerDomainObject}]
        '''
        is_status_found = False
        is_error_found = False
        timedOut = time.time() + timeout
        server_domain_object = None

        ''' @todo: Make this wait process more generic and robust '''
        while time.time() < timedOut:
            try:
                server_domain_object = self.get_server(server_name)
                if server_domain_object is not None:
                    self.provider_log.debug("Waiting for Server %s Status %s, current Status is %s . . ."
                                                                % (server_name, status, server_domain_object.Status))
                    if server_domain_object.Status == status:
                        is_status_found = True
                        break
                    elif server_domain_object.Status == None:
                        server_domain_object = None
                        break
                    elif server_domain_object.Status == NovaServerStatusTypes.ERROR and stop_on_error == True:
                        is_error_found = True
                        break
                else:
                    break
                self.provider_log.info("Still waiting for status: %s, Current status: %s Time remaining until timeout: %d"
                                       % (status, server_domain_object.Status, timedOut - time.time()))
                time.sleep(3)
            except Exception, wait_exception:
                self.provider_log.info("Exception waiting for server %s: status %s: %s"
                                                                        % (server_name, status, wait_exception))
                break
        return is_status_found, is_error_found, server_domain_object

    def wait_for_volume_status(self, volume_name, status, timeout=480, stop_on_error=True):
        '''
        @summary: Waits for a server to enter a specific status
        @param volume_name: Name of the volume
        @type volume_name: C{str}
        @param staus: Volume status to expect
        @type status: L{NovaVolumeStatusTypes}
        @param timeout: Wait time in seconds before time-out
        @type timeout: C{int}
        @param stop_on_error: Stops if volume enters error status (Only if not waiting on error status type)
        @type stop_on_error: C{bool}
        @return: Tuple with True/False for status found, error found and the valid or empty record if volume is/is not found
        @rtype: C{Tuple} [True/False, True/False, server dictionary]
        '''
        isStatusFound = False
        isErrorFound = False
        timeout = time.time() + timeout
        curr_status = None

        ''' @todo: Make this wait process more generic and robust '''
        while time.time() < timeout:

            #Get current volume status
            try:
                curr_status = self.get_volume_status(volume_name)
            except Exception, wait_exception:
                self.provider_log.info("Exception waiting for volume %s: "\
                                       "status %s: %s" % (volume_name, status,
                                                          wait_exception))
                timeout = 0
                break

            self.provider_log.info("Waiting for volume %s Status %s, current "\
                                   " Status is %s . . ." % (volume_name,
                                                            status,
                                                            curr_status))

            #Check if current status is the one we're waiting for
            if curr_status == status:
                isStatusFound = True
                break
            elif ((curr_status == NovaVolumeStatusTypes.ERROR and
                        stop_on_error == True) or
                  (curr_status == NovaVolumeStatusTypes.ERROR_DELETING and
                        stop_on_error == True)):
                isErrorFound = True
                self.provider_log.error("Volume encountered an error status "\
                                       "while waiting.(stop_on_error==True)")
                break

            self.provider_log.info("Still waiting for status: %s, Current "\
                                  "status: %s Time remaining until timeout: %d"
                               % (status, curr_status, timeout - time.time()))
            time.sleep(3)

        return isStatusFound, isErrorFound, curr_status

    def validate_server(self, server_record):
        '''
        @summary: Validates that a server exists
        @param server_record: Server record used for validation
        @type server_record: c{dict}
        @todo: Find a better home for validators that are related to but don't belong directly to the Nova Client Proc
        @return: True if server is valid
        @rtype: C{bool}
        '''
        isValid = False

        '''
        This parsing is based on the table that is returned from the nova client. The example below
        is the current as of 05/07/2012:
        Networks: 'public=2001:4801:7808:0052:5f4a:d80e:ff00:002c,50.57.94.4;private=10.182.64.39'
        '''
        public_ipv4_address = None
        ''' @todo: Move the get server public IP to a better global class '''
        addr_strings = server_record["Networks"].split(";")
        for tmp in addr_strings:
            if re.search('public=', tmp):
                addresses = tmp.split(',')
                for address in addresses:
                    address = address.replace('public=','')
                    try:
                        sys.stdout.flush()
                        inet_aton(address)
                    except Exception:
                        sys.exc_clear()
                    else:
                        public_ipv4_address = address
                        break
        self.provider_log.debug("Public_ipv4_address: %s" % (str(public_ipv4_address)))

        try:
            '''
            @todo: REPLACE THE PING VALIDATOR WITH A REAL ONE
            Adjusted to do 10 100 ms pings, this seems to be the sweet spot for detection.
            '''
            isValid = True
        #            pingProc = subprocess.Popen("ping -w 10 %s" % public_ipv4_address,
        #                                        stdout=subprocess.PIPE,
        #                                        stderr=subprocess.STDOUT,
        #                                        shell=True)
        #            pingProc.wait()
        #            for line in pingProc.stdout.readlines():
        #                if "100% packet loss" in line:
        #                    isValid = False
        #                    break
        #                else:
        #                    isValid = True
        except Exception, validate_exception:
            self.provider_log.info("Exception validating server: %s: %s" % (server_record, validate_exception))
        return isValid

    def select_volume_type(self, volume_type_name=None):
        '''
        @summary: Returns a random valid volume type
        @return: Random valid volume type record
        @rtype: L{VolumeTypeDomainObject}
        '''
        volume_type_domain_object = None
        try:
            self.provider_log.info("Selecting Volume Type . . .")
            nova_response = self.NovaShellClient.volume_type_list()
            if nova_response.IsEmpty is False and \
                    nova_response.IsError is False:
                if self.nova_shell_config.environment_type == 'hacker-jack':
                    vtype = nova_response.find_row("Name", "vtype")
                    volume_type_domain_object = VolumeTypeDomainObject(**vtype)
                elif self.nova_shell_config.environment_type == 'huddle':
                    volume_type_domain_object = None
                    if volume_type_name is not None:
                        for i in range(2):
                            vtype = nova_response.get_row(i)
                            if vtype['Name'].lower() == volume_type_name.lower():
                                volume_type_domain_object = VolumeTypeDomainObject(
                                    **vtype)
                    else:
                        volume_type_domain_object = VolumeTypeDomainObject(
                            **nova_response.get_row(0))
                else:
                    self.provider_log.error(
                        "Not a usable environment type. Please specify whether"
                        " hacker-jack or huddle")

                self.provider_log.info(
                    "Volume type selected: {0} for Environment Type: "
                    "{1}".format(
                        volume_type_domain_object,
                        self.nova_shell_config.environment_type))
            elif nova_response.IsError:
                self.provider_log.info(
                    "Volume Type List is invalid, nova returned:\n{0}".format(
                        nova_response))
            else:
                self.provider_log.info("No Volume Types found.")
        except Exception as exception:
            self.provider_log.exception(exception)

        return volume_type_domain_object

    def create_volume(self, volume_name, volume_type, volume_size, timeout=480):
        '''
        @summary: Boot a new volume, wait for it to return and report result
        @param volume_name: Name for the new volume (Display Name)
        @type volume_name: C{str}
        @param volume_type: Volume Type ID, (see 'nova volume-type-list').
        @type volume_type: C{str}
        @param volume_size: Size of volume in GB
        @type volume_size: C{int}
        @param timeout: Wait time in seconds before time-out
        @type timeout: C{int}
        @return: Valid record on success
        @rtype: C{dict}
        '''
        new_volume = None
        try:
            self.provider_log.info("Creating Volume with Size %d . . ." % volume_size)
            nova_response = self.NovaShellClient.volume_create(volume_name, volume_type, volume_size)
        except Exception, create_exception:
            self.provider_log.info("Exception creating volume: %s: %s" % (volume_name, create_exception))

        if not nova_response.IsError:
            self.provider_log.info("Volume %s created, waiting for volume to become available . . ." % volume_name)
            isStatusFound, isErrorFound, lastStatus = self.wait_for_volume_status(volume_name, NovaVolumeStatusTypes.AVAILABLE, timeout, True)
            if isStatusFound:
                new_volume = self.get_volume(volume_name)
                self.provider_log.info("Volume %s created, waiting for volume to become available . . ." % volume_name)
            else:
                if isErrorFound:
                    self.provider_log.info("Volume %s was created but entered an error state before becoming active. Last Status was: %s" % (volume_name, lastStatus))
                elif lastStatus != "":
                    self.provider_log.info("Volume %s was created but timed-out before becoming active. Last Status was: %s" % (volume_name, lastStatus))
                else:
                    self.provider_log.info("Volume %s was created but never found in the system" % volume_name)
        else:
            self.provider_log.info("Create volume failed, nova returned:\n%s" % nova_response)
        return new_volume

    def get_volume_status(self, volume_name = ""):
        '''
        @summary: Returns the specified volume
        @param volume_name: Name of the volume
        @type volume_name: C{str}
        @return: Valid record on success
        @rtype: C{dict}
        '''
        return self._get_volume_property(volume_name, 'status')

    def _get_volume_property(self, volume_name, property_name):
        '''
        @summary: Returns the specified volume property
        @param volume_name: Name of the volume
        @type volume_name: C{str}
        @param property_name: Name of the volume property
        @type property_name: C{str}
        @return: Valid record on success
        @rtype: C{dict}
        '''
        property_value = ""
        novaResponse = None
        if volume_name != "":
            try:
                novaResponse = self.NovaShellClient.volume_show(volume_name)
                if novaResponse.IsEmpty == False and novaResponse.IsError == False:
                    volume_info = novaResponse.find_row("Property", property_name)
                    property_value = volume_info['Value']
                elif novaResponse.IsError:
                    self.provider_log.info("Error retrieving volume, nova returned:\n%s" % novaResponse)
                else:
                    self.provider_log.info("volume Not Found.")
            except Exception as volume_exception:
                self.provider_log.info("Exception searching for volume: %s: %s" % (volume_name, volume_exception))
                raise volume_exception

        return property_value

    def get_volume(self, volume_name):
        '''
        @summary: Returns the specified volume
        @param volume_name: Name of the volume
        @type volume_name: C{str}
        @return: Valid record on success
        @rtype: C{dict}
        '''
        volume = {}
        self.provider_log.info("Searching for Volume %s . . ." % volume_name)

        try:
            nova_response = self.NovaShellClient.volume_list()
            if nova_response.IsEmpty == False and nova_response.IsError == False:
                volume = nova_response.find_row("Display Name", volume_name)
            elif nova_response.IsError:
                self.provider_log.info("Error retrieving volume, nova returned:\n%s" % nova_response)
            else:
                self.provider_log.info("volume Not Found.")
        except Exception, volume_exception:
            self.provider_log.info("Exception searching for volume: %s: %s" % (volume_name, volume_exception))
        return volume

    def delete_volume(self, volume_name, timeout=480):
        '''
        @summary: Delete a volume, wait for it to delete and be removed and report result
        @param volume_name: Display Name of the volume to delete. (see 'nova volume-list').
        @type volume_name: C{str}
        @param timeout: Wait time in seconds before time-out
        @type timeout: C{int}
        @return: True if deleted and removed
        @rtype: C{bool}
        '''
        wasDeleted = False
        volume = {}
        time_waited = 0

        #Locate Volume
        try:
            ''' Delete Volume requires the ID of the volume passed in, look it up first '''
            self.provider_log.info("Searching for Volume %s . . ." % volume_name)
            volume = self.get_volume(volume_name)
        except Exception, search_exception:
            self.provider_log.info("Exception locating volume: %s: %s" % (volume_name, search_exception))
            return False

        if (volume is None) or (volume == {}):
            self.provider_log.info("Error locating volume: %s:" % volume_name)
            return False

        #Delete Volume
        try:
            self.provider_log.info("Deleting Volume %s . . ." % volume_name)
            novaResponse = self.NovaShellClient.volume_delete(volume["ID"])
            self.provider_log.debug(novaResponse)
        except Exception, delete_exception:
            self.provider_log.info("Exception deleting volume: %s: %s" % (volume_name, delete_exception))

        #Wait for the 'Deleting' Status at least for timeout seconds
        status = None
        while True:
            self.provider_log.info("Waiting for volume deleting status: %s" % (volume_name))
            try:
                status = self.get_volume_status(volume_name)
                if status == '':
                    status = 'GONE'
                    break
            except:
                pass

            if status == NovaVolumeStatusTypes.DELETING:
                ''' Volume is in deleting state, see if it finishes withing timeout'''
                continue

            elif status == None:
                status = 'NONE'
                break

            elif status is not None:
                time.sleep(10)
                time_waited += 10

            if time_waited >= timeout:
                self.provider_log.info("Timeout reached waiting for %s . . ." % volume_name)
                break


        #Check final volume status
        wasDeleted = False
        if status == NovaVolumeStatusTypes.DELETING:
            ''' Did not finish deleting before timeout '''
            self.provider_log.info("Volume %s is in DELETING state." % volume_name)

        elif (NovaVolumeStatusTypes.ERROR == status) or (status == NovaVolumeStatusTypes.ERROR_DELETING):
            ''' Volume ended up in either an ERROR or ERROR DELETING state'''
            self.provider_log.error("Volume did not delete, current status: %s" % str(status))

        elif status == 'GONE':
            ''' Volume disappeared and is presumed deleted'''
            self.provider_log.info("Volume is GONE and presumed DELETED")
            wasDeleted = True

        elif status == 'NONE':
            ''' Volume status didn't return for some reason and is presumed deleted'''
            self.provider_log.info("Volume status was not returned at some point and is presumed deleted")
            wasDeleted = True

        elif status == 'UNKNOWN_EXCEPTION':
            self.provider_log.error("An unexpected exception occurred, volume status is unknown")

        elif (status is None) or (status == {}):
            self.provider_log.error("Volume status was not found, and is unknown")

        return wasDeleted

    def attach_volume(
            self, server_name, volume_name, device_name, timeout=480):
        '''
        @summary: Attach a volume to a server, wait for it to attach and report result
        @param server_name: Name or ID of server. (see 'nova list').
        @type server_name: C{str}
        @param volume_name: Display Name of the volume to attach. (see 'nova volume-list').
        @type volume_name: C{str}
        @param device_name: Name of the attached device e.g. /dev/vdb.
        @type device_name: C{str}
        @param timeout: Wait time in seconds before time-out
        @type timeout: C{int}
        @return: Valid record on success
        @rtype: C{dict}
        '''
        attachedVolume = {}

        #Get and verify volume ID
        volume = None
        try:
            ''' Attach Volume requires the ID of the volume passed in,
                look it up first
            '''
            self.provider_log.info("Searching for Volume {0}".format(
                volume_name))
            volume = self.get_volume(volume_name)

        except Exception, search_exception:
            self.provider_log.error("Exception locating volume {0}: {1}".format(
                volume_name, search_exception))

        if volume is None or volume == {}:
            self.provider_log.error("Unable to locate volume: %s" %\
                                   (volume_name))
            return None

        #Send Nova attach command and verify response
        novaResponse = None
        try:
            novaResponse = self.NovaShellClient.volume_attach(
                server_name, volume["ID"], device_name)
        except Exception as e:
            self.provider_log.exception(e)
            self.provider_log.error(
                "Exception attaching volume '{0}' to server '{1}' as device "
                "{2}".format(volume_name, server_name, device_name))

        if novaResponse.IsError:
            self.provider_log.error(
                "Error attaching volume '{0}' to server '{1}' as device "
                "{2}".format(volume_name, server_name, device_name))
            return None

        #Wait for volume to finish attaching
        isStatusFound = None
        isErrorFound = None
        lastStatus = None
        try:
            isStatusFound, isErrorFound, lastStatus =\
                self.wait_for_volume_status(
                    volume_name, NovaVolumeStatusTypes.IN_USE, timeout, True)
        except Exception as e:
            self.provider_log.exception(e)
            self.provider_log.debug(
                "wait_for_vlume_status isStatusFound response: {0}".format(
                    isStatusFound))
            self.provider_log.debug(
                "wait_for_vlume_status isErrorFound response: {0}".format(
                    isErrorFound))
            self.provider_log.debug(
                "wait_for_vlume_status LastStatus: {0}".format(lastStatus))
            self.provider_log.info(
                "Exception while waiting for volume '{0}' to attach to server"
                " '{1}' as device '{2}'".format(
                    volume_name, server_name, device_name))
            return None

        self.provider_log.debug(
            "wait_for_vlume_status isStatusFound response: {0}".format(
                isStatusFound))
        self.provider_log.debug(
            "wait_for_vlume_status isErrorFound response: {0}".format(
                isErrorFound))
        self.provider_log.debug(
            "wait_for_vlume_status LastStatus: {0}".format(lastStatus))

        #See if volume wait returned an error state
        if isStatusFound is False or isErrorFound is True:
            self.provider_log.info(
                "Error occured while waiting for volume '{0}' to attach to "
                "server '{1}' as device '{2}'".format(
                    volume_name, server_name, device_name))

            self.provider_log.info("The last reported status was {0}".format(
                lastStatus))
            return None

        #Retrieve attached volume info
        attachedVolume = None
        try:
            self.provider_log.info("Searching for Volume {0}".format(
                volume_name))

            attachedVolume = self.get_volume(volume_name)

        except Exception, search_exception:
            self.provider_log.info(
                "Exception while attempting to locate attached volume: "
                "{0}: {1}".format(volume_name, str(search_exception)))

        if attachedVolume is None or volume == {}:
            self.provider_log.info("Unable to locate attached volume: {0}".
                                   format(volume_name))
            return None

        return attachedVolume

    def create_volume_from_snapshot(self, volume_name, volume_snapshot_name, timeout=480):
        '''
        @summary: Create a new volume from a snapshot, wait for it to return and report result
        @param volume_name: Name for the new volume (Display Name)
        @type volume_name: C{str}
        @param volume_snapshot_id: Volume Snapshot ID, (see 'nova volume-snapshot-list').
        @type volume_snapshot_id: C{str}
        @param volume_type: Volume Type ID, (see 'nova volume-type-list').
        @type volume_type: C{str}
        @param timeout: Wait time in seconds before time-out
        @type timeout: C{int}
        @return: Valid record on success
        @rtype: L{VolumeDomainObject}
        '''
        new_volume = None
        volume_type_domain_object = self.select_volume_type()
        if volume_type_domain_object == None:
            return None
        volume_snapshot_id = self.get_volume_snapshot_id(volume_snapshot_name)
        if volume_snapshot_id is None:
            self.provider_log.info("Unable to retrieve snapshot id!")
            return None
        try:
            self.provider_log.info("Creating Volume from snapshot %s " % volume_snapshot_id)
            novaResponse = self.NovaShellClient.volume_create(display_name = volume_name, volume_type = volume_type_domain_object.Name, volume_size = 1, snapshot_id = volume_snapshot_id)
        except Exception, create_exception:
            self.provider_log.info("Exception creating volume %s from snapshot %s of type %s: %s" % (volume_name, volume_snapshot_id, volume_type_domain_object.Name, create_exception))

        if not novaResponse.IsError:
            self.provider_log.info("Volume %s created, waiting for volume to become available . . ." % volume_name)
            isStatusFound, isErrorFound, lastStatus = self.wait_for_volume_status(volume_name, NovaVolumeStatusTypes.AVAILABLE, timeout, True)
            if isStatusFound:
                new_volume = self.get_volume(volume_name)
                self.provider_log.info("Volume %s created, waiting for volume to become available . . ." % volume_name)
            else:
                if isErrorFound:
                    self.provider_log.info("Volume %s was created but entered an error state before becoming active. Last Status was: %s" % (volume_name, lastStatus))
                elif "" != lastStatus:
                    self.provider_log.info("Volume %s was created but timed-out before becoming active. Last Status was: %s" % (volume_name, lastStatus))
                else:
                    self.provider_log.info("Volume %s was created but never found in the system" % volume_name)
        else:
            self.provider_log.info("Create volume failed, nova returned:\n%s" % novaResponse)
        return new_volume

    def delete_all_servers(self, server_name_pattern):
        '''
        @summary: Returns the specified server
        @param server_name_pattern: Pattern used to match server. (I.E. Apollo would delete all servers that contain the name Apollo)
        @type server_name_pattern: C{str}
        @return: Count of servers found and count of servers deleted.
        @rtype: C{tuple}(C{int}, C{int})
        '''
        foundCount = 0
        deletedCount = 0
        novaResponse = None
        try:
            novaResponse = self.NovaShellClient.list_server()
            if novaResponse.IsEmpty == False and novaResponse.IsError == False:
                self.provider_log.info("Searching for pattern %s" % server_name_pattern)
                for row in novaResponse.yield_rows():
                    if row["Name"].find(server_name_pattern) > -1:
                        self.provider_log.info("Found %s . . ." % row["Name"])
                        foundCount += 1
                        if self.delete_server(row["Name"], 10):
                            deletedCount += 1
            elif novaResponse.IsError:
                self.provider_log.info("Error retrieving server list, nova returned:\n%s" % novaResponse)
            else:
                self.provider_log.info("No Servers Found.")
        except Exception, server_exception:
            self.provider_log.info("Exception searching for server: %s: %s" % (server_name_pattern, server_exception))
        return foundCount, deletedCount

    def delete_all_volumes(self, volume_name_pattern):
        '''
        @summary: Returns the specified volume
        @param volume_name_pattern: Pattern used to match volume. (I.E. Apollo would delete all volumes that contain the name Apollo)
        @type volume_name_pattern: C{str}
        @return: Count of volumes found and count of volumes deleted.
        @rtype: C{tuple}(C{int}, C{int})
        '''
        foundCount = 0
        deletedCount = 0
        novaResponse = None
        try:
            novaResponse = self.NovaShellClient.volume_list()
            if novaResponse.IsEmpty == False and novaResponse.IsError == False:
                self.provider_log.info("Searching for pattern %s" % volume_name_pattern)
                for row in novaResponse.yield_rows():
                    if row["DisplayName"].find(volume_name_pattern) > -1:
                        self.provider_log.info("Found %s . . ." % row["DisplayName"])
                        foundCount += 1
                        if self.delete_volume(row["DisplayName"], 10):
                            deletedCount += 1
            elif novaResponse.IsError:
                self.provider_log.info("Error retrieving volume list, nova returned:\n%s" % novaResponse)
            else:
                self.provider_log.info("No Volumes Found.")
        except Exception, volume_exception:
            self.provider_log.info("Exception searching for volume: %s: %s" % (volume_name_pattern, volume_exception))
        return foundCount, deletedCount

    def detach_volume(self, server_name, volume_name, timeout=480):
        '''
        @summary: Detach a volume from a server, wait for it to detach and report result
        @param server_name: Name or ID of server. (see 'nova list').
        @type server_name: C{str}
        @param volume_name: Display Name of the volume to detach. (see 'nova volume-list').
        @type volume_name: C{str}
        @param timeout: Wait time in seconds before time-out
        @type timeout: C{int}
        @return: Valid record on success
        @rtype: C{dict}
        '''
        detachedVolume = {}

        try:
            ''' Detach Volume requires the ID of the volume passed in, look it up first '''
            self.provider_log.info("Searching for Volume %s . . ." % (volume_name))
            volume = self.get_volume(volume_name)
        except Exception, search_exception:
            self.provider_log.info("Exception locating volume: %s: %s" % (volume_name, search_exception))

        if volume and volume != {}:
            try:
                novaResponse = self.NovaShellClient.volume_detach(server_name, volume["ID"])
            except Exception, detach_exception:
                self.provider_log.info("Exception detaching volume: %s from server: %s: %s" % (volume_name, server_name, detach_exception))

            if novaResponse.IsEmpty == True and novaResponse.IsError == False:
                self.provider_log.info("Volume %s detached, waiting for volume to become available . . ." % volume_name)
                isStatusFound, isErrorFound, lastStatus  = self.wait_for_volume_status(volume_name, NovaVolumeStatusTypes.AVAILABLE, timeout, True)
                if isStatusFound:
                    ''' Status was found within timeout '''
                    detachedVolume = self.get_volume(volume_name)
                else:
                    if isErrorFound:
                        self.provider_log.info("Volume %s was detached but entered an error state before becoming in use. Last Status was: %s" % (volume_name, lastStatus))
                    elif lastStatus == NovaVolumeStatusTypes.AVAILABLE:
                        self.provider_log.info("Volume %s was detached but timed-out before becoming available. Last Status was: %s" % (volume_name, lastStatus))
                    else:
                        self.provider_log.info("Volume %s was detached but could not be found in the system" % volume_name)
            else:
                self.provider_log.info("Detach volume failed, nova returned:\n%s" % novaResponse)
        else:
            self.provider_log.info("Un-able to locate volume: %s" % volume_name)
        return detachedVolume

    def get_image_by_name(self, image_name):
        #Normalize both image names and compare them
        fixed_image_name = image_name.replace(" ", "").lower()
        image_list = self.get_image_list()
        for image_info_list in image_list:
            id_ = image_info_list[0]
            name = image_info_list[1].replace(" ", "").lower()
            status = image_info_list[2]
            if name == image_name or name == fixed_image_name:
                if status.lower() == 'active':
                    return id_
                else:
                    raise Exception("Requested image is not active")

        raise Exception("Requested image was not found")

    def get_image_list(self):
        '''
        @summary: Returns the list of all images
        @return: List of valid records on success
        @rtype: C{list} of C{dict}
        '''
        volumeList = []
        novaResponse = None
        try:
            novaResponse = self.NovaShellClient.image_list()
            if novaResponse.IsEmpty == False and novaResponse.IsError == False:
                '''
                Need to first check if this is a hacker-jack environment
                @todo: This REALLY needs to be a better choice of random flavor
                '''
                volumeList = novaResponse.rows
            elif novaResponse.IsError:
                self.provider_log.info("Image list is invalid, nova returned:\n%s" % novaResponse)
            else:
                self.provider_log.info("No Images found.")
        except Exception, image_exception:
            volumeList = []
            self.provider_log.info("Exception processing Image list: %s" % image_exception)
        return volumeList

    def get_flavor_list(self):
        '''
        @summary: Returns the list of all flavors
        @return: List of valid records on success
        @rtype: C{list} of C{dict}
        '''
        flavorList = []
        novaResponse = None
        try:
            novaResponse = self.NovaShellClient.flavor_list()
            if novaResponse.IsEmpty == False and novaResponse.IsError == False:
                '''
                Need to first check if this is a hacker-jack environment
                @todo: This REALLY needs to be a better choice of random flavor
                '''
                flavorList = novaResponse.rows
            elif novaResponse.IsError:
                self.provider_log.info("Flavor list is invalid, nova returned:\n%s" % novaResponse)
            else:
                self.provider_log.info("No Flavors found.")
        except Exception, image_exception:
            flavorList = []
            self.provider_log.info("Exception processing Flavor list: %s" % image_exception)
        return(flavorList)

    def get_volume_id(self, volume_name = ""):
        '''
        @summary: Returns the specified volume
        @param volume_name: Name of the volume
        @type volume_name: C{str}
        @return: Valid record on success
        @rtype: C{dict}
        '''
        return self._get_volume_property(volume_name, 'id')

    def get_volume_type(self, volume_name = ""):
        '''
        @summary: Returns the specified volume
        @param volume_name: Name of the volume
        @type volume_name: C{str}
        @return: Valid record on success
        @rtype: C{dict}
        '''
        return self._get_volume_property(volume_name, 'volume_type')

    def get_volume_snapshot(self, snapshot_name = ""):
        '''
        @summary: Returns the specified volume snapshot
        @param snapshot_name: Name of the volume snapshot
        @type snapshot_name: C{str}
        @return: Valid record on success
        @rtype: C{dict}
        '''
        volume_snapshot = {}
        novaResponse = None
        if snapshot_name:
            try:
                novaResponse = self.NovaShellClient.volume_snapshot_list()
                if novaResponse.IsEmpty == False and novaResponse.IsError == False:
                    volume_snapshot = novaResponse.find_row("Display Name", snapshot_name)
                elif novaResponse.IsError:
                    self.provider_log.info("Error retrieving volume snapshot, nova returned:\n%s" % novaResponse)
                else:
                    self.provider_log.info("Snapshot %s Not Found." % snapshot_name)
            except Exception, volume_exception:
                volume_snapshot = {}
                self.provider_log.info("Exception searching for snapshot: %s: %s" % (snapshot_name, volume_exception))

        return(volume_snapshot)

    def get_volume_snapshot_info(self, snapshot_id):
        '''
        @summary: Returns the specified volume snapshot
        @param snapshot_id: Name of the volume snapshot
        @type snapshot_id: C{str}
        @return: Valid record on success
        @rtype: C{dict}
        '''
        volume_snapshot_info = {}
        novaResponse = None
        try:
            novaResponse = self.NovaShellClient.volume_snapshot_show(snapshot_id)
            if novaResponse.IsEmpty == False and novaResponse.IsError == False:
                return novaResponse
            elif novaResponse.IsError:
                self.provider_log.info("Error retrieving volume snapshot info, nova returned:\n%s" % novaResponse)
                return None
            else:
                self.provider_log.info("volume snapshot Not Found.")
        except Exception, snapshot_info_exception:
            self.provider_log.info("Exception getting info for snapshot %s: %s" % (snapshot_id, snapshot_info_exception))

        return novaResponse

    def get_volume_snapshot_id(self, snapshot_name):
        novaResponse = self.get_volume_snapshot_info(snapshot_name)
        if novaResponse is None:
            return None
        r = novaResponse.find_row('Property', 'id')
        return r['Value']

    def create_volume_snapshot(self, volume_name, display_name=None,
                               force_create=False, display_description=None, timeout=300):
        '''
        @summary: Create a volume snapshot
        @param volume_id: ID of the volume to create a snapshot of.
        @type volume_id: C{str}
        @param force_create: Force volume snapshot create.
        @type force_create: C{bool}
        @param display_name: Display name of new volume snapshot.
        @type display_name: C{str}
        @param display_description: Display description of new volume snapshot.
        @type display_description: C{str}
        @rtype: C{dict}
        '''
        new_volume_snapshot = {}
        volume = {}
        self.provider_log.info("Creating Snapshot of Volume %s named %s" % (volume_name, display_name))
        try:
            volume = self.get_volume(volume_name)
        except Exception, search_exception:
            self.provider_log.info("Exception locating volume: %s: %s" % (volume_name, str(search_exception)))

        if volume:
            try:
                nova_response = self.NovaShellClient.volume_snapshot_create(volume["ID"], force_create, display_name, display_description)
            except Exception, volume_snapshot_create_exception:
                self.provider_log.info("Exception creating snapshot of \
                volume %s where force = %s, snapshot_name = %s and \
                snapshot_description = %s: %s" % (str(volume_name), str(force_create),
                                                  str(display_name), str(display_description), volume_snapshot_create_exception))

            snapshot_name = display_name
            if not nova_response.IsError:
                self.provider_log.info("Snapshot %s created, waiting for volume to become available . . ." % snapshot_name)
                (is_status_found, is_error_found, volume_snapshot) = self.wait_for_volume_snapshot_status(snapshot_name, NovaVolumeSnapshotStatusTypes.AVAILABLE, timeout, True)
                if is_status_found:
                    new_volume_snapshot = volume_snapshot
                else:
                    if is_error_found:
                        self.provider_log.info("Volume Snapshot %s was created but entered an error state before becoming active. Last Status was: %s" % (snapshot_name, volume_snapshot["Status"]))
                    elif volume_snapshot != {}:
                        self.provider_log.info("Volume Snapshot %s was created but timed-out before becoming active. Last Status was: %s" % (snapshot_name, volume_snapshot["Status"]))
                    else:
                        self.provider_log.info("Volume Snapshot %s was created but never found in the system" % snapshot_name)
            else:
                self.provider_log.info("Create volume snapshot failed, nova returned:\n%s" % nova_response)
        else:
            self.provider_log.info("Un-able to locate volume: %s" % volume_name)
        return new_volume_snapshot

    def delete_volume_snapshot(self, snapshot_name, timeout=480):
        '''
        @summary: Delete specific snapshot
        @param snapshot_name: Name of the snapshot
        @type snapshot_name: C{str}
        @param timeout: Wait time in seconds before time-out
        @type timeout: C{int}
        @return: True on success, False on failure
        @rtype: C{bool}
        '''
        wasDeleted = False
        novaResponse = None
        try:
            ''' Delete Snapshot requires the ID of the snapshot passed in, look it up first '''
            self.provider_log.info("Searching for Snapshot %s . . ." % (snapshot_name))
            volume_snapshot = self.get_volume_snapshot(snapshot_name)
        except Exception, search_exception:
            self.provider_log.info("Exception locating snapshot: %s: %s" % (snapshot_name, search_exception))

        if volume_snapshot:
            self.provider_log.info("Deleting snapshot %s"%str(snapshot_name))
            try:
                novaResponse = self.NovaShellClient.volume_snapshot_delete(volume_snapshot["ID"])
            except Exception, delete_exception:
                self.provider_log.info("Exception deleting snapshot: %s: %s" % (snapshot_name, delete_exception))

            if not novaResponse.IsError:
                self.provider_log.info("Snapshot %s deleted, waiting for snapshot to be removed . . ." % snapshot_name)
                waitResult = self.wait_for_volume_snapshot_status(snapshot_name, NovaVolumeStatusTypes.DELETING, timeout, True)
                if waitResult[0]:
                    ''' Status was found within timeout '''
                    ''' @todo: add back in the final check for deleted '''
                    wasDeleted = self.wait_for_volume_snapshot_delete(snapshot_name)
                    if wasDeleted:
                        return wasDeleted
                else:
                    if waitResult[1]:
                        self.provider_log.info("Snapshot %s was deleted but entered an error state before being removed. Last Status was: %s" % (snapshot_name, waitResult[2]["Status"]))
                    elif waitResult[2] != {}:
                        self.provider_log.info("Snapshot %s was deleted but timed-out before being removed. Last Status was: %s" % (snapshot_name, waitResult[2]["Status"]))
                    else:
                        '''
                        The snapshot actually vanished before/during the wait for status call,
                        It's acceptable to assume that the delete was successful
                        '''
                        wasDeleted = True
                        self.provider_log.info("Volume Snapshot %s vanished before/during the wait for status call, and was assumed deleted." % snapshot_name)
            else:
                self.provider_log.info("Delete volume snapshot failed, nova returned:\n%s" % novaResponse)
        else:
            self.provider_log.info("Un-able to locate snapshot: %s" % snapshot_name)
        return wasDeleted

    def delete_volume_snapshots(self, volume_id):
        '''
        @summary: Delete all snapshots for a given volume
        @param volume_id: Name of the volume
        @type volume_id: C{str}
        @return: True on success, False on failure
        @rtype: C{bool}
        '''
        volume_snapshots = self.get_volume_snapshot_list(volume_id)
        return_response = True

        for snapshot in volume_snapshots:
            if snapshot['VolumeID'] == volume_id:
                return_response = return_response and self.delete_volume_snapshot(snapshot['ID'])

        return return_response

    def get_volume_snapshot_list(self, volume_id = None):
        '''
        @summary: Returns list of all snapshots for specifified volume, or just all snapshots if volume_id is None
        @param snapshot_id: Name of the volume snapshot
        @type snapshot_id: C{str}
        @return: Valid record(s) on success
        @rtype: C{list}
        '''
        novaResponse = None
        volume_snapshots = []

        try:
            novaResponse = self.NovaShellClient.volume_snapshot_list()
        except Exception, volume_snapshot_exception:
            volume_snapshot = {}
            self.provider_log.info("Exception searching for snapshot for volume %s: %s" % (volume_id, volume_snapshot_exception))

        for row in novaResponse.yield_rows():
            volume_snapshots.append(row)

        if volume_id is None:
            return volume_snapshots
        else:
            relevant_snapshots = []
            for snapshot in volume_snapshots:
                if snapshot['VolumeID'] == volume_id:
                    relevant_snapshots.append(snapshot)
            return relevant_snapshots

    def wait_for_volume_snapshot_status(self, snapshot_name, status, timeout=480, stop_on_error=False):
        '''
        @summary: Waits for a volume snapshot to enter given status
        @param volume_id id of the volume
        @type volume_id: C{str}
        @param snapshot_display_name snapshot display name
        @type snapshot_display_name: C{str}
        '''
        isStatusFound = False
        isErrorFound = False
        timedOut = time.time() + timeout
        volume_snapshot = {}

        ''' @todo: Make this wait process more generic and robust '''
        while time.time() < timedOut:
            try:
                volume_snapshot = self.get_volume_snapshot(snapshot_name)
                if volume_snapshot != {}:
                    self.provider_log.debug("Waiting for volume snapshot %s Status %s, current Status is %s . . ." % (snapshot_name, status, volume_snapshot["Status"]))
                    if volume_snapshot["Status"] == status:
                        isStatusFound = True
                        break
                    elif ((volume_snapshot["Status"] == NovaVolumeSnapshotStatusTypes.ERROR and stop_on_error == True) or
                          (volume_snapshot["Status"] == NovaVolumeSnapshotStatusTypes.ERROR_DELETING and stop_on_error == True)):
                        isErrorFound = True
                        break
                else:
                    break
                time.sleep(3)
            except Exception, wait_exception:
                self.provider_log.info("Exception waiting for volume snapshot %s: status %s: %s" % (snapshot_name, status, wait_exception))
                break

        return isStatusFound, isErrorFound, volume_snapshot

    def wait_for_volume_snapshot_delete(self, snapshot_name, timeout=480):
        gone = False
        time_waited = 0
        while not gone:
            try:
                snapshot = self.get_volume_snapshot(snapshot_name)
                if snapshot == {}:
                    self.provider_log.info('Unable to locate snapshot. It is presumed DELETED.')
                    gone = True
                else:
                    time.sleep(10)
                    time_waited += 10
            except:
                self.provider_log.info('Unable to locate snapshot. It is presumed DELETED.')
                gone = True

            if time_waited >= timeout:
                return gone

        return gone

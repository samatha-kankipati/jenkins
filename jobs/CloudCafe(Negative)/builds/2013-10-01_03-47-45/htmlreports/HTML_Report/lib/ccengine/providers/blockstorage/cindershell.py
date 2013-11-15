'''
@summary: Specifically provides access to Compute (nova) Clients/Helpers
@note: Should be the primary interface to a test case or external tool.
@attention: This is a port of the old provider in the compute module. When the old
smoke test is phased out, this should be moved or renamed appropriately.
@copyright: Copyright (c) 2012 Rackspace US, Inc.
'''
#from _socket import inet_aton
import random
import re
import time
import sys

from ccengine.providers.base_provider import BaseProvider
from ccengine.clients.blockstorage.cindershell import CinderShellClient
from ccengine.domain.compute.novashell import VolumeTypeDomainObject as  _VolumeTypeDomainObject
from ccengine.domain.types import NovaVolumeStatusTypes, NovaVolumeSnapshotStatusTypes


class CinderShellProvider(BaseProvider):
    def __init__(self, config):
        super(CinderShellProvider, self).__init__()
        self.config = config
        self.CinderShellClient = CinderShellClient(config)

        self.min_volume_size = int(self.config.cinder_shell.min_volume_size)
        self.max_volume_size = int(self.config.cinder_shell.max_volume_size)
        self.default_wait_period = 20
        self.default_volume_create_timeout = 600
        self.default_snapshot_create_timeout = max(self.min_volume_size * 18, self.default_volume_create_timeout)

    def wait_for_volume_status(self, volume_name, status, timeout=None, stop_on_error=True):
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
        timeout = timeout or self.default_volume_create_timeout
        isStatusFound = False
        isErrorFound = False
        timedOut = time.time() + timeout
        curr_status = None

        ''' @todo: Make this wait process more generic and robust '''
        while time.time() < timedOut:
            try:
                curr_status = self.get_volume_status(volume_name)
            except Exception, wait_exception:
                self.provider_log.info("Exception waiting for volume %s: status %s: %s" % (volume_name, status, wait_exception))
                timedOut = 0
                break

            self.provider_log.debug("Waiting for volume %s Status %s, current Status is %s . . ." % (volume_name, status, curr_status))
            if curr_status == status:
                isStatusFound = True
                break
            elif ((curr_status == NovaVolumeStatusTypes.ERROR and stop_on_error == True) or
                  (curr_status == NovaVolumeStatusTypes.ERROR_DELETING and stop_on_error == True)):
                isErrorFound = True
                break
            time.sleep(self.default_wait_period)

        return isStatusFound, isErrorFound, curr_status

    def select_volume_type(self):
        '''
        @summary: Returns a random valid volume type
        @return: Random valid volume type record
        @rtype: L{VolumeTypeDomainObject}
        '''
        volume_type_domain_object = None
        try:
            self.provider_log.info("Selecting Volume Type . . .")
            nova_response = self.CinderShellClient.volume_type_list()
            if nova_response.IsEmpty is False and nova_response.IsError is False:
                if self.config.cinder_shell.environment_type == 'hacker-jack':
                    vtype = nova_response.find_row("Name", "vtype")
                    volume_type_domain_object = _VolumeTypeDomainObject(**vtype)
                elif self.config.cinder_shell.environment_type == 'huddle':
                    volume_type_domain_object = _VolumeTypeDomainObject(**nova_response.get_row(0))
                else:
                    self.provider_log.error("Not a usable environment type. Please specify whether hacker-jack or huddle")
                self.provider_log.info("Volume type selected: %s for Environment Type: %s"
                                                    % (volume_type_domain_object, self.config.cinder_shell.environment_type))
            elif nova_response.IsError:
                self.provider_log.info("Volume Type List is invalid, nova returned:\n%s" % nova_response)
            else:
                self.provider_log.info("No Volume Types found.")
        except Exception, parse_exception:
            self.provider_log.info("Exception parsing Volume Type list: %s" % parse_exception)

        return volume_type_domain_object

    def create_volume(self, volume_name, volume_type, volume_size, timeout=None):
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
        timeout = timeout or self.default_volume_create_timeout
        new_volume = None
        try:
            self.provider_log.info("Creating Volume with Size %d . . ." % volume_size)
            nova_response = self.CinderShellClient.volume_create(volume_name, volume_type, volume_size)
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

    def get_volume_status(self, volume_name=""):
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
                novaResponse = self.CinderShellClient.volume_show(volume_name)
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
            nova_response = self.CinderShellClient.volume_list()
            if nova_response.IsEmpty == False and nova_response.IsError == False:
                volume = nova_response.find_row("Display Name", volume_name)
            elif nova_response.IsError:
                self.provider_log.info("Error retrieving volume, nova returned:\n%s" % nova_response)
            else:
                self.provider_log.info("volume Not Found.")
        except Exception, volume_exception:
            self.provider_log.info("Exception searching for volume: %s: %s" % (volume_name, volume_exception))
        return volume

    def delete_volume(self, volume_name, timeout=None):
        '''
        @summary: Delete a volume, wait for it to delete and be removed and report result
        @param volume_name: Display Name of the volume to delete. (see 'nova volume-list').
        @type volume_name: C{str}
        @param timeout: Wait time in seconds before time-out
        @type timeout: C{int}
        @return: True if deleted and removed
        @rtype: C{bool}
        '''
        timeout = timeout or self.default_volume_create_timeout
        wasDeleted = False
        volume = {}

        end = time.time() + timeout
        while time.time() < end:
            try:
                self.provider_log.info("Searching for Volume {0} . . .".format(
                    volume_name))
                volume = self.get_volume(volume_name)
            except Exception, search_exception:
                self.provider_log.info(
                    "Exception locating volume: {0}: {1}".format(
                        volume_name, search_exception))

            if (volume is None) or (volume == {}):
                self.provider_log.info(
                    "Volume may have been deleted before delete request was"
                    " made.  Either way, it was not found and is presumed GONE"
                    .format(volume_name))
                return True
            else:
                break
        else:
            self.provider_log.info(
                "Volume info retrieval timed out before getting to the delete")
            return False

        while time.time() < end:
            #Delete Volume
            delete_exception = None
            try:
                self.provider_log.info("Deleting Volume {0} . . .".format(
                    volume_name))
                self.CinderShellClient.volume_delete(volume["ID"])
                break
            except Exception, delete_exception:
                self.provider_log.info(
                    "Exception deleting volume: {0}: {1}".format(
                        volume_name, delete_exception))

            return False
        else:
            self.provider_log.info("Volume delete request timed out")
            return False

        #Wait for the 'Deleting' Status at least, continue where last timeout
        #loop left off
        status = None
        while time.time() < end:
            try:
                status = self.get_volume_status(volume_name)
                if status == '':
                    status = 'GONE'
                    break
            except Exception as e:
                status = 'UNKNOWN_EXCEPTION'
                self.provider_log.info(
                    "Exception occured while polling volume status")
                self.provider_log.exception(e)
                break

            if status == NovaVolumeStatusTypes.DELETING:
                #See if volume finishes before timeout
                continue

            #Wait 10 seconds before poling the API again.
            #TODO: Make this configurable like the volumes_api is
            time.sleep(10)
        else:
            self.provider_log.info("Timeout reached before verifying if volume was deleted")
            return False

        #Check final volume status
        wasDeleted = False
        if status == NovaVolumeStatusTypes.DELETING:
            #Did not finish deleting before timeout
            self.provider_log.info("Volume %s is in DELETING state." % volume_name)

        elif (status == NovaVolumeStatusTypes.ERROR or
              status == NovaVolumeStatusTypes.ERROR_DELETING):
            #Volume ended up in either an ERROR or ERROR DELETING state
            self.provider_log.error(
                "Volume did not delete, current status is {0}".format(status))

        elif status == 'GONE':
            #Volume dissapeared and is presumed deleted
            self.provider_log.info("Volume is GONE and presumed DELETED")
            wasDeleted = True

        elif status == 'UNKNOWN_EXCEPTION':
            self.provider_log.error(
                "An exception occurred, volume status is unknown")

        elif (status is None) or (status == {}):
            self.provider_log.error(
                "Volume status was not found, and is unknown")

        return wasDeleted

    def create_volume_from_snapshot(self, volume_name, volume_snapshot_name, timeout=None):
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
        timeout = timeout or self.default_snapshot_create_timeout
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
            novaResponse = self.CinderShellClient.volume_create(display_name = volume_name, volume_type = volume_type_domain_object.Name, volume_size = 1, snapshot_id = volume_snapshot_id)
        except Exception, create_exception:
            self.provider_log.info("Exception creating volume %s from snapshot %s of type %s: %s" % (volume_name, volume_snapshot_id, volume_type_domain_object, create_exception))

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
            novaResponse = self.CinderShellClient.volume_list()
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

    def get_volume_id(self, volume_name=""):
        '''
        @summary: Returns the specified volume
        @param volume_name: Name of the volume
        @type volume_name: C{str}
        @return: Valid record on success
        @rtype: C{dict}
        '''
        return self._get_volume_property(volume_name, 'id')

    def get_volume_type(self, volume_name=""):
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
                novaResponse = self.CinderShellClient.volume_snapshot_list()
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
        novaResponse = None
        try:
            novaResponse = self.CinderShellClient.volume_snapshot_show(snapshot_id)
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
                               force_create=False, display_description=None, timeout=None):
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
        @param timeout: Total seconds to wait for volume_snapshot to create.
        @type timeout: C{int}
        @rtype: C{dict}
        '''
        timeout = timeout or self.default_snapshot_create_timeout
        new_volume_snapshot = {}
        volume = {}
        self.provider_log.info("Creating Snapshot of Volume %s named %s" % (volume_name, display_name))
        try:
            volume = self.get_volume(volume_name)
        except Exception, search_exception:
            self.provider_log.info("Exception locating volume: %s: %s" % (volume_name, str(search_exception)))

        if volume:
            try:
                nova_response = self.CinderShellClient.volume_snapshot_create(volume["ID"], force_create, display_name, display_description)
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

    def delete_volume_snapshot(self, snapshot_name, timeout=None):
        '''
        @summary: Delete specific snapshot
        @param snapshot_name: Name of the snapshot
        @type snapshot_name: C{str}
        @param timeout: Wait time in seconds before time-out
        @type timeout: C{int}
        @return: True on success, False on failure
        @rtype: C{bool}
        '''
        timeout = timeout or self.default_snapshot_create_timeout
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
                novaResponse = self.CinderShellClient.volume_snapshot_delete(volume_snapshot["ID"])
            except Exception, delete_exception:
                self.provider_log.info("Exception deleting snapshot: %s: %s" % (snapshot_name, delete_exception))

            if not novaResponse.IsError:
                self.provider_log.info("Snapshot %s deleted, waiting for snapshot to be removed . . ." % snapshot_name)
                waitResult = self.wait_for_volume_snapshot_status(snapshot_name, NovaVolumeStatusTypes.DELETING, timeout, True)
                if waitResult[0]:
                    ''' Status was found within timeout '''
                    wasDeleted = self.wait_for_volume_snapshot_delete(snapshot_name)
                    self.provider_log.info("Snapshot %s was deleted." % snapshot_name)
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
            novaResponse = self.CinderShellClient.volume_snapshot_list()
        except Exception, volume_snapshot_exception:
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

    def wait_for_volume_snapshot_status(self, snapshot_name, status, timeout=None, stop_on_error=False):
        '''
        @summary: Waits for a volume snapshot to enter given status
        @param volume_id id of the volume
        @type volume_id: C{str}
        @param snapshot_display_name snapshot display name
        @type snapshot_display_name: C{str}
        '''
        timeout = timeout or self.default_snapshot_create_timeout
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
                time.sleep(self.default_wait_period)
            except Exception, wait_exception:
                self.provider_log.info("Exception waiting for volume snapshot %s: status %s: %s" % (snapshot_name, status, wait_exception))
                break

        return isStatusFound, isErrorFound, volume_snapshot

    def wait_for_volume_snapshot_delete(self, snapshot_name, timeout=None):
        '''
        @summary: Waits for a volume snapshot to enter given status
        @param volume_id id of the volume
        @type volume_id: C{str}
        @param snapshot_display_name snapshot display name
        @type snapshot_display_name: C{str}
        '''
        self.provider_log.info('Waiting for snapshot to be deleted')
        timeout = timeout or self.default_snapshot_create_timeout
        time_waited = 0
        wasDeleted = False

        while time_waited <= timeout:
            try:
                self.provider_log('Looking for volume snapshot')
                volume_snapshot = self.get_volume_snapshot(snapshot_name)
                self.provider_log.info('volume snapshot still there, waiting')
                time.sleep(10)
                time_waited += 10
            except:
                self.provider_log.info('Unable to find volume snapshot, presumed GONE and DELETED')
                wasDeleted = True

            if wasDeleted is True:
                return wasDeleted

            if time_waited <= timeout:
                self.provider_log.info('timed out waiting for snapshot to delete')

        return wasDeleted

'''
@summary: Provider Module for the Compute Volume API
@note: Should be the primary interface to a test case or external tool.
@copyright: Copyright (c) 2012 Rackspace US, Inc.
'''
import time
import re

from ccengine.clients.blockstorage.volumes_api import VolumesAPIClient
from ccengine.providers.identity.v2_0.identity_api import IdentityAPIProvider
from ccengine.providers.base_provider import BaseProvider, ProviderActionResult


class VolumesAPIProvider(BaseProvider):
    '''Provides helper methods for Volumes API functionality
    @ivar config: Configuration passed into constructor.
    @type config: L{MasterConfigProvider}
    @ivar volumes_client: Instance of Client to make calls to Volumes API
    @type volumes_client: L{VolumesAPIClient}
    '''

    def __init__(self, config):
        super(VolumesAPIProvider, self).__init__()
        self.config = config
        self.min_volume_size = int(self.config.volumes_api.min_volume_size)
        self.max_volume_size = int(self.config.volumes_api.max_volume_size)

        self.default_wait_period = int(
            self.config.volumes_api.default_wait_interval)
        self.default_max_waits = int(
            self.config.volumes_api.default_max_waits)
        self.default_timeout = int(
            self.default_wait_period) * int(self.default_max_waits)
        self.snapshot_create_wait = max((self.min_volume_size * 30), 500)

        #Get identity info
        self.identity_provider = IdentityAPIProvider(self.config)
        auth_response = self.identity_provider.authenticate()
        self.auth_data = auth_response.entity

        #Get Auth Token
        self.auth_token = self.auth_data.token.id

        #Set up services
        blockstorage_service = self.auth_data.serviceCatalog.get_service(
            self.config.volumes_api.identity_service_name)

        #Set up regions
        self.blockstorage_region = self.config.volumes_api.region

        #Get public URL
        self.blockstorage_public_url = blockstorage_service.\
            get_endpoint(self.blockstorage_region).publicURL

        #Get tenant id
        self.tenant_id = blockstorage_service.\
            get_endpoint(self.blockstorage_region).tenantId

        #setup client
        self.volumes_client = VolumesAPIClient(
            self.blockstorage_public_url,
            self.auth_token,
            self.tenant_id,
            self.config.misc.serializer,
            self.config.misc.deserializer)

    def get_type_name_by_id(self, volume_type_id):
        r = self.volumes_client.list_all_volume_types()
        if r.ok:
            vtypes = r.entity
            for t in vtypes:
                name = getattr(t, 'name')
                tid = getattr(t, 'id')
                if str(volume_type_id).lower() == str(name).lower():
                    return name
                if str(volume_type_id).lower() in str(tid).lower():
                    return name

    def get_type_id_by_name(self, volume_type_name):
        r = self.volumes_client.list_all_volume_types()
        if r.ok:
            vtypes = r.entity
            for t in vtypes:
                name = getattr(t, 'name')
                tid = getattr(t, 'id')
                if str(volume_type_name).lower() in str(name).lower():
                    return u'%s' % tid

    def get_list_of_snapshots_for_volume(self, volume_id):
        provider_action_response = ProviderActionResult()
        volume_snapshots = []

        resp = self.volumes_client.list_all_snapshots()
        provider_action_response.response = resp
        provider_action_response.ok = resp.ok
        snapshots = resp.entity
        if (snapshots is None) or (not resp.ok):
            return provider_action_response

        if type(snapshots)==type([]):
            for snapshot in snapshots:
                if str(snapshot.id).lower() == str(volume_id).lower():
                    volume_snapshots.append(snapshot)
        else:
            volume_snapshots.append(snapshots)

        provider_action_response.entity = volume_snapshots
        return provider_action_response

    def find_volumes_by_name(self, regex_volume_display_name, strict=False):
        '''
        @summary: This will return a list of all volumes who's display_name is
                  matched by the supplied regular expression.

        If you just want to do a string string==display_name search,
        set strict=True.
        Note: Volume names are not guaranteed to be unique.
        Returns a list of volume objects
        '''
        r = self.volumes_client.list_all_volumes()
        volume_list = r.entity if r.ok else []

        ret_list = []
        search_pattern = re.compile(str(regex_volume_display_name))
        for v in volume_list:
            if strict:
                if regex_volume_display_name == v.display_name:
                    ret_list.append(v)
            elif search_pattern.search(str(v.display_name)):
                ret_list.append(v)

        return ret_list

    def create_available_volume(
            self, display_name, size, volume_type, display_description=None,
            metadata=None, availability_zone=None, timeout=None,
            wait_period=None):

        '''Creates a volume and waits for it to reach 'available' status.
        Default timeout and wait_period are set by user configs.
        '''

        timeout = timeout or self.default_timeout
        wait_period = wait_period or self.default_wait_period
        provider_response = ProviderActionResult()
        ready_status = 'available'
        metadata = metadata or {}

        #Create Volume
        self.provider_log.info(
            "Creating Volume and making sure it's available")
        vol_create_resp = self.volumes_client.create_volume(
            display_name=display_name, size=size,
            volume_type=volume_type,
            display_description=display_description,
            metadata=metadata,
            availability_zone=availability_zone)

        if not vol_create_resp.ok:
            self.provider_log.info(
                "Error creating volume. Unable to create available volume")
            provider_response.ok = False
            return provider_response

        volume = vol_create_resp.entity
        provider_response.entity = volume

        #Wait for ready status
        wait_for_vol_status_resp = self.wait_for_volume_status(
            volume.id, ready_status, timeout, wait_period)
        wait_for_vol_status_resp.entity = volume

        #Returns the most info by smushing together the status from the wait
        #and the info from the create.  We don't care here because it's in the
        #provider.
        return wait_for_vol_status_resp

    def create_available_snapshot(
            self, volume_id, snapshot_display_name=None,
            snapshot_display_description=None, force_create='False',
            timeout=None, wait_period=None):
        '''Creates a volume and waits for it to reach 'available' status.
        Default timeout and wait_period are set by user configs.
        '''

        timeout = timeout or self.snapshot_create_wait
        wait_period = wait_period or self.default_wait_period
        provider_response = ProviderActionResult()
        ready_status = 'available'

        #Create Volume
        snap_create_resp = self.volumes_client.create_snapshot(
            volume_id, snapshot_display_name, snapshot_display_description,
            force_create)

        if not snap_create_resp.ok:
            provider_response.response = snap_create_resp
            provider_response.ok = False
            return provider_response
        snapshot = snap_create_resp.entity
        provider_response.entity = snapshot

        #Wait for ready status
        wait_for_snap_status_resp = self.wait_for_snapshot_status(
            snapshot.id, ready_status, timeout, wait_period)
        wait_for_snap_status_resp.entity = snapshot

        #Returns the most info by smushing together the status from the wait
        #and the info from the create.  We don't care here because it's in the
        #provider.

        return wait_for_snap_status_resp

    def wait_for_volume_status(
            self, volume_id, expected_status, timeout=None, wait_period=None):
        '''Waits for a specific status and returns when that status is
        observed.
        Note:  Shouldn't be used for transient statuses like 'deleting'.
        Default timeout and wait_period are set by user configs.
        '''

        wait_period = wait_period or self.default_wait_period
        timeout = timeout or self.default_timeout
        end_time = time.time() + timeout
        provider_response = ProviderActionResult()
        provider_response.ok = False

        while time.time() < end_time:
            resp = self.volumes_client.get_volume_info(
                volume_id=volume_id)
            provider_response.response = resp
            provider_response.ok = False

            if not resp.ok:
                self.provider_log.error(
                    "get_volume_info() call failed with status_code {0} while "
                    "waiting for volume status".format(resp.status_code))
                break

            if resp.entity is None:
                self.provider_log.error(
                    "get_volume_info() response body did not deserialize as "
                    "expected")
                break

            if resp.entity.status == expected_status:
                provider_response.ok = True
                self.provider_log.info('Volume status "{0}" observed'.format(
                    expected_status))
                break
        else:
            provider_response.ok = False
            self.provider_log.info(
                "wait_for_volume_status() ran for {0} seconds and did not "
                "observe the volume achieving the {1} status.".format(
                timeout, expected_status))

        return provider_response

    def wait_for_snapshot_status(
            self, snapshot_id, expected_status, timeout=None, wait_period=None):
        '''
        @summary: Waits for a specific status and returns when that status is
                  observed.
        Note:  Shouldn't be used for transient statuses like 'deleting'.
        Default timeout and wait_period are set by user configs.
        '''

        timeout = timeout or self.snapshot_create_wait
        wait_period = wait_period or self.default_wait_period
        time_waited = 0
        provider_response = ProviderActionResult()

        while True:
            snap_info_resp = self.volumes_client.get_snapshot_info(
                snapshot_id=snapshot_id)
            provider_response.response = snap_info_resp

            if not snap_info_resp.ok:
                provider_response.ok = False
                self.provider_log.error(
                    "Get Snapshot Info call failed while waiting for "
                    "snapshot status")
                break

            elif snap_info_resp.entity.status == expected_status:
                provider_response.ok = True
                self.provider_log.info('Snapshot status {0} reached'.format(
                    expected_status))
                break

            if time_waited >= timeout:
                self.provider_log.warning(
                    "Timed out while waiting for status: {0}. Last known "
                    "status was {1}".format(
                        expected_status, str(snap_info_resp.entity.status)))
                provider_response.ok = False
                break

            self.provider_log.info(
                "Waiting for Snapshot {0} to reach {1} status. "
                "Current status is {2}".format(
                    snapshot_id, expected_status,
                    snap_info_resp.entity.status))

            time.sleep(wait_period)
            time_waited += wait_period
            self.provider_log.info("Wait time remaining: {0} seconds".format(
                timeout - time_waited))

        return provider_response

    def delete_snapshot_confirmed(
            self, snapshot_id, timeout=None, wait_period=None):
        timeout = timeout or self.default_timeout
        wait_period = wait_period or self.default_wait_period
        time_waited = 0
        provider_response = ProviderActionResult()

        #Delete the snapshot.  Continue on 2XX, Return Success on a 404,
        #Fail on other.
        self.provider_log.info("Deleting snapshot and confirming delete")
        snap_del_resp = self.volumes_client.delete_snapshot(snapshot_id)
        provider_response.response = snap_del_resp

        #Catches special cases where snapshot is gone before we ask for delete.
        #Usefull for where tests may try to cleanup snapshots that are created in
        #setup but deleted as part of a test.
        if snap_del_resp.status_code == 404:
            self.provider_log.info(
                "Snapshot delete recieved 404, snapshot was deleted before "
                "function was called.")
            provider_response.ok = True
            return provider_response
        elif (snap_del_resp.status_code != 404) and (not snap_del_resp.ok):
            self.provider_log.error(
                "Snapshot delete request error. Unable to delete")
            provider_response.ok = False
            return provider_response

        #Wait for 404 return codw
        while True:
            self.provider_log.info(
                "Snapshot delete successfull, waiting for confirmation")
            #Get Snapshot status
            snap_info_resp = self.volumes_client.get_snapshot_info(snapshot_id)

            if snap_info_resp.status_code == 404:
                self.provider_log.info(
                    "Snapshot delete verified, 404 recieved")
                provider_response.ok = True
                return provider_response
            elif (snap_info_resp.status_code != 404) and (
                    not snap_info_resp.ok):
                self.provider_log.error(
                    "Error during snapshot delete verification, unable to "
                    "confirm delete")
                provider_response.ok = False
                provider_response.response = snap_info_resp
                return provider_response

            if time_waited >= timeout:
                self.provider_log.warning(
                    "Delete confirmation timed out. Last snapshot status was"
                    " {0}".format(snap_info_resp.entity.status))
                provider_response.ok = False
                provider_response.response = snap_info_resp
                break

            time.sleep(wait_period)
            time_waited += wait_period

        return provider_response

    def delete_volume_confirmed(
            self, volume_id, timeout=None, wait_period=None):
        '''
            Returns the last know status of the volume as a string, or
            'deleted' if a GET on the volume returns a 404.
        '''

        timeout = timeout or self.default_timeout
        wait_period = wait_period or self.default_wait_period
        time_waited = 0
        provider_response = ProviderActionResult()

        #Delete the volume.  Continue on 2XX, Return Success on a 404,
        #Fail on other.
        self.provider_log.info("Deleting volume and confirming delete")
        vol_del_resp = self.volumes_client.delete_volume(volume_id)
        provider_response.response = vol_del_resp

        #Catches special cases where volume is gone before we ask for delete.
        #Usefull for where tests may try to cleanup volumes that are created in
        #setup but deleted as part of a test.
        if vol_del_resp.status_code == 404:
            self.provider_log.info(
                "Volume delete recieved 404, volume was deleted before "
                "function was called.")
            provider_response.ok = True
            return provider_response
        elif (vol_del_resp.status_code != 404) and (not vol_del_resp.ok):
            self.provider_log.error(
                "Volume delete request error.  Unable to delete")
            provider_response.ok = False
            return provider_response

        #Wait for 404 return code
        while True:
            self.provider_log.info(
                "Volume delete successfull, waiting for confirmation")
            #Get volume status
            vol_info_resp = self.volumes_client.get_volume_info(volume_id)

            if vol_info_resp.status_code == 404:
                self.provider_log.info("Volume delete verified, 404 recieved")
                provider_response.ok = True
                return provider_response
            elif (vol_info_resp.status_code != 404) and (not vol_info_resp.ok):
                self.provider_log.error(
                    "Error during volume delete verification, unable to "
                    "confirm delete")
                provider_response.ok = False
                provider_response.response = vol_info_resp
                return provider_response

            if time_waited >= timeout:
                self.provider_log.warning(
                    "Delete confirmation timed out. Last volume status was "
                    "{0}".format(vol_info_resp.entity.status))
                provider_response.ok = False
                provider_response.response = vol_info_resp
                break

            time.sleep(wait_period)
            time_waited += wait_period

        return provider_response

    def delete_volume_with_snapshots(self, volume_id):
        self.provider_log.info('Deleting volume with snapshots')
        provider_response = ProviderActionResult()

        #Get a list of all snapshots for volume
        get_snapshots_response = self.get_list_of_snapshots_for_volume(
            volume_id)
        if not get_snapshots_response.ok:
            return get_snapshots_response

        if get_snapshots_response.entity is not None:
            #Delete all snapshots in the list
            for snapshot in get_snapshots_response.entity:
                snap_del_resp = self.delete_snapshot_confirmed(snapshot.id)
                provider_response.response = snap_del_resp
                if not snap_del_resp.ok:
                    self.provider_log.error(
                        'Error deleting snapshot: {0}'.format(snapshot.id))
                    provider_response.ok = False
                    return provider_response

        #Verify that volume has no snapshots
        vol_info_resp = self.volumes_client.get_volume_info(volume_id)
        provider_response.response = vol_info_resp
        if not vol_info_resp.ok:
            self.provider_log.error('Error retrieving volume info')
            provider_response.ok = False
            return provider_response

        volume = vol_info_resp.entity
        if volume.snapshot_id is not None:
            self.provider_log.error(
                "Volume is reporting that it still has snapshots, "
                "unable to delete")
            provider_response.ok = False
            return provider_response

        #Verifiably delete volume
        return self.delete_volume_confirmed(volume_id)

    def cleanup_volumes(self, volumes):
        for volume in volumes:
            self.delete_volume_with_snapshots(volume.id)

    def delete_volumes_by_regex(self):
        pass

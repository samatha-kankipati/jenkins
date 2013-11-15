'''
@summary: Provider Module for the CBS LUNR API
@note: Should be the primary interface to a test case or external tool.
@copyright: Copyright (c) 2012 Rackspace US, Inc.
'''
import json
import time
from datetime import datetime
from ccengine.providers.configuration import MasterConfigProvider
from ccengine.providers.base_provider import BaseProvider, ProviderActionResult
from ccengine.clients.blockstorage.lunr_api import LunrAPIClient as _lapic
from ccengine.domain.blockstorage.lunr_api import AccountResponse
from ccengine.domain.blockstorage.lunr_api import\
        StorageNode as _StorageNode,\
        Account as _AccountDomainObject,\
        Backup as _BackupDomainObject,\
        Volume as _VolumeDomainObject
from ccengine.domain.types import \
    LunrBackupStatusTypes as _LunrBackupStatusTypes,\
    LunrVolumeStatusTypes as _LunrVolumeStatusTypes


class LunrAPIProvider(BaseProvider):
    '''
        @summary: Provides an interface to all Volume related API Calls
    '''
    def __init__(self, config):
        '''
        @summary: Initializes config, logger, and Lunr API Client
        for instance of LunrAPIProvider
        @param config: lunr_api section of the config
        @type config: L{LavaAPIConfig}
        @param logger: Instance of Python Logger
        @type logger: C{Logger}
        @return: Instance of LunrAPIProvider
        @rtype: L{LunrAPIProvider}
        '''
        super(LunrAPIProvider, self).__init__()
        self.config = config

        self.lunr_api_admin_client = _lapic(
            bool(config.ssl), config.host, config.port)

        self.lunr_api_client = _lapic(
            bool(config.ssl),
            config.host,
            config.port,
            config.version,
            config.account_name,
            config.account_id)

    def list_storage_nodes(self):
        '''
            @summary: Finds all storage nodes visible to the Lunr API.
            @return: C{List} of L{StorageNodeDomainObject}
            @rtype: L{list}
        '''
        self.provider_log.info("Listing storage nodes")
        api_response = self.lunr_api_admin_client.Nodes.list()
        if not api_response.ok:
            self.provider_log.error('API returned %s' % str(api_response.status_code))
            return []
        node_info = json.loads(api_response.content)
        nodes = []
        for node in node_info:
            # lunr all-in-one deploys put storage nodes on the api node
            if node['hostname'] == '127.0.0.1':
                node['hostname'] = self.config.host
            nodes.append(_StorageNode(**node))

        return nodes

    def convert_json_to_domain_object_list(self, json_response, domain_object):
        '''
            @summary: Turns a list of generic dictionaries into a list of domain objects.
            @param json_response: List of dictionaries that each represent a domain object
            @type json_response: C{list}
            @param domain_object: Type of domain object that each dictionary will be converted into
            @type domain_object: C{class}
            @return: Domain object list.
            @rtype: C{list}
        '''
        domain_objects_list = []
        for json_object in json_response:
            domain_objects_list.append(domain_object(**json_object))
        return domain_objects_list

    def create_user_client(self):
        '''
            @summary: Creates a user's account and an instance of a
                      L{LunrAPIClient} for that account.
            @return: L{LunrAPIClient}
        '''
        account_name = "LunrTestAccount_%d" % datetime.now().microsecond
        api_response = self.lunr_api_admin_client.Accounts.create(params={'id': account_name})
        if not api_response.ok:
            self.provider_log.error('API returned %s' % str(api_response.status_code))
            return None

        assert api_response.ok, 'API Call to create new lunr account failed'\
                ' with {0}, expected 2XX'.format(api_response.status_code)

        created_user = AccountResponse._json_to_obj(api_response.content)

        return _lapic(bool(self.config.ssl), self.config.host,
            self.config.port, self.config.version, created_user.name,
            created_user.id)

    def create_specific_user_client(self, account_name, account_id):
        '''
            @summary: Creates a user's account and an instance of a L{LunrAPIClient} for that account.
            @return: L{LunrAPIClient}
        '''
        return _lapic(bool(self.config.ssl), self.config.host,
            self.config.port, self.config.version, account_name,
            account_id)

    def create_invalid_user(self):
        '''
            @summary: Create invalid user with invalid name and id
            @return: Instance of L{LunrAPIClient} to create API urls with nonexistent user information
            @rtype: L{LunrAPIClient}
        '''

        invalid_user_name = 'INVALID_NAME%d' % datetime.now().microsecond
        invalid_user_id = 'INVALID_ID%d' % datetime.now().microsecond
        invalid_account = _lapic(bool(self.config.ssl), self.config.host,
            self.config.port, self.config.version, invalid_user_name,
            invalid_user_id)
        self.provider_log.info("Created Invalid Account: %s" % invalid_user_name)
        return invalid_account

    def create_volume_backup(self, volume_id, user_client):
        '''
            @summary: Uses the user lunr api client to create a backup for the given volume.
            @param volume_id: ID of volume to be backed up
            @type volume_id: C{str}
            @param user_client: Client used to make API call for creating backup
            @type user_client: L{LunrAPIClient}
            @return: Backup domain object representing a successfully created backup. None is returned if any error occurs.
            @rtype: L{Backup}
        '''
        backup_name = "Backup_%d" % datetime.now().microsecond
        api_response = user_client.Backups.create(backup_name, params={'volume': volume_id})
        if api_response.ok:
            created_backup = _BackupDomainObject(**json.loads(api_response.content))
            wait_status = self.wait_for_volume_backup_status(created_backup.id, _LunrBackupStatusTypes.READY, user_client=user_client)
            if wait_status.ok:
                created_backup = wait_status.entity
                self.provider_log.info("Created Backup: %s" % created_backup.id)
                return created_backup

    def wait_for_volume_status(self, volume_id, expected_status, user_client, timeout=120):
        '''
            @summary: Waits a max of timeout seconds for the requests status to
            show up in the volume get-info response.
            @param volume_id: ID for volume to wait on for status
            @type volume_id: C{str}
            @param expected_status: Status that this method is waiting for volume to reach
            @type expected_status: C{str}
            @param user_client: Client to get info on volume to get its current status
            @type user_client: L{LunrAPIClient}
            @param timeout: Seconds until method times out if the expected status is never reached
            @type timeout: C{int}
            @return: Result object that includes last api response, whether the wait was successful,
            and the Volume domain object
            @rtype: L{ProviderActionResult}
        '''
        provider_action_result = ProviderActionResult()
        total_wait = 0
        wait_increment = 1
        self.provider_log.info("Waiting for volume %s Status %s. . ."
                                    % (volume_id, expected_status))
        while total_wait <= timeout:
            api_response = user_client.Volumes.get_info(volume_id)
            provider_action_result.response = api_response
            if not api_response.ok:
                self.provider_log.error('API returned %s' % str(api_response.status_code))
                break
            volume_domain_object = _VolumeDomainObject(**json.loads(api_response.content))
            provider_action_result.entity = volume_domain_object
            current_status = volume_domain_object.status
            self.provider_log.debug("Waiting for volume %s Status %s, current Status is %s . . ."
                                            % (volume_id, expected_status, current_status))
            if current_status == expected_status:
                self.provider_log.info("Volume %s returned with expected status %s"
                                       % (volume_domain_object, expected_status))
                provider_action_result.ok = True
                break
            else:
                self.provider_log.info("Still waiting for status: %s, Current status: %s Time remaining until timeout: %d"
                                       % (expected_status, current_status, timeout - total_wait))
                time.sleep(wait_increment)
                total_wait += wait_increment
        self.provider_log.warning("Volume %s never reached expected status %s before timeout %d"
                                  % (volume_domain_object, expected_status, timeout))
        return provider_action_result

    def wait_for_volume_backup_status(self, backup_id, expected_status, user_client, timeout=120):
        '''
            @summary: Waits a max of timeout seconds, 1 seconds at a time, for
            the requests status to show up in the volume get-info response.
            returns the final status state of the backup.
        '''
        total_wait = 0
        wait_increment = 1
        provider_action_result = ProviderActionResult()
        self.provider_log.info("Waiting for volume backup %s Status %s. . ."
                            % (backup_id, expected_status))
        while total_wait <= timeout:
            api_response = user_client.Backups.get_info(backup_id)
            provider_action_result.response = api_response
            if not api_response.ok:
                self.provider_log.error('API returned %s' % str(api_response.status_code))
                break
            backup_domain_object = _BackupDomainObject(**json.loads(api_response.content))
            provider_action_result.entity = backup_domain_object
            current_status = backup_domain_object.status
            self.provider_log.debug("Waiting for volume %s Status %s, current Status is %s . . ."
                                        % (backup_id, expected_status, current_status))
            if current_status == expected_status:
                self.provider_log.info("Volume backup %s returned with expected status %s"
                                       % (backup_domain_object, expected_status))
                provider_action_result.ok = True
                return provider_action_result
            else:
                self.provider_log.info("Still waiting for status: %s, Current status: %s Time remaining until timeout: %d"
                                       % (expected_status, current_status, timeout - total_wait))
                time.sleep(wait_increment)
                total_wait += wait_increment
        self.provider_log.warning("Backup %s never reached expected status %s before timeout %d"
                               % (backup_domain_object, expected_status, timeout))
        return provider_action_result

    def create_volume_for_user(self, user_client, volume_type):
        '''
            @summary: Makes a lunr api call for the user_client to create a volume of given volume type.
            @param user_client: Lunr API Client instance for a user
            @type user_client: C{LunrAPIClient}
            @param volume_type: Type for volume to be created as
            @type volume_type: C{str}
            @return: The json object, representing the created volume
            @rtype: C{dict}
        '''
        expected_name = "TestVolume_%d" % datetime.now().microsecond
        expected_size = volume_type['min_size']
        api_response = user_client.Volumes.create(expected_name, expected_size, volume_type['name'])
        assert api_response.ok, 'Volume create for {0} returned {0}, expected 2XX'.format(user_client.account_name, api_response.status_code)

        if api_response.ok:
            actual_volume = _VolumeDomainObject(**json.loads(api_response.content))
            wait_result = self.wait_for_volume_status(actual_volume.id, _LunrVolumeStatusTypes.READY, user_client)
            if wait_result.ok:
                return wait_result.entity

    def delete_user_volume(self, user_client, volume_id):
        '''
            @summary: Iterates through all volumes listed for a user and then deletes them
            @param user_client: Client associated to an account whose volume will be deleted
            @type user_client: L{LunrAPIClient}
            @param volume_id: ID of volume to be deleted
            @type volume_id: C{str}
            @return: Whether the volume was successfully deleted
            @rtype: C{bool}
        '''
        api_response = user_client.Volumes.delete(volume_id)
        if api_response.ok:
            wait_result = self.wait_for_volume_status(volume_id, _LunrVolumeStatusTypes.DELETED, user_client)
            if wait_result.ok:
                return True
        return False

    def delete_user_volumes(self, account_client):
        '''
            @summary: Iterates through all volumes listed for a user and then deletes them
            @param account_client: Client associated to an account whose volumes will be deleted
            @type account_client: L{LunrAPIClient}
            @return: Whether all volumes were successfully deleted
            @rtype: C{bool}
        '''
        api_response = account_client.Volumes.list()
        if not api_response.ok:
            self.provider_log.error('API returned %s' % str(api_response.status_code))
            return False
        volumes = self.convert_json_to_domain_object_list(json.loads(account_client.Volumes.list().content), _BackupDomainObject)
        for volume in volumes:
            api_response = account_client.Volumes.delete(volume.id)
            if not api_response.ok:
                self.provider_log.error('API returned %s' % str(api_response.status_code))
                return False
            self.provider_log.info("Deleting Volume: %s" % volume.id)
        for volume in volumes:
            if volume.status == _LunrVolumeStatusTypes.DELETING:
                wait_result = self.wait_for_volume_status(volume.id, _LunrVolumeStatusTypes.DELETED, account_client)
                if not wait_result.ok:
                    return False
        return True

    def delete_user_backups(self, account_client):
        '''
            @summary: Iterates through all backups listed for a user and then deletes them
            @param account_client: Client associated to an account whose backups will be deleted
            @type account_client: L{LunrAPIClient}
            @return: Whether all backups were successfully deleted
            @rtype: C{bool}
        '''
        api_response = account_client.Backups.list()
        if not api_response.ok:
            self.provider_log.error('API returned %s' % str(api_response.status_code))
            return False
        backups = self.convert_json_to_domain_object_list(json.loads(api_response.content), _BackupDomainObject)
        for backup in backups:
            self.provider_log.info("Deleting Backup: %s" % backup)
            api_response = account_client.Backups.delete(backup.id)
            if not api_response.ok:
                self.provider_log.warning("Call to Delete Backup %s failed" % backup)

        for backup in backups:
            if backup.status == _LunrBackupStatusTypes.DELETING:
                wait_status = self.wait_for_volume_backup_status(backup.id, _LunrBackupStatusTypes.DELETED, user_client=account_client)
                if not wait_status.ok:
                    return False
        return True

    def cleanup_account(self, account_client):
        '''
            @summary: Deletes account's backups and volumes then the account itself
            @param account_client: Client associated to account to be cleaned up
            @type account_client: L{LunrAPIClient}
        '''
        self.delete_user_backups(account_client)
        self.delete_user_volumes(account_client)
        self.provider_log.info("Deleting Account: %s" % account_client.account_name)
        api_response = self.lunr_api_admin_client.Accounts.delete(account_client.account_id)
        api_response.ok

    def is_account_auto_generated(self, user_id, admin_client):
        '''
            @summary: Checks if account exists and is active
            @param user_id: ID for account to be verified
            @type user_id: L{str}
            @param admin_client: Client associated to Lunr admin
            @type admin_client: L{LunrAPIClient}
            @return: Whether account exists and is active
            @rtype: C{bool}
        '''
        api_response = admin_client.Accounts.get_info(user_id)

        if api_response.ok is False:
            self.provider_log.warning("An account was NOT auto generated.")
            return False
        auto_generated_account = AccountResponse._json_to_obj(
                api_response.content)
        if auto_generated_account.status != 'ACTIVE':
            self.provider_log.warning("Auto Generated Account does not have status ACTIVE")
            return False

        self.provider_log.info("Account Auto Generated with status ACTIVE")
        return True

    def create_auto_generated_account(self, invalid_user, admin_client):
        '''
            @summary: Creates an Auto Generated Account via Volume List
            @param invalid_user: Client to create an API call for a nonexistent user
            @type invalid_user: L{LunrAPIClient}
            @param admin_client: Client for Lunr admin to get info on the auto-generated account
            @type: L{LunrAPIClient}
            @return: Client associated to the generated account. Returns None if unsuccessful
            @rtype: L{LunrAPIClient}
        '''
        #Creates an auto generated account
        invalid_user.Volumes.list()

        if self.is_account_auto_generated(invalid_user.account_id, admin_client):
            api_response = admin_client.Accounts.get_info(invalid_user.account_id)
            auto_generated_account = AccountResponse._json_to_obj(
                api_response.content)
            self.provider_log.info("Auto Generated Created: '%s'" % auto_generated_account)
            return auto_generated_account

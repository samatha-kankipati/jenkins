'''
@summary: Provider Module for the CBS Storage Node API
@note: Should be the primary interface to a test case or external tool.
@copyright: Copyright (c) 2012 Rackspace US, Inc.
'''
import json
import time
from ccengine.providers.base_provider import BaseProvider
from datetime import datetime
from ccengine.domain.blockstorage.storage_node_api import Volume as _VolumeDomainObject
from ccengine.clients.blockstorage.storage_node_api import\
        StorageNodeAPIClient as _snapic


class StorageNodeAPIProvider(BaseProvider):
    """
    @summary: Provides an interface to all Storage Node related API Calls
    """

    def __init__(self, config):
        super(StorageNodeAPIProvider, self).__init__()
        self.config = config
        self.storage_node_config = self.config.storage_node_api
        self.storage_node_api_clients = []

    def create_node_config(self, node):
        '''
        @summary: Generates a config from the node's host and port and
        Returns a storage node api client, using the generated configs
        '''
        mcpdict = {'storage_node_api': {'autodetect': 'False', 'host':
                str(node.hostname), 'port': str(node.port), 'ssl': 'False'}}

        node_config = self.config.mcp_override(mcpdict)
        return node_config

    def create_snapi_client(self, node):
        '''
        @summary: Generates a config from the node's host and port and
        Returns a storage node api client, using the generated config
        '''
        if self.storage_node_config.autodetect:
            node_config = self.create_node_config(node).storage_node_api
            snapi_client = _snapic(node_config.ssl, node_config.host,
                    node_config.port, name=node.name)
            return snapi_client
        else:
            print 'Currently, the CloudBlockStorage test fixture requires that the StorageNodeAPI Section be set to autodetect=True'
            raise NotImplementedError

    def delete_storage_node_volumes(self, snapi_clients, volumes):
        '''
            @summary: Loops through storage node api clients and deletes each node's volume
        '''
        for snapi_client in snapi_clients:
            volume = volumes[snapi_client.name]
            snapi_client.Volumes.delete(volume.id)
            volume_deleted = self.wait_for_volume_deleted(snapi_client, volume.id)
            if volume_deleted:
                self.provider_log.info("Deleted Volume: %s from Node: %s" % (volume.id, snapi_client.name))
            else:
                self.provider_log.info("Volume %s was not deleted" % volume.id)

    def delete_backups(self, snapi_clients, volumes, backups):
        '''
            @summary: Loops through storage node api clients and deletes each node's volume backups
        '''
        for snapi_client in snapi_clients:
            volume = volumes[snapi_client.name]
            backup = backups[(snapi_client, volume.id)]
            snapi_client.Backups.delete(volume.id, backup.id)
            self.wait_for_storage_node_vol_backup_to_complete(snapi_client, volume.id, backup.id)
            self.provider_log.info("Deleted Backup: %s for Volume: %s on Node: %s" % (backup.id, volume.id, snapi_client.name))

    def wait_for_volume_deleted(self, snapi_client, volume_id, timeout=120):
        '''
            @summary: Waits a max of timeout seconds, 1 seconds at a time, for
            the api response status to fail when volume cannot be found
        '''
        total_wait = 0
        wait_increment = 1
        while total_wait <= timeout:
            api_response = snapi_client.Volumes.get_info(volume_id)
            if not api_response.ok:
                if json.loads(api_response.content)['reason'] == "No volume named '%s'" % volume_id:
                    return True
            else:
                time.sleep(wait_increment)
                total_wait += wait_increment
        return False

    def create_volume(self, snapi_client):
        '''
            @summary: Creates volume on given storage node and returns the json object of the volume
        '''
        expected_name = "TestVolume_%d" % datetime.now().microsecond
        expected_size = 1
        api_response = snapi_client.Volumes.create(expected_name, params={'size':expected_size})
        if api_response.ok:
            created_volume = _VolumeDomainObject(**json.loads(api_response.content))
            self.provider_log.info("Created Volume: %s on Node: %s" % (created_volume.id, snapi_client.name))
        return created_volume

    def wait_for_storage_node_vol_backup_to_complete(self, snapi_client, volume_id, backup_id, timeout=120):
        '''
            @summary: Waits a max of timeout seconds, 2 seconds at a time, for get_info() to return 404.
            This means the backup job is done running.
        '''
        if timeout <= 0:
            raise 'wait_for_backup job_status timeout parameter must be greater than zero'
        total_wait = 0
        final_check = None
        while total_wait <= timeout:
            api_response = snapi_client.Backups.get_info(volume_id, backup_id)
            if api_response.status_code == 200:
                info = json.loads(api_response.content)
                self.provider_log.info('current status: %s' % info['status'])
            if api_response.status_code == 404:
                final_check = True
                break
            elif api_response.status_code != 200:
                assert False, 'Backup on storage node failed: %s:%s' % (str(api_response), str(api_response.content))
            else:
                self.provider_log.info('Waiting 2 seconds for storage node backup to finish saving')
                time.sleep(2)
                total_wait += 2

        self.provider_log.info('Storage Node volume backup complete: %s' % str(final_check))
        return api_response, final_check

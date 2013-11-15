import json
from ccengine.clients.base_client import BaseMarshallingClient


class BackupClient(BaseMarshallingClient):

    def __init__(self, url, auth_token, serialize_format=None,
                 deserialize_format=None):
        """
        Client that accesses the Cloud Backup API
        """
        super(BackupClient, self).__init__(serialize_format,
                                           deserialize_format)
        self.url = url
        self.auth_token = auth_token
        self.default_headers['X-Auth-Token'] = auth_token
        self.default_headers['Content-Type'] = 'application/{0}'.format(
            self.serialize_format)
        self.default_headers['Accept'] = 'application/{0}'.format(
            self.deserialize_format)

    def get_backup_status(self, ip_address):
        '''
        @summary: Returns the backup agent info for the given machine
        @param ip_address: IP address of the server
        @type : string
        '''
        url = "{0}".format(self.url)
        response = self.request("GET", url)
        json_resp = json.loads(response.text)
        for agent in json_resp:
            if agent['IPAddress'] == ip_address:
                return agent
        return None

    def get_backup_config(self, server_name):
        '''
        @summary : Returns the backup agent config details for the
                   given machine
        @param server_name: Machine name of the server
        @type server_name: string
        '''
        url = "{0}".format(self.url)
        response = self.request("GET", url)
        json_resp = json.loads(response.text)
        for agent in json_resp:
            if agent['MachineName'] == server_name:
                return agent
        return None

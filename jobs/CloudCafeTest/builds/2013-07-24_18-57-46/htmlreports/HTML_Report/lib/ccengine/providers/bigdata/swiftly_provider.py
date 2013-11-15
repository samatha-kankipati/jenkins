'''
@summary: Provider for Swiftly Commands
@copyright: Copyright (c) 2012 Rackspace US, Inc.
'''
from ccengine.providers.base_provider import BaseProvider
from ccengine.common.connectors.ssh import SSHConnector
from ccengine.clients.bigdata.swiftly_client import SwiftlyClient


class SwiftlyProvider(BaseProvider):
    def __init__(self, config, node):
        super(SwiftlyProvider, self).__init__()
        self.config = config
        self.ssh_connector = SSHConnector(node.ip,
                                          self.config.lava_api.USER_NAME,
                                          self.config.lava_api.PASSWORD)
        self.swiftly_client = SwiftlyClient(self.config.lava_api.USER_NAME,
                                            self.config.lava_api.PASSWORD,
                                            self.config.lava_api.SWIFTLY_AUTH_URL,
                                            self.config.lava_api.SWIFTLY_AUTH_USER,
                                            self.config.lava_api.SWIFTLY_AUTH_KEY,
                                            node.ip)

    def get_container_objects(self, container_name):
        response = self.swiftly_client.get(container_name)
        return response.split('\r\n')

    def get_containers(self):
        response = self.swiftly_client.get()
        return response.split('\r\n')

    def create_container(self, name):
        return self.swiftly_client.put(name)

    def create_file(self, container, name, source_file):
        source = 'cat %s | ' % source_file
        destination = container + "/" + name
        return self.swiftly_client.put(destination, source)

    def delete_container(self, container):
        '''
        @summary: Delete all objects in the container. Then delete the
                  container.
        @param node: Node to create ssh connection to access swiftly commands
        @type node: L{Node}
        @param container: Container to be cleared and deleted
        @type container: C{str}
        @return: None
        @rtype: None
        '''
        files_to_be_deleted = self.get_container_objects(container)
        for file in files_to_be_deleted:
            self.delete_file(container, file)

    def delete_file(self, container, file):
        delete_file = container + '/' + file
        self.swiftly_client.delete(delete_file)

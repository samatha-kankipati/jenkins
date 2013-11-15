'''
@summary: Client to execute Swiftly commands on a node
@copyright: Copyright (c) 2012 Rackspace US, Inc.
'''
from ccengine.clients.base_client import BaseClient
from ccengine.common.connectors.ssh import SSHConnector


class SwiftlyClient(BaseClient):
    def __init__(self,
                 username,
                 password,
                 swiftly_auth_url,
                 swiftly_auth_user,
                 swiftly_auth_key,
                 host):
        super(SwiftlyClient, self).__init__()
        self.username = username
        self.password = password
        self.swiftly_auth_url = swiftly_auth_url
        self.swiftly_auth_user = swiftly_auth_user
        self.swiftly_auth_key = swiftly_auth_key
        self.host = host
        self.ssh_connector = SSHConnector(self.host,
                                          self.username,
                                          self.password)

    def run_command(self, command, pre_variables='', post_variables=''):
        '''
        @summary: Use ssh connection to run a command with swiftly.
        @param command: Swiftly command to be run
        @type command: C{str}
        @param pre_variables: Variables to be added before the swiftly call
        @type pre_variables: C{str}
        @param post_variables: Variables to be added after the swiftly call
        @type post_variables: C{str}
        @return: Response from swiftly
        @rtype: C{str}
        '''
        prompt = "{0}@GATEWAY".format(self.username)
        command = "{0} swiftly -A {1} -U {2} -K {3} {4} {5}".format\
            (pre_variables, self.swiftly_auth_url,
             self.swiftly_auth_user,
             self.swiftly_auth_key, command, post_variables)
        response, prompt = self.ssh_connector.\
            exec_shell_command_wait_for_prompt(command,
                                               prompt,
                                               timeout=50)
        return response

    def get(self, container_name=''):
        return self.run_command("get", post_variables=container_name)

    def put(self, name, source=''):
        return self.run_command("put", pre_variables=source,
                                post_variables=name)

    def delete(self, filename):
        return self.run_command("delete", post_variables=filename)

    def get_file(self, cloud_file_path, local_file_path):
        return self.run_command("get", post_variables=cloud_file_path +
                                " -o %s" % (local_file_path))

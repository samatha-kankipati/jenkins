'''
@summary: Client to execute HBASE SHELL commands on a node
@copyright: Copyright (c) 2012 Rackspace US, Inc.
'''
from ccengine.clients.base_client import BaseClient
from ccengine.common.connectors.ssh import SSHConnector

class HbaseShellClient(BaseClient):
    def __init__(self, config, node):
        super(HbaseShellClient, self).__init__()
        self.config = config
        self.ssh_connector = SSHConnector(node.ip,
                                          self.config.lava_api.USER_NAME,
                                          self.config.lava_api.PASSWORD)
        self.PROMPT = "hbase(main)"

    def start_hbase_shell(self):
        response, prompt = self.ssh_connector.exec_shell_command_wait_for_prompt("hbase shell\n", self.PROMPT)
        return response

    def run_command(self, command, variables=''):
        response, prompt = self.ssh_connector.exec_shell_command_wait_for_prompt('%s %s\n' % (command, variables), self.PROMPT)
        return response



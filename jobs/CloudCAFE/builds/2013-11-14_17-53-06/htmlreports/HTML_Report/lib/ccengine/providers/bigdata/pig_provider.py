'''
@summary: Provider for Pig commands on a Node
@copyright: Copyright (c) 2012 Rackspace US, Inc.
'''
from ccengine.common.connectors.ssh import SSHConnector
from ccengine.providers.base_provider import BaseProvider


class PigProvider(BaseProvider):
    def __init__(self, config, node):
        super(PigProvider, self).__init__()
        self.config = config
        self.ssh_connector = SSHConnector(node.ip,
                                          self.config.lava_api.USER_NAME,
                                          self.config.lava_api.PASSWORD)
        ip_sections = self.ssh_connector.host.split('.')
        self.prompt = "%s@GATEWAY" % (self.config.lava_api.USER_NAME)
        self.timeout = float(self.config.lava_api.PIG_TIMEOUT)

    def run_pig_job(self, job_name):
        self.provider_log.info("Running Pig Job on Node")
        cmd = 'pig -f %s\n' % job_name
        response, prompt = self.ssh_connector.\
            exec_shell_command_wait_for_prompt(cmd,
                                               self.prompt,
                                               timeout=self.timeout)
        return response

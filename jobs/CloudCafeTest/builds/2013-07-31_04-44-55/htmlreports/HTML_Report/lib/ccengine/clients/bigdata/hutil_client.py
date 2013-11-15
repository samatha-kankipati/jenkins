'''
@summary: Client to execute Hadoop commands on a node
@copyright: Copyright (c) 2012 Rackspace US, Inc.
'''
import json
from ccengine.clients.base_client import BaseClient
from ccengine.common.connectors.ssh import SSHConnector

class HutilClient(BaseClient):
    def __init__(self, config, node):
        super(HutilClient, self).__init__()
        self.config = config
        self.ssh_connector = SSHConnector(node.ip,
                                          self.config.lava_api.USER_NAME,
                                          self.config.lava_api.PASSWORD)
        self.BASE_COMMAND = '/root/hutil/hutil'

    def run_query(self, job_type, job_name):
        '''
        @summary: Use ssh connection to run a job with hutil runquery
        @param job_type: Type of job to run. Used as argument in hutil command
        @type job_type: C{str}
        @param job_name: Name of job file to run. Used as argument in hutil command
        @type job_name: C{str}
        @return: The response of the command
        @rtype: C{dict}
        '''
        response,prompt = self.ssh_connector.exec_shell_command("%s runquery %s <'%s'\n"
                                                   % (self.BASE_COMMAND,
                                                      job_type,
                                                      job_name))
        self.client_log.info("runquery: \n'%s'" % response)

        response_dictionary = {}
        try:
            response_dictionary = json.loads(response)
        except ValueError, value_exception:
            self.client_log.warning("Response cannot be converted to JSON. Response: %s"
                                      % response)
        return response_dictionary

    def get_query_status(self, handle):
        '''
        @summary: Get status of query
        @param handle: ID for query
        @type handle: C{str}
        @return: Status. Return empty string if it failed to call command
        @rtype: C{str}
        '''
        response, prompt = self.ssh_connector.exec_shell_command("%s getquerystatus %s\n"
                                                   % (self.BASE_COMMAND,
                                                      handle))
        self.client_log.info("getquerystatus: \n %s" % response)
        try:
            response_dictionary = json.loads(response)
        except ValueError, value_exception:
            self.client_log.warning("Response cannot be converted to JSON. Response: %s"
                                % response)
            return ''
        return response_dictionary['status']

    def list_all_jobs(self):
        '''
        @summary: Use ssh connection to list all jobs with hutil listalljobs
        @return: The response of the command
        @rtype: C{dict}
        '''
        response = self.ssh_connector.exec_command("%s listalljobs\n"
                                                   % self.BASE_COMMAND)
        self.client_log.info("listalljobs: \n'%s'" % response)

        response_dictionary = {}
        try:
            response_dictionary = json.loads(response)
        except ValueError, value_exception:
            self.client_log.warning("Response cannot be converted to JSON. Response: %s"
                                      % response)
        return response_dictionary


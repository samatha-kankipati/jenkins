'''
@summary: Provider for hutil commands on a cluster
@copyright: Copyright (c) 2012 Rackspace US, Inc.
'''
import json
import time
from ccengine.common.connectors.ssh import SSHConnector
from ccengine.providers.base_provider import BaseProvider
from ccengine.clients.bigdata.hutil_client import HutilClient

class HutilProvider(BaseProvider):
    def __init__(self, config, node):
        super(HutilProvider, self).__init__()
        self.config = config
        self.ssh_connector = SSHConnector(node.ip, self.config.lava_api.USER_NAME, 
                                          self.config.lava_api.PASSWORD)
        self.BASE_COMMAND = '/root/hutil/hutil'
        self.hutil_client = HutilClient(config, node)

    def wait_for_handle_status(self, handle, expected_status, timeout = 500):
        '''
        @summary: Wait for query to reach a given status.
        Times out if query doesn't the status within alloted time.
        @param handle: Query's ID handle
        @type handle: C{str}
        @param expected_status: Status for query to reach
        @type expected_status: C{str}
        @param timeout: Maximum seconds to wait for query to 
                        reach expected status
        @type timeout: C{int}
        @return: Last status received for query
        @rtype: C{str}
        '''
        total_wait = 0
        WAIT_INCREMENT = 1
        current_status = ""

        while total_wait <= timeout:
            current_status = self.hutil_client.get_query_status(handle)
            if current_status == expected_status or current_status == 'Error':
                return current_status

            time.sleep(WAIT_INCREMENT)
            total_wait += WAIT_INCREMENT
            self.provider_log.info("Still waiting for status '%s', "\
                                   "Current Status '%s', Time remaining: '%d'"
                                   % (expected_status, 
                                      current_status, 
                                      timeout-total_wait))

        self.provider_log.warning("Handle '%s' never reached expected"\
                                  " status '%s' before timeout %d"
                                  % (handle, expected_status, timeout))
        return current_status
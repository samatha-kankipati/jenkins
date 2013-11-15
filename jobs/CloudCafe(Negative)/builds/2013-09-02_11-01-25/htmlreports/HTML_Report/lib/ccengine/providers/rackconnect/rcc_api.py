from ccengine.providers.base_provider import BaseProvider
from ccengine.clients.rackconnect.rackconnect_api import RackConnectApiClient
from ccengine.providers.identity.identity_v2_0_api import IdentityAPIProvider
import time


class RackconnectProvider(BaseProvider):
    def __init__(self, config, logger):

        super(RackconnectProvider, self).__init__()
        self.config = config
        self.identity_provider = IdentityAPIProvider(self.config)
        auth_data = self.identity_provider.authenticate().entity

        if config.rackconnect.url is not None:
            self.url = config.rackconnect.url

        else:
            service_name = config.rackconnect.identity_service_name
            service = auth_data.serviceCatalog.get_service(service_name)
            if service is not None:
                self.url = service.endpoints[0].publicURL
            else:
                self.provider_log.info('No endpoint url for rackconnect \
                                         to make call')

        self.racknova_client = \
        RackConnectApiClient(self.url, self.config.auth.username, self.config.auth.api_key,
                     config.misc.serializer, config.misc.deserializer)
        self.rackcore_client = \
        RackConnectApiClient(self.url, self.config.rackconnect.user, self.config.rackconnect.password,
                     config.misc.serializer, config.misc.deserializer)
    
    def wait_for_rackconnect_deployed_status(self, 
                                             account_number, 
                                             tenant_id,
                                             server_id,
                                             status_to_wait_for):
        '''
        @summary: Polls server level deployed status
            until status_to_wait_for is met

        '''
        tnn_configs = self.rackcore_client.get_tenant_automation_status(
            account_number=self.config.rackconnect.account_number,
            tenant_id=self.config.compute_api.tenant_id)
        for item in tnn_configs.entity:
            if item.api_server_id == server_id:
                automation_status = item.automation_status
        time_waited = 0
        interval_time = self.config.compute_api.build_interval
        while (automation_status.lower() != status_to_wait_for.lower() and
               time_waited < self.config.rackconnect.rackconnect_timeout):
            tnn_configs = self.rackcore_client.get_tenant_automation_status(
            account_number=self.config.rackconnect.account_number,
            tenant_id=self.config.compute_api.tenant_id)
            for item in tnn_configs.entity:
                if item.api_server_id == server_id:
                    automation_status = item.automation_status
            time.sleep(interval_time)
            time_waited += interval_time
        return automation_status

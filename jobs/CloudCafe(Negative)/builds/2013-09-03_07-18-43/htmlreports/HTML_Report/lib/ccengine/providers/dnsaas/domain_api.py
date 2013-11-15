from ccengine.providers.base_provider import BaseProvider
from ccengine.clients.dnsaas.domain_api import DnsaasAPIClient
from ccengine.clients.dnsaas.records_api import RecordsAPIClient
from ccengine.providers.identity.identity_v2_0_api import IdentityAPIProvider
from ccengine.domain.types import DnsaasAsyncStatusTypes as DnsStatus
import time
import json


class DomainProvider(BaseProvider):

    def __init__(self, config, logger):

        super(DomainProvider, self).__init__()
        self.config = config
        self.identity_provider = IdentityAPIProvider(self.config)
        auth_data = self.identity_provider.authenticate().entity
        if config.dnsaas.url is not None:
            self.url = config.dnsaas.url
        else:
            service_name = config.dnsaas.identity_service_name
            service = auth_data.serviceCatalog.get_service(service_name)
            if service is not None:
                self.url = service.endpoints[0].publicURL
            else:
                self.provider_log.info('No endpoint url present for dnsaas \
                                         to make call')
        self.client = DnsaasAPIClient(self.url, auth_data.token.id,
                                      config.misc.serializer,
                                      config.misc.deserializer)
        self.record_client = RecordsAPIClient(self.url, auth_data.token.id,
                                      config.misc.serializer,
                                      config.misc.deserializer)

    def test_cleanup(self):
        api_response = self.client.list_all_domain()
        self.data = []
        if api_response.entity.totalEntries != 0:
            for i in range(api_response.entity.totalEntries):
                self.domain_id = api_response.entity[i].id
                self.data.append(api_response.entity[i].id)
                api_responsedel = self.client.delete_domain(self.domain_id)
                assert api_responsedel.status_code == 202
                time.sleep(1)
                callbackUrl = api_responsedel.entity.callbackUrl
                api_responsecallback = self.client.call_backUrl(callbackUrl)
                assert api_responsecallback.status_code == 200
                status = api_responsecallback.entity.status
                while status != 'COMPLETED':
                    time.sleep(5)
                    api_responsecallback = self.client.call_backUrl(callbackUrl)
                    status = api_responsecallback.entity.status
                    if status == "ERROR":
                        break

            for dat in self.data:
                api_responsedomain = self.client.list_domain_details(dat)
                assert api_responsedomain.status_code == 404, 'DomainCleanup \
                not done: %s' % api_responsedomain.content
        else:
            pass
            self.fixture_log.info("No Domains Present: %s" % \
                                  (api_response.entity))

    def test_wait_for_status(self, api_responsedomain):
        """
        wait for callbackUrl to Complete and exit if its in error state
        """
        time_waited = 0
        interval_time = 3
        timeout = 360
        callbackUrl = api_responsedomain.entity.callbackUrl
        api_responsecallback = self.client.call_backUrl(callbackUrl)
        assert api_responsecallback.status_code == 200
        status = api_responsecallback.entity.status
        while (status != 'COMPLETED' and time_waited < timeout):
                    time.sleep(5)
                    api_responsecallback = self.client.call_backUrl(callbackUrl)
                    time_waited += interval_time
                    status = api_responsecallback.entity.status
                    if status == 'ERROR':
                        break
        return status

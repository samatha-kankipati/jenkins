from ccengine.providers.base_provider import BaseProvider
from ccengine.clients.dnsaas.ptr_api import PtrAPIClient
from ccengine.providers.identity.identity_v2_0_api import IdentityAPIProvider
import time


class PtrProvider(BaseProvider):
    def __init__(self, config, logger):

        super(PtrProvider, self).__init__()
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

        rel = config.dnsaas.rel
        href = config.dnsaas.href

        self.client = \
        PtrAPIClient(self.url, rel, href, auth_data.token.id,
                     config.misc.serializer, config.misc.deserializer)

    def test_wait_for_status(self, api_response):
        """
        wait for callbackUrl to Complete and exit if its in error state
        """
        time_waited = 0
        interval_time = 5
        timeout = 360
        callbackUrl = api_response.entity.callbackUrl
        api_responsecallback = self.client.call_backUrl(callbackUrl)
        assert api_responsecallback.status_code == 200
        status = api_responsecallback.entity.status
        while (status != 'COMPLETED' and time_waited < timeout):
                    time.sleep(interval_time)
                    api_responsecallback = self.client.call_backUrl(callbackUrl)
                    time_waited += interval_time
                    status = api_responsecallback.entity.status
                    if status == 'ERROR':
                        break
        return status

from testrepo.common.testfixtures.dnsaas import DomainFixture
from ccengine.domain.types import DnsaasAsyncStatusTypes as DelStatus
import time
import json


class CleanUpTest(DomainFixture):

    def test_cleanup(self):
        api_response = self.domain_provider.client.list_all_domain()

        self.assertTrue(api_response.ok, "Components get\
             domain failed with error:{0} and status code {1}: \n {2}"
             .format(api_response.reason, api_response.status_code,
                     json.loads(api_response.content)))
        self.data = []
        if api_response.entity.totalEntries != 0:
            for i in range(api_response.entity.totalEntries):
                self.domain_id = api_response.entity[i].id
                self.data.append(api_response.entity[i].id)
                api_responsedel = self.domain_provider.client.\
                delete_domain(self.domain_id)
                self.assertEquals(api_responsedel.status_code, 202)
                self.assertTrue(api_response.ok, "Components Delete failed \
                with error:{0} and status code {1}: \n {2}" \
                .format(api_responsedel.reason, api_responsedel.status_code,
                json.loads(api_responsedel.content)))
                time.sleep(1)
                callbackUrl = api_responsedel.entity.callbackUrl
                api_responsecallback = self.domain_provider.client.\
                    call_backUrl(callbackUrl)
                self.assertEqual(api_responsecallback.status_code, 200)
                status = api_responsecallback.entity.status
                while status != 'COMPLETED':
                    time.sleep(5)
                    api_responsecallback = self.domain_provider.client.\
                    call_backUrl(callbackUrl)
                    status = api_responsecallback.entity.status
                    if status == "ERROR":
                        break
            for dat in self.data:
                api_responsedomain = self.domain_provider.client.\
                list_domain_details(dat)
                self.assertEquals(api_responsedomain.status_code, 404)
        else:
            self.fixture_log.info("No Domains Present: {0}" \
                                  .format(api_response.entity))




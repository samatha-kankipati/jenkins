from testrepo.common.testfixtures.dnsaas import DomainFixture
import ccengine.common.tools.datagen as datagen
import time
import json


class SmokeTest(DomainFixture):

    def test_domain_crud(self):
        name = self.name
        emailAddress = self.emailAddress
        ttl = self.ttl
        comment = self.comment
        name_list = self.name_list
        subname_list = self.subname_list
        type_list = self.type_list
        data_list = self.data_list
        ttl_list = self.ttl_list
        comment_list = self.comment_list

        api_response = self.domain_provider.client.\
            create_domain(name=name, emailAddress=emailAddress, ttl=ttl,
                          comment=comment, name_list=name_list,
                          subname_list=subname_list, type_list=type_list,
                          data_list=data_list, ttl_list=ttl_list,
                          comment_list=comment_list)
        callback = self.domain_provider.\
            test_wait_for_status(api_response)
        self.assertEquals(callback, 'COMPLETED')
        errStr = " Create Domain call  failed with error: \
            {0} and status code {1}: \n '{2}"
        self.assertEquals(api_response.status_code, 202,
                         errStr.format(api_response.reason,
                                       api_response.status_code,
                                       json.loads(api_response.content)))
        api_response = self.domain_provider.client.list_all_domain()
        self.assertEquals(api_response.status_code, 200)
        errStr = " Create Domain call  failed with error: \
            {0} and status code {1}: \n '{2}"
        self.assertEquals(api_response.status_code, 200,
                          errStr.format(api_response.reason,
                                        api_response.status_code,
                                        json.loads(api_response.content)))
        self.data = []
        self.namedomain = []
        for i in range(len(api_response.entity)):

            temp1 = api_response.entity[i]
            self.nametemp = temp1.name
            self.domain_id = api_response.entity[i].id
            self.data.append(api_response.entity[i].id)
            self.namedomain.append(api_response.entity[i].name)

            api_responsedomain = self.domain_provider.client.\
                list_domain_id(self.domain_id)
            errStr = " Components get domain with an id failed with error: \
            {0} and status code {1}: \n '{2}"
            self.assertEquals(api_responsedomain.status_code, 200,
                              errStr.format(api_response.reason,
                                            api_response.status_code,
                                            json.loads(api_response.content)))

            api_responsedomain = self.domain_provider.client.\
                list_domain_details(self.domain_id)
            errStr = " Components get domain detail failed with error: \
            {0} and status code {1}: \n '{2}"
            self.assertEquals(api_responsedomain.status_code, 200,
                              errStr.format(api_response.reason,
                                            api_response.status_code,
                                            json.loads(api_response.content)))

            api_responsedomain = self.domain_provider.client.\
                list_domain_name(self.nametemp)
            errStr = " Components get domain by name failed with error: \
            {0} and status code {1}: \n '{2}"
            self.assertEquals(api_responsedomain.status_code, 200,
                errStr.format(api_response.reason,
                              api_response.status_code,
                              json.loads(api_response.content)))

        pdomain_id = min(self.data)
        comment_update = 'This an Updated comment'
        up_emailAddress = 'mailupdate@whoisthis.com'
        ttl = 3600
        api_responsedomain = self.domain_provider.client.\
            update_domain(pdomain_id, up_emailAddress, ttl, comment_update)

        callback = self.domain_provider.\
            test_wait_for_status(api_responsedomain)
        self.assertEquals(callback, 'COMPLETED')
        errStr = " Update Domain call  failed with error: \
            {0} and status code {1}: \n '{2}"
        self.assertEquals(api_responsedomain.status_code, 202,
            errStr.format(api_response.reason,
                          api_response.status_code,
                          json.loads(api_response.content)))

        api_responsedomain = self.domain_provider.client.\
            export_domain(pdomain_id)
        errStr = " Components export domain failed with error: \
            {0} and status code {1}: \n '{2}"
        self.assertEquals(api_responsedomain.status_code, 202,
            errStr.format(api_response.reason,
                          api_response.status_code,
                          json.loads(api_response.content)))
        callback = self.domain_provider.\
            test_wait_for_status(api_responsedomain)
        self.assertEquals(callback, 'COMPLETED')

        cleanup = self.domain_provider.test_cleanup()

    def test_import_domain(self):
        domainName = datagen.random_string('importdomain')
        import_response = self.domain_provider.client.import_domain(domainName)

        self.assertEquals(import_response.status_code, 202)
        callbackUrl = import_response.entity.callbackUrl
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
        cleanup = self.domain_provider.test_cleanup()

    def test_limits(self):
        api_response = self.domain_provider.client.list_all_limits()

        errStr = " Components get limits failed with error: \
            {0} and status code {1}: \n '{2}"
        self.assertEquals(api_response.status_code, 200,
            errStr.format(api_response.reason,
                          api_response.status_code,
                          json.loads(api_response.content)))

    def test_limits_types(self):
        api_response = self.domain_provider.client.list_limits_types()

        errStr = " Components get limits types failed with error: \
            {0} and status code {1}: \n '{2}"
        self.assertEquals(api_response.status_code, 200,
            errStr.format(api_response.reason,
                          api_response.status_code,
                          json.loads(api_response.content)))

    def test_limits_rate_limit(self):
        api_response = self.domain_provider.client.list_limits_rate_limit()

        errStr = " Components get rate limits failed with error: \
            {0} and status code {1}: \n '{2}"
        self.assertEquals(api_response.status_code, 200,
            errStr.format(api_response.reason,
                          api_response.status_code,
                          json.loads(api_response.content)))

    def test_limits_rate_domain_limit(self):
        api_response = self.domain_provider.client.list_domain_limit()

        errStr = " Components get domain domain limits failed with error: \
            {0} and status code {1}: \n '{2}"
        self.assertEquals(api_response.status_code, 200,
            errStr.format(api_response.reason,
                          api_response.status_code,
                          json.loads(api_response.content)))

    def test_limits_domain_limit(self):
        api_response = self.domain_provider.client.list_domain_record_limits()

        errStr = " Components get domain record limits failed with error: \
            {0} and status code {1}: \n '{2}"
        self.assertEquals(api_response.status_code, 200,
            errStr.format(api_response.reason,
                          api_response.status_code,
                          json.loads(api_response.content)))
 
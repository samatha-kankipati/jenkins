from testrepo.common.testfixtures.dnsaas import DomainFixture
import ccengine.common.tools.datagen as datagen
import time
import json


class SmokeTest(DomainFixture):

    def test_clone_domain(self):
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

        api_response = self.domain_provider.client.create_domain(name=name,
            emailAddress=emailAddress, ttl=ttl, comment=comment,
            name_list=name_list, subname_list=subname_list,
            type_list=type_list, data_list=data_list, ttl_list=ttl_list,
            comment_list=comment_list)
        self.assertEquals(api_response.status_code, 202)

        callback = self.domain_provider.\
            test_wait_for_status(api_response)
        self.assertEquals(callback, 'COMPLETED')
        api_response = self.domain_provider.client.list_all_domain()
        self.assertTrue(api_response.ok,
                        "Components create domain failed with error: {0}\
                         and status code {1}".format(api_response.reason,
                                                     api_response.status_code))

        data = []
        for i in range(len(api_response.entity)):
            data.append(api_response.entity[i].id)

        domain_id = min(data)
        clone_name = 'jijoe.com'

        api_responsedomain = self.domain_provider.client.\
            clone_domain(domain_id, clone_name)
        self.assertEquals(api_responsedomain.status_code, 202)
        callback = self.domain_provider.\
            test_wait_for_status(api_responsedomain)
        self.assertEquals(callback, 'COMPLETED')

        api_response = self.domain_provider.client.list_all_domain()
        errStr = "Components list domain failed with error: {0} \
            and status code {1}: \n"
        self.assertTrue(api_response.ok,
                        errStr.format(api_response.reason,
                                      api_response.status_code))

        namedomain = []
        for i in range(len(api_response.entity)):
            namedomain.append(api_response.entity[i].name)
        matching = [s for s in namedomain if "jijoe.com" in s]
        self.assertEquals(len(matching), 3)
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

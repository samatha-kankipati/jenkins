from testrepo.common.testfixtures.dnsaas import PtrFixtureLbaas
import json


class SmokeTest(PtrFixtureLbaas):

    @classmethod
    def setUpClass(cls):
        super(SmokeTest, cls).setUpClass()
        cls.name = cls.config.dnsaas.name
        cls.type = cls.config.dnsaas.type
        cls.rel = cls.config.dnsaas.rel
        cls.href = cls.config.dnsaas.href

    def test_ptr_crud(self):
        data = []
        name = self.name
        rel_id = self.lb_id
        data.append(self.lb_ipv4)
        data.append(self.lb_ipv6)

        type = self.type
        href = '{0}/{1}' .format(self.href, rel_id)
        rel = self.rel
        api_response = self.ptr_provider.client.delete_ptr_lb(rel_id)

        callback = self.ptr_provider.\
            test_wait_for_status(api_response)
        self.assertEquals(callback, 'COMPLETED')
        errStr = " delete call  failed with error: \
            {0} and status code {1}: \n '{2}"
        self.assertEquals(api_response.status_code, 202,
                          errStr.format(api_response.reason,
                                        api_response.status_code,
                                        json.loads(api_response.content)))
        api_response = self.ptr_provider.client.list_ptr_lb(rel_id)
        self.assertEquals(api_response.status_code, 404)
        for datarecord in data:
            if not datarecord:
                self.provider_log.info('The IPV4 is missing')
            api_response = self.ptr_provider.client.\
                create_ptr(name_list=[name],
                           type_list=[type],
                           data_list=[datarecord],
                           link={'rel': rel, 'href': href})
            self.assertEquals(api_response.status_code, 202)
            callback = self.ptr_provider.\
            test_wait_for_status(api_response)
            self.assertEquals(callback, 'COMPLETED')
        api_response = self.ptr_provider.client.list_ptr_lb(rel_id)

        errStr = "Components get failed with error: \
            {0} and status code {1}: \n '{2}"
        self.assertEquals(api_response.status_code, 200,
                          errStr.format(api_response.reason,
                                        api_response.status_code,
                                        json.loads(api_response.content)))
        recordId = []
        recordId.append(api_response.entity[0].id)
        recordId.append(api_response.entity[1].id)
        for recordIds in recordId:

            api_response = self.ptr_provider.client.list_ptr_info_lb(rel_id,
                                                                     recordIds)
            errStr = "Get PTR failed with error: \
                {0} and status code {1}: \n '{2}"
            self.assertTrue(api_response.ok,
                errStr.format(api_response.reason,
                              api_response.status_code,
                              json.loads(api_response.content)))

        for i in xrange(2):

            nameup = 'ptrforQE.com'
            api_response = self.ptr_provider.client.\
                update_ptr(name_list=[nameup],
                           type_list=[type],
                           data_list=[data[i]],
                           id_list=[recordId[i]],
                           link={'rel': rel, 'href': href})

            callback = self.ptr_provider.\
            test_wait_for_status(api_response)
            self.assertEquals(callback, 'COMPLETED')
            errStr = "Components Update failed with error:\
                {0} and status code {1}: \n '{2}"
            self.assertEquals(api_response.status_code, 202,
                              errStr.format(api_response.reason,
                                            api_response.status_code,
                                            json.loads(api_response.content)))
        for datarecord in data:

            api_response = self.ptr_provider.client.\
                delete_ptr_ip_lb(rel_id, datarecord)
            callback = self.ptr_provider.\
                test_wait_for_status(api_response)
            self.assertEquals(callback, 'COMPLETED')
            errStr = " delete call  failed with error: \
                {0} and status code {1}: \n '{2}"
            self.assertEquals(api_response.status_code, 202,
                              errStr.format(api_response.reason,
                                            api_response.status_code,
                                            json.loads(api_response.content)))

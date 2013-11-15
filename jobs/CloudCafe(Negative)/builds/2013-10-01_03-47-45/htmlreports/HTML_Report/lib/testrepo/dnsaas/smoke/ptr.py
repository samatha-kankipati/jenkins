from testrepo.common.testfixtures.dnsaas import PtrFixture
import json
import time 


class SmokeTest(PtrFixture):

    @classmethod
    def setUpClass(cls):
        super(SmokeTest, cls).setUpClass()
        cls.name = cls.config.dnsaas.name
        cls.type = cls.config.dnsaas.type
        cls.rel = cls.config.dnsaas.rel
        cls.href = cls.config.dnsaas.href

    def test_ptr_crud(self):

        name = self.name
        type = self.type
        data = self.data
        server_id = self.serverid
        href = '{0}/{1}' .format(self.href, server_id)
        rel = self.rel
        api_response = self.ptr_provider.client.delete_ptr_lb(server_id)
        errStr = " delete call  failed with error: \
                        {0} and status code {1}: \n '{2}"
        self.assertTrue(api_response.ok,
                        errStr.format(api_response.reason,
                                      api_response.status_code,
                                      json.loads(api_response.content)))
        callback = self.ptr_provider.\
            test_wait_for_status(api_response)
        self.assertEquals(callback, 'COMPLETED')
        api_response = self.ptr_provider.client.list_ptr_lb(server_id)
        self.assertEquals(api_response.status_code, 404)

        api_response = self.ptr_provider.client.create_ptr(name_list=[name],
                                                           type_list=[type],
                                                           data_list=[data],
                                                           link={'rel': rel,
                                                                 'href': href})
        self.assertEquals(api_response.status_code, 202)
        callback = self.ptr_provider.\
            test_wait_for_status(api_response)
        self.assertEquals(callback, 'COMPLETED')

        api_response = self.ptr_provider.client.list_ptr_lb(server_id)
        errStr = "Components get failed with error: \
                        {0} and status code {1}: \n '{2}"
        self.assertEquals(api_response.status_code, 202,
            errStr.format(api_response.reason,
                          api_response.status_code,
                          json.loads(api_response.content)))
        recordId = api_response.entity[0].id
        api_response = self.ptr_provider.client.list_ptr_info_lb(
            ptr_id=recordId, rel_id=server_id)
        errStr = "Get PTR failed with error: \
                        {0} and status code {1}: \n '{2}"
        self.assertTrue(api_response.ok,
                        errStr.format(api_response.reason,
                                      api_response.status_code,
                                      json.loads(api_response.content)))
        nameup = 'ptrforQE.com'
        api_response = self.ptr_provider.client.update_ptr(name_list=[nameup],
                                                           type_list=[type],
                                                           data_list=[data],
                                                           id_list=[recordId],
                                                           link={'rel': rel,
                                                                 'href': href})
        self.assertEquals(api_response.status_code, 202)
        callback = self.ptr_provider.\
            test_wait_for_status(api_response)
        self.assertEquals(callback, 'COMPLETED')

        api_response = self.ptr_provider.client.\
            delete_ptr_ip_lb(rel_id=server_id, data=data)
        errStr = " delete call  failed with error: \
            {0} and status code {1}: \n '{2}"
        self.assertTrue(api_response.ok,
                        errStr.format(api_response.reason,
                                      api_response.status_code,
                                      json.loads(api_response.content)))

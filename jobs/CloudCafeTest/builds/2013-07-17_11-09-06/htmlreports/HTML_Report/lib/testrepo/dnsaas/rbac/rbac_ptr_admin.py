from testrepo.common.testfixtures.dnsaas\
    import IdentityAdminFixture
from testrepo.common.testfixtures.dnsaas import PtrFixtureLbaas
import json


class SmokeTest(IdentityAdminFixture, PtrFixtureLbaas):

    @classmethod
    def setUpClass(cls):
        super(SmokeTest, cls).setUpClass()
        cls.name = cls.config.dnsaas.name
        cls.type = cls.config.dnsaas.type
        cls.rel = cls.config.dnsaas.rel
        cls.href = cls.config.dnsaas.href

    def test_ptr_crud_admin(self):
        data = []
        name = self.name
        rel_id = self.lb_id
        data.append(self.lb_ipv4)
        data.append(self.lb_ipv6)

        type = self.type
        href = '{0}/{1}'.format(self.href, rel_id)
        rel = self.rel
        api_response = self.client_admin_ptr.delete_ptr_lb(rel_id)
        self.assertTrue(api_response.ok, " delete call failed with error: \
                {0} and status code {1}" \
                .format(api_response.reason, api_response.status_code))
        api_response = self.client_creator_ptr.delete_ptr_lb(rel_id)
        self.assertEquals(api_response.status_code, 202)

        api_response = self.client_observer_ptr.delete_ptr_lb(rel_id)
        self.assertEquals(api_response.status_code, 405)

        api_response = self.client_admin_ptr.list_ptr_lb(rel_id)
        self.assertEquals(api_response.status_code, 404)
        for datarecord in data:
            if not datarecord:
                self.provider_log.info('The IPV4 is missing')
            api_response = self.client_creator_ptr.create_ptr(name_list=[name],
                            type_list=[type], data_list=[datarecord],
                            link={'rel': rel, 'href': href})
            self.assertEquals(api_response.status_code, 202)
            api_response = self.client_observer_ptr.create_ptr(\
                            name_list=[name],
                            type_list=[type], data_list=[datarecord],
                            link={'rel': rel, 'href': href})
            self.assertEquals(api_response.status_code, 405)

        api_response = self.client_admin_ptr.list_ptr_lb(rel_id)
        self.assertEquals(api_response.status_code, 200)

        api_response = self.client_creator_ptr.list_ptr_lb(rel_id)
        self.assertEquals(api_response.status_code, 200)

        api_response = self.client_observer_ptr.list_ptr_lb(rel_id)
        self.assertEquals(api_response.status_code, 200)

        recordId = []
        recordId.append(api_response.entity[0].id)
        recordId.append(api_response.entity[1].id)
        for recordIds in recordId:

            api_response = self.client_admin_ptr.list_ptr_info_lb(rel_id,
                                                                     recordIds)
            self.assertTrue(api_response.ok, " Get PTR failed with error: \
                {0} and status code {1}" \
                .format(api_response.reason, api_response.status_code))
            api_response = self.client_admin_ptr.list_ptr_info_lb(rel_id,
                                                                     recordIds)
            self.assertEquals(api_response.status_code, 200)
            api_response = self.client_admin_ptr.list_ptr_info_lb(rel_id,
                                                                     recordIds)
            self.assertEquals(api_response.status_code, 200)

        for i in xrange(2):

            nameup = 'ptrforQE.com'
            api_response = self.client_admin_ptr.update_ptr(name_list=[nameup],
            type_list=[type], data_list=[data[i]], id_list=[recordId[i]],
            link={'rel': rel, 'href': href})
            self.assertEquals(api_response.status_code, 202)

            nameup = 'ptrforQEcreaotor.com'
            api_response = self.client_creator_ptr.\
                update_ptr(name_list=[nameup], type_list=[type],
                            data_list=[data[i]], id_list=[recordId[i]],
                            link={'rel': rel, 'href': href})
            self.assertEquals(api_response.status_code, 202)

            nameup = 'ptrforQEcreaotor.com'
            api_response = self.client_observer_ptr.\
                update_ptr(name_list=[nameup], type_list=[type],
                            data_list=[data[i]], id_list=[recordId[i]],
                            link={'rel': rel, 'href': href})
            self.assertEquals(api_response.status_code, 405)

        for datarecord in data:

            api_response = self.client_creator_ptr.delete_ptr_ip_lb(rel_id,\
                                                                datarecord)
            self.assertEquals(api_response.status_code, 405)
            api_response = self.client_observer_ptr.delete_ptr_ip_lb(rel_id,\
                                                                datarecord)
            self.assertEquals(api_response.status_code, 405)
            api_response = self.client_admin_ptr.delete_ptr_ip_lb(rel_id,\
                                                                datarecord)
            self.assertTrue(api_response.ok, " delete call failed with error: \
                {0} and status code {1}" \
                .format(api_response.reason, api_response.status_code))

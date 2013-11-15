from testrepo.common.testfixtures.compute import DnsaasIntegrationFixture
import time
import json
from ccengine.common.exceptions.compute import ItemNotFound
from ccengine.common.decorators import attr


class CreateServerTest(DnsaasIntegrationFixture):

    @classmethod
    def setUpClass(cls):
        super(CreateServerTest, cls).setUpClass()
        # Creation of 1 servers needed for the tests
        active_server_response = cls.compute_provider.create_active_server()
        cls.server = active_server_response.entity
        cls.resources.add(cls.server.id,
                          cls.servers_client.delete_server)
        # Main dnsaas params
        cls.name = cls.config.dnsaas.name
        cls.type = cls.config.dnsaas.type
        cls.rel = cls.config.dnsaas.rel
        cls.href = cls.config.dnsaas.href
    
    @attr(type='smoke', net='no')
    def test_automated_ptr_deletion_after_server_delete(self):
        data = []
        name = self.name
        rel_id = self.server.id
        data.append(self.server.addresses.public.ipv4)
        data.append(self.server.addresses.public.ipv6)
        type = self.type
        href = '{0}/{1}'.format(self.href, rel_id)
        rel = self.rel

        with self.assertRaises(ItemNotFound):
            api_response = self.ptr_provider.client.list_ptr_lb(rel_id)

        for datarecord in data:
            if not datarecord:
                self.provider_log.info('The IPV4 is missing')
            api_response = self.ptr_provider.client.create_ptr(
                name_list=[name],
                type_list=[type],
                data_list=[datarecord],
                link={'rel': rel,
                'href': href})
            self.assertEquals(api_response.status_code, 202)
            time.sleep(float(self.config.dnsaas.ptr_timeout))

        api_response = self.ptr_provider.client.list_ptr_lb(rel_id)
        self.assertTrue(api_response.ok, "Components get failed with error: \
            '{0}' and status code '{1}': \n '{2}'" \
            .format(api_response.reason, api_response.status_code,
                json.loads(api_response.content)))

        del_server = self.compute_provider.delete_servers(
            server_list=[self.server.id])
        self.assertEquals(del_server, [])
        time.sleep(float(self.config.dnsaas.ptr_timeout))
        with self.assertRaises(ItemNotFound):
            api_response = self.ptr_provider.client.list_ptr_lb(rel_id)

    @attr(type='negative', net='no')
    def test_duplicated_ptr_records(self):
        """Duplicate ip4 PTR records should not exist """
        '''
                @TODO:  Work in progress
        '''
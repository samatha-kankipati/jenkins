import logging
from ccengine.common.decorators import attr
from testrepo.common.testfixtures.designate import DesignateFixture


class DomainTest(DesignateFixture):

    @attr('smoke', 'positive')
    def test_nslookup(self):
        nslookup = self.designate_provider.\
            ssh_connector.exec_shell_command('nslookup esmesolutions.com')
        for ns in nslookup:
            isinstance(ns, basestring)
            if "Address: 50.56.52.206" in ns:
                logging.info("nslookup command")

    @attr('smoke', 'positive')
    def test_dig(self):
        digs = self.designate_provider.ssh_connector.\
            exec_shell_command('dig @ns1.stabletransit.com esmesolutions.com')
        for dig in digs:
            if "SERVER: 69.20.95.4#53(69.20.95.4)" in dig:
                logging.info("dig command")
                logging.info(dig)

    @attr('smoke', 'positive')
    def test_list_domains_get_domain_by_id(self):

            api_response = self.designate_provider.domain_client.list_domains()
            errStr = "List call  failed with error: \
                {0} and status code {1}"
            self.assertEquals(api_response.status_code, 200,
                              errStr.format(api_response.reason,
                                            api_response.status_code))
            domain_list = []
            for i in range(len(api_response.entity)):
                domain_id = api_response.entity[i].id
                domain_list.append(api_response.entity[i].id)
                api_responsedomain = self.designate_provider.\
                    domain_client.get_domain(domain_id)
                errStr = " Components get domain with an id \
                    failed with error: {0} and status code {1}"
                self.assertEquals(api_responsedomain.status_code, 200,
                                  errStr.format(api_response.reason,
                                                api_response.status_code))

    @attr('smoke', 'positive')
    def test_update_domain(self):

            api_response = self.designate_provider.domain_client.list_domains()
            errStr = "List call  failed with error: \
                {0} and status code {1}"
            self.assertEquals(api_response.status_code, 200,
                              errStr.format(api_response.reason,
                                            api_response.status_code))
            domain_list = []
            for i in range(len(api_response.entity)):
                name = api_response.entity[i].name
                domain_id = api_response.entity[i].id
                domain_list.append(api_response.entity[i].id)
            up_emailAddress = 'mailupdate@updated.com'
            ttl = 3600
            api_responsedomain = self.designate_provider.domain_client.\
                update_domain(domain_id=domain_id, name=name,
                              email=up_emailAddress, ttl=ttl)
            errStr = " Update Domain call  failed with error: \
                {0} and status code {1}"
            self.assertEquals(api_responsedomain.status_code, 200,
                              errStr.format(api_response.reason,
                                            api_response.status_code))

    @attr('smoke', 'positive')
    def test_create_domain_delete_domain(self):

        random = 'designate'
        tempdomain = '{0}.com'.format(random)
        name = '{0}.'.format(tempdomain)
        email = 'mail@{0}'.format(tempdomain)
        ttl = 3600
        api_response = self.designate_provider.domain_client.\
            create_domain(name=name, email=email, ttl=ttl)
        errStr = " Create Domain call  failed with error: \
            {0} and status code {1}"
        self.assertEquals(api_response.status_code, 200,
                          errStr.format(api_response.reason,
                                        api_response.status_code))
        domain_id = api_response.entity[0].id
        logging.info(domain_id)
        api_response_delete = self.designate_provider.\
            domain_client.delete_domain(domain_id)
        errStr = " Components delete domain failed with error: \
                {0} and status code {1}"
        self.assertEquals(api_response_delete.status_code, 200,
                          errStr.format(api_response.reason,
                                        api_response.status_code))
        api_responsedomain = self.designate_provider.\
            domain_client.get_domain(domain_id)
        errStr = " Components get domain with after delete failed with error: \
            {0} and status code {1}"
        self.assertEquals(api_responsedomain.status_code, 404,
                          errStr.format(api_response.reason,
                                        api_response.status_code))

    @attr('smoke', 'positive')
    def test_create_update_delete_domain(self):

            random = 'designatecrud'
            tempdomain = '{0}.com'.format(random)
            name = '{0}.'.format(tempdomain)
            email = 'mail@{0}'.format(tempdomain)
            ttl = 3600
            api_response = self.designate_provider.domain_client.\
                create_domain(name=name, email=email, ttl=ttl)
            errStr = " Create Domain call  failed with error: \
                {0} and status code {1}"
            self.assertEquals(api_response.status_code, 200,
                              errStr.format(api_response.reason,
                                            api_response.status_code))
            domain_id = api_response.entity[0].id
            logging.info(domain_id)
            up_emailAddress = 'mailupdate@updateagaindomain.com'
            ttl = 3600
            api_responsedomain = self.designate_provider.domain_client.\
                update_domain(domain_id=domain_id,
                              name=name,
                              email=up_emailAddress,
                              ttl=ttl)
            errStr = " Update Domain call  failed with error: \
                {0} and status code {1}"
            self.assertEquals(api_responsedomain.status_code, 200,
                              errStr.format(api_response.reason,
                                            api_response.status_code))
            api_response_delete = self.designate_provider.\
                domain_client.delete_domain(domain_id)
            errStr = " Components delete domain failed with error: \
                    {0} and status code {1}"
            self.assertEquals(api_response_delete.status_code, 200,
                              errStr.format(api_response.reason,
                                            api_response.status_code))
            api_responsedomain = self.designate_provider.\
                domain_client.get_domain(domain_id)
            errStr = " Components get domain with after delete\
                failed with error: {0} and status code {1}"
            self.assertEquals(api_responsedomain.status_code, 404,
                              errStr.format(api_response.reason,
                                            api_response.status_code))

    @attr('smoke', 'positive')
    def test_list_sever_on_which_domain_exists(self):

            api_response = self.designate_provider.domain_client.list_domains()
            errStr = "List call  failed with error: \
                {0} and status code {1}"
            self.assertEquals(api_response.status_code, 200,
                              errStr.format(api_response.reason,
                                            api_response.status_code))
            domain_list = []
            for i in range(len(api_response.entity)):
                domain_id = api_response.entity[i].id
                domain_list.append(api_response.entity[i].id)

                api_responsedomain = self.designate_provider.\
                    domain_client.list_domain_servers(domain_id)
                errStr = " Components server on which domain exists'\
                     'with an id failed with error: \
                {0} and status code {1}"
                self.assertEquals(api_responsedomain.status_code, 200,
                                  errStr.format(api_response.reason,
                                                api_response.status_code))

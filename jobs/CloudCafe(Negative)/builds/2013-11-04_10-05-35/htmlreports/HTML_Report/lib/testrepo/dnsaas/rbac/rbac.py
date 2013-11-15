from testrepo.common.testfixtures.dnsaas\
        import IdentityAdminFixture
from ccengine.clients.identity.v2_0.rax_auth_api import IdentityClient
from ccengine.common.tools.datagen import rand_name
from ccengine.providers.identity.identity_v2_0_api import IdentityAPIProvider
import ccengine.common.tools.datagen as datagen
import time


class AdminRolesTest(IdentityAdminFixture):

    COM = '.com'
    MAIL = 'mail@'
    SUB1 = 'sub1.'
    SUB2 = 'sub2.'

    def test_domain_crud_admin(self):
        self.random = datagen.random_string('whoisthis')
        self.name = '{0}{1}'.format(self.random, self.COM)
        self.emailAddress = '{0}{1}'.format(self.MAIL, self.name)
        self.ttl = 3600
        self.comment = 'creating a Domain'
        self.name_list = [self.name, self.name]
        self.subname_list = ['{0}{1}'.format(self.SUB1, self.name),\
                                '{0}{1}'.format(self.SUB2, self.name)]
        self.type_list = ['A', 'A']
        self.data_list = ['192.0.2.17', '192.0.2.18']
        self.ttl_list = [3600, 5400]
        self.comment_list = ['just do it', 'just do it again']

        api_response_admin = self.clientadmin.create_domain(name=self.name,
                emailAddress=self.emailAddress, ttl=self.ttl,
                comment=self.comment, name_list=self.name_list,
                subname_list=self.subname_list,
                type_list=self.type_list, data_list=self.data_list,
                ttl_list=self.ttl_list, comment_list=self.comment_list)
        self.assertEquals(api_response_admin.status_code, 202)

        api_response_observer = self.clientobserver.create_domain(name=self.name,
                emailAddress=self.emailAddress, ttl=self.ttl,
                comment=self.comment, name_list=self.name_list,
                subname_list=self.subname_list,
                type_list=self.type_list, data_list=self.data_list,
                ttl_list=self.ttl_list, comment_list=self.comment_list)
        self.assertEquals(api_response_observer.status_code, 405)


        time.sleep(20)
        api_response_admin = self.clientadmin.list_all_domain()
        self.assertEquals(api_response_admin.status_code, 200)

        api_response_observer = self.clientobserver.list_all_domain()
        self.assertEquals(api_response_observer.status_code, 200)

        self.data = []
        self.namedomain = []
        for i in range(len(api_response_admin.entity)):

            temp1 = api_response_admin.entity[i]
            self.nametemp = temp1.name
            self.domain_id = api_response_admin.entity[i].id
            self.data.append(api_response_admin.entity[i].id)
            self.namedomain.append(api_response_admin.entity[i].name)

            api_responsedomain = \
                self.clientadmin.list_domain_id(self.domain_id)
            self.assertTrue(api_responsedomain.ok)

            api_responsedomain = \
                self.clientobserver.list_domain_id(self.domain_id)
            self.assertTrue(api_responsedomain.ok)

            api_responsedomain = self.clientadmin.\
                list_domain_details(self.domain_id)
            self.assertTrue(api_responsedomain.ok)

            api_responsedomain = self.clientobserver.\
                list_domain_details(self.domain_id)
            self.assertTrue(api_responsedomain.ok)

            api_responsedomain = self.clientadmin.\
            list_domain_name(self.nametemp)
            self.assertTrue(api_responsedomain.ok)

            api_responsedomain = self.clientobserver.\
            list_domain_name(self.nametemp)
            self.assertTrue(api_responsedomain.ok)

        pdomain_id = min(self.data)
        comment_update = 'This an Updated comment'
        up_emailAddress = 'mailupdate@whoisthis.com'
        ttl = 3600
        api_responsedomain = self.clientadmin.\
        update_domain(pdomain_id, up_emailAddress, ttl, comment_update)
        self.assertTrue(api_responsedomain.ok)

        try:
            api_responsedomain = self.clientadmin.\
            update_domain(pdomain_id, up_emailAddress, ttl, comment_update)
            self.assertTrue(api_responsedomain.ok)
        except:
            pass
        api_responsedomain = self.clientadmin.\
        export_domain(pdomain_id)
        self.assertTrue(api_responsedomain.ok)

        api_responsedomain = self.clientadmin.\
        export_domain(pdomain_id)
        self.assertTrue(api_responsedomain.ok)

        callbackUrl = api_responsedomain.entity.callbackUrl

        time.sleep(20)
        api_responsecallback = self.clientadmin.\
        call_backUrl(callbackUrl)
        self.assertTrue(api_responsecallback.ok)

        api_response_cleanup = self.clientadmin.list_all_domain()

        self.assertTrue(api_response_cleanup.ok)
        self.data = []
        if api_response_cleanup.entity.totalEntries != 0:
            for i in range(api_response_cleanup.entity.totalEntries):
                self.domain_id = api_response_cleanup.entity[i].id
                self.data.append(api_response_cleanup.entity[i].id)
                api_responsedel = self.clientobserver.\
                delete_domain(self.domain_id)
                self.assertEquals(api_responsedel.status_code, 405)
                api_responsedel = self.clientadmin.\
                delete_domain(self.domain_id)
                self.assertEquals(api_responsedel.status_code, 202)

    def test_limits_admin(self):
        api_response = self.clientadmin.list_all_limits()
        self.assertEquals(api_response.status_code, 200)

    def test_limits_types_admin(self):
        api_response = self.clientadmin.list_limits_types()
        self.assertEquals(api_response.status_code, 200)

    def test_limits_rate_limit_admin(self):
        api_response = self.clientadmin.list_limits_rate_limit()
        self.assertEquals(api_response.status_code, 200)

    def test_limits_rate_domain_limit_admin(self):
        api_response = self.clientadmin.list_domain_limit()
        self.assertEquals(api_response.status_code, 200)

    def test_limits_domain_limit_admin(self):
        api_response = self.clientadmin.list_domain_record_limits()
        self.assertEquals(api_response.status_code, 200)

    def test_limits_observer(self):
        api_response = self.clientcreator.list_all_limits()
        self.assertEquals(api_response.status_code, 200)

    def test_limits_types_observer(self):
        api_response = self.clientcreator.list_limits_types()
        self.assertEquals(api_response.status_code, 200)

    def test_limits_rate_limit_observer(self):
        api_response = self.clientcreator.list_limits_rate_limit()
        self.assertEquals(api_response.status_code, 200)

    def test_limits_rate_domain_limit_observer(self):
        api_response = self.clientcreator.list_domain_limit()
        self.assertEquals(api_response.status_code, 200)

    def test_limits_domain_limit_observer(self):
        api_response = self.clientcreator.list_domain_record_limits()
        self.assertEquals(api_response.status_code, 200)

    def test_list_credentials(self):

        list_users = self.public_client.list_users()
        users = list_users.entity

        for user in users:
            delete_user = \
                self.public_client.delete_user(
                userId=user.id)

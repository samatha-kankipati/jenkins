from ccengine.clients.base_client import BaseMarshallingClient
from ccengine.domain.loggingaas.response.logging_response import \
    Version as RspVersion, \
    Tenant as RspTenant, \
    Producer as RspProducer, \
    Producers as RspProducers, \
    Profile as RspProfile, \
    Profiles as RspProfiles, \
    Host as RspHost, \
    Hosts as RspHosts
from ccengine.domain.loggingaas.request.logging_request import \
    Host as ReqHost, \
    Tenant as ReqTenant, \
    Producer as ReqProducer, \
    Profile as ReqProfile


class LoggingTenantClient(BaseMarshallingClient):

    def __init__(self, url, appver, tenant_id):
        super(LoggingTenantClient, self).__init__()
        self.url = url
        self.appver = appver
        self.tenant_id = tenant_id

    def get_current_version(self):
        """
        GET /
        Calls to get the version number
        """
        version_response = self.request('GET', self.url,
                                        response_entity_type=RspVersion)

        return version_response

    def create_tenant(self):
        """
        POST /{app_version}
        Creates a Tenant
        """
        url = '{0}/{1}'.format(self.url, self.appver)
        request_tenant = ReqTenant(tenant_id=self.tenant_id)
        tenant_request = self.post(url, request_entity=request_tenant)

        return tenant_request

    def get_tenant(self, tenant_url):
        """
        GET /{app_version}/{tenant_id}
        Retrieve a tenant from given url
        """
        url = '{0}{1}'.format(self.url, tenant_url)
        tenant_response = self.request('GET', url,
                                       response_entity_type=RspTenant)

        return tenant_response


class LoggingProducerClient(BaseMarshallingClient):

    def __init__(self, url, appver, tenant_id, producer_name,
                 producer_pattern, producer_durable,
                 producer_encrypted):
        super(LoggingProducerClient, self).__init__()
        self.url = url
        self.appver = appver
        self.tenant_id = tenant_id
        self.producer_name = producer_name
        self.producer_pattern = producer_pattern
        self.producer_durable = producer_durable
        self.producer_encrypted = producer_encrypted

    def _generate_producer_url(self, producer_id):
        remote_url = '{0}/{1}/{2}/producers/{3}'.format(self.url,
                                                        self.appver,
                                                        self.tenant_id,
                                                        producer_id)
        return remote_url

    def create_tenant(self):
        """
        Creates tenant dependency for producer
        """
        tenantClient = LoggingTenantClient(self.url, self.appver,
                                           self.tenant_id)
        tenantClient.create_tenant()
        return tenantClient

    def create_producer(self, prod_name=None, prod_pattern=None,
                        prod_durable=None, prod_encrypted=None,
                        create_depend=True):
        """
        POST /{app_version}/{tenant_id}/producers
        Creates a new producer on a tenant
        """
        if create_depend:
            self.create_tenant()

        # Assign optionals for testing permutations
        if prod_name is None:
            prod_name = self.producer_name
        if prod_pattern is None:
            prod_pattern = self.producer_pattern
        if prod_durable is None:
            prod_durable = self.producer_durable
        if prod_encrypted is None:
            prod_encrypted = self.producer_encrypted

        request_producer = ReqProducer(producer_name=prod_name,
                                       producer_pattern=prod_pattern,
                                       producer_durable=prod_durable,
                                       producer_encrypted=prod_encrypted)

        url = '{0}/{1}/{2}/producers'.format(self.url, self.appver,
                                             self.tenant_id)
        producer_request = self.post(url, request_entity=request_producer)

        return producer_request

    def get_producer(self, producer_id):
        """
        GET /{app_version}/{tenant_id}/producers/{producer_id}
        Retrieves a Producer on a tenant
        """
        remote_url = self._generate_producer_url(producer_id)
        response = self.request('GET', remote_url,
                                response_entity_type=RspProducer)
        return response

    def get_all_producers(self):
        """
        GET /{app_version}/{tenant_id}/producers
        Retrieves all producers on a given tenants
        """
        remote_url = '{0}/{1}/{2}/producers'.format(self.url, self.appver,
                                                    self.tenant_id)
        response = self.request('GET', remote_url,
                                response_entity_type=RspProducers)
        return response

    def delete_producer(self, producer_id):
        """
        DELETE /{app_version}/{tenant_id}/producers/{producer_id}
        Removes a producer from a tenant
        """
        remote_url = self._generate_producer_url(producer_id)
        response = self.request('DELETE', remote_url)

        return response

    def update_producer(self, producer_id, producer_obj):
        """
        PUT /{app_version}/{tenant_id}/producers/{producer_id}
        Updates a producer
        """
        remote_url = self._generate_producer_url(producer_id)
        response = self.request('PUT', remote_url, request_entity=producer_obj)
        return response


class LoggingHostClient(BaseMarshallingClient):

    def __init__(self, url, appver, tenant_id, hostname, ip_v4, ip_v6):
        super(LoggingHostClient, self).__init__()
        self.url = url
        self.appver = appver
        self.tenant_id = tenant_id
        self.hostname = hostname
        self.ip_v4 = ip_v4
        self.ip_v6 = ip_v6

    def _generate_host_url(self, host_id):
        remote_url = '{0}/{1}/{2}/hosts/{3}'.format(self.url,
                                                    self.appver,
                                                    self.tenant_id,
                                                    host_id)
        return remote_url

    def create_host(self, hostname, ip_v4, ip_v6, profile_id,
                    create_depend=True):
        """
        POST /{app_version}/{tenant_id}/hosts
        Creates a new host on a tenant
        """
        remote_url = '{0}/{1}/{2}/hosts'.format(self.url, self.appver,
                                                self.tenant_id)

        host = ReqHost(hostname, profile_id, ip_v4, ip_v6)
        response = self.request('POST', remote_url, request_entity=host)

        return response

    def get_host(self, host_id):
        """
        GET /{app_version}/{tenant_id}/hosts/{host_id}
        Retrieves a host from a tenant
        """
        remote_url = self._generate_host_url(host_id)
        response = self.request('GET', remote_url,
                                response_entity_type=RspHost)
        return response

    def get_all_hosts(self):
        """
        GET /{app_version}/{tenant_id}/hosts
        Retrieves all hosts from a tenant
        """
        remote_url = '{base}/{version}/{tenant_id}/hosts'.format(
            base=self.url,
            version=self.appver,
            tenant_id=self.tenant_id)

        response = self.request('GET', remote_url,
                                response_entity_type=RspHosts)
        return response

    def update_host(self, host_id, hostname=None, ip_v4=None, ip_v6=None,
                    profile_id=None):
        """
        PUT /{app_version}/{tenant_id}/hosts/{host_id}
        Update a single host on a tenant
        """
        remote_url = self._generate_host_url(host_id)
        host = ReqHost(hostname, profile_id, ip_v4, ip_v6)

        response = self.request('PUT', remote_url, request_entity=host)
        return response

    def delete_host(self, host_id):
        """
        DELETE /{app_version}/{tenant_id}/hosts/{host_id}
        Removes a host from a tenant
        """
        remote_url = self._generate_host_url(host_id)
        response = self.request('DELETE', remote_url)

        return response


class LoggingProfileClient(BaseMarshallingClient):

    def __init__(self, url, appver, tenant_id, producer_name, producer_pattern,
                 producer_durable, producer_encrypted, profile_name,
                 event_producer_ids):
        super(LoggingProfileClient, self).__init__()
        self.url = url
        self.appver = appver
        self.tenant_id = tenant_id
        self.producer_name = producer_name
        self.producer_pattern = producer_pattern
        self.producer_durable = producer_durable
        self.producer_encrypted = producer_encrypted
        self.profile_name = profile_name
        self.event_producer_ids = event_producer_ids

    def _generate_profile_url(self, profile_id):
        remote_url = '{0}/{1}/{2}/profiles/{3}'.format(self.url,
                                                       self.appver,
                                                       self.tenant_id,
                                                       profile_id)
        return remote_url

    def create_producer(self):
        """
        Creates dependant producer object for a profile
        """
        producerClient = LoggingProducerClient(self.url, self.appver,
                                               self.tenant_id,
                                               self.producer_name,
                                               self.producer_pattern,
                                               self.producer_durable,
                                               self.producer_encrypted)
        producerClient.create_producer()
        return producerClient

    def create_profile(self, profile_name=None, event_producer_ids=None,
                       create_depend=True):
        """
        POST /{app_version}/{tenant_id}/profiles
        Creates a profile on a tenant
        """
        if create_depend:
            self.create_producer()

        # Assign optionals for testing permutations
        if profile_name is None:
            profile_name = self.profile_name
        if event_producer_ids is None:
            event_producer_ids = self.event_producer_ids

        request_profile = ReqProfile(profile_name=profile_name,
                                     event_producer_ids=event_producer_ids)
        url = '{0}/{1}/{2}/profiles'.format(self.url, self.appver,
                                            self.tenant_id)
        profile_request = self.post(url, request_entity=request_profile)
        return profile_request

    def get_profile(self, profile_id):
        """
        GET /{app_version}/{tenant_id}/profiles/{profile_id}
        Retrieves a profile from a tenant
        """
        remote_url = self._generate_profile_url(profile_id)
        response = self.request('GET', remote_url,
                                response_entity_type=RspProfile)
        return response

    def get_all_profiles(self):
        """
        GET /{app_version}/{tenant_id}/profiles
        Retrieves all profiles from a tenant
        """
        remote_url = '{0}/{1}/{2}/profiles'.format(self.url, self.appver,
                                                   self.tenant_id)
        response = self.request('GET', remote_url,
                                response_entity_type=RspProfiles)
        return response

    def delete_profile(self, profile_id):
        """
        DELETE /{app_version}/{tenant_id}/profiles/{profile_id}
        Removes a profile from a tenant
        """
        remote_url = self._generate_profile_url(profile_id)
        response = self.request('DELETE', remote_url)

        return response

    def update_profile(self, profile_id, profile_obj):
        """
        PUT /{app_version}/{tenant_id}/profiles/{profile_id}
        Updates a profile on a tenant
        """
        remote_url = self._generate_profile_url(profile_id)
        response = self.request('PUT', remote_url, request_entity=profile_obj)
        return response

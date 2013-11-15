from ccengine.providers.base_provider import BaseProvider
from ccengine.clients.loggingaas.logging_client import \
    LoggingTenantClient, \
    LoggingProducerClient, \
    LoggingProfileClient, \
    LoggingHostClient
from ccengine.domain.loggingaas.request.logging_request import \
    Producer as ReqProducer, \
    Profile as ReqProfile


class LoggingTenantProvider(BaseProvider):

    def __init__(self, config):
        super(LoggingTenantProvider, self).__init__()
        self.config = config
        self.client = LoggingTenantClient(config.loggingaas.base_url,
                                          config.loggingaas.appver,
                                          config.loggingaas.tenant_id)

    def create_tenant(self):
        return self.client.create_tenant()

    def get_current_version(self):
        version = self.client.get_current_version()
        assert version.status_code is 200, 'response status code should be 200'
        return version.entity

    def get_tenant(self, tenant_url):
        tenant = self.client.get_tenant(tenant_url)

        return tenant.entity


class LoggingProducerProvider(BaseProvider):

    def __init__(self, config):
        super(LoggingProducerProvider, self).__init__()
        self.config = config
        self.client = LoggingProducerClient(
            config.loggingaas.base_url,
            config.loggingaas.appver,
            config.loggingaas.tenant_id,
            config.loggingaas.producer_name,
            config.loggingaas.producer_pattern,
            config.loggingaas.producer_durable,
            config.loggingaas.producer_encrypted
        )

    def create_producer(self, producer_name=None, producer_pattern=None,
                        producer_durable=None, producer_encrypted=None,
                        create_depend=True):

        return self.client.create_producer(producer_name, producer_pattern,
                                           producer_durable,
                                           producer_encrypted, create_depend)

    def get_producer(self, producer_id):
        assert producer_id is not None
        return self.client.get_producer(producer_id)

    def get_all_producers(self):
        return self.client.get_all_producers()

    def delete_producer(self, producer_id):
        assert producer_id is not None
        return self.client.delete_producer(producer_id)

    def update_producer(self, producer_id, producer_name=None,
                        producer_pattern=None,
                        producer_durable=None,
                        producer_encrypted=None):
        producer = ReqProducer()

        # Using separate ifs so we can test different permutations
        if producer_name is not None:
            producer.name = producer_name
        if producer_pattern is not None:
            producer.pattern = producer_pattern
        if producer_durable is not None:
            producer.durable = producer_durable
        if producer_encrypted is not None:
            producer.encrypted = producer_encrypted

        return self.client.update_producer(producer_id, producer)


class LoggingProfileProvider(BaseProvider):

    def __init__(self, config):
        super(LoggingProfileProvider, self).__init__()
        self.config = config
        self.client = LoggingProfileClient(
            config.loggingaas.base_url,
            config.loggingaas.appver,
            config.loggingaas.tenant_id,
            config.loggingaas.producer_name,
            config.loggingaas.producer_pattern,
            config.loggingaas.producer_durable,
            config.loggingaas.producer_encrypted,
            config.loggingaas.profile_name,
            config.loggingaas.event_producer_ids)

    def create_profile(self, profile_name=None, producer_ids=None,
                       create_depend=True):
        return self.client.create_profile(profile_name=profile_name,
                                          event_producer_ids=producer_ids,
                                          create_depend=create_depend)

    def get_profile(self, profile_id):
        assert profile_id is not None
        return self.client.get_profile(profile_id)

    def get_all_profiles(self):
        return self.client.get_all_profiles()

    def delete_profile(self, profile_id):
        assert profile_id is not None
        return self.client.delete_profile(profile_id)

    def update_profile(self, profile_id, profile_name, event_producer_ids):
        profile = ReqProfile()

        # Using separate ifs so we can test different permutations
        if profile_name is not None:
            profile.name = profile_name
        if event_producer_ids is not None:
            profile.event_producer_ids = event_producer_ids
        return self.client.update_profile(profile_id, profile)


class LoggingHostProvider(BaseProvider):

    def __init__(self, config):
        super(LoggingHostProvider, self).__init__()
        self.config = config
        self.client = LoggingHostClient(
            config.loggingaas.base_url,
            config.loggingaas.appver,
            config.loggingaas.tenant_id,
            config.loggingaas.hostname,
            config.loggingaas.ip_address_v4,
            config.loggingaas.ip_address_v6
        )

    def create_host(self, hostname, ip_v4, ip_v6, profile_id,
                    create_depend=True):
        return self.client.create_host(hostname=hostname,
                                       ip_v4=ip_v4,
                                       ip_v6=ip_v6,
                                       profile_id=profile_id,
                                       create_depend=create_depend)

    def get_host(self, host_id):
        assert host_id is not None
        return self.client.get_host(host_id)

    def get_all_hosts(self):
        return self.client.get_all_hosts()

    def update_host(self, host_id, hostname=None, ip_v4=None, ip_v6=None,
                    profile_id=None):
        return self.client.update_host(host_id=host_id,
                                       hostname=hostname,
                                       ip_v4=ip_v4,
                                       ip_v6=ip_v6,
                                       profile_id=profile_id)

    def delete_host(self, host_id):
        assert host_id is not None
        return self.client.delete_host(host_id)

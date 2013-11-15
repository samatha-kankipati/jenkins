"""
Base Classes for Logging as a Serivce Test Suites
"""
from uuid import UUID
from ccengine.providers.loggingaas.logging_provider import \
    LoggingTenantProvider, LoggingProfileProvider, \
    LoggingProducerProvider, LoggingHostProvider
from ccengine.providers.loggingaas.pairing_provider \
    import PairingProvider
from testrepo.common.testfixtures.fixtures import BaseTestFixture
from ccengine.common.resource_manager.resource_pool import ResourcePool


class BaseLoggingTestFixture(BaseTestFixture):

    @classmethod
    def setUpClass(cls):
        super(BaseLoggingTestFixture, cls).setUpClass()
        cls.tenant_provider = LoggingTenantProvider(cls.config)


class TenantFixture(BaseLoggingTestFixture):

    @classmethod
    def setUpClass(cls):
        super(TenantFixture, cls).setUpClass()
        cls.resources = ResourcePool()

        cls.provider = LoggingTenantProvider(cls.config)


class ProducerFixture(BaseLoggingTestFixture):

    @classmethod
    def setUpClass(cls):
        super(ProducerFixture, cls).setUpClass()

    def setUp(self):
        self.provider = LoggingProducerProvider(self.config)


class ProfileFixture(BaseLoggingTestFixture):

    @classmethod
    def setUpClass(cls):
        super(ProfileFixture, cls).setUpClass()

    def setUp(self):
        self.provider = LoggingProfileProvider(self.config)


class HostFixture(ProducerFixture):

    @classmethod
    def setUpClass(cls):
        super(HostFixture, cls).setUpClass()

    def setUp(self):
        self.provider = LoggingHostProvider(self.config)


class PairingFixture(BaseTestFixture):

    @classmethod
    def setUpClass(cls):
        super(PairingFixture, cls).setUpClass()

    def setUp(self):
        self.provider = PairingProvider(self.config)

    def _pair_worker(self, hostname=None, callback=None, ip_v4=None,
                     ip_v6=None, personality=None, status=None, disk_path=None,
                     disk_used=None, disk_total=None, os_type=None,
                     memory_mb=None, arch=None, cpu_cores=None,
                     load_average=None):

        response = self.provider.pair_worker(
            hostname=hostname,
            callback=callback,
            ip_v4=ip_v4,
            ip_v6=ip_v6,
            personality=personality,
            status=status,
            disk_path=disk_path,
            disk_total=disk_total,
            disk_used=disk_used,
            os_type=os_type,
            memory_mb=memory_mb,
            arch=arch,
            cpu_cores=cpu_cores,
            load_average=load_average)

        # Used to passively verify Meniscus issue #111
        self.assertEquals(202, response.status_code)

        # Checking to see if the returned uid is valid
        worker_token, worker_id = None, None
        try:
            worker_token = UUID(response.entity.worker_token)
            worker_id = UUID(response.entity.worker_id)
        except ValueError as err:
            self.fail("Invalid uid received from pairing call: {}".format(err))

        return {
            'response_object': response.entity,
            'worker_token': worker_token,
            'worker_id': worker_id
        }

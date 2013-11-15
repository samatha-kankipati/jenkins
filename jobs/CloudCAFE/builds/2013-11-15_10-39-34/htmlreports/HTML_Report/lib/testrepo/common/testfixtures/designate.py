from testrepo.common.testfixtures.fixtures import BaseTestFixture
from ccengine.providers.designate.domain_api import DesignateProvider \
    as _DesignateProvider


class DesignateFixture(BaseTestFixture):
    @classmethod
    def setUpClass(cls):
        super(DesignateFixture, cls).setUpClass()
        # init providers
        cls.designate_provider = _DesignateProvider(cls.config,
                                                    cls.fixture_log)


class RecordFixture(BaseTestFixture):
    @classmethod
    def setUpClass(cls):
        super(RecordFixture, cls).setUpClass()
        cls.designate_provider = _DesignateProvider(cls.config,
                                                    cls.fixture_log)
        random = 'designaterecordstest'
        tempdomain = '{0}.com'.format(random)
        cls.name = '{0}.'.format(tempdomain)
        cls.email = 'mail@{0}'.format(tempdomain)
        ttl = 3600

        create_domain = cls.designate_provider.domain_client.\
            create_domain(name=cls.name,
                          email=cls.email,
                          ttl=ttl)
        if not create_domain.ok:
            cls.assertClassSetupFailure('Unable to create domain in \
            setup')
        cls.domain_id = create_domain.entity[0].id

    @classmethod
    def tearDownClass(cls):
        par = cls.designate_provider.domain_client.delete_domain(cls.domain_id)
        if not par.ok:
            cls.assertClassTeardownFailure('Unable to delete domain in \
            tear down')
        super(RecordFixture, cls).tearDownClass()


class ServerFixture(BaseTestFixture):
    @classmethod
    def setUpClass(cls):
        super(ServerFixture, cls).setUpClass()
        # init providers
        cls.domain_provider = _DesignateProvider(cls.config, cls.fixture_log)

from testrepo.common.testfixtures.fixtures import BaseTestFixture
from ccengine.providers.rad.rad_api import RADAPIProvider


class RADFixture(BaseTestFixture):

    """Fixture for a RAD API test."""

    @classmethod
    def setUpClass(cls):
        super(RADFixture, cls).setUpClass()
        cls.rad_provider = RADAPIProvider(cls.config, cls.fixture_log)

    @classmethod
    def tearDownClass(cls):
        super(RADFixture, cls).tearDownClass()

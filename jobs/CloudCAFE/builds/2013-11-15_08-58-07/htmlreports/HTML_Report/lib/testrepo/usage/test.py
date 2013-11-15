from testrepo.common.testfixtures.fixtures import BaseTestFixture
from ccengine.providers.usage.usage_provider import UsageIntegrationProvider


class UsageSetupFixture(BaseTestFixture):

    @classmethod
    def setUpClass(cls):
        super(UsageSetupFixture, cls).setUpClass()
        cls.usage_provider = UsageIntegrationProvider(cls.config)

    def test_quicktest(self):
        resp = self.usage_provider.create_active_cloud_account()
        print resp
        print 'working'

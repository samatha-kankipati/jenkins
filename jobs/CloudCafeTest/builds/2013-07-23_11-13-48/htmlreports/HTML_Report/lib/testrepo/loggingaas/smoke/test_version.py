from testrepo.common.testfixtures.loggingaas import BaseLoggingTestFixture


class VersionSmokeTests(BaseLoggingTestFixture):

    @classmethod
    def setUpClass(cls):
        super(VersionSmokeTests, cls).setUpClass()

    def test_version(self):
        version_list = self.provider.get_current_version()
        self.assertGreater(len(version_list), 0, "version list is empty")
        self.assertEqual(version_list[0].v1, 'current')

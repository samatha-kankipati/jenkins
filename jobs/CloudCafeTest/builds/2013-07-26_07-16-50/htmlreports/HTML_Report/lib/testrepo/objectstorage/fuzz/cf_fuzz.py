import unittest

from testrepo.common.testfixtures.object_storage_fixture \
        import CloudFilesFixtureParameterized
from ccengine.common.loaders.base_parameterized_loader \
        import BaseParameterizedLoader
from ccengine.common.data_generators.fuzz.data_generator \
        import SecDataGeneratorString
from unittest2.suite import TestSuite


def load_tests(loader, standard_tests, pattern):
    suite = TestSuite()

    #string fuzz
    data = SecDataGeneratorString(2)
    cluster_loader = BaseParameterizedLoader(data)
    cluster_loader.addTest(CloudFilesFuzz("fuzz_container_name"))
    suite.addTest(cluster_loader.getSuite())

    return suite


class CloudFilesFuzz(CloudFilesFixtureParameterized):

    @unittest.skip('fuzzing tests should not be run by default.')
    def fuzz_container_name(self):
        response = self.client.create_container(self.fuzz_data)
        self.assertTrue(response.ok, 'Create call to Cloud Files failed.\n API'
                ' Response: %s' % response.text)
        self.client.get_container_options(self.fuzz_data)
        self.assertTrue(response.ok, 'Get options call to Cloud Files failed.'
                '\nAPI Response: %s' % response.text)
        self.client.delete_container(self.fuzz_data)
        self.assertTrue(response.ok, 'Delete call to Cloud Files failed.\n API'
                ' Response: %s' % response.text)

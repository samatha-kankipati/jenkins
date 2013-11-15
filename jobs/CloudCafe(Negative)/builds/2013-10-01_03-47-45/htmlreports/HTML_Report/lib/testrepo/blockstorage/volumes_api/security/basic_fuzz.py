import json
from unittest2.suite import TestSuite
from uuid import uuid1

from ccengine.common.loaders.base_parameterized_loader import \
                                                BaseParameterizedLoader
from ccengine.common.data_generators.fuzz.data_generator import \
                           SecDataGeneratorCount, SecDataGeneratorString
from testrepo.common.testfixtures.blockstorage import \
                                           VolumesAPI_ParameterizedFixture


def load_tests(loader, standard_tests, pattern):
    suite = TestSuite()

    data = SecDataGeneratorString(2)
    cluster_loader = BaseParameterizedLoader(data)

    cluster_loader.addTest(CinderAPIFuzzTest("fuzz_name"))
    cluster_loader.addTest(CinderAPIFuzzTest("fuzz_type"))

    suite.addTest(cluster_loader.getSuite())

    #fuzzes size with a range of numbers
    data = SecDataGeneratorCount(-1, 3)
    cluster_loader = BaseParameterizedLoader(data)
    cluster_loader.addTest(CinderAPIFuzzTest("fuzz_size"))
    suite.addTest(cluster_loader.getSuite())

    return suite


class CinderAPIFuzzTest(VolumesAPI_ParameterizedFixture):
    '''
    @summary: Cinder fuzz testing
    '''

    @classmethod
    def setUpClass(cls):
        super(CinderAPIFuzzTest, cls).setUpClass()
        cls.expected_volumes = []

    @classmethod
    def tearDown(cls):
        cls.volumes_api_provider.cleanup_volumes(cls.expected_volumes)

    def fuzz_name(self):
        api_response = self.volumes_client.create_volume(self.fuzz_data,
                                                         2, "SSD")
        self.assertTrue(api_response.ok, 'Create Volume call to '
               'CinderAPI failed. API Response: %s'
               % json.loads(api_response.content))
        actual_volume = api_response.entity
        provider = self.volumes_api_provider
        actual_volume.volume_type = \
                 provider.get_type_name_by_id(actual_volume.volume_type)
        self.assertEqual(actual_volume.display_name, self.fuzz_data,
                         "Volume not created with indicated name")
        self.assertEqual(actual_volume.size, 2,
                         "Volume not created with indicated size")
        self.expected_volumes.append(api_response.entity)

    def fuzz_type(self):
        name = "CinderFuzzTest_%s" % (uuid1().hex)
        #most of these should fail so it is asserting false
        api_response = self.volumes_client.create_volume(name, 2,
                                                         self.fuzz_data)
        self.assertFalse(api_response.ok, 'Create Volume call to Cinder'
                         'API succeeded when the type was not correct'
                         '. API Response: %s'
                         % json.loads(api_response.content))

    def fuzz_size(self):
        name = "CinderFuzzTest_%s" % (uuid1().hex)
        api_response = self.volumes_client.create_volume(name,
                self.fuzz_data, "SSD")
        self.assertTrue(api_response.ok, 'Create Volume call to Cinder'
                'API failed. API Response: %s'
                % json.loads(api_response.content))
        actual_volume = api_response.entity
        provider = self.volumes_api_provider
        actual_volume.volume_type = provider.get_type_name_by_id(
                                              actual_volume.volume_type)
        self.expected_volumes.append(api_response.entity)
        self.assertEqual(actual_volume.display_name, name,
                               "Volume not created with indicated name")
        self.assertEqual(actual_volume.size, self.fuzz_data,
                               "Volume not created with indicated size")
        self.expected_volumes.append(api_response.entity)

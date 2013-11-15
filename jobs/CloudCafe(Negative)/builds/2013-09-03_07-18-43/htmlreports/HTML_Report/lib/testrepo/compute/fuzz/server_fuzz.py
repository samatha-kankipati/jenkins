from ccengine.common.loaders.base_parameterized_loader import \
                                                        BaseParameterizedLoader
from testrepo.common.testfixtures.compute import ComputeFixtureParameterized
from unittest2.suite import TestSuite
import base64
from ccengine.domain.types import NovaServerStatusTypes
from ccengine.common.data_generators.fuzz.data_generator import \
                                                         SecDataGeneratorString


def load_tests(loader, standard_tests, pattern):
    suite = TestSuite()

    data = SecDataGeneratorString(1)
    cluster_loader = BaseParameterizedLoader(data)

    #fuzzes name and type with strings
    cluster_loader.addTest(FuzzServerTest("fuzz_name"))
    suite.addTest(cluster_loader.getSuite())

    '''
    Example how to add a test with a different data generator
    fuzzes size with a range of numbers
    data = SecDataGeneratorCount(-1,3)
    cluster_loader = BaseParameterizedLoader(data)
    cluster_loader.addTest(FuzzServerTest("fuzz_size"))
    suite.addTest(cluster_loader.getSuite())
    '''
    return suite


class FuzzServerTest(ComputeFixtureParameterized):

    @classmethod
    def setUpClass(cls):
        super(FuzzServerTest, cls).setUpClass()
        cls.created_servers = []

    @classmethod
    def tearDown(cls):
        for i in cls.created_servers:
            cls.servers_client.delete_server(i)

    def fuzz_name(self):
        provider = self.compute_provider
        file_contents = 'This is a test file.'
        personality = [{'path': '/root/.csivh', 'contents':
                            base64.b64encode(file_contents)}]
        metadata = {'meta_key_1': 'meta_value_1',
                        'meta_key_2': 'meta_value_2'}
        create_resp = self.servers_client.create_server(self.fuzz_data,
                                               self.image_ref, self.flavor_ref,
                                               personality=personality,
                                               metadata=metadata)

        self.created_servers.append(create_resp.entity.id)
        wait_response = provider.wait_for_server_status(create_resp.entity.id,
                                                  NovaServerStatusTypes.ACTIVE)
        wait_response.entity.adminPass = create_resp.entity.adminPass
        server = wait_response.entity

        '''Verify the parameters are correct in the initial response'''
        self.assertTrue(server.id is not None,
                        msg="Server id was not set in the response")
        self.assertTrue(server.adminPass is not None,
                        msg="Admin password was not set in the response")
        self.assertTrue(server.links is not None,
                        msg="Server links were not set in the response")

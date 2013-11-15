import base64
from testrepo.common.testfixtures.identity.v2_0.identity import IdentityIntegrationFixture
from ccengine.common.tools.datagen import rand_name
from ccengine.domain.types import NovaServerStatusTypes
from ccengine.common.decorators import attr

class CreateServerTest(IdentityIntegrationFixture):

    @classmethod
    def setUpClass(cls):
        super(CreateServerTest, cls).setUpClass()
        cls.name = rand_name("cctestserver")
        cls.file_contents = 'This is a test file.'
        cls.personality = [{'path': '/root/.csivh', 'contents':
                            base64.b64encode(cls.file_contents)}]
        cls.metadata = {'meta_key_1': 'meta_value_1',
                        'meta_key_2': 'meta_value_2'}
        
        cls.create_resp = cls.servers_client.create_server(cls.name, cls.image_ref, cls.flavor_ref,
                                                           personality=cls.personality,
                                                           metadata=cls.metadata)
        
        created_server = cls.create_resp.entity
        wait_response = cls.compute_provider.wait_for_server_status(created_server.id,
                                                                    NovaServerStatusTypes.ACTIVE)
        wait_response.entity.adminPass = created_server.adminPass
        cls.image = cls.images_client.get_image(cls.image_ref).entity
        cls.flavor = cls.flavors_client.get_flavor_details(cls.flavor_ref).entity
        cls.server = wait_response.entity

    @classmethod
    def tearDownClass(cls):
        super(CreateServerTest, cls).tearDownClass()

    @attr(type='smoke', net='no')
    def test_create_server_response(self):
        '''Verify the parameters are correct in the initial response'''

        self.assertTrue(self.server.id is not None,
                        msg="Server id was not set in the response")
        self.assertTrue(self.server.adminPass is not None,
                        msg="Admin password was not set in the response")
        self.assertTrue(self.server.links is not None,
                        msg="Server links were not set in the response")
        
        # Teardown and Verification
        self.del_server = self.servers_client.delete_server(self.server.id)
        self.assertEqual(204, self.del_server.status_code, 'The delete call \
                        response was: %s' % (self.del_server.status_code))

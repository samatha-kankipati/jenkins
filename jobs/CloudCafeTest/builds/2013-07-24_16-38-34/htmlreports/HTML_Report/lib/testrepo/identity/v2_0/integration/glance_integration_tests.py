import base64
from testrepo.common.testfixtures.identity.v2_0.identity import IdentityIntegrationFixture
from ccengine.common.tools.datagen import rand_name
from ccengine.domain.types import NovaServerStatusTypes
from ccengine.common.decorators import attr

class ListImagesTest(IdentityIntegrationFixture):

    @classmethod
    def setUpClass(cls):
        super(ListImagesTest, cls).setUpClass()        
        
    @classmethod
    def tearDownClass(cls):
        super(ListImagesTest, cls).tearDownClass()
    
    @attr(type='smoke', net='no')        
    def test_get_image(self):
        images = self.images_client.list_images()
        images = [image.id for image in images.entity]
        image_ref_temp = images[0]
        '''The expected image should be returned'''
        
        image_response = self.images_client.get_image(image_ref_temp)
        image = image_response.entity
        self.assertEqual(image_ref_temp, image.id, "Could not retrieve the expected image with id %s" % (image.id))
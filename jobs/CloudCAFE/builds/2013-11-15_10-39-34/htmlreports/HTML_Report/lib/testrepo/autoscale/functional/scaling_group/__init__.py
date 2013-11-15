from testrepo.common.testfixtures.autoscale import AutoscaleFixture
import unittest2 as unittest
from ccengine.common.tools.datagen import rand_name
#from ccengine.common.decorators import attr

class CreateScalingGroupTest(AutoscaleFixture):

    @classmethod
    def setUpClass(cls):
        super(CreateScalingGroupTest, cls).setUpClass()
        cls.name = rand_name("cctest_scalinggroup")
        cls.metadata = {'meta_key_1': 'meta_value_1',
                        'meta_key_2': 'meta_value_2'}
        cls.create_resp = cls.autoscale_client.create_scaling_group(cls.name, cls.cooldown,cls.min_entities,cls.max_entities,
                                                           metadata=cls.metadata)
        created_scaling_group = cls.create_resp.entity

    @classmethod
    def tearDownClass(cls):
        super(CreateScalingGroupTest, cls).tearDownClass()

   # @attr(type='smoke', net='no')
    def test_create_scaling_group_response(self):
        '''Verify the parameters are correct in the initial response'''
        self.assertTrue(self.scaling_group.id is not None,
                        msg="Server id was not set in the response")
        self.assertTrue(self.scaling_group.links is not None,
                        msg="Server links were not set in the response")
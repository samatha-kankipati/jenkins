from testrepo.common.testfixtures.compute import CreateServerFixture
import unittest2 as unittest
import base64
from ccengine.common.tools.datagen import rand_name
from ccengine.common.decorators import attr
from datetime import datetime


class CreateServerEventsTest(CreateServerFixture):

    @classmethod
    def setUpClass(cls):
        cls.name = rand_name("cctestserver")
        cls.file_contents = 'This is a test file.'
        cls.personality = [{'path': '/root/.csivh', 'contents':
                            base64.b64encode(cls.file_contents)}]
        cls.metadata = {'meta_key_1': 'meta_value_1',
                        'meta_key_2': 'meta_value_2'}
        super(CreateServerEventsTest, cls).setUpClass(name=cls.name,
                                                      personality=cls.personality,
                                                      metadata=cls.metadata)
        cls.flavor = cls.flavors_client.get_flavor_details(cls.flavor_ref).entity
        cls.image = cls.images_client.get_image(cls.image_ref).entity
        cls.server = cls.server_response.entity
        cls.server_events = cls.nova_atomhopper_provider.search_compute_events_by_attribute('instance_id',
                                                                                            cls.server.id)

    @classmethod
    def tearDownClass(cls):
        super(CreateServerEventsTest, cls).tearDownClass()

    def test_create_server_start_events_detail(self):
        '''Verify the properties of the create.start event are correct'''
        actual_events = [event for event in self.server_events if event.event_type == 'compute.instance.create.start']
        self.assertEqual(len(actual_events), 1)
        self.verify_server_event_details(self.server, self.image,
                                         self.flavor, actual_events[0])

    def test_create_server_end_events_detail(self):
        '''Verify the properties of the create.end event are correct'''
        actual_events = [event for event in self.server_events if event.event_type == 'compute.instance.create.end']
        self.assertEqual(len(actual_events), 1)
        self.verify_server_event_details(self.server, self.image,
                                         self.flavor, actual_events[0])

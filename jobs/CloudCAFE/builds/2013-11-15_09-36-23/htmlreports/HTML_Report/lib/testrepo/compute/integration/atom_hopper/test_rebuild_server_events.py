from testrepo.common.testfixtures.compute import ComputeFixture
from ccengine.domain.types import NovaServerStatusTypes, NovaServerRebootTypes
import time
from ccengine.common.tools.datagen import rand_name
from ccengine.common.tools.equality_tools import EqualityTools
from ccengine.common.exceptions.compute import Forbidden
from ccengine.common.decorators import attr
import base64


class RebuildServerEventTests(ComputeFixture):

    @classmethod
    def setUpClass(cls):
        super(RebuildServerEventTests, cls).setUpClass()
        response = cls.compute_provider.create_active_server()
        cls.server = response.entity
        response = cls.flavors_client.get_flavor_details(cls.flavor_ref)
        cls.flavor = response.entity
        cls.resources.add(cls.server.id, cls.servers_client.delete_server)
        cls.metadata = {'key': 'value'}
        cls.name = rand_name('testserver')
        file_contents = 'Test server rebuild.'
        personality = [{'path': '/etc/rebuild.txt',
                       'contents': base64.b64encode(file_contents)}]
        cls.password = 'rebuild'

        rebuild_response = cls.servers_client.rebuild(cls.server.id,
                                                      cls.image_ref_alt,
                                                      name=cls.name,
                                                      metadata=cls.metadata,
                                                      personality=personality,
                                                      admin_pass=cls.password)
        cls.server = cls.compute_provider.wait_for_server_status(cls.server.id,
                                                                 NovaServerStatusTypes.ACTIVE).entity
        cls.flavor = cls.flavors_client.get_flavor_details(cls.flavor_ref).entity
        cls.image = cls.images_client.get_image(cls.image_ref).entity
        cls.server_events = cls.nova_atomhopper_provider.search_compute_events_by_attribute('instance_id', cls.server.id)

    @classmethod
    def tearDownClass(cls):
        super(RebuildServerEventTests, cls).tearDownClass()

    def test_rebuild_server_start_events_detail(self):
        """Verify the properties of the rebuild.start event are correct"""
        actual_events = [event for event in self.server_events if event.event_type == 'compute.instance.rebuild.start']
        self.assertEqual(len(actual_events), 1)
        self.verify_server_event_details(self.server, self.image,
                                         self.flavor, actual_events[0])

    def test_rebuild_server_end_events_detail(self):
        """Verify the properties of the rebuild.end event are correct"""
        actual_events = [event for event in self.server_events if event.event_type == 'compute.instance.rebuild.end']
        self.assertEqual(len(actual_events), 1)
        self.verify_server_event_details(self.server, self.image,
                                         self.flavor, actual_events[0])

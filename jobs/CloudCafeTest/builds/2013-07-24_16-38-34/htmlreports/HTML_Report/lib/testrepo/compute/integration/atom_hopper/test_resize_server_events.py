from testrepo.common.testfixtures.compute import ResizeServerFixture
import unittest2 as unittest
import pytest
import base64
from ccengine.common.tools.datagen import rand_name
from ccengine.common.decorators import attr
from datetime import datetime


class ResizeServerEventsTest(ResizeServerFixture):

    @classmethod
    def setUpClass(cls):
        super(ResizeServerEventsTest, cls).setUpClass()
        cls.expected_launched_at = datetime.strptime(str(datetime.utcnow()), '%Y-%m-%d %H:%M:%S.%f')
        cls.flavor = cls.flavors_client.get_flavor_details(cls.flavor_ref).entity
        cls.resized_flavor = cls.flavors_client.get_flavor_details(cls.resize_flavor).entity
        cls.image = cls.images_client.get_image(cls.image_ref).entity

        # Get the actual create event details
        cls.resize_update_events = cls.nova_atomhopper_provider.search_compute_events_by_attribute("instance_id", cls.resize_server.id)
        cls.expected_events_list = cls._get_expected_events_list()

    @classmethod
    def tearDownClass(cls):
        super(ResizeServerEventsTest, cls).tearDownClass()

    @classmethod
    def _get_expected_events_list(cls):
        update_events_list = ['compute.instance.update']
        expected_events_list = ["compute.instance.exists",
                               "compute.instance.resize.prep.start",
                               "compute.instance.finish_resize.start",
                               "compute.instance.finish_resize.end",
                               "compute.instance.resize.prep.end",
                               "compute.instance.resize.start",
                               "compute.instance.resize.end"]

        expected_events_list.extend(update_events_list * 5)
        return expected_events_list

    @classmethod
    def _get_expected_update_event_content(cls):
        update_event_expected_data = [
        {'new_task_state': 'resize_migrating', 'old_state': 'active', 'old_task_state': 'resize_prep', 'state': 'active', 'state_description': 'resize_migrating'},
        {'new_task_state': 'resize_migrated', 'old_state': 'active', 'old_task_state': 'resize_migrating', 'state': 'active', 'state_description': 'resize_migrated'},
        {'new_task_state': 'resize_finish', 'old_state': 'active', 'old_task_state': 'resize_migrated', 'state': 'active', 'state_description': 'resize_finish'},
        {'new_task_state': 'resize_prep', 'old_state': 'active', 'old_task_state': 'None', 'state': 'active', 'state_description': 'resize_prep'},
        {'new_task_state': 'None', 'old_state': 'active', 'old_task_state': 'resize_finish', 'state': 'resized', 'state_description': ''}
        ]
        return update_event_expected_data

    @classmethod
    def _get_actual_update_events(cls):
        actual_update_event = []
        for event in cls.create_update_events:
            if (event.event_type == "compute.instance.update"):
                actual_update_event_contents = {'new_task_state': event.new_task_state,
                                                'old_state': event.old_state,
                                                'old_task_state': event.old_task_state,
                                                'state': event.state,
                                                'state_description': event.state_description}
                actual_update_event.append(actual_update_event_contents)
        return actual_update_event

    @attr(type="ah")
    def test_resize_server_prep_start_events_detail(self):
        """
        @summary: Verifies the compute.instance.resize.prep.start details
        @param expected_data: Contains all the expected data to be verified
        @type expected_data: Dictionary
        @param event: Contains event details (actual data) to be verified.
        @type event: Dictionary
        """
        actual_events = [event for event in self.resize_update_events if event.event_type == 'compute.instance.resize.prep.start']
        expected_events = [event for event in self.expected_events_list if event == "compute.instance.resize.prep.start"]
        self.assertEquals(len(actual_events), len(expected_events),
                          msg="Count of actual event %s did not match count of expected events %s"
                          % (actual_events, expected_events))
        resize_prep_start_event = actual_events[0]
        self.assertEqual('', resize_prep_start_event.payload.deleted_at, msg=resize_prep_start_event.event_type + ": The deleted_at field was not blank.")
        self._verify_event_common_details(resize_prep_start_event)

    @attr(type="ah")
    def test_resize_server_prep_end_events_detail(self):
        """
        @summary: Verifies the compute.instance.resize.prep.end details
        @param expected_data: Contains all the expected data to be verified
        @type expected_data: Dictionary
        @param event: Contains event details (actual data) to be verified.
        @type event: Dictionary
        """
        actual_events = [event for event in self.resize_update_events if event.event_type == 'compute.instance.resize.prep.end']
        expected_events = [event for event in self.expected_events_list if event == "compute.instance.resize.prep.end"]
        resize_prep_end_event = actual_events[0]
        self.assertEquals(len(actual_events), len(expected_events),
                         msg="Count of actual event %s did not match count of expected events %s"
                         % (actual_events, expected_events))
        self.assertEqual(str(self.resized_flavor.id), str(resize_prep_end_event.payload.new_instance_type_id), msg=resize_prep_end_event.event_type + ":The id of the flavor with which the server is resized does not match with the one found in the event.")
        self.assertEqual(self.resized_flavor.name, resize_prep_end_event.payload.new_instance_type, msg=resize_prep_end_event.event_type + "The name of the flavor with which the server is resized does not match with the one found in the event.")
    
        self.assertEqual('', resize_prep_end_event.payload.deleted_at, msg=resize_prep_end_event.event_type + ": The deleted_at field was not blank.")
        self._verify_event_common_details(resize_prep_end_event)

    @attr(type="ah")    
    def test_resize_server_start_events_detail(self):
        """
        @summary: Verifies the compute.instance.resize.start details
        @param expected_data: Contains all the expected data to be verified
        @type expected_data: Dictionary
        @param event: Contains event details (actual data) to be verified.
        @type event: Dictionary
        """
        actual_events = [event for event in self.resize_update_events if event.event_type == 'compute.instance.resize.start']
        expected_events = [event for event in self.expected_events_list if event == "compute.instance.resize.start"]
        resize_start_event = actual_events[0]
        self.assertEquals(len(actual_events), len(expected_events),
                         msg="Count of actual event %s did not match count of expected events %s"
                         % (actual_events, expected_events))
    
        self.assertEqual('', resize_start_event.payload.deleted_at, msg=resize_start_event.event_type + ": The deleted_at field was not blank.")
        self._verify_event_common_details(resize_start_event)

    @attr(type="ah")    
    def test_resize_server_end_events_detail(self):
        """
        @summary: Verifies the compute.instance.resize.end details
        @param expected_data: Contains all the expected data to be verified
        @type expected_data: Dictionary
        @param event: Contains event details (actual data) to be verified.
        @type event: Dictionary
        """
        actual_events = [event for event in self.resize_update_events if event.event_type == 'compute.instance.resize.end']
        expected_events = [event for event in self.expected_events_list if event == "compute.instance.resize.end"]
        resize_end_event = actual_events[0]
        self.assertEquals(len(actual_events), len(expected_events),
                         msg="Count of actual event %s did not match count of expected events %s"
                         % (actual_events, expected_events))
    
        self.assertEqual('', resize_end_event.payload.deleted_at, msg=resize_end_event.event_type + ": The deleted_at field was not blank.")
        self._verify_event_common_details(resize_end_event)

    @attr(type="ah")    
    def test_server_finish_resize_start_events_detail(self):
        """
        @summary: Verifies the compute.instance.finish_resize.start details
        @param expected_data: Contains all the expected data to be verified
        @type expected_data: Dictionary
        @param event: Contains event details (actual data) to be verified.
        @type event: Dictionary
        """
        actual_events = [event for event in self.resize_update_events if event.event_type == 'compute.instance.finish_resize.start']
        expected_events = [event for event in self.expected_events_list if event == "compute.instance.finish_resize.start"]
        finish_resize_start_event = actual_events[0]
        self.assertEquals(len(actual_events), len(expected_events),
                         msg="Count of actual event %s did not match count of expected events %s"
                         % (actual_events, expected_events))
    
        self.assertEqual('', finish_resize_start_event.payload.deleted_at, msg=finish_resize_start_event.event_type + ": The deleted_at field was not blank.")
        self._verify_event_common_details(finish_resize_start_event)

    @attr(type="ah")    
    def test_server_finish_resize_end_events_detail(self):
        """
        @summary: Verifies the compute.instance.finish_resize.start details
        @param expected_data: Contains all the expected data to be verified
        @type expected_data: Dictionary
        @param event: Contains event details (actual data) to be verified.
        @type event: Dictionary
        """
        actual_events = [event for event in self.resize_update_events if event.event_type == 'compute.instance.finish_resize.end']
        expected_events = [event for event in self.expected_events_list if event == "compute.instance.finish_resize.end"]
        finish_resize_end_event = actual_events[0]
        self.assertEquals(len(actual_events), len(expected_events),
                         msg="Count of actual event %s did not match count of expected events %s"
                         % (actual_events, expected_events))
    
        self.assertEqual('', finish_resize_end_event.payload.deleted_at, msg=finish_resize_end_event.event_type + ": The deleted_at field was not blank.")
        self._verify_event_common_details(finish_resize_end_event)


    #TODO Move to a compute based atomhopper provider
    def _verify_event_common_details(self, event):
        """
        @summary: Verifies the common details for all server related events
        @param event: Contains event details (actual data) to be verified.
        @type event: Dictionary
        """
        self.assertEqual(self.resize_server.tenant_id, event.payload.tenant_id, msg=event.event_type + ": The expected tenant ID does not match with the one found in the event.")
        self.assertEqual(self.resize_server.user_id, event.payload.user_id, msg=event.event_type + ": The expected user ID does not match with the one found in the event.")

        if event.event_type == "compute.instance.finish_resize.end" or event.event_type == "compute.instance.finish_resize.start":
            self.assertEqual(str(self.resized_flavor.id), str(event.payload.instance_type_id), msg=event.event_type + ":The id of the flavor with which the server is resized does not match with the one found in the event.")
            self.assertEqual(self.resized_flavor.name, event.payload.instance_type, msg=event.event_type + "The name of the flavor with which the server is resized does not match with the one found in the event.")
            self.assertEqual(str(self.resized_flavor.ram), str(event.payload.memory_mb), msg=event.event_type + ": The expected RAM size does not match with the one found in the event.")
            self.assertEqual(str(self.resized_flavor.disk), str(event.payload.disk_gb), msg=event.event_type + ": The expected Disk size does not match with the one found in the event.")

        else:
            self.assertEqual(str(self.flavor.id), str(event.payload.instance_type_id), msg=event.event_type + ": The expected Flavor ID does not match with the one found in the event.")
            self.assertEqual(self.flavor.name, event.payload.instance_type, msg=event.event_type + ": The expected Flavor name does not match with the one found in the event. server.id: %s" % (self.resize_server.id))
            self.assertEqual(str(self.flavor.ram), str(event.payload.memory_mb), msg=event.event_type + ": The expected RAM size does not match with the one found in the event.")
            self.assertEqual(str(self.flavor.disk), str(event.payload.disk_gb), msg=event.event_type + ": The expected Disk size does not match with the one found in the event.")

        self.assertEqual(self.resize_server.id, event.payload.instance_id, msg=event.event_type + ": The expected Server id does not match with the one found in the event.")
        self.assertEqual(self.resize_server.name, event.payload.display_name, msg=event.event_type + ": The expected Server name does not match with the one found in the event.")
        #TODO Put in separate method
        image_id = event.payload.image_ref_url.rsplit('/')[-1]
        self.assertEqual(self.resize_server.image.id, image_id, msg=event.event_type + ": The expected image ID does not match with the one found in the event.")
        #TODO put in separate method or use dateutils.parser
        temp = event.payload.created_at.replace('T', ' ')
        actual_create_date = datetime.strptime(temp, '%Y-%m-%d %H:%M:%S')
        temp = self.resize_server.created.replace('T', ' ').replace('Z', '')
        expected_create_date = datetime.strptime(temp, '%Y-%m-%d %H:%M:%S')
        self.assertEqual(actual_create_date, expected_create_date,
                         msg=event.event_type + ": The expected creation time for the server does not match with the one found in the event.")
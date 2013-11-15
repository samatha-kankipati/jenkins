from ccengine.domain.configuration import MiscConfig
from ccengine.providers.atomhopper import AtomHopperProvider
from ccengine.providers.compute.compute_api import ComputeAPIProvider
from testrepo.common.testfixtures.atomhopper_events_validator\
    .image_events_validator import ImageEventsValidator
from testrepo.common.testfixtures.atomhopper_events_validator\
    .instance_events_validator import InstanceEventsValidator


class EventsValidator(InstanceEventsValidator, ImageEventsValidator):
    """
    @summary: Helper to validate all Event details
    """
    update_event_content = []

    @classmethod
    def setUpClass(cls):
        super(EventsValidator, cls).setUpClass()
        cls.compute_provider = ComputeAPIProvider(cls.config, cls.fixture_log)
        cls.flavors_client = cls.compute_provider.flavors_client
        cls.tenant_id = cls.config.compute_api.tenant_id

        ah_dict = {MiscConfig.SECTION_NAME:
                   {'serializer': 'xml', 'deserializer': 'xml'}}
        ah_config = cls.config.mcp_override(ah_dict)
        nova_atom_hopper_url = "{base_url}{suffix}".format(
            base_url=ah_config.compute_api.atom_hopper_url,
            suffix='/nova/events')
        glance_atom_hopper_url = "{base_url}{suffix}".format(
            base_url=ah_config.compute_api.atom_hopper_url,
            suffix='/glance/events')
        cls.nova_atomhopper_provider = AtomHopperProvider(
            nova_atom_hopper_url, ah_config)
        cls.glance_atomhopper_provider = AtomHopperProvider(
            glance_atom_hopper_url, ah_config)

    def verify_events(self, expected_data, events):
        """
        @summary: Verify the list of events against the expected data
        @param expected_data: The data against which the event data
            will be verified.
        @type expected_data: Dictionary
        @param events: The list of events that have to be verified.
        @type events: AtomEntry List
        """
        self.update_event_content = expected_data.get(
            'update_event_expected_data')

        for event in events:
            self.verify_event(expected_data, event)

    """
    @summary: Helper to validate single Event details
    """
    def verify_event(self, expected_data, event):
        """
        @summary: Verify the list of events against the expected data
        @param expected_data: The data against which the event data
            will be verified.
        @type expected_data: Dictionary
        @param events: The list of events that have to be verified.
        @type events: AtomEntry List
        """
        verify_func_name = "verify_{0}".format(
            event.event_type.replace(".", "_"))
        getattr(self, verify_func_name)(expected_data, event)

    def verify_events_count(self, actual_event_list, expected_event_list):
        """
        @summary: Verifies actual_event_list length is equal
            to expected_event_list length
        @param expected_event_list: Contains the list of expected events
        @type expected_event_list: List
        @param actual_event_list: Contains the list of actual events
        @type actual_event_list: List
        """
        self.assertEqual(len(expected_event_list), len(actual_event_list),
                         msg="The number of expected events not returned.\n"
                         "Expected Events: {0} \nReceived Events: {1}"
                         .format(expected_event_list, actual_event_list))

    def verify_duplicate_message_ids_in_events(self, actual_events):
        """
        @summary: Find and list message_id duplicates from events
        """
        message_id_list = []
        for event in actual_events:
            message_id_list.append(event.message_id)

        # Get counts
        message_count = {}
        for message_id in message_id_list:
            if message_id in message_count:
                message_count[message_id] += 1
            else:
                message_count[message_id] = 1
        # Get duplicates
        duplicates = []
        for message_id in message_count:
            if message_count[message_id] > 1:
                duplicates.append(message_id.key())

        self.assertListEqual(duplicates, [],
                             msg="Duplicate message ids found in the events. "
                             "\nduplicates: {0}".format(duplicates))

    def get_and_verify_ah_events(self, wait_for_target_timestamp=None,
                                 wait_for_event_type=None, date_break=None,
                                 expected_data=None, expected_event_types=None,
                                 atom_hopper_feed_limit=1000,
                                 atom_hopper_pagination_limit=30,
                                 product_type='nova'):
        """
        @summary: Verifies the image object with events from atomhopper
        @param wait_for_timestamp:  Timestamp of when to start checking AH feed
            This is usually before the start of a server create or delete.
        @type wait_for_timestamp: Datetime
        @param wait_for_event_type: Event Type to wait for
        @type wait_for_event_type: String
        @param date_break:  Timestamp of when to stop looping over pages of the
             AH feed.
        @type date_break: Datetime of when to break off from reading the feed
        @param expected_data: Image dict to verify against
        @type expected_data: Dictionary
        @param expected_event_types: List of expected events in order of last
            to first of their appearance in the AtomHopper feed
        @type expected_event_types: List
        @param product_type: Specifies which ah proudct provider to use
        @type product_type: String
        """

        product_string = "{0}_atomhopper_provider".format(product_type)
        if product_type.lower() == 'nova':
            attribute = 'instance_id'
            attribute_regex = expected_data['server'].id
        elif product_type.lower() == 'glance':
            attribute = 'id'
            attribute_regex = expected_data['image'].id
        else:
            raise Exception("Invalid product type defined: {0}"
                            .format(product_type))
        ah_provider = getattr(self, product_string)

        # Wait for AH to update with entries
        if wait_for_target_timestamp:
            ah_provider.wait_for_atomhopper_timestamp(
                wait_for_target_timestamp)
        if wait_for_event_type:
            ah_provider.wait_for_atomhopper_event(
                wait_for_event_type=wait_for_event_type,
                attribute=attribute, attribute_regex=attribute_regex)

        # Get all actual events
        actual_events = ah_provider.search_compute_events_by_attribute(
            attribute=attribute, attribute_regex=attribute_regex,
            atom_hopper_feed_limit=atom_hopper_feed_limit,
            atom_hopper_pagination_limit=atom_hopper_pagination_limit,
            date_break=date_break)

        # only get events that occur after the exists since events prior to
        # that are covered in another test
        if product_type.lower() == 'nova':
            filtered_actual_events = []
            for event in actual_events:
            # remove *.verified.old from list since that can be
            # emitted at any given time after the exists
                if event.event_type == 'compute.instance.exists.verified.old':
                    continue
                filtered_actual_events.append(event)
                if event.event_type == 'compute.instance.exists':
                    break
            actual_events = filtered_actual_events

        # Log event info for debugging
        self.fixture_log.info("expected_data: {0}".format(
            expected_data))
        self.fixture_log.info("length of actual events: {0}".format(
            len(actual_events)))
        self.fixture_log.info("contents of actual events: ")
        for event in actual_events:
            self.fixture_log.info(event.event_type)
            self.fixture_log.info(event)

        # Verify actual events
        self.verify_events(expected_data, actual_events)

        # Check event counts in order
        actual_event_types = [event.event_type for event in actual_events]
        self.assertListEqual(actual_event_types, expected_event_types)
        self.verify_duplicate_message_ids_in_events(actual_events)

    def verify_compute_instance_update(self, expected_data, event):
        """
        @summary: Verifies the compute.instance.update details
        @param expected_data: Contains all the expected data to be verified
        @type expected_data: Dictionary
        @param event: Contains event details (actual data) to be verified.
        @type event: Dictionary
        """

        actual_update_event_contents = \
            {'new_task_state': event.payload.new_task_state,
             'old_state': event.payload.old_state,
             'old_task_state': event.payload.old_task_state,
             'state': event.payload.state,
             'state_description': event.payload.state_description}
        self.assertIn(actual_update_event_contents, self.update_event_content,
                      msg="{0}: Actual update event contents - {1} was not "
                      "found in {2}".format(event.event_type,
                                            actual_update_event_contents,
                                            self.update_event_content))

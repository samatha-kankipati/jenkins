'''
@summary: Base Classes for Test Suites (Collections of Test Cases)
@note: Correspondes DIRECTLY TO A unittest.TestCase
@see: http://docs.python.org/library/unittest.html#unittest.TestCase
@copyright: Copyright (c) 2013 Rackspace US, Inc.
'''
import ast

from ccengine.common.tools.datatools import \
    are_datetimestrings_equal
from ccengine.domain.compute.bandwidth.compute_bandwidth import \
    BandwidthDeltas
from ccengine.providers.compute.bandwidth_compute_validator import \
    BandwidthComputeValidatorProvider
from testrepo.common.testfixtures.fixtures import BaseTestFixture


class BandwidthComputeValidatorFixture(BaseTestFixture):
    '''
    @summary: Fixture for Bandwidth Compute Validator
    '''
    @classmethod
    def setUpClass(cls):
        super(BandwidthComputeValidatorFixture, cls).setUpClass()

        test_type = cls.config.compute_api.test_type
        region = cls.config.compute_api.region
        env_name = cls.config.compute_api.env_name
        nova_atom_hopper_url = '{0}{1}'.format(
           cls.config.compute_api.atom_hopper_url,
           cls.config.compute_api.nova_atom_hopper_url_path)

        search_param = "compute.instance.exists"
        cls.datetime_seconds_leeway = (cls.config.compute_api
                                       .datetime_seconds_leeway)

        # init providers
        cls.bandwidth_validator_provider = BandwidthComputeValidatorProvider(
            cls.config, cls.fixture_log)

        expected_data, actual_data = (cls.bandwidth_validator_provider
                                      .get_expected_and_actual_data(
                                            search_param, nova_atom_hopper_url,
                                            env_name, region, test_type))

        cls.actual_data_filtered_dict = \
            (cls.bandwidth_validator_provider
             .get_actual_data_filtered_by_expected_server_ids(expected_data,
                                                              actual_data))
        cls.expected_data_dict = \
            (cls.bandwidth_validator_provider
             .get_expected_data_in_dict_by_server_ids(expected_data))

    def verify_common_details_for_each_event(self, expected_event,
                                             actual_event):
        '''
        @summary: Verifies the common attributes for all compute events
        @param expected_event: Contains event details (expected data)
                               to be verified against.
        @type expected_event: ExistsEventQueue object
        @param actual_event: Contains Atom Hopper event details (actual data)
                             to be verified
        @type actual_event: NovaAtomEvent object
        '''

        failure = 'Expected {0} field in event to be {1}, was {2}'

        expected_and_actual_string_attributes = {
            'tenant_id': 'tenant_id',
            'user_id': 'user_id',
            'flavor_id': 'instance_type_id',
            'server_id': 'instance_id',
            'server_name': 'display_name',
            'server_status': 'state',
            'state_description': 'state_description'
            }

        # checking strings
        for expected, actual in \
            expected_and_actual_string_attributes.iteritems():
            self.check_strings(actual_event=actual_event,
                               expected_event=expected_event,
                               expected_attribute=expected,
                               actual_attribute=actual)

        image_id = actual_event.payload.image_ref_url.rsplit('/')[-1]
        if image_id != expected_event.image_id:
            msg = failure.format('image id', expected_event.image_id,
                                 image_id)
            self.fixture_log.error(msg)

        bw_diff = BandwidthDeltas(
            ast.literal_eval(expected_event.bandwidth_usage),
            actual_event.payload.bandwidth)
        msg = "Public_in: delta = {0}".format(bw_diff._public_in.delta)
        self.fixture_log.debug(msg)

        # checking datetime strings
        expected_and_actual_datetime_attributes = {
            'created_date': 'created_at',
            'launched_at': 'launched_at',
            'audit_period_beginning': 'audit_period_beginning',
            'audit_period_ending': 'audit_period_ending'
        }

        for expected, actual in \
            expected_and_actual_datetime_attributes.iteritems():
            self.check_datetime_strings(actual_event=actual_event,
                                        expected_event=expected_event,
                                        expected_attribute=expected,
                                        actual_attribute=actual)

        if expected_event.deleted_at:
            self.check_datetime_strings(actual_event=actual_event,
                                        expected_event=expected_event,
                                        expected_attribute='deleted_at',
                                        actual_attribute='deleted_at')

    def check_strings(self, actual_event, expected_event,
                      expected_attribute, actual_attribute):
        '''
        @summary: Checks the datetime strings of attributes that contain
            datetime strings
        @param expected_event: Contains event details (expected data)
                               to be verified against.
        @type expected_event: ExistsEventQueue object
        @param actual_event: Contains event details (actual data)
                             to be verified
        @type actual_event: NovaAtomEvent object
        @param expected_attribute: The event attribute that we expected,
            taken from the DB
        @type expected_attribute: string
        @param actual_attribute: The event attribute that we got,
            taken from Atom Hopper
        @type actual_attribute: string
        '''
        failure_msg = 'Expected {0} field in event to be {1}, was {2}'
        actual_string = str(getattr(actual_event.payload, actual_attribute))
        expected_string = str(getattr(expected_event, expected_attribute))

        if actual_string != expected_string:
            self.fixture_log.error(
                failure_msg.format(actual_attribute,
                                   expected_string, actual_string))

    def check_datetime_strings(self, actual_event, expected_event,
                               expected_attribute, actual_attribute):
        '''
        @summary: Checks the datetime strings of attributes that contain
            datetime strings
        @param expected_event: Contains event details (expected data)
                               to be verified against.
        @type expected_event: ExistsEventQueue object
        @param actual_event: Contains event details (actual data)
                             to be verified
        @type actual_event: NovaAtomEvent object
        @param expected_attribute: The event attribute that we expected,
            taken from the DB
        @type expected_attribute: string
        @param actual_attribute: The event attribute that we got,
            taken from Atom Hopper
        @type actual_attribute: string
        '''
        failure_msg = 'Expected {0} field in event to be {1}, was {2}'
        actual_date = getattr(actual_event.payload, actual_attribute)
        expected_date = getattr(expected_event, expected_attribute)

        if not are_datetimestrings_equal(actual_date, expected_date,
                                         self.datetime_seconds_leeway):
            self.fixture_log.error(failure_msg.format(
                actual_attribute, expected_date, actual_date))

    def validate_event_details(self):
        '''
        @summary: Verifies the common attributes for all compute events
        @type expected_entry: List of ExistsEventQueue objects
        @type actual_entry: List of NovaAtomEvent objects
        '''

        for uuid in self.actual_data_filtered_dict:
            ''' actual entry looks like this:
                {uuid: [event1, [event2], [event3]]}
                where events are type NovaAtomEvent
            '''
            actual_entry = self.actual_data_filtered_dict[uuid]
            expected_entry = self.expected_data_dict[uuid]

            if len(actual_entry) != len(expected_entry):
                msg = "Length of actual does not match expected!" \
                      "uuid: {0} Length expected: {1}, Length actual {2}" \
                      .format(expected_entry[0].server_id,
                              len(expected_entry), len(actual_entry))
                self.fixture_log.error(msg)
            elif len(actual_entry) == 1:
                index = 0
                self.verify_common_details_for_each_event(
                    expected_entry[index],
                    actual_entry[index])
            else:
                for actual_entry_index in range(len(actual_entry)):
                    for expected_entry_index in range(len(expected_entry)):
                        if (actual_entry[actual_entry_index].payload.state ==
                                expected_entry[expected_entry_index].
                                    server_status):
                            self.verify_common_details_for_each_event(
                                  expected_entry[expected_entry_index],
                                  actual_entry[actual_entry_index])

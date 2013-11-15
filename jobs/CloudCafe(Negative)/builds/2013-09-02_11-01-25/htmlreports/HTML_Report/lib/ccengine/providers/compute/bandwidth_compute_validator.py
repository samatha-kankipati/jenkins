'''
@summary: Provider class for Bandwidth validation test
@note: Inherits ComputeAPIProvider; overrides some of it's methods
@copyright: Copyright (c) 2013 Rackspace US, Inc.
'''
from datetime import datetime, timedelta
from collections import defaultdict

from ccengine.providers.base_provider import BaseProvider
from ccengine.providers.auth.auth_api import AuthProvider as _AuthProvider
from ccengine.providers.atomhopper import AtomHopperProvider
from ccengine.domain.compute.bandwidth.exists_event_queue import \
    ExistsEventQueue


class BandwidthComputeValidatorProvider(BaseProvider):
    '''
    @summary: Provider Module for the Compute Bandwidth Validator
    @note: Should be the primary interface to a test case or external tool.
    @copyright: Copyright (c) 2013 Rackspace US, Inc.
    '''

    def __init__(self, config, logger=None):
        super(BandwidthComputeValidatorProvider, self).__init__()
        if config is None:
            self.provider_log.warning('empty (=None) config recieved in init')
            # Load configuration from default.conf
            self.config = _AuthProvider
        else:
            self.config = config

    def get_expected_and_actual_data(self, search_param, atom_hopper_url,
                                     env_name, region, test_type):

        audit_period_ending = datetime.utcnow()
        audit_period_ending = audit_period_ending.replace(
                                  audit_period_ending.year,
                                  audit_period_ending.month,
                                  audit_period_ending.day,
                                  00, 00, 00, 00)
        audit_period_beginning = audit_period_ending - timedelta(days=1)
        self.atomhopper_provider = AtomHopperProvider(
                                      url=atom_hopper_url,
                                      config=self.config)

        expected_data = ExistsEventQueue.get_validation_data(
                                 audit_period_beginning,
                                 audit_period_ending,
                                 test_type,
                                 region,
                                 env_name)
        actual_data = (self.atomhopper_provider
                            .get_events_by_audit_period(
                                search_param,
                                audit_period_beginning,
                                audit_period_ending))
        return expected_data, actual_data

    def get_distinct_uuids_from_expected_validation_data(self,
                                                         expected_data):
        """
        @summary: Returns a distinct list of uuids from expected data
        @param expected_data: expected exists events from db
        @type expected_data: sqlalchemy.orm.query.Query
            which contains ExistsEventQueue object
        """
        distinct_list = []
        for event in expected_data:
            if event.server_id not in distinct_list:
                distinct_list.append(event.server_id)
        return distinct_list

    def get_actual_data_filtered_by_expected_server_ids(self, expected_data,
                                                        actual_data):
        """
        @summary: Filters the actual exists events from Atom Hopper
            based on the expected distinct uuids from the db
        """

        expected_server_ids = \
            self.get_distinct_uuids_from_expected_validation_data(
                expected_data)

        actual_data_filtered_dict = defaultdict(list)
        for entry in actual_data:
            if entry.payload.instance_id in expected_server_ids:
                (actual_data_filtered_dict[entry.payload.instance_id]
                 .append(entry))
        return actual_data_filtered_dict

    def get_expected_data_in_dict_by_server_ids(self, expected_data):
        """
        @summary: Make a dict of expected exists events from DB
            with uuid mapped to event(s)
        """

        expected_data_dict = defaultdict(list)
        for entry in expected_data:
            expected_data_dict[entry.server_id].append(entry)
        return expected_data_dict

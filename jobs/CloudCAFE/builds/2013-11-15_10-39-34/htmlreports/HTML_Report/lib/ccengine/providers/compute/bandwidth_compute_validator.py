'''
@summary: Provider class for Bandwidth validation test
@note: Inherits ComputeAPIProvider; overrides some of it's methods
@copyright: Copyright (c) 2013 Rackspace US, Inc.
'''

from collections import defaultdict
from datetime import datetime, timedelta
from textwrap import dedent

from ccengine.common.tools.datatools import string_to_datetime
from ccengine.domain.compute.bandwidth.exists_event_queue import \
    ExistsEventQueue
from ccengine.providers.base_provider import BaseProvider
from ccengine.providers.atomhopper import AtomHopperProvider


class BandwidthComputeValidatorProvider(BaseProvider):
    '''
    @summary: Provider Module for the Compute Bandwidth Validator
    @note: Should be the primary interface to a test case or external tool.
    @copyright: Copyright (c) 2013 Rackspace US, Inc.
    '''

    def __init__(self, config, logger=None):
        super(BandwidthComputeValidatorProvider, self).__init__()
        self.config = config

        # get current audit period
        audit_period_ending = datetime.utcnow()
        self.audit_period_ending = audit_period_ending.replace(
            audit_period_ending.year,
            audit_period_ending.month,
            audit_period_ending.day,
            00, 00, 00, 00)
        self.audit_period_beginning = (self.audit_period_ending -
                                       timedelta(days=1))

    def get_expected_and_actual_data(self, search_param, atom_hopper_url,
                                     env_name, region, test_type,
                                     audit_period_beginning=None,
                                     audit_period_ending=None):

        if audit_period_beginning is None or audit_period_ending is None:
            audit_period_beginning = self.audit_period_beginning
            audit_period_ending = self.audit_period_ending
        else:
            self.audit_period_beginning = audit_period_beginning
            self.audit_period_ending = audit_period_ending

        self.provider_log.debug('audit_period_beginning: {0}'
                                .format(audit_period_beginning))
        self.provider_log.debug('audit_period_ending: {0}'
                                .format(audit_period_ending))
        self.atomhopper_provider = AtomHopperProvider(url=atom_hopper_url,
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

    def get_sorted_events_by_launched_at(self, expected, actual):
        '''
        @summary: sorts the list of events sent, by launched_at time
        @param expected: list of expected events to be sorted
        @type expected: list of ExistsEventQueue objects
        @param actual: list of actual events to be sorted
        @type actual: list of NovaAtomEvent objects
        @return: list of sorted expected & actual events
        '''
        expected_entries = sorted(expected, key=lambda entry:
                                  string_to_datetime(entry.launched_at),
                                  reverse=True)
        actual_entries = sorted(actual, key=lambda entry:
                                string_to_datetime(entry.payload.launched_at),
                                reverse=True)
        return expected_entries, actual_entries

    def format_report_for_email(self, test_results):
        """
        @summary: Creates a bandwidth report for emailing
        @param test_results: Object that contains bw test results
        @type test_results: Bandwidth Test Results object
        @return formatted_report: The bw report for use in mailing
        @type formatted_report: string
        """

        format_args = {
            'audit_period_beginning': self.audit_period_beginning,
            'audit_period_ending': self.audit_period_ending,
            'total_instances_tested': test_results.total_instances_tested,
            'total_instances_failed': test_results.total_instances_failed,
            'total_instances_passed': test_results.total_instances_passed,
            'total_instances_overbilling':
            test_results.total_instances_overbilling,
            'total_instances_underbilling':
            test_results.total_instances_underbilling,
            'total_instances_percent_under_bw':
            test_results.total_instances_percent_under_bw,
            'total_instances_percent_over_bw':
            test_results.total_instances_percent_over_bw,
            'total_instances_not_found':
            test_results.total_instances_with_events_not_found
        }

        report = \
            """
            Hi Everybody,

            Here are today's bandwidth test results.

            ############################################################
            BANDWIDTH TEST RESULTS
            Audit Period: {audit_period_beginning} - {audit_period_ending} UTC
            ############################################################

            ------------------------------
            {total_instances_not_found:03d} Missing Exists Events!\n
            ------------------------------
            {total_instances_overbilling:03d}% Over Billing!\n
            ------------------------------
            {total_instances_percent_under_bw:05.2f}% Under Billing!\n
             ------------------------------

            TOTAL INSTANCES :
            \t{total_instances_tested:03d} : TESTED
            \t{total_instances_passed:03d} : PASSED
            \t{total_instances_failed:03d} : FAILED
            \t\t{total_instances_overbilling:03d} : Over Billing
            \t\t{total_instances_underbilling:03d} : Under Billing

            ############################################################
            ############################################################

            -Compute Bandwidth Validator

            """.format(**format_args)

        report = dedent(report)
        # new section in case of missing instances
        if test_results.total_instances_with_events_not_found:
            report = "{0}Instances with Events Not Found:\n{1}\n\n".format(
                report, '\n'.join(test_results
                                  .instances_with_events_not_found.keys()))
            report = dedent(report)
        if test_results.total_instances_underbilling:
            report = "{0}Instances Underbilling:\n{1}\n\n".format(
                report, '\n'.join(test_results.instances_underbilling.keys()))
            report = dedent(report)
        if test_results.total_instances_overbilling:
            report = "{0}Instances Overbilling:\n{1}\n\n".format(
                report, '\n'.join(test_results.instances_overbilling.keys()))
            report = dedent(report)
        self.provider_log.debug(report)
        return report

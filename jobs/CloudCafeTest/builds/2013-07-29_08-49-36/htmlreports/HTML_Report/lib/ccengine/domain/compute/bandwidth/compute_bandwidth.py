from ccengine.common.tools.datatools import merge_dicts


class BandwidthBilling(object):

    def __init__(self, percent_diff, leeway=10.0):
        '''
        @summary: Represents Bandwidth Billing model that has an
            overcharge or undercharge property
        '''
        self.percent_diff = percent_diff
        self.leeway = leeway

    @property
    def overcharged(self):
        if self.percent_diff > 0:
            if self.percent_diff >= self.leeway:
                return True
        return False

    @property
    def undercharged(self):
        if self.percent_diff < 0:
            if self.percent_diff <= -self.leeway:
                return True
        return False


class BandwidthDeltas(object):

    no_bandwidth = {'expected': 0,
                    'actual': 0,
                    'delta': 0,
                    'percent_diff': 0.0}
    expected_no_bandwidth_buffer = 10485760

    def __init__(self, expected_bandwidth, actual_bandwidth):
        '''
        @summary: Represents Bandwidth Deltas model for a given event
        @note: This does the computations and returns the results as
            a list of [expected, actual, delta, percent_diff]
        '''
        self.expected_bandwidth = expected_bandwidth
        self.actual_bandwidth = actual_bandwidth

    def _bandwidth_percent_calculation(self, expected_bw, actual_bw):
        if expected_bw == 0:
            if actual_bw == 0:
                return self.no_bandwidth
            else:
                delta = actual_bw - self.expected_no_bandwidth_buffer
                percent_diff = (float(delta * 100) /
                                float(self.expected_no_bandwidth_buffer))
                return {'expected': self.expected_no_bandwidth_buffer,
                        'actual': actual_bw,
                        'delta': delta,
                        'percent_diff': percent_diff}
        delta = actual_bw - expected_bw
        percent_diff = float(delta * 100) / float(expected_bw)
        return {'expected': expected_bw,
                'actual': actual_bw,
                'delta': delta,
                'percent_diff': percent_diff}

    def _get_bw_details(self, traffic_type, traffic_dir):
        if traffic_type in dir(self.actual_bandwidth):
            expected = int(self.expected_bandwidth[traffic_type][traffic_dir])
            actual = int(getattr(self.actual_bandwidth, traffic_type)
                         [traffic_dir])
            return self._bandwidth_percent_calculation(expected, actual)
        else:
            return self.no_bandwidth

    @property
    def _private_out(self):
        return self._get_bw_details(traffic_type='private',
                                    traffic_dir='bw_out')

    @property
    def _private_in(self):
        return self._get_bw_details(traffic_type='private',
                                    traffic_dir='bw_in')

    @property
    def _public_out(self):
        return self._get_bw_details(traffic_type='public',
                                    traffic_dir='bw_out')

    @property
    def _public_in(self):
        return self._get_bw_details(traffic_type='public',
                                    traffic_dir='bw_in')

    def get_bandwidth_data(self):
        '''
        @summary: dict will look like this eventually from the return of the
            property defs:
            {public_bw_out: [expected_bw, actual_bw, delta, percent_diff],
             public_bw_in: [expected_bw, actual_bw, delta, percent_diff],
             private_bw_out: [expected_bw, actual_bw, delta, percent_diff],
             private_bw_in: [expected_bw, actual_bw, delta, percent_diff]
            }
        '''

        bandwidth_details_dict = dict()
        bandwidth_details_dict['public_bw_out'] = self._public_out
        bandwidth_details_dict['public_bw_in'] = self._public_in
        bandwidth_details_dict['private_bw_out'] = self._private_out
        bandwidth_details_dict['private_bw_in'] = self._private_in
        return bandwidth_details_dict


class BandwidthTestResults(object):

    expected_no_bandwidth_buffer = 10485760

    def __init__(self, test_results_dict, missing_events_dict):
        '''
        @summary: Represents Bandwidth Test Results model for
            processing a dictionary of bandwidth test results
            and a missing events dict
        @param test_results_dict: bandwidth test results to be processed
        @type test_results_dict: defaultdict(<type 'list'>)
        @param missing_events_dict: a dict of uuids mapped to expected data,
            representing events that were not found in AH
        @type missing_events_dict: list
        @note: The structure of the test_results_dict being passed in looks
            like this:
            { uuid1: [message_id_1 : { test_results_dict1, ... },
                     ...
                    ]
              ...
            }
        '''
        self.test_results_dict = test_results_dict
        self.missing_events_dict = missing_events_dict

    @property
    def total_instances_tested(self):
        return len(self.test_results_dict.keys())

    @property
    def total_events_tested(self):
        return sum(len(message_list) for message_list in
                   self.test_results_dict.values())

    # this is in the context of billing or failures in public bw out
    @property
    def total_events_failed(self):
        return (len(self.fail_details_public_bw_out_over) +
                len(self.fail_details_public_bw_out_under))

    @property
    def failed_events(self):
        return merge_dicts(self.fail_details_public_bw_out_over,
                           self.fail_details_public_bw_out_under)

    @property
    def total_instances_failed(self):
        return len(dict(self.fail_details_public_bw_out_over.items() +
                        self.fail_details_public_bw_out_under.items()))

    @property
    def failed_instances(self):
        return dict(self.fail_details_public_bw_out_over.items() +
                    self.fail_details_public_bw_out_under.items()).keys()

    # returns a dict of failures that occurred for each interface;
    # caller can do a len on each of the properties to get the
    # total number of failures for each
    @property
    def fail_details_public_bw_in_over(self):
        return self._get_bw_traffic_fail_details(traffic='public_bw_in',
                                                 leeway=float(10.0))

    @property
    def fail_details_public_bw_in_under(self):
        return self._get_bw_traffic_fail_details(traffic='public_bw_in',
                                                 leeway=float(-10.0))

    @property
    def fail_details_public_bw_out_over(self):
        return self._get_bw_traffic_fail_details(traffic='public_bw_out',
                                                 leeway=float(10.0))

    @property
    def fail_details_public_bw_out_under(self):
        return self._get_bw_traffic_fail_details(traffic='public_bw_out',
                                                 leeway=float(-10.0))

    @property
    def fail_details_private_bw_in_over(self):
        return self._get_bw_traffic_fail_details(traffic='private_bw_in',
                                                 leeway=float(10.0))

    @property
    def fail_details_private_bw_in_under(self):
        return self._get_bw_traffic_fail_details(traffic='private_bw_in',
                                                 leeway=float(-10.0))

    @property
    def fail_details_private_bw_out_over(self):
        return self._get_bw_traffic_fail_details(traffic='private_bw_out',
                                                 leeway=float(10.0))

    @property
    def fail_details_private_bw_out_under(self):
        return self._get_bw_traffic_fail_details(traffic='private_bw_out',
                                                 leeway=float(-10.0))

    # in case, we don't find any actual events
    # based on what we expected
    @property
    def total_events_not_found(self):
        return self.missing_events_dict

    @property
    def total_events_not_found_count(self):
        return len(self.missing_events_dict)

    # for tracking under/over/no billing on instances
    # so, this checking the public bw out interface ONLY
    # if bw out is over then we have overbilling,
    # bw out in under then underbilling
    @property
    def total_instances_overbilling(self):
        raise NotImplementedError("Work in progress.")

    @property
    def total_instances_underbilling(self):
        raise NotImplementedError("Work in progress.")

    # total instances that failed which have no significance to billing
    @property
    def total_instances_no_billing(self):
        raise NotImplementedError("Work in progress.")

    # for calculating total underbilling
    @property
    def total_bandwidth_expected(self):
        raise NotImplementedError("Work in progress.")

    @property
    def total_bandwidth_actual(self):
        raise NotImplementedError("Work in progress.")

    @property
    def total_bandwidth_difference(self):
        raise NotImplementedError("Work in progress.")

    @property
    def total_percent_under_bw(self):
        raise NotImplementedError("Work in progress.")

    # for calcuating total overbilling
    @property
    def total_bandwidth_expected_over(self):
        raise NotImplementedError("Work in progress.")

    @property
    def total_bandwidth_actual_over(self):
        raise NotImplementedError("Work in progress.")

    @property
    def total_bandwidth_difference_over(self):
        raise NotImplementedError("Work in progress.")

    @property
    def total_percent_over_bw(self):
        raise NotImplementedError("Work in progress.")

    # useful analytics
    # failures per compute; compute_name : # of failures
    @property
    def total_fail_count_compute(self):
        raise NotImplementedError("Work in progress.")

    # test name failures; testname: # of failures
    @property
    def total_fail_count_testname(self):
        raise NotImplementedError("Work in progress.")

    # test name failures per compute; host: testname: # of failures
    @property
    def total_fail_count_compute_testname(self):
        raise NotImplementedError("Work in progress.")

    # test name failures that results from underbilling
    @property
    def total_fail_count_testname_underbilling(self):
        raise NotImplementedError("Work in progress.")

    # compute failures that results from underbilling
    @property
    def total_fail_count_compute_underbilling(self):
        raise NotImplementedError("Work in progress.")

    # test name failures that results from overbilling
    @property
    def total_fail_count_testname_overbilling(self):
        raise NotImplementedError("Work in progress.")

    # compute failures that results from overbilling
    @property
    def total_fail_count_compute_overbilling(self):
        raise NotImplementedError("Work in progress.")

    def _get_bw_traffic_fail_details(self, traffic, leeway):
        fail_dict = {}
        for uuid, messages in self.test_results_dict.items():
            for message_id_dict in messages:
                for _message_id, test_attributes in message_id_dict.items():
                    percent_diff = \
                        test_attributes['bandwidth'][traffic]['percent_diff']
                    # check for overbilling
                    if percent_diff > leeway and leeway >= 0:
                        fail_type = '{0}_over'.format(traffic)
                        fail_dict = self._set_bw_failure_details_dict(
                            fail_dict, uuid, fail_type, message_id_dict)
                    # check for underbilling
                    elif percent_diff < leeway and leeway < 0:
                        # don't count underbilling where we
                        # had expected no bandwidth
                        expected_bw = \
                            test_attributes['bandwidth'][traffic]['expected']
                        if expected_bw != self.expected_no_bandwidth_buffer:
                            fail_type = '{0}_under'.format(traffic)
                            fail_dict = self._set_bw_failure_details_dict(
                                fail_dict, uuid, fail_type, message_id_dict)
        return fail_dict

    def _set_bw_failure_details_dict(self, fail_dict, uuid,
                                     fail_type, message_id_dict):
        '''
        @summary: Sets dicts for a specific uuid to a fail type.
            e.g., where fail_type can be public_bw_out_under,
            private_bw_in_under, etc.
        @param fail_dict: bandwidth test failures to be processed
        @type fail_dict: dict
        @param uuid: identifier of the instance
        @type uuid: string
        @param fail_type: interface and traffic flow; either under or over
             e.g., public_bw_out_under, private_bw_in_under, etc.
        @type fail_type: string
        @param message_id_dict: Failure details of the fail_type
        @type message_id_dict: dict
        @note: The structure of the dict being returned looks
            like this:
            { uuid1: {fail_type : { failed_event_info, ... },
                     ...
                    }
              ...
            }
        '''
        try:
            fail_dict[uuid][fail_type] = message_id_dict
        except KeyError:
            fail_dict[uuid] = {}
            fail_dict[uuid][fail_type] = message_id_dict
        return fail_dict

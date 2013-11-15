

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
                return [0, 0, 0, 0.0]
            else:
                leeway = 1048576
                delta = actual_bw - expected_bw
                percent_diff = float(delta * 100) / float(leeway)
                return [expected_bw, actual_bw, delta, percent_diff]
        delta = actual_bw - expected_bw
        percent_diff = float(delta * 100) / float(expected_bw)
        return [expected_bw, actual_bw, delta, percent_diff]

    def _get_bw_details(self, traffic_type, traffic_dir):
        if traffic_type in dir(self.actual_bandwidth):
            expected = int(self.expected_bandwidth[traffic_type][traffic_dir])
            actual = int(getattr(self.actual_bandwidth, traffic_type)
                         [traffic_dir])
            return self._bandwidth_percent_calculation(expected, actual)
        else:
            return [0, 0, 0, 0.0]

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

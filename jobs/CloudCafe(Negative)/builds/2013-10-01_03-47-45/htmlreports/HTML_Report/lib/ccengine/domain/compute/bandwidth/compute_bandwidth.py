

class BandwidthDiffParams(object):

    def __init__(self, delta=0, percent_diff=0.0):
        '''
        @summary: Represents Bandwidth differences for a given event
        '''
        self.delta = delta
        self.percent_diff = percent_diff


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
            BandwidthDiffParams object
        '''
        self.expected_bandwidth = expected_bandwidth
        self.actual_bandwidth = actual_bandwidth

    def _bandwidth_percent_calculation(self, expected_bw, actual_bw):
        if expected_bw == 0:
            if actual_bw == 0:
                return BandwidthDiffParams()
            else:
                expected_bw = 1048576
        delta = actual_bw - expected_bw
        percent_diff = float(delta * 100) / float(expected_bw)
        return BandwidthDiffParams(delta, percent_diff)

    def _percent_bw(self, traffic_type, traffic_dir):
        if traffic_type in dir(self.actual_bandwidth):
            expected = int(self.expected_bandwidth[traffic_type][traffic_dir])
            actual = int(getattr(self.actual_bandwidth, traffic_type)
                         [traffic_dir])
            return self._bandwidth_percent_calculation(expected, actual)
        return BandwidthDiffParams()

    @property
    def _private_out(self):
        return self._percent_bw(traffic_type='private', traffic_dir='bw_out')

    @property
    def _private_in(self):
        return self._percent_bw(traffic_type='private', traffic_dir='bw_in')

    @property
    def _public_out(self):
        return self._percent_bw(traffic_type='public', traffic_dir='bw_out')

    @property
    def _public_in(self):
        return self._percent_bw(traffic_type='public', traffic_dir='bw_in')

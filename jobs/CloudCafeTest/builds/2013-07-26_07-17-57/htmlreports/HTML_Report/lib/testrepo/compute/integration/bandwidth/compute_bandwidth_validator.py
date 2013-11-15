'''
@summary: Test cases classes for Compute Bandwidth tests
@copyright: Copyright (c) 2013 Rackspace US, Inc.
'''
from ccengine.common.decorators import attr
from testrepo.common.testfixtures.bandwidth_compute_validator \
    import BandwidthComputeValidatorFixture


class BwComputeValidator(BandwidthComputeValidatorFixture):
    '''
    @summary: Validates compute bandwidth
    '''

    @attr(type="bw_validator")
    def test_validate_compute_events(self):
        self.validate_event_details()

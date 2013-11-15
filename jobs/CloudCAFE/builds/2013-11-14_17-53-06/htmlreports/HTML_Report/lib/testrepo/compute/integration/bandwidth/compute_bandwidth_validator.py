'''
@summary: Test cases classes for Compute Bandwidth tests
@copyright: Copyright (c) 2013 Rackspace US, Inc.
'''
from datetime import datetime
from textwrap import dedent

from ccengine.common.decorators import attr
from testrepo.common.testfixtures.bandwidth_compute_validator \
    import BandwidthComputeValidatorFixture


class BwComputeValidator(BandwidthComputeValidatorFixture):
    '''
    @summary: Validates compute bandwidth and sends email
    '''

    @attr(type="bw_validator")
    def test_validate_compute_events(self):
        test_results = self.validate_events()
        my_report = self.bandwidth_validator_provider.format_report_for_email(
            test_results)
        subject = ('{0} Bandwidth Report Next Gen Preprod H52 for event_type '
                   '"{1}"'.format(datetime.utcnow().strftime("%Y%m%d"),
                                  self.config.compute_api.
                                  nova_event_type_in_atom_hopper_feed))
        response = self.mailgun_provider.send_simple_message(
            from_user=self.config.mailgun.from_email,
            to=self.config.mailgun.to_email,
            subject=subject,
            text=dedent(my_report))
        self.fixture_log.debug(response)

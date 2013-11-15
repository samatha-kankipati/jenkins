from testrepo.common.testfixtures.tq_search import TQSearchFixture
from ccengine.common.decorators import attr


class TestHealthCheck(TQSearchFixture):

    @attr(type='positive')
    def test_health_check_after_installation(self):
        'B-41831::Testing the health after deployment'
        health_report = self.gate_provider.gate_client.health_check().entity

        self.assertTrue(health_report is not None, "The response is Empty")
        self.assertEquals(health_report.status, "GREEN", "The status is: {0} \
                          not Green".format(health_report.status))
        self.assertEquals(health_report.cluster_name, "ticket.cluster",
                          "The cluster name is: {0} not \
                          elasticsearch".format(health_report.cluster_name))

    @attr(type='positive')
    def test_info_check_after_installation(self):
        'B-41831::Testing the info after deployment'
        info_report = self.gate_provider.gate_client.info_check().entity

        self.assertTrue(info_report is not None, "The info is Empty")
        self.assertTrue(info_report.version is not None,
                        "The version number is None")
        self.assertTrue(info_report.build_at is not None, "The build at \
                        field is None")

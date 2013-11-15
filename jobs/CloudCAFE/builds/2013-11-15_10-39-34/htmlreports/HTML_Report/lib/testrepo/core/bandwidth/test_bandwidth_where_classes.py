from testrepo.common.testfixtures.core import CoreFixture
from ccengine.common.decorators import attr
from ccengine.domain.core.request.core_request import WhereEquals


class TestBandwidth(CoreFixture):

    @attr(suite='regression', type='positive')
    def test_verify_bandwidth_using_AllotmentWhere(self):
        """
        @summary: Verify user can get attributes of Bandwidth.Allotment Class
        using AllotmentWhere method
        """
        snapshot_date = self.config.core.snapshot_date
        where_condition = WhereEquals("snapshot_date", snapshot_date)
        attributes = ["account", "allotment", "id", "snapshot_date"]
        bandwidth_details = self.bandwidth_client.\
                get_allotment_attributes_using_allotmentwhere(
                    where_condition, attributes, limit=None, offset=None)

        self.assertEqual(200, bandwidth_details.status_code,
                         "Response status code is not 200")
        self.assertEqual(len(bandwidth_details.entity), 0,
                        "Bandwidth details returns a list")

    @attr(suite='regression', type='positive')
    def test_verify_bandwidth_BillableDevicesWhere_using_computer(self):
        """
        @summary: Verify user can get attributes of Bandwidth.BillableDevices
        Class using BillableDevicesWhere method
        """
        computer = self.config.core.computer_id
        where_condition = WhereEquals("computer", computer)
        attributes = ["account", "billable_gb", "bytes_in", "bytes_out", "id",
                      "computer", "monitoring_preference", "snapshot_date"]
        bandwidth_details = self.bandwidth_client.\
            get_billabledevices_attributes_using_billabledeviceswhere(
                where_condition, attributes, limit=None, offset=None)

        self.assertEqual(200, bandwidth_details.status_code,
                         "Response status code is not 200")
        self.assertEqual(len(bandwidth_details.entity), 0,
                        "Bandwidth details returns a list")

    @attr(suite='regression', type='positive')
    def test_verify_bandwidth_BillableDevicesWhere_snapshotdate(self):
        """
        @summary: Verify user can get attributes of Bandwidth.BillableDevices
        Class using BillableDevicesWhere method
        """
        snapshot_date = self.config.core.snapshot_date
        where_condition = WhereEquals("snapshot_date", snapshot_date)
        attributes = ["account", "billable_gb", "bytes_in", "bytes_out", "id",
                      "computer", "monitoring_preference", "snapshot_date"]
        bandwidth_details = self.bandwidth_client.\
            get_billabledevices_attributes_using_billabledeviceswhere(
                where_condition, attributes, limit=None, offset=None)

        self.assertEqual(200, bandwidth_details.status_code,
                         "Response status code is not 200")
        self.assertEqual(len(bandwidth_details.entity), 0,
                        "Bandwidth details returns a list")

    @attr(suite='regression', type='positive')
    def test_verify_certificate_using_CertificateWhere(self):
        """
        @summary: Verify user can get attributes of Certificate.Certificate
        Class using CertificateWhere method
        """
        certificate_id = self.config.core.certificate_id
        where_condition = WhereEquals("id", certificate_id)
        attributes = ["account", "domain_name", "end_date",
                      "licenses", "start_date", "order_number",
                      "status", "ticket", "id"]
        certificate_details = self.bandwidth_client.\
                get_certificate_using_certificatewhere(
                    where_condition, attributes, limit=None, offset=None)

        self.assertEqual(200, certificate_details.status_code,
                         "Response status code is not 200")
        for item in certificate_details.entity:
            self.assertEqual(item.id, certificate_id,
                             "Certificate id's are not same")

import os
import uuid
from testrepo.common.testfixtures.usage import (CBSUsageFixture,
                                                CSVDataGenerator,
                                                CSVMetricsWriter)
from ccengine.common.decorators import DataDrivenFixture
from ccengine.common.decorators import data_driven_test

CSV_ALL_VARS = "cbs_atomhopper_all_vars.csv"

@DataDrivenFixture
class CBSUsageTesting(CBSUsageFixture):

    @classmethod
    def setUpClass(cls):
        super(CBSUsageTesting, cls).setUpClass()
        headers = [
            "Location", "Tenant ID", "Datacenter", "Region", "Message ID",
            "Start Time", "End Time", "Resource Id", "Message Type",
            "Environment", "Version", "Service Code", "Resouce Type",
            "Provisioned Space", "Volume Type", "Snapshot Space",
            "Status Code"]

        logpath = os.path.join(
            os.getenv('CLOUDCAFE_LOG_PATH'), cls.filename)
        cls.metrics = CSVMetricsWriter(logpath, headers, True)

    @data_driven_test(CSVDataGenerator(CSV_ALL_VARS))
    def ddtest_cbs_usage(
            self, tenant_id, datacenter, region,
            message_id, start_time, end_time, resource_id,
            message_type, environment, version,
            service_code, resource_type, provisioned,
            vol_type, snapshot):

        message_id = str(uuid.uuid4())

        resp = self.atomhopper_client.add_event(
            tenant_id=tenant_id, datacenter=datacenter, region=region,
            message_id=message_id, start_time=start_time, end_time=end_time,
            resource_id=resource_id, message_type=message_type,
            environment=environment, version=version,
            service_code=service_code, resource_type=resource_type,
            provisioned=provisioned, vol_type=vol_type, snapshot=snapshot)

        if "location" in resp.headers:
            location = resp.headers["location"]
            self.metrics.writerow([
                location, tenant_id, datacenter, region, message_id,
                start_time, end_time, resource_id, message_type, environment,
                version, service_code, resource_type, provisioned, vol_type,
                snapshot, resp.status_code])
        self.assertEqual(resp.status_code, 201, "Post entry should pass. 201")

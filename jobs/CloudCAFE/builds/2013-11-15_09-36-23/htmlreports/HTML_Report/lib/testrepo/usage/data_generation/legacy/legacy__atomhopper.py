from datetime import datetime, timedelta
import os
from random import choice
import uuid
from testrepo.common.testfixtures.usage import (
    CSVDataGenerator, CSVMetricsWriter, LegacyUsageFixture)
from ccengine.common.decorators import attr
from ccengine.common.decorators import DataDrivenFixture
from ccengine.common.decorators import data_driven_test
from ccengine.common.constants.usage import LEGACY_PRICING_DATA

CSV_ALL_VARS = "legacy_atomhopper_all_vars.csv"
CSV_COMMIT = "legacy_atomhopper_commit.csv"
LEGACY_BANDWIDTH = "E2ECloud server BandWidth"
LEGACY_RHEL = "E2E Cloud Server RHEL Count"
LEGACY_UPTIME = "E2ECloud Server Uptime"


@DataDrivenFixture
class LegacyUsageTesting(LegacyUsageFixture):

    @classmethod
    def setUpClass(cls):
        super(LegacyUsageTesting, cls).setUpClass()
        headers = [
            "Title", "Location", "Tenant ID", "Datacenter", "Region",
            "Message ID", "Start Time", "End Time", "Resource Id", "Version",
            "Service Code", "Resouce Type", "Bandwidth In", "Bandwidth_Out",
            "Flavor", "Extra Public Ips", "Extra Private Ips", "Is Redhat",
            "Is Mssql", "Is Mssqlweb", "Is Windows", "Is Selinux",
            "Is Managed", "Status Code", "Price", "Request Body"]

        logpath = os.path.join(
            os.getenv('CLOUDCAFE_LOG_PATH'), cls.filename)
        cls.metrics = CSVMetricsWriter(logpath, headers, False)

    @data_driven_test(CSVDataGenerator(CSV_ALL_VARS))
    def ddtest_legacy_usage(
            self, title, tenant_id, message_id, resource_id, datacenter,
            region, start_time, end_time, version, service_code, resource_type,
            bandwidth_in, bandwidth_out, flavor, extra_public_ips,
            extra_private_ips, is_redhat, is_mssql, is_mssqlweb, is_windows,
            is_selinux, is_managed):

        message_id = str(uuid.uuid4())

        resp = self.atomhopper_client.add_event(
            title, tenant_id, message_id, resource_id, datacenter,
            region, start_time, end_time, version, service_code, resource_type,
            bandwidth_in, bandwidth_out, flavor, extra_public_ips,
            extra_private_ips, is_redhat, is_mssql, is_mssqlweb, is_windows,
            is_selinux, is_managed)

        if "location" in resp.headers:
            location = resp.headers["location"]
            self.metrics.writerow([
                title, location, tenant_id, datacenter, region, message_id,
                start_time, end_time, resource_id, version, service_code,
                resource_type, bandwidth_in, bandwidth_out, flavor,
                extra_public_ips, extra_private_ips, is_redhat, is_mssql,
                is_mssqlweb, is_windows, is_selinux, is_managed,
                resp.status_code, "0"])

        self.assertEqual(resp.status_code, 201, "Post entry should pass. 201")

    @attr('commit')
    @attr('commit_legacy')
    @data_driven_test(CSVDataGenerator(CSV_COMMIT))
    def ddtest_legacy_usage_commit(
            self, price, tenant_id="12345", title="E2ECloud Server Uptime",
            region=None, option_id=None, version="1",
            service_code="CloudServers", resource_type="SLICE",
            bandwidth_in="0", bandwidth_out="0", flavor=None,
            extra_public_ips="1", extra_private_ips="1", is_redhat="false",
            is_mssql="false", is_mssqlweb="false", is_windows="false",
            is_selinux="false", is_managed=None):

        _region = region
        _is_managed = is_managed
        _option_id = option_id
        _flavor = flavor
        price = float(price)
        seconds = 86400
        while(seconds == 86400):
            message_id = str(uuid.uuid4())
            resource_id = str(uuid.uuid4())
            tmp = datetime.utcnow()
            end_time = datetime(tmp.year, tmp.month, tmp.day, 0, 0, 0, 0)
            key = choice(LEGACY_PRICING_DATA.get_keys(
                region=_region, managed=_is_managed, option_id=_option_id,
                flavor=_flavor))
            flavor = key[0]
            option_id = key[1]
            is_managed = key[2]
            region = key[3]
            datacenter = region + "1"
            is_windows = is_mssql = is_mssqlweb = is_redhat = is_selinux = \
                'false'
            if option_id == "4":
                is_windows = 'true'
            elif option_id == "12":
                is_windows = 'true'
                is_mssql = 'true'
            elif option_id == "36":
                is_windows = 'true'
                is_mssqlweb = 'true'
            elif option_id == "1":
                is_redhat = 'true'
            elif option_id == "2":
                is_selinux = 'true'

            price_per_hour = LEGACY_PRICING_DATA.get_price(*key)
            seconds = price / price_per_hour * 60 * 60
            if seconds > 86400:
                seconds = 86400
            rprice = price_per_hour * seconds / 60.0 / 60.0
            price -= rprice

            billed_time = timedelta(seconds=seconds)
            start_time = end_time - billed_time
            start_time = start_time.strftime("%Y-%m-%dT%H:%M:%SZ")
            end_time = end_time.strftime("%Y-%m-%dT%H:%M:%SZ")

            resp = self.atomhopper_client.add_event(
                tenant_id=tenant_id, message_id=message_id,
                resource_id=resource_id, datacenter=datacenter, region=region,
                start_time=start_time, end_time=end_time, flavor=flavor,
                is_redhat=is_redhat, is_mssql=is_mssql,
                is_mssqlweb=is_mssqlweb, is_windows=is_windows,
                is_selinux=is_selinux, is_managed=is_managed)

            request = resp.request.body

            if "location" in resp.headers:
                location = resp.headers["location"]
            else:
                location = ""

            self.metrics.writerow([
                "E2ECloud Server Uptime", location, tenant_id, datacenter,
                region, message_id, start_time, end_time, resource_id, '1',
                'CloudServers', 'SLICE', '0', '0', flavor, '1', '1', is_redhat,
                is_mssql, is_mssqlweb, is_windows, is_selinux, is_managed,
                resp.status_code, rprice, request])

            self.assertEqual(
                resp.status_code, 201, "Post entry should pass. 201")

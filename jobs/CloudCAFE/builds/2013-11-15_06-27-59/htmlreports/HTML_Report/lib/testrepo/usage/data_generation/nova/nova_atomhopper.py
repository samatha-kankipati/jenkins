from datetime import datetime, timedelta
import os
import uuid
import unittest
from random import choice
from testrepo.common.testfixtures.usage import (CSVDataGenerator,
                                                CSVMetricsWriter,
                                                NovaUsageFixture)
from ccengine.common.decorators import attr
from ccengine.common.decorators import DataDrivenFixture
from ccengine.common.decorators import data_driven_test
from ccengine.common.constants.usage import NOVA_PRICING_DATA

CSV_ALL_VARS = "nova_atomhopper_all_vars.csv"
CSV_COMMIT = "nova_atomhopper_commit.csv"


@DataDrivenFixture
class NovaUsageTesting(NovaUsageFixture):

    @classmethod
    def setUpClass(cls):
        super(NovaUsageTesting, cls).setUpClass()
        headers = [
            "Usage", "Location", "Datacenter", "Region", "Message ID",
            "Audit Period Beginning", "Audit Period Ending", "Tenant ID",
            "Public Bandwidth In", "Public Bandwidth Out",
            "Private Bandwidth In", "Private Bandwidth Out", "Memory",
            "Option ID", "Display Name", "Instance Id", "Status Code", "Price",
            "Request Body"]
        logpath = os.path.join(
            os.getenv('CLOUDCAFE_LOG_PATH'), cls.filename)
        cls.metrics = CSVMetricsWriter(logpath, headers, True)

    @attr('base_test')
    @data_driven_test(CSVDataGenerator(CSV_ALL_VARS))
    def ddtest_nova_usage(
            self, tenant_id, datacenter, region, message_id,
            audit_period_beginning, audit_period_ending, display_name,
            instance_id, memory_mb, bw_in_public, bw_out_public, bw_in_private,
            bw_out_private, flavor, option_id):
        '''
            This is just a stub test to ensure the fixture and client are
            working properly
        '''

        message_id = str(uuid.uuid4())

        resp = self.atomhopper_client.add_event(
            datacenter=datacenter, region=region, message_id=message_id,
            audit_period_beginning=audit_period_beginning, tenant_id=tenant_id,
            bw_in_public=bw_in_public, bw_out_public=bw_out_public,
            bw_in_private=bw_in_private, bw_out_private=bw_out_private,
            memory_mb=memory_mb, audit_period_ending=audit_period_ending,
            display_name=display_name, instance_id=instance_id,
            option_id=option_id, flavor=flavor)

        if "location" in resp.headers:
            location = resp.headers["location"]
        else:
            location = None
        self.metrics.writerow([
            location, datacenter, region, message_id, audit_period_beginning,
            audit_period_ending, tenant_id, bw_in_public, bw_out_public,
            bw_in_private, bw_out_private, memory_mb, option_id, display_name,
            instance_id, resp.status_code, "0"])

        self.assertEqual(resp.status_code, 201, "Post entry should pass. 201")

    @attr('commit')
    @attr('commit_nova')
    @data_driven_test(CSVDataGenerator(CSV_COMMIT))
    def ddtest_nova_usage_commit(
            self, price, tenant_id, datacenter=None, region=None,
            option_id=None, display_name=None, bw_in_public="0",
            bw_out_public="0", flavor=None, is_managed=None,
            late_usage="NORMAL"):
        '''
            This is just a stub test to ensure the fixture and client are
            working properly
        '''
        _region = region
        _is_managed = is_managed
        _option_id = option_id
        _flavor = flavor

        price = float(price)
        start_price = price
        seconds = 86400

        while(seconds == 86400):
            message_id = str(uuid.uuid4())
            instance_id = str(uuid.uuid4())
            tmp = datetime.utcnow()
            end_time = datetime(tmp.year, tmp.month, tmp.day, 0, 0, 0, 0)

            key = choice(NOVA_PRICING_DATA.get_keys(
                region=_region, managed=_is_managed, option_id=_option_id,
                flavor=_flavor))
            flavor = key[0]
            option_id = key[1]
            is_managed = key[2]
            region = key[3]
            datacenter = region + "1"
            if flavor == "2":
                memory_mb = "512MB"
            elif flavor == "3":
                memory_mb = '1GB'
            elif flavor == "4":
                memory_mb = '2GB'
            elif flavor == "5":
                memory_mb = '4GB'
            elif flavor == "6":
                memory_mb = "8GB"
            elif flavor == "7":
                memory_mb = "15GB"
            elif flavor == "8":
                memory_mb = "30GB"

            price_per_hour = NOVA_PRICING_DATA.get_price(*key)
            seconds = price / price_per_hour * 60 * 60
            if seconds > 86400:
                seconds = 86400
            else:
                seconds = int(seconds / 60.0 / 60.0) * 60 * 60
            rprice = price_per_hour * seconds / 60.0 / 60.0
            price -= rprice
            if late_usage == "LATE":
                late_usage_delta = timedelta(weeks=8)
            elif late_usage == "REALLYLATE":
                late_usage_delta = timedelta(weeks=16)
            else:
                late_usage_delta = timedelta(weeks=0)

            billed_time = timedelta(seconds=seconds)
            end_time -= late_usage_delta
            start_time = end_time - billed_time
            start_time = start_time.strftime("%Y-%m-%d %H:%M:%S")
            end_time = end_time.strftime("%Y-%m-%d %H:%M:%S")

            resp = self.atomhopper_client.add_event(
                tenant_id=tenant_id, option_id=option_id, flavor=flavor,
                datacenter=datacenter, region=region, message_id=message_id,
                instance_id=instance_id, audit_period_beginning=start_time,
                audit_period_ending=end_time, memory_mb=memory_mb)

            request = resp.request.body

            if "location" in resp.headers:
                location = resp.headers["location"]
            else:
                location = None

            self.metrics.writerow([
                late_usage, location, datacenter, region, message_id,
                start_time, end_time, tenant_id, "0", "0", "0", "0", memory_mb,
                option_id, "Fake Server", instance_id, resp.status_code,
                rprice, request])

            self.assertEqual(
                resp.status_code, 201, "Post entry should pass. 201")
        submitted_price = str(start_price - price)
        self.metrics.writerow([
            "TOTAL", submitted_price, "", "", "", "", "", "", "", "", "", "",
            "", "", "", "", "", "", ""])

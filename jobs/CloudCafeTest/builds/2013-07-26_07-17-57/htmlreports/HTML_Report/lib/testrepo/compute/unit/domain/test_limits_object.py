from ccengine.domain.compute.response.limits import Limits
import unittest2 as unittest


class LimitsDomainTests(object):
    def test_max_image_meta(self):
        self.assertEqual(self.limits_response.absolute.get('totalVolumesUsed'), 0)

    def test_max_server_meta(self):
        self.assertEqual(self.limits_response.absolute.get('maxServerMeta'), 20)

    def test_max_personality_file_limits(self):
        self.assertEqual(self.limits_response.absolute.get('maxPersonality'), 6)

    def test_personality_file_size_limit(self):
        self.assertEqual(self.limits_response.absolute.get('maxPersonalitySize'), 10240)

    def test_max_total_instances(self):
        self.assertEqual(self.limits_response.absolute.get('maxTotalInstances'), 100)

    def test_max_total_ram_size(self):
        self.assertEqual(self.limits_response.absolute.get('maxTotalRAMSize'), 66560)

    def test_total_ram_used(self):
        self.assertEqual(self.limits_response.absolute.get('totalRAMUsed'), 16896)


class LimitsXMLDomainTest(unittest.TestCase, LimitsDomainTests):

    @classmethod
    def setUpClass(cls):
        cls.limits_xml = '<?xml version="1.0" encoding="UTF-8"?> <limits xmlns:lim="http://docs.openstack.org/common/api/v1.0" xmlns="http://docs.openstack.org/common/api/v1.0"> <rates> <rate regex="/v[^/]/(\d+)/(rax-networks)/?.*" uri="/rax-networks"> <limit next-available="2012-09-10T20:14:17.997Z" unit="DAY" remaining="0" value="0" verb="POST"/> <limit next-available="2012-09-10T20:14:17.997Z" unit="MINUTE" remaining="0" value="0" verb="GET"/> </rate> <rate regex="/v[^/]/(\d+)/(servers)/?.*" uri="/servers"> <limit next-available="2012-09-10T20:14:17.997Z" unit="DAY" remaining="1000" value="1000" verb="POST"/> </rate> <rate regex="/v[^/]/(\d+)/?.*" uri="*"> <limit next-available="2012-09-10T20:14:17.997Z" unit="MINUTE" remaining="100" value="100" verb="ALL"/> </rate> </rates> <absolute xmlns:os-used-limits="http://docs.openstack.org/compute/ext/used_limits/api/v1.1" xmlns:atom="http://www.w3.org/2005/Atom"> <limit name="maxServerMeta" value="20"/> <limit name="maxTotalInstances" value="100"/> <limit name="maxPersonality" value="6"/> <limit name="totalPrivateNetworksUsed" value="0"/> <limit name="maxImageMeta" value="20"/> <limit name="maxPersonalitySize" value="10240"/> <limit name="totalVolumesUsed" value="0"/> <limit name="maxTotalPrivateNetworks" value="0"/> <limit name="maxTotalKeypairs" value="100"/> <limit name="totalCoresUsed" value="9"/> <limit name="maxTotalVolumes" value="0"/> <limit name="totalRAMUsed" value="16896"/> <limit name="totalInstancesUsed" value="3"/> <limit name="totalVolumeGigabytesUsed" value="0"/> <limit name="maxTotalCores" value="-1"/> <limit name="totalSecurityGroupsUsed" value="0"/> <limit name="maxTotalFloatingIps" value="5"/> <limit name="totalKeyPairsUsed" value="0"/> <limit name="maxTotalVolumeGigabytes" value="-1"/> <limit name="maxTotalRAMSize" value="66560"/> </absolute> </limits>'
        cls.limits_response = Limits.deserialize(cls.limits_xml, 'xml')


class LimitsJSONDomainTest(unittest.TestCase, LimitsDomainTests):

    @classmethod
    def setUpClass(cls):
        cls.limits_json = '{"limits": {"absolute": {"maxImageMeta": 20, "maxPersonality": 6, "maxPersonalitySize": 10240, "maxServerMeta": 20, "maxTotalCores": -1, "maxTotalFloatingIps": 5, "maxTotalInstances": 100, "maxTotalKeypairs": 100, "maxTotalPrivateNetworks": 0, "maxTotalRAMSize": 66560, "maxTotalVolumeGigabytes": -1, "maxTotalVolumes": 0, "totalCoresUsed": 9, "totalInstancesUsed": 3, "totalKeyPairsUsed": 0, "totalPrivateNetworksUsed": 0, "totalRAMUsed": 16896, "totalSecurityGroupsUsed": 0, "totalVolumeGigabytesUsed": 0, "totalVolumesUsed": 0}, "rate": [{"limit": [{"next-available": "2012-09-10T20:11:45.146Z", "remaining": 0, "unit": "DAY", "value": 0, "verb": "POST"}, {"next-available": "2012-09-10T20:11:45.146Z", "remaining": 0, "unit": "MINUTE", "value": 0, "verb": "GET"}], "regex": "/(rax-networks)/?.*", "uri": "/rax-networks"}, {"limit": [{"next-available": "2012-09-10T20:11:45.146Z", "remaining": 1000, "unit": "DAY", "value": 1000, "verb": "POST"}], "regex": "/(servers)/?.*", "uri": "/servers"}, {"limit": [{"next-available": "2012-09-10T20:11:45.146Z", "remaining": 100, "unit": "MINUTE", "value": 100, "verb": "ALL"}], "regex": "/?.*", "uri": "*"}]}}'
        cls.limits_response = Limits.deserialize(cls.limits_json, 'json')

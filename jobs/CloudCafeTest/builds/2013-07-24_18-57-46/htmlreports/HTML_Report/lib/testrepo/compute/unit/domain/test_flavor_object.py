from ccengine.domain.compute.response.server import Flavor
import unittest2 as unittest


class FlavorDomainTest():

    def test_flavor_id(self):
        self.assertEqual(self.flavor.id, "2")

    def test_flavor_name(self):
        self.assertEqual(self.flavor.name, "512MB Standard Instance")

    def test_flavor_vcpus(self):
        self.assertEqual(self.flavor.vcpus, 1)

    def test_flavor_ram(self):
        self.assertEqual(self.flavor.ram, 512)

    def test_flavor_disk(self):
        self.assertEqual(self.flavor.disk, 20)

    def test_flavor_rxtx_factor(self):
        self.assertEqual(self.flavor.rxtx_factor, 2)

    def test_flavor_swap_factor(self):
        self.assertEqual(self.flavor.swap, 512)

    def test_flavor_links_self(self):
        self.assertEqual(self.flavor.links.self, "https://preprod.ord.servers.api.rackspacecloud.com/v2/5825921/flavors/2")

    def test_flavor_links_bookmark(self):
        self.assertEqual(self.flavor.links.bookmark, "https://preprod.ord.servers.api.rackspacecloud.com/5825921/flavors/2")


class FlavorXMLDomainTest(unittest.TestCase, FlavorDomainTest):

    @classmethod
    def setUpClass(cls):
        cls.flavor_xml = '<flavor xmlns:atom="http://www.w3.org/2005/Atom" xmlns="http://docs.openstack.org/compute/api/v1.1" disk="20" vcpus="1" ram="512" name="512MB Standard Instance" id="2" swap="512" rxtx_factor="2.0"><atom:link href="https://preprod.ord.servers.api.rackspacecloud.com/v2/5825921/flavors/2" rel="self"/><atom:link href="https://preprod.ord.servers.api.rackspacecloud.com/5825921/flavors/2" rel="bookmark"/></flavor>'
        cls.flavor = Flavor.deserialize(cls.flavor_xml, 'xml')


class FlavorJSONDomainTest(unittest.TestCase, FlavorDomainTest):

    @classmethod
    def setUpClass(cls):
        cls.flavor_json = '{"flavor": {"name": "512MB Standard Instance", "links": [{"href": "https://preprod.ord.servers.api.rackspacecloud.com/v2/5825921/flavors/2", "rel": "self"}, {"href": "https://preprod.ord.servers.api.rackspacecloud.com/5825921/flavors/2", "rel": "bookmark"}], "ram": 512, "vcpus": 1, "swap": 512, "rxtx_factor": 2.0, "disk": 20, "id": "2"}}'
        cls.flavor = Flavor.deserialize(cls.flavor_json, 'json')

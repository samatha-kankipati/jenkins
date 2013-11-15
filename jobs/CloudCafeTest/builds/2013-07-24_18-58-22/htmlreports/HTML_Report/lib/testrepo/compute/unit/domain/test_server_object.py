from ccengine.domain.compute.response.server import Server
from ccengine.domain.compute.request.server_requests import UpdateServer
import unittest2 as unittest
import xml.etree.ElementTree as ET


class ServerDomainTest(object):

    def test_server_disk_config(self):
        self.assertEqual(self.server.diskConfig, "AUTO")

    def test_server_power_state(self):
        self.assertEqual(self.server.power_state, 1)

    def test_server_progress(self):
        self.assertEqual(self.server.progress, 100)

    def test_server_task_state(self):
        self.assertEqual(self.server.task_state, None)

    def test_server_vm_state(self):
        self.assertEqual(self.server.vm_state, "active")

    def test_server_id(self):
        self.assertEqual(self.server.id, "a9a74ef8-2f46-469a-92e8-82a1b224ebe9")

    def test_server_name(self):
        self.assertEqual(self.server.name, "testserver47476")

    def test_tenant_id(self):
        self.assertEqual(self.server.tenant_id, "5825921")

    def test_server_status(self):
        self.assertEqual(self.server.status, "ACTIVE")

    def test_server_updated_time(self):
        self.assertEqual(self.server.updated, "2012-12-03T19:04:06Z")

    def test_host_id(self):
        self.assertEqual(self.server.hostId, "c70459909166c82b9fb53917dc665c44003c57b24d4a4015a3c8d108")

    def test_user_id(self):
        self.assertEqual(self.server.user_id, "199835")

    def test_server_created_time(self):
        self.assertEqual(self.server.created, "2012-12-03T18:59:16Z")

    def test_server_access_ips(self):
        self.assertEqual(self.server.accessIPv4, "192.168.1.10")
        self.assertEqual(self.server.accessIPv6, "2001:4801:7808:0052:2159:58b9:ff00:2154")

    def test_server_addresses(self):
        self.assertEqual(self.server.addresses.public.ipv4, "198.61.236.10")
        self.assertEqual(self.server.addresses.public.addresses[0].version, 4)
        self.assertEqual(self.server.addresses.public.ipv6, "2001:4801:7811:0069:cf10:c02d:ff10:3ffa")
        self.assertEqual(self.server.addresses.public.addresses[1].version, 6)
        self.assertEqual(self.server.addresses.private.ipv4, "10.176.99.109")
        self.assertEqual(self.server.addresses.private.addresses[0].version, 4)

    def test_server_flavor(self):
        self.assertEqual(self.server.flavor.id, "2")
        self.assertEqual(self.server.flavor.links.bookmark, "https://preprod.ord.servers.api.rackspacecloud.com/5825921/flavors/2")

    def test_server_image(self):
        self.assertEqual(self.server.image.id, "a10eacf7-ac15-4225-b533-5744f1fe47c1")
        self.assertEqual(self.server.image.links.bookmark, "https://preprod.ord.servers.api.rackspacecloud.com/5825921/images/a10eacf7-ac15-4225-b533-5744f1fe47c1")

    def test_server_links(self):
        self.assertEqual(self.server.links.self, "https://preprod.ord.servers.api.rackspacecloud.com/v2/5825921/servers/a9a74ef8-2f46-469a-92e8-82a1b224ebe9")
        self.assertEqual(self.server.links.bookmark, "https://preprod.ord.servers.api.rackspacecloud.com/5825921/servers/a9a74ef8-2f46-469a-92e8-82a1b224ebe9")


class ServerUpdateDomainJSONTest(object):

    def test_update_name(self):
        self.assertEqual(self.server_serial_name, '{"server": {"name": "new-server-test"}}')

    def test_update_address(self):
        self.assertEqual(self.server_serial_address, '{"server": {"accessIPv4": "67.23.10.132", "accessIPv6": "::babe:67.23.10.132"}}')


class ServerUpdateDomainXMLTest(object):

    def test_update_name(self):
        actual_element = ET.fromstring(self.server_serial_name)
        temp = '<?xml version="1.0" encoding="UTF-8"?><server name="new-server-test" xmlns="http://docs.openstack.org/compute/api/v1.1" />'
        comparable_element = ET.fromstring(temp)
        self.assertEqual(actual_element.attrib, comparable_element.attrib)

    def test_update_address(self):
        actual_element = ET.fromstring(self.server_serial_address)
        temp = '<?xml version="1.0" encoding="UTF-8"?><server accessIPv4="67.23.10.132" accessIPv6="::babe:67.23.10.132" xmlns="http://docs.openstack.org/compute/api/v1.1" />'
        comparable_element = ET.fromstring(temp)
        self.assertEqual(actual_element.attrib, comparable_element.attrib)


class ServerXMLDomainTest(unittest.TestCase, ServerDomainTest):

    @classmethod
    def setUpClass(cls):
        cls.server_xml = '<server xmlns:rax-bandwidth="http://docs.rackspace.com/servers/api/ext/server_bandwidth/" xmlns:OS-DCF="http://docs.openstack.org/compute/ext/disk_config/api/v1.1" xmlns:OS-EXT-STS="http://docs.openstack.org/compute/ext/extended_status/api/v1.1" xmlns:atom="http://www.w3.org/2005/Atom" xmlns="http://docs.openstack.org/compute/api/v1.1" status="ACTIVE" updated="2012-12-03T19:04:06Z" hostId="c70459909166c82b9fb53917dc665c44003c57b24d4a4015a3c8d108" name="testserver47476" created="2012-12-03T18:59:16Z" userId="199835" tenantId="5825921" accessIPv4="192.168.1.10" accessIPv6="2001:4801:7808:0052:2159:58b9:ff00:2154" progress="100" id="a9a74ef8-2f46-469a-92e8-82a1b224ebe9" OS-EXT-STS:vm_state="active" OS-EXT-STS:task_state="None" OS-EXT-STS:power_state="1" OS-DCF:diskConfig="AUTO"><image id="a10eacf7-ac15-4225-b533-5744f1fe47c1"><atom:link href="https://preprod.ord.servers.api.rackspacecloud.com/5825921/images/a10eacf7-ac15-4225-b533-5744f1fe47c1" rel="bookmark"/></image><flavor id="2"><atom:link href="https://preprod.ord.servers.api.rackspacecloud.com/5825921/flavors/2" rel="bookmark"/></flavor><metadata/><addresses><network id="public"><ip version="4" addr="198.61.236.10"/><ip version="6" addr="2001:4801:7811:0069:cf10:c02d:ff10:3ffa"/></network><network id="private"><ip version="4" addr="10.176.99.109"/></network></addresses><atom:link href="https://preprod.ord.servers.api.rackspacecloud.com/v2/5825921/servers/a9a74ef8-2f46-469a-92e8-82a1b224ebe9" rel="self"/><atom:link href="https://preprod.ord.servers.api.rackspacecloud.com/5825921/servers/a9a74ef8-2f46-469a-92e8-82a1b224ebe9" rel="bookmark"/><rax-bandwidth:bandwidth/></server>'
        cls.server = Server.deserialize(cls.server_xml, 'xml')


class ServerJSONDomainTest(unittest.TestCase, ServerDomainTest):

    @classmethod
    def setUpClass(cls):
        cls.server_json = '{"server": {"status": "ACTIVE", "updated": "2012-12-03T19:04:06Z", "hostId": "c70459909166c82b9fb53917dc665c44003c57b24d4a4015a3c8d108", "addresses": {"public": [{"version": 4, "addr": "198.61.236.10"}, {"version": 6, "addr": "2001:4801:7811:0069:cf10:c02d:ff10:3ffa"}], "private": [{"version": 4, "addr": "10.176.99.109"}]}, "links": [{"href": "https://preprod.ord.servers.api.rackspacecloud.com/v2/5825921/servers/a9a74ef8-2f46-469a-92e8-82a1b224ebe9", "rel": "self"}, {"href": "https://preprod.ord.servers.api.rackspacecloud.com/5825921/servers/a9a74ef8-2f46-469a-92e8-82a1b224ebe9", "rel": "bookmark"}], "image": {"id": "a10eacf7-ac15-4225-b533-5744f1fe47c1", "links": [{"href": "https://preprod.ord.servers.api.rackspacecloud.com/5825921/images/a10eacf7-ac15-4225-b533-5744f1fe47c1", "rel": "bookmark"}]}, "OS-EXT-STS:task_state": null, "OS-EXT-STS:vm_state": "active", "flavor": {"id": "2", "links": [{"href": "https://preprod.ord.servers.api.rackspacecloud.com/5825921/flavors/2", "rel": "bookmark"}]}, "id": "a9a74ef8-2f46-469a-92e8-82a1b224ebe9", "rax-bandwidth:bandwidth": [], "user_id": "199835", "name": "testserver47476", "created": "2012-12-03T18:59:16Z", "tenant_id": "5825921", "OS-DCF:diskConfig": "AUTO", "accessIPv4": "192.168.1.10", "accessIPv6": "2001:4801:7808:0052:2159:58b9:ff00:2154", "progress": 100, "OS-EXT-STS:power_state": 1, "metadata": {}}}'
        cls.server = Server.deserialize(cls.server_json, 'json')


class ServerUpdateJSONDomainTest(unittest.TestCase, ServerUpdateDomainJSONTest):

    @classmethod
    def setUpClass(cls):
        cls.server_json = '{"server": {"status": "ACTIVE", "updated": "2012-12-03T19:04:06Z", "hostId": "c70459909166c82b9fb53917dc665c44003c57b24d4a4015a3c8d108", "addresses": {"public": [{"version": 4, "addr": "198.61.236.10"}, {"version": 6, "addr": "2001:4801:7811:0069:cf10:c02d:ff10:3ffa"}], "private": [{"version": 4, "addr": "10.176.99.109"}]}, "links": [{"href": "https://preprod.ord.servers.api.rackspacecloud.com/v2/5825921/servers/a9a74ef8-2f46-469a-92e8-82a1b224ebe9", "rel": "self"}, {"href": "https://preprod.ord.servers.api.rackspacecloud.com/5825921/servers/a9a74ef8-2f46-469a-92e8-82a1b224ebe9", "rel": "bookmark"}], "image": {"id": "a10eacf7-ac15-4225-b533-5744f1fe47c1", "links": [{"href": "https://preprod.ord.servers.api.rackspacecloud.com/5825921/images/a10eacf7-ac15-4225-b533-5744f1fe47c1", "rel": "bookmark"}]}, "OS-EXT-STS:task_state": null, "OS-EXT-STS:vm_state": "active", "flavor": {"id": "2", "links": [{"href": "https://preprod.ord.servers.api.rackspacecloud.com/5825921/flavors/2", "rel": "bookmark"}]}, "id": "a9a74ef8-2f46-469a-92e8-82a1b224ebe9", "rax-bandwidth:bandwidth": [], "user_id": "199835", "name": "testserver47476", "created": "2012-12-03T18:59:16Z", "tenant_id": "5825921", "OS-DCF:diskConfig": "AUTO", "accessIPv4": "192.168.1.10", "accessIPv6": "2001:4801:7808:0052:2159:58b9:ff00:2154", "progress": 100, "OS-EXT-STS:power_state": 1, "metadata": {}}}'
        cls.server = Server.deserialize(cls.server_json, 'json')
        cls.server_serial_name = UpdateServer.serialize(UpdateServer(name="new-server-test"), 'json')
        cls.server_serial_address = UpdateServer.serialize(UpdateServer(accessIPv4="67.23.10.132", accessIPv6="::babe:67.23.10.132"), 'json')


class ServerUpdateXMLDomainTest(unittest.TestCase, ServerUpdateDomainXMLTest):

    @classmethod
    def setUpClass(cls):
        cls.server_xml = '<server xmlns:rax-bandwidth="http://docs.rackspace.com/servers/api/ext/server_bandwidth/" xmlns:OS-DCF="http://docs.openstack.org/compute/ext/disk_config/api/v1.1" xmlns:OS-EXT-STS="http://docs.openstack.org/compute/ext/extended_status/api/v1.1" xmlns:atom="http://www.w3.org/2005/Atom" xmlns="http://docs.openstack.org/compute/api/v1.1" status="ACTIVE" updated="2012-12-03T19:04:06Z" hostId="c70459909166c82b9fb53917dc665c44003c57b24d4a4015a3c8d108" name="testserver47476" created="2012-12-03T18:59:16Z" userId="199835" tenantId="5825921" accessIPv4="192.168.1.10" accessIPv6="2001:4801:7808:0052:2159:58b9:ff00:2154" progress="100" id="a9a74ef8-2f46-469a-92e8-82a1b224ebe9" OS-EXT-STS:vm_state="active" OS-EXT-STS:task_state="None" OS-EXT-STS:power_state="1" OS-DCF:diskConfig="AUTO"><image id="a10eacf7-ac15-4225-b533-5744f1fe47c1"><atom:link href="https://preprod.ord.servers.api.rackspacecloud.com/5825921/images/a10eacf7-ac15-4225-b533-5744f1fe47c1" rel="bookmark"/></image><flavor id="2"><atom:link href="https://preprod.ord.servers.api.rackspacecloud.com/5825921/flavors/2" rel="bookmark"/></flavor><metadata/><addresses><network id="public"><ip version="4" addr="198.61.236.10"/><ip version="6" addr="2001:4801:7811:0069:cf10:c02d:ff10:3ffa"/></network><network id="private"><ip version="4" addr="10.176.99.109"/></network></addresses><atom:link href="https://preprod.ord.servers.api.rackspacecloud.com/v2/5825921/servers/a9a74ef8-2f46-469a-92e8-82a1b224ebe9" rel="self"/><atom:link href="https://preprod.ord.servers.api.rackspacecloud.com/5825921/servers/a9a74ef8-2f46-469a-92e8-82a1b224ebe9" rel="bookmark"/><rax-bandwidth:bandwidth/></server>'
        cls.server = Server.deserialize(cls.server_xml, 'xml')
        cls.server_serial_name = UpdateServer.serialize(UpdateServer(name="new-server-test"), 'xml')
        cls.server_serial_address = UpdateServer.serialize(UpdateServer(accessIPv4="67.23.10.132", accessIPv6="::babe:67.23.10.132"), 'xml')

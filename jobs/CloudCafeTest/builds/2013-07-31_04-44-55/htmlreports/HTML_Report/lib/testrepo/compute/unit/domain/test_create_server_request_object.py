from ccengine.domain.compute.request.server_requests import CreateServer
import unittest2 as unittest
import base64
import xml.etree.ElementTree as ET


class CreateServerJSONDomainTest(object):

    def test_create_server_json(self):
        self.assertEqual(self.server_request_json, '{"server": {"name": "cctestserver", "image_ref": "a10eacf7 - ac15 - 4225 - b533 - 5744f1fe47c1", "flavorRef": "2", "OS-DCF:diskConfig": "AUTO", "diskConfig": "AUTO", "metadata": {"meta_key_1": "meta_value_1", "meta_key_2": "meta_value_2"}, "networks": [{"uuid": "4ebd35cf-bfe7-4d93-b0d8-eb468ce2245a"}, {"uuid": "00000000-0000-0000-0000-000000000000"}], "personality": [{"path": "/root/.csivh", "contents": "VGhpcyBpcyBhIHRlc3QgZmlsZS4="}]}}')


class CreateServerXMLDomainTest(object):

    def test_server_attributes(self):
        self.assertEqual(self.server_request_xml, {'flavorRef': '2', 'name': 'cctestserver', 'image_ref': 'a10eacf7 - ac15 - 4225 - b533 - 5744f1fe47c1', '{http://docs.openstack.org/compute/ext/disk_config/api/v1.1}diskConfig': 'AUTO'})

    def test_server_metadata_xml(self):
        meta_key_1 = self.server_request_xml_child[0]._children[0]
        meta_key_2 = self.server_request_xml_child[0]._children[1]

        self.assertEqual(meta_key_1.attrib['key'], 'meta_key_1')
        self.assertEqual(meta_key_1.text, 'meta_value_1')
        self.assertEqual(meta_key_2.attrib['key'], 'meta_key_2')
        self.assertEqual(meta_key_2.text, 'meta_value_2')

    def test_server_personality(self):
        file_path = self.server_request_xml_child[2]._children[0]
        self.assertEqual(file_path.attrib['path'], '/root/.csivh')
        self.assertEqual(file_path.text, 'VGhpcyBpcyBhIHRlc3QgZmlsZS4=')

    def test_server_network_xml(self):
        first_uuid = self.server_request_xml_child[1]._children[0]
        second_uuid = self.server_request_xml_child[1]._children[1]
        self.assertEqual(first_uuid.attrib['uuid'], "4ebd35cf-bfe7-4d93-b0d8-eb468ce2245a")
        self.assertEqual(second_uuid.attrib['uuid'], "00000000-0000-0000-0000-000000000000")


class CreateServerObjectJSON(unittest.TestCase, CreateServerJSONDomainTest):
    @classmethod
    def setUpClass(cls):
        networks = [{'uuid': "4ebd35cf-bfe7-4d93-b0d8-eb468ce2245a"}, {'uuid': "00000000-0000-0000-0000-000000000000"}]
        file_contents = 'This is a test file.'

        personality = [{'path': '/root/.csivh', 'contents':
                            base64.b64encode(file_contents)}]
        server_request_object = CreateServer(name='cctestserver', flavorRef='2',
                                             imageRef='a10eacf7 - ac15 - 4225 - b533 - 5744f1fe47c1',
                                             metadata={'meta_key_1': 'meta_value_1', 'meta_key_2': 'meta_value_2'},
                                             personality=personality, diskConfig='AUTO',
                                             networks=networks)
        cls.server_request_json = server_request_object.serialize('json')


class CreateServerObjectXML(unittest.TestCase, CreateServerXMLDomainTest):
    @classmethod
    def setUpClass(cls):
        network_list = [{'uuid': "4ebd35cf-bfe7-4d93-b0d8-eb468ce2245a"}, {'uuid': "00000000-0000-0000-0000-000000000000"}]
        file_contents = 'This is a test file.'

        personality = [{'path': '/root/.csivh', 'contents':
                            base64.b64encode(file_contents)}]
        server_request_object = CreateServer(name='cctestserver', flavorRef='2',
                                             imageRef='a10eacf7 - ac15 - 4225 - b533 - 5744f1fe47c1',
                                             metadata={'meta_key_1': 'meta_value_1', 'meta_key_2': 'meta_value_2'},
                                             personality=personality, diskConfig='AUTO', networks=network_list)
        cls.server_request = server_request_object.serialize('xml')
        root = ET.fromstring(cls.server_request)
        cls.server_request_xml = root.attrib
        cls.server_request_xml_child = root.getchildren()

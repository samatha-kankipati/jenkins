from ccengine.domain.compute.response.rescue import Rescue
import unittest2 as unittest


class RescueDomainTest(object):
    def test_adminpass(self):
        self.assertEqual(self.rescue_response.adminPass, 'eBHcCgGBVj6Z')


class testXMLDomainTest(unittest.TestCase, RescueDomainTest):

    @classmethod
    def setUpClass(cls):
        cls.rescue_xml = '<adminPass>eBHcCgGBVj6Z</adminPass>'
        cls.rescue_response = Rescue.deserialize(cls.rescue_xml, 'xml')


class testJSONDomainTest(unittest.TestCase, RescueDomainTest):

    @classmethod
    def setUpClass(cls):
        cls.rescue_json = '{"adminPass": "eBHcCgGBVj6Z"}'
        cls.rescue_response = Rescue.deserialize(cls.rescue_json, 'json')

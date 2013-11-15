import unittest
from testrepo.common.testfixtures.object_storage_fixture \
        import ObjectStorageTestFixture
from elementtree import ElementTree


"""
Adobe crossdomain.xml Test
http://www.adobe.com/devnet/articles/crossdomain_policy_file_spec.html
"""


class CrossdomainTest(ObjectStorageTestFixture):
    def test_crossdomain_xml_file_exists_with_valid_account(self):
        r = self.client.get_crossdomain_xml()
        self.assertEqual(r.status_code, 200, 'should return a xml file.')

        tree = ElementTree.fromstring(r.content)
        site_control = tree.find('site-control')
        self.assertNotEqual(site_control, None,
                'should contain a site-control node.')
        self.assertEqual(site_control.attrib[
                'permitted-cross-domain-policies'], 'master-only',
                'permitted-cross-domain-policies should be master-only.')

        allow_access_from = tree.find('allow-access-from')
        self.assertNotEqual(allow_access_from, None,
                'should contain a allow-access-from node.')
        self.assertEqual(allow_access_from.attrib['domain'], '*',
                'domain should be *.')

        allow_http_request_headers_from = tree.find(
                'allow-http-request-headers-from')
        self.assertNotEqual(allow_http_request_headers_from, None,
                'should contain a allow-http-request-headers-from node.')
        self.assertEqual(allow_http_request_headers_from.attrib['domain'], '*',
                'domain should be *.')
        self.assertEqual(allow_http_request_headers_from.attrib['headers'],
                '*', 'headers should be *.')

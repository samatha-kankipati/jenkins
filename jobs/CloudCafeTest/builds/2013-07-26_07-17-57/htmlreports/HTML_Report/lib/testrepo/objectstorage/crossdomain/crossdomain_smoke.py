import unittest
import zlib

from testrepo.common.testfixtures.object_storage_fixture \
        import ObjectStorageTestFixture


"""
Adobe crossdomain.xml Test
http://www.adobe.com/devnet/articles/crossdomain_policy_file_spec.html
"""


class CrossdomainSmokeTest(ObjectStorageTestFixture):
    def test_crossdomain_xml_file_exists_with_valid_account(self):
        r = self.client.get_crossdomain_xml()
        self.assertEqual(r.status_code, 200, 'should return a xml file.')

import hashlib
import requests

from testrepo.common.testfixtures.object_storage_fixture \
    import CloudFilesTestFixture
from ccengine.common.tools.datatools import CLOUDCAFE_DATA_DIRECTORY

MANUAL_TEST_OUTPUT_HEADER = \
    "=======================================" \
    "=======================================\n" \
    "= THIS IS A MANUAL TEST                " \
    "                                      =\n" \
    "=======================================" \
    "======================================="

MANUAL_TEST_OUTPUT_SEPARATOR = '=' * 80


class CDNUsageTest(CloudFilesTestFixture):
    @classmethod
    def read_file(slef, filename):
        """
        """
        f = open(CLOUDCAFE_DATA_DIRECTORY + filename, 'r')
        data = f.read()
        return data

    @classmethod
    def setUpClass(cls):
        super(CDNUsageTest, cls).setUpClass()
        cls.output = []
        cls.total_bandwidth_used = 0

        cls.container_name = cls.client.generate_unique_container_name()
        cls.client.create_cdn_container(cls.container_name, ttl='900')

        cls.object_name = 'ed_1024_512kb.mp4'
        object_data = cls.read_file(
            ''.join(['/objectstorage/video/', cls.object_name]))
        object_size = str(len(object_data))
        cls.client.set_storage_object(
            cls.container_name,
            cls.object_name,
            content_length=object_size,
            payload=object_data)

        m = hashlib.md5()
        m.update(object_data)
        cls.object_hash = m.hexdigest()

        cls.output.append(MANUAL_TEST_OUTPUT_HEADER)
        cls.output.append(''.join(['= original file name: ', cls.object_name]))
        cls.output.append(''.join(['= original file size: ', object_size]))
        cls.output.append(''.join(['= original file hash: ', cls.object_hash]))
        cls.output.append(''.join(['= container name: ', cls.container_name]))

    @classmethod
    def tearDownClass(cls):
        super(CDNUsageTest, cls).tearDownClass()

        cls.output.append(MANUAL_TEST_OUTPUT_SEPARATOR)
        cls.output.append(
            ''.join(['= total bandwidth out used: ',
            str(cls.total_bandwidth_used)]))
        cls.output.append(MANUAL_TEST_OUTPUT_SEPARATOR)
        cls.output.append('= WHAT TO DO NOW')
        cls.output.append(MANUAL_TEST_OUTPUT_SEPARATOR)
        cls.output.append(
            '= Log into stats server and verify that accumulated '
            'files match the numbers given.')
        cls.output.append(MANUAL_TEST_OUTPUT_SEPARATOR)

        for line in cls.output:
            print line

        cls.client.force_delete_containers([cls.container_name])

    def log_results(self, msg):
        CDNUsageTest.output.append(''.join(['= ', msg]))

    def update_bandwidth_used(self, amount):
        CDNUsageTest.total_bandwidth_used += int(amount)

    def test_generate_cdn_usage(self):
        r = self.client.get_object_via_cdn(
            self.container_name,
            self.object_name)
        m = hashlib.md5()
        m.update(r.content)
        h = m.hexdigest()
        self.assertEqual(
            self.object_hash, h, "cdn object should be identical.")

        self.log_results(MANUAL_TEST_OUTPUT_SEPARATOR)
        self.log_results(''.join(['cdn size: ', r.headers['content-length']]))
        self.log_results(''.join(['cdn hash: ', h]))
        self.update_bandwidth_used(r.headers['content-length'])

    def test_generate_cdn_ssl_usage(self):
        r = self.client.get_object_via_cdn_ssl(
            self.container_name,
            self.object_name)
        m = hashlib.md5()
        m.update(r.content)
        h = m.hexdigest()
        self.assertEqual(
            self.object_hash, h, "cdn ssl object should be identical.")

        self.log_results(MANUAL_TEST_OUTPUT_SEPARATOR)
        self.log_results(
            ''.join(['cdn ssl size: ', r.headers['content-length']]))
        self.log_results('cdn ssl hash: ' + h)
        self.update_bandwidth_used(r.headers['content-length'])

    def test_generate_cdn_streaming_usage(self):
        r = self.client.get_object_via_cdn(
            self.container_name, self.object_name)
        self.assertEquals(
            r.status_code, requests.codes.ok,
            "cdn object should stream.")

        self.log_results(MANUAL_TEST_OUTPUT_SEPARATOR)
        self.log_results(
            ''.join(['cdn streaming size: ', r.headers['content-length']]))
        self.update_bandwidth_used(r.headers['content-length'])

    def test_generate_cdn_ios_streaming_usage(self):
        rl = self.client.get_object_via_cdn_ios_streaming(
            self.container_name, self.object_name)
        bandwidth_used = 0
        for r in rl:
            bandwidth_used += int(r.headers['content-length'])

        self.log_results(MANUAL_TEST_OUTPUT_SEPARATOR)
        self.log_results(
            ''.join(['cdn ios streaming size: ', str(bandwidth_used)]))
        self.update_bandwidth_used(bandwidth_used)

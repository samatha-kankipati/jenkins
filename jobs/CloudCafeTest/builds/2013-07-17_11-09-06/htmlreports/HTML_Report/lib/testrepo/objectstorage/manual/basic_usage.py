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

SECONDS_CONTAINER_IS_VALID = 1205600


class BasicUsageTest(CloudFilesTestFixture):
    @classmethod
    def read_file(slef, filename):
        """
        """
        f = open(CLOUDCAFE_DATA_DIRECTORY + filename, 'r')
        data = f.read()
        return data

    @classmethod
    def setUpClass(cls):
        super(BasicUsageTest, cls).setUpClass()
        cls.output = []
        cls.total_bandwidth_used = 0

        r = cls.client.retrieve_account_metadata()
        account_size = r.headers['x-account-bytes-used']

        cls.container_name = cls.client.generate_unique_container_name()
        headers = {
            'X-Delete-After': SECONDS_CONTAINER_IS_VALID}
        cls.client.create_container(
            cls.container_name, headers=headers)

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
        cls.output.append(''.join(['= account size pre-run: ', account_size]))
        cls.output.append(''.join(['= original file name: ', cls.object_name]))
        cls.output.append(''.join(['= original file size: ', object_size]))
        cls.output.append(''.join(['= original file hash: ', cls.object_hash]))
        cls.output.append(''.join(['= container name: ', cls.container_name]))
        cls.output.append(''.join(
            ['= container delete after: ', str(SECONDS_CONTAINER_IS_VALID)]))

    @classmethod
    def tearDownClass(cls):
        super(BasicUsageTest, cls).tearDownClass()

        r = cls.client.retrieve_account_metadata()
        account_size = r.headers['x-account-bytes-used']

        cls.output.append(MANUAL_TEST_OUTPUT_SEPARATOR)
        cls.output.append(''.join(['= account size post-run: ', account_size]))
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

    def log_results(self, msg):
        BasicUsageTest.output.append(''.join(['= ', msg]))

    def update_bandwidth_used(self, amount):
        BasicUsageTest.total_bandwidth_used += int(amount)

    def test_generate_usage(self):
        r = self.client.get_storage_object(
            self.container_name,
            self.object_name)
        m = hashlib.md5()
        m.update(r.content)
        h = m.hexdigest()
        self.assertEqual(
            self.object_hash, h, "object should be identical.")

        self.log_results(MANUAL_TEST_OUTPUT_SEPARATOR)
        self.log_results(''.join(['http size: ', r.headers['content-length']]))
        self.log_results(''.join(['http hash: ', h]))
        self.update_bandwidth_used(r.headers['content-length'])

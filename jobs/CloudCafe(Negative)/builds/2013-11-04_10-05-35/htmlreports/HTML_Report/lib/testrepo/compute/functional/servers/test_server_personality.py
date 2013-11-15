from ccengine.common.tools.datagen import rand_name
import base64
from ccengine.common.exceptions.compute import OverLimit
from testrepo.common.testfixtures.compute import ComputeFixture
from ccengine.common.decorators import attr


class ServerPersonalityTest(ComputeFixture):

    limits_set = False

    @classmethod
    def setUpClass(cls):
        super(ServerPersonalityTest, cls).setUpClass()
        cls.home_folder = "c:\\" if cls.config.compute_api.os_type.lower() == 'windows' else "/etc/"
        cls.personality_file_limit = cls.limits_client.get_personality_file_limit()
        if cls.personality_file_limit is not None:
            cls.limits_set = True

    @attr(type='positive', net='yes')
    def test_personality_file_already_exists(self):
        """Check for a personality file which already exists in the created server"""
        file_contents = 'This is a test file.'
        personality = [{'path': '/etc/crontab', 'contents': base64.b64encode(file_contents)}]

        server_response = self.compute_provider.create_active_server(personality=personality)
        server = server_response.entity
        remote_client = self.compute_provider.get_remote_instance_client(server)

        self.assertEqual('This is a test file.',
                         remote_client.get_file_details('/etc/crontab').content,
                         "The personality file contents did not match")
        self.assertTrue(remote_client.is_file_present('/etc/crontab.bak.*'),
                        "The backup file was not created")

    @attr(type='negative', net='no')
    def test_personality_files_number_exceed_limit(self):
        """Server creation should fail if greater than the maximum allowed number of files are injected into the server"""
        name = rand_name('testserver')
        file_contents = 'This is a test file.'
        personality = []

        for i in range(0, int(self.personality_file_limit) + 1):
            path = self.home_folder + 'test' + str(i) + '.txt'
            personality.append({'path': path,
                                'contents': base64.b64encode(file_contents)})
        with self.assertRaises(OverLimit):
            server_response = self.servers_client.create_server(name, self.image_ref,
                                                                self.flavor_ref,
                                                                personality=personality)

    @attr(type='negative', net='no')
    def test_personality_file_name_exceeds_limit(self):
        """Server should not get created with a personality file whose name exceeds the max file name limit"""
        name = rand_name('testserver')
        test_name = '1234tester'
        file_contents = 'This is a test file.'
        filename_greater_than_255_chars = 25 * test_name + "abcdef"
        path = self.home_folder + 'test' + filename_greater_than_255_chars + '.txt'
        file_contents = 'This is a test file.'
        personality = [{'path': path, 'contents': base64.b64encode(file_contents)}]
        with self.assertRaises(OverLimit):
            server_response = self.servers_client.create_server(name, self.image_ref,
                                                                self.flavor_ref,
                                                                personality=personality)

    @attr(type='negative', net='no')
    def test_personality_file_size_exceeds_limit(self):
        """Server creation should fail if file size bigger than the maximum allowed file size is injected into the server"""
        name = rand_name('testserver')
        file_contents = ''
        personality = []
        max_file_size_limit = self.limits_client.get_personality_file_size_limit()
        while (len(file_contents) < int(max_file_size_limit) + 1):
            file_contents += 'a'
        path = self.home_folder + 'testPersonality.txt'
        personality.append({'path': path,
                            'contents': base64.b64encode(file_contents)})
        with self.assertRaises(OverLimit):
            server_response = self.servers_client.create_server(name, self.image_ref,
                                                                self.flavor_ref,
                                                                personality=personality)

    @attr(type='positive', net='yes')
    def test_can_create_server_with_max_number_of_files_as_personality_files(self):
        """Server should be created successfully if maximum allowed number of files is injected into the server during create as personality files"""
        file_names = []
        personality = []
        name = rand_name('testserver')
        file_contents = 'This is a test file.'

        file_limit = self.limits_client.get_personality_file_limit()

        for i in range(int(file_limit)):
            file_name = 'test' + str(i) + '.txt'
            path = self.home_folder + file_name
            file_names.append(path)
            personality.append({'path': path,
                                'contents': base64.b64encode(file_contents)})

        server_response = self.compute_provider.create_active_server(personality=personality)
        server = server_response.entity

        files_returned = self.compute_provider.get_remote_instance_client(server).get_files(self.home_folder + "test*.txt")

        for file_name in file_names:
            self.assertTrue(file_name in files_returned, "The file (%s) was not found in the server" % file_name)

    @attr(type='positive', net='yes')
    def test_personality_file_is_empty(self):
        """Check if the personality file does not have content when a server is created with such personality file"""
        name = rand_name('testserver')
        file_contents = ''
        path = self.home_folder + 'testempty'
        personality = [{'path': path, 'contents': base64.b64encode(file_contents)}]

        server_response = self.compute_provider.create_active_server(personality=personality)
        server = server_response.entity
        self.assertEqual('', self.compute_provider.get_remote_instance_client(server).get_file_details(path).content,
                         "The file contents was not empty")

from testrepo.common.testfixtures.compute import CreateServerFixture
from ccengine.domain.types import NovaServerStatusTypes
from ccengine.common.tools.datagen import rand_name
from ccengine.common.decorators import attr


class ChangeServerPasswordTests(CreateServerFixture):

    @classmethod
    def setUpClass(cls):
        super(ChangeServerPasswordTests, cls).setUpClass()
        cls.server = cls.server_response.entity
        cls.new_password = "newslice129690TuG72Bgj2"

        # Change password and wait for server to return to active state
        cls.compute_provider.change_password_and_await(cls.server.id,
                                                       cls.new_password)

    @classmethod
    def tearDownClass(cls):
        super(ChangeServerPasswordTests, cls).tearDownClass()

    @attr(type='smoke', net='yes')
    def test_can_log_in_with_new_password(self):
        '''Verify the admin user can log in with the new password'''

        '''Get server details '''
        response = self.servers_client.get_server(self.server.id)
        self.server = response.entity
        '''Set the server's adminPass attribute to the new password,vas this field is not set in getServer'''
        self.server.adminPass = self.new_password

        public_address = self.compute_provider.get_public_ip_address(self.server)
        '''Get an instance of the remote client '''
        remote_client = self.compute_provider.get_remote_instance_client(self.server, public_address)

        self.assertTrue(remote_client.can_connect_to_public_ip(),
                        "Could not connect to server (%s) using new admin password %s" %
                        (public_address, self.new_password))

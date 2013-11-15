from testrepo.common.testfixtures.compute import ComputeFixture
from ccengine.common.decorators import attr


class ServerClientTest(ComputeFixture):

    @classmethod
    def setUpClass(cls):
        super(ServerClientTest, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        super(ServerClientTest, cls).tearDownClass()

    def test_list_servers(self):
        self.servers_client.list_servers()
        self.servers_client.list_servers_with_detail()

    def test_list_images(self):
        self.images_client.list_images()
        self.images_client.list_images_with_detail()

    def test_list_flavors(self):
        self.flavors_client.list_flavors()
        self.flavors_client.list_flavors_with_detail()

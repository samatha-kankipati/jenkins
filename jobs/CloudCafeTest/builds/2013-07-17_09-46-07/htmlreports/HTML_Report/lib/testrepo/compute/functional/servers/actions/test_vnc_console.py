from ccengine.common.constants.compute_constants import VncConsoleTypes
from testrepo.common.testfixtures.compute import ComputeFixture
from ccengine.common.decorators import attr


class ServerVncConsoleTests(ComputeFixture):

    @classmethod
    def setUpClass(cls):
        super(ServerVncConsoleTests, cls).setUpClass()
        response = cls.compute_provider.create_active_server()
        cls.server = response.entity
        cls.resources.add(cls.server.id, cls.servers_client.delete_server)

    @attr(type='smoke', net='no')
    def test_get_xvpvnc_console(self):
        resp = self.vnc_client.get_vnc_console(
            self.server.id, VncConsoleTypes.XVPVNC)
        self.assertEqual(resp.status_code, 200)

        console = resp.entity
        self.assertEqual(console.type, VncConsoleTypes.XVPVNC)
        self.assertIsNotNone(console.url)

    @attr(type='smoke', net='no')
    def test_get_novnc_console(self):
        resp = self.vnc_client.get_vnc_console(
            self.server.id, VncConsoleTypes.NOVNC)
        self.assertEqual(resp.status_code, 200)

        console = resp.entity
        self.assertEqual(console.type, VncConsoleTypes.NOVNC)
        self.assertIsNotNone(console.url)

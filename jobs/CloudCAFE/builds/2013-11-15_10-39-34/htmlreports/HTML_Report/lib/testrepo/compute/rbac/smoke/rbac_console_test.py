from ccengine.common.decorators import attr
from ccengine.common.constants.compute_constants import VncConsoleTypes
from ccengine.common.exceptions.compute import Forbidden
from testrepo.common.testfixtures.compute import RbacComputeFixture


class ConsoleLimitsTest(RbacComputeFixture):

    @classmethod
    def setUpClass(cls):
        super(ConsoleLimitsTest, cls).setUpClass()
        # Common for Gets verification
        response = cls.compute_provider.create_active_server()
        cls.server = response.entity
        cls.resources.add(cls.server.id, cls.servers_client.delete_server)
    
    @attr(type='positive', net='no')
    def test_get_xvpvnc_console_admin_user(self):
        """Verify the response code and contents are correct for Admin"""
        resp = self.vnc_client.get_vnc_console(
            self.server.id, VncConsoleTypes.XVPVNC)
        self.assertEqual(resp.status_code, 200)

    @attr(type='positive', net='no')
    def test_get_novnc_console_admin_user(self):
        """Verify the response code and contents are correct for Admin"""
        resp = self.vnc_client.get_vnc_console(
            self.server.id, VncConsoleTypes.NOVNC)
        self.assertEqual(resp.status_code, 200)
    
    @attr(type='positive', net='no')
    def test_get_xvpvnc_console_creator_user(self):
        """Verify the response code and contents are correct for Creator"""
        with self.assertRaises(Forbidden):
            resp = self.creator_vnc_client.get_vnc_console(
                self.server.id, VncConsoleTypes.XVPVNC)

    @attr(type='positive', net='no')
    def test_get_novnc_console_creator_user(self):
        """Verify the response code and contents are correct for Creator"""
        with self.assertRaises(Forbidden):
            resp = self.creator_vnc_client.get_vnc_console(
                self.server.id, VncConsoleTypes.NOVNC)
    
    @attr(type='positive', net='no')
    def test_get_xvpvnc_console_observer_user(self):
        """Verify the response code and contents are correct for Observer"""
        with self.assertRaises(Forbidden):
            resp = self.observer_vnc_client.get_vnc_console(
                self.server.id, VncConsoleTypes.XVPVNC)

    @attr(type='positive', net='no')
    def test_get_novnc_console_observer_user(self):
        """Verify the response code and contents are correct for Observer"""
        with self.assertRaises(Forbidden):
            resp = self.observer_vnc_client.get_vnc_console(
                self.server.id, VncConsoleTypes.NOVNC)


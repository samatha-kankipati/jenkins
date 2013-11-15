#from ccengine.domain.compute.response.server import Server
from ccengine.domain.compute.request.server_requests import Reboot, Rebuild, Resize, \
    ConfirmResize, RevertResize, ResetState
from ccengine.domain.compute.request.server_requests import CreateImage, ChangePassword
from ccengine.domain.compute.request.server_requests import RescueMode, ExitRescueMode
import unittest2 as unittest
import xml.etree.ElementTree as ET
import base64


class AllActionJSONDomainTest(object):

    def test_server_reboot(self):
        self.assertEqual(self.reboot_json, '{"reboot": {"type": "HARD"}}')

    def test_server_rebuild(self):
        self.assertEqual(self.rebuild_json, '{"rebuild": {"name": "new-server-test", "image_ref": "d42f821e-c2d1-4796-9f07-af5ed7912d0e", "adminPass": "diane123", "flavorRef": "2", "OS-DCF:diskConfig": "AUTO", "diskConfig": "AUTO", "metadata": {"meta_key_1": "meta_value_1"}, "personality": [{"path": "/root/.csivh", "contents": "VGhpcyBpcyBhIHRlc3QgZmlsZS4="}]}}')

    def test_server_resize(self):
        self.assertEqual(self.resize_json, '{"resize": {"flavorRef": "3"}}')

    def test_server_image(self):
        self.assertEqual(self.image_json, '{"createImage": {"name": "new-image", "metadata": {"meta_key_1": "meta_value_1"}}}')

    def test_server_password(self):
        self.assertEqual(self.change_password_json, '{"changePassword": {"adminPass": "Test1234"}}')

    def test_server_rescue(self):
        self.assertEqual(self.rescue_json, '{"rescue": {}}')

    def test_server_exit_rescue(self):
        self.assertEqual(self.exit_rescue_json, '{"unrescue": {}}')

    def test_server_confirm_resize(self):
        self.assertEqual(self.confirm_resize_json, '{"confirmResize": {}}')

    def test_server_revert_resize(self):
        self.assertEqual(self.revert_resize_json, '{"revertResize": {}}')

    def test_server_reset_state(self):
        self.assertEqual(self.reset_state_json, '{"os-resetState": {"state": "error"}}')


class AllActionXMLDomainTest(object):

    def test_server_reboot(self):
        actual_element = ET.fromstring(self.reboot_xml)
        temp = '<?xml version="1.0" encoding="UTF-8"?><reboot type="HARD" xmlns="http://docs.openstack.org/compute/api/v1.1" />'
        comparable_element = ET.fromstring(temp)
        self.assertEqual(actual_element.attrib, comparable_element.attrib)

    def test_server_rebuild(self):
        actual_element = ET.fromstring(self.rebuild_xml)
        temp = '<?xml version="1.0" encoding="UTF-8"?><rebuild OS-DCF:diskConfig="AUTO" adminPass="diane123" flavorRef="2" image_ref="d42f821e-c2d1-4796-9f07-af5ed7912d0e" name="new-server-test" xmlns="http://docs.openstack.org/compute/api/v1.1" xmlns:OS-DCF="http://docs.openstack.org/compute/ext/disk_config/api/v1.1"><metadata><meta key="meta_key_1">meta_value_1</meta></metadata><personality><file path="/root/.csivh">VGhpcyBpcyBhIHRlc3QgZmlsZS4=</file></personality></rebuild>'
        comparable_element = ET.fromstring(temp)
        self.assertEqual(actual_element.attrib, comparable_element.attrib)

    def test_server_resize(self):
        actual_element = ET.fromstring(self.resize_xml)
        temp = '<?xml version="1.0" encoding="UTF-8"?><resize flavorRef="3" xmlns="http://docs.openstack.org/compute/api/v1.1" />'
        comparable_element = ET.fromstring(temp)
        self.assertEqual(actual_element.attrib, comparable_element.attrib)

    def test_server_image(self):
        actual_element = ET.fromstring(self.image_xml)
        temp = '<?xml version="1.0" encoding="UTF-8"?><createImage name="new-image" xmlns="http://docs.openstack.org/compute/api/v1.1" xmlns:atom="http://www.w3.org/2005/Atom"><metadata><meta key="meta_key_1">meta_value_1</meta></metadata></createImage>'
        comparable_element = ET.fromstring(temp)
        self.assertEqual(actual_element.attrib, comparable_element.attrib)

    def test_server_password(self):
        actual_element = ET.fromstring(self.change_password_xml)
        temp = '<?xml version="1.0" encoding="UTF-8"?><changePassword adminPass="Test1234" xmlns="http://docs.openstack.org/compute/api/v1.1" />'
        comparable_element = ET.fromstring(temp)
        self.assertEqual(actual_element.attrib, comparable_element.attrib)

    def test_server_rescue(self):
        actual_element = ET.fromstring(self.rescue_xml)
        temp = '<?xml version="1.0" encoding="UTF-8"?><rescue xmlns="http://docs.openstack.org/compute/ext/rescue/api/v1.1" />'
        comparable_element = ET.fromstring(temp)
        self.assertEqual(actual_element.attrib, comparable_element.attrib)

    def test_server_exit_rescue(self):
        actual_element = ET.fromstring(self.exit_rescue_xml)
        temp = '<?xml version="1.0" encoding="UTF-8"?><unrescue xmlns="http://docs.rackspacecloud.com/servers/api/v1.1" />'
        comparable_element = ET.fromstring(temp)
        self.assertEqual(actual_element.attrib, comparable_element.attrib)

    def test_server_confirm_resize(self):
        temp = '<?xml version="1.0" encoding="UTF-8"?><confirmResize xmlns="http://docs.openstack.org/compute/api/v1.1" xmlns:atom="http://www.w3.org/2005/Atom" />'
        comparable_element = ET.fromstring(temp)
        actual_element = ET.fromstring(self.confirm_resize_xml)
        self.assertEqual(actual_element.attrib, comparable_element.attrib)

    def test_server_revert_resize(self):
        temp = '<?xml version="1.0" encoding="UTF-8"?><revertResize xmlns="http://docs.openstack.org/compute/api/v1.1" xmlns:atom="http://www.w3.org/2005/Atom" />'
        comparable_element = ET.fromstring(temp)
        actual_element = ET.fromstring(self.revert_resize_xml)
        self.assertEqual(actual_element.attrib, comparable_element.attrib)

    def test_server_reset_state(self):
        actual_element = ET.fromstring(self.reset_state_xml)
        temp = '<?xml version="1.0" encoding="UTF-8"?><os-resetState state= "error" xmlns= "http://docs.openstack.org/compute/api/v1.1" />'
        comparable_element = ET.fromstring(temp)
        self.assertEqual(actual_element.attrib, comparable_element.attrib)


class ActionXMLDomainTest(unittest.TestCase, AllActionXMLDomainTest):

    @classmethod
    def setUpClass(cls):
        cls.file_contents = 'This is a test file.'
        cls.reboot_xml = Reboot.serialize(Reboot(reboot_type="HARD"), 'xml')
        cls.rebuild_xml = Rebuild.serialize(Rebuild(name="new-server-test",
                                                    imageRef="d42f821e-c2d1-4796-9f07-af5ed7912d0e",
                                                    flavorRef="2",
                                                    adminPass="diane123",
                                                    diskConfig="AUTO",
                                                    metadata={'meta_key_1': 'meta_value_1'},
                                                    personality=[{'path': '/root/.csivh', 'contents':
                                                                    base64.b64encode(cls.file_contents)}]), 'xml')
        cls.resize_xml = Resize.serialize(Resize(flavorRef="3"), 'xml')
        cls.image_xml = CreateImage.serialize(CreateImage(name="new-image", metadata={'meta_key_1': 'meta_value_1'}), 'xml')
        cls.change_password_xml = ChangePassword.serialize(ChangePassword(adminPassword="Test1234"), 'xml')
        cls.rescue_xml = RescueMode.serialize(RescueMode(), 'xml')
        cls.exit_rescue_xml = ExitRescueMode.serialize(ExitRescueMode(), 'xml')
        cls.confirm_resize_xml = ConfirmResize()
        cls.confirm_resize_xml = cls.confirm_resize_xml.serialize('xml')
        cls.revert_resize_xml = RevertResize()
        cls.revert_resize_xml = cls.revert_resize_xml.serialize('xml')
        cls.reset_state_xml = ResetState.serialize(ResetState('error'), 'xml')


class ActionJSONDomainTest(unittest.TestCase, AllActionJSONDomainTest):

    @classmethod
    def setUpClass(cls):
        cls.file_contents = 'This is a test file.'
        cls.reboot_json = Reboot.serialize(Reboot(reboot_type="HARD"), 'json')
        cls.rebuild_json = Rebuild.serialize(Rebuild(name="new-server-test",
                                                    imageRef="d42f821e-c2d1-4796-9f07-af5ed7912d0e",
                                                    flavorRef="2",
                                                    adminPass="diane123",
                                                    diskConfig="AUTO",
                                                    metadata={'meta_key_1': 'meta_value_1'},
                                                    personality=[{'path': '/root/.csivh', 'contents':
                                                                    base64.b64encode(cls.file_contents)}]), 'json')
        cls.resize_json = Resize.serialize(Resize(flavorRef="3"), 'json')
        cls.image_json = CreateImage.serialize(CreateImage(name="new-image", metadata={'meta_key_1': 'meta_value_1'}), 'json')
        cls.change_password_json = ChangePassword.serialize(ChangePassword(adminPassword="Test1234"), 'json')
        cls.rescue_json = RescueMode.serialize(RescueMode(), 'json')
        cls.exit_rescue_json = ExitRescueMode.serialize(ExitRescueMode(), 'json')
        cls.confirm_resize_json = ConfirmResize()
        cls.confirm_resize_json = cls.confirm_resize_json.serialize('json')
        cls.revert_resize_json = RevertResize()
        cls.revert_resize_json = cls.revert_resize_json.serialize('json')
        cls.reset_state_json = ResetState.serialize(ResetState('error'), 'json')

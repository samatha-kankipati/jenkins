from ccengine.common.decorators import attr
from testrepo.common.testfixtures.encore import EncoreFixture


class TestDeviceDetails(EncoreFixture):

    """@summary: Tests to verify Device Details"""

    @classmethod
    def setUpClass(cls):
        super(TestDeviceDetails, cls).setUpClass()
        cls.account_id = cls.config.encore.account_id
        cls.device_id = cls.config.encore.device_num

    @attr('smoke')
    def test_get_device_detail(self):
        """@summary: Verify detail of a given device"""
        response = self.encore_client.get_device(self.account_id,
                                                 self.device_id)
        device = response.entity
        self.assertEqual(response.status_code, 200,
                         "Status code {0} is not same as 200"
                         .format(response.status_code))
        self.assertEqual(int(self.device_id), device.computer_number,
                         "Device number {0} is not same as expected {1}"
                         .format(device.computer_number, self.device_id))

    @attr('smoke')
    def test_list_device_account(self):
        """@summary: Verify list of devices for an given account"""
        expected_length = 50
        response = self.encore_client.list_devices(self.account_id)
        self.assertEqual(response.status_code, 200,
                         "Status code {0} is not same as 200"
                         .format(response.status_code))
        device_list = response.entity
        self.assertEqual(len(device_list), expected_length,
                         "List of device {0} is not same as expected {1}"
                         .format(len(device_list), expected_length))

    @attr('smoke')
    def test_list_device_invalid_account(self):
        """@summary: Verify list of device for an invalid account"""
        invalid_account = 00000001
        response = self.encore_client.list_devices(invalid_account)
        self.assertEqual(response.status_code, 404,
                         "Status code {0} is not same as 404"
                         .format(response.status_code))

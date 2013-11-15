from testrepo.common.testfixtures.core import CoreFixture
from ccengine.common.decorators import attr


class TestComputerComputer(CoreFixture):

    @classmethod
    def setUpClass(cls):
        super(TestComputerComputer, cls).setUpClass()
        cls.computer = "218321"

    @attr(type='smoke')
    def test_update_computer_nickname(self):
        '''
        Test: Verify that user can update computer attributes
        '''
        response = self.computer_client.update_computer(self.computer,
                                                        "nickname", "test")
        self.assertEquals(response.status_code, 200)

    @attr(type='smoke')
    def test_get_networks(self):
        '''
        @summary: Verify user can get vlan, ip and network for device
        '''
        response = self.computer_client.get_networks(self.computer)
        self.assertEquals(response.status_code, 200)

    @attr(type='smoke')
    def test_get_skus_and_labels(self):
        '''
        @summary: Verify user can get skus and labels
        '''
        response = self.computer_client.get_skus_and_labels(self.computer)
        self.assertEquals(response.status_code, 200)

    @attr(type='smoke')
    def test_get_valid_skus_and_labels(self):
        '''
        @summary: Verify user can get valid skus and labels
        '''
        response = self.computer_client.get_valid_skus_and_labels(self.computer)
        self.assertEquals(response.status_code, 200)

    @attr(type='smoke')
    def test_get_computer_status_value_table_details(self):
        '''
        @summary: Verify Computer Status is a value table and returns statuses
        '''
        expected_computer_statuses = 50
        response = self.computer_client.get_computer_status_details()
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(response.entity), expected_computer_statuses,
                          "There should be {0} computer statuses"
                          .format(len(response.entity)))

    @attr(type='smoke')
    def test_hypervisor_attribute_returns_null_for_non_hypervisor_device(self):
        '''
        @summary: Verify Computer.Computer.hypervisor is returning null,\
        for non Hypervisor computers
        '''
        attribute_name = "hypervisor"
        response = self.computer_client.\
                        get_computer_attribute(self.computer,
                                               attribute=attribute_name)

        self.assertTrue(response.content == "null", "Response is not null")

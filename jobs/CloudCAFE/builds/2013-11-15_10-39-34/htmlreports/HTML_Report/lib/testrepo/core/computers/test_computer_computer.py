from ccengine.common.decorators import attr
from ccengine.domain.core.request.core_request import WhereEquals
from testrepo.common.testfixtures.core import CoreFixture


class TestComputerComputer(CoreFixture):

    @classmethod
    def setUpClass(cls):
        super(TestComputerComputer, cls).setUpClass()
        cls.computer = cls.config.core.computer_id
        cls.employee_number = cls.config.core.employee_num
        cls.account = cls.config.core.account_id
        cls.special_account = cls.config.core.special_account_id
        cls.support_team_name = cls.config.core.support_team_name
        cls.support_team_id = cls.config.core.support_team_id

    @attr(suite='smoke', type='positive')
    def test_update_computer_nickname(self):
        """
        Test: Verify that user can update computer attributes
        """
        new_nickname = "testAutomataion"
        response = self.computer_client.update_computer(
            self.computer, "nickname", new_nickname)
        self.assertEquals(response.status_code, 200)
        updated_name = self.computer_client.get_computer_attribute(
            self.computer, "nickname").entity
        self.assertEqual(updated_name, new_nickname, "Nickname did not got \
                         updated to {0}".format(new_nickname))

    @attr(suite='smoke', type='positive')
    def test_get_networks(self):
        """ @summary: Verify user can get vlan, ip and network for device """
        response = self.computer_client.get_networks(self.computer)
        self.assertEquals(response.status_code, 200)
        managed_backup = getattr(response.entity, 'Managed Backup')
        self.assertIsNotNone(managed_backup['ip'], "Ip is not returned")
        self.assertIsNotNone(managed_backup['vlan'], "vlan is not returned")
        self.assertIsNotNone(managed_backup['network'],
                             "network is not returned")

    @attr(suite='smoke', type='positive')
    def test_get_skus_and_labels(self):
        """ @summary: Verify user can get list of sku with id, label,
        display_label and description for this computer's parts """
        response = self.computer_client.get_skus_and_labels(self.computer)
        self.assertEquals(response.status_code, 200)
        expected_sku_ele = [100282, 'ip_num', 'IP Addresses', 'Number of IPs']
        actual_sku_element = response.entity[0]
        self.assertEqual(len(response.entity), 22, "Number of sku got changed")
        self.assertEqual(actual_sku_element, expected_sku_ele,
                         "Actual sku element {0} is not same as expected {1}"
                         .format(actual_sku_element, expected_sku_ele))

    @attr(suite='smoke', type='positive')
    def test_get_valid_skus_and_labels(self):
        """@summary: Verify user can get list of skunits and skus"""
        response = self.computer_client.get_valid_skus_and_labels(self.computer)
        self.assertEquals(response.status_code, 200)
        self.assertEqual(len(response.entity), 70,
                         "Number of skuunits got changed")

    @attr(suite='smoke', type='positive')
    def test_get_computer_status_value_table_details(self):
        """
        @summary: Verify Computer Status is a value table and returns statuses
        """
        expected_computer_statuses = 50
        response = self.computer_client.get_computer_status_details()
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(response.entity), expected_computer_statuses,
                          "There should be {0} computer statuses"
                          .format(len(response.entity)))

    @attr(suite='smoke', type='positive')
    def test_hypervisor_attribute_returns_null_for_non_hypervisor_device(self):
        """
        @summary: Verify Computer.Computer.hypervisor is returning null,
        for non Hypervisor computers
        """
        computer = 218321
        attribute_name = "hypervisor"
        response = \
            self.computer_client.get_computer_attribute(
                computer, attribute=attribute_name)
        self.assertTrue(response.content == "null", "Response is not null")

    @attr(suite='smoke', type='positive')
    def test_set_sales_representive(self):
        """
        @summary: Verify user can set a sales representative for a given server
        """
        response = self.computer_client.set_sales_rep(self.computer,
                                                      self.employee_number)
        self.assertEqual(200, response.status_code,
                         "Status code {0} is not same as 200"
                         .format(response.status_code))
        sales_rep = self.computer_client.get_computer_attribute(self.computer,
                                                       'sales_representative')
        sales_rep_id = sales_rep.entity['load_value']
        sales_rep = self.contact_client.get_contact_attribute(sales_rep_id,
                                                       'employee_number')
        self.assertEqual(sales_rep.entity, self.employee_number,
                         "expected sales rep {0} is not same as actual {1}"
                         .format(self.employee_number, sales_rep.entity))

    @attr(suite='regression', type='negative')
    def test_set_invalid_sales_representive(self):
        """
        @summary: Verify user gets an error message while setting an
        invalid sales representative number for a given server
        """
        employee_number = 1325345435
        response = self.computer_client.set_sales_rep(self.computer,
                                                      employee_number)
        self.assertEqual(500, response.status_code,
                         "Status code {0} is not same as 500"
                         .format(response.status_code))

    @attr(suite='regression', type='negative')
    def test_set_sales_representive_invalid_server(self):
        """
        @summary: Verify user gets an error message while setting an
        sales representative number for a invalid server
        """
        server_id = 517886000
        response = self.computer_client.set_sales_rep(server_id,
                                                      self.employee_number)
        self.assertEqual(404, response.status_code,
                         "Status code {0} is not same as 404"
                         .format(response.status_code))

    @attr(suite='smoke', type='positive')
    def test_verify_computer_all_attributes_using_computerWhere(self):
        """
        @summary: Verify user can get the attributes of Computer.Computer class
        using computerWhere method
        """
        where_condition = WhereEquals("number", self.computer)
        attributes = ["number", "vlans", "dedicated_san_list", "is_server",
                      "admin_ip", "aggexnet_vlans", "attached_san_or_das",
                      "das_iscsi_config_list", "zone"]
        response = self.computer_client.\
                get_computer_attributes_using_computerwhere(
                     where_condition, attributes, limit=None, offset=None)
        self.assertEqual(200, response.status_code,
                         "Response status code is not 200")
        computer_details = response.entity[0]
        self.assertEqual(self.computer, computer_details.number,
                         "Computer number {0} is not same as expected {1}"
                         .format(int(computer_details.number), self.computer))
        self.assertTrue(computer_details.is_server, True)

    @attr(suite='smoke', type='positive')
    def test_add_aggexnet_vlan(self):
        """
        @summary: Verify addAggExNetvlan method in Computer.Computer class
        """
        vlan = 1
        response = self.computer_client.add_aggexnet_vlan(self.computer, vlan)
        self.assertEquals(response.status_code, 200)
        self.assertEqual(response.entity.success, True, "message")

    @attr(suite='smoke', type='positive')
    def test_add_das_disk_group(self):
        """
        @summary: Verify addDASdiskgroup method in Computer.Computer class
        """
        disk_group_id = 1
        raid_level = 1
        disk_count = 1
        disk_size = 1
        response = self.computer_client.add_das_disk_group(
            self.computer, disk_group_id, raid_level, disk_count, disk_size)
        self.assertEquals(response.status_code, 200)

    @attr(suite='smoke', type='positive')
    def test_add_das_iscsi_conf(self):
        """
        @summary: Verify addDASISCSIconf method in Computer.Computer class
        """
        ip_address = "10.5.255.1"
        das_switch_port = 1
        das_port = 1
        das_iqn = 1
        vlan_id = 514
        response = self.computer_client.add_das_iscsi_conf(self.computer,
                                                           ip_address,
                                                           das_switch_port,
                                                           das_port,
                                                           das_iqn,
                                                           vlan_id)
        self.assertEquals(response.status_code, 200)

    @attr(suite='smoke', type='positive')
    def test_add_dedicated_san(self):
        """
        @summary: Verify addDedicatedSan method in Computer.Computer class
        """
        lun_id = 1
        raid_level = 1
        mount_point = 1
        hlu = 3
        disk_type = 1
        capacity = 1
        hosts = 1
        storage_array = 1
        response = self.computer_client.add_dedicated_san(self.computer,
                                                          lun_id,
                                                          raid_level,
                                                          mount_point,
                                                          hlu,
                                                          disk_type,
                                                          capacity,
                                                          hosts,
                                                          storage_array)
        self.assertEquals(response.status_code, 200)

    @attr(suite='smoke', type='positive')
    def test_add_host_iscsi_conf(self):
        """
        @summary: Verify addHostISCSIconf method in Computer.Computer class
        """
        ip_address = "10.5.255.1"
        host = 2
        port = 2
        host_iqn = 1
        pci_slot = 1
        response = self.computer_client.add_host_iscsi_conf(
            self.computer, ip_address, host, port, host_iqn, pci_slot)
        self.assertEquals(response.status_code, 200)

    @attr('failed')
    def test_add_hot_spare(self):
        """@summary: Verify addHotSpare method in Computer.Computer class"""
        quantity = 1
        slot = 1
        size = 2
        response = self.computer_client.add_hot_spare(
            self.computer, quantity, slot, size)
        self.assertEquals(response.status_code, 200)

    @attr(suite='smoke', type='positive')
    def test_add_managed_storage(self):
        """
        @summary: Verify addManagedStorage method in Computer.Computer class
        """
        lun_id = 1
        raid_level = 1
        storage_group_name = "DFW1-922 Group 1"
        uuid = 1
        purpose = 1
        capacity = 1
        host_name = 1
        storage_array = 1
        response = self.computer_client.add_managed_storage(self.computer,
                                                            lun_id,
                                                            uuid,
                                                            raid_level,
                                                            storage_group_name,
                                                            storage_array,
                                                            purpose,
                                                            host_name,
                                                            capacity)
        self.assertEquals(response.status_code, 200)
        response_storage = response.entity.load_value
        managed_storage_details = \
            self.computer_client.get_managedstorage_attribute(
                response_storage, "storage_group_name").entity
        self.assertEqual(managed_storage_details, storage_group_name,
                         "Expected storage group name {0} does not match with\
                         the actual storage group name {1}"
                         .format(storage_group_name, managed_storage_details))

    @attr('pending-smoke')
    def test_add_rpa_cluster_config(self):
        """
        @summary: Verify addRPAClusterConfig method in Computer.Computer class
        """
        target_lun_id = 1
        source_lun_id = 1
        raid_level = 1
        mount_point = 1
        hlu = 1
        disk_type = 1
        capacity = 1
        hosts = 1
        storage_array = 1
        response = self.computer_client.add_rpa_cluster_config(self.computer,
                                                               target_lun_id,
                                                               source_lun_id,
                                                               raid_level,
                                                               mount_point,
                                                               hlu,
                                                               disk_type,
                                                               capacity,
                                                               hosts,
                                                               storage_array)
        self.assertEquals(response.status_code, 200)

    @attr('Pending-smoke')
    def test_add_replace_part(self):
        """
        @summary: Verify addReplacePart method in Computer.Computer class
        """
        sku = 1
        skunit = 1
        response = self.computer_client.\
            add_replace_part(self.computer, sku, skunit)
        self.assertEquals(response.status_code, 200)

    @attr(suite='smoke', type='positive')
    def test_change_status_with_mandatory_params(self):
        """@summary: Verify changeStatus method in Computer.Computer class"""
        new_status = 70
        computer = 477574
        reason = "Upgraded via test automation"
        self.computer_client.change_status(computer=computer,
                                           new_status=new_status,
                                           reason=reason)
        get_status = self.computer_client.get_computer_attribute(computer,
                                                                 "status")
        self.assertEqual(new_status, get_status.entity.get('id'),
                         "updated status is same as new status")
        new_status = 12
        update_status = self.computer_client.change_status(computer=computer,
                                                           new_status=new_status,
                                                           reason=reason)
        self.assertEquals(update_status.status_code, 200)

    @attr(suite='smoke', type='positive')
    def test_change_status_with_optional_params(self):
        """
        @summary: Verify changeStatus method in Computer.Computer class
        with optional parameter
        """
        new_status = 70
        computer = 477574
        included_bandwidth = 4000
        mrr_currency = "US Dollar"
        reason = "Upgraded via test automation"
        response = \
            self.computer_client.\
                change_status(computer=computer,
                              new_status=new_status,
                              reason=reason,
                              included_bandwidth=included_bandwidth,
                              mrr_currency=mrr_currency)
        self.assertEquals(response.status_code, 200)
        get_status = self.computer_client.get_computer_attribute(computer,
                                                                 "status")
        updated_status = get_status.entity.get('id')
        self.assertEqual(new_status, updated_status,
                         "updated status {0} is same as new status {1}\
                         ".format(new_status, updated_status))
        new_status = 12
        self.computer_client.change_status(computer=computer,
                                           new_status=new_status,
                                           reason=reason)

    @attr(suite='smoke', type='positive')
    def test_clone(self):
        """
        @summary: Verify clone method with mandatory parameters
        in Computer.Computer class
        """
        response = self.computer_client.clone(self.computer)
        self.assertEquals(response.status_code, 200)

    @attr('Pending-smoke')
    def test_clone_with_all_params(self):
        """
        @summary: Verify clone method with optional parameters in
        Computer.Computer class
        """
        name = "clone1"
        datacenter = "DFW1"
        response = self.computer_client.clone(self.computer,
                                              name,
                                              self.account,
                                              datacenter)
        self.assertEquals(response.status_code, 200)

    @attr('Pending-smoke')
    def test_remove_Managed_Storage(self):
        """
        @summary: Verify removeManagedStorage method  in Computer.Computer
        class
        """
        ms = 1
        response = self.computer_client.remove_managed_storage(self.computer,
                                                               ms)
        self.assertEquals(response.status_code, 200)

    @attr('Pending-smoke')
    def test_remove_part(self):
        """
        @summary: Verify removePart method  in Computer.Computer class
        """
        skunit_name = 1
        product = 1
        response = self.computer_client.remove_part(self.computer,
                                                    skunit_name,
                                                    product)
        self.assertEquals(response.status_code, 200)

    @attr('failed')
    def test_status_change_notice(self):
        """
        @summary: Verify statusChangeNotice method  in Computer.Computer class
        """
        new_status = 4
        response = self.computer_client.status_change_notice(self.computer,
                                                             new_status)
        self.assertEquals(response.status_code, 200)

    @attr('Pending-smoke')
    def test_virtual_machine_on_off(self):
        """
        @summary: Verify virtualMachineOnOff method  in Computer.Computer class
        """
        new_status = 1
        response = self.computer_client.virtual_machine_on_off(
            self.computer, new_status, suspended_if_vm_inactive=0)
        self.assertEquals(response.status_code, 200)

    @attr("failed")
    def test_verify_ComputerOffline_attributes_ComputerOfflineWhere(self):
        """
        @summary: Verify user can query computer attributes using
        ComputerOfflineWhere method in Computer.Computer class
        """
        where_condition = WhereEquals("number", 3149)
        attributes = ["status"]
        computer_details = self.computer_client.\
                get_computeroffline_attributes_using_computerofflinewhere(
                    where_condition, attributes, limit=None, offset=None)
        self.assertEqual(200, computer_details.status_code,
                         "Response status code is not 200")

    @attr(suite='smoke', type='positive')
    def test_computer_details_with_support_team(self):
        """
        @summary: Verify the user can query computer number and account with a valid
        account and valid support team name
        """
        support_team_name = self.support_team_name
        where_condition = WhereEquals("account", self.special_account)\
                          .AND(WhereEquals("support_team", support_team_name))
        attributes = ["number", "account"]
        response = self.computer_client.\
            get_computer_attributes_using_computerwhere(
                where_condition, attributes, limit=None, offset=None)
        self.assertEqual(200, response.status_code,
                         "Response status code is not 200")
        computers_list = response.entity
        for computer in computers_list:
            comp_account = computer.account.get("load_value")
            self.assertEqual(comp_account, self.special_account,
                             "Account number is not same as expected"
                             .format(self.special_account, comp_account))

    @attr(suite='smoke', type='positive')
    def test_computer_details_with_support_team_id(self):
        """
        @summary: Verify the user can query computer number and computer account
        with a valid account and valid support team id
        """
        support_team_id = self.support_team_id
        where_condition = WhereEquals("account", self.special_account)\
                          .AND(WhereEquals("support_team_id", support_team_id))
        attributes = ["number", "account"]
        response = self.computer_client.\
            get_computer_attributes_using_computerwhere(
                where_condition, attributes, limit=None, offset=None)
        self.assertEqual(200, response.status_code,
                         "Response status code is not 200")
        computers_list = response.entity
        for computer in computers_list:
            comp_account = computer.account.get("load_value")
            self.assertEqual(comp_account, self.special_account,
                             "Account number is not same as expected"
                             .format(self.special_account, comp_account))

    @attr(suite='regression', type='negative')
    def test_computer_details_invalid_account_valid_supportid(self):
        """
        @summary: Verify the user gets an 400 error code, while querying
        computer details with a invalid account and valid support team id
        """
        invalid_account = 54251
        support_team_id = self.support_team_id
        where_condition = WhereEquals("account", invalid_account)\
                          .AND(WhereEquals("support_team_id", support_team_id))
        response = self.computer_client.\
            get_computer_attributes_using_computerwhere(
                where_condition, limit=None, offset=None)
        self.assertEqual(400, response.status_code,
                         "Response status code should be {0}"
                         .format(response.status_code))

    @attr(suite='regression', type='negative')
    def test_computer_details_valid_account_invalid_support_id(self):
        """
        @summary: Verify the user gets an 400 error code, while querying
        computer details with a valid account and invalid support team name
        """
        account = self.account
        support_team_id = 54254111
        where_condition = WhereEquals("account", account)\
                          .AND(WhereEquals("support_team_id", support_team_id))
        response = self.computer_client.\
            get_computer_attributes_using_computerwhere(
                where_condition, limit=None, offset=None)
        self.assertEqual(200, response.status_code,
                         "Response status code should be {0}"
                         .format(response.status_code))
        self.assertEqual(len(response.entity), 0,
                        "Computer list should be empty")

    @attr(suite='regression', type='negative')
    def test_computer_details_with_invalid_support_id(self):
        """
        @summary: Verify the user gets an empty list, while querying computer
        details with a invalid support team id
        """
        support_team_id = 54254111
        where_condition = WhereEquals("support_team_id", support_team_id)
        response = self.computer_client.\
            get_computer_attributes_using_computerwhere(
                where_condition, limit=None, offset=None)
        self.assertEqual(200, response.status_code,
                         "Response status code should be {0}"
                         .format(response.status_code))
        self.assertEqual(len(response.entity), 0,
                        "Computer list should be empty")

    @attr(suite='regression', type='negative')
    def test_computer_details_with_invalid_support_id_type(self):
        """
        @summary: Verify the user gets an 400 response code, while querying
        computer details with a invalid type support team id
        """
        support_team_id = "ABCDEF"
        where_condition = WhereEquals("support_team_id", support_team_id)
        response = self.computer_client.\
            get_computer_attributes_using_computerwhere(
                where_condition, limit=None, offset=None)
        self.assertEqual(400, response.status_code,
                         "Response status code should be {0}"
                         .format(response.status_code))

    @attr(suite='regression', type='negative')
    def test_computer_details_with_invalid_account(self):
        """
        @summary: Verify the user gets an 400 error code, while querying
        computer details with a invalid account
        """
        invalid_account = 54251
        where_condition = WhereEquals("account", invalid_account)
        response = self.computer_client.\
            get_computer_attributes_using_computerwhere(
                where_condition, limit=None, offset=None)
        self.assertEqual(400, response.status_code,
                         "Response status code should be {0}"
                         .format(response.status_code))

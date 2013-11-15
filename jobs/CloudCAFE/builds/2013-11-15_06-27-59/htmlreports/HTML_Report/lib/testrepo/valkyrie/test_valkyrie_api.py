import json

from testrepo.common.testfixtures.compute import ComputeFixture
from testrepo.common.testfixtures.valkyrie import ValkyrieFixture
from ccengine.common.tools.datagen import rand_name


class ValkyrieTests(ValkyrieFixture, ComputeFixture):

    @classmethod
    def setUpClass(cls):
        super(ValkyrieTests, cls).setUpClass()
        cls.dedicated_account = cls.valkyrie_provider.dedicated_account
        cls.cloud_account = cls.valkyrie_provider.cloud_account
        active_server_response = cls.compute_provider.create_active_server(
            name=rand_name('ValkyrieServer'))
        cls.server = active_server_response.entity
        cls.resources.add(cls.server.id,
                          cls.servers_client.delete_server)
        cls.managed_cloud_timeout = cls.config.managedcloud. \
            managed_cloud_timeout

    @classmethod
    def tearDownClass(cls):
        super(ValkyrieTests, cls).tearDownClass()

    def test_get_account_details(self):
        account_details = self.valkyrie_provider.valkyrie_client.\
            get_dedicated_account_details(
                account_id=self.dedicated_account).entity
        self.assertIsNotNone(account_details.primary_contact_id,
                             msg="Blank Account ID")

    def test_list_contacts(self):
        account_contacts_response = self.valkyrie_provider.valkyrie_client. \
            list_contacts(account_id=self.dedicated_account)
        account_contacts = account_contacts_response.entity
        self.assertGreater(len(account_contacts), 0, msg='Empty contact list')
        self.assertIsNotNone(account_contacts[0].emails,
                             msg="No account email provided")
        self.assertIsNotNone(account_contacts[0].contact_id,
                             msg="No account contact id provided")
        self.assertIsNotNone(account_contacts[0].role_id,
                             msg="No account contact role provided")

    def test_list_inventory(self):
        inventory_list = self.valkyrie_provider.valkyrie_client.list_inventory(
            account_id=self.dedicated_account).entity
        self.assertGreater(len(inventory_list), 0, msg='Empty inventory list')
        self.assertIsNotNone(inventory_list[0].id,
                             msg="No device id is returned")
        self.assertIsNotNone(inventory_list[0].type,
                             msg="No device type is returned")
        self.assertIsNotNone(inventory_list[0].datacenter,
                             msg="No data center is returned")
        self.assertIsNotNone(inventory_list[0].parts,
                             msg="No data parts is returned")

    def test_get_inventory_details(self):
        device_id = self.valkyrie_provider.valkyrie_client.list_inventory(
            account_id=self.dedicated_account).entity[0].id
        device = self.valkyrie_provider.valkyrie_client.get_inventory_details(
            account_id=self.dedicated_account,
            inventory_id=device_id).entity
        self.assertIsNotNone(device.id, msg="No device id is returned")
        self.assertIsNotNone(device.type, msg="No device type is returned")
        self.assertIsNotNone(device.datacenter, msg="No data center returned")
        self.assertIsNotNone(device.parts, msg="No data parts is returned")

    def test_list_server_inventory(self):
        inventory_list = self.valkyrie_provider.valkyrie_client. \
            list_server_category_inventory(
                account_id=self.dedicated_account).entity
        self.assertGreater(len(inventory_list), 0, msg="Empty Server List")
        self.assertIsNotNone(inventory_list[0].id,
                             msg="No device id is returned")
        self.assertIsNotNone(inventory_list[0].type,
                             msg="No device type is returned")
        self.assertIsNotNone(inventory_list[0].datacenter,
                             msg="No data center is returned")
        self.assertIsNotNone(inventory_list[0].parts,
                             msg="No data parts is returned")

    def test_get_server(self):
        inventory_list = self.valkyrie_provider.valkyrie_client. \
            list_server_category_inventory(
                account_id=self.dedicated_account).entity
        server_details = self.valkyrie_provider.valkyrie_client. \
            get_server_inventory(self.dedicated_account,
                                 inventory_list[0].id).entity
        self.assertIsNotNone(server_details.type,
                             msg="No device type is returned")
        self.assertIsNotNone(server_details.datacenter,
                             msg="No data center is returned")
        self.assertIsNotNone(server_details.parts,
                             msg="No data parts is returned")

    def test_list_network_inventory(self):
        inventory_list = self.valkyrie_provider.valkyrie_client. \
            list_network_category_inventory(
                account_id=self.dedicated_account).entity
        self.assertGreater(len(inventory_list), 0, msg="Empty Network List")
        self.assertIsNotNone(inventory_list[0].id,
                             msg="No network id is returned")
        self.assertIsNotNone(inventory_list[0].type,
                             msg="No network type is returned")
        self.assertIsNotNone(inventory_list[0].datacenter,
                             msg="No network data center is returned")
        self.assertIsNotNone(inventory_list[0].parts,
                             msg="No network parts is returned")

    def test_get_network(self):
        inventory_list = self.valkyrie_provider.valkyrie_client. \
            list_network_category_inventory(
                account_id=self.dedicated_account).entity
        network_details = self.valkyrie_provider.valkyrie_client. \
            get_network_inventory(self.dedicated_account,
                                  inventory_list[0].id).entity
        self.assertIsNotNone(network_details.id,
                             msg="No network id is returned")
        self.assertIsNotNone(network_details.type,
                             msg="No network type is returned")
        self.assertIsNotNone(network_details.datacenter,
                             msg="No network data center is returned")
        self.assertIsNotNone(network_details.parts,
                             msg="No network parts is returned")

    def test_list_service_inventory(self):
        inventory_list = self.valkyrie_provider.valkyrie_client. \
            list_service_category_inventory(
                account_id=self.dedicated_account).entity
        self.assertGreater(len(inventory_list), 0, msg="Empty Services List")
        self.assertIsNotNone(inventory_list[0].id,
                             msg="No service id is returned")
        self.assertIsNotNone(inventory_list[0].type,
                             msg="No network type is returned")
        self.assertIsNotNone(inventory_list[0].permissions,
                             msg="No permissions is returned")
        self.assertIsNotNone(inventory_list[0].parts,
                             msg="No network parts is returned")

    def test_get_service(self):
        inventory_list = self.valkyrie_provider.valkyrie_client. \
            list_service_category_inventory(
                account_id=self.dedicated_account).entity
        service_details = self.valkyrie_provider.valkyrie_client. \
            get_service_inventory(self.dedicated_account,
                                  inventory_list[0].id).entity

        self.assertIsNotNone(service_details.id,
                             msg="No service id is returned")
        self.assertIsNotNone(service_details.type,
                             msg="No service type is returned")
        self.assertIsNotNone(service_details.permissions,
                             msg="No permissions is returned")
        self.assertIsNotNone(service_details.parts,
                             msg="No service parts is returned")

    def test_list_storage_inventory(self):
        inventory_list = self.valkyrie_provider.valkyrie_client. \
            list_storage_category_inventory(
                account_id=self.dedicated_account).entity
        self.assertGreater(len(inventory_list), 0, msg="Empty Storage List")
        self.assertIsNotNone(inventory_list[0].id is not None,
                             msg="No storage id is returned")
        self.assertIsNotNone(inventory_list[0].type,
                             msg="No storage type is returned")
        self.assertIsNotNone(inventory_list[0].permissions,
                             msg="No storage permissions is returned")
        self.assertIsNotNone(inventory_list[0].parts,
                             msg="No storage  parts is returned")

    def test_get_storage(self):
        inventory_list = self.valkyrie_provider.valkyrie_client. \
            list_storage_category_inventory(
                account_id=self.dedicated_account).entity
        storage_details = self.valkyrie_provider.valkyrie_client. \
            get_storage_inventory(self.dedicated_account,
                                  inventory_list[0].id).entity
        self.assertIsNotNone(storage_details.id,
                             msg="No storage id is returned")
        self.assertIsNotNone(storage_details.type,
                             msg="No storage type is returned")
        self.assertIsNotNone(storage_details.permissions,
                             msg="No storage permissions is returned")
        self.assertIsNotNone(storage_details.parts,
                             msg="No storage  parts is returned")

    def test_list_support_inventory(self):
        inventory_list = self.valkyrie_provider.valkyrie_client. \
            list_support_category_inventory(
                account_id=self.dedicated_account).entity
        self.assertGreater(len(inventory_list), 0, msg="No Support Device")
        self.assertIsNotNone(inventory_list[0].id,
                             msg="No support device id is returned")
        self.assertIsNotNone(inventory_list[0].datacenter,
                             msg="No support datacenter is returned")
        self.assertIsNotNone(inventory_list[0].permissions,
                             msg="No support device permissions is returned")
        self.assertIsNotNone(inventory_list[0].parts,
                             msg="No support parts is returned")

    def test_get_support_device(self):
        inventory_list = self.valkyrie_provider.valkyrie_client. \
            list_support_category_inventory(
                account_id=self.dedicated_account).entity
        support_device_details = self.valkyrie_provider.valkyrie_client. \
            get_support_inventory(self.dedicated_account,
                                  inventory_list[0].id).entity
        self.assertIsNotNone(support_device_details.id,
                             msg="No support device id is returned")
        self.assertIsNotNone(support_device_details.datacenter,
                             msg="No support datacenter is returned")
        self.assertIsNotNone(support_device_details.permissions,
                             msg="No support device permissions is returned")
        self.assertIsNotNone(support_device_details.parts,
                             msg="No support parts is returned")

    def test_list_tickets(self):
        ticket_list = self.valkyrie_provider.valkyrie_client.list_tickets(
            account_id=self.dedicated_account).entity
        self.assertGreater(len(ticket_list), 0, msg="Empty Ticket List")
        self.assertIsNotNone(ticket_list[0].status,
                             msg='Ticket Status Not Defined')
        self.assertIsNotNone(ticket_list[0].ticket_number,
                             msg='Ticket Number Not Defined')
        self.assertIsNotNone(ticket_list[0].subject,
                             msg='Ticket Subject Not Defined')

    def test_get_ticket(self):
        ticket = self.valkyrie_provider.valkyrie_client.get_ticket(
            account_id=self.dedicated_account,
            ticket_id=self.valkyrie_provider.valkyrie_test_ticket).entity
        self.assertIsNotNone(ticket.status.name,
                             msg='Ticket Status Not Defined')
        self.assertIsNotNone(ticket.number, msg='Ticket Number Not Defined')
        self.assertIsNotNone(ticket.subject, msg='Ticket Subject Not Defined')
        self.assertGreater(len(ticket.recipients), 0,
                           msg="No defined recipients")
        self.assertIsNotNone(ticket.queue, msg="No defined queue")
        self.assertIsNotNone(ticket.category, msg="No defined category")
        self.assertIsNotNone(ticket.subject, msg="No defined category")

    def test_list_ticket_recipients(self):
        ticket_recipients = self.valkyrie_provider.valkyrie_client. \
            list_ticket_recipients(
                account_id=self.dedicated_account,
                ticket_id=self.valkyrie_provider.valkyrie_test_ticket).entity
        self.assertGreater(len(ticket_recipients), 0,
                           msg='Empty recipient list')
        self.assertIsNotNone(ticket_recipients[0].employee_userid,
                             msg='No employee userid')
        self.assertIsNotNone(ticket_recipients[0].contact_id,
                             msg='No contact id')
        self.assertIsNotNone(ticket_recipients[0].role_id,
                             msg='No role id')
        self.assertIsNotNone(ticket_recipients[0].role_name,
                             msg='No role name')
        self.assertIsNotNone(ticket_recipients[0].contact_name,
                             msg='No contact name')

    def test_get_ticket_messages(self):
        ticket_messages = self.valkyrie_provider.valkyrie_client. \
            list_ticket_messages(account_id=self.dedicated_account,
                                 ticket_id=self.valkyrie_provider.
                                 valkyrie_test_ticket).entity
        self.assertGreater(len(ticket_messages), 0, msg='Empty message list')
        self.assertEquals(str(ticket_messages[0].ticket_number),
                          self.valkyrie_provider.valkyrie_test_ticket,
                          msg="Incorrect messages fetched")
        self.assertGreater(len(ticket_messages[0].recipients), 0,
                           msg="No recipients for the message")
        self.assertEquals(str(ticket_messages[0].account_number),
                          self.dedicated_account, msg="Account id dont match")

    def test_list_files(self):
        files = self.valkyrie_provider.valkyrie_client.list_files(
            account_id=self.dedicated_account).entity
        self.assertGreater(len(files), 0, msg='Empty files list')
        self.assertIsNotNone(files[0].name, msg="No File Name")
        self.assertIsNotNone(files[0].content_type, msg="No File content type")
        self.assertIsNotNone(files[0].file_id, msg="No File id")

    def test_get_file(self):
        files = self.valkyrie_provider.valkyrie_client.list_files(
            account_id=self.dedicated_account).entity
        file = self.valkyrie_provider.valkyrie_client.get_file(
            account_id=self.dedicated_account,
            file_id=files[0].file_id)
        self.assertTrue(200, file.status_code)

    def test_list_contacts_with_permission_on_item_types(self):
        contact_list_response = self.valkyrie_provider.valkyrie_client. \
            list_contacts_with_permission(account_id=self.dedicated_account,
                                          item_type="accounts")
        contact_list = json.loads(contact_list_response.text)
        self.assertEquals(200, contact_list_response.status_code)
        self.assertGreater(len(contact_list), 0, msg="Empty contact list")

    def test_get_device_details(self):
        server_list = self.valkyrie_provider.valkyrie_client. \
            list_server_category_inventory(
                account_id=self.dedicated_account).entity
        device_details = self.valkyrie_provider.valkyrie_client. \
            get_device_details(account_id=self.dedicated_account,
                               device_id=server_list[0].id).entity
        self.assertIsNotNone(device_details.primary_username,
                             msg="No primary username")
        self.assertIsNotNone(device_details.account_number,
                             msg="No account number")
        self.assertEquals(str(self.dedicated_account),
                          str(device_details.account_number))

    def test_list_revenue_categories(self):
        revenue_categories_response = self.valkyrie_provider.valkyrie_client. \
            list_revenue_categories()
        self.assertEquals(200, revenue_categories_response.status_code)
        revenue_categories_dict = json.loads(revenue_categories_response.text)
        self.assertGreater(len(revenue_categories_dict.keys()), 0,
                           msg='Empty revenue categories')

    def test_list_revenue_types(self):
        revenue_types_response = self.valkyrie_provider.valkyrie_client. \
            list_revenue_types()
        self.assertEquals(200, revenue_types_response.status_code)
        revenue_types = json.loads(revenue_types_response.text)
        self.assertGreater(len(revenue_types.keys()), 0,
                           msg='Empty revenue types')

    def test_list_revenue_currencies(self):
        revenue_types_response = self.valkyrie_provider.valkyrie_client. \
            list_revenue_types()
        self.assertEquals(200, revenue_types_response.status_code)
        revenue_types = json.loads(revenue_types_response.text)
        self.assertGreater(len(revenue_types.keys()), 0,
                        msg='Empty revenue currencies')

    def test_get_cloud_account_details(self):
        cloud_account_details = self.valkyrie_provider.valkyrie_client. \
            get_cloud_account_details(
                cloud_account_id=self.cloud_account).entity
        self.assertEquals(str(self.cloud_account),
                          str(cloud_account_details.cloud_account_number))

    def test_managed_cloud_data_setup(self):
        self.compute_provider.wait_for_server_metadata(
            self.server.id, "rax_service_level_automation",
            self.managed_cloud_timeout)
        metadata = self.compute_provider.wait_for_server_metadata_status(
            self.server.id, "rax_service_level_automation", "Complete",
            timeout=self.managed_cloud_timeout).entity
        self.assertEquals("Complete", metadata.rax_service_level_automation,
                          msg="Managedcloud data not setup")

    def test_managed_cloud_password(self):
        admin_passwords = self.valkyrie_provider.valkyrie_client. \
            get_managed_cloud_password(cloud_account_id=self.cloud_account,
                                       server_location="us",
                                       server_id=self.server.id).entity
        self.assertGreater(len(admin_passwords), 0, msg="No password list")
        self.assertIsNotNone(admin_passwords[0].admin_password,
                             msg="No password returned")

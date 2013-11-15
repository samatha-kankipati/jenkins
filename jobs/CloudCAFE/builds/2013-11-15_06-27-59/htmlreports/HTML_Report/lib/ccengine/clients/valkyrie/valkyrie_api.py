from ccengine.clients.base_client import BaseMarshallingClient
from ccengine.domain.valkyrie.response.valkyrie_response import Storage, \
    Inventory, Contact, Server, Network, Service, AccountDetails, File, \
    Tickets, Permission, Password, SupportDevice, TicketRecipient, Ticket, \
    TicketMessage, Device, CloudAccount


class ValkyrieAPIClient(BaseMarshallingClient):
    def __init__(self, url, auth_token, serialize_format=None,
                 deserialize_format=None):
        super(ValkyrieAPIClient, self).__init__(serialize_format,
                                                deserialize_format)
        self.auth_token = auth_token
        ct = '{content_type}/{content_subtype}'.format(
            content_type='application',
            content_subtype=self.serialize_format)
        accept = '{content_type}/{content_subtype}'.format(
            content_type='application',
            content_subtype=self.deserialize_format)
        self.default_headers['Content-Type'] = ct
        self.default_headers['Accept'] = accept
        self.default_headers['X-Auth_token'] = self.auth_token
        self.url = url

    def get_dedicated_account_details(self, account_id):
        '''
        @summary: Retrieves account details
        @rtype: Response Object
        @param account_id: Account id for which details needs to be fetched.
        @type account_id: String
        '''
        url = '{0}/account/{1}'.format(self.url, account_id)
        valkyrie_response = self.request('GET', url,
                                         response_entity_type=AccountDetails)
        return valkyrie_response

    def list_contacts(self, account_id):
        '''
        @summary: Retrieves the list of contacts for the account
        @rtype: Response Object
        @param account_id: Account id for which details needs to be fetched.
        @type account_id: String
        '''
        url = '{0}/account/{1}/contacts'.format(self.url, account_id)
        valkyrie_response = self.request('GET', url,
                                         response_entity_type=Contact)
        return valkyrie_response

    def list_inventory(self, account_id):
        '''
        @summary: Retrieves account inventory
        @rtype: Response Object
        @param account_id: Account id for which details needs to be fetched.
        @type account_id: String
        '''
        url = '{0}/account/{1}/inventory'.format(self.url, account_id)
        valkyrie_response = self.request('GET', url,
                                         response_entity_type=Inventory)
        return valkyrie_response

    def get_inventory_details(self, account_id, inventory_id):
        '''
        @summary: Get detailed information for an item in the inventory.
        @rtype: Response Object
        @param account_id: Account id for which details needs to be fetched.
        @type account_id: String
        @param inventory_id: Inventory id for which details is fetched.
        @type inventory_id: String
        '''
        url = '{0}/account/{1}/inventory/{2}'.format(self.url, account_id,
                                                     inventory_id)
        valkyrie_response = self.request('GET', url,
                                         response_entity_type=Inventory)
        return valkyrie_response

    def list_server_category_inventory(self, account_id):
        '''
        @summary : Retrieves server category specific inventory for an account
        @rtype: Response Object
        @param account_id: Account id for which details needs to be fetched.
        @type account_id: String
        '''
        url = '{0}/account/{1}/inventory/servers/'.format(self.url, account_id)
        server_response = self.request('GET', url,
                                       response_entity_type=Server)
        return server_response

    def list_network_category_inventory(self, account_id):
        '''
        @summary : Retrieves network category specific inventory for an account
        @rtype: Response Object
        @param account_id: Account id for which details needs to be fetched.
        @type account_id: String
        '''

        url = '{0}/account/{1}/inventory/network'.format(self.url,
                                                         account_id)
        valkyrie_response = self.request('GET', url,
                                         response_entity_type=Network)
        return valkyrie_response

    def list_service_category_inventory(self, account_id):
        '''
        @summary : Retrieves service category specific inventory for an account
        @rtype: Response Object
        @param account_id: Account id for which details needs to be fetched.
        @type account_id: String
        '''

        url = '{0}/account/{1}/inventory/services'.format(self.url,
                                                          account_id)
        valkyrie_response = self.request('GET', url,
                                         response_entity_type=Service)
        return valkyrie_response

    def list_storage_category_inventory(self, account_id):
        '''
        @summary : Retrieves storage category specific inventory for an account
        @rtype: Response Object
        @param account_id: Account id for which details needs to be fetched.
        @type account_id: String
        '''
        url = '{0}/account/{1}/inventory/storage'.format(self.url,
                                                         account_id)
        valkyrie_response = self.request('GET', url,
                                         response_entity_type=Storage)
        return valkyrie_response

    def list_support_category_inventory(self, account_id):
        '''
        @summary : Retrieves support category specific inventory for an account
        @rtype: Response Object
        @param account_id: Account id for which details needs to be fetched.
        @type account_id: String
        '''

        url = '{0}/account/{1}/inventory/support'.format(self.url, account_id)
        api_response = self.request('GET', url,
                                    response_entity_type=SupportDevice)
        return api_response

    def get_server_inventory(self, account_id, id):
        '''
        @summary: Get the server details from the inventory.
        @rtype: Response Object
        @param account_id: Account id for which details needs to be fetched.
        @type account_id: String
        @param id: Server id for which details needs to be fetched.
        @type id: String

        '''

        url = '{0}/account/{1}/inventory/servers/{2}'. \
            format(self.url, account_id, id)
        server_response = self.request('GET', url,
                                       response_entity_type=Server)
        return server_response

    def get_network_inventory(self, account_id, id):
        '''
        @summary: Get the network details from the inventory.
        @rtype: Response Object
        @param account_id: Account id for which details needs to be fetched.
        @type account_id: String
        @param id: Network id for which details needs to be fetched.
        @type id: String
        '''

        url = '{0}/account/{1}/inventory/network/{2}'.format(self.url,
                                                             account_id, id)
        network_response = self.request('GET', url,
                                        response_entity_type=Network)
        return network_response

    def get_service_inventory(self, account_id, id):
        '''
        @summary: Get the services details from the inventory.
        @rtype: Response Object
        @param account_id: Account id for which details needs to be fetched.
        @type account_id: String
        @param id: Network id for which details needs to be fetched.
        @type id: String
        '''

        url = '{0}/account/{1}/inventory/services/{2}'.format(self.url,
                                                              account_id, id)
        network_response = self.request('GET', url,
                                        response_entity_type=Service)
        return network_response

    def get_storage_inventory(self, account_id, id):
        '''
        @summary: Get the storage details from the inventory.
        @rtype: Response Object
        @param account_id: Account id for which details needs to be fetched.
        @type account_id: String
        @param id: Storage id for which details needs to be fetched.
        @type id: String
        '''

        url = '{0}/account/{1}/inventory/storage/{2}'.format(self.url,
                                                             account_id, id)
        storage_response = self.request('GET', url,
                                        response_entity_type=Storage)
        return storage_response

    def get_support_inventory(self, account_id, id):
        '''
        @summary: Get the support details from the inventory.
        @rtype: Response Object
        @param account_id: Account id for which details needs to be fetched.
        @type account_id: String
        @param id: Support id for which details needs to be fetched.
        @type id: String
        '''

        url = '{0}/account/{1}/inventory/support/{2}'.format(self.url,
                                                             account_id, id)
        storage_response = self.request('GET', url,
                                        response_entity_type=SupportDevice)
        return storage_response

    def list_tickets(self, account_id):
        '''
        @summary: List all the tickets for a given account.
        @rtype: Response Object
        @param account_id: Account id for which details needs to be fetched.
        @type account_id: String
        '''

        url = '{0}/account/{1}/tickets'.format(self.url, account_id)
        valkyrie_response = self.request('GET', url,
                                         response_entity_type=Tickets)
        return valkyrie_response

    def get_ticket(self, account_id, ticket_id):
        '''
        @summary :Get the detailed information for a ticket
        @rtype: Response Object
        @param account_id: Account id for which details needs to be fetched.
        @type account_id: String
        @param ticket_id: Ticket id for which details needs to be fetched.
        @type id: String
        '''

        url = '{0}/account/{1}/tickets/{2}'.format(self.url, account_id,
                                                   ticket_id)
        valkyrie_response = self.request('GET', url,
                                         response_entity_type=Ticket)
        return valkyrie_response

    def list_ticket_recipients(self, account_id, ticket_id):
        '''
        @summary : Get the list of ticket recipients
        @rtype: Response Object
        @param account_id: account id  for which ticket recipients is fetched
        @param ticket_id: ticket id  for which recipients is fetched
        @return: recipient list
        '''

        url = '{0}/account/{1}/tickets/{2}/recipients'.format(self.url,
                                                              account_id,
                                                              ticket_id)
        valkyrie_response = self.request('GET', url,
                                         response_entity_type=TicketRecipient)
        return valkyrie_response

    def list_ticket_messages(self, account_id, ticket_id):
        '''
        @summary : Get the list of ticket messages
        @rtype: Response Object
        @param account_id: account id  for which ticket recipients is fetched
        @param ticket_id: ticket id  for which recipients is fetched
        @return: recipient list
        '''

        url = '{0}/account/{1}/tickets/{2}/messages'.format(self.url,
                                                            account_id,
                                                            ticket_id)
        valkyrie_response = self.request('GET', url,
                                         response_entity_type=TicketMessage)
        return valkyrie_response

    def list_files(self, account_id):
        '''
        @summary: List all the files for a given account.
        @rtype: Response Object
        @param account_id: Account id for which files needs to be fetched.
        @type account_id: String
        '''
        url = '{0}/account/{1}/files'.format(self.url, account_id)
        valkyrie_response = self.request('GET', url,
                                         response_entity_type=File)
        return valkyrie_response

    def get_file(self, account_id, file_id):
        '''
        @summary : Get a file by file id
        @rtype: Response Object
        @param account_id: Account id for which the file needs to be fetched.
        @type account_id: String
        @param file_id: File id for which details needs to be fetched.
        @type id: String
        '''
        url = '{0}/account/{1}/files/{2}'.format(self.url, account_id, file_id)
        valkyrie_response = self.request('GET', url)
        return valkyrie_response

    def list_permission(self, account_id):
        '''
        @summary:List all the effective permissions of a given account
        @rtype: Response Object
        @param account_id: Account id for which details needs to be fetched.
        @type account_id: String
        '''

        url = '{0}/account/{1}/permissions'.format(self.url, account_id)
        valkyrie_response = self.request('GET', url,
                                         response_entity_type=Permission)
        return valkyrie_response

    def list_contacts_with_permission(self, account_id, item_type,
                                      item_id=None):
        '''
        @summary:List of contacts with permissions on given items.
        @return type : Response Object
        @param account_id: Account id for which details needs to be fetched.
        @type account_id: String
        @param item_type: Item type of the concerned item.
        @type item_type: String
        @param item_id: Item id for which details needs to be fetched.
        @type item_id: String
        '''

        if item_id is None:
            url = '{0}/account/{1}/permissions/contacts_with_permissions/{2}' \
                .format(self.url, account_id, item_type)
        else:
            url = '{0}/account/{1}/permissions/contacts_with_permissions/{2}' \
                  '/{3}'.format(self.url, account_id, item_type, item_id)
        valkyrie_response = self.request('GET', url)
        return valkyrie_response

    def get_device_details(self, account_id, device_id):
        '''
        @summary: Get the details for a given device id .
        @return type Response Object
        @param account_id: Account id for which details needs to be fetched.
        @type account_id: String
        @param device_id: Device id for which details needs to be fetched.
        @type device_id: String
        '''

        url = '{0}/account/{1}/device/{2}'.format(self.url, account_id,
                                                  device_id)
        valkyrie_response = self.request('GET', url,
                                         response_entity_type=Device)
        return valkyrie_response

    def list_revenue_types(self):
        '''
        @summary: List all the revenue types
        @rtype: Response object
        '''

        url = '{0}/account/revenue/types'.format(self.url)
        valkyrie_response = self.request('GET', url)
        return valkyrie_response

    def list_revenue_categories(self):
        '''
        @summary: List all the revenue categories
        @rtype:Response Object
        '''

        url = '{0}/account/revenue/categories'.format(self.url)
        valkyrie_response = self.request('GET', url)
        return valkyrie_response

    def list_revenue_currencies(self):
        '''
        @summary: List the currencies supported
        @rtype: Response Object
        '''

        url = '{0}/account/revenue/currencies'.format(self.url)
        valkyrie_response = self.request('GET', url)
        return valkyrie_response

    def get_cloud_account_details(self, cloud_account_id):
        '''
        @summary: Get the details of a cloud account.
        @rtype: Response Object
        @param cloud_account_id: Cloud account id.
        @type cloud_account_id: String
        '''

        url = '{0}/cloud_account/{1}'.format(self.url, cloud_account_id)
        valkyrie_response = self.request('GET', url,
                                         response_entity_type=CloudAccount)
        return valkyrie_response

    def get_managed_cloud_password(self, cloud_account_id, server_location,
                                   server_id):
        '''

        @summary:Retrieves the journal of managed cloud password for the server
        @rtype: Response Object
        @param cloud_account_id: Cloud account id.
        @type cloud_account_id: String
        @param server_location: Location of the server
        @type server_location: String
        @param server_id: Server ID
        @type server_id: String

        '''
        url = '{0}/cloud_account/{1}/locations/{2}/servers/{3}/' \
              'admin_passwords'.format(self.url, cloud_account_id,
                                       server_location, server_id)
        valkyrie_response = self.request('GET', url,
                                         response_entity_type=Password)
        return valkyrie_response

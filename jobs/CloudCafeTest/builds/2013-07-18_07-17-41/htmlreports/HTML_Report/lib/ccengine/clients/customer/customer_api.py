from ccengine.domain.customer.request.customer_request import \
                     CreateCustomerRequest, UpdateCustomerRequest, \
                     CreateContactRequest, UpdateContactRequest
from ccengine.domain.customer.response.customer_response import \
                     GetCustomerResponse, \
                     GetCustomerAccountsResponse, GetContactsResponse, \
                     GetChildCustomersResponse, GetCustomerAccountResponse,\
                     GetCustomerAccountContactsResponse, \
                     GetCustomerAccountStatusHistoryResponse, \
                     GetContactResponse, GetCountriesResponse, \
                     GetCountryResponse, GetAllCustomerEventsResponse
from ccengine.clients.base_client import BaseMarshallingClient



class CustomerAPIClient(BaseMarshallingClient):
    """
    @summary: The Customer API client
    """

    def __init__(self, base_url, auth_token=None, serialize_format=None,
                 deserialize_format=None):
        """
        @summary: Customer API Client setup
        @param base_url: The base url to be prepended to the request urls
                         e.g: 'http://test.customer.api.rackspace.com'
        @type base_url: String                 
        @param auth_token: The authentication token to be used
        @type auth_token: String
        @param serialize_format: The serialization format to use
                                 values allowed: 'json' or 'xml'
        @type serialize_format: String
        @param deserialize_format: The deserialization format to use
                                   values allowed: 'json' or 'xml'
        @type deserialize_format: String        
        """
                 
        super(CustomerAPIClient, self).__init__(serialize_format,
                                                deserialize_format)

        self.base_url = base_url
        self.auth_token = auth_token
        self.default_headers['X-Auth-Token'] = auth_token
        self.default_headers['Content-Type'] = 'application/{0}'.format(
                                                        serialize_format)
        self.default_headers['Accept'] = 'application/{0}'.format(
                                                        deserialize_format)
                
           
    def create_customer(self, customer_type=None, name=None, 
                        child_customers=None, customer_accounts=None, 
                        contacts=None, requestslib_kwargs=None):
        """
        POST
        /v3/customers
        
        
        @summary: Creates a POST request to create a new customer
        @param customer_type: The customer type, e.g: 'RESELLER'
        @type customer_type: String
        @param name: The name of the customer, e.g: 'Bob'
        @type name: String
        @param child_customers: Child customers, specifically their unique 
                                identifiers that belong to the customer,
                                e.g: [
                                        {'number': 'RCN-111-222-422'},
                                        {'number': 'RCN-283-343-232'}
                                     ]
        @type child_customers: List of customer numbers(dictionary)    
        @param customer_accounts: Customer accounts that belong to the customer
                                  e.g: [{
                                           'status': 'Active',
                                           'name': 'Hubspot Accounting',
                                           'number': 19293384938,
                                           'type': 'CLOUD'
                                       }]
        @type customer_accounts: List of customer accounts(dictionary)
        @param contacts: The list of contact information
                         e.g: 
                           [  
							   {
							       'lastName':'Jones',
							       'phoneNumbers':{
								   'phoneNumber':[
								    {
								       'number':'8374384343',
								       'country':'US'
								    }
								    ]
							      },
							      'roles':{
								 'customerAccountRole':[
								    {
								       'value':'BILLING',
								       'customerAccountNumber':'19293384938',
								       'customerAccountType':'CLOUD'
								    }
								 ]
							      },
							      'addresses':{
								 'address':[
								    {
								       'zipcode':'78366',
								       'street':'1 Dezavala Place',
								       'primary':true,
								       'state':'Texas',
								       'country':'US',
								       'city':'San Francisco'
								    }
								 ]
							      },
							      'firstName':'Mike',
							      'emailAddresses':{
								 'emailAddress':[
								    {
								       'address':'mike.jones@thecompany.com',
								       'primary':true
								    }
								 ]
							      }
							   }
							]                         
        @type contacts: List of contacts(dictionary)
        @param requestslib_kwargs: Used for future additions so that we don't 
                                   break current code
        @type requestslib_kwargs: Dictionary
        @return: Headers and response codes without a response body       
        """
        
        url = '{0}/v3/customers'.format(self.base_url)
        
        customer_request_entity = CreateCustomerRequest(
                                        customer_type=customer_type, name=name, 
                                        child_customers=child_customers,
                                        customer_accounts=customer_accounts, 
                                        contacts=contacts)
            
        return self.request('POST', url, 
                            request_entity=customer_request_entity,
                            requestslib_kwargs=requestslib_kwargs)         
                            
    def update_customer(self, customer_number=None, customer_type=None, 
                        customer_name=None, requestslib_kwargs=None):
        """
        PUT
        /v3/customers/{customer_number}
        
        
        @summary: Makes a PUT request to update a customer's type and name
        @param customer_number: The unique identifier that is associated with 
                                the customer, e.g: 'RCN-230-348-343'
        @type customer_number: String
        @param customer_type: The type of the customer, e.g: 'RESELLER'
        @type customer_type: String
        @param customer_name: The name of the customer, e.g: 'Bob'
        @type customer_name: String
        @param requestslib_kwargs: Used for future additions so that we don't 
                                   break current code
        @type requestslib_kwargs: Dictionary
        @return: Headers and response codes without a response body       
        """
        
        url = '{0}/v3/customers/{1}'.format(self.base_url, customer_number)
        
        customer_request_entity = None

        req = {}
        for attr, val in vars(self).iteritems():
            if val is not None:
                req[key] = val
        customer_request_entity = UpdateCustomerRequest(**req)

        return self.request('PUT', url, 
                            response_entity_type=UpdateCustomerResponse,
                            request_entity=customer_request_entity,
                            requestslib_kwargs=requestslib_kwargs)
    
    def delete_customer(self, customer_number=None, requestslib_kwargs=None):
        """
        DELETE
        /v3/customers/{customer_number}
        
        
        @summary: Makes a DELETE request to deletes the specified customer
        @param customer_number: The unique identifier that is associated with 
                                the customer, e.g: 'RCN-230-348-343'
        @type customer_number: String
        @param requestslib_kwargs: Used for future additions so that we don't 
                                   break current code
        @type requestslib_kwargs: Dictionary
        @return: Headers and response codes without a response body       
        """
        
        url = '{0}/v3/customers/{1}'.format(self.base_url, customer_number)
        
        return self.request('DELETE', url, 
                            requestslib_kwargs=requestslib_kwargs)
        
    def get_customer(self, customer_number=None, requestslib_kwargs=None):
        """
        GET
        /v3/customers/{customer_number}
        
        
        @summary: Makes a GET request to get the customer information
        @param customer_number: The unique identifier that is associated with 
                                the customer, e.g: 'RCN-230-348-343'
        @type customer_number: String
        @param requestslib_kwargs: Used for future additions so that we don't 
                                   break current code
        @type requestslib_kwargs: Dictionary
        @return: Headers and response codes with customer information in 
                  response body       
        """
        
        url = '{0}/v3/customers/{1}'.format(self.base_url, customer_number)

        return self.request('GET', url, 
                            response_entity=GetCustomerResponse,
                            requestslib_kwargs=requestslib_kwargs)
        
    def merge_customer(self, customer_number=None, from_customer_number=None,
                       requestslib_kwargs=None):
        """
        PUT
        /v3/customers/{customer_number}/merge/{from_customer_number}
        
        
        @summary: Makes a PUT request to merge two customers, 
                  e.g: customer <= customer + from_customer
        @param customer_number: The unique identifier that is associated with 
                                the customer, e.g: 'RCN-111-222-422'
        @type customer_number: String
        @param from_customer_number: The unique identifier that is associated 
                                     with the customer, e.g: 'RCN-230-348-343'
        @type from_customer_number: String
        @param requestslib_kwargs: Used for future additions so that we don't 
                                   break current code
        @type requestslib_kwargs: Dictionary
        @return: Headers and response codes without a response body        
        """
        
        url = '{0}/v3/customers/{1}/merge/{2}'.format(self.base_url, 
                                                      customer_number,
                                                      from_customer_number)
                                                                       
        return self.request('PUT', url, requestslib_kwargs=requestslib_kwargs)
        
    def get_customer_accounts(self, customer_number=None, 
                              requestslib_kwargs=None):
        """
        GET
        /v3/customers/{customer_number}/customer_accounts
        
        
        @summary: Makes a GET request to get the customer's accounts
        @param customer_number: The unique identifier that is associated with 
                                the customer, e.g: 'RCN-230-348-343'
        @type customer_number: String
        @param requestslib_kwargs: Used for future additions so that we don't 
                                   break current code
        @type requestslib_kwargs: Dictionary
        @return: Headers and response codes with customer accounts in 
                  response body        
        """
        
        url = '{0}/v3/customers/{1}/customer_accounts'.format(self.base_url, 
                                                              customer_number)
        
        return self.request('GET', url, 
                            response_entity=GetCustomerAccountsResponse, 
                            requestslib_kwargs=requestslib_kwargs)
                            
    def get_contacts(self, customer_number=None, role=None, 
                     requestslib_kwargs=None):
        """
        GET
        /v3/customers/{customer_number}/contacts?role={role}
        
        
        @summary: Makes a GET request to get the customer's contacts
        @param customer_number: The unique identifier that is associated with 
                                the customer, e.g: 'RCN-230-348-343'
        @type customer_number: String
        @param role: (optional) The role of the contact to filter contacts by 
                     e.g: 'BILLING'
        @type role: String
        @param requestslib_kwargs: Used for future additions so that we don't 
                                   break current code
        @type requestslib_kwargs: Dictionary
        @return: Headers and response codes with customer contacts in
                  response body       
        """
        
        url = '{0}/v3/customers/{1}/contacts'.format(self.base_url, 
                                                     customer_number)
        
        #add optional parameters to the request
        params = {}
        if role is not None:
            params['role'] = role

        return self.request('GET', url, params=params,
                            response_entity_type=GetContactsResponse,
                            requestslib_kwargs=requestslib_kwargs)
        
    def get_child_customers(self, customer_number=None, 
                            requestslib_kwargs=None):
        """
        GET
        /v3/customers/{customer_number}/child_customers
        
        
        @summary: Makes a GET request to get the list of all child customers of
                  the customer
        @param customer_number: The unique identifier that is associated with 
                                the customer, e.g: 'RCN-230-348-343'
        @type customer_number: String
        @param requestslib_kwargs: Used for future additions so that we don't 
                                   break current code
        @type requestslib_kwargs: Dictionary
        @return: Headers and response codes with child customers of a customer
                  in the response body        
        """
        
        url = '{0}/v3/customers/{1}/child_customers'.format(self.base_url, 
                                                            customer_number)
                                                    
        return self.request('GET', url, 
                            response_entity_type=GetChildCustomersResponse,
                            requestslib_kwargs=requestslib_kwargs)
        
    def add_child_customer(self, customer_number=None, 
                           child_customer_number=None, 
                           requestslib_kwargs=None):
        """
        PUT
        /v3/customers/{customer_number}/child_customers/{child_customer_number}
        
        
        @summary: Makes a PUT request to add a child customer to a customer
        @param customer_number: The unique identifier that is associated with 
                                the customer, e.g: 'RCN-230-348-343'
        @type customer_number: String
        @param child_customer_number: The unique identifier that is associated 
                                      with the customer, e.g: 'RCN-111-222-422'
        @type child_customer_number: String
        @param requestslib_kwargs: Used for future additions so that we don't 
                                   break current code
        @type requestslib_kwargs: Dictionary
        @return: Headers and response codes without a response body        
        """
        
        url = '{0}/v3/customers/{1}/child_customers/{2}'.format(
                      self.base_url, customer_number, child_customer_number)
        
        return self.request('PUT', url, 
                            response_entity_type=AddChildCustomerResponse,
                            requestslib_kwargs=requestslib_kwargs)
        
    def remove_child_customer(self, customer_number=None, 
                              child_customer_number=None, 
                              requestslib_kwargs=None):
        """
        DELETE
        /v3/customers/{customer_number}/child_customers/{child_customer_number}
        
        
        @summary: Makes a DELETE request to remove a child customer from 
                  a customer account
        @param customer_number: The unique identifier that is associated with 
                                the customer, e.g: 'RCN-230-348-343'
        @type customer_number: String
        @param child_customer_number: The unique identifier that is associated 
                                      with the customer, e.g: 'RCN-111-222-422'
        @type child_customer_number: String
        @param requestslib_kwargs: Used for future additions so that we don't 
                                   break current code
        @type requestslib_kwargs: Dictionary
        @return: Headers and response codes without a response body        
        """
        
        url = '{0}/v3/customers/{1}/child_customers/{2}'.format(
                      self.base_url, customer_number, child_customer_number)
                                        
        return self.request('DELETE', url, 
                            response_entity_type=DeleteChildCustomerResponse,
                            requestslib_kwargs=requestslib_kwargs)
        
    def get_customer_account(self, account_type=None, account_number=None,
                             requestslib_kwargs=None):
        """
        GET
        /v3/customer_accounts/{accountType}/{accountNumber|
        
        
        @summary: Makes a GET request to get the customer account information
        @param account_type: The type of the customer's account, e.g: 'CLOUD'
        @type account_type: String
        @param account_number: The account number of the account to view,
                               e.g: '19293384938'
        @type account_number: String
        @param requestslib_kwargs: Used for future additions so that we don't 
                                   break current code
        @type requestslib_kwargs: Dictionary
        @return: Headers and response codes with customer account information
                  in response body        
        """
        url = '{0}/v3/customer_accounts/{1}/{2}'.format(self.base_url, 
                                                        account_type,
                                                        account_number)
                                        
        return self.request('GET', url, 
                            response_entity_type=GetCustomerAccountResponse,
                            requestslib_kwargs=requestslib_kwargs)
        
    def get_customer_account_contacts(self, account_type=None, 
                                      account_number=None, role=None, 
                                      username=None, requestslib_kwargs=None):
        """
        GET
        /v3/customer_accounts/{account_type}/{account_number}/contacts?
                              role={role}&username={username}
                                        
                                        
        @summary: Makes a GET request to get a list of contact information from
                  the customer's account
        @param account_type: The type of the customer's account, e.g: 'CLOUD'
        @type account_type: String
        @param account_number: The account number of the account to view,
                               e.g: '19293384938'
        @type account_number: String
        @param role: (optional) The role of the contact to filter contacts by 
                     e.g: 'BILLING'
        @type role: String
        @param username: (optional) The username of the contact to filter 
                         contacts by, e.g: 'mike.jones'
        @type username: String
        @param requestslib_kwargs: Used for future additions so that we don't 
                                   break current code
        @type requestslib_kwargs: Dictionary
        @return: Headers and response codes with contacts of customer account
                  in response body                 
        """
        
        url = '{0}/v3/customer_accounts/{1}/{2}/contacts'.format(
                      self.base_url, account_type, account_number)
                                        
        #add optional parameters to the request
        params = {}
        if role is not None:
            params['role'] = role                           
        if username is not None:
            params['username'] = username                               
            
        return self.request('GET', url, params=params, 
                    response_entity_type=GetCustomerAccountContactsResponse,
                    requestslib_kwargs=requestslib_kwargs)
        
    def get_customer_account_status_history(self, account_type=None,
                             account_number=None, requestslib_kwargs=None):
        """
        GET
        /v3/customer_accounts/{account_type}/{account_number}/status_history
        
        
        @summary: Makes a GET request to get the list of all the status changes
                  for the specified customer account
        @param account_type: The type of the customer's account, e.g: 'CLOUD'
        @type account_type: String
        @param account_number: The account number of the account to view,
                               e.g: '19293384938'
        @type account_number: String    
        @param requestslib_kwargs: Used for future additions so that we don't 
                                   break current code
        @type requestslib_kwargs: Dictionary
        @return: Headers and response codes with status changes of customer
                  account in response body        
        """
        
        url = '{0}/v3/customer_accounts/{1}/{2}/status_history'.format(
                      self.base_url, account_type, account_number)
                                        
        return self.request('GET', url, 
                    response_entity_type=\
                                    GetCustomerAccountStatusHistoryResponse,
                    requestslib_kwargs=requestslib_kwargs)
                    
    def create_contact(self, first_name=None, last_name=None, suffix=None,
                       title=None, username=None, addresses=None,
                       email_addresses=None, phone_numbers=None, roles=None,
                       requestslib_kwargs=None):
        """
        POST
        /v3/contacts
        
        
        @summary: Makes a POST request to create a new contact
        @param first_name: The first name of the contact, e.g: 'John'
        @type first_name: String
        @param last_name: The last name of the contact, e.g: 'Denton'
        @type last_name: String
        @param suffix: The suffix of the contact's name, e.g: 'Senior'
        @type suffix: String
        @param title: The title of the contact's name, e.g: 'Mr'
        @type title: String
        @param username: The username of the contact, e.g: 'john0982'
        @type username: String
        @param addresses: The list of the addresses of the contact,
                          e.g: [{
                                    'zipcode': '78366',
                                    'street': '1 Dezavala Place',
                                    'primary': True,
                                    'state': 'Texas',
                                    'country': 'US',
                                    'city': 'San Francisco'
                               }]
        @type addresses: List of addresses(Dictionary)
        @param requestslib_kwargs: Used for future additions so that we don't 
                                   break current code
        @type requestslib_kwargs: Dictionary
        @return: Headers and response codes without response body        
        """
        
        url = '{0}/v3/contacts'.format(self.base_url)
        
        contact_request_entity = CreateContactRequest(
                                       first_name=first_name,
                                       last_name=last_name, suffix=suffix,
                                       title=title, username=username,
                                       addresses=addresses, 
                                       email_addresses=email_addresses,
                                       phone_numbers=phone_numbers, 
                                       roles=roles,
                                       requestslib_kwargs=requstslib_kwargs)
            
        return self.request('POST', url, 
                            request_entity_type=contact_request_entity,
                            requestslib_kwargs=requestslib_kwargs)
                            
    def get_contact(self, contact_number=None, requestslib_kwargs=None):
        """
        GET
        /v3/contacts/{contact_number}
        
        
        @summary: Makes a GET request to get the specified contact's 
                  information
        @param contact_number: The unique identifier of the contact
                               e.g: 'RPN-823-034-233'
        @type contact_number: String
        @param requestslib_kwargs: Used for future additions so that we don't 
                                   break current code
        @type requestslib_kwargs: Dictionary
        @return: Headers and response codes with contact information in the 
                  response body      
        """
        
        url = '{0}/v3/contacts/{1}'.format(self.base_url, contact_number)
                                                            
        return self.request('GET', url, 
                            response_entity_type=GetContactResponse,
                            requestslib_kwargs=requestslib_kwargs)
                                    
    def update_contact(self, contact_number=None, first_name=None, 
                       last_name=None, suffix=None, title=None,
                       username=None, addresses=None, 
                       email_addresses=None, phone_numbers=None,
                       roles=None, requestslib_kwargs=None):
        """
        PUT
        /v3/contacts/{contact_number}
        
        
        @summary: Makes a PUT request to update the specified contact's 
                  information
        @param contact_number: The unique identifier of the contact
                               e.g: 'RPN-823-034-233'
        @type contact_number: String
        @param first_name: The first name of the contact, e.g: 'John'
        @type first_name: String
        @param last_name: The last name of the contact, e.g: 'Denton'
        @type last_name: String
        @param suffix: The suffix of the contact's name, e.g: 'Senior'
        @type suffix: String
        @param title: The title of the contact's name, e.g: 'Mr'
        @type title: String
        @param username: The username of the contact, e.g: 'john0982'
        @type username: String
        @param addresses: The list of the addresses of the contact,
                          e.g: [{
                                    'zipcode': '78366',
                                    'street': '1 Dezavala Place',
                                    'primary': True,
                                    'state': 'Texas',
                                    'country': 'US',
                                    'city': 'San Francisco'
                               }]
        @type addresses: List of addresses(Dictionary)
        @param email_addresses: The list of email addresses of the contact,
                                e.g: [{
                                          'address': 'john.doe@incogneeto.com',
                                          'primary': True
                                     }]
        @type email_addresses: List of email addresses(Dictionary)   
        @param phone_numbers: The phone numbers of the contact, 
                              e.g: [{
                                        'number': '6758783848',
                                        'country': 'US'
                                   }]
        @type phone_numbers: List of phone numbers(Dictionary)
        @param roles: The list of roles of the contact
                      e.g: [{
                                'value': 'BILLING',
                                'customer_account_number': '7483483',
                                'customer_account_type': 'CLOUD'
                           }]
        @type roles: List of roles(Dictionary)        
        @param requestslib_kwargs: Used for future additions so that we don't 
                                   break current code
        @type requestslib_kwargs: Dictionary
        @return: Headers and response codes without response body       
        """
        
        url = '{0}/v3/contacts/{1}'.format(self.base_url, contact_number)
        
                
        customer_request_entity = None

        req = {}
        for attr, val in vars(self).iteritems():
            if val is not None:
                req[key] = val
        contact_request_entity = UpdateContactRequest(**req)
            
        return self.request('PUT', url, 
                            request_entity_type=contact_request_entity,
                            requestslib_kwargs=requestslib_kwargs)
                                
    def delete_contact(self, contact_number=None, requestslib_kwargs=None):
        """
        DELETE
        /v3/contacts/{contact_number}
        
        
        @summary: Makes a DELETE request to delete the specified contact
        @param contact_number: The unique identifier of the contact
                               e.g: 'RPN-823-034-233'
        @type contact_number: String               
        @param requestslib_kwargs: Used for future additions so that we don't 
                                   break current code
        @type requestslib_kwargs: Dictionary
        @return: Headers and response codes without response body       
        """
        
        url = '{0}/v3/contacts/{1}'.format(self.base_url, contact_number)
        
        return self.request('DELETE', url, 
                            requestslib_kwargs=requestslib_kwargs)
                                    
    def get_contact_by_username(self, username=None, requestslib_kwargs=None):
        """
        GET
        /v3/contact_usernames/{username}
        
        
        @summary: Makes a GET request to get contact information by username
        @param username: The username of the contact, e.g: 'john0982'
        @type username: String             
        @param requestslib_kwargs: Used for future additions so that we don't 
                                   break current code
        @type requestslib_kwargs: Dictionary
        @return: Headers and response codes with the contact information in 
                  the response body                
        """
        
        url = '{0}/v3/contact_usernames/{1}'.format(self.base_url, username)
        
        return self.request('GET', url, requestslib_kwargs=requestslib_kwargs)
        
    def grant_contact_role_on_customer_account(self, account_type=None, 
                                               account_number=None, 
                                               contact_number=None, 
                                               role_name=None,
                                               requestslib_kwargs=None):
        """
        PUT
        /v3/customer_accounts/{account_type}/{account_number}/contacts/
                              {contact_number}/roles/{role_name}
                              
        
        @summary: Makes a PUT request to grant a role to the specified contact
        @param account_type: The type of the customer's account, e.g: 'CLOUD'
        @type account_type: String
        @param account_number: The account number of the account to view,
                               e.g: '19293384938'
        @type account_number: String    
        @param contact_number: The unique identifier of the contact
                               e.g: 'RPN-823-034-233'
        @type contact_number: String  
        @param role_name: The name of the role that is to be granted to the 
                          customer's account, e.g: 'BILLING'
        @type role_name: String
        @param requestslib_kwargs: Used for future additions so that we don't 
                                   break current code
        @type requestslib_kwargs: Dictionary
        @return: Headers and response codes without response body       
        """
        
        url = '{0}/v3/customer_accounts/{1}/{2}/contacts/{3}/roles/{4}'.format(
                                        self.base_url, account_type,
                                        account_number, contact_number,
                                        roles_name)
                                            
        return self.request('PUT', url, requestslib_kwargs=requestslib_kwargs)
        
    def delete_contact_role_on_customer_account(self, account_type=None,
                                                account_number=None, 
                                                contact_number=None, 
                                                role_name=None,
                                                requestslib_kwargs=None):
        """
        DELETE
        /v3/customer_accounts/{account_type}/{account_number}/contacts/
                              {contact_number}/roles/{role_name}
                                    
        @summary: Makes a DELETE request to delete the role from the specified
                  customer account                            
        @param account_type: The type of the customer's account, e.g: 'CLOUD'
        @type account_type: String
        @param account_number: The account number of the account to view,
                               e.g: '19293384938'
        @type account_number: String    
        @param contact_number: The unique identifier of the contact
                               e.g: 'RPN-823-034-233'
        @type contact_number: String  
        @param role_name: The name of the role that is to be granted to the 
                          customer's account, e.g: 'BILLING'
        @type role_name: String
        @param requestslib_kwargs: Used for future additions so that we don't 
                                   break current code
        @type requestslib_kwargs: Dictionary
        @return: Headers and response codes without response body                                   
        """
        
        url = '{0}/v3/customer_accounts/{1}/{2}/contacts/{3}/roles/{4}'.format(
                                        self.base_url, account_type,
                                        account_number, contact_number,
                                        roles_name)
                                            
        return self.request('DELETE', url, 
                            requestslib_kwargs=requestslib_kwargs)      
                                        
    def get_list_of_countries(self, requestslib_kwargs=None):
        """
        GET
        /v3/countries
        
        
        @summary: Makes a GET request to get the list of all countries and 
                  corresponding country codes
        @param requestslib_kwargs: Used for future additions so that we don't 
                                   break current code
        @type requestslib_kwargs: Dictionary
        @return: Headers and response codes with list of countries and country
                  codes in the response body          
        """
        
        url = '{0}/v3/countries'.format(self.base_url)
        
        return self.request('GET', url, 
                            response_entity_type=GetCountriesResponse,
                            requestslib_kwargs=requestslib_kwargs)
                                
    def get_country(self, country_code=None, requestslib_kwargs=None):
        """
        GET
        /v3/countries/{country_code}
        
        @summary: Makes a GET request to get the country with the specified 
                  country code
        @param country_code: The country code of the country, e.g: 'US'
        @type country_code: String          
        @param requestslib_kwargs: Used for future additions so that we don't 
                                   break current code
        @type requestslib_kwargs: Dictionary
        @return: Headers and response codes with country in the response body 
        """
        
        url = '{0}/v3/countries/{1}'.format(self.base_url, country_code)
        
        return self.request('GET', url, 
                            response_entity_type=GetCountryResponse,
                            requestslib_kwargs=requestslib_kwargs)
                                
    def get_all_customer_events(self, marker=None, direction=None, limit=None,
                                requestslib_kwargs=None):
        """
        GET
        /v3/events/customers?marker={marker}&direction={direction}&
                                             limit={limit}
        
        
        @summary: Makes a GET request to return all customer events relative
                  to the marker, direction, and limit
        @param marker: (optional) The unique id of an atom entry, 
                       e.g: 'uskdf982988k-urn:289'
                       if not specified, the returned feed will use current day 
                       at start of midnight UTC
        @type marker: String
        @param direction: (optional) The direction from the current marker or 
                          entry to start getting more entries from, defaults
                          to 'forward'
                          values allowed: 'forward' or 'backward'
        @type direction: String
        @param limit: (optional) The number of entries to return, has a default
                      of 50
        @type limit: int
        @param requestslib_kwargs: Used for future additions so that we don't 
                                   break current code
        @type requestslib_kwargs: Dictionary
        @return: Headers and response codes with atom feed of customer events
                  in the response body             
        """
        
        url = '{0}/v3/events/customers'.format(self.base_url)

        #add optional parameters
        params = {}
        if marker is not None:
            params['marker'] = marker                           
        if direction is not None:
            params['direction'] = direction
        if limit is not None:
            params['limit'] = limit
            
        self.request('GET', url, params=params,
                     response_entity_type=GetAllCustomerEventsResponse,
                     requestslib_kwargs=requestslib_kwargs)
        
    def get_customer_event_marker(self, datetime=None, 
                                  requestslib_kwargs=None):
        """
        GET
        /v3/events/customers/marker?datetime={datetime}
        
        
        @summary: Makes a GET request to get the customer event marker for the 
                  specified datetime
        @param datetime: (optional) The datetime where we want to get the 
                         marker for, e.g: '2012-03-11T06:00:00.000-05:00'
                         defaults to current time if none specified
        @param requestslib_kwargs: Used for future additions so that we don't 
                                   break current code
        @type requestslib_kwargs: Dictionary
        @return: Headers and response codes with customer event marker in 
                  the response body           
        """
        
        url = '{0}/v3/events/customers/marker?date={1}'.format(self.base_url,
                                                               datetime)
        
        #add optional parameters to the request
        params = {}
        if datetime is not None:
            params['datetime'] = datetime
            
        self.request('GET', url, params=params,
                     response_entity_type=GetCustomerEventMarkerResponse,
                     requestslib_kwargs=requestslib_kwargs)
        
    def get_all_contact_events(self, marker=None, direction=None, limit=None,
                               requestslib_kwargs=None):
        """
        GET
        /v3/events/contacts?marker={marker}&direction={direction}&
                                             limit={limit}
        
        
        @summary: Makes a GET request to return all contact events relative
                  to the marker, direction, and limit
        @param marker: (optional) The unique id of an atom entry, 
                       e.g: 'uskdf982988k-urn:289'
                       if not specified, the returned feed will use current day 
                       at start of midnight UTC
        @type marker: String
        @param direction: (optional) The direction from the current marker or 
                          entry to start getting more entries from, defaults
                          to 'forward'
                          values allowed: 'forward' or 'backward'
        @type direction: String
        @param limit: (optional) The number of entries to return, has a default
                      of 50
        @type limit: int
        @param requestslib_kwargs: Used for future additions so that we don't 
                                   break current code
        @type requestslib_kwargs: Dictionary
        @return: Headers and response codes with atom feed of customer events
                  in the response body                
        """
        
        url = '{0}/v3/events/contacts'.format(self.base_url)

        #add optional parameters
        params = {}
        if marker is not None:
            params['marker'] = marker                           
        if direction is not None:
            params['direction'] = direction
        if limit is not None:
            params['limit'] = limit
            
        self.request('GET', url, params=params,
                     response_entity_type=GetAllContactEventsResponse,
                     requestslib_kwargs=requestslib_kwargs)
        
    def get_contact_event_marker(self, datetime=None, requestslib_kwargs=None):
        """
        GET
        /v3/events/contacts/marker?datetime={datetime}
        
        @summary: Makes a GET request to get the contact event marker for the 
                  specified datetime
        @param datetime: (optional) The datetime where we want to get the 
                         marker for, e.g: '2012-03-11T06:00:00.000-05:00'
                         defaults to current time if none specified
        @param requestslib_kwargs: Used for future additions so that we don't 
                                   break current code
        @type requestslib_kwargs: Dictionary
        @return: Headers and response codes with contact event marker in 
                  the response body              
        """
        
        url = '{0}/v3/events/contacts/marker?date={1}'.format(self.base_url,
                                                              datetime)
        
        #add optional parameters to the request
        params = {}
        if datetime is not None:
            params['datetime'] = datetime
            
        self.request('GET', url, params=params,
                     response_entity_type=GetContactEventMarkerResponse,
                     requestslib_kwargs=requestslib_kwargs)
        

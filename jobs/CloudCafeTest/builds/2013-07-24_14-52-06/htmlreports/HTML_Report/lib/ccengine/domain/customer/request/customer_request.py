import json
import xml.etree.ElementTree as ET
from ccengine.domain.base_domain import \
    BaseMarshallingDomain, BaseMarshallingDomainList


"""
values to be treated as constants that is used throughout
"""

CUSTOMER_REQ_XMLNS_KEY = 'xmlns'
CUSTOMER_REQ_XMLNS_VALUE = "http://customer.api.rackspace.com/v1"
CUSTOMER_REQ_XMLNS_ATOM_KEY = 'xmlns:atom'
CUSTOMER_REQ_XMLNS_ATOM_VALUE = "http://www.w3.org/2005/Atom"


class ChildCustomersItem(BaseMarshallingDomain):
    """
    @summary: A child customer object
    """

    def __init__(self, number=None):
        """
        @summary: Setup the child customer object
        @param number: The unique identifier of the child customer
                       e.g: 'RCN-111-222-422'
        @type number: String
        """

        self.number = number

    def _obj_to_xml_ele(self):
        """
        @summary: Convert the child customer object to an XML element
        @return: XML element representation of the child customer
        """

        element = ET.Element('customer')
        e_attrs = {}
        e_attrs["number"] = self.number
        element = self._set_xml_attrs(element, e_attrs)

        return element

    def _obj_to_json_dict(self):
        """
        @summary: Convert the child customer object to a JSON dictionary
        @return: JSON representation of the child customer
        """

        attrs = {}
        attrs["number"] = self.number

        attrs = self._remove_empty_values(attrs)
        return attrs


class ChildCustomersList(BaseMarshallingDomainList):
    """
    @summary: A list of child customer objects
    @ivar ROOT_TAG: Used for the XML creation that needs to keep track of
                    parent element
    @type ROOT_TAG: String
    """

    ROOT_TAG = 'childCustomers'

    def append_new_child_customer(self, number=None):
        """
        @summary: Appends the given child customer to the child customers list
        @param number: The unique identifier of the child customer
                       e.g: 'RCN-111-222-422'
        @type number: String
        """

        self.append(ChildCustomersItem(number=number))

    def extend_new_child_customers(self, list_of_child_customers):
        """
        @summary: Takes a list of child customers and extends the current list
        @param list_of_child_customers: The list of child customer objects
                                        e.g: [
                                                 {'number': 'RCN-111-222-422'},
                                                 {'number': 'RCN-283-343-232'}
                                             ]
        @type list_of_child_customers: List of child customer items(Dictionary)
        """

        list_of_child_customers = list_of_child_customers or []
        if list_of_child_customers:
            for child_customer in list_of_child_customers:
                self.append_new_child_customer(**child_customer)

    def _obj_to_xml_ele(self):
        """
        @summary: Converts the child customers list to a XML element
        @return: XML element of child customers list
        """

        element = ET.Element(self.ROOT_TAG)
        for child_customer in self:
            element.append(child_customer._obj_to_xml_ele())

        return element

    def _obj_to_json_dict(self):
        """
        @summary: Converts the child customers list to a JSON dictionary
        @return: JSON dictionary of child customers list
        """

        attrs = {}
        child_customers_list = []
        for child_customer in self:
            child_customers_list.append(child_customer._obj_to_json_dict())
        attrs['customer'] = child_customers_list

        return self._remove_empty_values(attrs)


class CustomerAccountsItem(BaseMarshallingDomain):
    """
    @summary: A customer account object
    """

    def __init__(self, name=None, number=None, status=None, type_=None):
        """
        @summary: Setup of a customer account object
        @param name: The name given to customer account, e.g: 'Hubspot'
        @type name: String
        @param number: The unique identifier of the customer account
                       e.g: '19293384938'
        @type number: String
        @param status: The status of the customer account, e.g: 'Active'
        @type status: String
        @param type_: The type of the customer account, e.g: 'CLOUD'
        @type type_: String
        """

        self.name = name
        self.number = number
        self.status = status
        self.type_ = type_

    def _obj_to_xml_ele(self):
        """
        @summary: Convert customer account object to XML element
        @return: XML element of customer account object
        """

        element = ET.Element('customerAccount')
        e_attrs = {}
        e_attrs["name"] = self.name
        e_attrs["number"] = self.number
        e_attrs["status"] = self.status
        e_attrs["type"] = self.type_
        element = self._set_xml_attrs(element, e_attrs)

        return element

    def _obj_to_json_dict(self):
        """
        @summary: Convert customer account object to JSON dictionary
        @return: JSON dictionary of customer account object
        """

        attrs = {}
        attrs["name"] = self.name
        attrs["number"] = self.number
        attrs["status"] = self.status
        attrs["type"] = self.type_

        attrs = self._remove_empty_values(attrs)
        return attrs


class CustomerAccountsList(BaseMarshallingDomainList):
    """
    @summary: A list of customer account objects
    @ivar ROOT_TAG: Used for the XML creation that needs to keep track of
                    parent element
    @type ROOT_TAG: String
    """

    ROOT_TAG = 'customerAccounts'

    def append_new_customer_account(self, name=None, number=None,
                                    status=None, type_=None):
        """
        @summary: Appends a new customer account to the customer accounts list
        @param name: The name used for the customer account, e.g: 'Hubspot'
        @type name: String
        @param number: The unique identifier for the customer account
                       e.g: '19293384938'
        @type number: String
        @param status: The status of the customer account, e.g: 'Active'
        @type status: String
        @param type_: The type of customer account, e.g: 'CLOUD'
        @type type_: String
        """

        self.append(CustomerAccountsItem(name=name, number=number,
                                         status=status, type_=type_))

    def extend_new_customer_accounts(self, list_of_customer_accounts):
        """
        @summary: Takes a list of customer accounts and extends current list
        @param list_of_customer_accounts: The list of child customer objects
                                          e.g:
                                            [{
                                                'name': 'Hubspot',
                                                'number': '19293384938',
                                                'status': 'Active',
                                                'type_': 'CLOUD'
                                            }]
        @type list_of_customer_accounts: List of customer account
                                         items(Dictionary)
        """

        list_of_customer_accounts = list_of_customer_accounts or []
        if list_of_customer_accounts:
            for customer_account in list_of_customer_accounts:
                self.append_new_customer_account(**customer_account)

    def _obj_to_xml_ele(self):
        """
        @summary: Converts list of customer account object to XML list
        @return: XML list representation of customer account objects
        """

        element = ET.Element(self.ROOT_TAG)
        for customer_account in self:
            element.append(customer_account._obj_to_xml_ele())

        return element

    def _obj_to_json_dict(self):
        """
        @summary: Converts list of customer account object to JSON list
        @return: JSON list of customer account objects
        """

        attrs = {}
        customer_accounts_list = []
        for customer_account in self:
            customer_accounts_list.append(customer_account._obj_to_json_dict())
        attrs['customerAccount'] = customer_accounts_list

        return self._remove_empty_values(attrs)


class AddressesItem(BaseMarshallingDomain):
    """
    @summary: An address object
    """

    def __init__(self, city=None, country=None, primary=None, state=None,
                 street=None, zipcode=None):
        """
        @summary: Setup of the address object
        @param city: The city of the address, e.g: 'San Francisco'
        @type city: String
        @param country: The country of the address, e.g: 'US'
        @type country: String
        @param primary: Indicates if primary address, e.g: 'true'
        @type primary: String of a boolean
        @param state: The state of the address, e.g: 'Texas'
        @type state: String
        @param street: The street address of the address,
                       e.g: '1 Dezavala Place'
        @type street: String
        @param zipcode: The zipcode of the address, e.g: '78366'
        @type zipcode: String
        """

        self.city = city
        self.country = country
        self.primary = primary
        self.state = state
        self.street = street
        self.zipcode = zipcode

    def _obj_to_xml_ele(self):
        """
        @summary: Converts address object to XML element
        @return: XML element representation of address object
        """

        element = ET.Element('address')
        e_attrs = {}
        e_attrs["city"] = self.city
        e_attrs["country"] = self.country
        e_attrs["primary"] = self.primary
        e_attrs["state"] = self.state
        e_attrs["street"] = self.street
        e_attrs["zipcode"] = self.zipcode
        return self._set_xml_attrs(element, e_attrs)

    def _obj_to_json_dict(self):
        """
        @summary: Converts address object to JSON dictionary
        @return: JSON dictionary representation of address object
        """

        attrs = {}
        attrs["city"] = self.city
        attrs["country"] = self.country
        attrs["primary"] = self.primary
        attrs["state"] = self.state
        attrs["street"] = self.street
        attrs["zipcode"] = self.zipcode
        return self._remove_empty_values(attrs)


class AddressesList(BaseMarshallingDomainList):
    """
    @summary: A list of address objects
    @ivar ROOT_TAG: Used for the XML creation that needs to keep track of
                    parent element
    @type ROOT_TAG: String
    """

    ROOT_TAG = 'addresses'

    def append_new_address(self, city=None, country=None, primary=None,
                           state=None, street=None, zipcode=None):
        """
        @summary: Appends a new address to the addresses list
        @param city: The city of the address, e.g: 'San Francisco'
        @type city: String
        @param country: The country code of the address, e.g: 'US'
        @type country: String
        @param primary: Indicates if primary address, e.g: 'true'
        @type primary: String of a boolean
        @param state: The state of the address, e.g: 'Texas'
        @type state: String
        @param street: The street address of the address,
                       e.g: '1 Dezavala Place'
        @type street: String
        @param zipcode: The zipcode of the address, e.g: '78366'
        @type zipcode: String
        """

        self.append(AddressesItem(city=city, country=country,
                                  primary=primary, state=state,
                                  street=street, zipcode=zipcode))

    def extend_new_addresses(self, list_of_addresses):
        """
        @summary: Takes a list of addresses and extends current list
        @param list_of_addresses: List of address objects.
                                  e.g: [{
                                           'zipcode':'78366',
                                           'street':'1 Dezavala Place',
                                           'primary': 'true',
                                           'state':'Texas',
                                           'country':'US',
                                           'city':'San Francisco'
                                       }]
        @type list_of_addresses: List of addresses(Dictionary)
        """

        list_of_addresses = list_of_addresses or []
        if list_of_addresses:
            for address in list_of_addresses:
                self.append_new_address(**address)

    def _obj_to_xml_ele(self):
        """
        @summary: Converts list of address objects to XML list
        @return: XML list representation of address objects
        """

        element = ET.Element(self.ROOT_TAG)
        for address in self:
            element.append(address._obj_to_xml_ele())

        return element

    def _obj_to_json_dict(self):
        """
        @summary: Converts list of address objects to JSON list
        @return: JSON list representation of address objects
        """

        attrs = {}
        addresses_list = []
        for address in self:
            addresses_list.append(address._obj_to_json_dict())
        attrs['address'] = addresses_list

        return self._remove_empty_values(attrs)


class EmailAddressesItem(BaseMarshallingDomain):
    """
    @summary: A email address object
    """

    def __init__(self, address=None, primary=None):
        """
        @summary: Setup of email address object
        @param address: The address of the email address,
                        e.g: 'test@testing.com'
        @type address: String
        @param primary: Indicates if primary email address, e.g: 'true'
        @type primary: String of a boolean
        """

        self.address = address
        self.primary = primary

    def _obj_to_xml_ele(self):
        """
        @summary: Converts email address object to XML element
        @return: XML element representation of email address object
        """

        element = ET.Element('emailAddress')
        e_attrs = {}
        e_attrs["address"] = self.address
        e_attrs["primary"] = self.primary
        return self._set_xml_attrs(element, e_attrs)

    def _obj_to_json_dict(self):
        """
        @summary: Converts email address object to JSON dictionary
        @return: JSON dictionary representation of email address object
        """

        attrs = {}
        attrs["address"] = self.address
        attrs["primary"] = self.primary
        return self._remove_empty_values(attrs)


class EmailAddressesList(BaseMarshallingDomainList):
    """
    @summary: A list of email address objects
    @ivar ROOT_TAG: Used for the XML creation that needs to keep track of
                    parent element
    @type ROOT_TAG: String
    """

    ROOT_TAG = 'emailAddresses'

    def append_new_email_address(self, address=None, primary=None):
        """
        @summary: Appends new email address to email addresses list
        @param address: The address of the email address,
                        e.g: 'test@testing.com'
        @type address: String
        @param primary: Indicates if primary email address, e.g: 'true'
        @type primary: String of a boolean
        """

        self.append(EmailAddressesItem(address=address, primary=primary))

    def extend_new_email_addresses(self, list_of_email_addresses):
        """
        @summary: Takes a list of email addresses and extends current list
        @param list_of_email_addresses: List of email address objects
                                        e.g: [{
                                                 'address': 'test@test.com',
                                                 'primary': 'true'
                                             }]
        @type list_of_email_addresses: List of email addresses(Dictionary)
        """

        list_of_email_addresses = list_of_email_addresses or []
        if list_of_email_addresses:
            for email_address in list_of_email_addresses:
                self.append_new_email_address(**email_address)

    def _obj_to_xml_ele(self):
        """
        @summary: Converts list of email address objects to XML list
        @return: XML list representation of email addresses
        """

        element = ET.Element(self.ROOT_TAG)
        for email_address in self:
            element.append(email_address._obj_to_xml_ele())

        return element

    def _obj_to_json_dict(self):
        """
        @summary: Converts list of email address objects to JSON list
        @return: JSON list representation of email addresses
        """

        attrs = {}
        email_addresses_list = []
        for email_address in self:
            email_addresses_list.append(email_address._obj_to_json_dict())
        attrs['emailAddress'] = email_addresses_list
        return self._remove_empty_values(attrs)


class PhoneNumbersItem(BaseMarshallingDomain):
    """
    @summary: A phone number object
    """

    def __init__(self, country=None, number=None):
        """
        @summary: Setup for phone number object
        @param country: The country code for the phone number, e.g: 'US'
        @type country: String
        @param number: The actual number to the phone number, e.g: '8374384343'
        @type number: String
        """

        self.country = country
        self.number = number

    def _obj_to_xml_ele(self):
        """
        @summary: Converts phone number object to XML element
        @return: XML element representation of phone number object
        """

        element = ET.Element('phoneNumber')
        e_attrs = {}
        e_attrs["country"] = self.country
        e_attrs["number"] = self.number
        return self._set_xml_attrs(element, e_attrs)

    def _obj_to_json_dict(self):
        """
        @summary: Converts phone number object to JSON
        @return: JSON representation of phone number object
        """

        attrs = {}
        attrs["country"] = self.country
        attrs["number"] = self.number
        return self._remove_empty_values(attrs)


class PhoneNumbersList(BaseMarshallingDomainList):
    """
    @summary: A list of phone number objects
    @ivar ROOT_TAG: Used for the XML creation that needs to keep track of
                    parent element
    @type ROOT_TAG: String
    """

    ROOT_TAG = 'phoneNumbers'

    def append_new_phone_number(self, country=None, number=None):
        """
        @summary: Appends new phone number to phone numbers list
        @param country: The country code for the phone number, e.g: 'US'
        @type country: String
        @param number: The actual number to the phone number, e.g: '8374384343'
        @type number: String
        """

        self.append(PhoneNumbersItem(country=country, number=number))

    def extend_new_phone_numbers(self, list_of_phone_numbers):
        """
        @summary: Takes a list of phone numbers and extends current list
        @param list_of_phone_numbers: List of phone number objects
                                      e.g: [{
                                               'number': '8374384343',
                                               'country': 'US'
                                           }]
        @type list_of_phone_numbers: List of phone numbers(Dictionary)
        """

        list_of_phone_numbers = list_of_phone_numbers or []
        if list_of_phone_numbers:
            for phone_number in list_of_phone_numbers:
                self.append_new_phone_number(**phone_number)

    def _obj_to_xml_ele(self):
        """
        @summary: Converts list of phone number objects to XML list
        @return: XML list representation of phone numbers
        """

        element = ET.Element(self.ROOT_TAG)
        for phone_number in self:
            element.append(phone_number._obj_to_xml_ele())

        return element

    def _obj_to_json_dict(self):
        """
        @summary: Converts list of phone number objects to JSON list
        @return: JSON list representation of phone numbers
        """

        attrs = {}
        phone_numbers_list = []
        for phone_number in self:
            phone_numbers_list.append(phone_number._obj_to_json_dict())
        attrs['phoneNumber'] = phone_numbers_list
        return self._remove_empty_values(attrs)

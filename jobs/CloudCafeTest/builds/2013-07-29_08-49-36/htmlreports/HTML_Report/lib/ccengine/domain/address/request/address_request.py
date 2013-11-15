# -*- coding: utf-8 -*-

import json
import xml.etree.ElementTree as ET
from ccengine.domain.base_domain import BaseMarshallingDomain

"""
values to be treated as constants that is used throughout
"""

ADDRESS_REQ_XMLNS_KEY = 'xmlns'
ADDRESS_REQ_XMLNS_VALUE = "http://address.api.rackspace.com/v1"
ADDRESS_REQ_XMLNS_ATOM_KEY = 'xmlns:atom'
ADDRESS_REQ_XMLNS_ATOM_VALUE = "http://www.w3.org/2005/Atom"


class AddressRequest(BaseMarshallingDomain):
    """
    @summary: The request that contains address information
    """

    def __init__(self, street=None, city=None, state=None,
                 zipcode=None, country=None):
        """
        @summary: Setup of the address request
        @param street: The street of the address, e.g: '1 Dezavala Place'
        @type street: String
        @param city: The city of the address, e.g: 'San Francisco'
        @type city: String
        @param state: The state of the address, e.g: 'Texas'
        @type state: String
        @param zipcode: The zipcode of the address, e.g: '78366'
        @type zipcode: String
        @param country: The country code of the address, e.g: 'US'
        @type country: String
        """

        self.street = street
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.country = country

    def _obj_to_xml_ele(self):
        """
        @summary: Serialize the address request to XML
        @return: Serialized XML of address request
        """

        element = ET.Element('address')
        e_attrs = {}
        e_attrs[ADDRESS_REQ_XMLNS_KEY] = ADDRESS_REQ_XMLNS_VALUE
        e_attrs[ADDRESS_REQ_XMLNS_ATOM_KEY] = ADDRESS_REQ_XMLNS_ATOM_VALUE

        e_attrs['street'] = self.street
        e_attrs['city'] = self.city
        e_attrs['state'] = self.state
        e_attrs['zipcode'] = self.zipcode
        e_attrs['country'] = self.country

        element = self._set_xml_attrs(element, e_attrs)

        return element

    #Reqeust Generators
    def _obj_to_json_dict(self):
        """
        @summary: Serialize the address request to JSON
        @return: Serialized JSON dictionary of address request
        """

        attrs = {}
        attrs['street'] = self.street
        attrs['city'] = self.city
        attrs['state'] = self.state
        attrs['zipcode'] = self.zipcode
        attrs['country'] = self.country

        return self._remove_empty_values(attrs)

    def _obj_to_json(self):
        """
        @summary: Converts the address request to JSON
        @return: JSON of create customer request
        """

        return json.dumps(self._obj_to_json_dict())

    def _obj_to_xml(self):
        """
        @summary: Converts the address request to XML string
        @return: XML string representation of create customer request,
                 UTF-8 is used for the encoding so that we can pass diacritics
        """

        return ET.tostring(self._obj_to_xml_ele(), encoding="UTF-8")

import json
import xml.etree.ElementTree as ET
from ccengine.domain.base_domain import \
    BaseMarshallingDomain, \
    BaseMarshallingDomainList
from ccengine.domain.customer.response.xml_tools import XMLTools


class GetListOfCountriesResponse(BaseMarshallingDomain):
    """
    @summary: The list of countries response object
    """

    def __init__(self, countries=None):
        """
        @summary: Setup of the list of countries response object
        @param countries: A list of countries
        @type countries: CountriesList
        """

        if countries is not None:
            self.countries = CountriesList()

            if XMLTools._is_et_elem(countries):
                self.countries._xml_ele_to_obj(countries)
            else:
                self.countries.extend_new_countries(countries)
        else:
            self.countries = None

    @classmethod
    def _json_ele_to_obj(cls, dict_to_convert):
        """
        @summary: Converts the JSON response to a GetListOfCountriesResponse
                  object
        @param dict_to_convert: The dictionary that will be converted to a
                                GetListOfCountriesResponse object
        @type dict_to_convert: dict
        @return: A GetListOfCountriesResponse object
        """

        countries = dict_to_convert['country']

        return GetListOfCountriesResponse(countries=countries)

    @classmethod
    def _json_to_obj(cls, serialized_str):
        """
        @summary: Converts an JSON serialized string to an object
        @param serialized_str: The serialized JSON string
        @type serialized_str: String
        @return: Object representation of the serialized string
        """

        json_dict = json.loads(serialized_str)

        return cls._dict_to_obj(json_dict)

    @classmethod
    def _xml_ele_to_obj(cls, element):
        """
        @summary: Converts the XML element to a GetListOfCountriesResponse
                  object
        @param element: The XML element that will be converted to a
                        GetListOfCountriesResponse object
        @type element: ElementTree.Element
        @return: A GetListOfCountriesResponse object
        """

        elem = XMLTools._remove_namespace(element)
        children = XMLTools._get_children(elem)

        countries = children.get('country', None)

        return GetListOfCountriesResponse(countries=countries)

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        """
        @summary: Converts a XML serialized string to an object
        @param serialized_str: The serialized XML string
        @type serialized_str: String
        @return: Object representation of the serialized string
        """

        element = ET.fromstring(serialized_str)

        return cls._xml_ele_to_obj(element)


class CountriesItem(BaseMarshallingDomain):
    """
    @summary: The country object
    """

    def __init__(self, code=None, name=None, link=None):
        """
        @summary: Setup of the country object
        @param code: The country code, e.g: 'US'
        @type code: String
        @param name: The name of the country, e.g: 'United States'
        @type name: String
        @param link: The link to the information of the country
        @type link: LinksList()
        """

        self.code = code
        self.name = name

        if link is not None:
            self.link = LinksList()

            if XMLTools._is_et_elem(link):
                self.link._xml_ele_to_obj(link)
            else:
                self.link.extend_new_links(link)
        else:
            self.link = None

    @classmethod
    def _xml_ele_to_obj(cls, element):
        """
        @summary: Creates the CountriesItem object from an XML element
        @param element: The XML element to be converted to a CountriesItem
                        object
        @type element: ElementTree.Element
        @return: CountriesItem object
        """

        elem = XMLTools._remove_namespace(element)
        children = XMLTools._get_children(elem)

        code = elem.get('code', None)
        name = elem.get('name', None)
        link = children.get('link', None)

        return CountriesItem(code=code, name=name, link=link)


class CountriesList(BaseMarshallingDomainList):
    """
    @summary: A list of country objects
    """

    def append_new_country(self, code=None, name=None, link=None):
        """
        @summary: Appends a new country to the list of countries
        @param code: The country code of the country, e.g: 'US'
        @type code: String
        @param name: The name of the country, e.g: 'United States'
        @type name: String
        @param link: The link to the information of the country
        @type link: LinksList()
        """

        self.append(CountriesItem(code=code, name=name, link=link))

    def extend_new_countries(self, list_of_countries):
        """
        @summary: Takes a list of countries and extends the current list
        @param list_of_countries: The list of countries to add
        @type list_of_countries: CountriesList()
        """

        list_of_countries = list_of_countries or []

        if list_of_countries:
            for country in list_of_countries:
                self.append_new_country(**country)

    def _xml_ele_to_obj(self, element):
        """
        @summary: Takes a list of XML elements and builds a list of
                  CountriesItem objects
        @param element: A list of similar XML element types
        @type element: list of ElementTree.Element
        """

        elem = XMLTools._remove_namespace(element)

        for item in elem:
            country = CountriesItem._xml_ele_to_obj(item)
            self.append(country)


class LinksList(BaseMarshallingDomainList):
    """
    @summary: Creates a list of links (href, rel)
    """

    def append_new_link(self, href=None, rel=None):
        """
        @summary: Appends a new link to the list of links
        @param href: The link destination, e.g: 'http://blahblahblah.com'
        @type href: String
        @param rel: The relationship between the current document and the
                    linked document, e.g: 'via', 'alternate'
        @type rel: String
        """

        self.append(LinksItem(href=href, rel=rel))

    def extend_new_links(self, list_of_links):
        """
        @summary: Takes the list of new links and extends current list
        @param list_of_links: The list of new links,
                              e.g: [{
                                       'href': 'http://blahblahblah.com',
                                       'rel': 'via'
                                   }]
        @type list_of_links: LinksList()
        """

        list_of_links = list_of_links or []

        if list_of_links:
            for link in list_of_links:
                self.append_new_link(**link)

    def _xml_ele_to_obj(self, element):
        """
        @summary: Takes a list of XML elements and builds a list of
                  CountriesItem objects
        @param element: A list of similar XML element types
        @type element: list of ElementTree.Element
        """

        elem = XMLTools._remove_namespace(element)

        for item in elem:
            link = LinksItem._xml_ele_to_obj(item)
            self.append(link)


class LinksItem(BaseMarshallingDomain):
    """
    @summary: A link object that contains the href and rel
    """

    def __init__(self, href=None, rel=None):
        """
        @summary: Setup of the link object
        @param href: The link destination, e.g: 'http://blahblahblah.com'
        @type href: String
        @param rel: The relationship between the current document and the
                    linked document, e.g: 'via', 'alternate'
        @type rel: String
        """

        self.href = href
        self.rel = rel

    @classmethod
    def _xml_ele_to_obj(cls, element):
        """
        @summary: Creates the LinksItem object from an XML element
        @param element: The XML element to be converted to a LinksItem object
        @type element: ElementTree.Element
        @return: LinksItem object
        """

        elem = XMLTools._remove_namespace(element)

        href = elem.get('href', None)
        rel = elem.get('rel', None)

        return LinksItem(href=href, rel=rel)

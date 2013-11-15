from ccengine.domain.base_domain import \
    BaseMarshallingDomain, BaseMarshallingDomainList
from ccengine.domain.address.response.parse_to_obj import \
    ParseToObj


class GetListOfCountriesResponse(ParseToObj, BaseMarshallingDomain):
    """
    @summary: The list of countries response object
    """

    def __init__(self, countries=None):
        """
        @summary: Setup of the list of countries response object
        @param countries: A list of countries
        @type countries: CountriesList()
        """

        if countries is not None:
            self.countries = CountriesList()
            self.countries.extend_new_countries(countries)
        else:
            self.countries = None

    @classmethod
    def _dict_to_obj(cls, dict_to_convert):
        """
        @summary: Converts a dictionary to a GetListOfCountriesResponse object
        @param dict_to_convert: The dictionary that will be converted to a
                                GetListOfCountriesResponse object
        @type dict_to_convert: Dictionary
        @return: A GetListOfCountriesResponse object
        """

        countries = dict_to_convert['country']

        return GetListOfCountriesResponse(countries=countries)


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
            self.link.extend_new_links(link)


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


class GetCountryResponse(ParseToObj, BaseMarshallingDomain):
    """
    @summary: The get country response object
    """

    def __init__(self, code=None, name=None, phonemask=None, states=None):
        """
        @summary: Setup of the GetCountryResponse object
        @param states: The list of states
        @type states: StatesList()
        """

        self.code = code
        self.name = name
        self.phonemask = phonemask

        if states is not None:
            self.states = StatesList()
            self.states.extend_new_states(states)
        else:
            self.states = None

    @classmethod
    def _dict_to_obj(cls, dict_to_convert):
        """
        @summary: Converts a dictionary to a GetCountryResponse object
        @param dict_to_convert: The dictionary that will be converted to a
                                GetCountryResponse object
        @type dict_to_convert: Dictionary
        @return: A GetCountryResponse object
        """

        code = dict_to_convert['code']
        name = dict_to_convert['name']
        phonemask = dict_to_convert['phonemask']
        states = dict_to_convert['states']

        return GetCountryResponse(code=code, name=name, phonemask=phonemask,
                                  states=states)


class StatesItem(BaseMarshallingDomain):
    """
    @summary: The state object
    """

    def __init__(self, code=None, name=None, type_=None):
        """
        @summary: Setup of the state object
        @param code: The postal state abbreviation code, e.g: 'TX'
        @type code: String
        @param name: The name of the state, e.g: 'Texas'
        @type name: String
        @param type_: The type of the state, e.g: 'State'
        @type type_: String
        """

        self.code = code
        self.name = name
        self.type_ = type_


class StatesList(BaseMarshallingDomainList):
    """
    @summary: A list of state objects
    """

    def append_new_state(self, code=None, name=None, type_=None):
        """
        @summary: Appends a new state to the list of state objects
        @param code: The postal state abbreviation code, e.g: 'TX'
        @type code: String
        @param name: The name of the state, e.g: 'Texas'
        @type name: String
        @param type_: The type of the state, e.g: 'State'
        @type type_: String
        """

        self.append(StatesItem(code=code, name=name, type_=type_))

    def extend_new_states(self, list_of_states):
        """
        @summary: Takes a list of states and extends the current list
        @param list_of_states: A list of states
        @type list_of_states: List of states(Dictionary) - StatesItem
        """

        list_of_states = list_of_states or []

        if list_of_states:
            for state in list_of_states:
                if 'type' in state:
                    state['type_'] = state['type']
                    del state['type']

                self.append_new_state(**state)


class ErrorFieldsItem(BaseMarshallingDomain):
    """
    @summary: The error field object, which holds a description of the error
    """

    def __init__(self, description=None, name=None):
        """
        @summary: Setup of the error field object
        @param description: The description of the error
        @type description: String
        @param name: The field which has the error, e.g: 'zipcode'
        @type name: String
        """

        self.description = description
        self.name = name


class ErrorFieldsList(BaseMarshallingDomainList):
    """
    @summary: A list of error field objects
    """

    def append_new_error_field(self, description=None, name=None):
        """
        @summary: Appends a new error field object to the error fields list
        @param description: The description of the error
        @type description: String
        @param name: The field which has the error, e.g: 'zipcode'
        @type name: String
        """

        self.append(ErrorFieldsItem(description=description, name=name))

    def extend_new_error_fields(self, list_of_error_fields=None):
        """
        @summary: Takes a list of error fields and extends current list
        @param list_of_error_fields: A list of error fields
        @type list_of_error_fields: List of error fields(Dictionary)
        """

        list_of_error_fields = list_of_error_fields or []

        if list_of_error_fields:
            for error_field in list_of_error_fields:
                self.append_new_error_field(**error_field)


class ValidateAddressResponse(ParseToObj, BaseMarshallingDomain):
    """
    @summary: The validation result response object
    """

    def __init__(self, outcome=None, error_fields=None):
        """
        @summary: Setup of the address validation response object
        @param outcome: The outcome of the validation,
                        e.g: 'VALID' or 'INVALID'
        @type outcome: String
        """

        self.outcome = outcome

        if error_fields is not None:
            self.error_fields = ErrorFieldsList()
            self.error_fields.extend_new_error_fields(error_fields)
        else:
            self.error_fields = None

    @classmethod
    def _dict_to_obj(cls, dict_to_convert):
        """
        @summary: Converts a dictionary to a ValidateAddressResponse object
        @param dict_to_convert: The dictionary that will be converted to a
                                ValidateAddressResponse object
        @type dict_to_convert: Dictionary
        @return: A ValidateAddressResponse object
        """

        outcome = dict_to_convert['outcome']

        if 'errorField' in dict_to_convert:
            error_fields = dict_to_convert['errorField']
        else:
            error_fields = None

        return ValidateAddressResponse(outcome=outcome,
                                       error_fields=error_fields)


class SuggestedAddressesResponse(ParseToObj, BaseMarshallingDomain):
    """
    @summary: The suggested addresses response object
    """

    def __init__(self, count=None, status=None, addresses=None):
        """
        @summary: Setup for the SuggestedAddressesResponse object
        @param count: The number of address suggestions
        @type count: int
        @param status: The status of the address suggestions, e.g: 'PROCESSED'
        @type status: String
        @param addresses: The list of suggested addresses
        @type addresses: AddressesList()
        """

        self.count = count
        self.status = status

        if addresses is not None:
            self.addresses = AddressesList()
            self.addresses.extend_new_addresses(addresses)
        else:
            self.addresses = None

    @classmethod
    def _dict_to_obj(cls, dict_to_convert):
        """
        @summary: Converts a dictionary to a SuggestedAddressesResponse object
        @param dict_to_convert: The dictionary that will be converted to a
                                SuggestedAddressesResponse object
        @type dict_to_convert: Dictionary
        @return: A SuggestedAddressesResponse object
        """

        count = dict_to_convert['count']
        status = dict_to_convert['status']
        addresses = dict_to_convert['address']

        return SuggestedAddressesResponse(count=count, status=status,
                                          addresses=addresses)


class AddressesItem(BaseMarshallingDomain):
    """
    @summary: The address object which contains the address and scoring info
    """

    def __init__(self, street=None, city=None, state=None,
                 zipcode=None, country=None, selectable=None, score=None):
        """
        @summary: Setup of the address object
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
        @param selectable: Indicates if the suggested address is selectable
        @type selectable: bool
        @param score: The score of the suggested address, from 0-100
        @type score: String
        """

        self.street = street
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.country = country
        self.selectable = selectable
        self.score = score


class AddressesList(BaseMarshallingDomainList):
    """
    @summary: A list of address objects
    """
    def append_new_address(self, street=None, city=None, state=None,
                           zipcode=None, country=None, selectable=None,
                           score=None):
        """
        @summary: Appends a new address to the list of addresses
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
        @param selectable: Indicates if the suggested address is selectable
        @type selectable: bool
        @param score: The score of the suggested address, from 0-100
        @type score: String
        """

        self.append(AddressesItem(street=street, city=city, state=state,
                                  zipcode=zipcode, country=country,
                                  selectable=selectable, score=score))

    def extend_new_addresses(self, list_of_addresses):
        """
        @summary: Takes a list of address and extends the current list
        @param list_of_addresses: A list of addresses
        @type list_of_addresses: List of addresses(Dictionary) - AddressesItem
        """

        list_of_addresses = list_of_addresses or []

        if list_of_addresses:
            for address in list_of_addresses:
                self.append_new_address(**address)

import json
import xml.etree.ElementTree as ET
from ccengine.domain.base_domain import BaseMarshallingDomain, \
    BaseMarshallingDomainList

SIGNUP_REQ_XMLNS_KEY = 'xmlns'
SIGNUP_REQ_XMLNS_VALUE = "http://signup.api.rackspace.com/v1.0"
SIGNUP_REQ_XMLNS_ATOM_KEY = 'xmlns:atom'
SIGNUP_REQ_XMLNS_ATOM_VALUE = "http://www.w3.org/2005/Atom"


def bool_to_string_xml(value, true_string='true', false_string='false'):
    if isinstance(value, bool):
        return true_string if value else false_string
    return value


class BaseMarshallingSubDomain(BaseMarshallingDomain):

    def _obj_to_xml(self):
        return ET.tostring(self._obj_to_xml_ele())

    def _obj_to_xml_ele(self):
        raise NotImplementedError


class BaseMarshallingSubDomainList(BaseMarshallingDomainList):

    def _obj_to_xml(self):
        return ET.tostring(self._obj_to_xml_ele())

    def _obj_to_xml_ele(self):
        element = ET.Element(self.ROOT_TAG)

        for item in self:
            element.append(item._obj_to_xml_ele())
        return element

    def _obj_to_json(self):
        return json.dumps(self._obj_to_json_dict())

    def _obj_to_json_list(self):
        things = []
        for item in self:
            things.append(item._obj_to_json_ele())
        return things


class SignupRequest(BaseMarshallingDomain):

    def __init__(self, accept_terms_and_conditions=None, account_name=None,
                 business_type=None, promo_code=None, region=None,
                 service_level=None, terms_and_conditions=None, type_=None,
                 vat_code=None, xmlns=None, xmlns_atom=None,
                 contacts=None, payment_method=None, description=None,
                 metadata=None, order=None, affiliate_code_and_type=None,
                 skip_fraud_check=None, referral_code=None,
                 managed_account_number=None, geo_location=None,
                 geography=None, default_region=None):

        self.accept_terms_and_conditions = accept_terms_and_conditions
        self.account_name = account_name
        self.business_type = business_type
        self.promo_code = promo_code
        self.region = region
        self.service_level = service_level
        self.terms_and_conditions = terms_and_conditions
        self.type_ = type_
        self.vat_code = vat_code
        self.skip_fraud_check = skip_fraud_check
        self.referral_code = referral_code
        self.managed_account_number = managed_account_number
        self.xmlns = xmlns
        self.xmlns_atom = xmlns_atom
        self.geo_location = geo_location
        self.geography = geography
        self.default_region = default_region

        #Create sub domain objects
        self.contacts = Contacts()
        self.payment_method = PaymentMethod()
        self.description = Description(description)
        self.metadata = Metadata()
        self.order = Order(**(order or {})) if order is not None else None
        self.affiliate_code_and_type = AffiliateCodeandType(
            **(affiliate_code_and_type or {})) \
            if affiliate_code_and_type is not None else None

        #Init sub domain list objects
        self.contacts.extend_new_contacts(contacts)
        self.metadata.extend_new_properties(metadata)
        payment_method = payment_method or {}
        for key in payment_method:
            datadict = payment_method[key] or {}
            if key == 'consolidated_invoice':
                self.payment_method.append_new_consolidated_invoice(**datadict)
            elif key == 'payment_card':
                self.payment_method.append_new_payment_card(**datadict)

    def _obj_to_xml_ele(self):
        element = ET.Element('signupRequest')
        e_attrs = {}
        e_attrs[SIGNUP_REQ_XMLNS_KEY] = self.xmlns or SIGNUP_REQ_XMLNS_VALUE
        e_attrs[SIGNUP_REQ_XMLNS_ATOM_KEY] = self.xmlns_atom or\
            SIGNUP_REQ_XMLNS_ATOM_VALUE
        e_attrs["acceptTermsAndConditions"] = bool_to_string_xml(
            self.accept_terms_and_conditions)
        e_attrs["accountName"] = self.account_name
        e_attrs["businessType"] = self.business_type
        e_attrs["promoCode"] = self.promo_code
        e_attrs["region"] = self.region
        e_attrs["serviceLevel"] = self.service_level
        e_attrs["termsAndConditions"] = self.terms_and_conditions
        e_attrs["type"] = self.type_
        e_attrs["vatCode"] = self.vat_code
        e_attrs["skipFraudCheck"] = bool_to_string_xml(self.skip_fraud_check)
        e_attrs["referralCode"] = self.referral_code
        e_attrs["managedAccountNumber"] = self.managed_account_number
        e_attrs["geoLocation"] = self.geo_location
        e_attrs["geography"] = self.geography
        e_attrs["defaultRegion"] = self.default_region
        element = self._set_xml_attrs(element, e_attrs)

        #Serialize all the sub domain objects and append them to this object's
        #element
        element.append(self.contacts._obj_to_xml_ele())
        element.append(self.payment_method._obj_to_xml_ele())
        element.append(self.description._obj_to_xml_ele())
        element.append(self.metadata._obj_to_xml_ele())
        element.append(self.order._obj_to_xml_ele())
        if self.affiliate_code_and_type is not None:
            element.append(self.affiliate_code_and_type._obj_to_xml_ele())
        return element

    #Reqeust Generators
    def _obj_to_json_dict(self):
        attrs = {}
        attrs['acceptTermsAndConditions'] = self.accept_terms_and_conditions
        attrs['accountName'] = self.account_name
        attrs['businessType'] = self.business_type
        attrs['promoCode'] = self.promo_code
        attrs['region'] = self.region
        attrs['serviceLevel'] = self.service_level
        attrs['termsAndConditions'] = self.terms_and_conditions
        attrs['type'] = self.type_
        attrs['vatCode'] = self.vat_code
        attrs["skipFraudCheck"] = self.skip_fraud_check
        attrs["referralCode"] = self.referral_code
        attrs["managedAccountNumber"] = self.managed_account_number
        attrs["geoLocation"] = self.geo_location
        attrs["geography"] = self.geography
        attrs["defaultRegion"] = self.default_region

        #Serialize sub domain objects
        attrs['contacts'] = self.contacts._obj_to_json_dict()
        if self.affiliate_code_and_type is not None:
            attrs['affiliateCodeAndType'] =\
                self.affiliate_code_and_type._obj_to_json_dict()
        if self.order is not None:
            attrs['order'] = self.order._obj_to_json_dict()
        attrs['paymentMethod'] = self.payment_method._obj_to_json_dict()
        attrs['metadata'] = self.metadata._obj_to_json_dict()
        attrs['description'] = self.description.\
            _obj_to_json_dict()['description']

        return self._remove_empty_values(attrs)

    def _obj_to_json(self):
        return json.dumps(self._obj_to_json_dict())

    def _obj_to_xml(self):
        return ET.tostring(self._obj_to_xml_ele())


class Contact(BaseMarshallingSubDomain):
    def __init__(self, first_name=None, last_name=None, suffix=None,
                 title=None, addresses=None, email_addresses=None,
                 phone_numbers=None, roles=None, user=None):

        self.first_name = first_name
        self.last_name = last_name
        self.suffix = suffix
        self.title = title

        #Initialize Sub domain object dictionaries
        self.addresses = Addresses()
        self.email_addresses = EmailAddresses()
        self.phone_numbers = PhoneNumbers()
        self.roles = Roles()
        self.user = User(**(user or {}))

        #Init sub domain list objects
        self.addresses.extend_new_addresses(addresses)
        self.email_addresses.extend_new_email_addresses(email_addresses)
        self.phone_numbers.extend_new_phone_numbers(phone_numbers)
        self.roles.extend_new_roles(roles)

    def _obj_to_xml_ele(self):
        element = ET.Element('contact')
        e_attrs = {}
        e_attrs["firstName"] = self.first_name
        e_attrs["lastName"] = self.last_name
        e_attrs["suffix"] = self.suffix
        e_attrs["title"] = self.title
        element = self._set_xml_attrs(element, e_attrs)

        element.append(self.addresses._obj_to_xml_ele())
        element.append(self.email_addresses._obj_to_xml_ele())
        element.append(self.phone_numbers._obj_to_xml_ele())
        element.append(self.roles._obj_to_xml_ele())
        element.append(self.user._obj_to_xml_ele())

        return element

    def _obj_to_json_dict(self):
        attrs = {}
        attrs["firstName"] = self.first_name
        attrs["lastName"] = self.last_name
        attrs["suffix"] = self.suffix
        attrs["title"] = self.title

        attrs['addresses'] = self.addresses._obj_to_json_dict()
        attrs['emailAddresses'] = self.email_addresses._obj_to_json_dict()
        attrs['phoneNumbers'] = self.phone_numbers._obj_to_json_dict()
        attrs['roles'] = self.roles._obj_to_json_dict()
        attrs['user'] = self.user._obj_to_json_dict()

        attrs = self._remove_empty_values(attrs)
        return attrs


class Contacts(BaseMarshallingSubDomainList):
    ROOT_TAG = 'contacts'

    def append_new_contact(self, first_name=None, last_name=None, suffix=None,
                           title=None, addresses=None, email_addresses=None,
                           phone_numbers=None, roles=None, user=None):

        self.append(
            Contact(
                first_name=first_name,
                last_name=last_name,
                suffix=suffix,
                title=title,
                addresses=addresses,
                email_addresses=email_addresses,
                phone_numbers=phone_numbers,
                roles=roles, user=user))

    def extend_new_contacts(self, list_of_kwarg_dicts):
        list_of_kwarg_dicts = list_of_kwarg_dicts or []
        if list_of_kwarg_dicts is not None:
            for kwarg_dict in list_of_kwarg_dicts:
                self.append_new_contact(**kwarg_dict)

    def _obj_to_json_dict(self):
        attrs = {}
        contacts_list = []
        for item in self:
            contacts_list.append(item._obj_to_json_dict())
        attrs["contact"] = contacts_list
        return self._remove_empty_values(attrs)


class Address(BaseMarshallingSubDomain):
    def __init__(self, city=None, country=None, primary=None, state=None,
                 street=None, zipcode=None):
        self.city = city
        self.country = country
        self.primary = primary
        self.state = state
        self.street = street
        self.zipcode = zipcode

    def _obj_to_xml_ele(self):
        element = ET.Element('address')
        e_attrs = {}
        e_attrs["city"] = self.city
        e_attrs["country"] = self.country
        e_attrs["primary"] = bool_to_string_xml(self.primary)
        e_attrs["state"] = self.state
        e_attrs["street"] = self.street
        e_attrs["zipcode"] = self.zipcode
        return self._set_xml_attrs(element, e_attrs)

    def _obj_to_json_dict(self):
        attrs = {}
        attrs["city"] = self.city
        attrs["country"] = self.country
        attrs["primary"] = self.primary
        attrs["state"] = self.state
        attrs["street"] = self.street
        attrs["zipcode"] = self.zipcode
        return self._remove_empty_values(attrs)


class Addresses(BaseMarshallingSubDomainList):
    ROOT_TAG = 'addresses'

    def append_new_address(self, city=None, country=None, primary=None,
                           state=None, street=None, zipcode=None):
        self.append(
            Address(
                city=city,
                country=country,
                primary=primary,
                state=state,
                street=street,
                zipcode=zipcode))

    def extend_new_addresses(self, list_of_kwarg_dicts):
        list_of_kwarg_dicts = list_of_kwarg_dicts or []
        if list_of_kwarg_dicts is not None:
            for kwarg_dict in list_of_kwarg_dicts:
                self.append_new_address(**kwarg_dict)

    def _obj_to_json_dict(self):
        attrs = {}
        ea_list = []
        for item in self:
            ea_list.append(item._obj_to_json_dict())
        attrs['address'] = ea_list
        return self._remove_empty_values(attrs)


class EmailAddress(BaseMarshallingSubDomain):
    def __init__(self, address=None, primary=None):
        self.address = address
        self.primary = primary

    def _obj_to_xml_ele(self):
        element = ET.Element('emailAddress')
        e_attrs = {}
        e_attrs["address"] = self.address
        e_attrs["primary"] = bool_to_string_xml(self.primary)
        return self._set_xml_attrs(element, e_attrs)

    def _obj_to_json_dict(self):
        attrs = {}
        attrs["address"] = self.address
        attrs["primary"] = self.primary
        return self._remove_empty_values(attrs)


class EmailAddresses(BaseMarshallingSubDomainList):
    ROOT_TAG = 'emailAddresses'

    def append_new_email_address(self, address=None, primary=None):
        self.append(EmailAddress(address=address, primary=primary))

    def extend_new_email_addresses(self, list_of_kwarg_dicts):
        list_of_kwarg_dicts = list_of_kwarg_dicts or []
        if list_of_kwarg_dicts is not None:
            for kwarg_dict in list_of_kwarg_dicts:
                self.append_new_email_address(**kwarg_dict)

    def _obj_to_json_dict(self):
        attrs = {}
        ea_list = []
        for item in self:
            ea_list.append(item._obj_to_json_dict())
        attrs['emailAddress'] = ea_list
        return self._remove_empty_values(attrs)


class PhoneNumber(BaseMarshallingSubDomain):
    def __init__(self, category=None, country=None, number=None, primary=None):
        self.category = category
        self.country = country
        self.number = number
        self.primary = primary

    def _obj_to_xml_ele(self):
        element = ET.Element('phoneNumber')
        e_attrs = {}
        e_attrs["category"] = self.category
        e_attrs["country"] = self.country
        e_attrs["number"] = self.number
        e_attrs["primary"] = bool_to_string_xml(self.primary)
        return self._set_xml_attrs(element, e_attrs)

    def _obj_to_json_dict(self):
        attrs = {}
        attrs["category"] = self.category
        attrs["country"] = self.country
        attrs["number"] = self.number
        attrs["primary"] = self.primary
        return self._remove_empty_values(attrs)


class PhoneNumbers(BaseMarshallingSubDomainList):
    ROOT_TAG = 'phoneNumbers'

    def append_new_phone_number(self, category=None, country=None, number=None,
                                primary=None):
        self.append(
            PhoneNumber(
                category=category,
                country=country,
                number=number,
                primary=primary))

    def extend_new_phone_numbers(self, list_of_kwarg_dicts):
        list_of_kwarg_dicts = list_of_kwarg_dicts or []
        if list_of_kwarg_dicts is not None:
            for kwarg_dict in list_of_kwarg_dicts:
                self.append_new_phone_number(**kwarg_dict)

    def _obj_to_json_dict(self):
        attrs = {}
        pn_list = []
        for item in self:
            pn_list.append(item._obj_to_json_dict())
        attrs['phoneNumber'] = pn_list
        return self._remove_empty_values(attrs)


class Role(BaseMarshallingSubDomain):
    def __init__(self, role=None):
        #note, role is a tag, so you have to do et.find('role').text=
        #<role value> to set it
        self.role = role

    def _obj_to_xml_ele(self):
        element = ET.Element('role')
        element.text = self.role
        return element


class Roles(BaseMarshallingSubDomainList):
    ROOT_TAG = 'roles'

    def append_new_role(self, role=None):
        self.append(Role(role=role))

    def extend_new_roles(self, list_of_kwarg_dicts):
        list_of_kwarg_dicts = list_of_kwarg_dicts or []
        for kwarg_dict in list_of_kwarg_dicts:
            self.append_new_role(**kwarg_dict)

    def _obj_to_json_dict(self):
        attrs = {}
        role_list = []
        for item in self:
            role_list.append(item.role)
        attrs['role'] = role_list
        return self._remove_empty_values(attrs)


class PaymentCard(BaseMarshallingSubDomain):
    def __init__(self, card_holder_name=None, card_number=None, card_type=None,
                 card_verification_number=None, expiration_date=None):
        self.card_holder_name = card_holder_name
        self.card_number = card_number
        self.card_type = card_type
        self.card_verification_number = card_verification_number
        self.expiration_date = expiration_date

    def _obj_to_xml_ele(self):
        element = ET.Element('paymentCard')
        e_attrs = {}
        e_attrs["cardHolderName"] = self.card_holder_name
        e_attrs["cardNumber"] = self.card_number
        e_attrs["cardType"] = self.card_type
        e_attrs["cardVerificationNumber"] = self.card_verification_number
        e_attrs["expirationDate"] = self.expiration_date
        return self._set_xml_attrs(element, e_attrs)

    def _obj_to_json_dict(self):
        attrs = {}
        attrs["cardHolderName"] = self.card_holder_name
        attrs["cardNumber"] = self.card_number
        attrs["cardType"] = self.card_type
        attrs["cardVerificationNumber"] = self.card_verification_number
        attrs["expirationDate"] = self.expiration_date
        return self._remove_empty_values(attrs)


class ConsolidatedInvoice(BaseMarshallingSubDomain):

    def __init__(self, managed_account_number=None):
        self.managed_account_number = managed_account_number

    def _obj_to_xml_ele(self):
        element = ET.Element('consolidatedInvoice')
        e_attrs = {}
        e_attrs["managedAccountNumber"] = self.managed_account_number
        return self._set_xml_attrs(element, e_attrs)

    def _obj_to_json_dict(self):
        attrs = {}
        attrs["managedAccountNumber"] = self.managed_account_number
        return self._remove_empty_values(attrs)


class PaymentMethod(BaseMarshallingSubDomainList):
    ROOT_TAG = 'paymentMethod'

    def append_new_payment_card(self, card_holder_name=None, card_number=None,
                                card_type=None, card_verification_number=None,
                                expiration_date=None):

        self.append(
            PaymentCard(
                card_holder_name=card_holder_name,
                card_number=card_number,
                card_type=card_type,
                card_verification_number=card_verification_number,
                expiration_date=expiration_date))

    def extend_new_payment_cards(self, list_of_kwarg_dicts):
        list_of_kwarg_dicts = list_of_kwarg_dicts or []
        if list_of_kwarg_dicts is not None:
            for kwarg_dict in list_of_kwarg_dicts:
                self.append_new_payment_card(**kwarg_dict)

    def append_new_consolidated_invoice(self, managed_account_number=None):

        self.append(
            ConsolidatedInvoice(managed_account_number=managed_account_number))

    def extend_new_consolidated_invoices(self, list_of_kwarg_dicts):
        list_of_kwarg_dicts = list_of_kwarg_dicts or []
        if list_of_kwarg_dicts is not None:
            for kwarg_dict in list_of_kwarg_dicts:
                self.append_new_consolidated_invoice(**kwarg_dict)

    def _obj_to_json_dict(self):
        #Must support multiple internal types
        attrs = {}

        for payment_method in self:
            pay_meth_type_name = type(payment_method).__name__.lower()
            if pay_meth_type_name == 'consolidatedinvoice':
                attrs['consolidatedInvoice'] =\
                    payment_method._obj_to_json_dict()
            if pay_meth_type_name == 'paymentcard':
                attrs['paymentCard'] = payment_method._obj_to_json_dict()

        return self._remove_empty_values(attrs)


class MetadataProperty(BaseMarshallingSubDomain):
    def __init__(self, key=None, value=None):
        self.key = key
        self.value = value

    def _obj_to_xml_ele(self):
        element = ET.Element('property')
        e_attrs = {}
        e_attrs["key"] = self.key
        e_attrs["value"] = self.value
        return self._set_xml_attrs(element, e_attrs)

    def _obj_to_json_dict(self):
        attrs = {}
        attrs['key'] = self.key
        attrs['value'] = self.value
        return self._remove_empty_values(attrs)


class Metadata(BaseMarshallingSubDomainList):
    ROOT_TAG = 'metadata'

    def append_new_property(self, key=None, value=None):
        self.append(MetadataProperty(key=key, value=value))

    def extend_new_properties(self, list_of_kwarg_dicts):
        list_of_kwarg_dicts = list_of_kwarg_dicts or []
        if list_of_kwarg_dicts is not None:
            for kwarg_dict in list_of_kwarg_dicts:
                self.append_new_property(**kwarg_dict)

    def _obj_to_json_dict(self):
        attrs = {}
        property_list = []
        for item in self:
            property_list.append(item._obj_to_json_dict())
        attrs['property'] = property_list
        return self._remove_empty_values(attrs)


class OrderItem(BaseMarshallingSubDomain):
    def __init__(self, offering_id=None, product_id=None, quantity=None):
        self.offering_id = offering_id
        self.product_id = product_id
        self.quantity = quantity

    def _obj_to_xml_ele(self):
        element = ET.Element('item')
        e_attrs = {}
        e_attrs["offeringId"] = self.offering_id
        e_attrs["productId"] = self.product_id
        e_attrs["quantity"] = self.quantity
        return self._set_xml_attrs(element, e_attrs)

    def _obj_to_json_dict(self):
        attrs = {}
        attrs["offeringId"] = self.offering_id
        attrs["productId"] = self.product_id
        attrs["quantity"] = int(self.quantity)
        return self._remove_empty_values(attrs)


class Order(BaseMarshallingSubDomainList):
    ROOT_TAG = 'order'

    def __init__(self, id_=None, order_items=None, metadata=None):
        self.id_ = id_

        self.extend_new_items(order_items)

        if metadata is not None:
            self.metadata = Metadata()
            self.metadata.extend_new_properties(metadata)

    def append_new_item(self, offering_id=None, product_id=None,
                        quantity=None):
        self.append(
            OrderItem(
                offering_id=offering_id,
                product_id=product_id,
                quantity=quantity))

    def extend_new_items(self, list_of_kwarg_dicts):
        list_of_kwarg_dicts = list_of_kwarg_dicts or []
        if list_of_kwarg_dicts is not None:
            for kwarg_dict in list_of_kwarg_dicts:
                self.append_new_item(**kwarg_dict)

    def _obj_to_xml_ele(self):
        element = ET.Element(self.ROOT_TAG)
        e_attrs = {}
        e_attrs["id"] = self.id_
        try:
            element.append(self.metadata._obj_to_xml_ele())
        except:
            pass
        element = self._set_xml_attrs(element, e_attrs)
        for item in self:
            element.append(item._obj_to_xml_ele())
        return element

    def _obj_to_json_dict(self):
        attrs = {}
        item_list = []

        try:
            attrs['metadata'] = self.metadata._obj_to_json_dict()
        except:
            pass
        for item in self:
            item_list.append(item._obj_to_json_dict())
        attrs['item'] = item_list
        return self._remove_empty_values(attrs)


class SecretQA(BaseMarshallingSubDomain):
    def __init__(self, answer=None, question=None):
        self.answer = answer
        self.question = question

    def _obj_to_xml_ele(self):
        element = ET.Element('secretQA')
        e_attrs = {}
        e_attrs["answer"] = self.answer
        e_attrs["question"] = self.question
        return self._set_xml_attrs(element, e_attrs)

    def _obj_to_json_dict(self):
        attrs = {}
        attrs["answer"] = self.answer
        attrs["question"] = self.question
        return self._remove_empty_values(attrs)


class User(BaseMarshallingSubDomain):
    def __init__(self, password=None, username=None, secret_qa=None):
        self.password = password
        self.username = username
        self.secret_qa = SecretQA(**(secret_qa or {}))

    def _obj_to_xml_ele(self):
        element = ET.Element('user')
        e_attrs = {}
        e_attrs["password"] = self.password
        e_attrs["username"] = self.username
        element = self._set_xml_attrs(element, e_attrs)
        element.append(self.secret_qa._obj_to_xml_ele())
        return element

    def _obj_to_json_dict(self):
        attrs = {}
        attrs['password'] = self.password
        attrs['username'] = self.username
        attrs['secretQA'] = self.secret_qa._obj_to_json_dict()
        return self._remove_empty_values(attrs)


class AffiliateCodeandType(BaseMarshallingSubDomain):
    def __init__(self, code=None, type_=None):
            self.code = code
            self.type_ = type_

    def _obj_to_xml_ele(self):
        element = ET.Element('affiliateCodeandType')
        e_attrs = {}
        e_attrs["code"] = self.code
        e_attrs["type"] = self.type_
        return self._set_xml_attrs(element, e_attrs)

    def _obj_to_json_dict(self):
        attrs = {}
        attrs['code'] = self.code
        attrs['type'] = self.type_
        return self._remove_empty_values(attrs)

    def _obj_to_json(self):
        return json.dumps(self._obj_to_json_dict())


class Description(BaseMarshallingSubDomain):
    def __init__(self, description=None):
        self.description = description

    def _obj_to_xml_ele(self):
        element = ET.Element('description')
        element.text = self.description
        return element

    def _obj_to_json_dict(self):
        attrs = {}
        attrs['description'] = self.description
        return self._remove_empty_values(attrs)

    def _obj_to_json(self):
        return json.dumps(self._obj_to_json_dict())


class EmailAndAppsSignupRequest(SignupRequest):
    pass


class CloudSignupRequest(SignupRequest):
    '''
    Technically, I should override orderitems so that I don't send an id or
    order metadata by default.  For now, the fixture is taking care of that
    by sending None as the value for those fields by default for this type
    of request.
    '''
    pass


class TrustedCloudSignupRequest(SignupRequest):
    pass

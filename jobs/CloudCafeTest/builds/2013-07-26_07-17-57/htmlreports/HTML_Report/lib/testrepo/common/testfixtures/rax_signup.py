from testrepo.common.testfixtures.fixtures import BaseTestFixture
from ccengine.providers.rax_signup.rax_signup_api import RaxSignupProvider
import random
import string
import time
import re
#from ccengine.domain.rax_signup.request import signup_request


class RaxSignupAPI_BaseFixture(BaseTestFixture):
    @classmethod
    def setUpClass(cls):
        super(RaxSignupAPI_BaseFixture, cls).setUpClass()
        cls.provider = RaxSignupProvider(cls.config)
        cls.client = cls.provider.get_default_client()

    @staticmethod
    def gen_random_domain_name():
        #all lower case alpha, 0-9
        #max length of 64 chars
        valid_chars = [s for s in string.ascii_lowercase]
        valid_chars.extend([d for d in string.digits])
        final_word = []
        length = random.randrange(10, 50)

        for x in range(length):
            value = random.sample(valid_chars, 1)
            final_word.append(value[0])
        word = "".join(final_word)
        postfix = random.sample(['com', 'net', 'org'], 1)[0]
        return "{0}.raxqetest.{1}".format(word, postfix)

    @staticmethod
    def gen_random_us_domain_name():
        #all lower case alpha, 0-9
        #max length of 64 chars
        valid_chars = [s for s in string.ascii_lowercase]
        valid_chars.extend([d for d in string.digits])
        final_word = []
        length = random.randrange(10, 50)

        for x in range(length):
            value = random.sample(valid_chars, 1)
            final_word.append(value[0])
        word = "".join(final_word)
        postfix = 'us'
        return "{0}.raxqetest.{1}".format(word, postfix)

    @staticmethod
    def gen_random_username():
        #all lower case alpha, 0-9
        #3-15 char
        valid_chars = [s for s in string.ascii_lowercase]
        name = "".join(random.sample((valid_chars), 4))
        now = time.time()
        unique_random_number = int(now % 100000)
        return "{0}{1}".format(name, unique_random_number)

    @staticmethod
    def gen_random_password():
        #all lower case alpha, all upper case alpha, 0-9
        #8-19 characters
        lower_alpha = random.sample([s for s in string.ascii_lowercase],
                                    random.randrange(3, 6))
        upper_alpha = random.sample([s for s in string.ascii_uppercase],
                                    random.randrange(3, 6))
        numerical = random.sample([d for d in string.digits],
                                  random.randrange(3, 6))
        final_list = []
        final_list.extend(lower_alpha)
        final_list.extend(upper_alpha)
        final_list.extend(numerical)
        final_password = "".join(final_list)
        return final_password

    @staticmethod
    def _set_dict_override(kwargs, section_dict, section_name):
        kwargs_section = kwargs.get(section_name)
        if kwargs_section == {}:
            return {}
        keys = section_dict.keys()

        if kwargs_section is None:
            return section_dict

        try:
            keys.extend(kwargs_section.keys())
        except:
            pass

        for key in keys:
            try:
                section_dict[key] = kwargs_section[key]
            except:
                pass

        return section_dict

    @staticmethod
    def _set_list_override(kwargs, section_list, section_name):
        try:
            return kwargs[section_name]
        except:
            return section_list

    @classmethod
    def get_signup_request_dict(cls, **kwargs):
        '''
        The dictionaries and lists can be overriden entierely via key word
        arguments by sending in replacement objects of the same name and type
        in kwargs.
        (Example:  If you want 'contacts' to be completely empty, send
        contacts=[] via kwargs to this method)

        Individual attributes of these objects can be overriden by passing in
        objects via kwargs with only those attributes overriden.
        (example:  If you want 'account_name' in signup_request to be 'bob',
        send signup_request = {'account_name' = 'bob'} to this method.

        For objects that are themselves attributes of another object, you
        can override them either directly (contacts=[]) or via their
        super-object (signup_request={contacts=[]})

        signup_request (dictionary)
            accept_terms_and_conditions (bool)
            account_name (string)
            business_type (string)
            promo_code (string)
            region (string)
            service_level (string)
            terms_and_conditions (string)
            type_ (string)
            vat_code (string)
            skip_fraud_check (bool)
            description (string)
            contacts <SEE contacts (list)>
            payment_method <SEE payment_method (dictionary)>
            metadata <SEE metadata (list)>
            order <SEE order (dictionary)>
            affiliate_code_and_type <SEE affiliate_code_and_type (dictionary)>
            geo_location (string)

        contacts (list)
            This is a list of dictionaries.
            By default for testing, contacts includes a single dictionary
            called default_contact <SEE default_contact (dictionary)>

        default_contact (dictionary)
            first_name (string)
            last_name (string)
            suffix (string)
            title (string)
            addresses <SEE addresses (list)>
            email_addresses <SEE email_addresses (list)>
            phone_numbers <SEE phone_numbers (list)>
            roles <SEE roles (list of dictionaries)>
            user <SEE user (dictionary)>

        addresses (list)
            This is a list of dictionaries.
            By default for testing, addresses includes a single dictionary
            called default_address <SEE default_address (dictionary)>

        default_address (dictionary)
            city (string)
            country (string)
            primary (bool)
            state (string)
            street (string)
            zipcode (string)

        email_addresses (list)
            This is a list of dictionaries.
            By default for testing, email_addresses includes a single
            dictionary called default_email_address
            <SEE default_email_address (dictionary)>

        default_email_address (dictionary)
            address (string)
            primary (bool)

        phone_numbers (list)
            This is a list of dictionaries.
            By default for testing, phone_numbers includes a single dictionary
            called default_phone_number <SEE default_phone_number (dictionary)>

        default_phone_number (dictionary)
            category (string)
            country (string)
            number (string)
            primary (bool)

        roles(list of dictionaries)
            Note, this is a really simple construct, so I didn't feel it was
            necessary to include a "default_role" like with the other lists
            that hold dictionaries
            {"role": (string)}

        user (dictionary)
            password (string)
            username (string)
            secret_qa <SEE secret_qa (dictionary)>

        secret_qa (dictionary)
            question (string)
            answer (string)

        payment_method (dictionary) (only has payment card defined by default)
            payment_card <SEE default_payment_card (dictionary)>
            consolidated_invoice <SEE default_consolidated_invoice (dictionary)

        default_payment_card (dictionary)
            card_holder_name (string)
            card_number (string)
            card_type (string)
            card_verification_number (string)
            expiration_date (string)

        default_consolidated_invoice (dictionary)
            managed_account_number (string)

        metadata (list)
            This is a list of dictionaries.
            By default for testing, metadata includes a single dictionary
            called default_metadata <SEE default_metadata (dictionary)>

        default_metadata (dictionary)
            key (string)
            value (string)

        order (dictionary)
            id_ (string)
            order_items <SEE order_items (list)>
            metadata <SEE order_metadata (list)>

        order_items (list)
            This is a list of dictionaries.
            By default for testing, order_items includes a single dictionary
            called default_order_item <SEE default_order_item (dictionary)>

        default_order_item (dictionary)
            offering_id (string)
            product_id (string)
            quantity (string)

        order_metadata (list)
            This is a list of dictionaries.
            By default for testing, order_metadata includes a single dictionary
            called default_order_metadata
            <SEE default_order_metadata (dictionary)>

        default_order_metadata (dictionary)
            key (string)
            value (string)

        affiliate_code_and_type (dictionary)
            code (string)
            type_ (string)
        '''

        #Lambda to decrease function call length and complexity
        override_dict = lambda section_dict, section_name:\
            cls._set_dict_override(kwargs, section_dict, section_name)

        #Lambda to decrease function call length and complexity
        override_list = lambda section_list, section_name:\
            cls._set_list_override(kwargs, section_list, section_name)

        #Overide affiliate_code_and_type
        affiliate_code_and_type = {
            'code': 'My Affiliate',
            'type_': 'BRC'}
        affiliate_code_and_type = override_dict(affiliate_code_and_type,
                                                'affiliate_code_and_type')

        #Overide default_order_item, order_items, and order
        default_order_item = {
            'offering_id': 'FAKE_ID',
            'product_id': 'FAKE_ID',
            'quantity': '1'}
        order_items = [override_dict(default_order_item, 'default_order_item')]
        order_items = override_list(order_items, 'order_items')

        default_order_metadata = {
            "key": "SomeRandomMetadata",
            "value": "false"}
        order_metadata = [override_dict(default_order_metadata,
                                        'default_order_metadata')]
        order_metadata = override_list(order_metadata, 'order_metadata')

        order = {'id_': '12345',
                 'order_items': order_items,
                 'metadata': order_metadata}
        order = override_dict(order, 'order')

        #Overide default_metadata and metadata
        default_metadata = {
            "key": "SomeRandomMetadata",
            "value": "false"}
        metadata = [override_dict(default_metadata, 'default_metadata')]
        metadata = override_list(metadata, 'metadata')

        default_payment_card = {
            'card_holder_name': 'Homer Simpson',
            'card_number': '378282246310005',
            'card_type': 'AMEX',
            'card_verification_number': '1234',
            'expiration_date': '01/2014'}
        default_payment_card = override_dict(default_payment_card,
                                             'default_payment_card')

        payment_method = {'payment_card': default_payment_card}
        payment_method = override_dict(payment_method, 'payment_method')

        secret_qa = {
            'question': 'Who was your childhood hero?',
            'answer': 'Phil'}
        secret_qa = override_dict(secret_qa, 'secret_qa')

        user = {
            'password': cls.gen_random_password(),
            'username': cls.gen_random_username(),
            'secret_qa': secret_qa}
        user = override_dict(user, 'user')

        roles = [
            {'role': 'BILLING'},
            {'role': 'PRIMARY'}, ]
        roles = override_list(roles, 'roles')

        default_phone_number = {
            'category': 'HOME',
            'country': 'US',
            'number': '5555555555',
            'primary': True}
        phone_numbers = [override_dict(default_phone_number,
                                       'default_phone_number')]
        phone_numbers = override_list(phone_numbers, 'phone_numbers')

        default_email_address = {
            #This is a secure rax test /dev/null email
            'address': 'testbox@mailtrust.com',
            'primary': True}
        email_addresses = [override_dict(default_email_address,
                                         'default_email_address')]
        email_addresses = override_list(email_addresses, 'email_addresses')

        default_address = {
            'city': 'San Antonio',
            'country': 'US',
            'primary': True,
            'state': 'TX',
            'street': '5000 Walzem Road',
            'zipcode': '78218'}
        addresses = [override_dict(default_address, 'default_address')]
        addresses = override_list(addresses, 'addresses')

        default_contact = {
            'first_name': 'Homer',
            'last_name': 'Simpson',
            'suffix': 'Senior',
            'title': 'Mr',
            'addresses': addresses,
            'email_addresses': email_addresses,
            'phone_numbers': phone_numbers,
            'roles': roles,
            'user': user}
        contacts = [override_dict(default_contact, 'default_contact')]
        contacts = override_list(contacts, 'contacts')

        signup_request = {
            'accept_terms_and_conditions': True,
            'account_name': 'Rackspace',
            'promo_code': '80085',
            'region': 'US',
            'service_level': 'MANAGED',
            'type_': 'CLOUD',
            'vat_code': 'GB0177282',
            'skip_fraud_check': False,
            'description': 'THIS IS A FAKE DESCRIPTION',
            'contacts': contacts,
            'payment_method': payment_method,
            'metadata': metadata,
            'order': order,
            'affiliate_code_and_type': affiliate_code_and_type,
            'geo_location': None}
        signup_request = override_dict(signup_request, 'signup_request')

        return signup_request

    def assertDefaultResponseOK(self, api_response, expected_status_code=201):
        self.assertTrue(api_response.ok,
                        "API signup request failed with {0}".format(
                        api_response.status_code))

        self.assertEqual(
            expected_status_code, api_response.status_code,
            "API signup request expected a return staus code of {0} but "
            "recieved a {1}".format(expected_status_code,
                                    api_response.status_code))

        self.assertTrue(hasattr(api_response, 'entity'),
                        'Response could not be deserialized')

        self.assertIsNotNone(api_response.entity.id_,
                             'Response did not send back an id')

    def validate_contract_entity(self, signup_id=None, country_code='US',
                                 cloud_type='US', business_type='CONSUMER',
                                 contract_entity=None):
        '''
        Method to check the value of contract entity
        '''
        # Condition to decide the contract entity
        apac_countries = ['BD', 'KH', 'CN', 'HK', 'IN', 'ID', 'JP', 'KP', 'KR',
                          'MO', 'MY', 'MN', 'MM', 'PK', 'PH', 'SG', 'LK', 'TW',
                          'TJ', 'TH', 'VN', 'BT', 'BN', 'KZ', 'KG', 'LA', 'MV',
                          'NP', 'TM', 'UZ']
        ch_countries = [apac_countries, 'AU', 'NZ']

        if (contract_entity is None):
            if (cloud_type == 'UK' or ((country_code in ch_countries) and
                                       (business_type == 'BUSINESS'))):
                contract_entity = 'CONTRACT_CH'
            else:
                contract_entity = 'CONTRACT_US'

        if (cloud_type == 'UK' and business_type is None):
            business_type = 'BUSINESS'

        signup_id = {'id': signup_id}

        # Get steps
        api_response1 = "{0}".format((self.client.signup_steps(signup_id))
                                     .content)

        # Checking the request and response to BSL
        bsl_req = re.search('CONTRACT_ENTITY COMPLETE(.+)CONTRACT_ENTITY',
                            api_response1).group(1)
        bsl_parameters = 'cloudType=\[{0}\], countryCode=\[{1}\], businessType=\[{2}\]'.format(cloud_type, country_code, business_type)
        contract_entity_returned = 'code.+?{0}'.format(contract_entity)
        self.assertIsNotNone(re.search(bsl_parameters, bsl_req),
                             "contract entity request not as expected")
        self.assertIsNotNone(re.search(contract_entity_returned, bsl_req),
                             "contract entity response not as expected")

        # Checking the value of contract_entity sent to PSL
        if (cloud_type == 'US'):
            psl_regex = 'PAYMENT_CARD_VALIDATION COMPLETE(.+)PAYMENT_CARD_VALIDATION'
            psl_req = re.search(psl_regex, api_response1).group(1)
            self.assertIsNotNone(re.search(contract_entity, psl_req),
                                 "contract entity sent to psl not as expected")

    def validate_user_identity(self, api_response=None, username=None):
        '''
        Helper Method to check the User Identity call
        '''
        # To get the signupId
        response_headers = "{0}".format(api_response.headers)
        signup_id = re.search('v1/signups/(.+?)\',', response_headers).group(1)

        # To check the steps for UserIdentity call
        signup_id = {'id': signup_id}
        steps_response = "{0}".format((self.client.signup_steps(signup_id))
                              .content)
        identity_regex = 'CLOUD_GEO_LOCATION COMPLETE'
        self.assertIsNotNone(re.search(identity_regex, steps_response),
                             "Identity Call not done")

        # To check identity whether SYD is set as default Region
        #  Get user by username identity call
        get_user_identity = self.client.get_user_identity(
            username=username).content
        default_region = '\"RAX-AUTH:defaultRegion\":\"SYD\"'
        self.assertIsNotNone(re.search(default_region, get_user_identity),
                             "Identity Call not done")

    def assertBadRequestCodeAndMessage(method, account_type, request,
                                       response_message, response_code=400):
        """
        To Assert the Response Code and Response Message from the API Response
        Body
        """
        if (account_type == 'TRUSTED_CLOUD'):
            api_response = method.client.signup_new_trusted_cloud_customer(
                **request)
        else:
            api_response = method.client.signup_new_cloud_customer(**request)

        method.assertEqual(api_response.status_code, response_code,
                           'Returned a {0} but expected {1}'
                           .format(api_response.status_code,
                           response_code))

        method.assertIsNotNone(re.search(response_message,
                               api_response.content), method.assert_msg.format(
                               response_message))
        return api_response

    #Implementation of Signup POST calls
    def signup_post_calls(method, request_dict, account_type):
        """
        To make Signups based on Account Types
        """
        if (account_type == "CLOUD"):
            api_response = method.client.signup_new_cloud_customer(
                **request_dict)

        elif (account_type == "TRUSTED_CLOUD"):
            api_response = method.client.signup_new_trusted_cloud_customer(
                **request_dict)

        else:
            api_response = method.client.signup_new_email_and_apps_customer(
                **request_dict)

        method.assertDefaultResponseOK(api_response)

        return api_response

    def get_reference_entity_id(method, api_response):
        """
        To process the API Response to retrieve Reference Entity ID
        """
        reference_entity_id = api_response.entity.id_

        return reference_entity_id

    def get_marker(method, api_response):
        """
        To process the API Response to retrieve Marker
        """
        header_location = api_response.headers["location"]
        marker = re.search("signups/(\d+)", header_location).group(1)

        return marker


class Business_Type(object):
    '''
    To define the values for the attribute business_type
    '''
    BUSINESS = "BUSINESS"
    CONSUMER = "CONSUMER"


class Account_Type(object):
    '''
    To define the values for the attribute type(account_type)
    '''
    Cloud = "CLOUD"
    Trusted_Cloud = "TRUSTED_CLOUD"
    Email_Apps = "EMAIL_APPS"


class CreditCards(object):
        '''
        The below list of Credit Cards can be used to override default
        card_type and card_number in the default_payment_card of
        signup_request
        '''
        VISA_CARD = "VISA"
        AMERICANEXPRESS_CARD = "AMEX"
        MASTER_CARD = "MASTERCARD"
        DISCOVER_CARD = "DISCOVER"
        VISA_CARD_NUMBER = "4012888888881881"
        AMERICANEXPRESS_CARD_NUMBER = "378282246310005"
        MASTER_CARD_NUMBER = "5111005111051128"
        DISCOVER_CARD_NUMBER = "6559906559906557"


class RaxSignupAPI_EmailAndAppsSignupFixture(RaxSignupAPI_BaseFixture):
    @classmethod
    def get_signup_request_dict(cls, **kwargs):

        #Lambda to decrease function call length and complexity
        override_dict = lambda section_dict, section_name:\
            cls._set_dict_override(kwargs, section_dict, section_name)

        #Lambda to decrease function call length and complexity
        override_list = lambda section_list, section_name:\
            cls._set_list_override(kwargs, section_list, section_name)

        signup_request = {
            'type_': 'EMAIL_APPS',
            'account_name': 'Rackspace'}
        kwargs['signup_request'] = override_dict(signup_request,
                                                 'signup_request')

        order_metadata = [
            {"key": "domainName",
             "value": cls.gen_random_domain_name()},
            {"key": "domainRegistrationPrice",
             "value": '10'},
            {"key": "domainYears",
             "value": '1'},
            {"key": "dnsType",
             "value": "new"},
            {"key": "nexus",
             "value": "Business Entity"},
            {"key": "purpose",
             "value": "For Profit"},
            {"key": "us_country",
             "value": "US"}]
        kwargs['order_metadata'] = override_list(order_metadata,
                                                 'order_metadata')
        #print kwargs['order_metadata']

        order_items = [
            {"offering_id": "RACKSPACE_EMAIL",
             "quantity": 25,
             "product_id": "RACKSPACE_MAILBOX"}]
        kwargs['order_items'] = override_list(order_items, 'order_items')

        return super(RaxSignupAPI_EmailAndAppsSignupFixture, cls).\
            get_signup_request_dict(**kwargs)


class RaxSignupAPI_CloudSignupFixture(RaxSignupAPI_BaseFixture):

    @classmethod
    def get_signup_request_dict(cls, **kwargs):

        #Lambda to decrease function call length and complexity
        override_dict = lambda section_dict, section_name:\
            cls._set_dict_override(kwargs, section_dict, section_name)

        #Lambda to decrease function call length and complexity
        override_list = lambda section_list, section_name:\
            cls._set_list_override(kwargs, section_list, section_name)

        #Overide default_order_item, order_items, and order
        default_order_item = {
            'offering_id': 'FAKE_ID',
            'product_id': 'FAKE_ID',
            'quantity': '1'}
        order_items = [override_dict(default_order_item, 'default_order_item')]
        order_items = override_list(order_items, 'order_items')

        order = {'id_': None,
                 'order_items': order_items,
                 'metadata': None}
        kwargs['order'] = override_dict(order, 'order')

        return super(RaxSignupAPI_CloudSignupFixture, cls).\
            get_signup_request_dict(**kwargs)


class RaxSignupAPI_CloudSignupFixture_UK(RaxSignupAPI_CloudSignupFixture):

    @classmethod
    def get_signup_request_dict(cls, **kwargs):
        #Lambda to decrease function call length and complexity
        override_dict = lambda section_dict, section_name:\
            cls._set_dict_override(kwargs, section_dict, section_name)

        default_phone_number = {
            'category': 'HOME',
            'country': 'GB',
            'number': '5555555555',
            'primary': True}

        kwargs['default_phone_number'] = override_dict(default_phone_number,
                                                       'default_phone_number')

        signup_request = {'region': 'UK'}

        kwargs['signup_request'] = override_dict(signup_request,
                                                 'signup_request')

        default_address = {
            'city': 'London',
            'country': 'GB',
            'primary': True,
            'state': 'England',
            'street': '5000 Walzem Road',
            'zipcode': 'W37RP'}

        kwargs['default_address'] = override_dict(default_address,
                                                  'default_address')

        default_payment_card = {
            'card_holder_name': 'Clay John',
            'card_number': '4012888888881881',
            'card_type': 'VISA',
            'card_verification_number': '555',
            'expiration_date': '02/2020'}

        kwargs['default_payment_card'] = override_dict(default_payment_card,
                                                       'default_payment_card')

        return super(RaxSignupAPI_CloudSignupFixture_UK, cls).\
            get_signup_request_dict(**kwargs)


class RaxSignupAPI_TrustedCloudSignupFixture(RaxSignupAPI_BaseFixture):

    @classmethod
    def get_signup_request_dict(cls, **kwargs):

        #Lambda to decrease function call length and complexity
        override_dict = lambda section_dict, section_name:\
            cls._set_dict_override(kwargs, section_dict, section_name)

        #Lambda to decrease function call length and complexity
        override_list = lambda section_list, section_name:\
            cls._set_list_override(kwargs, section_list, section_name)

        #Overide default_order_item, order_items, and order
        default_order_item = {
            'offering_id': 'FAKE_ID',
            'product_id': 'FAKE_ID',
            'quantity': '1'}

        kwargs['default_order_item'] = override_dict(default_order_item,
                                                     'default_order_item')

        order = {'id_': None,
                 'metadata': None}
        kwargs['order'] = override_dict(order, 'order')

        default_consolidated_invoice = {'managed_account_number': '91282392'}
        kwargs['default_consolidated_invoice'] = override_dict(
            default_consolidated_invoice, 'default_consolidated_invoice')

        payment_method = {'consolidated_invoice': default_consolidated_invoice}
        kwargs['payment_method'] = override_dict(payment_method,
                                                 'payment_method')

        signup_request = {
            'referral_code': "987",
            'region': 'US',
            'service_level': 'MANAGED',
            'type_': 'TRUSTED_CLOUD',
            'skip_fraud_check': True,
            'managed_account_number': '91282392'}
        kwargs['signup_request'] = override_dict(signup_request,
                                                 'signup_request')

        return super(RaxSignupAPI_TrustedCloudSignupFixture, cls).\
            get_signup_request_dict(**kwargs)


class RaxSignupAPI_TrustedCloudSignupFixture_UK(
        RaxSignupAPI_TrustedCloudSignupFixture):

    @classmethod
    def get_signup_request_dict(cls, **kwargs):

        #Lambda to decrease function call length and complexity
        override_dict = lambda section_dict, section_name:\
            cls._set_dict_override(kwargs, section_dict, section_name)

        #Lambda to decrease function call length and complexity
        override_list = lambda section_list, section_name:\
            cls._set_list_override(kwargs, section_list, section_name)

        default_phone_number = {
            'category': 'HOME',
            'country': 'GB',
            'number': '5555555555',
            'primary': True}

        kwargs['default_phone_number'] = override_dict(default_phone_number,
                                                       'default_phone_number')

        signup_request = {
            'region': 'UK',
            'referral_code': '987',
            'vat_code': 'GB0177282',
            'service_level': 'MANAGED',
            'type_': 'TRUSTED_CLOUD',
            'skip_fraud_check': True,
            'managed_account_number': '91282392'}

        kwargs['signup_request'] = override_dict(signup_request,
                                                 'signup_request')

        default_address = {
            'city': 'London',
            'country': 'GB',
            'primary': True,
            'state': 'England',
            'street': '5000 Walzem Road',
            'zipcode': 'W37RP'}

        kwargs['default_address'] = override_dict(default_address,
                                                  'default_address')

        default_payment_card = {
            'card_holder_name': 'Clay John',
            'card_number': '4012888888881881',
            'card_type': 'VISA',
            'card_verification_number': '555',
            'expiration_date': '02/2020'}
        kwargs['default_payment_card'] = override_dict(default_payment_card,
                                                       'default_payment_card')

        return super(RaxSignupAPI_TrustedCloudSignupFixture, cls).\
            get_signup_request_dict(**kwargs)

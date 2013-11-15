from ccengine.providers.base_provider import BaseProvider
from ccengine.providers.identity.identity_v2_0_api import IdentityAPIProvider
from ccengine.clients.rax_signup.rax_signup_api import RaxSignupAPIClient
import random
import string
import time


class RaxSignupProvider(BaseProvider):
    '''
    Provides constructors for different client configurations.
    '''

    def __init__(self, config):
        super(RaxSignupProvider, self).__init__()
        self.config = config
        self.identity_provider = IdentityAPIProvider(self.config)
        self.client = self.get_default_client()

    def get_default_client(
            self, base_url=None, auth_token=None, serialize_format=None,
            deserialize_format=None, ah_endpoint=None, identity_endpoint=None):

        auth_token = self.get_token()

        if deserialize_format is None:
            deserialize_format = self.config.misc.deserializer

        return RaxSignupAPIClient(
            base_url=self.config.rax_signup.base_url,
            auth_token=auth_token,
            serialize_format=self.config.misc.serializer,
            deserialize_format=deserialize_format,
            ah_endpoint=self.config.atom_hopper_events.ah_endpoint,
            identity_endpoint=self.config.user_identity.identity_endpoint)

    def get_token(self):
        par = self.identity_provider.authenticate()
        auth_token = par.response.entity.token.id
        assert auth_token is not None, "Could not locate an auth token"
        return auth_token

    @staticmethod
    def gen_random_domain_name(postfix=None):
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
        postfix = postfix or random.sample(['com', 'net', 'org', 'us'], 1)[0]
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

    def generate_default_signup_request_dictionary(self, **kwargs):
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

        def _set_list_override(kwargs, section_list, section_name):
            try:
                return kwargs[section_name]
            except:
                return section_list

        #Lambda to decrease function call length and complexity
        override_dict = lambda section_dict, section_name:\
            _set_dict_override(kwargs, section_dict, section_name)

        #Lambda to decrease function call length and complexity
        override_list = lambda section_list, section_name:\
            _set_list_override(kwargs, section_list, section_name)

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
            'password': self.gen_random_password(),
            'username': self.gen_random_username(),
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

    def create_new_cloud_account(self, **kwargs):
        request = self.generate_default_signup_request_dictionary()
        resp = self.client.signup_new_cloud_customer(**request)
        assert resp.ok, 'Unable to signup new coud customer'
        assert resp.entity is not None, (
            'Unable to deserialize create account response')

        return resp



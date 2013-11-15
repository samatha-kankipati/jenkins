#from ccengine.common.connectors import rest
from ccengine.domain.rax_signup.request.signup_request import \
    CloudSignupRequest, EmailAndAppsSignupRequest,\
    TrustedCloudSignupRequest
from ccengine.domain.rax_signup.response.signup_response import \
    ReferenceEntity, ListSignupResponse
from ccengine.clients.base_client import BaseMarshallingClient
from testrepo.common.testfixtures.fixtures import BaseTestFixture


class RaxSignupAPIClient(BaseMarshallingClient):
    def __init__(self, base_url, auth_token, ah_endpoint, identity_endpoint,
                 serialize_format=None, deserialize_format=None):
        super(RaxSignupAPIClient, self).__init__(serialize_format,
                                                 deserialize_format)

        self.base_url = base_url
        self.auth_token = auth_token
        self.ah_endpoint = ah_endpoint
        self.identity_endpoint = identity_endpoint
        self.default_headers['X-Auth-Token'] = auth_token
        self.default_headers['Content-Type'] = 'application/{0}'.format(
            serialize_format)
        self.default_headers['Accept'] = 'application/{0}'.format(
            deserialize_format)

    def signup_new_cloud_customer(
            self, accept_terms_and_conditions=None, referral_code=None,
            account_name=None, business_type=None, promo_code=None,
            region=None, service_level=None, terms_and_conditions=None,
            type_=None, vat_code=None, xmlns=None, xmlns_atom=None,
            contacts=None, payment_method=None, description=None,
            metadata=None, order=None, affiliate_code_and_type=None,
            skip_fraud_check=None, managed_account_number=None,
            geo_location=None, data=None, requestslib_kwargs=None):
        '''
        POST
        /v1/signups
        '''

        url = '{0}/v1/signups'.format(self.base_url)

        signup_request_entity = None
        if data is None:
            signup_request_entity = CloudSignupRequest(
                referral_code=referral_code,
                accept_terms_and_conditions=accept_terms_and_conditions,
                account_name=account_name, business_type=business_type,
                promo_code=promo_code, region=region,
                service_level=service_level,
                terms_and_conditions=terms_and_conditions, type_=type_,
                vat_code=vat_code, xmlns=xmlns, xmlns_atom=xmlns_atom,
                contacts=contacts, payment_method=payment_method,
                description=description, metadata=metadata, order=order,
                affiliate_code_and_type=affiliate_code_and_type,
                skip_fraud_check=skip_fraud_check,
                managed_account_number=managed_account_number,
                geo_location=geo_location)

        return self.request('POST', url,
                            response_entity_type=ReferenceEntity,
                            request_entity=signup_request_entity,
                            data=data,
                            requestslib_kwargs=requestslib_kwargs)

    def signup_new_trusted_cloud_customer(
            self, accept_terms_and_conditions=None, referral_code=None,
            account_name=None, business_type=None, promo_code=None,
            region=None, service_level=None, terms_and_conditions=None,
            type_=None, vat_code=None, xmlns=None, xmlns_atom=None,
            contacts=None, payment_method=None, description=None,
            metadata=None, order=None, affiliate_code_and_type=None,
            skip_fraud_check=None, managed_account_number=None,
            geo_location=None, data=None, requestslib_kwargs=None):
        '''
        POST
        /v1/signups
        '''

        url = '{0}/v1/signups'.format(self.base_url)

        signup_request_entity = None
        if data is None:
            signup_request_entity = TrustedCloudSignupRequest(
                referral_code=referral_code,
                accept_terms_and_conditions=accept_terms_and_conditions,
                account_name=account_name, business_type=business_type,
                promo_code=promo_code, region=region,
                service_level=service_level,
                terms_and_conditions=terms_and_conditions, type_=type_,
                vat_code=vat_code, xmlns=xmlns, xmlns_atom=xmlns_atom,
                contacts=contacts, payment_method=payment_method,
                description=description, metadata=metadata, order=order,
                affiliate_code_and_type=affiliate_code_and_type,
                skip_fraud_check=skip_fraud_check,
                managed_account_number=managed_account_number,
                geo_location=geo_location)

        return self.request('POST', url,
                            response_entity_type=ReferenceEntity,
                            request_entity=signup_request_entity,
                            data=data,
                            requestslib_kwargs=requestslib_kwargs)

    def signup_new_email_and_apps_customer(
            self, accept_terms_and_conditions=None, account_name=None,
            business_type=None, promo_code=None, region=None,
            service_level=None, terms_and_conditions=None, type_=None,
            vat_code=None, xmlns=None, xmlns_atom=None, contacts=None,
            payment_method=None, description=None, metadata=None,
            order=None, affiliate_code_and_type=None, referral_code=None,
            skip_fraud_check=None, geo_location=None, data=None,
            requestslib_kwargs=None):
            '''
            POST
            /v1/signups
            '''

            url = '{0}/v1/signups'.format(self.base_url)

            signup_request_entity = None
            if data is None:
                signup_request_entity = EmailAndAppsSignupRequest(
                    accept_terms_and_conditions=accept_terms_and_conditions,
                    account_name=account_name, business_type=business_type,
                    promo_code=promo_code, region=region,
                    service_level=service_level,
                    terms_and_conditions=terms_and_conditions, type_=type_,
                    vat_code=vat_code, xmlns=xmlns, xmlns_atom=xmlns_atom,
                    contacts=contacts, payment_method=payment_method,
                    description=description, metadata=metadata, order=order,
                    affiliate_code_and_type=affiliate_code_and_type,
                    skip_fraud_check=skip_fraud_check,
                    referral_code=referral_code, geo_location=geo_location)

            return self.request('POST', url,
                                response_entity_type=ReferenceEntity,
                                request_entity=signup_request_entity,
                                data=data,
                                requestslib_kwargs=requestslib_kwargs)

    def list_signups(self, status=None, region=None, type_=None,
                     reference_entity_id=None, after_datetime=None,
                     marker=None, limit=None, params=None,
                     requestslib_kwargs=None):
        '''
        GET
        /v1/signups/?{params}
        '''

        url = '{0}/v1/signups'.format(self.base_url)

        #Convert expected paramaters into a dictionary with proper param names
        expected_params = {'status': status, 'region': region, 'type': type_,
                           'reference_entity_id': reference_entity_id,
                           'after_datetime': after_datetime, 'marker': marker,
                           'limit': limit}

        #Merge expected params with the params argument in case the caller
        #added any additional params.  In case of conflict, params wins over
        #expected_params
        params = dict(expected_params, **(params or {}))

        return self.request('GET', url, params=params,
                            response_entity_type=ListSignupResponse,
                            requestslib_kwargs=requestslib_kwargs)

    def signup_steps(self, signup_id=None, async=None, params=None):
        '''
        GET
        /v1/signups/{signup_id}/steps?{params}
        '''
        url = '{0}/v1/signups/{1}/steps'.format(self.base_url, signup_id)
        expected_params = {'async': async}

        params = dict(expected_params, **(params or {}))
        return self.request('GET', url, params=params)

    def signup_events(self, marker=None, limit=None, direction=None,
                      params=None, requestslib_kwargs=None):
        '''
        GET
        /v1/events/signups/success?{params}
        '''
        url = '{0}/v1/events/signups/success'.format(self.base_url)
        expected_params = {'marker': marker, 'limit': limit,
                           'direction': direction}
        params = dict(expected_params, **(params or {}))
        return self.request('GET', url, params=params)

    def signup_events_marker(self, datetime=None, params=None):
        '''
        GET
        /v1/events/signups/success/marker?{params}
        '''
        url = '{0}/v1/events/signups/success/marker'.format(self.base_url)
        expected_params = {'datetime': datetime}
        params = dict(expected_params, **(params or {}))
        return self.request('GET', url, params=params)

    def get_a_signup(self, signup_id=None):
        '''
        GET
        /v1/signups/{signup_id}
        '''
        url = '{0}/v1/signups/{1}'.format(self.base_url, signup_id)
        return self.request('GET', url)

    def get_atom_hopper_events(self):
        '''
        GET
        https://atom.staging.ord1.us.ci.rackspace.net/sites/events
        '''
        # the url is as in the configuration. This is hard coded as this
        # url is been given in the signup.properties configuration and
        # will be same for any QE environment. The url is
        # 'https://atom.staging.ord1.us.ci.rackspace.net/sites/events'
        url = self.ah_endpoint
        return self.request('GET', url)

    def get_user_identity(self, username=None):
        '''
        GET
        https://staging.identity.api.rackspacecloud.com/v2.0/users/{username}

        '''
        #identity_url = 'https://staging.identity.api.rackspacecloud.com'
        url = '{0}/v2.0/users?name={1}'.format(
            self.identity_endpoint, username)
        return self.request('GET', url)

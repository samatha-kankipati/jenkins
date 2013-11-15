from ccengine.clients.base_client import BaseMarshallingClient
from ccengine.domain.core.request.core_request import CoreQuery, \
     LoadArgs, Where, CTKObject
from ccengine.domain.core.response.core import Core
from ccengine.domain.core.response.core import Value


class CoreAPIClient(BaseMarshallingClient):
    '''
    Client for CTK API
    '''
    def __init__(self, url, auth_token, serialize_format=None,
                 deserialize_format=None):

        super(CoreAPIClient, self).__init__(serialize_format,
                                            deserialize_format)
        self.auth_token = eval(auth_token).get("authtoken")
        self.default_headers['X-Auth'] = self.auth_token
        ct = ''.join(['application/', self.serialize_format])
        accept = ''.join(['application/', self.deserialize_format])
        self.default_headers['Content-Type'] = ct
        self.default_headers['Accept'] = accept
        self.url = url

    def query(self, class_name, load_arg, load_method=None, attributes=None,
              set_attribute=None, method=None, args=None,
              keyword_args=None, result_map=None, action=None, meta=None,
              requestslib_kwargs=None):
        '''
        @summary: Returns the result of a query operation on CTK-API
        @param class_name: Class name on which query is executed
        @type class_name: String
        @param load_arg: Load argument object that resulted in this query
        @type load_arg: String or CTK-API object or Where Object
        @param load_method: CTK Method for loading devices
        @type load_method: String
        @param attributes: Attributes of CTK Objects
        @type attributes: List of attributes or dictionary of name-value pairs
        @param set_attribute: Sets values of attributes
        @type set_attribute: CTK object, single item or array of one item
        @param method: Name of method to be executed
        @type method: String
        @param args: Array of arguments to be passed to a method or action
        @type args: Array
        @param keyword_args: Associative array of key/value pairs to be passed
        @type keyword_args: Key Value Pairs
        @param result_map: Set of attributes to map a the result of a method
        @type result_map: Array
        @param action: Name of action to be executed
        @type action: String
        '''
        core_request_object = CoreQuery(class_name=class_name,
                                        load_arg=LoadArgs(load_arg),
                                        load_method=load_method,
                                        attributes=attributes,
                                        set_attribute=set_attribute,
                                        method=method,
                                        args=args,
                                        keyword_args=keyword_args,
                                        result_map=result_map,
                                        action=action,
                                        meta=meta
                                       )
        url = '%squery' % (self.url)
        response = self.request('POST', url,
                                response_entity_type=Core,
                                request_entity=core_request_object,
                                requestslib_kwargs=requestslib_kwargs)
        return response

    def list(self, class_name, where_class, where_conditions, attributes,
             limit=None, offset=None):
        '''
        @summary: Returns the result of a where query on CTK-API
        @param class_name: Query class to be used
        @type class_name: String
        @param where_class: WhereTable class to be used
        @type where_class: String
        @param where_conditions: Values of where conditions
        @param type: Array of CTK API objects
        @param limit: Effective limit on returned query
        @type limit: integer
        @param offset: Effective offset of returned query
        @type offset: integer
        '''
        where_load_arg = Where(where_class, where_conditions,
                               limit, offset)
        response = self.query(class_name=class_name,
                             load_arg=where_load_arg,
                             attributes=attributes)
        return response

    def build_ctk_object(self, class_name, load_value_or_where_conditions,
                         load_method=None):
        '''
        @summary: Build CTK Request Object for use in query request calls
        @param class_name: class name
        @type class_name: string
        @param load_value_or_where_conditions: Load_value for the ctk instance
        @type load_value_or_where_conditions: Load_value for the ctk instance
                                              or Where conditions of type
                                              WhereCondition or WhereSet
        @param load_method: Name of the load method
        @type load_method: string
        '''
        ctk_object = CTKObject(class_name, load_value_or_where_conditions,
                               load_method)
        return ctk_object

    def set_attribute(self, class_name, load_arg,
                      attribute_name, attribute_value):
        '''
        @summary: Set Attribute value on a CTK object
        @param class_name: Class Name
        @type class_name: string
        @param load_arg:  Load value to get the CTK object
        @type load_arg: LoadArgs
        @param attributeName: Name of the attribute
        @type attributeName: string
        @param attributeValue: Value of the attribute
        @type attributeValue: Type of the attribute
        '''
        attribute_map = {attribute_name: attribute_value}
        ctk_object = self.query(class_name, load_arg,
                                set_attribute=attribute_map)
        return ctk_object

    def get_attribute(self, class_name, load_value, attribute,
                      requestslib_kwargs=None):
        '''
        @summary: Get attribute value on a CTK object
        @param class_name: Class Name
        @type class_name: string
        @param load_value:  Load value to get the CTK object
        @type load_value: load_value
        @param attribute: Name of the attribute
        @type attribute: string
        '''
        url = "{0}attribute/{1}/{2}/{3}".format(self.url, class_name,
                                                load_value, attribute)
        response = self.request('GET', url,
                                response_entity_type=Value,
                                request_entity=None,
                                requestslib_kwargs=None)
        return response

    def get_values(self, class_name):
        '''
        @summary: get all values of the specified class
        @param class_name: Class Name
        @type class_name: string
        '''
        url = "{0}values/{1}".format(self.url, class_name)

        response = self.request('GET', url,
                                response_entity_type=Value,
                                request_entity=None,
                                requestslib_kwargs=None)
        return response

    def get_session_detail(self, auth_token):
        '''
        @summary: get session details for an given auth_token
        @param auth_token: auth_token
        @type auth_token: string
        '''
        url = "{0}session/{1}".format(self.url, auth_token)
        response = self.request('GET', url,
                                response_entity_type=Value,
                                request_entity=None,
                                requestslib_kwargs=None)
        return response

    def get_module_details(self):
        '''
        @summary: get the number of modules available in CTKAPI
        '''
        url = "{0}modules".format(self.url)
        response = self.request('GET', url,
                                response_entity_type=Value,
                                request_entity=None,
                                requestslib_kwargs=None)
        return response

    def get_class_details(self, module):
        '''
        @summary: get class details for an given module
        @param module: module
        @type module: string
        '''
        url = "{0}classes/{1}".format(self.url, module)
        response = self.request('GET', url,
                                response_entity_type=Value,
                                request_entity=None,
                                requestslib_kwargs=None)
        return response

    def get_methods_in_a_class(self, module, class_name):
        '''
        @summary: get class details for an given module
        @param module: module
        @type module: string
        @param class_name: Class name
        @type class_name: string
        '''
        url = "{0}methods/{1}.{2}".format(self.url, module, class_name)
        response = self.request('GET', url,
                                response_entity_type=Value,
                                request_entity=None,
                                requestslib_kwargs=None)
        return response

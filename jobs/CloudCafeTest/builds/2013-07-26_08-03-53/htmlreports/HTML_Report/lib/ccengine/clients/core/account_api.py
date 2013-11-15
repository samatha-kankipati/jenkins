from ccengine.clients.core.core_api import CoreAPIClient


class AccountAPIClient(CoreAPIClient):
    '''
    Client for account related queries in CTK API
    '''
    def __init__(self, url, auth_token, serialize_format=None,
                 deserialize_format=None):

        super(AccountAPIClient, self).__init__(url, auth_token,
                                               serialize_format,
                                               deserialize_format)

    def account_add_contract(self, account_id, start_date, length, result_map,
                             site_id=None, label=None, sales_rep=None, keyword_args=None):
        '''
        @param account: Account on which contract to be added
        @type account: String
        @param start_date: start_date of a contract
        @type start_date: Date
        @param label: Label for a Contract (optional)
        @type label: String
        @param length: Length for a Contract (optional)
        @type length: integer
        @param site_id: site_id for a Contract (optional)
        @type site_id: integer
        @param result_map: Results Map
        @type: Array of Name Value pairs
        '''
        class_name = "Account.Account"
        method = "addContract"
        load_arg = account_id
        args = [start_date, length, site_id, label, sales_rep]

        response = self.query(load_arg=load_arg,
                              class_name=class_name,
                              method=method, args=args,
                              keyword_args=keyword_args,
                              result_map=result_map)
        return response

    def add_note_account(self, account_id, note):
        '''
        @param account: Account on which contract to be added
        @type account: String
        @param note: Text message which can be added to an account
        @type note: String
        '''
        class_name = "Account.Account"
        method = "addNote"
        load_arg = account_id
        args = [note]

        response = self.query(load_arg=load_arg,
                              class_name=class_name,
                              method=method, args=args)
        return response

    def get_recent_notes(self, account_id):
        '''
        @param account id: Id of an account for which note is added
        @type account id: Integer
        '''
        attributes = {"recent_note": "recent_notes.text"}
        class_name = "Account.Account"
        load_arg = account_id
        response = self.query(load_arg=load_arg,
                              class_name=class_name,
                              attributes=attributes)
        return response

    def get_account_attributes(self, where_conditions, attributes=None,
                               limit=None, offset=None):
        '''
        @summary: Get Attributes of an Account
        @param where_conditions: Values of where conditions
        @type where_conditions: Array of CTK API objects
        @param attributes: Attributes of CTK Objects
        @type attributes: List or dictionary of attribute name-value pairs
        @param limit: Effective limit on returned query
        @type limit: integer
        @param offset: Effective offset of returned query
        @type offset: integer
        '''
        if attributes is None:
            attributes = ["number"]
        response = self.list(class_name="Account.Account",
                             where_class="Account.AccountWhere",
                             where_conditions=where_conditions,
                             attributes=attributes,
                             limit=limit, offset=offset)
        return response

    def get_account_attribute(self, load_value, attribute=None):
        '''
        @summary: Get Attribute value of an Contact module
        @param attributes: Attributes of Contact module
        @type attributes: String
        '''
        if attribute is None:
            attribute = ["id"]
        response = self.get_attribute(class_name="Account.Account",
                                      load_value=load_value,
                                      attribute=attribute)
        return response

    def get_session_details(self):
        '''
        @summary: Get user_id of a user with department, for a valid auth token
        '''
        auth_token = eval(self.auth_token).get("authtoken")
        response = self.get_session_detail(auth_token)
        return response

    def get_invalid_session_details(self):
        '''
        @summary: Get validity as False, for an invalid auth token
        '''
        auth_token = '"34t5374hsdhkjh"'
        response = self.get_session_detail(auth_token=auth_token)
        return response

from ccengine.clients.core.core_api import CoreAPIClient
from ccengine.domain.core.request.core_request import LoadArgs, Where


class ContactAPIClient(CoreAPIClient):

    def __init__(self, url, auth_token, serialize_format=None,
                 deserialize_format=None):
        super(ContactAPIClient, self).__init__(url, auth_token,
                                               serialize_format,
                                               deserialize_format)

    def build_contact_object(self, load_arg,
                             load_method=None):
        '''
        Builds a contact object
        '''
        load_arg = LoadArgs(Where("Contact.ContactWhere", load_arg))
        contact_object = self.build_ctk_object("Contact.Contact", load_arg)
        return contact_object

    def get_contact_attributes(self, where_conditions, attributes=None,
                               limit=None, offset=None):
        '''
        @summary: Get Attributes of an Contact
        @param where_conditions: Values of where conditions
        @type where_conditions: Array of CTK API objects
        @param attributes: Attribute of CTK Objects
        @type attributes: List or dictionary of attribute name-value pairs
        @param limit: Effective limit on returned query
        @type limit: integer
        @param offset: Effective offset of returned query
        @type offset: integer
        '''
        if attributes is None:
            attributes = ["id"]
        response = self.list(class_name="Contact.Contact",
                             where_class="Contact.ContactWhere",
                             where_conditions=where_conditions,
                             attributes=attributes,
                             limit=limit, offset=offset)
        return response

    def get_contact_attribute(self, load_value, attribute=None):
        '''
        @summary: Get Attribute value of an Contact module
        @param attributes: Attributes of Contact module
        @type attributes: String
        @param load_value: Contact id
        @type load_value: integer
        '''
        if attribute is None:
            attribute = ["id"]
        response = self.get_attribute(class_name="Contact.Contact",
                                      load_value=load_value,
                                      attribute=attribute)
        return response

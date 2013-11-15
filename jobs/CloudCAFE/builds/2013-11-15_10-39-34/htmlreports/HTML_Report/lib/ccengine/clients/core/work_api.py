#from ccengine.clients.core.core_api import CoreAPIClient
#from ccengine.domain.core.request.core_request import LoadArgs, Where
#
#
#class ContactAPIClient(CoreAPIClient):
#
#    def __init__(self, url, auth_token, serialize_format=None,
#                 deserialize_format=None):
#        super(ContactAPIClient, self).__init__(url, auth_token,
#                                               serialize_format,
#                                               deserialize_format)
#
#    def build_contact_object(self, load_arg,
#                             load_method=None):
#        '''
#        Builds a contact object
#        '''
#        load_arg = LoadArgs(Where("Contact.ContactWhere", load_arg))
#        contact_object = self.build_ctk_object("Contact.Contact", load_arg)
#        return contact_object

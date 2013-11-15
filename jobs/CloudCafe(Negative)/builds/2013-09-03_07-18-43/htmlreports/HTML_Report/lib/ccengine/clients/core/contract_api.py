from ccengine.clients.core.core_api import CoreAPIClient


class ContractAPIClient(CoreAPIClient):
    '''
    Client for Contract related queries in CTK API
    '''
    def __init__(self, url, auth_token, serialize_format=None,
                 deserialize_format=None):

        super(ContractAPIClient, self).__init__(url, auth_token,
                                                serialize_format,
                                                deserialize_format)

    def get_contract_details(self, contract):
        '''
        @param contract id: Id of a contract
        @type contract id: Integer
        '''
        attributes = ["start", "length", "id", "label", "site_id", "salesperson"]
        class_name = "Contract.Contract"
        load_arg = contract
        response = self.query(load_arg=load_arg,
                              class_name=class_name,
                              attributes=attributes)
        return response

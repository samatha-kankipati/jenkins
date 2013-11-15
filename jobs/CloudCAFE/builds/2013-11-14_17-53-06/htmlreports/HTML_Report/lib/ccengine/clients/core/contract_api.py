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

    def add_new_server(self, contract, datacenter):
        """
        @summary: It creates a new server in the given data center for a valid
        contract id, otherwise gives valid exception with error message
        @param Contract: Contract Id
        @type Contract: Integer
        @param Datacenter: Datacenter Id
        @type Datacenter: Integer
        """
        class_name = "Contract.Contract"
        load_arg = contract
        args = [datacenter]
        response = self.query(load_arg=load_arg,
                              class_name=class_name,
                              method="addNewServer",
                              args=args)
        return response

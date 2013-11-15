from urlparse import urljoin
from ccengine.clients.base_client import BaseMarshallingClient


class MaasAPIClient(BaseMarshallingClient):

    def __init__(self, url, auth_token,
                 serialize_format=None, deserialize_format=None):
        super(MaasAPIClient, self).__init__(serialize_format,
                                            deserialize_format)
        self.auth_token = auth_token
        self.default_headers['X-Auth-Token'] = auth_token
        self.default_headers['Content-Type'] = 'application/{0}'.format(
            self.serialize_format)
        self.default_headers['Accept'] = 'application/{0}'.format(
            self.deserialize_format)
        # Url needs a trailing '/' for urljoin
        self.url = "{0}/".format(url)

    def get_entities_list(self):
        '''
        @summary : Lists all the entities of the account
        @rtype: Response Object
        '''

        '''
        GET
        /entities
        '''
        url = urljoin(self.url, "entities")
        server_response = self.request("GET", url=url)
        return server_response

    def get_agents_list(self):
        '''
        @summary : Lists all the agents of the account
        @rtype: Response Object
        '''

        '''
        GET
        /agents
        '''
        url = urljoin(self.url, "agents")
        server_response = self.request("GET", url=url)
        return server_response

    def get_entity(self, entity_id):
        '''
       @summary : Return the entity with id entity_id
       @rtype: Response Object
       '''

        '''
        GET
        /entities/{entityId}
        '''
        url = urljoin(self.url, 'entities/%s' % entity_id)
        server_response = self.request("GET", url=url)
        return server_response

    def get_agent(self, agent_id):
        '''
       @summary : Return the agent with id agent_id
       @rtype: Response Object
       '''

        '''
        GET
        /agents/{agentId}
        '''

        url = urljoin(self.url, 'entities/%s' % agent_id)
        server_response = self.request("GET", url=url)
        return server_response

    def get_agent_connections_list(self, agent_id):
        '''
        @summary : Return the agent connections for agent with id agent_id
        @rtype: Response Object
        '''

        '''
        GET
        agents/{agentId}/connections
        '''
        url = urljoin(self.url, 'agents/%s/connections' % agent_id)
        server_response = self.request("GET", url=url)
        return server_response
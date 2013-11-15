from ccengine.domain.atomhopper import AtomFeed
from ccengine.clients.base_client import BaseMarshallingClient
#from xml.etree import ElementTree


class AtomHopperClient(BaseMarshallingClient):

    def __init__(self, atom_feed_url, token=None, serialize_format='xml',
                 deserialize_format='xml'):
        self.atom_feed_url = atom_feed_url
        super(AtomHopperClient, self).__init__(serialize_format,
                                               deserialize_format)
        self.token = token
        if token is not None:
            self.default_headers['X-Auth-Token'] = token
        self.url = atom_feed_url

    def get_preconstructed_feed(self, url, requestslib_kwargs=None):
        requestslib_kwargs = requestslib_kwargs or {}
        return self.request('GET', url,
                                  response_entity_type=AtomFeed,
                                  requestslib_kwargs=None)

    def get_feed(self, url=None, limit=None, search=None, params=None,
                 requestslib_kwargs=None):
        '''
        @summary: Returns an iterable atom feed.
        @param url: the url used to get the atom feed (used for overriding the
                    instance's default self.atom_feed_url on a per-call basis)
        @type url: String
        @param limit: limits the results per page returned by the API. Added
                      to the Requests params dictionary
        @type limit: Int
        @param search: A string sent to the api. Added to the Requests params
                       dictionary
        @type search: String
        @param params: The query string paramters.
        @type params: Dictionary
        @return: The atom feed domain object.
        @rtype: Object(AtomFeed)
        '''

        #Set 'limit' and 'search' in the 'params' dictionary unless those keys
        #already exist in 'params'.
        params = dict({'limit': limit, 'search': search}, **(params or {}))

        #Use the url that was set when this client was instantiated unless
        #another url is passed in to override it.
        url = url or self.atom_feed_url

        return self.request('GET', url, params=params,
                                  response_entity_type=AtomFeed,
                                  requestslib_kwargs=requestslib_kwargs)

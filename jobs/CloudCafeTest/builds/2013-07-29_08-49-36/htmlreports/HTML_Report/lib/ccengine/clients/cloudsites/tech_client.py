from ccengine.common.connectors import rest

class SitesTechnologies(object):
    _suffix = '/technologies'

    def __init__(self, url):
#        auth_token = '324f1c86-8720-4633-86b6-d193c544ca8a'
        self.url = ''.join([url, self._suffix])
#        self.auth_token = auth_token
        self.headers = {}
#        self.headers['X-Auth-Token'] = auth_token
        self.headers['Content-Type'] = 'application/json'
        self.headers['Accept'] = 'application/json'
        self.headers['Bypass-Auth'] = 'true'
        
    def get_techtype(self, **kwargs):
        '''
            GET
            /technologies
        '''
        return rest.get(self.url, headers=self.headers, verify=False)
    
    def __str__(self):
        return str(self.url) + str(self.headers)
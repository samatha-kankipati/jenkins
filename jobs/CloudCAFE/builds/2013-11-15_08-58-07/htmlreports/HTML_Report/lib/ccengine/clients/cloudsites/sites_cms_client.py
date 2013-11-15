from ccengine.common.connectors import rest

class SitesCmsWp(object):
    _suffix = '/sites'

    def __init__(self, url):
#        auth_token = '324f1c86-8720-4633-86b6-d193c544ca8a'
        self.url = ''.join([url, self._suffix])
#        self.auth_token = auth_token
        self.headers = {}
#        self.headers['X-Auth-Token'] = auth_token
        self.headers['Content-Type'] = 'application/xml'
        self.headers['Accept'] = 'application/xml'
        self.headers['Bypass-Auth'] = 'true'

    def get_callback(self, jobid):
        '''
            GET
            /sites/{jobid}
        '''
        return rest.get('/'.join([self.url, jobid]), headers=self.headers, verify=False)
    
    def post_createwp(self, body, **kwargs):
        '''
            POST
            /sites/
        '''
        body = """<siteContainer xmlns="http://docs.openstack.org/sites/api/v1.0">
<site fqdn="www.ryanqesite225.com"  technologyType="PHP53" />
<database name="ryqe225" password="Password!" user="ryqe225"/>
<application title="wptitle" username="wpryan" password="Password!" emailAddress="ryan.dorothy@gmail.com"/>
</siteContainer>"""
        return rest.post(self.url, headers=self.headers, data=body, 
                         verify=False)
        

    
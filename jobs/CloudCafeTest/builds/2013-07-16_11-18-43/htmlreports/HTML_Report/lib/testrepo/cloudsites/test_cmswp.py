from ccengine.clients.CloudSites.sites_cms_client import SitesCmsWp
#from xml.dom.minidom import parseString
import unittest

''' Soc = SitesOrchestration '''

class SocCmsTest(unittest.TestCase):
    
    def test_test(self):
        url = 'http://orch-n01.dev.ord1.stabletransit.com:8080/v1.0/99200004'
#        url = 'http://orch-n01.dev.ord1.stabletransit.com:8080/v1.0/99200004/technologies'
#        auth_token = '03538544-7e1b-4247-843d-563c83ba6154'
#        jobid = '121'
        '''
        The next three lines of code are the correct way to send only one
        request and set the response to a variable which is then used to get
        specific fields from that response
        '''
        client = SitesCmsWp(url) 
        response = client.post_createwp('')
        print response.request.url


#        print client.post_createwp('').request.url
#        print client.post_createwp('').content
#        print client.post_createwp('').status_code
#        print client.post_createwp('').headers
#        print client.get_callback(jobid).request.url
#        print client.get_callback(jobid).content
#        data = client.get_callback(jobid).content
#        dom = parseString(data)
#        xmlTag = dom.getElementsByTagName('status')[0].toxml()
#        print xmlTag

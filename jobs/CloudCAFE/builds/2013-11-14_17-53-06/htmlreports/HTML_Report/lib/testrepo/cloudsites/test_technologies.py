from ccengine.clients.CloudSites.tech_client import SitesTechnologies as ST
import unittest
import json

''' Soc = SitesOrchestration '''

class SocTechTest(unittest.TestCase):
    
    def test_smk_tech(self):
        url = 'http://orch-n01.dev.ord1.stabletransit.com:8080/v1.0/99200004'
        client = ST(url)
        response = client.get_techtype()
        self.assertEqual(response.status_code, 200)
        print 'Smoke test passed!'
        
    def test_int_tech(self):
        is_wordpress = False
        is_php53 = False
        is_iis = False
        is_iisdotnet4 = False
        url = 'http://orch-n01.dev.ord1.stabletransit.com:8080/v1.0/99200004'
        client = ST(url)
        response = client.get_techtype()
        json_vals = json.loads(response.text)
        for x in json_vals[u'technologies']:
            n = x.get(u'name')
            if n == u'WORDPRESS':
                is_wordpress = True
            if n == u'PHP53':
                is_php53 = True
            if n == u'IIS':
                is_iis = True
            if n == u'IISDOTNET4':
                is_iisdotnet4 = True
        self.assertTrue(is_wordpress and is_iis and is_iisdotnet4 and is_php53,
                         'You failed HARD!!!!')
        print 'Integration test 1 passed'                
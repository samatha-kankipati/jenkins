import time
import json
import re
import os
import pickle

from ccengine.common.tools import datagen
from testrepo.common.testfixtures.object_storage_fixture \
        import CloudFilesTestFixture


class CloudFiles_AtomHopper_Smoke(CloudFilesTestFixture):

    @classmethod
    def setUpClass(cls):
        super(CloudFiles_AtomHopper_Smoke, cls).setUpClass()

    #def tearDown(self):
    #    pass

    #def test_atom_hopper_connection(self):
    #    resp = self.atomhopper_provider.\
    #            events_by_tenantId_par(self.provider.account_id, 10, 1000)

        #self.assertTrue(resp.ok,
        #        'Atom feed events returned a successfull status code')
        #print resp.entity


        #    results[search_regex] = self.atomhopper_provider.\
        #    search_past_events_by_attribute(search_attrib, search_regex,
        #                                    cutoff_attrib, cutoff_regex)
        #
        #for r in results:
        #    assert results[r] is not None, 'Volume %s not Found' % str(r)

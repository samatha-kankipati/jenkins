from testrepo.common.testfixtures.blockstorage import VolumesAPIFixture
import time
import json
import re
import os
import pickle
from ccengine.common.tools import datagen


class VolumesAPI_Usage_Smoke(VolumesAPIFixture):

    @classmethod
    def setUpClass(cls):
        super(VolumesAPI_Usage_Smoke, cls).setUpClass()

    def tearDown(self):
        #r = self.volumes_api_provider.volumes_client.list_all_volumes()
        #assert r.ok, 'list volumes response code ok'
        #assert getattr(r, 'entity', None), 'Response domain object unavailable'
        #volumes = r.entity
        #for v in volumes:
        #    if v.display_name is not None:
        #        if re.search('QEUsageIntegrationTest*', v.display_name):
        #            status = self.volumes_api_provider.verifiable_volume_delete(v.id)
        #            print v.display_name
        #            print v.id
        #            print status
        #            print '\n'
        pass

    def load_usage_data(self):
        data = []
        for f in os.listdir('./'):
            if re.search('volumepickle*', f):
                fh = open(f, 'r')
                vinfo = pickle.load(fh)

                #Setup search and cutoff vars from data
                search_attrib = 'resource_id'
                search_regex = vinfo.display_name
                cutoff_attrib = 'start_time'

                '''
                    TODO: Use the time library here instead of this
                         custom time-parsing code-debacle
                '''

                c_date, c_time = vinfo.created_at.split('T')
                m = re.search(r'([0-9][0-9][0-9][0-9])-([0-1][0-9])-([0-9][0-9])', c_date)
                assert m is not None

                #Decrement date by 1 day
                c_year, c_month, c_day = m.groups()
                c_day = int(c_day) - 1
                if c_day == 0:
                    c_day = 28
                    c_month = int(c_month) - 1
                if c_month == 0:
                    c_month = 12
                    c_year = int(c_year) - 1

                c_year = str(c_year)

                if len(str(c_month)) == 1:
                    c_month = '0%s' % str(c_month)

                if len(str(c_day)) == 1:
                    c_day = '0%s' % str(c_day)

                cutoff_regex = '%s-%s-%sT.*' % (c_year, c_month, c_day)
                data.append((search_attrib, search_regex, cutoff_attrib, cutoff_regex))
        return data

    def test_verify_usage(self):
        results = {}
        #usage_data = self.load_usage_data()
        usage_data = [('resource_id', 'TestVolume_854868', 'start_time', '2012-09-18T')]
        for data in usage_data:
            #Load data and setup search and cutoff vars
            search_attrib, search_regex, cutoff_attrib, cutoff_regex = data

            results[search_regex] = self.atomhopper_provider.\
            search_past_events_by_attribute(search_attrib, search_regex,
                                            cutoff_attrib, cutoff_regex)

        for r in results:
            assert results[r] is not None, 'Volume %s not Found' % str(r)

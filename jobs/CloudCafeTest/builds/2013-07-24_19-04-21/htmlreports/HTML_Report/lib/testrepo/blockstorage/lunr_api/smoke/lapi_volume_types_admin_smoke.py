'''
@summary: Lunr API Volume Types Smoke Test - List Volume Types.
@copyright: Copyright (c) 2012 Rackspace US, Inc.
'''
import json

from testrepo.common.testfixtures.blockstorage import LunrAPIFixture
from ccengine.domain.blockstorage.lunr_api import VolumeType


class LunrVolumeTypesAdminAPISmokeTest(LunrAPIFixture):
    '''
        @summary: Lunr API Volume Types Smoke Test - List Volume Types.
    '''
    def test_list_volume_types(self):
        resp = self.admin_client.VolumeTypes.list()
        assert resp.ok, 'VolumeTypes list returned {0}, expected 2XX'
        vtypes = self.LunrAPIProvider.convert_json_to_domain_object_list(
                json.loads(resp.content), VolumeType)
        for vtype in vtypes:
            self.assertTrue(hasattr(vtype, 'status'))
            self.assertTrue(hasattr(vtype, 'name'))
            self.assertTrue(hasattr(vtype, 'min_size'))
            self.assertTrue(hasattr(vtype, 'max_size'))

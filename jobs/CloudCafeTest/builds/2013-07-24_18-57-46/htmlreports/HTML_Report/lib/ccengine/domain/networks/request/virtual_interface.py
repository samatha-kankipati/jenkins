from ccengine.domain.base_domain import BaseMarshallingDomain
import json
import xml.etree.ElementTree as ET
from ccengine.common.constants.compute_constants import Constants


class VirtualInterface(BaseMarshallingDomain):

    ROOT_TAG = 'virtual_interface'

    def __init__(self, network_id=None):
        '''An object that represents the data of a Virtual Interface'''
        super(VirtualInterface, self).__init__()
        self.network_id = network_id

    def _obj_to_json(self):
        ret = {'network_id': self.network_id}
        ret = {self.ROOT_TAG: ret}
        return json.dumps(ret)

    def _obj_to_xml(self):
        ret = self._mini_auto_to_xml(format_type='attr')
        return ret

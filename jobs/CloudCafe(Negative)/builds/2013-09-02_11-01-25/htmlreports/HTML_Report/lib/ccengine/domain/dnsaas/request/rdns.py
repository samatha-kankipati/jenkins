from ccengine.domain.base_domain import BaseMarshallingDomain
from ccengine.domain.base_domain import BaseDomain
import xml.etree.ElementTree as ET
import json


class RDNS(BaseMarshallingDomain):

    def __init__(self, recordsList=None, link=None):
        self.recordsList = recordsList
        self.link = link

    def _obj_to_json(self):
        return json.dumps(self._obj_to_dict())

    def _obj_to_dict(self):
        ret = {'recordsList': self.recordsList._obj_to_dict(),
               'link': self.link._obj_to_dict()}
        return ret

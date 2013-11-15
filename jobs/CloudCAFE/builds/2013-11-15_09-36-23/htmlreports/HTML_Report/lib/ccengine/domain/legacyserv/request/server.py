from ccengine.domain.base_domain import BaseMarshallingDomain
from ccengine.domain.base_domain import BaseDomain
import xml.etree.ElementTree as ET
import json


class Server(BaseMarshallingDomain):

    def __init__(self, name=None, image_id=None, flavor_id=None,
                  path=None, metadata=None, content=None):

        #Common Attributes
        self.name = name
        self.content = content
        self.metadata = metadata
        self.image_id = image_id
        self.flavor_id = flavor_id
        self.path = path

    #Request Generators
    def _obj_to_json(self):
        ret = self._obj_to_dict()
        return json.dumps(ret)

    def _obj_to_dict(self):

        ret = {}
        if self.name:
            ret["name"] = self.name
        if self.image_id:
            ret["imageId"] = self.image_id
        if self.flavor_id:
            ret['flavorId'] = self.flavor_id

        return {'server': ret}
    
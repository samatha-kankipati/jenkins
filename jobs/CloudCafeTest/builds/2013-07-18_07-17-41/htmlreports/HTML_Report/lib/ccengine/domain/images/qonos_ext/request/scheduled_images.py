from ccengine.domain.base_domain import BaseMarshallingDomain
from ccengine.common.constants.images_constants import Constants
import json
import xml.etree.ElementTree as ET


class ScheduledImages(BaseMarshallingDomain):

    ROOT_TAG = 'image_schedule'

    def __init__(self, retention=None):

        super(ScheduledImages, self).__init__()
        self.retention = retention

    def _obj_to_json(self):

        ret = self._obj_to_dict()

        return json.dumps({self.ROOT_TAG: ret})

    def _obj_to_dict(self):

        ret = {}

        if self.retention is not None:
            ret["retention"] = self.retention

        return ret

    def _obj_to_xml(self):

        element = ET.Element(self.ROOT_TAG)
        xml = Constants.XML_HEADER

        element.set('xmlns', Constants.XML_API_SCH_IMG_NAMESPACE)
        element.set('retention', str(self.retention))

        xml += ET.tostring(element)

        return xml

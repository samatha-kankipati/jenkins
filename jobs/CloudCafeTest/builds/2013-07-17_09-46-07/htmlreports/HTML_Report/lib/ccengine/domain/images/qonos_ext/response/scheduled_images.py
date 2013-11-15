from ccengine.domain.base_domain import BaseMarshallingDomain
import json
import xml.etree.ElementTree as ET
from ccengine.common.constants.images_constants import Constants


class ScheduledImages(BaseMarshallingDomain):

    ROOT_TAG = 'image_schedule'

    def __init__(self, retention=None):

        super(ScheduledImages, self).__init__()
        self.retention = retention

    @classmethod
    def _json_to_obj(cls, serialized_str):

        ret = None

        json_dict = json.loads(serialized_str)

        if json_dict.get(cls.ROOT_TAG) is not None:
            ret = cls._dict_to_obj(json_dict.get(cls.ROOT_TAG))

        return ret

    @classmethod
    def _dict_to_obj(cls, dic):

        kwargs = {'retention': str(dic.get('retention'))}

        return ScheduledImages(**kwargs)

    @classmethod
    def _xml_to_obj(cls, serialized_str):

        element = ET.fromstring(serialized_str)
        cls._remove_namespace(element, Constants.XML_API_SCH_IMG_NAMESPACE)
        sch_img_dict = {}

        for child in element:
            if child.tag == 'retention':
                sch_img_dict['retention'] = child.text

        sch_img = ScheduledImages(**sch_img_dict)

        return sch_img

    @classmethod
    def _xml_ele_to_obj(cls, element):

        sch_img_dict = {}

        for child in element:
            if child.tag == 'retention':
                sch_img_dict['retention'] = str(child.text)

        sch_img = ScheduledImages(**sch_img_dict)

        return sch_img

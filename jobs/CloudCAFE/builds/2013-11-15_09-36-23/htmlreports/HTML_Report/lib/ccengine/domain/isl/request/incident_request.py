from ccengine.domain.base_domain import BaseMarshallingDomain
import json
import xml.etree.ElementTree as ET
from ccengine.common.constants.isl_constants import Constants

class CreateIncident(BaseMarshallingDomain):
    ROOT_TAG = 'incident'
    ROOT_TAG_FOR_CREATE = 'incidentForCreate'

    def __init__(self, subject, description, email_cc, category,
                 comment=[]):

        super(CreateIncident, self).__init__()
        self.subject = subject
        self.description = description
        self.email_cc = email_cc
        self.category = category
        self.comment = comment

    def _obj_to_json(self):
        ret = self._auto_to_dict()
        return json.dumps(ret)

    def _obj_to_xml(self):
        element = ET.Element('inapi:' + self.ROOT_TAG_FOR_CREATE)
        xml = Constants.XML_HEADER
        element.set('xmlns:inapi', Constants.XML_API_NAMESPACE)
        element.set('xmlns:xsi', Constants.XML_API_SCHEMA_NAMESPACE)
        element.set('xsi:type', Constants.XSI_CREATE_TYPE)
        element.set('xsi:schemaLocation', Constants.XML_API_SCHEMA_LOCATION_NAMESPACE)
        subject_ele = ET.Element('inapi:subject')
        subject_ele.text = self.subject
        element.append(subject_ele)
        desc_ele = ET.Element('inapi:description')
        desc_ele.text = self.description
        element.append(desc_ele)
        email_ele = ET.Element('inapi:email-cc')
        email_ele.text = self.email_cc
        element.append(email_ele)
        category_ele = ET.Element('inapi:category')
        for key, value in self.category.items():
            if key != 'sub-category':
               id_ele = ET.Element('inapi:' + key)
               id_ele.text = value
               category_ele.append(id_ele)
            else:
               sub_cat_ele = ET.Element('inapi:' + key)
               for key2, value2 in value.items():
                   ele = ET.Element('inapi:' + key2)
                   ele.text = value2
                   sub_cat_ele.append(ele)
               category_ele.append(sub_cat_ele)
        element.append(category_ele)
        xml += ET.tostring(element)
        return xml

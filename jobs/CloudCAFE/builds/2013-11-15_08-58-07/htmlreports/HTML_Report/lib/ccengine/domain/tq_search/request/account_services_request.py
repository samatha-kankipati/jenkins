import xml.etree.ElementTree as ET

from ccengine.common.constants.compute_constants import Constants
from ccengine.common.tools.equality_tools import EqualityTools
from ccengine.domain.base_domain import BaseDomain
from ccengine.domain.base_domain import BaseMarshallingDomain


class AccountServicesRequest(BaseMarshallingDomain):
    ROOT_TAG = 'account'

    def __init__(self, team, type, number):
        super(AccountServicesRequest, self).__init__()
        self.team = team
        self.type = type
        self.number = number

    def _obj_to_xml(self):
        element = ET.Element(self.ROOT_TAG)
        xml = Constants.XML_HEADER
        element.set('xmlns', 'http://rackspace.com/service/account/v1.0')
        element.set('team', self.team)
        element.set('type', self.type)
        element.set('number', str(self.number))
        element = ET.tostring(element)
        xml = xml + str(element)
        return xml

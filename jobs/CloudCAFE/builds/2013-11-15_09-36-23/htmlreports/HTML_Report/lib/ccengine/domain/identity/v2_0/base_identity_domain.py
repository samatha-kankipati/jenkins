from ccengine.domain.base_domain \
    import BaseMarshallingDomain, BaseMarshallingDomainList
from ccengine.common.constants.identity import V2_0Constants


class BaseIdentityDomain(BaseMarshallingDomain):

    @classmethod
    def _remove_identity_xml_namespaces(cls, element):
        cls._remove_namespace(element, V2_0Constants.XML_NS)
        cls._remove_namespace(element, V2_0Constants.XML_NS_OS_KSADM)
        cls._remove_namespace(element, V2_0Constants.XML_NS_RAX_KSKEY)
        cls._remove_namespace(element, V2_0Constants.XML_NS_OS_KSEC2)
        cls._remove_namespace(element, V2_0Constants.XML_NS_RAX_KSQA)
        cls._remove_namespace(element, V2_0Constants.XML_NS_RAX_AUTH)
        cls._remove_namespace(element, V2_0Constants.XML_NS_RAX_KSGRP)
        cls._remove_namespace(element, V2_0Constants.XML_NS_OPENSTACK_COMMON)
        cls._remove_namespace(element, V2_0Constants.XML_NS_ATOM)


class BaseIdentityDomainList(BaseMarshallingDomainList):

    @classmethod
    def _remove_identity_xml_namespaces(cls, element):
        BaseIdentityDomain._remove_identity_xml_namespaces(element)

import sys
import xml.etree.ElementTree as ET

from ccengine.common.constants.compute_constants import Constants
from ccengine.common.tools import logging_tools


class BaseDomain(object):
    ''' Base Domain Object '''
    __attrs__ = []
    __REPR_SEPARATOR__ = '\n'

    def __init__(self, **kwargs):
        self._log = logging_tools.getLogger(
                            logging_tools.get_object_namespace(self.__class__))

        for attr in self.__attrs__:
            try:
                setattr(self, attr, kwargs[attr])
            except KeyError:
                setattr(self, attr, None)

    def selective_compare(self, **kwargs):
        for k in kwargs:
            val = kwargs[k]
            dom_val = getattr(self, k)
            if str(val) != str(dom_val):
                return False
        return True

    @classmethod
    def _my_name(cls):
        return cls.__class__.__name__

    def __eq__(self, obj):
        if obj is None:
            return False
        for key in self.__dict__.keys():
            if self.__dict__[key] != obj.__dict__[key]:
                return False
        return True

    def __ne__(self, obj):
        if obj is None:
            return True
        for key in self.__dict__.keys():
            if self.__dict__[key] != obj.__dict__[key]:
                return True
        return False

    def __str__(self):
        ret = '<{0} object> {1}'.format(self.__class__.__name__,
                                        self.__REPR_SEPARATOR__)
        for key in self.__dict__.keys():
            if str(key) == '_log':
                continue
            ret = '{0}{1} = {2}{3}'.format(ret,
                                           str(key),
                                           str(self.__dict__[key]),
                                           self.__REPR_SEPARATOR__)
        return ret

    def __repr__(self):
        return self.__str__()


class BaseMarshallingDomain(BaseDomain):
    ''' Base Domain Object '''
    _log = logging_tools.getLogger(__name__)

    def __init__(self, **kwargs):
        super(BaseMarshallingDomain, self).__init__(**kwargs)
        self._log = logging_tools.getLogger(
                            logging_tools.get_object_namespace(self.__class__))

    def serialize(self, format_type):
        try:
            return getattr(self, '_obj_to_%s' % format_type)()
        except Exception as e:
            self._log.error('Error occured during domain object serialization')
            self._log.exception(e)
        return None

    @classmethod
    def deserialize(cls, serialized_str, format_type):
        cls._log = logging_tools.getLogger(
                                       logging_tools.get_object_namespace(cls))

        ret = None
        deserialization_exception = None
        if (serialized_str is not None) and (len(serialized_str) != 0):
            try:
                ret = getattr(cls, '_%s_to_obj' % format_type)(serialized_str)
                ''' @todo: Find a better way for backward
                           compat to < 2.7.x Python
                '''
            except Exception as deserialization_exception:
                cls._log.exception(deserialization_exception)

            #Format log strings
            if deserialization_exception:
                try:
                    cls._log.debug("Deserialization Error: Attempted to deserialize type using type: " + format_type.decode(encoding='UTF-8', errors='ignore'))
                    cls._log.debug("Deserialization Error: Unble to deserialize the following:\n" + serialized_str.decode(encoding='UTF-8', errors='ignore'))
                except Exception as e:
                    cls._log.exception(e)
                    cls._log.debug("Unable to log information regarding the deserialization exception")

        return ret

    #Serialization Functions
    def _obj_to_json(self):
        raise NotImplementedError

    def _obj_to_xml(self):
        raise NotImplementedError

    #Deserialization Functions
    @classmethod
    def _xml_to_obj(cls, serialized_str):
        raise NotImplementedError

    @classmethod
    def _json_to_obj(cls, serialized_str):
        raise NotImplementedError

    #Experimental! Use at own risk.  Requires a constant ROOT_TAG to be defined
    #in the subclass
    def _auto_to_dict(self):
        ret = {}
        for attr in vars(self).keys():
            value = vars(self).get(attr)
            #quick and dirty fix for _log getting added in
            #ideally _log should be __log, talk to Jose about this.
            if value is not None and attr != '_log':
                ret[attr] = self._auto_value_to_dict(value)

        if hasattr(self, 'ROOT_TAG'):
            return {self.ROOT_TAG: ret}
        else:
            return ret

    def _auto_value_to_dict(self, value):
        ret = None
        if isinstance(value, (int, str, unicode, bool)):
            ret = value
        elif isinstance(value, list):
            ret = []
            for item in value:
                ret.append(self._auto_value_to_dict(item))
        elif isinstance(value, dict):
            ret = {}
            for key in value.keys():
                ret[key] = self._auto_value_to_dict(value[key])
        elif isinstance(value, BaseMarshallingDomain):
            ret = value._obj_to_json()
        return ret

    def _mini_auto_to_xml(self, format_type='text', header=None):
        """Simple XML converter that assumes all attributes are strings
        and go as attributes of the ROOT_TAG if the type is attr or as
        child node text values if the type set to text (other than attr)"""
        if format_type == 'attr':
            attrib = dict(vars(self))
            if '_log' in attrib:
                del attrib['_log']
            attrs_to_delete = []
            for attr, value in attrib.iteritems():
                if value is None:
                    attrs_to_delete.append(attr)
                if value == False or value == True:
                    attrib[attr] = str(value).lower()
            for attr in attrs_to_delete:
                del attrib[attr]
            element = ET.Element(self.ROOT_TAG, attrib)
        else:
            element = ET.Element(self.ROOT_TAG)
            #if self attrs will contain lists functionality needs to be added
            for attr, value in vars(self).iteritems():
                if value is not None and attr != '_log':
                    child_node = ET.SubElement(element, attr)
                    if value == False or value == True:
                        value = str(value).lower()
                    child_node.text = value
        ret = ET.tostring(element)
        if header:
            xml = Constants.XML_HEADER
            ret = ''.join([xml, ret])
        return ret

    def _auto_to_xml(self):
        #XML is almost impossible to do without a schema definition because it
        #cannot be determined when an instance variable should be an attribute
        #of an element or text between that element's tags
        ret = ET.Element(self.ROOT_TAG)
        for attr in vars(self).keys():
            value = vars(self).get(attr)
            if value is not None:
                assigned = self._auto_value_to_xml(attr, value)
                if isinstance(assigned, ET.Element):
                    ret.append(assigned)
                else:
                    ret.set(attr, str(assigned))
        return ret

    def _auto_value_to_xml(self, key, value):
        if isinstance(value, (int, str, unicode)):
            ret = value
        elif isinstance(value, list):
            ret = ET.Element(key)
            for item in value:
                singular_key_name = key[:(len(key) - 1)]
                assigned = self._auto_value_to_xml(singular_key_name, item)
                if isinstance(assigned, ET.Element):
                    ret.append(assigned)
        elif isinstance(value, dict):
            ret = ET.Element(key)
            for dict_key in value.keys():
                assigned = self._auto_value_to_xml(dict_key, value[dict_key])
                if isinstance(assigned, ET.Element):
                    ret.append(assigned)
                else:
                    ret.set(dict_key, str(assigned))
        elif isinstance(value, BaseMarshallingDomain):
            ret = value._obj_to_xml()
        return ret

    def _set_xml_attrs(self, xml_etree_element, attr_dict):
        '''
        Sets a dictionary of keys and values as attributes of the element
        '''
        for key in attr_dict:
            if attr_dict[key] is not None:
                xml_etree_element.set(str(key), unicode(attr_dict[key]))
        return xml_etree_element

    def _remove_empty_values(self, dictionary):
        '''Returns a new dictionary based on 'dictionary', minus any keys with
        values that are None
        '''
        return dict((k, v) for k, v in dictionary.iteritems() if v is not None)

    @classmethod
    def _remove_namespace(cls, doc, namespace):
        """Remove namespace in the passed document in place."""
        ns = u'{%s}' % namespace
        nsl = len(ns)
        for elem in doc.getiterator():
            for key in elem.attrib:
                if key.startswith(ns):
                    new_key = key[nsl:]
                    elem.attrib[new_key] = elem.attrib[key]
                    del elem.attrib[key]
            if elem.tag.startswith(ns):
                elem.tag = elem.tag[nsl:]

    @classmethod
    def _remove_namespace_from_attrb(cls, doc, namespace):
        """DEPRECATED - This is being done in _remove_namespace now.
        Remove namespaces in the passed document in place."""
        ns = u'{%s}' % namespace
        nsl = len(ns)
        for elem, val in doc.items():
            if elem.startswith(ns):
                doc[elem[nsl:]] = doc.pop(elem)


class BaseDomainList(list, BaseDomain):

    def __str__(self):
        return list.__str__(self)


class BaseMarshallingDomainList(list, BaseMarshallingDomain):

    def __str__(self):
        return list.__str__(self)

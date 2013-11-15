from xml.etree import ElementTree as ET


class XMLNamespaceConstants(object):
    """
    @summary: Contains mappings of XML namespaces
    @ivar XML_NAMESPACE_MAPPINGS: The XML namespace mappings
    @tyoe XML_NAMESPACE_MAPPINGS: dict
    """

    XML_NAMESPACE_MAPPINGS = {
        '{http://customer-admin.api.rackspace.com/v1}': '',
        '{http://www.w3.org/2005/Atom}': '',
        '{http://customer.api.rackspace.com/v1}': '',
        '{http://docs.openstack.org/identity/api/v2.0}': ''}


class XMLTools(object):
    """
    @summary: Helper functions to be used in the processing of XML elements
    """

    @classmethod
    def _remove_namespace(cls, doc):
        """
        @summary: Replaces namespaces using the XML namespace mappings defined
                  in XMLNamespaceConstants
        @param doc: The element which we want to remove the namespaces from the
                    attributes
        @type doc: ElementTree.Element
        @return: The new element tree object with the namespaces replaced
        """

        if isinstance(doc, ET.Element):
            namespaces = XMLNamespaceConstants.XML_NAMESPACE_MAPPINGS

            for elem in doc.iter():
                for ns, new_val in namespaces.iteritems():
                    ns_len = len(ns)

                    for key in elem.attrib:
                        if key.startswith(ns):
                            temp_key = key[ns_len:]
                            new_key = '{0}{1}'.format(namespaces[ns], temp_key)
                            elem.attrib[new_key] = elem.attrib[key]
                            del elem.attrib[key]

                    if elem.tag.startswith(ns):
                        elem.tag = '{0}{1}'.format(namespaces[ns],
                                                   elem.tag[ns_len:])

        return doc

    @classmethod
    def _get_children(cls, element):
        """
        @summary: Gets the direct children elements of the current XML element
        @param element: The element that we want to get the direct children of
        @type element: ElementTree.Element
        @return: A dict of list of children. The keys in the dict are the tag
                 names and its value is a list of the children that have that
                 tag name.
        """

        children_dict = {}

        if isinstance(element, ET.Element):
            children = list(element)

            for child in children:
                child_no_ns = cls._remove_namespace(child)

                if child_no_ns.tag not in children_dict:
                    children_dict[child_no_ns.tag] = child_no_ns
                else:
                    if not isinstance(children_dict[child_no_ns.tag], list):
                        foster_child = children_dict[child_no_ns.tag]
                        children_dict[child_no_ns.tag] = [foster_child,
                                                          child_no_ns]
                    else:
                        children_dict[child_no_ns.tag].append(child_no_ns)

        return children_dict

    @classmethod
    def _is_et_elem(cls, element):
        """
        @summary: Indicates if the object is of type ElementTree.Element
        @param element: The element that we want to check
        @type element: object
        @return: bool
        """

        is_et_elem = False

        elem_type = type(element)

        if elem_type is list:
            if elem_type:
                if type(element[0]) is ET.Element:
                    is_et_elem = True

        if elem_type is ET.Element:
            is_et_elem = True

        return is_et_elem

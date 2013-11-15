import xml.etree.ElementTree as ET


class ETreeConvert(object):
    """
    @summary: Converts XML to a dictionary that matches JSON specific to
              how Rackspace uses it for its services
              Should not be used as a generic XML to dictionary converter
              without making the necessary changes
    @param DISABLE_NAMESPACE: Indicates whether to strip out the namespaces
                              where appropriate
    @type DISABLE_NAMESPACE: bool
    @param NAMESPACE_TO_IGNORE: A list of namespaces to strip out of the tags
                                '<?xml version' should always be in the list
    @type NAMESPACE_TO_IGNORE: List of Strings
    @param NAMESPACE_TO_USE: An instance variable that is to be populated when
                             the serialized XML string is read in
    @type NAMESPACE_TO_USE: dict
    """

    DISABLE_NAMESPACE = True
    NAMESPACE_TO_IGNORE = ['<?xml version', 'atom']
    NAMESPACE_TO_USE = {}

    def is_repeating_tag(self, element_list):
        """
        @param element_list: A list of children from the element in the
                             ElementTree
        @type element_list: List of element objects from ElementTree
        @return: A repeating element tag if exist, otherwise None
        """

        repeating_tag = None

        set_of_tags = set()
        for item in element_list:
            set_of_tags.add(self.remove_namespace(item.tag))

        if len(set_of_tags) == 1:
            repeating_tag = set_of_tags.pop()

        return repeating_tag

    def remove_namespace(self, strip_string):
        """
        @param strip_string: The string to strip the namespace from
        @type strip_string: String
        @return: A string stripped or replaced of its namespace
        """

        new_string = strip_string

        if self.DISABLE_NAMESPACE:
            if strip_string.startswith('{http://'):
                position = strip_string.find('}') + 1

                find_namespace_key = strip_string[1:position-1]

                temp_string = ''
                if find_namespace_key in self.NAMESPACE_TO_USE:
                    temp_string = '{0}:'.format(
                        self.NAMESPACE_TO_USE[find_namespace_key])
                elif strip_string.startswith(
                        '{http://customer-admin.api.rackspace.com/'):
                    temp_string = 'customer_admin:'

                if position > 0:
                    new_string = '{0}{1}'.format(temp_string,
                                                 strip_string[position:])

        return new_string

    def etree_to_dict(self, tree_node):
        """
        @param tree_node: The ElementTree instance that is to be converted
                          to a dict
        @type tree_node: ElementTree node
        @return: dict
        """

        temp_dict = {}
        children = list(tree_node)
        tree_node_tag = self.remove_namespace(tree_node.tag)

        if children:
            children_list = map(self.etree_to_dict, children)
            tag = self.is_repeating_tag(children)

            key_list = []
            for child in children:
                key_list.append(self.remove_namespace(child.tag))

            for index, child in enumerate(children_list):
                if not isinstance(child, str):
                    key_i = key_list[index]

                    if key_i in temp_dict:
                        temp_list = []

                        if isinstance(temp_dict[key_i], dict):
                            temp_list.append(temp_dict[key_i])
                        elif isinstance(temp_dict[key_i], list):
                            temp_list.extend(temp_dict[key_i])

                        if key_i in child:
                            temp_list.append(child[key_i])
                        else:
                            temp_list.append(child)

                        temp_dict.update({key_i: temp_list})
                    else:
                        if key_i == 'link' or \
                                (tag is not None and
                                 key_i not in child and
                                 isinstance(child, dict)):
                            if not isinstance(child, list):
                                child = [child]

                        if key_i in child:
                            temp_dict.update(child)
                        else:
                            temp_dict.update({key_i: child})

        if tree_node.attrib:
            temp_dict.update({self.remove_namespace(item_tag): item_value
                              for item_tag, item_value
                              in tree_node.attrib.iteritems()})

        if tree_node.text:
            text = tree_node.text.strip()

            if children or tree_node.attrib:
                if text:
                    temp_dict['value'] = text
            elif children == [] and tree_node.attrib == {}:
                if text:
                    temp_dict[tree_node_tag] = text
            else:
                temp_dict = text

        return temp_dict

    def xml_to_dict(self, serialized_string):
        """
        @summary: Takes a serialized XML string and converts it to a dictionary
        @param serialized_string: The serialized XML string
        @type serialized_string: String
        @return: A dictionary representation of the XML
        """

        clean_string = serialized_string.strip()

        namespace_tokens = clean_string.split('xmlns:')
        namespace_dict = {}
        for item in namespace_tokens:
            equal_position = item.find('=')
            quotation_mark_1 = item.find('"', equal_position) + 1
            quotation_mark_2 = item.find('"', quotation_mark_1)

            key = item[quotation_mark_1:quotation_mark_2]
            value = item[:equal_position]

            namespace_dict.update({key: value})

        self.NAMESPACE_TO_USE = {}
        for namespace_url, namespace_tag in namespace_dict.items():
            if namespace_tag not in self.NAMESPACE_TO_IGNORE and \
                    not namespace_tag.startswith('ns'):
                self.NAMESPACE_TO_USE.update({namespace_url: namespace_tag})

        root_node = ET.fromstring(clean_string)
        xml_dict = self.etree_to_dict(root_node)

        return xml_dict

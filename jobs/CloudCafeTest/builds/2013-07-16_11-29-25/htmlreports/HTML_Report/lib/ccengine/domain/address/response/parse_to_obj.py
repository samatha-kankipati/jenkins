import json
from convert_xml_to_dict import ETreeConvert as ETC


class ParseToObj(object):
    """
    @summary: Contains common functions for converting to object
              It is meant to be inherited
    """

    @classmethod
    def _json_to_obj(cls, serialized_str):
        """
        @summary: Converts an JSON serialized string to an object
        @param serialized_str: The serialized JSON string
        @type serialized_str: String
        @return: Object representation of the serialized string
        """

        json_dict = json.loads(serialized_str)
        return cls._dict_to_obj(json_dict)

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        """
        @summary: Converts an XML serialized string to an object
        @param serialized_str: The serialized XML string
        @type serialized_str: String
        @return: Object representation of the serialized string
        """

        xd = ETC()
        xml_dict = xd.xml_to_dict(serialized_str)
        return cls._dict_to_obj(xml_dict)

    @classmethod
    def _dict_to_obj(cls, dict_to_convert):
        """
        @summary: this method should be overwritten by inheriting class
        """

        pass

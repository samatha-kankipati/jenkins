import json

from ccengine.common.tools.equality_tools import EqualityTools
from ccengine.domain.base_domain import BaseMarshallingDomain


class MailgunEntity(BaseMarshallingDomain):

    def __init__(self, message, id):
        """
        An object that represents a MailgunEntity.
        """
        super(MailgunEntity, self).__init__()
        self.message = message
        self.id = id

    def __repr__(self):
        values = []
        for prop in self.__dict__:
            values.append("{0}: {1}".format(prop, self.__dict__[prop]))
        return "[{represenation}]".format(represenation=', '.join(values))

    @classmethod
    def _json_to_obj(cls, serialized_str):
        """
        Returns an instance of a MailgunEntity based on the
        json serialized_str passed in.
        """
        response_dict = json.loads(serialized_str)
        response = MailgunEntity(**response_dict)
        return response

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        """
        Not Implemented
        """
        raise NotImplementedError("Not Implemented.")

    @classmethod
    def _xml_ele_to_obj(cls, element):
        """
        Not Implemented
        """
        raise NotImplementedError("Not Implemented.")

    def __eq__(self, other):
        """
        @summary: Overrides the default equals
        @param other: Entity object to compare with
        @type other: Entity
        @return: True if Entity objects are equal, False otherwise
        @rtype: bool
        """
        return EqualityTools.are_objects_equal(self, other)

    def __ne__(self, other):
        """
        @summary: Overrides the default not-equals
        @param other: Entity object to compare with
        @type other: Entity
        @return: True if Entity objects are not equal, False otherwise
        @rtype: bool
        """
        return not self == other

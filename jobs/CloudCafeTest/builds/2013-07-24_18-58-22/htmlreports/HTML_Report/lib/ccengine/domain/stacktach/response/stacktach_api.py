from ccengine.domain.base_domain import BaseMarshallingDomain
import json
from ccengine.common.tools.equality_tools import EqualityTools


class StackTachEntity(BaseMarshallingDomain):

    def __init__(self, **kwargs):
        '''An object that represents an Entity.

        Keyword arguments:
        '''
        super(StackTachEntity, self).__init__(**kwargs)
        for keys, values in kwargs.items():
            setattr(self, keys, values)

    def __repr__(self):
        values = []
        for prop in self.__dict__:
            values.append("%s: %s" % (prop, self.__dict__[prop]))
        return '[' + ', '.join(values) + ']'

    @classmethod
    def _json_to_obj(cls, serialized_str):
        '''Returns an instance of a Entity based on the 
        json serialized_str passed in.'''
        results = json.loads(serialized_str)
        ''' One or more deployments will be a list'''
        entities = []
        for row in results[1:]:
            entity_dict = {}
            for i in range(0, len(results[0])):
                entity_dict[results[0][i]] = row[i]
                entity = cls._dict_to_obj(entity_dict)
            entities.append(entity)
        return entities

    @classmethod
    def _dict_to_obj(cls, entity_dict):
        '''Helper method to turn dictionary into Deployment instance.'''
        entity = StackTachEntity(**entity_dict)
        return entity

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        '''Not Implemented'''
        pass

    @classmethod
    def _xml_ele_to_obj(cls, element):
        '''Not Implemented'''
        pass

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

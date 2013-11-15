import json

from ccengine.domain.base_domain import BaseMarshallingDomain


class ComplexQuery(BaseMarshallingDomain):

    def __init__(self, query):
        self.query = query

    def _obj_to_json(self):
        return '{{"query": {0}}}'.format(self.query._obj_to_json())


class Property(BaseMarshallingDomain):

    def __init__(self, property_name):
        self.property_name = property_name

    def equals(self, *values):
        values = list(values)if len(values) > 1 else values[0]
        return PropertyCondition(self.property_name, Operators.EQUALS, values)

    def not_equals(self, *values):
        values = list(values)if len(values) > 1 else values[0]
        not_property = PropertyCondition(self.property_name,
                                         Operators.NOT_EQUALS, values)
        return PropertyConditionSet(not_property, Clauses.NOT)

    def in_list(self, *values):
        return PropertyCondition(self.property_name, Operators.IN,
                                 list(values))

    def in_range(self, from_value, to_value):
        return PropertyCondition(self.property_name, Operators.RANGE,
                                 from_value, to_value)


class PropertyCondition(BaseMarshallingDomain):

    def __init__(self, property, operator, value, range_value=None):
        self.property = property
        self.operator = operator
        self.value = value
        self.range_value = range_value

    def __or__(self, condition):
        return PropertyConditionSet(self, Clauses.OR, condition)

    def __repr__(self):
        return "Condition : {0} {1} {2} {3}".format(self.property,
                                                    self.operator,
                                                    self.value1,
                                                    self.value2)

    def __and__(self, condition):
        return PropertyConditionSet(self, Clauses.AND, condition)

    def __not__(self, condition):
        return PropertyConditionSet(self, Clauses.NOT, condition)

    def _obj_to_json(self):
        ret_obj = {}
        if (self.operator == Operators.RANGE):
            query = {"range": {self.property: {"from": self.value,
                                               "to": self.range_value}}}
            ret_obj = json.dumps(query)
            return ret_obj
        else:
            ret_obj = json.dumps({self.property: self.value})
            ret_obj = ret_obj.translate(None, "{}")
            return ret_obj


class PropertyConditionSet(BaseMarshallingDomain):

    def __init__(self, operand, clause, second_operand=None):
        self.operand = operand
        self.clause = clause
        self.second_operand = second_operand

    def __or__(self, condition):
        return PropertyConditionSet(self, Clauses.OR, condition)

    def __and__(self, condition):
        return PropertyConditionSet(self, Clauses.AND, condition)

    def _obj_to_json(self):
        ret_conditions = ""
        if(self.clause) is Clauses.AND:
            ret_conditions = '{{"and" : {0}}}'.format(self._operands_to_json())
        elif(self.clause) is Clauses.OR:
            ret_conditions = '{{"or" : {0}}}'.format(self._operands_to_json())
        elif(self.clause) is Clauses.NOT:
            ret_conditions = '{{"not" : {{{0}}}}}'.format(
                self.operand._obj_to_json())
        else:
            raise Exception("Clause {0} is not supported".format(self.clause))
        return ret_conditions

    def _operands_to_json(self):
        if isinstance(self.operand, PropertyConditionSet):
            return '[{0},{1}]'.format(self.operand._obj_to_json(),
                   self.second_operand._obj_to_json())
        else:
            return '{{{0},{1}}}'.format(self.operand._obj_to_json(),
                   self.second_operand._obj_to_json())

    def __repr__(self):
        return "{0} {1} {2}".format(self.operand, self.clause,
                                    self.second_operand)


class Operators(object):
    EQUALS = "equals"
    NOT_EQUALS = "not_equals"
    IN = "in"
    RANGE = "range"


class Clauses(object):
    AND = "and"
    OR = "or"
    NOT = "not"

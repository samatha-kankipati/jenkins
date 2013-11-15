from ccengine.domain.base_domain import BaseMarshallingDomain
import json

'''
@summary: CTK API Request Domain Objects
@todo: Rename as core_query.py or ctk_query.py
'''


class CoreQuery(BaseMarshallingDomain):
    '''
    @summary: Represents the CTK API Query Schema Object as per
    the Query Schema "https://<core_url>/ctkapi/schemabrowse/query"
    '''

    def __init__(self, class_name, load_arg, load_method=None,
                 attributes=None, set_attribute=None,
                 method=None, args=None, keyword_args=None,
                 result_map=None, action=None, meta=None):
        '''
        @summary: Constructs a Query Object
        @param class_name: Class of the object on which actions have to be
            performed
        @type class_name: string
        @param load_arg: Load argument to load CTK Objects
        @type load_arg: LoadArgs object
        @param load_method: CTK Method for loading object
        @type load_method: string
        @param attributes: Attributes to be returned on the CTK Object(s)
            under operation
        @type attributes: list
        @param set_attribute: Attribute and Value key value pair to be set
        @type set_attribute: dictionary
        @param method: Name of method to be executed
        @type method: string
        @param args: Mandatory arguments to be passed to a method or action
        @type args: list
        @param keyword_args: Arguments as key/value pairs to be passed to a
            method, usually the optional parameters to the method
        @type keyword_args: dictionary
        @param result_map: Set of attributes to map the result of a method to
            be used when executing a method via the 'method' action.
        @type result_map: dictionary
        @param action: Name of action to be executed
        @type action: string
        '''
        super(CoreQuery, self).__init__()
        self.class_name = class_name
        self.load_method = load_method
        self.load_arg = load_arg
        self.attributes = attributes
        self.set_attribute = set_attribute
        self.method = method
        self.args = args
        self.keyword_args = keyword_args
        self.result_map = result_map
        self.action = action
        self.meta = meta

    def _obj_to_json(self):

        list_ret = []
        ret = {}
        if self.class_name is not None:
            ret["class"] = self.class_name
        if self.load_arg is not None:
            ret["load_arg"] = self.load_arg._obj_to_json()
        if self.load_method is not None:
            ret["load_method"] = self.load_method
        if self.attributes is not None:
            ret["attributes"] = self.attributes
        if self.set_attribute is not None:
            ret["set_attribute"] = self._auto_value_to_dict(self.set_attribute)
        if self.method is not None:
            ret["method"] = self.method
        if self.args is not None:
            ret["args"] = self.args
        if self.keyword_args is not None:
            ret["keyword_args"] = self.keyword_args
        if self.result_map is not None:
            ret["result_map"] = self.result_map
        if self.action is not None:
            ret["action"] = self.action
        if self.meta is not None:
            ret["meta"] = self.meta
        list_ret.append(ret)
        return json.dumps(list_ret)


class LoadArgs(BaseMarshallingDomain):
    '''
    @summary: Represents the LoadArgs Domain object described in the CTK API
        schema https://<core_url>/ctkapi/schemabrowse/load_argument
    '''

    def __init__(self, value):
        '''
        @summary Constructs a value object for load_arg property
        @param load_arg_value : Load argument value that can be used for
            loading a CTK object
        @type load_arg_value: Can be a string / integer / CTK object /
            Where type object
        '''
        super(LoadArgs, self).__init__()
        self.value = value

    def _obj_to_json(self):
        if type(self.value) is Where:
            return self.value._obj_to_json()
        elif type(self.value) is object:
            return self.value._obj_to_json()
        else:
            return self.value


class Where(BaseMarshallingDomain):
    '''
    @summary: Represents the Where object represented in the CTK API schema
        https://<core_url>/ctkapi/schemabrowse/where
    '''
    def __init__(self, where_class, where_values, limit=None, offset=None):
        self.where_class = where_class
        self.where_values = where_values
        self.limit = limit
        self.offset = offset

    def _obj_to_json(self):

        ret = {}
        if self.where_class is not None:
            ret["class"] = self.where_class
        if self.where_values._obj_to_json() is not None:
            ret["values"] = self.where_values._obj_to_json()
        if self.limit is not None:
            ret["limit"] = self.limit
        if self.offset is not None:
            ret["offset"] = self.offset
        return ret


class WhereCondition(BaseMarshallingDomain):
    '''
    @summary: Represents the Where object represented in the CTK API schema
        https://<core_url>/ctkapi/schemabrowse/where_condition
    '''
    def __init__(self, column, operator, value):
        self.column = column
        self.operator = operator
        self.value = value

    def AND(self, other):
        return WhereSet(self, WhereSetOperators.AND, other)

    def OR(self, other):
        return WhereSet(self, WhereSetOperators.OR, other)

    def _obj_to_json(self):
        return [self.column, self.operator, self.value]


class WhereSet:
    '''
    @summary: Represents the Where object represented in the CTK API schema
        https://<core_url>/ctkapi/schemabrowse/where_set
    '''
    def __init__(self, condition1, conjunction, condition2):
        self.condition1 = condition1
        self.conjunction = conjunction
        self.condition2 = condition2

    def AND(self, other):
        return WhereSet(self, WhereSetOperators.AND, other)

    def OR(self, other):
        return WhereSet(self, WhereSetOperators.OR, other)

    def _obj_to_json(self):
        return [self.condition1._obj_to_json(),
                self.conjunction, self.condition2._obj_to_json()]


class WhereEquals(WhereCondition):

    def __init__(self, column, value):

        self.column = column
        self.operator = WhereOperators.EQUALS
        self.value = value


class WhereGreaterOrEquals(WhereCondition):

    def __init__(self, column, value):

        self.column = column
        self.operator = WhereOperators.GREATEROREQUAL
        self.value = value


class WhereLessOrEquals(WhereCondition):

    def __init__(self, column, value):

        self.column = column
        self.operator = WhereOperators.LESSOREQUAL
        self.value = value


class WhereNotEquals(WhereCondition):

    def __init__(self, column, value):

        self.column = column
        self.operator = WhereOperators.NOT
        self.value = value


class WhereIn(WhereCondition):

    def __init__(self, column, value):

        self.column = column
        self.operator = WhereOperators.IN
        self.value = value


class WhereGreater(WhereCondition):

    def __init__(self, column, value):

        self.column = column
        self.operator = WhereOperators.GREATER
        self.value = value


class WhereLess(WhereCondition):
    def __init__(self, column, value):

        self.column = column
        self.operator = WhereOperators.LESS
        self.value = value


class WhereNotIn(WhereCondition):

    def __init__(self, column, value):

        self.column = column
        self.operator = WhereOperators.NOTIN
        self.value = value


class WhereOperators:

    EQUALS = '='
    GREATEROREQUAL = ">="
    LESSOREQUAL = "<="
    IN = "in"
    NOT = "!="
    NOTIN = "not in"
    GREATER = ">"
    LESS = "<"


class WhereSetOperators:

    AND = '&'
    OR = '|'


class Attributes:
    pass


class CTKObject(BaseMarshallingDomain):
    '''
    @summary: Represents the CTK Object represented in the CTK API schema
        https://<core_url>/ctkapi/schemabrowse/ctk_object
    '''
    def __init__(self, class_name, load_arg, load_method=None, reduce=None):
        self.class_name = class_name
        self.load_arg = load_arg
        self.load_method = load_method
        self.reduce = reduce

    def _obj_to_json(self):
        ret = {}
        if self.class_name != None:
            ret["class"] = self.class_name
        if self.load_arg != None:
            ret["load_arg"] = self.load_arg
        if self.load_method != None:
            ret["load_method"] = self.load_method
        if self.reduce != None:
            ret["reduce"] = self.reduce
        return ret

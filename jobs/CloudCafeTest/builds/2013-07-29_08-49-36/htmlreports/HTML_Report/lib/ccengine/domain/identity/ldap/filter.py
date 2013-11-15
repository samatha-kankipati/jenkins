class Filter(object):

    NOT = '(!{0})'
    EQUAL = '({0}={1})'
    PRESENT = '({0}=*{1})'
    SIMILAR = '({0}=~{1})'
    LTE = '({0}<={1})'
    GTE = '({0}>={1})'
    AND = '&'
    OR = '|'

    def __init__(self):
        self._filter = ''

    def add_equal(self, key, value):
        return self._add(self.EQUAL, None, key, value)

    def add_and_equal(self, key, value):
        return self._add(self.EQUAL, self.AND, key, value)

    def add_or_equal(self, key, value):
        return self._add(self.EQUAL, self.OR, key, value)

    def add_not_equal(self, key, value):
        comparitor = self.NOT.format(self.EQUAL)
        return self._add(comparitor, None, key, value)

    def add_and_not_equal(self, key, value):
        comparitor = self.NOT.format(self.EQUAL)
        return self._add(comparitor, self.AND, key, value)

    def add_or_not_equal(self, key, value):
        comparitor = self.NOT.format(self.EQUAL)
        return self._add(comparitor, self.OR, key, value)

    def add_present(self, key):
        return self._add(self.PRESENT, None, key, '')

    def add_and_present(self, key):
        return self._add(self.PRESENT, self.AND, key, '')

    def add_or_present(self, key):
        return self._add(self.PRESENT, self.OR, key, '')

    def add_not_present(self, key):
        comparitor = self.NOT.format(self.PRESENT)
        return self._add(comparitor, None, key, '')

    def add_and_not_present(self, key):
        comparitor = self.NOT.format(self.PRESENT)
        return self._add(comparitor, self.AND, key, '')

    def add_or_not_present(self, key):
        comparitor = self.NOT.format(self.PRESENT)
        return self._add(comparitor, self.OR, key, '')

    def add_similar(self, key, value):
        return self._add(self.SIMILAR, None, key, value)

    def add_and_similar(self, key, value):
        return self._add(self.SIMILAR, self.AND, key, value)

    def add_or_similar(self, key, value):
        return self._add(self.SIMILAR, self.OR, key, value)

    def add_not_similar(self, key, value):
        comparitor = self.NOT.format(self.SIMILAR)
        return self._add(comparitor, None, key, value)

    def add_and_not_similar(self, key, value):
        comparitor = self.NOT.format(self.SIMILAR)
        return self._add(comparitor, self.AND, key, value)

    def add_or_not_similar(self, key, value):
        comparitor = self.NOT.format(self.SIMILAR)
        return self._add(comparitor, self.OR, key, value)

    def add_less_than(self, key, value):
        return self._add(self.LTE, None, key, value)

    def add_and_less_than(self, key, value):
        return self._add(self.LTE, self.AND, key, value)

    def add_or_less_than(self, key, value):
        return self._add(self.LTE, self.OR, key, value)

    def add_not_less_than(self, key, value):
        comparitor = self.NOT.format(self.LTE)
        return self._add(comparitor, None, key, value)

    def add_and_not_less_than(self, key, value):
        comparitor = self.NOT.format(self.LTE)
        return self._add(comparitor, self.AND, key, value)

    def add_or_not_less_than(self, key, value):
        comparitor = self.NOT.format(self.LTE)
        return self._add(comparitor, self.OR, key, value)

    def add_greater_than(self, key, value):
        return self._add(self.GTE, None, key, value)

    def add_and_greater_than(self, key, value):
        return self._add(self.GTE, self.AND, key, value)

    def add_or_greater_than(self, key, value):
        return self._add(self.GTE, self.OR, key, value)

    def add_not_greater_than(self, key, value):
        comparitor = self.NOT.format(self.GTE)
        return self._add(comparitor, None, key, value)

    def add_and_not_greater_than(self, key, value):
        comparitor = self.NOT.format(self.GTE)
        return self._add(comparitor, self.AND, key, value)

    def add_or_not_greater_than(self, key, value):
        comparitor = self.NOT.format(self.GTE)
        return self._add(comparitor, self.OR, key, value)

    def _add(self, comparitor, composer, key, value):
        filter = self._filter
        if not filter:
            tmp = comparitor.format(key, value)
        elif self._in_block(filter, composer):
            tmp = filter[0:len(filter) - 1]
            tmp += comparitor.format(key, value)
            tmp += ')'
        else:
            tmp = '(' + composer
            tmp += filter
            tmp += comparitor.format(key, value)
            tmp += ')'

        self._filter = tmp
        return self

    def _reset(self):
        self._filter = ''

    def _in_block(self, filter, composer):
        return filter[1] == composer

    def build(self):
        return self._filter

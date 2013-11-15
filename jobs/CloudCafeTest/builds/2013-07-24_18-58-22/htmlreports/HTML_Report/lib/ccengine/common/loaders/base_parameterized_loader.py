from ccengine.common.exceptions.configuration import BadTestConfigDataException

from unittest2.suite import TestSuite


class BaseParameterizedLoader(object):
    '''
    Instantiate this class with a data generator object(DataGenerator subclass)
    Then use that instance to add your tests like you add your tests into the suite.
    e.g. data_generator = LavaAPIDataGenerator()
         custom_loader =  BaseParameterizedLoader(data_generator)
         custom_loader.addTest(TestClass("test-1"))
         custom_loader.addTest(TestClass("test-2"))
         custom_loader.addTest(TestClass("test-3"))
         custom_loader.getSuite()
    '''
    def __init__(self, data_provider=None):
        self.data_provider = data_provider
        self.tests = []
        self.data_gens_for_tests = {}

    def addTest(self,
                testcase,
                data_gen=None):
        '''
        Add tests to this loader. This takes a test case object as a parameter
        See e.g. above
        '''
        self.tests.append(testcase)
        if data_gen is not None:
            self.data_gens_for_tests[testcase] = data_gen

    def parameterize_test(self,
                          test,
                          test_record):
        if test_record.keys()[0] in test.__dict__:
            test_to_be_mod = test.__copy__()
        else:
            test_to_be_mod = test
        for key in test_record.keys():
            setattr(test_to_be_mod, key, test_record[key])
        setattr(test_to_be_mod, "test_record", test_record)
        return test_to_be_mod

    def getSuite(self):
        '''
        returns a test suite used by the unittest to run packages.
        load_tests function can return this.
        '''
        if len(self.tests) != 0:
            '''
            Port all the jsons to instance variables of the class
            '''
            suite = TestSuite()
            if self.data_provider is not None:
                for test_record in self.data_provider.generate_test_records():
                    for test in self.tests:
                        if test in self.data_gens_for_tests.keys():
                            method_data_gen = self.data_gens_for_tests[test]
                            for m_test_record in \
                            method_data_gen.generate_test_records():
                                f_test_record = m_test_record.copy()
                                f_test_record.update(test_record)
                                suite.addTest(
                                    self.parameterize_test(test,
                                                           f_test_record))
                        else:
                            suite.addTest(
                                self.parameterize_test(test,
                                                       test_record))
            else:
                for test in self.tests:
                    if test in self.data_gens_for_tests.keys():
                        for test_record in \
                        method_data_gen.generate_test_records():
                            suite.addTest(
                                self.parameterize_test(test, test_record))
                    else:
                        suite.addTest(test)
            return suite
        else:
            raise BadTestConfigDataException(
                "No tests added to the parameterized loader")

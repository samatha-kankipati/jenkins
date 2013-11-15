import math

from ccengine.common.dataset_generators import (
    BaseDatasetGenerator, DatasetGenerator, TestMultiplier)
from ccengine.common.decorators import attr, DataDrivenTestCase, datasource

from testrepo.common.testfixtures.fixtures import BaseTestFixture


class MyDynamicDataGenerator(BaseDatasetGenerator):
    def __init__(self, num_range):
        for num in range(num_range):
            dataset = {"base": num,
                       "sqr": math.pow(num, 2),
                       "sqrt": math.sqrt(num),
                       "aaa": 'aaa',
                       'zzz': 'zzz'}
            self.append_new_dataset(str(num), dataset)


class MyStaticDataGenerator(BaseDatasetGenerator):
    def __init__(self):
        self.append_new_dataset(
            "first_run",
            {"arg1": "first_run_arg1",
             "arg2": "first_run_arg2",
             "arg3": "first_run_arg3"}),

        self.append_new_dataset(
            "second_run",
            {"arg1": "second_run_arg1",
             "arg2": "second_run_arg2",
             "arg3": "second_run_arg3"}),

        self.append_new_dataset(
            "third_run",
            {"arg1": "third_run_arg1",
             "arg2": "third_run_arg2",
             "arg3": "third_run_arg3"})


@DataDrivenTestCase
class MainPMZ_TestCase(BaseTestFixture):

    class_global_data = [
        {"arg1": "first_run_arg1",
         "arg2": "first_run_arg2",
         "arg3": "first_run_arg3"},

        {"arg1": "second_run_arg1",
         "arg2": "second_run_arg2",
         "arg3": "second_run_arg3"},

        {"arg1": "third_run_arg1",
         "arg2": "third_run_arg2",
         "arg3": "third_run_arg3"},
    ]

    dataset_generator = DatasetGenerator(class_global_data)

    # Note that the attribute (tag) decorator works with this and the
    # order it's applied doesn't matter
    @attr('ExampleTest1')
    @datasource(MyDynamicDataGenerator(10))
    def ddtest_dynamic_generator_test(self, base, sqr, sqrt):
        print base, sqr, sqrt

    # Another module-defined generator that doesn't take any input.
    @attr('ExampleTest2')
    @datasource(MyStaticDataGenerator())
    def ddtest_static_generator_test(self, arg1, arg2, arg3):
        print arg1, arg2, arg3

    # Note that class-global generators also work
    @datasource(dataset_generator)
    @attr('ExampleTest3')
    def ddtest_static_generator_test_2(self, arg1, arg2, arg3):
        print arg1, arg2, arg3

    # This test doesn't take any keyword arguments, but can be multipled so
    # that it runs multiple times.
    @datasource(TestMultiplier(10))
    @attr('ExampleTest4')
    def ddtest_multiplier_generator_test(self):
        print __name__

from types import FunctionType
from unittest2 import TestCase


DATA_DRIVEN_TEST_ATTR = "__data_driven_test_data__"
DATA_DRIVEN_TEST_PREFIX = "ddtest_"


class DataDrivenTestCaseError(Exception):
    pass


def attr(*args, **kwargs):
    def decorator(func):
        setattr(func, 'decorated', 1)
        for name in args:
            setattr(func, name, 1)
        func.__dict__.update(kwargs)
        return func
    return decorator


def datasource(datasource=None):
    """Used to define the data source for a parameterized test in a
    parameterized Unittest TestCase class"""

    def decorator(func):
        setattr(func, DATA_DRIVEN_TEST_ATTR, datasource)
        return func
    return decorator


def DataDrivenTestCase(cls):
    """Generates new unittest test methods from methods defined in the
    decorated class"""

    if not issubclass(cls, TestCase):
        raise DataDrivenTestCaseError

    test_case_attrs = dir(cls)
    for attr_name in test_case_attrs:
        if attr_name.startswith(DATA_DRIVEN_TEST_PREFIX) is False:
            # Not a data driven test, skip it
            continue

        original_test = getattr(cls, attr_name, None).__func__
        test_data = getattr(original_test, DATA_DRIVEN_TEST_ATTR, None)

        if test_data is None:
            # no data was provided to the datasource decorator or this is not a
            # data driven test, skip it.
            continue

        for dataset in test_data:
            # Name the new test based on original and dataset names
            base_test_name = str(original_test.__name__)[
                int(len(DATA_DRIVEN_TEST_PREFIX)):]
            new_test_name = "test_{0}_{1}".format(
                base_test_name, dataset.name)

            # Create a new test from the old test
            new_test = FunctionType(
                original_test.func_code, original_test.func_globals,
                name=new_test_name)

            # Copy over any other attributes the original test had (mainly to
            # support test tag decorator)
            for attr in list(set(dir(original_test)) - set(dir(new_test))):
                setattr(new_test, attr, getattr(original_test, attr))

            # Change the new test's default keyword values to the appropriate
            # new data as defined by the datasource decorator
            new_default_values = []
            for arg in list(original_test.func_code.co_varnames)[1:]:
                new_default_values.append(dataset.data[arg])
            setattr(new_test, "func_defaults", tuple(new_default_values))

            # Add the new test to the TestCase
            setattr(cls, new_test_name, new_test)
    return cls

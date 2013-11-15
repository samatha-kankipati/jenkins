import inspect
import itertools
from types import FunctionType
from unittest2 import TestCase

TAGS_DECORATOR_TAG_LIST_NAME = "__test_tags__"
TAGS_DECORATOR_ATTR_DICT_NAME = "__test_attrs__"
DATA_DRIVEN_TEST_ATTR = "__data_driven_test_data__"
DATA_DRIVEN_TEST_PREFIX = "ddtest_"


class DataDrivenFixtureError(Exception):
    pass


def attr(*args, **kwargs):
    def decorator(func):
        setattr(func, 'decorated', 1)
        for name in args:
            setattr(func, name, 1)
        func.__dict__.update(kwargs)
        return func
    return decorator


def data_driven_test(dataset_source=None):
    """Used to define the data source for a data driven test in a
    DataDrivenFixture decorated Unittest TestCase class"""

    def decorator(func):
        setattr(func, DATA_DRIVEN_TEST_ATTR, dataset_source)
        return func
    return decorator


def DataDrivenFixture(cls):
    """Generates new unittest test methods from methods defined in the
    decorated class"""

    if not issubclass(cls, TestCase):
        raise DataDrivenFixtureError

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
            args, _, _, defaults = inspect.getargspec(original_test)
            defaults = defaults or ()

            # Self doesn't have a default, so we need to remove it
            args.remove('self')

            #Make sure we take into account required arguments.  Throw an
            #exception if a required argument was not passed in the dataset.
            required_arg_count = len(args) - len(defaults)
            missing_required_args = []
            for req_arg in args[0:required_arg_count]:
                if req_arg not in dataset.data.keys():
                    missing_required_args.append(req_arg)

            if len(missing_required_args) != 0:
                verb = "are" if len(missing_required_args) > 1 else "is"
                raise TypeError(
                    "{missing_args} {verb} required by {original_test_name}, "
                    "but not found in the provided dataset".format(
                        missing_args=missing_required_args, verb=verb,
                        original_test_name=str(original_test.__name__)))

            kwargs = dict(itertools.izip_longest(
                args[::-1], list(defaults)[::-1], fillvalue=None))

            kwargs.update(dataset.data)

            # Make sure the updated values are in the correct order
            new_default_values = [kwargs[arg] for arg in args]
            setattr(new_test, "func_defaults", tuple(new_default_values))

            # Add the new test to the TestCase
            setattr(cls, new_test_name, new_test)
    return cls


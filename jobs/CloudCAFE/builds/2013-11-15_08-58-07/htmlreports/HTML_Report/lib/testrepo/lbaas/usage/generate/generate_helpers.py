from testrepo.lbaas.usage import UsageKeys
import inspect


def function_name():
    return inspect.stack()[1][3]


def write_usage_data(data, filename):
    with open('/'.join([UsageKeys.USAGE_DATA_PATH, filename]),
              'wb') as configfile:
        data.write(configfile)

import os
import string
import copy
import random
import collections
from hashlib import md5
from uuid import uuid4
from datetime import datetime, timedelta
import time

from ccengine.common.tools.equality_tools import EqualityTools


CLOUDCAFE_DATA_DIRECTORY = os.getenv('CLOUDCAFE_DATA_DIRECTORY') or None
CLOUDCAFE_TEMP_DIRECTORY = '/tmp'


'''
    IEC Standard definitions for binary bytes (those expressed as multiples of
    powers of two) starting with 1024 bytes (2^10).
'''
KiB = 2 ** 10
MiB = KiB ** 2
GiB = KiB ** 3
TiB = KiB ** 4


'''
    SI Standard definitions for decimal bytes (those expressed as multiples of
    powers of ten) starting with 1000 bytes (10^3).
'''
KB = 10 ** 3
MB = KB ** 2
GB = KB ** 3
TB = KB ** 4


def create_datafile(size, path=None, name=None, data_source=None,
                    block_write_size=None):
    '''
        Creates a file at <path>/<random_uuid> of <size> bytes
        returns a python filehandle object or None on error.

        default path is /tmp
        default name is a uuid as returned by uuid.uuid4()
        data_source should be a function, and defaults to random ascii
        printable characters.
        Default block_write_size is 65536 bytes.
    '''
    default_random_source = lambda count: [random.choice(string.printable) for
                                           num in range(count)]

    path = path or '/tmp'
    name = name or str(uuid4())
    data_source = data_source or default_random_source
    block_write_size = block_write_size or (2 ** 10) * 64

    #if not os.path.exists(path):
    #    os.path.create
    #    with open(path, 'w+') as f:
    #        for i in range(size_bytes):
    #                f.write(os.urandom(512))
    #                #[random.choice(string.printable) for num in range(10)]


def get_datastring(num_bytes):
    pass


def get_md5_hash(data, block_size_multiplier=1):
    """
    returns an md5 sum. data is a string or file pointer.
    block size is 512 (md5 msg length).
    """

    default_block_size = 2 ** 9
    blocksize = block_size_multiplier * default_block_size

    hash = None
    if type(data) is file:
        while True:
            read_data = data.read(blocksize)
            if not read_data:
                break
            md5.update(read_data)
        data.close()
    else:
        md5.update(str(data))
    hash = md5.hexdigest()
    return hash


def string_to_datetime(datetimestring):
    dateformats = ['%Y-%m-%d %H:%M:%S', '%Y-%m-%d %H:%M:%S.%f',
                   '%Y-%m-%dT%H:%M:%S.%fZ', '%Y-%m-%dT%H:%M:%S.%f',
                   "%Y-%m-%dT%H:%M:%SZ", '%Y-%m-%dT%H:%M:%S.000+0000']
    for dateformat in dateformats:
        try:
            return datetime.strptime(datetimestring, dateformat)
        except ValueError:
            continue
    else:
        raise


def are_datetimestrings_equal(datetimestring1, datetimestring2, leeway=0):
    return \
        EqualityTools.are_datetimes_equal(string_to_datetime(datetimestring1),
                                          string_to_datetime(datetimestring2),
                                          timedelta(seconds=leeway))


def convert_unicode_to_str(data):
    """Converts unicode to str, manages list and dict data types"""
    if isinstance(data, unicode):
        return str(data)
    elif isinstance(data, str):
        return data
    elif isinstance(data, collections.Mapping):
        return dict(map(convert_unicode_to_str, data.iteritems()))
    elif isinstance(data, collections.Iterable):
        return type(data)(map(convert_unicode_to_str, data))
    else:
        return data


def replace_response_value(data, old_value, new_value):
    """Replaces values in a json response with a key value
    where the value can be a list of dicts or one dict"""
    # data is the json response content
    new_data = copy.deepcopy(data)
    for name, datalist in new_data.iteritems():
        # if the dict value of the json response is a list of dicts
        if isinstance(datalist, list):
            for datadict in datalist:
                for key, value in datadict.iteritems():
                    if value == old_value:
                        datadict[key] = new_value
        # if datalist is a single dict
        else:
            datadict = datalist
            for key, value in datadict.iteritems():
                if value == old_value:
                    datadict[key] = new_value
    return new_data


def replace_response_key(data, old_key, new_key):
    """Replaces key names in a json response with a key value
    where the value can be a list of dicts or one dict"""
    # data is the json response content
    new_data = copy.deepcopy(data)
    for name, datalist in new_data.iteritems():
        # if the dict value of the json response is a list of dicts
        if isinstance(datalist, list):
            for datadict in datalist:
                if old_key in datadict:
                    value = datadict[old_key]
                    datadict[new_key] = value
                    del datadict[old_key]
        # if datalist is a single dict
        else:
            datadict = datalist
            if old_key in datadict:
                value = datadict[old_key]
                datadict[new_key] = value
                del datadict[old_key]
    return new_data


def convert_date_from_cst_to_utc_date(datetime_str, date_format=None):
    converted_date = string_to_datetime(datetime_str)

    dst_date = datetime(year=converted_date.year, month=3, day=10,
                        hour=00, minute=00, second=00)
    if converted_date.year > 2007:
        dst_end_date = dst_date + timedelta(weeks=34)
    else:
        dst_end_date = dst_date + timedelta(weeks=30)

    if dst_date < converted_date < dst_end_date:
        os.environ['TZ'] = 'Etc/CST5'
    else:
        os.environ['TZ'] = 'Etc/CST6'

    time.tzset()
    if date_format is None:
        converted_date = time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime(
            time.mktime(converted_date.timetuple())))

    else:
        converted_date = time.strftime(date_format, time.gmtime(time.mktime(
            converted_date.timetuple())))

    return converted_date


def bytes_to_gb(val):
    return float(val) / 1073741824


def gb_to_bytes(val):
    return int(val * 1073741824)


def bytes_to_mb(val):
    return float(val) / 1024

def nested_getattr(obj, attr, default=None):
    '''
        @summary: returns value of a nested object. Eg: obj1.obj2.obj3
        @param name: attr
        @param desc: the nested/normal attribute of a class
        @param type: String
        @param name: default
        @param desc: default return
        @param type: String
    '''
    attributes = attr.split(".")
    for attribute in attributes:
        try:
            obj = getattr(obj, attribute)
        except AttributeError:
            if default:
                return default
            else:
                raise
    return obj


def merge_dicts(dict1, dict2):
    '''
    @summary: Returns a merge of 2 dicts of dicts
    @param dict1: dictionary
        e.g., dict1 = {'a': {1: 2}, 'b': {3: 4}}
    @type dict1: dict
    @param dict2: dictionary
        e.g., dict2 = {'a': {5: 6}}
    @type dict2: string
    @returns: merged dict as
        {'a': {1: 2, 5: 6}, 'b': {3: 4}}
    '''
    def _merge_dicts_generator(dict1, dict2):
        for k in set(dict1.keys()).union(dict2.keys()):
            if k in dict1 and k in dict2:
                yield (k, dict(_merge_dicts_generator(dict1[k], dict2[k])))
            elif k in dict1:
                yield (k, dict1[k])
            else:
                yield (k, dict2[k])
    return dict(_merge_dicts_generator(dict1, dict2))

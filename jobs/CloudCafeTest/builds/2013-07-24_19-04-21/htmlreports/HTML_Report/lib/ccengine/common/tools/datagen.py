import hashlib
import os
from uuid import uuid4
import random
from math import pow
import time
from exceptions import Exception

SOURCE_RANDOM = '/dev/urandom'
SOURCE_ZEROS = '/dev/zero'
TEMP_LOCATION = '/tmp'

#Binary prefixes
#IEE_MAGNITUDE = int(pow(2,10))
EXACT_BYTE = 8
EXACT_KIBIBYTE = int(pow(2,10))
EXACT_MEBIBYTE = int(pow(2,20))
EXACT_GIBIBYTE = int(pow(2,30))
EXACT_TEBIBYTE = int(pow(2,40))

#Decimal prefixes
#SI_MAGNITURE = int(pow(10,3))

EXACT_KILOBYTE = int(pow(10,3))
EXACT_MEGABYTE = int(pow(10,6))
EXACT_GIGABYTE = int(pow(10,9))
EXACT_TERABYTE = int(pow(10,12))

class UnsupportedDataGenTypeError(Exception):
    pass

#def generate_data_dict(size_in_bytes, chunksize=EXACT_KIBIBYTE, source=SOURCE_RANDOM):
#    '''
#    generates data based on source type. (yields a generator)
#    Default source type is random.  Also supports zeros (SOURCE_ZEROS)
#    '''
#    if (source != SOURCE_RANDOM) and (source != SOURCE_ZEROS):
#        raise UnsupportedDataGenTypeError
#
#    #Calculate chunks, chunksize and modulo
#    modulo = size_in_bytes % chunksize
#    if modulo == size_in_bytes:
#        chunksize = size_in_bytes
#        modulo = 0
#    total_chunks = size_in_bytes / chunksize
#
#    #open random data source
#    try:
#        fh = open(SOURCE_RANDOM, 'r')
#    except:
#        print 'Unable to open random data source'
#        raise
#
#    while True:
#        if total_chunks <= 0:
#            break
#
#        total_chunks -= 1
#        yield str(fh.read(chunksize))
#
#    if modulo > 0:
        #yield str(fh.read(modulo))



def timestamp_string(prefix=None, suffix=None, decimal_precision=6):
    '''
        Return a unix timestamp surrounded by any defined prefixes and suffixes
        Decimal precision is full (6) by default.
    '''
    t = str('%f' % time.time())
    int_seconds, dec_seconds = t.split('.')
    for x in range(6 - decimal_precision):
        dec_seconds=dec_seconds[:-1]

    int_seconds = str(int_seconds)
    dec_seconds = str(dec_seconds)
    prefix = prefix or ''
    suffix = suffix or ''
    final = None
    if len(dec_seconds) > 0:
        final = '%s%s%s' % ( prefix, int_seconds, suffix)
    else:
        final = '%s%s.%s%s' % ( prefix, int_seconds, dec_seconds, suffix)

    return final


def random_string(prefix=None, suffix=None, size=8):
    '''
        Return exactly size bytes worth of base_text as a string
        surrounded by any defined pre or suf-fixes
    '''

    base_text = str(uuid4()).replace('-','0')

    if size <= 0:
        return '%s%s' % (prefix, suffix)

    extra = size % len(base_text)
    body = ''

    if extra == 0:
        body = base_text * size

    if extra == size:
        body = base_text[:size]

    if (extra > 0) and (extra < size):
        body = (size / len(base_text)) * base_text + base_text[:extra]

    body = str(prefix) + str(body) if prefix is not None else body
    body = str(body) + str(suffix) if suffix is not None else body
    return body

def random_ip(pattern=None):
    '''Takes a pattern as a string in the format of #.#.#.# where a # is an
    integer, and a can be substituded with an * to produce a random octet.
    pattern = 127.0.0.* would return a random string between 127.0.0.1 and
    127.0.0.254'''
    if pattern is None:
        pattern = '*.*.*.*'
    num_asterisks = 0
    for c in pattern:
        if c == '*':
            num_asterisks += 1
    rand_list = [random.randint(1, 255) for i in range(0, num_asterisks)]
    for item in rand_list:
        pattern = pattern.replace('*', str(item), 1)
    return pattern

def random_cidr(ip_pattern=None, mask=None, min_mask=0, max_mask=30):
    '''Gets a random cidr using the random_ip function in this module. If mask
    is None then a random mask between 0 and 30 inclusive will be assigned.'''
    if mask is None:
        mask = random.randint(min_mask, max_mask)
    ip = random_ip(ip_pattern)
    return ''.join([ip, '/', str(mask)])

def random_int(min_int, max_int):
    return random.randint(min_int, max_int)

def rand_name(name='test'):
    return name + str(random.randint(99999, 1000000))

def random_item_in_list(selection_list):
    return random.choice(selection_list)

def bytes_to_gb(val):
    return float(val) / 1073741824

def gb_to_bytes(val):
    return int(val * 1073741824)

def bytes_to_mb(val):
    return float(val) / 1024

#def exact_string(scalar, magnitude):
#    pass
#
#class Filegen(object):
#
#    def __init__(path_to_folder=None, source=None):
#        self.folder = path_to_folder or '/tmp'
#        self._source = RANDOM_SOURCE
#
#    def exactly(size_in_bytes):
#        pass
#
#    def _exec_dd(self, datasource, filepath, block_size, multiplier):
#        #Create the dd command to be executed
#        dd_command = "dd if=" + str(data_source) + " of="+ str(testfile_path)\
#                     + " bs=" + str(block_size) + " count=" + str(dd_multiplier)
#
#        #print "Creating File: %s"%(testfile_path)
#        #print "dd command: %s"%(dd_command)
#
#        subprocess_call(dd_command, shell=True)
#
#        #Check if the path exists
#        try:
#            if os.path.exists(testfile_path):
#                _dd_complete = True
#        except:
#            return None
#            print "Error creating test file"
#
#
#    def generate_random_file(**kwargs):
#        """
#            If no arguments are specified, will return a path to a randomized file
#            1024 bytes in size, named '1_kibibyte_of_randomness'
#
#            Keyword Arguments:
#            'format' = ['absolute_path', 'file_handle']
#                Default: 'absolute_path'
#                Returns the file in the format specified.
#                binary_blob will return a utf-8 encoded string.
#
#            'scalar_size' = [Integer]
#                Default: 1
#                Sets file size to 'scalar_size' multiplied by values
#                dictated by the 'unit' and 'multiplier' arguments.
#                Ex:  if unit = byte, multiplier = 'kilo', and size = 8,
#                     then a file of size 1024 * 8 (8096) bytes will be returned.
#                Note:  If 'exact' is chosen for the multiplier, the filesize if
#                       set to 'scalar_size' amount of bytes.
#
#            'multiplier' = ['exact-bytes', 'kilo', 'mega', 'giga', 'kibi', 'mibi', 'gibi']
#                Default: 'kilo'
#                Sets randomized file size to 'multiplier' multiplied by values
#                dictated by the 'scalar_size' and 'unit' arguments.
#                If multipier='exact-bytes', final file size is dictated by the scalar_size
#                in bytes. (exact bits isn't supported)
#
#            'unit' = ['bit', 'byte']
#                Default: 'byte'
#                Sets file size to either 1 or 8 (bit vs byte) multiplied
#                by values dictated by the 'scalar_size' and 'multiplier' arguments.
#                Note:  If exact is chosen as the multipler, this value is ignored.
#
#            'content' = ['randomness', 'zeros', <arbitrary_string>]
#                Default: 'randomness'
#                Generates a files with contents set to either randomness binary data or
#                all zeros.
#                If an arbitrary string is provided, creates a file who's contents
#                are this arbitrary string repeated 'scalar_size' times
#                (the multiplier and unit arguments are ignored)
#
#            'specific_file' = (name of file in default test_file folder)
#                If specified, will search for a file in the test_files directory
#                who's name matches the arbitrary_string exactly.
#                This is mostly a convenience function to help in accessing
#                files that cannot be generated on the fly.
#                Note: If called, ignores all other arguments
#
#            'special_function' = ['force_duplicate','force_overwrite', 'md5_name']
#                Default: None
#
#                if 'force_duplicate'
#                Creates a file regardless of whether another of the same
#                size exists, and appends a timestamp to the end of the filename.
#                UNIMPLEMENTED
#
#                if 'force_overwrite'
#                Creates a file regardless of whether another of the same
#                size exists by overwriting the currently present file.
#                UNIMPLEMENTED
#
#                if 'md5_name'
#                Creates a file regardless of whether another of the same
#                size exists by naming it based on it's md5 hash.
#                If a file of the same hash already exists, that file is returned
#                instead.ZL
#                UNIMPLEMENTED
#
#            pluto_is_a_planet_mode = [Boolean]
#                Default: False
#                If True, assumes binary definitions for 'kilo', 'giga', and 'kibi'
#                multipliers (making them aliases for 'kibi', 'mibi', and 'gigi'),
#                and disables the creation of decimal-base sized files.
#                (ie, if enabled, kilo=1024, if disabled, kilo=1000)
#                (Note:  The name is long because this is a rediculous option
#                        to enable.  Pluto's not a planet anymore, and Kilo = 1000)
#        """
#
#        valid_args = {'format':['absolute_path', 'file_handle'],
#                      'scalar_size':'int',
#                      'multiplier':['exact-bytes', 'kilo', 'mega', 'giga', 'kibi', 'mibi',
#                                    'gibi'],
#                      'unit':['bit', 'byte'],
#                      'content':['randomness', 'zeros'],
#                      'specific_file':'str',
#                      'special_function':['specific_file', 'force_duplicate',
#                                          'force_overwrite', 'md5_name'],
#                      'pluto_is_a_planet_mode':'bool',
#                      }
#
#
#        #verify all args
#        for arg in kwargs:
#            if arg not in valid_args:
#                raise TypeError( str(arg) + ' is not a valid argument for get_testfile')
#                return
#
#        #set defaults
#        if 'format' not in kwargs:
#            kwargs['format'] = 'absolute_path'
#
#        if 'multiplier' not in kwargs:
#            kwargs['multiplier'] = 'kibi'
#
#        if 'unit' not in kwargs:
#            kwargs['unit'] = 'byte'
#
#        if 'scalar_size' not in kwargs:
#            if 'content' not in kwargs:
#                kwargs['scalar_size'] = 1
#            else:
#                kwargs['scalar_size'] = 1
#                #Special case to trip exception later on
#                pass
#
#        if 'content' not in kwargs:
#            kwargs['content'] = 'randomness'
#
#        if 'pluto_is_a_planet_mode' not in kwargs:
#            kwargs['pluto_is_a_planet_mode'] = False
#
#        #Special case for 'specific_file'
#        if 'specific_file' in kwargs:
#            if type(kwargs['specific_file']).__name__ == valid_args['specific_file']:
#                #Check if specific file exists
#                folder = os.path.expanduser(CONSTS.DEFAULT_UPLOADS_FOLDER)
#                filepath = os.path.join(folder, str(kwargs['specific_file']))
#                try:
#                    if os.path.exists(filepath):
#                        return filepath
#                    else:
#                        return None
#                except:
#                    sys.stderr.write("\nUnable to find specified file\n")
#                    return None
#            else:
#                sys.stderr.write("\nSpecific File: Invalid Type Specified\n")
#                return None
#
#
#        #Special-Case code for arbitrary string filled File
#        if 'content' in kwargs:
#            if kwargs['content'] not in valid_args['content']:
#                if type(kwargs['content']).__name__ != 'str':
#                    raise TypeError( str(kwargs['content'])
#                                    + ' is invalid data for the \'content\' argument' )
#                    return None
#
#                #Arbitrary String request verified
#                #check to makes sure the size argument is also present
#                if 'scalar_size' not in kwargs:
#                    raise TypeError('File filled with arbitrary string was called, but the scalar_size argument was not defined')
#                    return None
#
#                if type(kwargs['scalar_size']).__name__ != 'int':
#                    raise TypeError('scalar_size argument was passed a non-integer value')
#                    return None
#
#                #scalar_size verifed, create arbitrary string file
#                #IMPLEMENT ARBITRARY STRING FILLED FILE HERE
#                raise TypeError('ARBITRARY STRING FILLED FILE NOT IMPLEMENTED YET :D')
#                return None
#                pass
#
#        #Set data_source for non-arbitrary-string call
#        data_source = None
#        ctype = kwargs['content']
#        if ctype == 'randomness':
#            data_source = '/dev/urandom'
#        elif ctype == 'zeros':
#            data_source = '/dev/zero'
#
#        #Init
#        file_size = 0
#        dd_multiplier = 1
#
#        #flags for skipping parts of the file creation process
#        _dd_complete = False
#        _run_dd = False
#        _md5_name = False
#
#        #Set Scalar size
#        #Forces int-ness for scalar_size.
#        #I might want to add some kind of non string, non int check here
#        #TODO:  Need to put check to raise error if float
#        scalar_size = int(kwargs['scalar_size'])
#
#        #Set unit size based on if it's a bit or byte count
#        data_unit_size = 1
#        if kwargs['unit'] == 'bit':
#            data_unit_size = 8
#
#        #set testfile_folderpath
#        testfile_folderpath = os.path.expanduser(CONSTS.DEFAULT_UPLOADS_FOLDER)
#        testfile_name = str(kwargs['scalar_size']) + "_" + str(kwargs['multiplier']) + str(kwargs['unit'])
#
#        #proper gramars r importants
#        if kwargs['scalar_size'] != 1:
#            testfile_name = testfile_name + "s"
#
#        #Append data content type to name
#        testfile_name = testfile_name + "_of_" + str(kwargs['content'])
#
#        #Final Total Path
#        testfile_path = os.path.join(testfile_folderpath, testfile_name)
#
#
#        mult = kwargs['multiplier']
#        if mult == 'exact-bytes':
#            data_unit_size = 1
#            if scalar_size == 0:
#                #write a zero-byte file, and return it
#                _run_dd = False
#                _dd_complete = True
#                testfile_path = os.path.join(testfile_folderpath, '0_bytes')
#                try:
#                    with io.open(testfile_path, 'wb') as file:
#                        file.truncate(0)
#                except:
#                    pass
#                finally:
#                    return testfile_path
#
#            else:
#                file_size = scalar_size
#                data_unit_size = 1
#                dd_multiplier = 1
#
#        if mult == 'kibi':
#            dd_multiplier = KIBI_POW
#            file_size = (dd_multiplier * scalar_size) / data_unit_size
#
#        if mult == 'mibi':
#            dd_multiplier = MIBI_POW
#            file_size = (dd_multiplier * scalar_size) / data_unit_size
#
#        if mult == 'gibi':
#            file_size = (GIBI_POW * scalar_size) / data_unit_size
#            dd_multiplier = 64
#
#        if mult == 'kilo':
#            dd_multiplier = KILO_POW
#            if kwargs['pluto_is_a_planet_mode'] == 'True':
#                dd_multiplier = KIBI_POW
#            file_size = (dd_multiplier * scalar_size) / data_unit_size
#
#        if mult == 'mega':
#            dd_multiplier = MEGA_POW
#            if kwargs['pluto_is_a_planet_mode'] == 'True':
#                dd_multiplier = MIBI_POW
#            file_size = (dd_multiplier * scalar_size) / data_unit_size
#
#        if mult == 'giga':
#            giga_mult = GIGA_POW
#            dd_multiplier = 100
#            if kwargs['pluto_is_a_planet_mode'] == 'True':
#                giga_mult = GIBI_POW
#                dd_multiplier = 64
#            file_size = (giga_mult * scalar_size) / data_unit_size
#
#        #Set block size for dd
#        block_size = file_size / dd_multiplier
#
#        #Decide to create a new file, overwrite an existing file, or create
#        #a duplicate
#        try:
#            if os.path.exists(testfile_path):
#                _run_dd = False
#            else:
#                _run_dd = True
#        except:
#            _run_dd = True
#
#        if 'special_function' in kwargs:
#            if kwargs['special_function'] == 'force_duplicate':
#                _run_dd == True
#                tname = get_unique_filename(search_type = 'dir',
#                                          search_location = testfile_folderpath,
#                                          base_string = testfile_name)
#
#                if tname is not None:
#                    testfile_name = tname
#                else:
#                    sys.stderr.write("Could not force duplicate, unique name"
#                                     + " could not be generated\n")
#                    return None
#
#            elif kwargs['special_function'] == 'force_overwrite':
#                _run_dd == True
#
#            elif kwargs['special_function'] == 'md5_name':
#                _md5_name = True
#
#        if _run_dd == True:
#
#            #Create the dd command to be executed
#            dd_command = "dd if=" + str(data_source) + " of="+ str(testfile_path)\
#                         + " bs=" + str(block_size) + " count=" + str(dd_multiplier)
#
#            #print "Creating File: %s"%(testfile_path)
#            #print "dd command: %s"%(dd_command)
#
#            subprocess_call(dd_command, shell=True)
#
#            #Check if the path exists
#            try:
#                if os.path.exists(testfile_path):
#                    _dd_complete = True
#            except:
#                return None
#                print "Error creating test file"
#        else:
#            #Return the file path
#            return testfile_path
#
#        #Check to see if the file already exists
#        if _dd_complete == True:
#            if _md5_name == True:
#                fhash = get_md5_hash(testfile_path)
#                #Rename file with md5 hash
#                try:
#                    os.rename(testfile_path, str(os.path.join(testfile_folderpath, fhash)))
#                except IOError:
#                    print "Unable to rename file to md5 hash"
#                    return None
#            elif kwargs['format'] == 'file_handle':
#                fh = open(testfile_path, 'r')
#                return fh
#            else:
#                return testfile_path
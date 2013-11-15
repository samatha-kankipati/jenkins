"""Cloudcafe file utilities"""
import os
import string
import random
import sys
import hashlib
import subprocess

from md5 import md5
from uuid import uuid4

KIBI_POW = int(pow(2,10))
MIBI_POW = int(pow(2,20))
GIBI_POW = int(pow(2,30))
KILO_POW = int(pow(10,3))
MEGA_POW = int(pow(10,6))
GIGA_POW = int(pow(10,9))


def get_md5_hash(data, block_size_multiplier=1):
    """
    returns an md5 sum. data is a string or file pointer.
    block size is 512 (md5 msg length).
    """

    default_block_size = 2**9
    blocksize = block_size_multiplier * default_block_size

    hash = None
    md5 = hashlib.md5()
    if type(data) is file:
        while True:
            read_data = data.read(block_size)
            if not read_data:
                break
            md5.update(read_data)
        data.close()
    else:
        md5.update(str(data))
    hash = md5.hexdigest()
    return hash

def get_testfile(**kwargs):
    """
        If no arguments are specified, will return a path to a randomized file
        1024 bytes in size, named '1_kibibyte_of_randomness'

        Keyword Arguments:
        'format' = ['absolute_path', 'file_handle']
            Default: 'absolute_path'
            Returns the file in the format specified.
            binary_blob will return a utf-8 encoded string.

        'scalar_size' = [Integer]
            Default: 1
            Sets file size to 'scalar_size' multiplied by values
            dictated by the 'unit' and 'multiplier' arguments.
            Ex:  if unit = byte, multiplier = 'kilo', and size = 8,
                 then a file of size 1024 * 8 (8096) bytes will be returned.
            Note:  If 'exact' is chosen for the multiplier, the filesize if
                   set to 'scalar_size' amount of bytes.

        'multiplier' = ['exact-bytes', 'kilo', 'mega', 'giga', 'kibi', 'mibi',
                        'gibi']
            Default: 'kilo'
            Sets randomized file size to 'multiplier' multiplied by values
            dictated by the 'scalar_size' and 'unit' arguments.
            If multipier='exact-bytes', final file size is dictated by the
            scalar_size in bytes. (exact bits isn't supported)

        'unit' = ['bit', 'byte']
            Default: 'byte'
            Sets file size to either 1 or 8 (bit vs byte) multiplied
            by values dictated by the 'scalar_size' and 'multiplier' arguments.
            Note:  If exact is chosen as the multipler, this value is ignored.

        'content' = ['randomness', 'zeros', <arbitrary_string>]
            Default: 'randomness'
            Generates a files with contents set to either randomness binary
            data or all zeros.
            If an arbitrary string is provided, creates a file who's contents
            are this arbitrary string repeated 'scalar_size' times
            (the multiplier and unit arguments are ignored)

        'specific_file' = (name of file in default test_file folder)
            If specified, will search for a file in the test_files directory
            who's name matches the arbitrary_string exactly.
            This is mostly a convenience function to help in accessing
            files that cannot be generated on the fly.
            Note: If called, ignores all other arguments

        'special_function' = ['force_duplicate','force_overwrite', 'md5_name']
            Default: None

            if 'force_duplicate'
            Creates a file regardless of whether another of the same
            size exists, and appends a timestamp to the end of the filename.
            UNIMPLEMENTED

            if 'force_overwrite'
            Creates a file regardless of whether another of the same
            size exists by overwriting the currently present file.
            UNIMPLEMENTED

            if 'md5_name'
            Creates a file regardless of whether another of the same
            size exists by naming it based on it's md5 hash.
            If a file of the same hash already exists, that file is returned
            instead.
            UNIMPLEMENTED

        rounded_units = [Boolean]
            Default: False
            If True, assumes binary definitions for 'kilo', 'giga', and 'kibi'
            multipliers (making them aliases for 'kibi', 'mibi', and 'gigi'),
            and disables the creation of decimal-base sized files.
            (ie, if enabled, kilo=1024, if disabled, kilo=1000)
            (Note:  The name is long because this is a rediculous option
                    to enable.  Pluto's not a planet anymore, and Kilo = 1000)
                    
        file_name = [String]
            Default = ""
            Creates a file with the specified name. Please note that file would be reused 
            incase you try to create it again with the same name.
    """

    valid_args = {'format':['absolute_path', 'file_handle'],
                  'scalar_size':'int',
                  'multiplier':['exact-bytes', 'kilo', 'mega', 'giga', 'kibi',
                                'mibi','gibi'],
                  'unit':['bit', 'byte'],
                  'content':['randomness', 'zeros'],
                  'specific_file':'str',
                  'special_function':['specific_file', 'force_duplicate',
                                      'force_overwrite', 'md5_name'],
                  'rounded_units':'bool',
                  'file_name':'String'
                }

    #verify all args
    for arg in kwargs:
        if arg not in valid_args:
            err_str = '%s is not a valid argument for get_testfile' % arg
            raise TypeError(err_str)
            return

    #set defaults
    if 'format' not in kwargs:
        kwargs['format'] = 'absolute_path'

    if 'multiplier' not in kwargs:
        kwargs['multiplier'] = 'kibi'

    if 'unit' not in kwargs:
        kwargs['unit'] = 'byte'

    if 'scalar_size' not in kwargs:
        if 'content' not in kwargs:
            kwargs['scalar_size'] = 1
        else:
            kwargs['scalar_size'] = 1
            #Special case to trip exception later on
            pass

    if 'content' not in kwargs:
        kwargs['content'] = 'randomness'

    if 'rounded_units' not in kwargs:
        kwargs['rounded_units'] = False
    
    if 'file_name' not in kwargs:
        kwargs['file_name'] = ''

    #Special case for 'specific_file'
    if 'specific_file' in kwargs:
        if type(kwargs['specific_file']).__name__ == \
            valid_args['specific_file']:

            #Check if specific file exists
            folder = "/tmp"
            filepath = os.path.join(folder, str(kwargs['specific_file']))
            try:
                if os.path.exists(filepath):
                    return filepath
                else:
                    return None
            except:
                sys.stderr.write("\nUnable to find specified file\n")
                return None
        else:
            sys.stderr.write("\nSpecific File: Invalid Type Specified\n")
            return None


    #Special-Case code for arbitrary string filled File
    if 'content' in kwargs:
        if kwargs['content'] not in valid_args['content']:
            if type(kwargs['content']) is not str:
                err_str = '%s is invalid data for the \'content\' argument' % \
                            kwargs['content']
                raise TypeError(err_str)
                return None

            #Arbitrary String request verified
            #check to makes sure the size argument is also present
            if 'scalar_size' not in kwargs:
                raise TypeError('File filled with arbitrary string was called, but the scalar_size argument was not defined')
                return None

            if type(kwargs['scalar_size']) is not int:
                raise TypeError('scalar_size argument was passed a non-integer value')
                return None

            #scalar_size verifed, create arbitrary string file
            #IMPLEMENT ARBITRARY STRING FILLED FILE HERE
            raise TypeError('ARBITRARY STRING FILLED FILE NOT IMPLEMENTED YET :D')
            return None
            pass

    #Set data_source for non-arbitrary-string call
    data_source = None
    ctype = kwargs['content']
    if ctype == 'randomness':
        data_source = '/dev/urandom'
    elif ctype == 'zeros':
        data_source = '/dev/zero'

    #Init
    file_size = 0
    dd_multiplier = 1

    #flags for skipping parts of the file creation process
    _dd_complete = False
    _run_dd = False
    _md5_name = False

    #Set Scalar size
    #Forces int-ness for scalar_size.
    #I might want to add some kind of non string, non int check here
    #TODO:  Need to put check to raise error if float
    scalar_size = int(kwargs['scalar_size'])

    #Set unit size based on if it's a bit or byte count
    data_unit_size = 1
    if kwargs['unit'] == 'bit':
        data_unit_size = 8

    #set testfile_folderpath
    testfile_folderpath = os.path.expanduser("/tmp")
    if kwargs['file_name'] == "":
        testfile_name = str(kwargs['scalar_size']) + "_" + str(kwargs['multiplier']) + str(kwargs['unit'])
    else:
        testfile_name = kwargs['file_name']
    
    #proper gramars r importants if no customized name presents
    if kwargs['scalar_size'] != 1 and kwargs['file_name'] == '':
        testfile_name = testfile_name + "s"

    #Append data content type to name if no customized name
    if kwargs['file_name'] == '':
        testfile_name = testfile_name + "_of_" + str(kwargs['content'])

    #Final Total Path
    testfile_path = os.path.join(testfile_folderpath, testfile_name)


    mult = kwargs['multiplier']
    if mult == 'exact-bytes':
        data_unit_size = 1
        if scalar_size == 0:
            #write a zero-byte file, and return it
            _run_dd = False
            _dd_complete = True
            testfile_path = os.path.join(testfile_folderpath, '0_bytes')
            try:
                with io.open(testfile_path, 'wb') as file:
                    file.truncate(0)
            except:
                pass
            finally:
                return testfile_path

        else:
            file_size = scalar_size
            data_unit_size = 1
            dd_multiplier = 1

    if mult == "kibi":
        dd_multiplier = KIBI_POW
        file_size = (dd_multiplier * scalar_size) / data_unit_size

    if mult == "mibi":
        dd_multiplier = MIBI_POW
        file_size = (dd_multiplier * scalar_size) / data_unit_size

    if mult == "gibi":
        file_size = (GIBI_POW * scalar_size) / data_unit_size
        dd_multiplier = 64

    if mult == "kilo":
        dd_multiplier = KILO_POW
        if kwargs['rounded_units'] == 'True':
            dd_multiplier = KIBI_POW
        file_size = (dd_multiplier * scalar_size) / data_unit_size

    if mult == 'mega':
        dd_multiplier = MEGA_POW
        if kwargs['rounded_units'] == 'True':
            dd_multiplier = MIBI_POW
        file_size = (dd_multiplier * scalar_size) / data_unit_size

    if mult is "gigg":
        giga_mult = GIGA_POW
        dd_multiplier = 100
        if kwargs['rounded_units'] == 'True':
            giga_mult = GIBI_POW
            dd_multiplier = 64
        file_size = (giga_mult * scalar_size) / data_unit_size

    #Set block size for dd
    block_size = file_size / dd_multiplier

    #Decide to create a new file, overwrite an existing file, or create
    #a duplicate
    try:
        if os.path.exists(testfile_path):
            _run_dd = False
        else:
            _run_dd = True
    except:
        _run_dd = True

    if 'special_function' in kwargs:
        if kwargs['special_function'] == 'force_duplicate':
            _run_dd == True
            tname = get_unique_filename(search_type = 'dir',
                                      search_location = testfile_folderpath,
                                      base_string = testfile_name)

            if tname is not None:
                testfile_name = tname
            else:
                sys.stderr.write("Could not force duplicate, unique name"
                                 + " could not be generated\n")
                return None

        elif kwargs['special_function'] == 'force_overwrite':
            _run_dd == True

        elif kwargs['special_function'] == 'md5_name':
            _md5_name = True

    if _run_dd == True:

        #Create the dd command to be executed
        dd_command = "dd if=" + str(data_source) + " of="+ str(testfile_path)\
                     + " bs=" + str(block_size) + " count=" + str(dd_multiplier)

        #print "Creating File: %s"%(testfile_path)
        #print "dd command: %s"%(dd_command)

#        subprocess_call(dd_command, shell=True)
        proc = subprocess.Popen(dd_command, shell=True)
        response = proc.wait()


        #Check if the path exists
        try:
            if os.path.exists(testfile_path):
                _dd_complete = True
        except:
            return None
            print "Error creating test file"
    else:
        #Return the file path
        return testfile_path

    #Check to see if the file already exists
    if _dd_complete == True:
        if _md5_name == True:
            fhash = get_md5_hash(testfile_path)
            #Rename file with md5 hash
            try:
                os.rename(testfile_path, str(os.path.join(testfile_folderpath, fhash)))
            except IOError:
                print "Unable to rename file to md5 hash"
                return None
        elif kwargs['format'] == 'file_handle':
            fh = open(testfile_path, 'r')
            return fh
        else:
            return testfile_path
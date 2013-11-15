import logging
import os
import sys


def get_object_namespace(obj):
    '''
        Returns a dotted string name representation or the form
        'package.module.class' for an object that has an __mro__ attribute.

        This allows you to name loggers inside objects in such a way
        that the logger recognizes them as child loggers to the modules
        they originate from.

        returns a string representation of the object's dotted namespace
        heirarchy.

        Raises an exception if the object does not have an __mro__ attribute.
    '''

    return parse_class_namespace_string(str(obj.__mro__[0]))


def parse_class_namespace_string(class_string):
    '''Parses the dotted namespace out of a class mro tuple member of the form
       "<class 'package.module.class'>"
       Returns a string
    '''
    class_string = str(class_string)
    class_string = class_string.replace("'>", "")
    class_string = class_string.replace("<class '", "")
    return str(class_string)


def getLogger(log_name, log_level=None):
    '''
        Convenience function to create a logger and
        set it's log level at the same time.
        Log level defaults to logging.DEBUG
    '''

    #Create new log
    new_log = logging.getLogger(name=log_name)
    new_log.setLevel(log_level or logging.DEBUG)

    #@TODO: Make this more configurable
    #Force ccengine to setup ultra verbose native handlers.
    cc_verbose_logging_var = os.getenv('CLOUDCAFE_ENABLE_VERBOSE_LOGGING')
    if cc_verbose_logging_var == 'TRUE':
        if logging.getLogger(log_name).handlers == []:
            if log_name == '':
                log_name = 'cc.master'
            new_log.addHandler(setup_new_cchandler(log_name))

    return new_log


def setup_new_cchandler(log_file_name, log_dir=None, encoding=None,
                        msg_format=None):
    '''
        Creates a log handler names <log_file_name> configured to save the log
        in <log_dir> or <os environment variable 'CLOUDCAFE_LOG_PATH'> or
        './logs', in that order or precedent.

        File handler defaults: 'a+', encoding=encoding or "UTF-8", delay=True
    '''

    default_log_dir = './logs'
    os_env_log_dir = os.getenv('CLOUDCAFE_LOG_PATH')

    log_dir = log_dir or os_env_log_dir or default_log_dir

    if log_dir == default_log_dir:
        print log_file_name
        sys.stderr.write('CLOUDCAFE_LOG_PATH environment variable was either'
                        'not set or is None. Logging to base default "{0}"\n'\
                         .format(log_dir))

    try:
        log_dir = os.path.expanduser(log_dir)
    except Exception as e:
        sys.stderr.write('\nUnable to verify log directory: %s\n' % str(e))

    try:
        if not os.path.exists(log_dir):
            os.mkdir(log_dir)
    except Exception as e:
        sys.stderr.write('\nError creating log directory: %s\n' % str(e))

    log_path = os.path.join(log_dir, "{0}.log".format(log_file_name))

    #Set up handler with encoding and msg formatter in log directory
    log_handler = logging.FileHandler(log_path, 'a+',
                                      encoding=encoding or "UTF-8", delay=True)

    fmt = msg_format or '%(asctime)s: %(levelname)s: %(name)s: %(message)s'
    log_handler.setFormatter(logging.Formatter(fmt=fmt))

    return log_handler

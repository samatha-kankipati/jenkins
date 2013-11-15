'''
@summary: Global namespace and engine for CloudCAFE specific framework
@note: TestREPO is the primary consumer for this engine
'''

# Set default logging handler to avoid "No handler found" warnings.
#Stolen from urllib3 and requestslib as a way to do this for all versions of
#python.

import logging

try:
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

logging.getLogger(__name__).addHandler(NullHandler())
logging.getLogger(__name__).setLevel(logging.DEBUG)
del NullHandler
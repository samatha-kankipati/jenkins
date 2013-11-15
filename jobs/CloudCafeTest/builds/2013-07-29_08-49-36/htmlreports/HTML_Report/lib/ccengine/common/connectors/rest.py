'''
@summary: Common classes, base class types, enumerated types, etc...
          that can belong to *any* product's automated tests
@copyright: Copyright (c) 2012 Rackspace US, Inc.
@see: http://docs.python-requests.org/en/latest/api/#requests.Response
'''
import requests
from time import time
from ccengine.common.connectors.base_connector import BaseConnector
from ccengine.common.tools import logging_tools


def log_transaction(log, level=logging_tools.logging.DEBUG):
    ''' Paramaterized decorator takes a python Logger object and an optional
        logging level.
    '''
    def decorator(func):
        '''Accepts a function and returns wrapped version of that function.'''
        def wrapper(*args, **kwargs):
            '''Logging wrapper for any method that returns a requests response
            object.
            Logs requestslib response objects, and the args and kwargs
            sent to the request() method, to the provided log at the
            provided log level
            '''
            logline = '{0} {1}'.format(args, kwargs)

            try:
                log.debug(logline.decode('utf-8', 'replace'))
            except Exception as exception:
                #Ignore all exceptions that happen in logging, then log them
                log.info(
                    'Exception occured while logging signature of calling'
                    'method in rest connector')
                log.exception(exception)

            #requests 1.0 changed 'prefetch' to 'stream' and inverted the
            #relationship.  This performs bi-directional translation
            #for the stream and prefetch keyword args between older
            #and newer versions of requests
            requests_session_attrs = None
            try:
                requests_session_attrs = requests.sessions.Session.__attrs__
            except Exception as exception:
                log.info(
                    'Exception occured while attempting to get requests'
                    'session attrs during call to rest.request()')
                log.exception(exception)

            if requests_session_attrs is not None:
                if 'stream' in requests_session_attrs:
                    if 'prefetch' in kwargs:
                        kwargs['stream'] = not kwargs['prefetch']
                        del kwargs['prefetch']
                elif 'prefetch' in requests_session_attrs:
                    if 'stream' in kwargs:
                        kwargs['prefetch'] = not kwargs['stream']
                        del kwargs['stream']

            #MAKE THE REQUEST
            response = None
            elapsed = None
            try:
                start = time()
                response = func(*args, **kwargs)
                end = time()
                elapsed = end - start
            except Exception as exception:
                log.critical('Call to Requests failed due to exception')
                log.exception(exception)
                raise exception

            #Add elapsed time as an attribute to the response.  This is in
            #lieu of a real stats object
            try:
                setattr(response.request, 'timestamp', start)
                setattr(response, 'timestamp', end)
                setattr(response, 'elapsed_time', elapsed)
            except Exception as exception:
                log.critical('Setting the timestamp and elapsed_time for the'
                             'requests object failed')
                log.exception(exception)

            #requests lib 1.0.0 renamed body to data in the request object
            request_body = ''
            if 'body' in dir(response.request):
                request_body = response.request.body
            elif 'data' in dir(response.request):
                request_body = response.request.data
            else:
                log.info("Unable to log request body, neither a 'data' nor a "
                         "'body' object could be found")

            #requests lib 1.0.4 removed params from r.request
            request_params = ''
            request_url = response.request.url
            if 'params' in dir(response.request):
                request_params = response.request.params
            elif '?' in request_url:
                request_url, request_params = request_url.split('?')

            logline = ''.join([
                '\n{0}\nREQUEST SENT\n{0}\n'.format('-' * 12),
                'request method  : {0}\n'.format(response.request.method),
                'request url     : {0}\n'.format(request_url),
                'request params  : {0}\n'.format(request_params),
                'request headers : {0}\n'.format(response.request.headers),
                'request body    : {0}\n'.format(request_body)])
            try:
                log.log(level, logline.decode('utf-8', 'replace'))
            except Exception as exception:
                #Ignore all exceptions that happen in logging, then log them
                log.log(level, '\n{0}\nREQUEST INFO\n{0}\n'.format('-' * 12))
                log.exception(exception)

            logline = ''.join([
                '\n{0}\nRESPONSE RECIEVED\n{0}\n'.format('-' * 17),
                'response status  : {0}\n'.format(response),
                'response time    : {0}\n'.format(elapsed),
                'response headers : {0}\n'.format(response.headers),
                'response body    : {0}\n'.format(response.content),
                '-' * 79])
            try:
                log.log(level, logline.decode('utf-8', 'replace'))
            except Exception as exception:
                #Ignore all exceptions that happen in logging, then log them
                log.log(level, '\n{0}\nRESPONSE INFO\n{0}\n'.format('-' * 13))
                log.exception(exception)
            return response
        return wrapper
    return decorator


def inject_exception(exception_handlers):
    '''Paramaterized decorator takes a list of exception_handler objects'''
    def decorator(func):
        '''Accepts a function and returns wrapped version of that function.'''
        def wrapper(*args, **kwargs):
            '''Wrapper for any function that returns a Requests response
            Allows exception handlers to raise custom exceptions based on
            response object attributes such as status_code.
            '''
            response = func(*args, **kwargs)
            if exception_handlers:
                for handler in exception_handlers:
                    handler.check_for_errors(response)
            return response
        return wrapper
    return decorator


class RestConnector(BaseConnector):
    '''Class re-implementation of the Reqeusts library api with verbose logging
    Removes a lot of the assumptions that the Requests library makes in api.py
    Supports response-code based exception injection.
    '''
    _log = logging_tools.getLogger(__name__)
    _exception_handlers = []

    def __init__(self):
        super(RestConnector, self).__init__()

    @inject_exception(_exception_handlers)
    @log_transaction(log=_log)
    def request(self, method, url, **kwargs):
        ''' Performs <method> HTTP request to <url>  using the requests lib'''
        return requests.request(method, url, **kwargs)

    def put(self, url, **kwargs):
        ''' HTTP PUT request '''
        return self.request('PUT', url, **kwargs)

    def copy(self, url, **kwargs):
        ''' HTTP COPY request '''
        return self.request('COPY', url, **kwargs)

    def post(self, url, data=None, **kwargs):
        ''' HTTP POST request '''
        return self.request('POST', url, data=data, **kwargs)

    def get(self, url, **kwargs):
        ''' HTTP GET request '''
        return self.request('GET', url, **kwargs)

    def head(self, url, **kwargs):
        ''' HTTP HEAD request '''
        return self.request('HEAD', url, **kwargs)

    def delete(self, url, **kwargs):
        ''' HTTP DELETE request '''
        return self.request('DELETE', url, **kwargs)

    def options(self, url, **kwargs):
        ''' HTTP OPTIONS request '''
        return self.request('OPTIONS', url, **kwargs)

    def patch(self, url, **kwargs):
        ''' HTTP PATCH request '''
        return self.request('PATCH', url, **kwargs)

    @classmethod
    def add_exception_handler(cls, handler):
        '''
        @summary: Adds a specific L{ExceptionHandler} to the rest connector
        @warning: SHOULD ONLY BE CALLED FROM A PROVIDER THROUGH A TEST FIXTURE
        '''
        cls._exception_handlers.append(handler)

    @classmethod
    def delete_exception_handler(cls, handler):
        '''
        @summary: Removes a specific L{ExceptionHandler} to the rest connector
        @warning: SHOULD ONLY BE CALLED FROM A PROVIDER THROUGH A TEST FIXTURE
        '''
        if handler in cls._exception_handlers:
            cls._exception_handlers.remove(handler)

import re


class BaseNegativeUsersTest():

    STATUS_MATCH_ERROR = 'Expected status: %s; Received status: %s'
    STATUS_NOT_MATCH_ERROR = 'Received status: %s; expected other'
    TOKEN_ERROR_MATCHER = re.compile(r'no valid token provided\.', re.I)
    TEST_ACCOUNT_PREFIX = 'CloudCafeTestAccount'
    APIKEY = 'apiKey'
    PASSWORD = 'password'


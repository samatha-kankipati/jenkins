class ItemNotFound(Exception):
    def __init__(self):
        self.message = '404 - Not found.'

    def __str__(self):
        return repr(self.message)


class BuildErrorException(Exception):
    """ Exception on Snapshot build """
    def __init__(self, message='Build Error'):
        self.message = message

    def __str__(self):
        return repr(self.message)


class WorkerStartException(Exception):
    """ Exception on Starting worker """
    def __init__(self, message='Work Start Error'):
        self.message = message

    def __str__(self):
        return repr(self.message)


class WorkerKillException(Exception):
    """ Exception on Killing worker """
    def __init__(self, message='Work Kill Error'):
        self.message = message

    def __str__(self):
        return repr(self.message)


class UnexpectedResponse(Exception):
    """ Unexpected response received """
    def __init__(self, message='Unexpected Response'):
        self.message = message

    def __str__(self):
        return repr(self.message)

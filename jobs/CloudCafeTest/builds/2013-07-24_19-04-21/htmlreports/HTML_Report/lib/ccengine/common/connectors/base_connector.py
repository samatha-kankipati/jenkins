from ccengine.common.tools import logging_tools


class BaseConnector(object):

    def __init__(self):
        super(BaseConnector, self).__init__()
        self.connector_log = logging_tools.getLogger(
                            logging_tools.get_object_namespace(self.__class__))

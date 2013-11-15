import os
import ldap
from ccengine.common.connectors.base_connector import BaseConnector


class LDAPConnector(BaseConnector):

    def __init__(
            self, host=None, port=None, bind_dn=None, password=None,
            page_size=None):
        super(LDAPConnector, self).__init__()
        self.host = host
        self.port = port
        self.bind_dn = bind_dn
        self.password = password
        self.page_size = page_size
        self.server = "ldaps://{0}:{1}/".format(self.host, self.port)

    def bind(self):
        ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)
        ldap.set_option(ldap.OPT_X_TLS_CACERTDIR,
                        os.path.dirname(os.path.realpath(__file__)))

        try:
            self.connector_log.debug(
            "Attempting to bind LDAP connection to {0} as {1}".format(
                self.host, self.bind_dn))
            connection = ldap.initialize(self.server)
            connection.simple_bind_s(self.bind_dn, self.password)
            return connection
        except Exception as exception:
            self.connector_log.exception(exception)
            raise exception

    def unbind(self, connection):
        connection.unbind_s()

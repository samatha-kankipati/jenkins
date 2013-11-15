from testrepo.common.testfixtures.fixtures import BaseTestFixture
from ccengine.clients.identity.ldap.client import RackspaceLDAPClient


class LDAPFixture(BaseTestFixture):

    @classmethod
    def setUpClass(cls):
        super(LDAPFixture, cls).setUpClass()
        port = cls.config.ldap.port
        host = cls.config.ldap.host
        bind_dn = cls.config.ldap.bind_dn
        password = cls.config.ldap.password
        page_size = cls.config.ldap.page_size
        #if LDAP configurations won't be there in staging config files
        #so ldap_client not created and its assigned as None.
        if host:
            cls.ldap_client = RackspaceLDAPClient(host,
                                                  port,
                                                  bind_dn,
                                                  password,
                                                  page_size)
        else:
            cls.ldap_client = None

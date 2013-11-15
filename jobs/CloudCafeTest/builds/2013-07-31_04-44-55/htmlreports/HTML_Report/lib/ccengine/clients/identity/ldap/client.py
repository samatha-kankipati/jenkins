import ldap
from ldap.controls import SimplePagedResultsControl
from ccengine.common.connectors.ldap_connector import LDAPConnector
from ccengine.domain.identity.ldap.filter import Filter


class LDAPConstants(object):
    '''
    Simple mix in to provide ldap constants
    '''
    PAGE_SIZE = 1000
    LDAP_TIMEOUT = None

    SUB = ldap.SCOPE_SUBTREE
    BASE = ldap.SCOPE_BASE

    # Rackspace Specific Constants
    USERS_DN = 'ou=users,o=rackspace,dc=rackspace,dc=com'
    APPLICATIONS_DN = 'ou=applications,o=rackspace,dc=rackspace,dc=com'
    RACKERS_DN = 'ou=rackers,o=rackspace,dc=rackspace,dc=com'
    BASE_DN = 'o=rackspace,dc=rackspace,dc=com'
    GROUPS_DN = 'ou=groups,ou=cloud,o=rackspace,dc=rackspace,dc=com'


## WRAPS ldap
class RackspaceLDAPClient(LDAPConstants, LDAPConnector):

    def __init__(self, host, port, bind_dn, password, page_size):
        super(RackspaceLDAPClient, self).__init__(
                                host, port, bind_dn, password, page_size)

        self.PAGE_SIZE = page_size
        bind_connection = LDAPConnector(
                                host, port, bind_dn, password, page_size)
        try:
            self.connection = bind_connection.bind()
            #self.PAGE_SIZE = bind_connection.page_size
        except Exception as exception:
            self.connector_log.exception(exception)
            raise exception

    def __del__(self):
        self.connection.unbind()

    def release(self):
        self.connection.unbind()

    def delete_entry(self, dn):
        return self.connection.delete_s(dn)

    def get_entry(self, dn, attributes=None):
        if not attributes:
            attributes = ['*']

        search_filter = Filter()
        search_filter.add_equal('objectClass', '*')
        results = self.search(dn, search_filter.build(), ldap.SCOPE_BASE,
                               attributes)
        return results[0][1]

    def search(self, search_dn, search_filter, scope, attributes=['*']):
        results = self.connection.search_s(
            search_dn,
            scope,
            search_filter,
            attrlist=attributes
        )
        return results

    def paged_search(self, search_dn, search_filter, scope, results_processor,
                     attributes=None):
        if not attributes:
            attributes = ['*']

        page_control = SimplePagedResultsControl(True, self.PAGE_SIZE, '')
        serverctrls = [page_control]

        msgid = self.connection.search_ext(
            search_dn,
            scope,
            search_filter,
            attrlist=attributes,
            serverctrls=serverctrls
        )

        page = 0
        records = 0
        while True:
            page += 1
            try:
                result_type, results, result_msg, serverctrls = \
                self.connection.result3(msgid=msgid, timeout=self.LDAP_TIMEOUT)

                records += len(results)
                results_processor(results)

                pagectrls = [
                    serverctrl
                    for serverctrl in serverctrls
                    if serverctrl.controlType == SimplePagedResultsControl.
                                    controlType
                ]

                if pagectrls:
                    if pagectrls[0].cookie:
                        page_control.cookie = pagectrls[0].cookie
                        msgid = self.connection.search_ext(
                            search_dn,
                            scope,
                            search_filter,
                            attrlist=attributes,
                            serverctrls=[page_control]
                        )
                    else:
                        break
                else:
                    break

            except Exception as exception:
                self.connector_log.exception(exception)
                raise exception

    ## RACKSPACE SPECIFIC SEARCHES
    def get_users(self, search_filter, attributes=None):
        if not attributes:
            attributes = ['*']

        return self.search(self.USERS_DN, search_filter, ldap.SCOPE_SUBTREE,
                           attributes=attributes)

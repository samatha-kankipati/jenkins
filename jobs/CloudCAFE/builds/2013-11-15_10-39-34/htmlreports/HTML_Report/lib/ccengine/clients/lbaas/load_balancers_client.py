from ccengine.clients.base_client import BaseMarshallingClient
from ccengine.domain.lbaas.load_balancer import LoadBalancer, LoadBalancerList
from ccengine.domain.lbaas.error_page import ErrorPage
from ccengine.domain.lbaas.stats import Stats
from ccengine.domain.lbaas.node import Node, NodeList, \
    NodeServiceEventList
from ccengine.domain.lbaas.virtual_ip import VirtualIpList, VirtualIp
from ccengine.domain.lbaas.allowed_domain import AllowedDomainList
from ccengine.domain.lbaas.account_billing import AccountBilling
from ccengine.domain.lbaas.load_balancer_usage import LoadBalancerUsage
from ccengine.domain.lbaas.access_list import AccessList, NetworkItem
from ccengine.domain.lbaas.health_monitor import HealthMonitor
from ccengine.domain.lbaas.session_persistence import SessionPersistence
from ccengine.domain.lbaas.connection_logging import ConnectionLogging
from ccengine.domain.lbaas.connection_throttle import ConnectionThrottle
from ccengine.domain.lbaas.content_caching import ContentCaching
from ccengine.domain.lbaas.protocol import ProtocolList
from ccengine.domain.lbaas.algorithm import AlgorithmList
from ccengine.domain.lbaas.ssl_termination import SSLTermination
from ccengine.domain.lbaas.metadata import Metadata, Meta


class LoadBalancersClient(BaseMarshallingClient):

    _suffix = '/loadbalancers'

    def __init__(self, url, auth_token, serialize_format,
                 deserialize_format=None):
        super(LoadBalancersClient, self).__init__(serialize_format,
                                                  deserialize_format)
        self.base_url = url
        self.url = ''.join([url, self._suffix])
        self.auth_token = auth_token
        self.default_headers['X-Auth-Token'] = auth_token
        ct = ''.join(['application/', self.serialize_format])
        accept = ''.join(['application/', self.deserialize_format])
        self.default_headers['Content-Type'] = ct
        self.default_headers['Accept'] = accept

    def create_load_balancer(self, name, nodes, protocol, virtualIps,
                             halfClosed=None, accessList=None, algorithm=None,
                             connectionLogging=None, connectionThrottle=None,
                             healthMonitor=None, metadata=None, port=None,
                             timeout=None, sessionPersistence=None,
                             contentCaching=None, httpsRedirect=None,
                             requestslib_kwargs=None):
        if virtualIps is not None:
            virtualIps = VirtualIpList(virtualIps=[VirtualIp(**vip)
                                                   for vip in virtualIps])
        if nodes is not None:
            nodes = NodeList(nodes=[Node(**node) for node in nodes])
        if accessList is not None:
            accessList = AccessList(accessList=[NetworkItem(**netitem)
                                                for netitem in accessList])
        if connectionLogging is not None:
            connectionLogging = ConnectionLogging(**connectionLogging)
        if connectionThrottle is not None:
            connectionThrottle = ConnectionThrottle(**connectionThrottle)
        if healthMonitor is not None:
            healthMonitor = HealthMonitor(**healthMonitor)
        if sessionPersistence is not None:
            sessionPersistence = SessionPersistence(**sessionPersistence)
        if contentCaching is not None:
            contentCaching = ContentCaching(**contentCaching)
        if metadata is not None:
            metadata = Metadata(metadata=[Meta(key=meta.get('key'),
                                               value=meta.get('value'))
                                          for meta in metadata])
        lb = LoadBalancer(name=name, nodes=nodes, protocol=protocol,
                          halfClosed=halfClosed, virtualIps=virtualIps,
                          accessList=accessList, algorithm=algorithm,
                          connectionLogging=connectionLogging,
                          connectionThrottle=connectionThrottle,
                          healthMonitor=healthMonitor, metadata=metadata,
                          port=port, sessionPersistence=sessionPersistence,
                          contentCaching=contentCaching, timeout=timeout,
                          httpsRedirect=httpsRedirect)

        return self.request('POST', self.url,
                            response_entity_type=LoadBalancer,
                            request_entity=lb,
                            requestslib_kwargs=requestslib_kwargs)

    def list_load_balancers(self, limit=None, marker=None, offset=None,
                            nodeaddress=None, requestslib_kwargs=None):
        params = {}
        if limit is not None:
            params['limit'] = str(limit)
        if marker is not None:
            params['marker'] = str(marker)
        if offset is not None:
            params['offset'] = str(offset)
        if nodeaddress is not None:
            params['nodeaddress'] = str(nodeaddress)
        headers = {'Content-Type': 'application/json'}
        return self.request('GET', self.url, params=params,
                            response_entity_type=LoadBalancerList,
                            requestslib_kwargs=requestslib_kwargs)

    def update_load_balancer(self, load_balancer_id, name=None, protocol=None,
                             algorithm=None, timeout=None, halfClosed=None,
                             port=None, httpsRedirect=None,
                             requestslib_kwargs=None):
        lb = LoadBalancer(name=name, protocol=protocol, algorithm=algorithm,
                          port=port, timeout=timeout, halfClosed=halfClosed,
                          httpsRedirect=httpsRedirect)
        full_url = '/'.join([self.url, str(load_balancer_id)])
        return self.request('PUT', full_url,
                            request_entity=lb,
                            requestslib_kwargs=requestslib_kwargs)

    def get_load_balancer(self, load_balancer_id, requestslib_kwargs=None):
        full_url = '/'.join([self.url, str(load_balancer_id)])
        return self.request('GET', full_url,
                            response_entity_type=LoadBalancer,
                            requestslib_kwargs=requestslib_kwargs)

    def delete_load_balancer(self, load_balancer_id, requestslib_kwargs=None):
        full_url = '/'.join([self.url, str(load_balancer_id)])
        return self.request('DELETE', full_url,
                            requestslib_kwargs=requestslib_kwargs)

    def batch_delete_load_balancers(self, load_balancer_id_list,
                                    requestslib_kwargs=None):
        params = {'id': load_balancer_id_list}
        return self.request('DELETE', self.url, params=params,
                            requestslib_kwargs=requestslib_kwargs)

    # Error Page
    _ERROR_PAGE = 'errorpage'

    def get_error_page(self, load_balancer_id, requestslib_kwargs=None):
        full_url = '/'.join([self.url, str(load_balancer_id),
                             self._ERROR_PAGE])
        return self.request('GET', full_url,
                            response_entity_type=ErrorPage,
                            requestslib_kwargs=requestslib_kwargs)

    def update_error_page(self, load_balancer_id, content,
                          requestslib_kwargs=None):
        ep = ErrorPage(content=content)
        full_url = '/'.join([self.url, str(load_balancer_id),
                             self._ERROR_PAGE])
        return self.request('PUT', full_url,
                            request_entity=ep,
                            response_entity_type=ErrorPage,
                            requestslib_kwargs=requestslib_kwargs)

    def delete_error_page(self, load_balancer_id, requestslib_kwargs=None):
        full_url = '/'.join([self.url, str(load_balancer_id),
                             self._ERROR_PAGE])
        return self.request('DELETE', full_url,
                            requestslib_kwargs=requestslib_kwargs)

    # Stats
    _STATS = 'stats'

    def list_load_balancer_stats(self, load_balancer_id,
                                 requestslib_kwargs=None):
        full_url = '/'.join([self.url, str(load_balancer_id), self._STATS])
        return self.request('GET', full_url,
                            response_entity_type=Stats,
                            requestslib_kwargs=requestslib_kwargs)

    # Nodes
    _NODES = 'nodes'

    def list_nodes(self, load_balancer_id, limit=None, marker=None,
                   offset=None, requestslib_kwargs=None):
        params = {}
        if limit is not None:
            params['limit'] = str(limit)
        if marker is not None:
            params['marker'] = str(marker)
        if offset is not None:
            params['offset'] = str(offset)
        full_url = '/'.join([self.url, str(load_balancer_id), self._NODES])
        return self.request('GET', full_url, params=params,
                            response_entity_type=NodeList,
                            requestslib_kwargs=requestslib_kwargs)

    def get_node(self, load_balancer_id, node_id, requestslib_kwargs=None):
        full_url = '/'.join([self.url, str(load_balancer_id), self._NODES,
                             str(node_id)])
        return self.request('GET', full_url,
                            response_entity_type=Node,
                            requestslib_kwargs=requestslib_kwargs)

    def update_node(self, load_balancer_id, node_id, condition=None,
                    type=None, weight=None, requestslib_kwargs=None):
        node = Node(condition=condition, type=type, weight=weight)
        full_url = '/'.join([self.url, str(load_balancer_id), self._NODES,
                             str(node_id)])
        return self.request('PUT', full_url,
                            request_entity=node,
                            response_entity_type=Node,
                            requestslib_kwargs=requestslib_kwargs)

    def add_nodes(self, load_balancer_id, address, condition, port,
                  type=None, weight=None, requestslib_kwargs=None):
        if isinstance(address, list):
            if type is None:
                type = [None for i in range(len(address))]
            if weight is None:
                weight = [None for i in range(len(address))]
            nodes = [Node(address=address[i], condition=condition[i],
                          port=port[i], type=type[i], weight=weight[i])
                     for i in range(len(address))]
        else:
            nodes = [Node(address=address, condition=condition, port=port,
                          type=type, weight=weight)]
        node_list = NodeList(nodes=nodes)
        full_url = '/'.join([self.url, str(load_balancer_id), self._NODES])
        return self.request('POST', full_url,
                            request_entity=node_list,
                            response_entity_type=NodeList,
                            requestslib_kwargs=requestslib_kwargs)

    def delete_node(self, load_balancer_id, node_id, requestslib_kwargs=None):
        full_url = '/'.join([self.url, str(load_balancer_id), self._NODES,
                             str(node_id)])
        return self.request('DELETE', full_url,
                            response_entity_type=Node,
                            requestslib_kwargs=requestslib_kwargs)

    def batch_delete_nodes(self, load_balancer_id, node_id_list,
                           requestslib_kwargs=None):
        params = {'id': node_id_list}
        full_url = '/'.join([self.url, str(load_balancer_id), self._NODES])
        return self.request('DELETE', full_url, params=params,
                            response_entity_type=Node,
                            requestslib_kwargs=requestslib_kwargs)

    _NODE_EVENTS = 'events'

    def list_node_service_events(self, load_balancer_id,
                                 requestslib_kwargs=None):
        full_url = '/'.join([self.url, str(load_balancer_id), self._NODES,
                             self._NODE_EVENTS])
        return self.request('GET', full_url,
                            response_entity_type=NodeServiceEventList,
                            requestslib_kwargs=requestslib_kwargs)

    # Virtual Ips
    _VIRTUAL_IPS = 'virtualips'

    def list_virtual_ips(self, load_balancer_id, requestslib_kwargs=None):
        full_url = '/'.join([self.url, str(load_balancer_id),
                             self._VIRTUAL_IPS])
        return self.request('GET', full_url,
                            response_entity_type=VirtualIpList,
                            requestslib_kwargs=requestslib_kwargs)

    def add_virtual_ip(self, load_balancer_id, type, ipVersion,
                       requestslib_kwargs=None):
        vip = VirtualIp(type=type, ipVersion=ipVersion)
        full_url = '/'.join([self.url, str(load_balancer_id),
                             self._VIRTUAL_IPS])
        return self.request('POST', full_url,
                            request_entity=vip,
                            response_entity_type=VirtualIp,
                            requestslib_kwargs=requestslib_kwargs)

    def delete_virtual_ip(self, load_balancer_id, virtual_ip_id,
                          requestslib_kwargs=None):
        full_url = '/'.join([self.url, str(load_balancer_id),
                             self._VIRTUAL_IPS, str(virtual_ip_id)])
        return self.request('DELETE', full_url,
                            requestslib_kwargs=requestslib_kwargs)

    # Allowed Domains
    _ALLOWED_DOMAINS = 'alloweddomains'

    def list_allowed_domains(self, requestslib_kwargs=None):
        full_url = '/'.join([self.url, self._ALLOWED_DOMAINS])
        return self.request('GET', full_url,
                            response_entity_type=AllowedDomainList,
                            requestslib_kwargs=requestslib_kwargs)

    # Usage Reports
    _BILLABLE = 'billable'
    _USAGE = 'usage'
    _CURRENT = 'current'

    def list_billable_load_balancers(self, startTime=None, endTime=None,
                                     limit=None, marker=None, offset=None,
                                     requestslib_kwargs=None):
        params = {}
        if startTime is not None:
            params['startTime'] = startTime
        if endTime is not None:
            params['endTime'] = endTime
        if limit is not None:
            params['limit'] = str(limit)
        if marker is not None:
            params['marker'] = str(marker)
        if offset is not None:
            params['offset'] = str(offset)
        full_url = '/'.join([self.url, self._BILLABLE])
        return self.request('GET', full_url, params=params,
                            response_entity_type=LoadBalancer,
                            requestslib_kwargs=requestslib_kwargs)

    def list_account_usage(self, startTime=None, endTime=None,
                           limit=None, marker=None, offset=None,
                           requestslib_kwargs=None):
        params = {}
        if startTime is not None:
            params['startTime'] = startTime
        if endTime is not None:
            params['endTime'] = endTime
        if limit is not None:
            params['limit'] = str(limit)
        if marker is not None:
            params['marker'] = str(marker)
        if offset is not None:
            params['offset'] = str(offset)
        full_url = '/'.join([self.url, self._USAGE])
        return self.request('GET', full_url, params=params,
                            response_entity_type=AccountBilling,
                            requestslib_kwargs=requestslib_kwargs)

    def list_load_balancer_usage(self, load_balancer_id, startTime=None,
                                 endTime=None, limit=None, marker=None,
                                 offset=None, requestslib_kwargs=None):
        params = {}
        if startTime is not None:
            params['startTime'] = startTime
        if endTime is not None:
            params['endTime'] = endTime
        if limit is not None:
            params['limit'] = str(limit)
        if marker is not None:
            params['marker'] = str(marker)
        if offset is not None:
            params['offset'] = str(offset)
        full_url = '/'.join([self.url, str(load_balancer_id), self._USAGE])
        return self.request('GET', full_url, params=params,
                            response_entity_type=LoadBalancerUsage,
                            requestslib_kwargs=requestslib_kwargs)

    def list_current_usage(self, load_balancer_id, limit=None,
                           marker=None, offset=None,
                           requestslib_kwargs=None):
        params = {}
        if limit is not None:
            params['limit'] = str(limit)
        if marker is not None:
            params['marker'] = str(marker)
        if offset is not None:
            params['offset'] = str(offset)
        full_url = '/'.join([self.url, str(load_balancer_id), self._USAGE,
                             self._CURRENT])
        return self.request('GET', full_url, params=params,
                            response_entity_type=LoadBalancerUsage,
                            requestslib_kwargs=requestslib_kwargs)

    # access lists
    _ACCESS_LIST = 'accesslist'

    def get_access_list(self, load_balancer_id, requestslib_kwargs=None):
        full_url = '/'.join([self.url, str(load_balancer_id),
                             self._ACCESS_LIST])
        return self.request('GET', full_url,
                            response_entity_type=AccessList,
                            requestslib_kwargs=requestslib_kwargs)

    def create_access_list(self, load_balancer_id, address, type,
                           requestslib_kwargs=None):
        if isinstance(address, list):
            access_list = [NetworkItem(address=address[i], type=type[i])
                           for i in range(len(address))]
        else:
            access_list = [NetworkItem(address=address, type=type)]
        req_entity = AccessList(accessList=access_list)
        full_url = '/'.join([self.url, str(load_balancer_id),
                             self._ACCESS_LIST])
        return self.request('POST', full_url,
                            request_entity=req_entity,
                            response_entity_type=AccessList,
                            requestslib_kwargs=requestslib_kwargs)

    def delete_access_list_item(self, load_balancer_id, network_item_id,
                                requestslib_kwargs=None):
        full_url = '/'.join([self.url, str(load_balancer_id),
                             self._ACCESS_LIST, str(network_item_id)])
        return self.request('DELETE', full_url,
                            requestslib_kwargs=requestslib_kwargs)

    def delete_access_list(self, load_balancer_id, requestslib_kwargs=None):
        full_url = '/'.join([self.url, str(load_balancer_id),
                             self._ACCESS_LIST])
        return self.request('DELETE', full_url,
                            requestslib_kwargs=requestslib_kwargs)

    def batch_delete_access_list_items(self, load_balancer_id,
                                       network_item_id_list,
                                       requestslib_kwargs=None):
        params = {'id': network_item_id_list}
        full_url = '/'.join([self.url, str(load_balancer_id),
                             self._ACCESS_LIST])
        return self.request('DELETE', full_url, params=params,
                            response_entity_type=AccessList,
                            requestslib_kwargs=requestslib_kwargs)

    # monitors
    _HEALTH_MONITOR = 'healthmonitor'

    def get_health_monitor(self, load_balancer_id, requestslib_kwargs=None):
        full_url = '/'.join([self.url, str(load_balancer_id),
                             self._HEALTH_MONITOR])
        return self.request('GET', full_url,
                            response_entity_type=HealthMonitor,
                            requestslib_kwargs=requestslib_kwargs)

    def update_health_monitor(self, load_balancer_id,
                              attemptsBeforeDeactivation, delay, timeout, type,
                              path=None, statusRegex=None, bodyRegex=None,
                              hostHeader=None, requestslib_kwargs=None):
        health_monitor = HealthMonitor(delay=delay, timeout=timeout, type=type,
                                       attemptsBeforeDeactivation=
                                       attemptsBeforeDeactivation,
                                       hostHeader=hostHeader, path=path,
                                       statusRegex=statusRegex,
                                       bodyRegex=bodyRegex)
        full_url = '/'.join([self.url, str(load_balancer_id),
                             self._HEALTH_MONITOR])
        return self.request('PUT', full_url,
                            request_entity=health_monitor,
                            response_entity_type=HealthMonitor,
                            requestslib_kwargs=requestslib_kwargs)

    def delete_health_monitor(self, load_balancer_id, requestslib_kwargs=None):
        full_url = '/'.join([self.url, str(load_balancer_id),
                             self._HEALTH_MONITOR])
        return self.request('DELETE', full_url,
                            requestslib_kwargs=requestslib_kwargs)

    # sessions
    _SESSION_PERSISTENCE = 'sessionpersistence'

    def get_session_persistence(self, load_balancer_id,
                                requestslib_kwargs=None):
        full_url = '/'.join([self.url, str(load_balancer_id),
                             self._SESSION_PERSISTENCE])
        return self.request('GET', full_url,
                            response_entity_type=SessionPersistence,
                            requestslib_kwargs=requestslib_kwargs)

    def update_session_persistence(self, load_balancer_id, persistenceType,
                                   requestslib_kwargs=None):
        session_persistence = \
            SessionPersistence(persistenceType=persistenceType)
        full_url = '/'.join([self.url, str(load_balancer_id),
                             self._SESSION_PERSISTENCE])
        return self.request('PUT', full_url,
                            request_entity=session_persistence,
                            response_entity_type=SessionPersistence,
                            requestslib_kwargs=requestslib_kwargs)

    def delete_session_persistence(self, load_balancer_id,
                                   requestslib_kwargs=None):
        full_url = '/'.join([self.url, str(load_balancer_id),
                             self._SESSION_PERSISTENCE])
        return self.request('DELETE', full_url,
                            requestslib_kwargs=requestslib_kwargs)

    # connection logging
    _CONNECTION_LOGGING = 'connectionlogging'

    def get_connection_logging(self, load_balancer_id,
                               requestslib_kwargs=None):
        full_url = '/'.join([self.url, str(load_balancer_id),
                             self._CONNECTION_LOGGING])
        return self.request('GET', full_url,
                            response_entity_type=ConnectionLogging,
                            requestslib_kwargs=requestslib_kwargs)

    def update_connection_logging(self, load_balancer_id, enabled,
                                  requestslib_kwargs=None):
        connection_logging = ConnectionLogging(enabled=enabled)
        full_url = '/'.join([self.url, str(load_balancer_id),
                             self._CONNECTION_LOGGING])
        return self.request('PUT', full_url,
                            request_entity=connection_logging,
                            response_entity_type=ConnectionLogging,
                            requestslib_kwargs=requestslib_kwargs)

    # connection throttle
    _CONNECTION_THROTTLE = 'connectionthrottle'

    def get_connection_throttle(self, load_balancer_id,
                                requestslib_kwargs=None):
        full_url = '/'.join([self.url, str(load_balancer_id),
                             self._CONNECTION_THROTTLE])
        return self.request('GET', full_url,
                            response_entity_type=ConnectionThrottle,
                            requestslib_kwargs=requestslib_kwargs)

    def update_connection_throttle(self, load_balancer_id,
                                   maxConnectionRate=None, maxConnections=None,
                                   minConnections=None, rateInterval=None,
                                   requestslib_kwargs=None):
        connection_throttle = ConnectionThrottle(
            maxConnectionRate=maxConnectionRate,
            maxConnections=maxConnections,
            minConnections=minConnections,
            rateInterval=rateInterval)
        full_url = '/'.join([self.url, str(load_balancer_id),
                             self._CONNECTION_THROTTLE])
        return self.request('PUT', full_url,
                            request_entity=connection_throttle,
                            response_entity_type=ConnectionThrottle,
                            requestslib_kwargs=requestslib_kwargs)

    def delete_connection_throttle(self, load_balancer_id,
                                   requestslib_kwargs=None):
        full_url = '/'.join([self.url, str(load_balancer_id),
                             self._CONNECTION_THROTTLE])
        return self.request('DELETE', full_url,
                            requestslib_kwargs=requestslib_kwargs)

    # content caching
    _CONTENT_CACHING = 'contentcaching'

    def get_content_caching(self, load_balancer_id,
                            requestslib_kwargs=None):
        full_url = '/'.join([self.url, str(load_balancer_id),
                             self._CONTENT_CACHING])
        return self.request('GET', full_url,
                            response_entity_type=ContentCaching,
                            requestslib_kwargs=requestslib_kwargs)

    def update_content_caching(self, load_balancer_id, enabled,
                               requestslib_kwargs=None):
        content_caching = ContentCaching(enabled=enabled)
        full_url = '/'.join([self.url, str(load_balancer_id),
                             self._CONTENT_CACHING])
        return self.request('PUT', full_url,
                            request_entity=content_caching,
                            response_entity_type=ContentCaching,
                            requestslib_kwargs=requestslib_kwargs)

    # limits
    _LIMITS = 'limits'

    # TODO - Create Domain Objects
    def list_rate_limits(self, limit=None, marker=None, offset=None,
                         requestslib_kwargs=None):
        params = {}
        if limit is not None:
            params['limit'] = str(limit)
        if marker is not None:
            params['marker'] = str(marker)
        if offset is not None:
            params['offset'] = str(offset)
        full_url = '/'.join([self.base_url, self._LIMITS])
        return self.request('GET', full_url, params=params,
                            # response_entity_type=AlgorithmList,
                            requestslib_kwargs=requestslib_kwargs)

    _ABSOLUTE_LIMITS = 'absolutelimits'

    # TODO - Create Domain Objects
    def list_absolute_limits(self, limit=None, marker=None, offset=None,
                             requestslib_kwargs=None):
        params = {}
        if limit is not None:
            params['limit'] = str(limit)
        if marker is not None:
            params['marker'] = str(marker)
        if offset is not None:
            params['offset'] = str(offset)
        full_url = '/'.join([self.url, self._ABSOLUTE_LIMITS])
        return self.request('GET', full_url, params=params,
                            # response_entity_type=AlgorithmList,
                            requestslib_kwargs=requestslib_kwargs)

    # protocols
    _PROTOCOLS = 'protocols'

    def list_protocols(self, limit=None, marker=None, offset=None,
                       requestslib_kwargs=None):
        params = {}
        if limit is not None:
            params['limit'] = str(limit)
        if marker is not None:
            params['marker'] = str(marker)
        if offset is not None:
            params['offset'] = str(offset)
        full_url = '/'.join([self.url, self._PROTOCOLS])
        return self.request('GET', full_url, params=params,
                            response_entity_type=ProtocolList,
                            requestslib_kwargs=requestslib_kwargs)

    # algorithms
    _ALGORITHMS = 'algorithms'

    def list_algorithms(self, limit=None, marker=None, offset=None,
                        requestslib_kwargs=None):
        params = {}
        if limit is not None:
            params['limit'] = str(limit)
        if marker is not None:
            params['marker'] = str(marker)
        if offset is not None:
            params['offset'] = str(offset)
        full_url = '/'.join([self.url, self._ALGORITHMS])
        return self.request('GET', full_url, params=params,
                            response_entity_type=AlgorithmList,
                            requestslib_kwargs=requestslib_kwargs)
        # ssl termination
    _SSL_TERMINATION = 'ssltermination'

    def get_ssl_termination(self, load_balancer_id, requestslib_kwargs=None):
        full_url = '/'.join([self.url, str(load_balancer_id),
                             self._SSL_TERMINATION])
        return self.request('GET', full_url,
                            response_entity_type=SSLTermination,
                            requestslib_kwargs=requestslib_kwargs)

    def delete_ssl_termination(self, load_balancer_id,
                               requestslib_kwargs=None):
        full_url = '/'.join([self.url, str(load_balancer_id),
                             self._SSL_TERMINATION])
        return self.request('DELETE', full_url,
                            requestslib_kwargs=requestslib_kwargs)

    def update_ssl_termination(self, load_balancer_id, securePort=None,
                               privatekey=None, certificate=None,
                               intermediateCertificate=None, enabled=None,
                               secureTrafficOnly=None,
                               requestslib_kwargs=None):
        ssl_term = SSLTermination(securePort=securePort, privatekey=privatekey,
                                  certificate=certificate, enabled=enabled,
                                  intermediateCertificate=
                                  intermediateCertificate,
                                  secureTrafficOnly=secureTrafficOnly)
        full_url = '/'.join([self.url, str(load_balancer_id),
                             self._SSL_TERMINATION])
        return self.request('PUT', full_url,
                            response_entity_type=SSLTermination,
                            request_entity=ssl_term,
                            requestslib_kwargs=requestslib_kwargs)

    # metadata
    _METADATA = 'metadata'

    def list_load_balancer_metadata(self, load_balancer_id,
                                    requestslib_kwargs=None):
        full_url = '/'.join([self.url, str(load_balancer_id), self._METADATA])
        return self.request('GET', full_url,
                            response_entity_type=Metadata,
                            requestslib_kwargs=requestslib_kwargs)

    def get_load_balancer_meta_item(self, load_balancer_id, meta_id,
                                    requestslib_kwargs=None):
        full_url = '/'.join([self.url, str(load_balancer_id), self._METADATA,
                             str(meta_id)])
        return self.request('GET', full_url,
                            response_entity_type=Meta,
                            requestslib_kwargs=requestslib_kwargs)

    def list_node_metadata(self, load_balancer_id, node_id,
                           requestslib_kwargs=None):
        full_url = '/'.join([self.url, str(load_balancer_id),
                             self._NODES, str(node_id), self._METADATA])
        return self.request('GET', full_url,
                            response_entity_type=Metadata,
                            requestslib_kwargs=requestslib_kwargs)

    def get_node_meta_item(self, load_balancer_id, node_id, meta_id,
                           requestslib_kwargs=None):
        full_url = '/'.join([self.url, str(load_balancer_id), self._NODES,
                             str(node_id), self._METADATA, str(meta_id)])
        return self.request('GET', full_url,
                            response_entity_type=Meta,
                            requestslib_kwargs=requestslib_kwargs)

    def add_load_balancer_metadata(self, load_balancer_id, metadata,
                                   requestslib_kwargs=None):
        md_list = []
        for meta in metadata:
            md_list.append(Meta(key=meta.get('key'), value=meta.get('value')))
        md = Metadata(metadata=md_list)
        full_url = '/'.join([self.url, str(load_balancer_id), self._METADATA])
        return self.request('POST', full_url,
                            request_entity=md,
                            response_entity_type=Metadata,
                            requestslib_kwargs=requestslib_kwargs)

    def add_node_metadata(self, load_balancer_id, node_id, metadata,
                          requestslib_kwargs=None):
        md_list = []
        for meta in metadata:
            md_list.append(Meta(key=meta.get('key'), value=meta.get('value')))
        md = Metadata(metadata=md_list)
        full_url = '/'.join([self.url, str(load_balancer_id),
                             self._NODES, str(node_id), self._METADATA])
        return self.request('POST', full_url,
                            request_entity=md,
                            response_entity_type=Metadata,
                            requestslib_kwargs=requestslib_kwargs)

    def update_load_balancer_meta_item(self, load_balancer_id, meta_id,
                                       value, requestslib_kwargs=None):
        meta = Meta(value=value)
        full_url = '/'.join([self.url, str(load_balancer_id), self._METADATA,
                             str(meta_id)])
        return self.request('PUT', full_url,
                            request_entity=meta,
                            response_entity_type=Meta,
                            requestslib_kwargs=requestslib_kwargs)

    def update_node_meta_item(self, load_balancer_id, node_id, meta_id,
                              value, requestslib_kwargs=None):
        meta = Meta(value=value)
        full_url = '/'.join([self.url, str(load_balancer_id),
                             self._NODES, str(node_id), self._METADATA,
                             str(meta_id)])
        return self.request('PUT', full_url,
                            request_entity=meta,
                            response_entity_type=Meta,
                            requestslib_kwargs=requestslib_kwargs)

    def delete_load_balancer_meta_item(self, load_balancer_id, meta_id,
                                       requestslib_kwargs=None):
        full_url = '/'.join([self.url, str(load_balancer_id), self._METADATA,
                             str(meta_id)])
        return self.request('DELETE', full_url,
                            requestslib_kwargs=requestslib_kwargs)

    def batch_delete_load_balancer_meta_items(self, load_balancer_id,
                                              meta_id_list,
                                              requestslib_kwargs=None):
        params = {'id': meta_id_list}
        full_url = '/'.join([self.url, str(load_balancer_id), self._METADATA])
        return self.request('DELETE', full_url, params=params,
                            requestslib_kwargs=requestslib_kwargs)

    def delete_node_meta_item(self, load_balancer_id, node_id, meta_id,
                              requestslib_kwargs=None):
        full_url = '/'.join([self.url, str(load_balancer_id),
                             self._NODES, str(node_id), self._METADATA,
                             str(meta_id)])
        return self.request('DELETE', full_url,
                            requestslib_kwargs=requestslib_kwargs)

    def batch_delete_node_meta_items(self, load_balancer_id, node_id,
                                     meta_id_list, requestslib_kwargs=None):
        params = {'id': meta_id_list}
        full_url = '/'.join([self.url, str(load_balancer_id), self._NODES,
                             str(node_id), self._METADATA])
        return self.request('DELETE', full_url, params=params,
                            requestslib_kwargs=requestslib_kwargs)

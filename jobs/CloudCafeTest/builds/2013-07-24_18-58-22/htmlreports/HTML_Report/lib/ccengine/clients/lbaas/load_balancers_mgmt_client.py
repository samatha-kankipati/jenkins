from ccengine.clients.base_client import BaseMarshallingClient
from ccengine.domain.lbaas.virtual_ip import VirtualIp, VirtualIpList
from ccengine.domain.lbaas.mgmt.virtual_ip_block import VirtualIpBlock, \
    VirtualIpBlockList
from ccengine.domain.lbaas.mgmt.assign_vip import AssignVIP
from ccengine.domain.lbaas.mgmt.suspension import Suspension
from ccengine.domain.lbaas.mgmt.backup import BackupList
from ccengine.domain.lbaas.mgmt.absolute_limits import AbsoluteLimits, Limit
from ccengine.domain.lbaas.mgmt.load_balancer import LoadBalancerList, \
    ExtendedAccountLoadBalancerList
from ccengine.domain.lbaas.mgmt.ticket import TicketList, Ticket
from ccengine.domain.lbaas.mgmt.extended_view_load_balancer import \
    ExtendedLoadBalancer
from ccengine.domain.lbaas.mgmt.cluster import ClusterList, Cluster
from ccengine.domain.lbaas.mgmt.host import HostList, Host, \
    HostCapacityReportList
from ccengine.domain.lbaas.mgmt.subnet_mapping import HostSubnetList, \
    HostSubnet, NetInterfaceList, NetInterface, CidrList, Cidr
from ccengine.domain.lbaas.mgmt.customers import CustomerList
from ccengine.domain.lbaas.mgmt.health_checks import HealthCheckList
from ccengine.domain.lbaas.mgmt.account_usage_and_billing import \
    AccountBillingList, AccountUsageRecordList, LoadBalancerUsageList
from ccengine.domain.lbaas.mgmt.cluster_customer_count \
    import ClusterCustomerCount
from ccengine.domain.lbaas.mgmt.host_customer_count \
    import HostCustomerCount
from ccengine.domain.lbaas.mgmt.alert import AlertList, Alert
from ccengine.domain.lbaas.mgmt.host_usage import HostUsageRecords
from ccengine.domain.lbaas.mgmt.events import AccountLoadBalancerEventList
from ccengine.domain.lbaas.allowed_domain import AllowedDomainList, \
    AllowedDomain
from ccengine.domain.lbaas.mgmt.blacklist import Blacklist, BlacklistItem
from ccengine.domain.lbaas.mgmt.scheduled_jobs import JobList, Job
from ccengine.domain.lbaas.mgmt.virtual_ip_availability_report import \
    VirtualIpAvailabilityReportList
from ccengine.domain.lbaas.mgmt.audit import LoadBalancerAuditList
from ccengine.domain.lbaas.mgmt.loadbalancer_status_history import \
    LoadBalancerStatusHistoryList
import base64


class LoadBalancersMgmtClient(BaseMarshallingClient):

    _suffix = '/management'
    _BACKUPS = 'backups'
    _HOSTS = 'hosts'
    _ACCOUNTS = 'accounts'
    _ABSOLUTE_LIMITS = 'absolutelimits'
    _LOADBALANCERS = 'loadbalancers'
    _TICKETS = 'tickets'
    _EXTENDEDVIEW = 'extendedview'
    _CLUSTERS = 'clusters'
    _ENDPOINT = 'endpoint'
    _ENABLE = 'enable'
    _DISABLE = 'disable'
    _POLLER = 'pollendpoints'
    _VIRTUALIPS = 'virtualips'
    _VIPBLOCKS = 'virtualipblocks'
    _SUBNETMAPPINGS = 'subnetmappings'
    _CUSTOMERS = 'customers'
    _CUSTOMERCOUNT = 'customercount'
    _SUSPEND = 'suspension'
    _BILLING = 'billing'
    _USAGE = 'usage'
    _SETSTATUS = 'setstatus'
    _ALERTS = 'alerts'
    _EVENT = 'event'
    _ALLOWED_DOMAINS = 'alloweddomains'
    _BLACKLIST = 'blacklist'
    _JOBS = 'jobs'
    _HOST_CAPACITY = 'capacityreport'
    _VIP_AVAILABILITY = 'availabilityreport'

    def __init__(self, url, user, password, serialize_format,
                 deserialize_format=None):
        super(LoadBalancersMgmtClient, self).__init__(serialize_format,
                                                      deserialize_format)
        self.url = ''.join([url, self._suffix])
        encrypted_password = \
            base64.encodestring('%s:%s' % (user, password))[:-1]
        self.default_headers['Authorization'] = ''.join(['Basic ',
                                                         encrypted_password])
        ct = ''.join(['application/', self.serialize_format])
        accept = ''.join(['application/', self.deserialize_format])
        self.default_headers['Content-Type'] = ct
        self.default_headers['Accept'] = accept

    def add_virtual_ip(self, load_balancer_id, type, ticket,
                       requestslib_kwargs=None):
        avip = AssignVIP(type=type, ticket=ticket)
        full_url = '/'.join([self.url, self._LOADBALANCERS,
                             str(load_balancer_id), self._VIRTUALIPS])
        return self.request('POST', full_url,
                            response_entity_type=VirtualIp,
                            request_entity=avip,
                            requestslib_kwargs=requestslib_kwargs)

    def get_region_vips(self, requestslib_kwargs=None):
        full_url = '/'.join([self.url, self._VIRTUALIPS])
        return self.request('GET', full_url,
                            response_entity_type=VirtualIpList,
                            requestslib_kwargs=requestslib_kwargs)

    def get_vips_on_cluster(self, clusterId, requestslib_kwargs=None):
        full_url = '/'.join([self.url, self._CLUSTERS, str(clusterId),
                            self._VIRTUALIPS])
        return self.request('GET', full_url,
                            response_entity_type=VirtualIpList,
                            requestslib_kwargs=requestslib_kwargs)

    def get_vips_on_loadbalancer(self, loadBalancerId,
                                 requestslib_kwargs=None):
        full_url = '/'.join([self.url, self._LOADBALANCERS,
                             str(loadBalancerId), self._VIRTUALIPS])
        return self.request('GET', full_url,
                            response_entity_type=VirtualIpList,
                            requestslib_kwargs=requestslib_kwargs)

    def delete_virtual_ip(self, vipId, requestslib_kwargs=None):
        full_url = '/'.join([self.url, self._VIRTUALIPS, str(vipId)])
        return self.request('DELETE', full_url, response_entity_type=None,
                            requestslib_kwargs=requestslib_kwargs)

    def add_vip_block(self, clusterId, firstIp, lastIp, type,
                      requestslib_kwargs=None):
        full_url = '/'.join([self.url, self._CLUSTERS, str(clusterId),
                             self._VIPBLOCKS])
        blocks = VirtualIpBlockList(type, [VirtualIpBlock(firstIp, lastIp)])
        return self.request('POST', full_url, request_entity=blocks,
                            requestslib_kwargs=requestslib_kwargs)

    def get_load_balancer_suspension(self, lb_id,
                                     requestslib_kwargs=None):
        full_url = '/'.join([self.url, self._LOADBALANCERS, str(lb_id),
                             self._SUSPEND])
        return self.request('GET', full_url, response_entity_type=Suspension,
                            requestslib_kwargs=requestslib_kwargs)

    def suspend_load_balancer(self, load_balancer_id, reason=None, user=None,
                              ticket=None, requestslib_kwargs=None):
        susp = Suspension(reason=reason, user=user, ticket=ticket)
        full_url = '/'.join([self.url, 'loadbalancers', str(load_balancer_id),
                             'suspension'])
        return self.request('POST', full_url,
                            response_entity_type=None,
                            request_entity=susp,
                            requestslib_kwargs=requestslib_kwargs)

    def unsuspend_load_balancer(self, load_balancer_id,
                                requestslib_kwargs=None):
        full_url = '/'.join([self.url, 'loadbalancers', str(load_balancer_id),
                             'suspension'])
        return self.request('DELETE', full_url,
                            response_entity_type=None,
                            requestslib_kwargs=requestslib_kwargs)

    def delete_suspended_load_balancer(self, load_balancer_id,
                                       requestslib_kwargs=None):
        full_url = '/'.join([self.url, 'loadbalancers', str(load_balancer_id),
                             'suspended'])
        return self.request('DELETE', full_url,
                            response_entity_type=None,
                            requestslib_kwargs=requestslib_kwargs)

    def delete_errored_load_balancer(self, load_balancer_id,
                                     requestslib_kwargs=None):
        full_url = '/'.join([self.url, 'loadbalancers', str(load_balancer_id),
                             'error'])
        return self.request('DELETE', full_url,
                            response_entity_type=None,
                            requestslib_kwargs=requestslib_kwargs)

    def sync_load_balancer(self, load_balancer_id, requestslib_kwargs=None):
        full_url = '/'.join([self.url, 'loadbalancers', str(load_balancer_id),
                             'sync'])
        return self.request('PUT', full_url,
                            response_entity_type=None,
                            requestslib_kwargs=requestslib_kwargs)

    def get_absolute_limits(self, account_id, requestslib_kwargs=None):
        full_url = '/'.join([self.url, self._ACCOUNTS, str(account_id),
                             self._LOADBALANCERS, self._ABSOLUTE_LIMITS])
        return self.request('GET', full_url,
                            response_entity_type=AbsoluteLimits,
                            requestslib_kwargs=requestslib_kwargs)

    def add_absolute_limit(self, account_id, name, value,
                           requestslib_kwargs=None):
        full_url = '/'.join([self.url, self._ACCOUNTS, str(account_id),
                             self._LOADBALANCERS, self._ABSOLUTE_LIMITS])
        return self.request('POST', full_url,
                            request_entity=Limit(name=name, value=value),
                            response_entity_type=None,
                            requestslib_kwargs=requestslib_kwargs)

    def update_absolute_limit(self, account_id, value, limit_id,
                              requestslib_kwargs=None):
        full_url = '/'.join([self.url, self._ACCOUNTS, str(account_id),
                             self._LOADBALANCERS, self._ABSOLUTE_LIMITS,
                             str(limit_id)])
        return self.request('PUT', full_url,
                            request_entity=Limit(value=value),
                            response_entity_type=None,
                            requestslib_kwargs=requestslib_kwargs)

    def delete_absolute_limit(self, account_id, limit_id,
                              requestslib_kwargs=None):
        full_url = '/'.join([self.url, self._ACCOUNTS, str(account_id),
                             self._LOADBALANCERS, self._ABSOLUTE_LIMITS,
                             str(limit_id)])
        return self.request('DELETE', full_url,
                            response_entity_type=None,
                            requestslib_kwargs=requestslib_kwargs)

    def get_load_balancers_with_vip(self, vipid=None, vipaddress=None,
                                    requestslib_kwargs=None):
        full_url = '/'.join([self.url, self._LOADBALANCERS])
        params = {}
        if vipid is not None:
            params['vipid'] = str(vipid)
        if vipaddress is not None:
            params['vipaddress'] = str(vipaddress)
        return self.request('GET', full_url, params=params,
                            response_entity_type=LoadBalancerList,
                            requestslib_kwargs=requestslib_kwargs)

    def get_extended_view_load_balancer(self, loadBalancerId,
                                        requestslib_kwargs=None):
        full_url = '/'.join([self.url, self._LOADBALANCERS,
                             str(loadBalancerId), self._EXTENDEDVIEW])
        return self.request('GET', full_url,
                            response_entity_type=ExtendedLoadBalancer,
                            requestslib_kwargs=requestslib_kwargs)

    def get_tickets(self, loadBalancerId, requestslib_kwargs=None):
        full_url = '/'.join([self.url, self._LOADBALANCERS,
                             str(loadBalancerId), self._TICKETS])
        return self.request('GET', full_url, response_entity_type=TicketList,
                            requestslib_kwargs=requestslib_kwargs)

    def add_ticket(self, loadBalancerId, comment, ticketId,
                   requestslib_kwargs=None):
        full_url = '/'.join([self.url, self._LOADBALANCERS,
                             str(loadBalancerId), self._TICKETS])
        ticket = Ticket(comment=comment, ticketId=ticketId)
        return self.request('POST', full_url, response_entity_type=Ticket,
                            request_entity=ticket,
                            requestslib_kwargs=requestslib_kwargs)

    def get_clusters(self, requestslib_kwargs=None):
        full_url = '/'.join([self.url, self._CLUSTERS])
        return self.request('GET', full_url, response_entity_type=ClusterList,
                            requestslib_kwargs=requestslib_kwargs)

    def get_cluster(self, clusterId, requestslib_kwargs=None):
        full_url = '/'.join([self.url, self._CLUSTERS, str(clusterId)])
        return self.request('GET', full_url, response_entity_type=Cluster,
                            requestslib_kwargs=requestslib_kwargs)

    def get_hosts_on_cluster(self, clusterId, requestslib_kwargs=None):
        full_url = '/'.join([self.url, self._CLUSTERS, str(clusterId),
                             self._HOSTS])
        return self.request('GET', full_url, response_entity_type=HostList,
                            requestslib_kwargs=requestslib_kwargs)

    def get_hosts(self, requestslib_kwargs=None):
        full_url = '/'.join([self.url, self._HOSTS])
        return self.request('GET', full_url, response_entity_type=HostList,
                            requestslib_kwargs=requestslib_kwargs)

    def get_host(self, hostId, requestslib_kwargs=None):
        full_url = '/'.join([self.url, self._HOSTS, str(hostId)])
        return self.request('GET', full_url, response_entity_type=Host,
                            requestslib_kwargs=requestslib_kwargs)

    def add_host(self, name, clusterId, coreDeviceId, zone, managementIp,
                 managementSoapInterface, maxConcurrentConnections,
                 trafficManagerName, type, soapEndpointActive, ipv4Servicenet,
                 ipv4Public, requestslib_kwargs=None):
        full_url = '/'.join([self.url, self._HOSTS])
        host = Host(name=name, clusterId=clusterId, coreDeviceId=coreDeviceId,
                    zone=zone, managementIp=managementIp, type=type,
                    managementSoapInterface=managementSoapInterface,
                    maxConcurrentConnections=maxConcurrentConnections,
                    trafficManagerName=trafficManagerName,
                    soapEndpointActive=soapEndpointActive,
                    ipv4Servicenet=ipv4Servicenet, ipv4Public=ipv4Public)
        return self.request('POST', full_url, response_entity_type=Host,
                            request_entity=host,
                            requestslib_kwargs=requestslib_kwargs)

    def update_host(self, hostId, name=None, coreDeviceId=None,
                    managementIp=None, managementSoapInterface=None,
                    maxConcurrentConnections=None, trafficManagerName=None,
                    soapEndpointActive=None, ipv4Servicenet=None,
                    ipv4Public=None, requestslib_kwargs=None):
        full_url = '/'.join([self.url, self._HOSTS, str(hostId)])
        host = Host(name=name, coreDeviceId=coreDeviceId,
                    managementIp=managementIp, ipv4Public=ipv4Public,
                    managementSoapInterface=managementSoapInterface,
                    maxConcurrentConnections=maxConcurrentConnections,
                    trafficManagerName=trafficManagerName,
                    soapEndpointActive=soapEndpointActive,
                    ipv4Servicenet=ipv4Servicenet)
        return self.request('PUT', full_url, response_entity_type=Host,
                            request_entity=host,
                            requestslib_kwargs=requestslib_kwargs)

    def delete_host(self, hostId, requestslib_kwargs=None):
        full_url = '/'.join([self.url, self._HOSTS, str(hostId)])
        return self.request('DELETE', full_url, response_entity_type=None,
                            requestslib_kwargs=requestslib_kwargs)

    def get_host_endpoint(self, clusterId, requestslib_kwargs=None):
        full_url = '/'.join([self.url, self._CLUSTERS, str(clusterId),
                             self._ENDPOINT])
        return self.request('GET', full_url, response_entity_type=Host,
                            requestslib_kwargs=requestslib_kwargs)

    def update_host_endpoint_enable(self, hostId, requestslib_kwargs=None):
        full_url = '/'.join([self.url, self._HOSTS, str(hostId),
                             self._ENDPOINT, self._ENABLE])
        return self.request('PUT', full_url, response_entity_type=None,
                            requestslib_kwargs=requestslib_kwargs)

    def update_host_endpoint_disable(self, hostId, requestslib_kwargs=None):
        full_url = '/'.join([self.url, self._HOSTS, str(hostId),
                             self._ENDPOINT, self._DISABLE])
        return self.request('PUT', full_url, response_entity_type=None,
                            requestslib_kwargs=requestslib_kwargs)

    def call_host_endpoint_poller(self, requestslib_kwargs=None):
        full_url = '/'.join([self.url, self._CLUSTERS, self._POLLER])
        return self.request('PUT', full_url, response_entity_type=None,
                            requestslib_kwargs=requestslib_kwargs)

    def get_host_backups(self, host_id, requestslib_kwargs=None):
        full_url = '/'.join([self.url, self._HOSTS, str(host_id),
                             self._BACKUPS])
        return self.request('GET', full_url, response_entity_type=BackupList,
                            requestslib_kwargs=requestslib_kwargs)

    def get_subnet_mappings(self, host_id, requestslib_kwargs=None):
        full_url = '/'.join([self.url, self._HOSTS, str(host_id),
                             self._SUBNETMAPPINGS])
        return self.request('GET', full_url,
                            response_entity_type=HostSubnetList,
                            requestslib_kwargs=requestslib_kwargs)

    #here
    def add_subnet_mappings(self, host_id, subnet, requestslib_kwargs=None):
        full_url = '/'.join([self.url, self._HOSTS, str(host_id),
                             self._SUBNETMAPPINGS])
        subnetList = self.build_host_subnet_list(subnet)
        return self.request('PUT', full_url,
                            request_entity=subnetList,
                            requestslib_kwargs=requestslib_kwargs)

    def delete_subnet_mappings(self, host_id, subnet, requestslib_kwargs=None):
        full_url = '/'.join([self.url, self._HOSTS, str(host_id),
                             self._SUBNETMAPPINGS])
        subnetList = self.build_host_subnet_list(subnet)
        return self.request('DELETE', full_url,
                            request_entity=subnetList,
                            response_entity_type=HostSubnetList,
                            requestslib_kwargs=requestslib_kwargs)

    # Helper method for add/delete subnet mappings
    def build_host_subnet_list(self, host_subnet_dict):
        # [{'name': 'Is name', 'cidrs':[{'block': '10.1.1.0/24'}]}]
        interfaces = NetInterfaceList([])
        for item in host_subnet_dict:
            # interface = NetInterface(name=item['name'])
            cidrs = [Cidr(block=cidr_dic['block'])
                     for cidr_dic in item['cidrs']]
            cidr_list = CidrList(cidrs=cidrs)
            interface = NetInterface(name=item['name'], cidrs=cidr_list)
            # for obj in item['cidrs']:
            #     interface.cidrs = CidrList(cidrs=[Cidr(block=obj['block'])])
            interfaces.append(interface)
        return HostSubnetList([HostSubnet(netInterfaces=interfaces)])

    def get_hosts_customers(self, byIdOrName, requestslib_kwargs=None):
        full_url = '/'.join([self.url, self._HOSTS, self._CUSTOMERS])
        return self.request('POST', full_url,
                            request_entity=byIdOrName,
                            response_entity_type=CustomerList,
                            requestslib_kwargs=requestslib_kwargs)

    def get_clusters_customers(self, byIdOrName, requestslib_kwargs=None):
        full_url = '/'.join([self.url, self._CLUSTERS, self._CUSTOMERS])
        return self.request('POST', full_url,
                            request_entity=byIdOrName,
                            response_entity_type=CustomerList,
                            requestslib_kwargs=requestslib_kwargs)

    def get_customer_count_on_host(self, host_id=None,
                                   requestslib_kwargs=None):
        full_url = '/'.join([self.url, self._HOSTS, str(host_id),
                             self._CUSTOMERCOUNT])
        return self.request('GET', full_url,
                            response_entity_type=HostCustomerCount,
                            requestslib_kwargs=requestslib_kwargs)

    def get_customer_count_on_cluster(self, cluster_id=None,
                                      requestslib_kwargs=None):
        full_url = '/'.join([self.url, self._CLUSTERS, str(cluster_id),
                             self._CUSTOMERCOUNT])
        return self.request('GET', full_url,
                            response_entity_type=ClusterCustomerCount,
                            requestslib_kwargs=requestslib_kwargs)

    def get_health_check(self, requestslib_kwargs=None):
        full_url = '/'.join([self.url, 'healthcheck'])
        return self.request('GET', full_url,
                            response_entity_type=HealthCheckList,
                            requestslib_kwargs=requestslib_kwargs)

    def get_load_balancers_on_account(self, account_id,
                                      requestslib_kwargs=None):
        full_url = '/'.join([self.url, self._ACCOUNTS, str(account_id),
                             self._LOADBALANCERS])
        return self.request('GET', full_url,
                            response_entity_type=LoadBalancerList,
                            requestslib_kwargs=requestslib_kwargs)

    def get_extended_load_balancers_on_account(self, account_id,
                                               requestslib_kwargs=None):
        full_url = '/'.join([self.url, self._ACCOUNTS, str(account_id),
                             'extendedloadbalancers'])
        return self.request('GET', full_url,
                            response_entity_type=
                            ExtendedAccountLoadBalancerList,
                            requestslib_kwargs=requestslib_kwargs)

    def get_accounts_billing(self, requestslib_kwargs=None):
        full_url = '/'.join([self.url, self._ACCOUNTS, self._BILLING])
        return self.request('GET', full_url,
                            params={'startTime': '2012-12-17T00:00:00',
                                    'endTime': '2012-12-17T20:00:00'},
                            response_entity_type=AccountBillingList,
                            requestslib_kwargs=requestslib_kwargs)

    def get_accounts_usage(self, requestslib_kwargs=None):
        full_url = '/'.join([self.url, self._ACCOUNTS, self._USAGE])
        return self.request('GET', full_url,
                            params={'startTime': '2012-12-17T00:00:00',
                                    'endTime': '2012-12-17T20:00:00'},
                            response_entity_type=AccountUsageRecordList,
                            requestslib_kwargs=requestslib_kwargs)

    def get_load_balancers_usage(self, start_time, end_time,
                                 requestslib_kwargs=None):
        full_url = '/'.join([self.url, self._LOADBALANCERS, self._USAGE])
        return self.request('GET', full_url, params={'startTime': start_time,
                                                     'endTime': end_time},
                            response_entity_type=LoadBalancerUsageList,
                            requestslib_kwargs=requestslib_kwargs)

    def update_load_balancer_status_active(self, lb_id,
                                           requestslib_kwargs=None):
        full_url = '/'.join([self.url, self._LOADBALANCERS, str(lb_id),
                             self._SETSTATUS, 'ACTIVE'])
        return self.request('PUT', full_url, response_entity_type=None,
                            requestslib_kwargs=requestslib_kwargs)

    def update_load_balancer_status_build(self, lb_id,
                                          requestslib_kwargs=None):
        full_url = '/'.join([self.url, self._LOADBALANCERS, str(lb_id),
                             self._SETSTATUS, 'BUILD'])
        return self.request('PUT', full_url, response_entity_type=None,
                            requestslib_kwargs=requestslib_kwargs)

    def update_load_balancer_status_deleted(self, lb_id,
                                            requestslib_kwargs=None):
        full_url = '/'.join([self.url, self._LOADBALANCERS, str(lb_id),
                             self._SETSTATUS, 'DELETED'])
        return self.request('PUT', full_url, response_entity_type=None,
                            requestslib_kwargs=requestslib_kwargs)

    def update_load_balancer_status_error(self, lb_id,
                                          requestslib_kwargs=None):
        full_url = '/'.join([self.url, self._LOADBALANCERS, str(lb_id),
                             self._SETSTATUS, 'ERROR'])
        return self.request('PUT', full_url, response_entity_type=None,
                            requestslib_kwargs=requestslib_kwargs)

    def update_load_balancer_status_pending_delete(self, lb_id,
                                                   requestslib_kwargs=None):
        full_url = '/'.join([self.url, self._LOADBALANCERS, str(lb_id),
                             self._SETSTATUS, 'PENDING_DELETE'])
        return self.request('PUT', full_url, response_entity_type=None,
                            requestslib_kwargs=requestslib_kwargs)

    def update_load_balancer_status_pending_update(self, lb_id,
                                                   requestslib_kwargs=None):
        full_url = '/'.join([self.url, self._LOADBALANCERS, str(lb_id),
                             self._SETSTATUS, 'PENDING_UPDATE'])
        return self.request('PUT', full_url, response_entity_type=None,
                            requestslib_kwargs=requestslib_kwargs)

    def get_alerts(self, requestslib_kwargs=None):
        full_url = '/'.join([self.url, self._ALERTS])
        return self.request('GET', full_url, response_entity_type=AlertList,
                            requestslib_kwargs=requestslib_kwargs)

    def get_alert(self, alert_id, requestslib_kwargs=None):
        full_url = '/'.join([self.url, self._ALERTS, str(alert_id)])
        return self.request('GET', full_url, response_entity_type=Alert,
                            requestslib_kwargs=requestslib_kwargs)

    def get_alerts_on_load_balancer(self, lb_id, requestslib_kwargs=None):
        full_url = '/'.join([self.url, self._ALERTS, 'loadbalancer'])
        return self.request('GET', full_url, params={'id': str(lb_id)},
                            response_entity_type=AlertList,
                            requestslib_kwargs=requestslib_kwargs)

    def get_alerts_on_load_balancers(self, lb_id_list,
                                     requestslib_kwargs=None):
        full_url = '/'.join([self.url, self._ALERTS, 'byloadbalancerids'])
        return self.request('GET', full_url, params={'id': lb_id_list},
                            response_entity_type=AlertList,
                            requestslib_kwargs=requestslib_kwargs)

    def get_alerts_on_accounts(self, account_id_list, show_stack_trace=None,
                               requestslib_kwargs=None):
        full_url = '/'.join([self.url, self._ALERTS, 'account'])
        params = {'account': account_id_list}
        if show_stack_trace is not None:
            params['showStackTrace'] = str(show_stack_trace)
        return self.request('GET', full_url, params=params,
                            response_entity_type=AlertList,
                            requestslib_kwargs=requestslib_kwargs)

    def get_alerts_on_cluster(self, cluster_id, requestslib_kwargs=None):
        full_url = '/'.join([self.url, self._ALERTS, 'cluster',
                             str(cluster_id)])
        return self.request('GET', full_url, response_entity_type=AlertList,
                            requestslib_kwargs=requestslib_kwargs)

    def get_alerts_unacknowledged(self, requestslib_kwargs=None):
        full_url = '/'.join([self.url, self._ALERTS])
        params = {'status': 'UNACKNOWLEDGED'}
        return self.request('GET', full_url, params=params,
                            response_entity_type=AlertList,
                            requestslib_kwargs=requestslib_kwargs)

    def update_alert_to_acknowledged(self, alert_id, requestslib_kwargs=None):
        full_url = '/'.join([self.url, self._ALERTS, str(alert_id),
                             'acknowledged'])
        return self.request('PUT', full_url, response_entity_type=None,
                            requestslib_kwargs=requestslib_kwargs)

    def get_host_usage(self, start_date, end_date, requestslib_kwargs=None):
        full_url = '/'.join([self.url, self._HOSTS, self._USAGE])
        params = {'startDate': start_date, 'endDate': end_date}
        return self.request('GET', full_url, params=params,
                            response_entity_type=HostUsageRecords,
                            requestslib_kwargs=requestslib_kwargs)

    def get_events_on_load_balancer(self, account_id, requestslib_kwargs=None):
        full_url = '/'.join([self.url, self._EVENT, 'account', str(account_id),
                             'loadbalancer'])
        params = {}
        params['startDate'] = '2013-2-15'
        params['endDate'] = '2013-2-15'
        return self.request('GET', full_url, params=params,
                            response_entity_type=AccountLoadBalancerEventList,
                            requestslib_kwargs=requestslib_kwargs)

    def get_events_for_user(self, user_name, requestslib_kwargs=None):
        full_url = '/'.join([self.url, self._EVENT, 'user', str(user_name)])
        params = {}
        params['startDate'] = '2013-2-15'
        params['endDate'] = '2013-2-15'
        return self.request('GET', full_url, params=params,
                            response_entity_type=AccountLoadBalancerEventList,
                            requestslib_kwargs=requestslib_kwargs)

    def get_allowed_domains(self, name=None, requestslib_kwargs=None):
        full_url = '/'.join([self.url, self._ALLOWED_DOMAINS])
        params = {}
        if name is not None:
            params['matches'] = str(name)
        return self.request('GET', full_url, params=params,
                            response_entity_type=AllowedDomainList,
                            requestslib_kwargs=requestslib_kwargs)

    def add_allowed_domain(self, name, requestslib_kwargs=None):
        full_url = '/'.join([self.url, self._ALLOWED_DOMAINS])
        domain = AllowedDomain(name=name)
        return self.request('PUT', full_url,
                            request_entity=domain,
                            response_entity_type=None,
                            requestslib_kwargs=requestslib_kwargs)

    def delete_allowed_domain(self, name, requestslib_kwargs=None):
        full_url = '/'.join([self.url, self._ALLOWED_DOMAINS])
        params = {'name': str(name)}
        return self.request('DELETE', full_url, params=params,
                            response_entity_type=None,
                            requestslib_kwargs=requestslib_kwargs)

    def get_blacklist(self, requestslib_kwargs=None):
        full_url = '/'.join([self.url, self._BLACKLIST])
        return self.request('GET', full_url,
                            response_entity_type=Blacklist,
                            requestslib_kwargs=requestslib_kwargs)

    def add_blacklist_item(self, cidr_block, ip_version, type=None,
                           requestslib_kwargs=None):
        full_url = '/'.join([self.url, self._BLACKLIST])
        body = Blacklist([BlacklistItem(cidrBlock=cidr_block,
                                        ipVersion=ip_version, type=type)])
        return self.request('POST', full_url,
                            request_entity=body,
                            response_entity_type=None,
                            requestslib_kwargs=requestslib_kwargs)

    def delete_blacklist_item(self, item_id,
                              requestslib_kwargs=None):
        full_url = '/'.join([self.url, self._BLACKLIST, str(item_id)])
        return self.request('DELETE', full_url,
                            response_entity_type=None,
                            requestslib_kwargs=requestslib_kwargs)

    def get_jobs(self, state=None, requestslib_kwargs=None):
        full_url = '/'.join([self.url, self._JOBS])
        params = {}
        if state is not None:
            params['state'] = state
        return self.request('GET', full_url, params=params,
                            response_entity_type=JobList,
                            requestslib_kwargs=requestslib_kwargs)

    def get_job(self, job_id, requestslib_kwargs=None):
        full_url = '/'.join([self.url, self._JOBS, str(job_id)])
        return self.request('GET', full_url, response_entity_type=Job,
                            requestslib_kwargs=requestslib_kwargs)

    def get_hosts_capacity_report(self, requestslib_kwargs=None):
        full_url = '/'.join([self.url, self._HOSTS, self._HOST_CAPACITY])
        return self.request('GET', full_url,
                            response_entity_type=HostCapacityReportList,
                            requestslib_kwargs=requestslib_kwargs)

    def get_host_capacity_report(self, host_id, requestslib_kwargs=None):
        full_url = '/'.join([self.url, self._HOSTS, str(host_id),
                             self._HOST_CAPACITY])
        return self.request('GET', full_url,
                            response_entity_type=HostCapacityReportList,
                            requestslib_kwargs=requestslib_kwargs)

    def get_vip_availability_report(self, requestslib_kwargs=None):
        full_url = '/'.join([self.url, self._VIRTUALIPS,
                             self._VIP_AVAILABILITY])
        return self.request('GET', full_url,
                            response_entity_type=
                            VirtualIpAvailabilityReportList,
                            requestslib_kwargs=requestslib_kwargs)

    def get_cluster_vip_availability_report(self, cluster_id,
                                            requestslib_kwargs=None):
        full_url = '/'.join([self.url, self._CLUSTERS, str(cluster_id),
                             self._VIRTUALIPS, self._VIP_AVAILABILITY])
        return self.request('GET', full_url,
                            response_entity_type=
                            VirtualIpAvailabilityReportList,
                            requestslib_kwargs=requestslib_kwargs)

    def get_load_balancer_audit(self, status, changes_since=None,
                                requestslib_kwargs=None):
        full_url = '/'.join([self.url, 'audit', 'status'])
        params = {'status': status}
        if changes_since is not None:
            params['changes-since'] = changes_since
        return self.request('GET', full_url, params=params,
                            response_entity_type=LoadBalancerAuditList,
                            requestslib_kwargs=requestslib_kwargs)

    def get_load_balancer_state_history(self, account_id,
                                        requestslib_kwargs=None):
        full_url = '/'.join([self.url, self._LOADBALANCERS, str(account_id),
                             'lbstatehistory'])
        return self.request('GET', full_url,
                            response_entity_type=LoadBalancerStatusHistoryList,
                            requestslib_kwargs=requestslib_kwargs)

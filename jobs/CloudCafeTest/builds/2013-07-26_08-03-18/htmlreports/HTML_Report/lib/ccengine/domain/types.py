'''
@summary: Types applicable to any L{ccengine.domain} object
@copyright: Copyright (c) 2012 Rackspace US, Inc.
'''


class NovaServerStatusTypes(object):
    '''
    @summary: Types dictating an individual Server Status
    @cvar ACTIVE: Server is active and available
    @type ACTIVE: C{str}
    @cvar BUILD: Server is being built
    @type BUILD: C{str}
    @cvar ERROR: Server is in error
    @type ERROR: C{str}
    @note: This is essentially an Enumerated Type
    '''
    ACTIVE = "ACTIVE"
    BUILD = "BUILD"
    REBUILD = "REBUILD"
    ERROR = "ERROR"
    DELETING = "DELETING"
    DELETED = "DELETED"
    RESCUE = "RESCUE"
    PREP_RESCUE = "PREP_RESCUE"
    INVALID_OPTION = "INVALID_OPTION"
    RESIZE = "RESIZE"
    VERIFY_RESIZE = "VERIFY_RESIZE"


class NovaImageStatusTypes(object):
    '''
    @summary: Types dictating an individual Server Status
    @cvar ACTIVE: Server is active and available
    @type ACTIVE: C{str}
    @cvar BUILD: Server is being built
    @type BUILD: C{str}
    @cvar ERROR: Server is in error
    @type ERROR: C{str}
    @note: This is essentially an Enumerated Type
    '''
    ACTIVE = "ACTIVE"
    SAVING = "SAVING"
    ERROR = "ERROR"
    DELETED = "DELETED"
    UNKNOWN = "UNKNOWN"


class NovaManagedMetaStatusTypes(object):
    '''
    @summary: Types dictating an individual Managed Server Status
    @cvar ACTIVE: Managed Server is active and available
    @type ACTIVE: C{str}
    @cvar PROGRESS: Server is being prepared
    @type PROGRESS: C{str}
    @cvar ERROR: Server is in error
    @type ERROR: C{str}
    @note: This is essentially an Enumerated Type
    '''
    ACTIVE = "Complete"
    PROGRESS = "In Progress"
    ERROR = "Build Error"

class NovaRackConnectAutomationStatusTypes(object):
    '''
    @summary: Types dictating an individual Managed Server Status
    @cvar ACTIVE: Server is deployed
    @type ACTIVE: C{str}
    @cvar PROGRESS: Server is being deployed
    @type PROGRESS: C{str}
    @note: This is essentially an Enumerated Type
    '''
    ACTIVE = "DEPLOYED"
    PROGRESS = "DEPLOYING"


class NovaServerRebootTypes(object):
    '''
    @summary: Types dictating server reboot types
    @cvar HARD: Hard reboot
    @type HARD: C{str}
    @cvar SOFT: Soft reboot
    @type SOFT: C{str}
    @note: This is essentially an Enumerated Type
    '''
    HARD = "HARD"
    SOFT = "SOFT"


class NovaVolumeStatusTypes(object):
    '''
    @summary: Types dictating an individual Volume Status
    @cvar AVAILABLE: Volume is active and available
    @type AVAILABLE: C{str}
    @cvar CREATING: Volume is being created
    @type CREATING: C{str}
    @cvar ERROR: Volume is in error
    @type ERROR: C{str}
    @cvar DELETING: Volume is being deleted
    @type DELETING: C{str}
    @cvar ERROR_DELETING: Volume is in error while being deleted
    @type ERROR_DELETING: C{str}
    @cvar IN_USE: Volume is active and available
    @type IN_USE: C{str}
    @note: This is essentially an Enumerated Type
    '''
    AVAILABLE = "available"
    ATTACHING = "attaching"
    CREATING = "creating"
    DELETING = "deleting"
    ERROR = "error"
    ERROR_DELETING = "error_deleting"
    IN_USE = "in-use"


class NovaVolumeSnapshotStatusTypes(object):
    '''
    @summary: Types dictating an individual Volume Status
    @cvar AVAILABLE: Volume Snapshot is active and available
    @type AVAILABLE: C{str}
    @cvar CREATING: Volume Snapshot is being created
    @type CREATING: C{str}
    @cvar DELETING: Volume Snapshot is deleting
    @type DELETING: C{str}
    @cvar ERROR: Volume Snapshot is in error
    @type ERROR: C{str}
    @cvar ERROR_DELETING: Volume Snapshot is in error while being deleted
    @type ERROR_DELETING: C{str}
    @note: This is essentially an Enumerated Type
    '''
    AVAILABLE = "available"
    CREATING = "creating"
    DELETING = "deleting"
    ERROR = "error"
    ERROR_DELETING = "error_deleting"


class LunrVolumeStatusTypes(object):
    '''
    @summary: Types dictating an individual Volume Status returned from Lunr
    @cvar READY: Volume is ready for use
    @type READY: C{str}
    @cvar DELETING: Volume is deleting
    @type DELETING: C{str}
    @cvar DELETED: Volume is marked as deleted
    @type DELETED: C{str}
    '''
    READY = 'ACTIVE'
    DELETING = 'DELETING'
    DELETED = 'DELETED'


class LunrBackupStatusTypes(object):
    '''
    @summary: Types dictating an individual Backup Status returned from Lunr
    @cvar READY: Backup is ready for use
    @type READY: C{str}
    @cvar DELETING: Backup is deleting
    @type DELETING: C{str}
    @cvar DELETED: Backup is marked as deleted
    @type DELETED: C{str}
    '''
    READY = 'AVAILABLE'
    DELETING = 'DELETING'
    DELETED = 'DELETED'


class LavaClusterStatusTypes(object):
    '''
    @summary: Types dictating an individual Cluster Status returned from Lava
    @cvar READY: Backup is ready for use
    @type READY: C{str}
    @cvar DELETING: Backup is deleting
    @type DELETING: C{str}
    @cvar DELETED: Backup is marked as deleted
    @type DELETED: C{str}
    '''
    ACTIVE = 'ACTIVE'
    ERROR = 'ERROR'
    DELETED = 'DELETED'
    BUILD = 'BUILD'
    CONFIGURING = 'CONFIGURING',
    CONFIGURED = 'CONFIGURED'


class LoadBalancerStatusTypes(object):
    '''
    @summary: Types dictating an individual Load Balancer Status
    @cvar ACTIVE: Load balancer is ready for use
    @type ACTIVE: C{str}
    @cvar BUILD: Load balancer is building after being created.
    @type BUILD: C{str}
    @cvar PENDING_UPDATE: Load balancer is pending update.
    @type PENDING_UPDATE: C{str}
    @cvar PENDING_DELETE: Load balancer is waiting to be deleted.
    @type PENDING_DELETE: C{str}
    @cvar DELETED: Load balancer has been deleted.
    @type DELETED: C{str}
    @cvar ERROR: Load balancer errored for some reason.
    @type ERROR: C{str}
    @cvar SUSPENDED: Load balancer is suspended.
    @type SUSPENDED: C{str}
    '''
    ACTIVE = 'ACTIVE'
    BUILD = 'BUILD'
    PENDING_UPDATE = 'PENDING_UPDATE'
    PENDING_DELETE = 'PENDING_DELETE'
    DELETED = 'DELETED'
    ERROR = 'ERROR'
    SUSPENDED = 'SUSPENDED'


class LoadBalancerUsageEventTypes(object):
    '''
    @summary: Types dictating the events used for Load Balancer usage.
    @cvar CREATE_LOADBALANCER: Load balancer was created
    @type CREATE_LOADBALANCER: C{str}
    @cvar DELETE_LOADBALANCER: Load balancer was delete.
    @type DELETE_LAODBALANCER: C{str}
    @cvar CREATE_VIRTUAL_IP: Load balancer added a VIP.
    @type CREATE_VIRTUAL_IP: C{str}
    @cvar DELETE_VIRTUAL_IP: Load balancer deleted a VIP.
    @type DELETE_VIRTUAL_IP: C{str}
    @cvar SSL_ONLY_ON: Load balancer enabled SSL ONLY.
    @type SSL_ONLY_ON: C{str}
    @cvar SSL_MIXED_ON: Load balancer enabled SSL_MIXED
    @type SSL_MIXED_ON: C{str}
    @cvar SSL_OFF: Load balancer disabled SSL Termination.
    @type SSL_OFF: C{str}
    @cvar SUSPEND_LOADBALANCER: Load balancer was suspended.
    @type SUSPEND_LOADBALANCER: C{str}
    @cvar SUSPENDED_LOADBALANCER: Load balancer is suspended.
    @type SUSPENDED_LOADBALANCER: C{str}
    @cvar UNSUSPEND_LOADBALANCER: Load balancer was unsuspended.
    @type UNSUSPEND_LOADBALANCER: C{str}
    '''
    CREATE_LOADBALANCER = 'CREATE_LOADBALANCER'
    DELETE_LOADBALANCER = 'DELETE_LOADBALANCER'
    CREATE_VIRTUAL_IP = 'CREATE_VIRTUAL_IP'
    DELETE_VIRTUAL_IP = 'DELETE_VIRTUAL_IP'
    SSL_ONLY_ON = 'SSL_ONLY_ON'
    SSL_MIXED_ON = 'SSL_MIXED_ON'
    SSL_OFF = 'SSL_OFF'
    SUSPEND_LOADBALANCER = 'SUSPEND_LOADBALANCER'
    SUSPENDED_LOADBALANCER = 'SUSPENDED_LOADBALANCER'
    UNSUSPEND_LOADBALANCER = 'UNSUSPEND_LOADBALANCER'


class LoadBalancerVirtualIpTypes(object):
    '''
    @summary: Types dictating the virtual IP types for a load balancer.
    @cvar SERVICENET: A virtual IP on servicenet
    @type SERVICENET: C{str}
    @cvar PUBLIC: A virtual IP with a public address.
    @type PUBLIC: C{str}
    '''
    SERVICENET = 'SERVICENET'
    PUBLIC = 'PUBLIC'


class LoadBalancerVirtualIpVersions(object):
    '''
    @summary: Types dictating the virtual IP versions for a load balancer.
    @cvar IPV4: IP Version 4
    @type IPV4: C{str}
    @cvar IPV6: IP Version 6
    @type IPV6: C{str}
    '''
    IPV4 = 'IPV4'
    IPV6 = 'IPV6'


class LoadBalancerNodeConditions(object):
    '''
    @summary: Types dictating the node conditions of a load balancer.
    @cvar ENABLED: Node is enabled and being load balanced.
    @type ENABLED: C{str}
    @cvar DISABLED: Node is disabled and out of load balancing rotation.
    @type DISABLED: C{str}
    @cvar DRAINING: Node is no longer in rotation and serving remaining traffic
    @type DRAINING: C{str}
    '''
    ENABLED = 'ENABLED'
    DISABLED = 'DISABLED'
    DRAINING = 'DRAINING'


class LoadBalancerNodeTypes(object):
    '''
    @summary: Types dictating the node types of a load balancer.
    @cvar PRIMARY: Node is a primary node.
    @type PRIMARY: C{str}
    @cvar SECONDARY: Node is a secondary node (backup node).
    @type SECONDARY: C{str}
    '''
    PRIMARY = 'PRIMARY'
    SECONDARY = 'SECONDARY'


class LoadBalancerNodeStatus(object):
    '''
    @summary: Types dictating the node status of a load balancer.
    @cvar ONLINE: Node is online and able to serve traffic.
    @type ONLINE: C{str}
    @cvar OFFLINE: Node is offline and unable to serve traffic.
    @type OFFLINE: C{str}
    @cvar DRAINING: Node is being removed from rotation..
    @type DRAINING: C{str}
    '''
    ONLINE = 'ONLINE'
    OFFLINE = 'OFFLINE'
    DRAINING = 'DRAINING'


class LoadBalancerSslModes(object):
    '''
    @summary: Types dictating the SSL Termination modes of a load balancer.
    @cvar MIXED: Load balancer is able to serve normal and ssl traffic.
    @type MIXED: C{str}
    @cvar ON: Load balancer only serves ssl traffic.
    @type ON: C{str}
    @cvar OFF: Load balancer only serves normal traffic.
    @type OFF: C{str}
    '''
    MIXED = 'MIXED'
    ON = 'ON'
    OFF = 'OFF'


class LoadBalancerAccessListTypes(object):
    '''
    @summary: Types dictating access list types.
    @cvar ALLOW: Address is allowed.
    @type ALLOW: C{str}
    @cvar DENY: Address is blocked.
    @type DENY: C{str}
    '''
    ALLOW = 'ALLOW'
    DENY = 'DENY'


class LoadBalancerHealthMonitorTypes(object):
    '''
    @summary: Types dictating the health monitor types of a load balancer.
    @cvar CONNECT: Connect Health Monitor, for non HTTP and non HTTPS LBs.
    @type CONNECT: C{str}
    @cvar HTTP: health monitor for HTTP load balancers.
    @type HTTP: C{str}
    @cvar HTTPS: Health Monitor for HTTPS load balancers.
    @type HTTPS: C{str}
    '''
    CONNECT = 'CONNECT'
    HTTP = 'HTTP'
    HTTPS = 'HTTPS'


class LoadBalancerSessionPersistenceTypes(object):
    '''
    @summary: Types dictating the persistence types of session persistence.
    @cvar SOURCE_IP: Always persists to the same IP.
    @type SOURCE_IP: C{str}
    @cvar HTTP_COOKIE: Persists connections with a cookie.
    @type HTTP_COOKIE: C{str}
    '''
    SOURCE_IP = 'SOURCE_IP'
    HTTP_COOKIE = 'HTTP_COOKIE'


class LoadBalancerAtomHopperEvents(object):
    '''
    @summary: Types dictating the event types Atom Hopper expects.
    @cvar DELETE: Delete event for a load balancer that got deleted.
    @type DELETE: C{str}
    '''
    DELETE = 'DELETE'


class LoadBalancerAtomHopperStatusTypes(object):
    '''
    @summary: Types dictating the load balancer statuses Atom Hopper expects.
    @cvar ACTIVE: Load balancer is active.
    @type ACTIVE: C{str}
    @cvar SUSPENDED: Load balancer is suspended.
    @type SUSPENDED: C{str}
    '''
    ACTIVE = 'ACTIVE'
    SUSPENDED = 'SUSPENDED'


class CinderSnapshotStatusTypes(object):
    '''
    @summary: Types dictating a Snapshot Status returned from Cinder
    @cvar AVAILABLE: Snapshot is available for use
    @type AVAILALBE: C{str}
    '''
    AVAILABLE = 'available'


class LavaJobStatusTypes(object):
    '''
    @summary: Types dictating a Job Status returned from Lava
    @cvar STARTING: Job is preparing to run
    @type STARTING: C{str}
    @cvar ERROR: Job encountered an error
    @type ERROR: C{str}
    @cvar RUNNING: Job is running
    @type RUNNING: C{str}
    @cvar FINISHED: Job has run
    @type FINISHED: C{str}
    '''
    STARTING = 'Starting'
    ERROR = 'Error'
    RUNNING = 'Running'
    FINISHED = 'Finished'


class LavaClusterTypes(object):
    '''
    @summary: Type of cluster return from Lava
    @cvar RAW: 'raw' cluster type
    @type RAW: C{str}
    @cvar HADOOP_CLOUDERA: 'hadoop_cdh3' cluster type
    @type HADOOP_CLOUDERA: C{str}
    @cvar HADOOP_HDP: 'hadoop_hdp1_1' cluster type
    @type HADOOP_HDP: C{str}
    @cvar HBASE_CLOUDERA: 'hbase_cdh3' cluster type
    @type HBASE_CLOUDERA: C{str}
    @cvar HBASE_HDP: 'hbase_hdp1_1' cluster type
    @type HBASE_HDP: C{str}
    '''
    RAW = 'raw'
    HADOOP_CLOUDERA = 'HADOOP_CDH3'
    HADOOP_HDP = 'HADOOP_HDP1_1'
    HBASE_CLOUDERA = 'HBASE_CDH3'
    HBASE_HDP = 'HBASE_HDP1_1'


class LegacyServerStatusTypes(object):
    ACTIVE = 'ACTIVE'
    BUILD = 'BUILD'
    ERROR = 'ERROR'


class DnsaasAsyncStatusTypes(object):
    COMPLETE = 'COMPLETE'
    ERROR = 'ERROR'


class ScheduledImagesJobStatus(object):
    '''
    @summary: Types dictating the job status of a scheduled images.
    '''
    QUEUED = 'QUEUED'
    PROCESSING = 'PROCESSING'
    DONE = 'DONE'
    ERROR = 'ERROR'
    CANCELLED = 'CANCELLED'
    TIMED_OUT = 'TIMED_OUT'

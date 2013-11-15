import os


class UsageKeys(object):

    SSL_SITE_PREFIX = 'sslterm'

    USAGE_DATA_PATH = os.getcwd()
    USAGE_DATA_FILENAME = 'usage_data.usage_out'
    ACC_FILENAME = 'acc.usage_out'
    UPTIME_FILENAME = 'uptime.usage_out'
    EVENTS_FILENAME = 'events.usage_out'
    BANDWIDTH_FILENAME = 'bandwidth.usage_out'

    GENERATED_NUM_CONNECTIONS = 100

    SMALL_FILENAME = 'small.iso'
    MEDIUM_FILENAME = 'medium.iso'
    LARGE_FILENAME = 'large.iso'

    LOAD_BALANCER_ID_FIELD = 'lb_id'
    CREATE_TIME = 'createTime'
    AVERAGE_NUM_CONNECTIONS = "averageNumConnections"
    BANDWIDTH_OUT_FIELD = 'outgoingTransfer'
    BANDWIDTH_IN_FIELD = 'incomingTransfer'
    BANDWIDTH_OUT_SSL_FIELD = 'outgoingTransferSsl'
    BANDWIDTH_IN_SSL_FIELD = 'incomingTransferSsl'
    SSL_ON_TIME = 'sslOnTime'
    SSL_OFF_TIME = 'sslOffTime'
    NUM_POLLS = "numPolls"
    START_TIME = "startTime"
    END_TIME = "endTime"
    EVENT_TYPE = "eventType"
    NUM_VIPS = 'numVips'
    VIP_TYPE = 'vipType'
    SSL_MODE = 'sslMode'
    BANDWIDTH_OUT_FIELD_2 = "outgoingTransfer2"
    BANDWIDTH_IN_FIELD_2 = "incomingTransfer2"
    BANDWIDTH_OUT_FIELD_3 = "outgoingTransfer3"
    BANDWIDTH_IN_FIELD_3 = "incomingTransfer3"
    BANDWIDTH_OUT_SSL_FIELD_2 = "outgoingTransferSsl2"
    BANDWIDTH_IN_SSL_FIELD_2 = "incomingTransferSsl2"
    BANDWIDTH_OUT_SSL_FIELD_3 = "outgoingTransferSsl3"
    BANDWIDTH_IN_SSL_FIELD_3 = "incomingTransferSsl3"

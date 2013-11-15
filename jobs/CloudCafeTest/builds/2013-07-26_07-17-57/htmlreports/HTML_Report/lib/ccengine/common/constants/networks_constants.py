class Constants(object):
    PUBLIC_NETWORK_ID = '00000000-0000-0000-0000-000000000000'
    PRIVATE_NETWORK_ID = '11111111-1111-1111-1111-111111111111'
    DELETE_SERVER_TIMEOUT = 30
    FLAVOR_QOS_RATES = {'2': 20480,
                        '3': 0,
                        '4': 0,
                        '5': 0,
                        '6': 0,
                        '7': 0,
                        '8': 0}


class HTTPResponseCodes(object):
    CREATE_NETWORK = 200
    LIST_NETWORKS = 200
    LIST_SERVERS = 200
    CREATE_SERVER = 202
    GET_NETWORK = 200
    GET_SERVER = 200
    DELETE_NETWORK = 202
    ADD_FIXED_IP = 202
    REMOVE_FIXED_IP = 202

    CREATE_INTERFACE = 200
    LIST_INTERFACES = 200
    DELETE_INTERFACE = 200

    NOT_FOUND = 404
    SERVER_ERROR = 500
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_ALLOWED = 405


class QuantumResponseCodes(object):
    """HTTP Response codes for the Quantum API V2.0"""
    LIST_NETWORKS = 200
    SHOW_NETWORK = 200
    CREATE_NETWORK = 201
    UPDATE_NETWORK = 200
    DELETE_NETWORK = 204
    LIST_SUBNETS = 200
    SHOW_SUBNET = 200
    CREATE_SUBNET = 201
    UPDATE_SUBNET = 200
    DELETE_SUBNET = 204
    LIST_PORTS = 200
    SHOW_PORT = 200
    CREATE_PORT = 201
    UPDATE_PORT = 200
    DELETE_PORT = 204

    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    NETWORK_IN_USE = 409
    CONFLICT = 409
    MAC_GENERATION_FAILURE = 503


class QOS(object):
    """NVP Switch port Logical Queue expected data based on server flavors"""
    class Two(object):
        """Logical Queue Switch Port data for flavor 2 (512MB)"""
        class Public(object):
            min_bw_rate = 0
            max_bw_rate = 20480
            qos_marking = 'untrusted'
            dscp = 0

        class Private(object):
            min_bw_rate = 0
            max_bw_rate = 40960
            qos_marking = 'untrusted'
            dscp = 0

        class isolated(object):
            pass

    class Three(object):
        """Logical Queue Switch Port data for flavor 3 (512MB)"""
        class Public(object):
            min_bw_rate = 0
            max_bw_rate = 30720
            qos_marking = 'untrusted'
            dscp = 0

        class Private(object):
            min_bw_rate = 0
            max_bw_rate = 61440
            qos_marking = 'untrusted'
            dscp = 0

        class isolated(object):
            pass
    #TODO: add data for flavors 4, 5, 6, 7 & 8

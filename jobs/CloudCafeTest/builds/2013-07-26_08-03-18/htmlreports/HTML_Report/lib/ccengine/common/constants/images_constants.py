class Constants(object):
    DELETE_SCHEDULE_TIMEOUT = 30
    ID_RE = '^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$'
    MESSAGE = "Unexpected {0} value received. Expected: {1}, Received: {2}"
    MESSAGE_ALT = "Unexpected {0} value received. Expected: {1} or {2}, Received: {3}"
    NOT_FOUND_ERROR_MESSAGE = "NOT FOUND"
    XML_API_NAMESPACE = 'http://docs.openstack.org/common/api/v1.0'
    XML_API_SCH_IMG_NAMESPACE = 'http://docs.openstack.org/servers/api/ext/scheduled_images/v1.0'
    XML_API_ATOM_NAMESPACE = 'http://www.w3.org/2005/Atom'
    XML_HEADER = "<?xml version='1.0' encoding='UTF-8'?>"

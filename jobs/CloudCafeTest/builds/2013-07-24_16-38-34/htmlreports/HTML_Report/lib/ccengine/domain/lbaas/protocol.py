from ccengine.domain.base_domain import BaseMarshallingDomain, \
    BaseMarshallingDomainList
import json
import xml.etree.ElementTree as ET


class ProtocolList(BaseMarshallingDomainList):

    ROOT_TAG = 'protocols'

    def __init__(self, protocols=[]):
        super(ProtocolList, self).__init__()
        for protocol in protocols:
            self.append(protocol)

    def contains(self, name, port=None):
        for protocol in self:
            if protocol.name == name and port is None:
                return True
            elif protocol.name == name and protocol.port == port:
                return True
        return False

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        if cls.ROOT_TAG not in json_dict:
            return None
        return cls._dict_to_obj(json_dict.get(cls.ROOT_TAG))

    @classmethod
    def _dict_to_obj(cls, protocol_dict):
        kwargs = {cls.ROOT_TAG: [Protocol._dict_to_obj(protocol)
                                 for protocol in protocol_dict]}
        return ProtocolList(**kwargs)

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        pass


class Protocol(BaseMarshallingDomain):

    ROOT_TAG = ''

    def __init__(self, name=None, port=None):
        self.name = name
        self.port = port

    _protocol_zeus_dict = {'HTTP': 'http',
                           'FTP': 'ftp',
                           'IMAPv2': 'imapv2',
                           'IMAPv3': 'imapv3',
                           'IMAPv4': 'imapv4',
                           'POP3': 'pop3',
                           'SMTP': 'smtp',
                           'LDAP': 'ldap',
                           'HTTPS': 'https',
                           'IMAPS': 'imaps',
                           'POP3S': 'pop3s',
                           'LDAPS': 'ldaps',
                           'DNS_TCP': 'dns_tcp',
                           'DNS_UDP': 'dns',
                           'TCP_CLIENT_FIRST': 'client_first',
                           'UDP': 'udp',
                           'UDP_STREAM': 'udpstreaming',
                           'MYSQL': 'server_first',
                           'TCP': 'server_first',
                           'SFTP': 'server_first'}

    @classmethod
    def zeus_name(cls, name=None):
        if name is None:
            return cls._protocol_zeus_dict.get(cls.name)
        else:
            return cls._protocol_zeus_dict.get(name)

    @classmethod
    def _json_to_obj(cls, serialized_str):
        pass

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        pass

    @classmethod
    def _dict_to_obj(cls, dic):
        return Protocol(**dic)

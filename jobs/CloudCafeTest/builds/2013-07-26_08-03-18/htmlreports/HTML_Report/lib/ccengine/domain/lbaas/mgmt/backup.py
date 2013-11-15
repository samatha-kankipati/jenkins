from ccengine.domain.base_domain import BaseMarshallingDomain
from ccengine.domain.base_domain import BaseMarshallingDomainList
import xml.etree.ElementTree as ET
import json


class BackupList(BaseMarshallingDomainList):

    ROOT_TAG = 'backups'

    def __init__(self, backups=None):
        '''A list of host backups

        '''
        for backup in backups:
            self.append(backup)

    def _obj_to_json(self):
        ret = self._auto_to_dict()
        return json.dumps(ret[self.ROOT_TAG])

    def _obj_to_xml(self):
        ret = self._auto_to_xml()
        return ET.tostring(ret)

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        return cls._dict_to_obj(json_dict)

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        pass

    @classmethod
    def _dict_to_obj(cls, dic):
        kwargs = {cls.ROOT_TAG: [Backup._dict_to_obj(backup)
                                 for backup in dic.get(cls.ROOT_TAG)]}
        return BackupList(**kwargs)


class Backup(BaseMarshallingDomain):

    ROOT_TAG = 'backup'

    def __init__(self, id=None, name=None, backupTime=None, hostId=None):
        '''An object providing details about a backup of a host

        '''
        self.id = id
        self.name = name
        self.backupTime = backupTime
        self.hostId = hostId

    def _obj_to_json(self):
        ret = self._auto_to_dict()
        return json.dumps(ret[self.ROOT_TAG])

    def _obj_to_xml(self):
        ret = self._auto_to_xml()
        return ET.tostring(ret)

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        return cls._dict_to_obj(json_dict)

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        pass

    @classmethod
    def _dict_to_obj(cls, dic):
        return Backup(**dic)

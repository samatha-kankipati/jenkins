from ccengine.domain.base_domain import BaseMarshallingDomain
import json
import xml.etree.ElementTree as ET
from ccengine.common.constants.compute_constants import Constants
from ccengine.domain.compute.metadata import Metadata


class CreateServer(BaseMarshallingDomain):
    ROOT_TAG = 'server'

    def __init__(self, name, imageRef, flavorRef, adminPass=None,
                 diskConfig=None, metadata=None, personality=None,
                 accessIPv4=None, accessIPv6=None, networks=None,
                 min_count=None, max_count=None, key_name=None):

        super(CreateServer, self).__init__()
        self.name = name
        self.imageRef = imageRef
        self.flavorRef = flavorRef
        self.diskConfig = diskConfig
        self.adminPass = adminPass
        self.metadata = metadata
        self.personality = personality
        self.accessIPv4 = accessIPv4
        self.accessIPv6 = accessIPv6
        self.min_count = min_count
        self.max_count = max_count
        self.networks = networks
        self.key_name = key_name

    def _obj_to_json(self):
        ret = self._auto_to_dict()
        for _, serv_dict in ret.iteritems():
            value = serv_dict.get('diskConfig')
        if value is not None:
            ret[self.ROOT_TAG]['OS-DCF:diskConfig'] = value
        return json.dumps(ret)

    def _obj_to_xml(self):
        element = ET.Element(self.ROOT_TAG)
        xml = Constants.XML_HEADER
        element.set('xmlns', Constants.XML_API_NAMESPACE)
        element.set('name', self.name)
        element.set('imageRef', self.imageRef)
        element.set('flavorRef', self.flavorRef)
        if self.adminPass is not None:
            element.set('adminPass', self.adminPass)
        if self.diskConfig is not None:
            element.set('xmlns:OS-DCF',
                        Constants.XML_API_DISK_CONFIG_NAMESPACE)
            element.set('OS-DCF:diskConfig', self.diskConfig)
        if self.metadata is not None:
            meta_ele = ET.Element('metadata')
            for key, value in self.metadata.items():
                meta_ele.append(Metadata._dict_to_xml(key, value))
            element.append(meta_ele)
        if self.networks is not None:
            networks_ele = ET.Element('networks')
            for network_id in self.networks:
                network = ET.Element('network')
                network.set('uuid', network_id['uuid'])
                networks_ele.append(network)
            element.append(networks_ele)
        if self.personality is not None:
            personality_ele = ET.Element('personality')
            personality_ele.append(Personality._obj_to_xml(self.personality))
            element.append(personality_ele)
        if self.accessIPv4 is not None:
            element.set('accessIPv4', self.accessIPv4)
        if self.accessIPv6 is not None:
            element.set('accessIPv6', self.accessIPv6)
        xml += ET.tostring(element)
        return xml


class UpdateServer(BaseMarshallingDomain):

    ROOT_TAG = 'server'

    def __init__(self, name=None, metadata=None,
                 accessIPv4=None, accessIPv6=None):
        self.name = name
        self.metadata = metadata
        self.accessIPv4 = accessIPv4
        self.accessIPv6 = accessIPv6

    def _obj_to_json(self):
        return json.dumps(self._auto_to_dict())

    def _obj_to_xml(self):
        element = ET.Element(self.ROOT_TAG)
        xml = Constants.XML_HEADER
        element.set('xmlns', Constants.XML_API_NAMESPACE)
        if self.name is not None:
            element.set('name', self.name)
        if self.metadata is not None:
            meta_ele = ET.Element('metadata')
            for key, value in self.metadata.items():
                meta_ele.append(Metadata._dict_to_xml(key, value))
            element.append(meta_ele)
        if self.accessIPv4 is not None:
            element.set('accessIPv4', self.accessIPv4)
        if self.accessIPv6 is not None:
            element.set('accessIPv6', self.accessIPv6)
        xml += ET.tostring(element)
        return xml


class Reboot(BaseMarshallingDomain):
    ROOT_TAG = 'reboot'
    '''
    Reboot Request Object , Server action
    '''

    def __init__(self, reboot_type):
        self.type = reboot_type

    def _obj_to_json(self):
        ret = self._auto_to_dict()
        return json.dumps(ret)

    def _obj_to_xml(self):
        xml = Constants.XML_HEADER
        element = ET.Element(self.ROOT_TAG)
        element.set('xmlns', Constants.XML_API_NAMESPACE)
        element.set('type', self.type)
        xml += ET.tostring(element)
        return xml


class Personality(BaseMarshallingDomain):
    '''
    @summary: Personality Request Object for Server
    '''
    ROOT_TAG = 'personality'

    def __init__(self, type):
        self.type = type

    @classmethod
    def _obj_to_json(self):
        ret = self._auto_to_dict()
        return json.dumps(ret)

    @classmethod
    def _obj_to_xml(self, list_dicts):
        for pers_dict in list_dicts:
            pers_element = ET.Element('file')
            pers_element.set('path', pers_dict.get('path'))
            pers_element.text = pers_dict.get('contents')
        return pers_element


class Rebuild(CreateServer):
    '''
    @summary: Rebuild Request Object for Server
    '''

    ROOT_TAG = 'rebuild'

    def __init__(self, name, imageRef, flavorRef, adminPass, diskConfig=None,
                 metadata=None, personality=None, accessIPv4=None,
                 accessIPv6=None):
        super(Rebuild, self).__init__(name=name, imageRef=imageRef,
                                      flavorRef=flavorRef, adminPass=adminPass,
                                      diskConfig=diskConfig, metadata=metadata,
                                      personality=personality,
                                      accessIPv4=accessIPv4,
                                      accessIPv6=accessIPv6)

#    def _obj_to_json(self):
#        ret = self._auto_to_dict()
#        value = ret.pop('diskConfig', None)
#        ret['OS-DCF:diskConfig'] = value
#        return json.dumps(ret)

#    def _obj_to_xml(self):
#        element = ET.Element(self.ROOT_TAG)
#        #TODO: Put this in an enumerated string accessible everywhere
#        xml = Constants.XML_HEADER
#        element.set('xmlns', Constants.XML_API_NAMESPACE)
#        element.set('name', self.name)
#        element.set('imageRef', self.imageRef)
#        element.set('flavorRef', self.flavorRef)
#        element.set('adminPass', self.adminPass)
#        if self.diskConfig is not None:
#            element.set('xmlns:OS-DCF',
#                         Constants.XML_API_DISK_CONFIG_NAMESPACE)
#            element.set('OS-DCF:diskConfig', self.diskConfig)
#        if self.metadata is not None:
#            metadata_element = Metadata(self.metadata)
#        element.set('metadata', metadata_element)
#        element.set('personality', self.personality)
#        element.set('accessIPv4', self.accessIPv4)
#        element.set('accessIPv6', self.accessIPv6)
#
#        xml += ET.tostring(element)
#        return xml


class Resize(BaseMarshallingDomain):
    '''
    @summary: Resize Request Object for Server
    '''
    ROOT_TAG = 'resize'

    def __init__(self, flavorRef, diskConfig=None):
        self.flavorRef = flavorRef
        self.diskConfig = diskConfig

    def _obj_to_json(self):
        ret = self._auto_to_dict()
        return json.dumps(ret)

    def _obj_to_xml(self):
        xml = Constants.XML_HEADER
        element = ET.Element(self.ROOT_TAG)
        element.set('xmlns', Constants.XML_API_NAMESPACE)
        element.set('flavorRef', self.flavorRef)
        if self.diskConfig is not None:
            element.set('xmlns:OS-DCF', Constants.XML_API_ATOM_NAMESPACE)
            element.set('OS-DCF:diskConfig', self.diskConfig)
        xml += ET.tostring(element)
        return xml


class ResetState(BaseMarshallingDomain):
    '''
    @summary: Reset State Request Object for Server
    '''
    ROOT_TAG = 'os-resetState'

    def __init__(self, state):
        self.state = state

    def _obj_to_json(self):
        ret = self._auto_to_dict()
        return json.dumps(ret)

    def _obj_to_xml(self):
        xml = Constants.XML_HEADER
        element = ET.Element(self.ROOT_TAG)
        element.set('xmlns', Constants.XML_API_NAMESPACE)
        element.set('state', self.state)
        xml += ET.tostring(element)
        return xml


class ResetNetwork(BaseMarshallingDomain):
    '''
    @summary: Reset Network Request Object for Server
    '''
    ROOT_TAG = 'resetNetwork'

    def _obj_to_json(self):
        ret = self._auto_to_dict()
        return json.dumps(ret)

    def _obj_to_xml(self):
        xml = Constants.XML_HEADER
        element = ET.Element(self.ROOT_TAG)
        element.set('xmlns', Constants.XML_API_NAMESPACE)
        xml += ET.tostring(element)
        return xml


class ConfirmResize(BaseMarshallingDomain):
    '''
    @summary: Confirm Resize Request Object for Server
    '''
    ROOT_TAG = 'confirmResize'

    def _obj_to_json(self):
        ret = self._auto_to_dict()
        return json.dumps(ret)

    def _obj_to_xml(self):
        xml = Constants.XML_HEADER
#        element = self._auto_to_xml()
        element = ET.Element(self.ROOT_TAG)
        element.set('xmlns', Constants.XML_API_NAMESPACE)
        element.set('xmlns:atom', Constants.XML_API_ATOM_NAMESPACE)
        xml += ET.tostring(element)
        return xml


class RevertResize(BaseMarshallingDomain):
    '''
    @summary: Revert Resize Request Object for Server

    '''
    ROOT_TAG = 'revertResize'

    def _obj_to_json(self):
        ret = self._auto_to_dict()
        return json.dumps(ret)

    def _obj_to_xml(self):
        xml = Constants.XML_HEADER
        element = ET.Element(self.ROOT_TAG)
#        element = self._auto_to_xml()
        element.set('xmlns', Constants.XML_API_NAMESPACE)
        element.set('xmlns:atom', Constants.XML_API_ATOM_NAMESPACE)
        xml += ET.tostring(element)
        return xml


class MigrateServer(BaseMarshallingDomain):
    '''
    @summary: Migrate Server Request Object
    '''
    ROOT_TAG = 'migrate'

    def _obj_to_json(self):
        ret = self._auto_to_dict()
        return json.dumps(ret)

    def _obj_to_xml(self):
        xml = Constants.XML_HEADER
        element = self._auto_to_xml()
        element.set('xmlns', Constants.XML_API_NAMESPACE)
        element.set('xmlns:atom', Constants.XML_API_ATOM_NAMESPACE)
        xml += ET.tostring(element)
        return xml


class LiveMigrateServer(BaseMarshallingDomain):
    '''
    @summary: Live Migrate Server Request Object
    '''
    ROOT_TAG = 'os-migrateLive'

    def __init__(self, host=None,
                 block_migration=None,
                 disk_over_commit=None):
        self.host = host
        self.block_migration = block_migration
        self.disk_over_commit = disk_over_commit

    def _obj_to_json(self):
        ret = self._auto_to_dict()
        return json.dumps(ret)

    def _obj_to_xml(self):
        xml = Constants.XML_HEADER
        element = self._auto_to_xml()
        element.set('xmlns', Constants.XML_API_NAMESPACE)
        element.set('xmlns:atom', Constants.XML_API_ATOM_NAMESPACE)
        if self.host is not None:
            element.set('host', self.host)
        if self.block_migration is not None:
            element.set('block_migration', self.block_migration)
        if self.disk_over_commit is not None:
            element.set('disk_over_commit', self.disk_over_commit)
        xml += ET.tostring(element)
        return xml


class ConfirmServerMigration(BaseMarshallingDomain):
    '''
    @summary: Confirm Server Migration Request Object
    '''
    ROOT_TAG = 'confirmResize'

    def _obj_to_json(self):
        ret = self._auto_to_dict()
        return json.dumps(ret)

    def _obj_to_xml(self):
        xml = Constants.XML_HEADER
        element = self._auto_to_xml()
        element.set('xmlns', Constants.XML_API_NAMESPACE)
        element.set('xmlns:atom', Constants.XML_API_ATOM_NAMESPACE)
        xml += ET.tostring(element)
        return xml


class Lock(BaseMarshallingDomain):
    '''
    @summary: Lock Server Request Object
    '''
    ROOT_TAG = 'lock'

    def _obj_to_json(self):
        ret = self._auto_to_dict()
        return json.dumps(ret)

    def _obj_to_xml(self):
        xml = Constants.XML_HEADER
        element = self._auto_to_xml()
        element.set('xmlns', Constants.XML_API_NAMESPACE)
        element.set('xmlns:atom', Constants.XML_API_ATOM_NAMESPACE)
        xml += ET.tostring(element)
        return xml


class Unlock(BaseMarshallingDomain):
    '''
    @summary: Unlock Server Request Object
    '''
    ROOT_TAG = 'unlock'

    def _obj_to_json(self):
        ret = self._auto_to_dict()
        return json.dumps(ret)

    def _obj_to_xml(self):
        xml = Constants.XML_HEADER
        element = self._auto_to_xml()
        element.set('xmlns', Constants.XML_API_NAMESPACE)
        element.set('xmlns:atom', Constants.XML_API_ATOM_NAMESPACE)
        xml += ET.tostring(element)
        return xml


class Start(BaseMarshallingDomain):
    '''
    @summary: Start Server Request Object
    '''
    ROOT_TAG = 'os-start'

    def _obj_to_json(self):
        ret = self._auto_to_dict()
        return json.dumps(ret)

    def _obj_to_xml(self):
        xml = Constants.XML_HEADER
        element = self._auto_to_xml()
        element.set('xmlns', Constants.XML_API_NAMESPACE)
        element.set('xmlns:atom', Constants.XML_API_ATOM_NAMESPACE)
        xml += ET.tostring(element)
        return xml


class Stop(BaseMarshallingDomain):
    '''
    @summary: Stop Server Request Object
    '''
    ROOT_TAG = 'os-stop'

    def _obj_to_json(self):
        ret = self._auto_to_dict()
        return json.dumps(ret)

    def _obj_to_xml(self):
        xml = Constants.XML_HEADER
        element = self._auto_to_xml()
        element.set('xmlns', Constants.XML_API_NAMESPACE)
        element.set('xmlns:atom', Constants.XML_API_ATOM_NAMESPACE)
        xml += ET.tostring(element)
        return xml


class Suspend(BaseMarshallingDomain):
    '''
    @summary: Suspend Server Request Object
    '''
    ROOT_TAG = 'suspend'

    def _obj_to_json(self):
        ret = self._auto_to_dict()
        return json.dumps(ret)

    def _obj_to_xml(self):
        xml = Constants.XML_HEADER
        element = self._auto_to_xml()
        element.set('xmlns', Constants.XML_API_NAMESPACE)
        element.set('xmlns:atom', Constants.XML_API_ATOM_NAMESPACE)
        xml += ET.tostring(element)
        return xml


class Resume(BaseMarshallingDomain):
    '''
    @summary: Resume Server Request Object
    '''
    ROOT_TAG = 'resume'

    def _obj_to_json(self):
        ret = self._auto_to_dict()
        return json.dumps(ret)

    def _obj_to_xml(self):
        xml = Constants.XML_HEADER
        element = self._auto_to_xml()
        element.set('xmlns', Constants.XML_API_NAMESPACE)
        element.set('xmlns:atom', Constants.XML_API_ATOM_NAMESPACE)
        xml += ET.tostring(element)
        return xml


class Pause(BaseMarshallingDomain):
    '''
    @summary: Pause Server Request Object
    '''
    ROOT_TAG = 'pause'

    def _obj_to_json(self):
        ret = self._auto_to_dict()
        return json.dumps(ret)

    def _obj_to_xml(self):
        xml = Constants.XML_HEADER
        element = self._auto_to_xml()
        element.set('xmlns', Constants.XML_API_NAMESPACE)
        element.set('xmlns:atom', Constants.XML_API_ATOM_NAMESPACE)
        xml += ET.tostring(element)
        return xml


class Unpause(BaseMarshallingDomain):
    '''
    @summary: Unpause Server Request Object
    '''
    ROOT_TAG = 'unpause'

    def _obj_to_json(self):
        ret = self._auto_to_dict()
        return json.dumps(ret)

    def _obj_to_xml(self):
        xml = Constants.XML_HEADER
        element = self._auto_to_xml()
        element.set('xmlns', Constants.XML_API_NAMESPACE)
        element.set('xmlns:atom', Constants.XML_API_ATOM_NAMESPACE)
        xml += ET.tostring(element)
        return xml


class RescueMode(BaseMarshallingDomain):
    '''
    Rescue Server Action Request Object
    '''
    ROOT_TAG = 'rescue'

    def _obj_to_json(self):
        ret = self._auto_to_dict()
        return json.dumps(ret)

    def _obj_to_xml(self):
        xml = Constants.XML_HEADER
        element = ET.Element(self.ROOT_TAG)
        element.set('xmlns', Constants.XML_API_RESCUE)
        xml += ET.tostring(element)
        return xml


class ExitRescueMode(BaseMarshallingDomain):
    '''
    Exit Rescue Action Request Object
    '''
    ROOT_TAG = 'unrescue'

    def _obj_to_json(self):
        ret = self._auto_to_dict()
        return json.dumps(ret)

    def _obj_to_xml(self):
        xml = Constants.XML_HEADER
        element = ET.Element(self.ROOT_TAG)
        element.set('xmlns', Constants.XML_API_UNRESCUE)
        xml += ET.tostring(element)
        return xml


class CreateBackup(BaseMarshallingDomain):
    '''
    Create Backup Request Object for Admin API
    '''
    ROOT_TAG = 'createBackup'

    def __init__(self, name, backup_type, rotation, metadata=None):
        self.name = name
        self.backup_type = backup_type
        self.rotation = rotation

    def _obj_to_json(self):
        ret = self._auto_to_dict()

        return json.dumps(ret)

    def _obj_to_xml(self):
        xml = Constants.XML_HEADER
        element = ET.Element(self.ROOT_TAG)
        element.set('xmlns', Constants.XML_API_NAMESPACE)
        element.set('xmlns:atom', Constants.XML_API_ATOM_NAMESPACE)
        element.set('name', self.name)
        if self.backup_type is not None:
            element.set('backup_type', self.backup_type)
        if self.rotation is not None:
            element.set('rotation', self.rotation)
        xml += ET.tostring(element)
        return xml


class CreateImage(BaseMarshallingDomain):
    '''
    Create Image Server Action Request Object
    '''
    ROOT_TAG = 'createImage'

    def __init__(self, name, metadata=None):
        self.name = name
        self.metadata = metadata

    def _obj_to_json(self):
        ret = self._auto_to_dict()

        return json.dumps(ret)

    def _obj_to_xml(self):
        xml = Constants.XML_HEADER
        element = ET.Element(self.ROOT_TAG)
        element.set('xmlns', Constants.XML_API_NAMESPACE)
        element.set('xmlns:atom', Constants.XML_API_ATOM_NAMESPACE)
        element.set('name', self.name)
        if self.metadata is not None:
            meta_ele = ET.Element('metadata')
            for key, value in self.metadata.items():
                meta_ele.append(Metadata._dict_to_xml(key, value))
            element.append(meta_ele)
        xml += ET.tostring(element)
        return xml


class ChangePassword(BaseMarshallingDomain):
    ROOT_TAG = 'changePassword'
    '''
    Change Password Request Object
    '''

    def __init__(self, adminPassword):
        self.adminPass = adminPassword

    def _obj_to_json(self):
        ret = self._auto_to_dict()
        return json.dumps(ret)

    def _obj_to_xml(self):
        xml = Constants.XML_HEADER
        element = ET.Element(self.ROOT_TAG)
        element.set('xmlns', Constants.XML_API_NAMESPACE)
        element.set('adminPass', self.adminPass)
        xml += ET.tostring(element)
        return xml


class AddFixedIP(BaseMarshallingDomain):
    '''
    Add Fixed IP Action Request Object
    '''
    ROOT_TAG = 'addFixedIp'

    def __init__(self, networkId):
        self.networkId = networkId

    def _obj_to_json(self):
        ret = self._auto_to_dict()
        return json.dumps(ret)

    def _obj_to_xml(self):
        #TODO: Implement when xml is known
        raise NotImplementedError


class RemoveFixedIP(BaseMarshallingDomain):
    '''
    Remove Fixed IP Action Request Object
    '''
    ROOT_TAG = 'removeFixedIp'

    def __init__(self, networkId):
        self.networkId = networkId

    def _obj_to_json(self):
        ret = self._auto_to_dict()
        return json.dumps(ret)

    def _obj_to_xml(self):
        #TODO: Implement when xml is known
        raise NotImplementedError


class Evacuate(BaseMarshallingDomain):
    '''
    Evacuate Request Object for Admin API
    '''
    ROOT_TAG = 'evacuate'

    def __init__(self, host, onSharedStorage, adminPass, metadata=None):
        self.host = host
        self.onSharedStorage = onSharedStorage
        self.adminPass = adminPass

    def _obj_to_json(self):
        ret = self._auto_to_dict()

        return json.dumps(ret)

    def _obj_to_xml(self):
        xml = Constants.XML_HEADER
        element = ET.Element(self.ROOT_TAG)
        element.set('xmlns', Constants.XML_API_NAMESPACE)
        element.set('xmlns:atom', Constants.XML_API_ATOM_NAMESPACE)
        if self.host is not None:
            element.set('host', self.host)
        if self.onSharedStorage is not None:
            element.set('onSharedStorage', self.onSharedStorage)
        if self.adminPass is not None:
            element.set('adminPass', self.adminPass)
        xml += ET.tostring(element)
        return xml


class GetConsole(BaseMarshallingDomain):

    def __init__(self, vnc_type=None, tenant_id=None):

        super(GetConsole, self).__init__()
        self.vnc_type = vnc_type
        self.tenant_id = tenant_id

    def _obj_to_json(self):
        ret = {'os-getVNCConsole': self._obj_to_dict()}
        return json.dumps(ret)

    def _obj_to_dict(self):
        ret = {}
        ret['type'] = self.vnc_type
        ret['tenant_id'] = self.tenant_id
        self._remove_empty_values(ret)
        return ret

    def _obj_to_xml(self):
        raise NotImplemented

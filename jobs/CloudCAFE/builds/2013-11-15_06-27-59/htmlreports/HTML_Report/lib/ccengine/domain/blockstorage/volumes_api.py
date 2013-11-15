from ccengine.domain.base_domain import (
    BaseMarshallingDomain, BaseMarshallingDomainList)
import json
import xml.etree.ElementTree as ET


XMLNS = ''#'http://docs.rackspace.com/volume/api/v1'


class Volume(BaseMarshallingDomain):
    def __init__(self, display_name=None, size=None, volume_type=None,
                 display_description=None, metadata=None,
                 availability_zone=None, volume_id=None, snapshot_id=None,
                 attachments=None, created_at=None, status=None):

        #Common attributes
        self.display_name = display_name
        self.display_description = display_description
        self.size = size
        self.volume_type = volume_type
        self.metadata = metadata or {}
        self.availability_zone = availability_zone
        self.snapshot_id = snapshot_id

        #Response-only attributes
        self.id = volume_id
        self.attachments = attachments
        self.created_at = created_at
        self.status = status

    #Reqeust Generators
    def _obj_to_json(self):
        body = {"volume": {}}
        if self.display_name is not None:
            body['volume']["display_name"] = self.display_name
        if self.display_description is not None:
            body['volume']["display_description"] = self.display_description
        if self.size is not None:
            body['volume']["size"] = self.size
        if self.volume_type is not None:
            body['volume']["volume_type"] = self.volume_type
        if self.metadata is not None:
            body['volume']["metadata"] = self.metadata
        if self.availability_zone is not None:
            body['volume']["availability_zone"] = self.availability_zone
        if self.snapshot_id is not None:
            body['volume']['snapshot_id'] = self.snapshot_id
        ret = json.dumps(body)
        return ret

    def _obj_to_xml(self):
        volume_e = ET.Element('volume')
        volume_e.set('xmlns', XMLNS)
        if self.display_name is not None:
            volume_e.set('display_name', self.display_name)
        if self.display_description is not None:
            volume_e.set('display_description', self.display_description)
        if self.size is not None:
            volume_e.set('size', str(self.size))
        if self.volume_type is not None:
            volume_e.set('volume_type', self.volume_type)
        if self.availability_zone is not None:
            volume_e.set('availability_zone', self.availability_zone)
        if len(self.metadata.keys()) > 0:
            vol_metadata = ET.Element('metadata')
            for key in self.metadata.keys():
                meta = ET.Element('meta')
                meta.set('key', key)
                meta.text = self.metadata[key]
                vol_metadata.append(meta)
            volume_e.append(vol_metadata)
        xmlstr = ET.tostring(volume_e)
        return xmlstr

    #Response Deserializers
    @classmethod
    def _json_to_obj(cls, serialized_str):
        '''
            Handles both the single and list version of the Volume
            call, obviating the need for separate domain objects for "Volumes"
            and "Lists of Volumes" responses.
        '''
        json_dict = json.loads(serialized_str)
        vdict = json_dict.get('volume')

        return Volume(display_name=vdict.get('display_name'),
                size=vdict.get('size'), volume_type=vdict.get('volume_type'),
                display_description=vdict.get('display_description'),
                metadata=vdict.get('metadata'),
                availability_zone=vdict.get('availability_zone'),
                volume_id=vdict.get('id'),
                snapshot_id=vdict.get('snapshot_id'),
                attachments=vdict.get('attachments'),
                created_at=vdict.get('created_at'), status=vdict.get('status'))

    #Response Deserializers
    @classmethod
    def _xml_to_obj(cls, serialized_str):
        '''
            Handles both the single and list version of the Volume
            call, obviating the need for separate domain objects for "Volumes"
            and "Lists of Volumes" responses.
        '''
        element = ET.fromstring(serialized_str)
        return cls._xml_ele_to_obj(element)

    @classmethod
    def _xml_ele_to_obj(cls, element):
        return Volume(display_name=element.get('display_name'),
            size=element.get('size'), volume_type=element.get('volume_type'),
            display_description=element.get('display_description'),
            metadata=element.get('metadata'),
            availability_zone=element.get('availability_zone'),
            volume_id=element.get('id'),
            snapshot_id=element.get('snapshot_id'),
            attachments=element.get('attachments'),
            created_at=element.get('created_at'), status=element.get('status'))


class Volumes(Volume):

    #Response Deserializers
    @classmethod
    def _xml_to_obj(cls, serialized_str):
        '''
        Returns NONE if not a list
        '''
        element = ET.fromstring(serialized_str)
        ret = []
        for child in element:
            ret.append(cls._xml_ele_to_obj(child))

        return ret

    #Response Deserializers
    @classmethod
    def _json_to_obj(cls, serialized_str):
        ret = []
        json_dict = json.loads(serialized_str)
        vdict_list = json_dict.get('volumes')

        for vdict in vdict_list:
            if vdict:
                ret.append(Volume(display_name=vdict.get('display_name'),
                        size=vdict.get('size'),
                        volume_type=vdict.get('volume_type'),
                        display_description=vdict.get('display_description'),
                        metadata=vdict.get('metadata'),
                        availability_zone=vdict.get('availability_zone'),
                        volume_id=vdict.get('id'),
                        snapshot_id=vdict.get('snapshot_id'),
                        attachments=vdict.get('attachments'),
                        created_at=vdict.get('created_at'),
                        status=vdict.get('status')))
        return ret


class VolumeType(BaseMarshallingDomain):
    def __init__(self, volume_type_id=None, name=None, extra_specs=None):

        #Response-only attributes
        self.name = name
        self.id = volume_type_id
        self.extra_specs = extra_specs

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        vtype_dict = json_dict.get('volume_type')
        return cls._json_dict_to_obj(vtype_dict)

    @classmethod
    def _json_dict_to_obj(cls, json_dict):
        return VolumeType(
            volume_type_id=json_dict.get('id'),
            name=json_dict.get('name'),
            extra_specs=json_dict.get('extra_specs'))

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        element = ET.fromstring(serialized_str)
        return cls._xml_ele_to_obj(element)

    @classmethod
    def _xml_ele_to_obj(cls, xml_ele):
        kwargs = {
            'volume_type_id': xml_ele.get('id'),
            'name': xml_ele.get('name'),
            'extra_specs': xml_ele.get('extra_specs')}
        return VolumeType(**kwargs)


class VolumeTypes(BaseMarshallingDomainList):

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        vtype_dict_list = json_dict.get('volume_types')
        return cls._json_list_to_obj(vtype_dict_list)

    #Response Deserializers
    @classmethod
    def _json_list_to_obj(cls, json_list):
        vtype_list = VolumeTypes()
        for vtype in json_list:
            vtype_list.append(VolumeType._json_dict_to_obj(vtype))
        return vtype_list

    #Response Deserializers
    @classmethod
    def _xml_to_obj(cls, serialized_str):
        element = ET.fromstring(serialized_str)
        return cls._xml_ele_to_obj(element)

    @classmethod
    def _xml_ele_to_obj(cls, xml_ele):
        vtype_list = VolumeTypes()
        for child_element in xml_ele:
            vtype_list.append(VolumeType._xml_ele_to_obj(child_element))
        return vtype_list


class VolumeSnapshot(BaseMarshallingDomain):
    def __init__(self, volume_id=None, force=True, display_name=None,
                 display_description=None, snapshot_id=None, status=None,
                 size=None, created_at=None, name=None):

        #Request-only attribtes
        self.force = force

        #Common attributes
        self.display_name = display_name
        self.display_description = display_description
        self.volume_id = volume_id
        self.name = name

        #Response-only attributes
        self.id = snapshot_id
        self.status = status
        self.size = size
        self.created_at = created_at

    #Reqeust Generators
    def _obj_to_json(self):
        body = {
            "snapshot": {
                "volume_id": self.volume_id,
                "force": self.force,
                "display_name": self.display_name,
                "display_description": self.display_description}}

        return json.dumps(body)

    def _obj_to_xml(self):
        snap_e = ET.Element('snapshot')
        snap_e.set('xmlns', XMLNS)
        if self.display_name is not None:
            snap_e.set('name', str(self.name))
        if self.id is not None:
            snap_e.set('id', str(self.id))
        if self.display_name is not None:
            snap_e.set('display_name', str(self.display_name))
        if self.display_description is not None:
            snap_e.set('display_description', str(self.display_description))
        if self.volume_id is not None:
            snap_e.set('volume_id', str(self.volume_id))
        if self.force is not None:
            snap_e.set('force', str(self.force))
        xmlstr = ET.tostring(snap_e)
        return xmlstr

    #Response Deserializers
    @classmethod
    def _json_to_obj(cls, serialized_str):
        '''
            Handles both the single and list version of the Volume
            call, obviating the need for separate domain objects for "Volumes"
            and "Lists of Volumes" responses.
        '''
        json_dict = json.loads(serialized_str)
        is_list = True if json_dict.get('snapshots') else False
        vsdict_list = []

        if is_list:
            for v in json_dict.get('snapshots'):
                vsdict_list.append(v)
        else:
            vsdict_list.append(json_dict.get('snapshot'))

        ret = []
        for vsdict in vsdict_list:
            if vsdict:
                ret.append(VolumeSnapshot(
                       snapshot_id=vsdict.get('id'),
                       display_name=vsdict.get('display_name'),
                       display_description=vsdict.get('display_description'),
                       volume_id=vsdict.get('volume_id'),
                       status=vsdict.get('status'),
                       size=vsdict.get('size'),
                       created_at=vsdict.get('createdAt'),)
                          )

        #If this was a list of volumes, return the entire list, otherwise
        #just return the first element since it's the only volume.
        #NOTE:  Still returns a list if this WAS a list and there's only one
        #       volume in it.  This is correct behavior.
        if is_list:
            return ret
        elif ret:
            return ret[0]
        else:
            return None

    #Response Deserializers
    @classmethod
    def _xml_to_obj(cls, serialized_str):
        '''
            Handles both the single and list version of the Volume
            call, obviating the need for separate domain objects for "Volumes"
            and "Lists of Volumes" responses.
        '''
        element = ET.fromstring(serialized_str)
        return cls._xml_ele_to_obj(element)

    @classmethod
    def _xml_ele_to_obj(cls, element):
        vsdict = element.attrib
        return VolumeSnapshot(snapshot_id=vsdict.get('id'),
                display_name=vsdict.get('display_name'),
                display_description=vsdict.get('display_description'),
                volume_id=vsdict.get('volume_id'),
                status=vsdict.get('status'),
                size=vsdict.get('size'),
                created_at=vsdict.get('createdAt'))


class VolumeSnapshots(VolumeSnapshot):
    #Response Deserializers
    @classmethod
    def _xml_to_obj(cls, serialized_str):
        '''
            Handles both the single and list version of the Volume
            call, obviating the need for separate domain objects for "Volumes"
            and "Lists of Volumes" responses.
        '''
        element = ET.fromstring(serialized_str)
        ret = []
        for child in element:
            ret.append(cls._xml_ele_to_obj(child))
        return ret

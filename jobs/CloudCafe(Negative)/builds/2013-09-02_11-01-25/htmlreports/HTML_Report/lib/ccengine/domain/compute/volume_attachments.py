from ccengine.domain.base_domain import BaseMarshallingDomain
import json
from xml.etree import ElementTree


class VolumeAttachment(BaseMarshallingDomain):
    def __init__(self, volume_id=None, device=None):
        self.id = None
        self.server_id = None
        self.volume_id = volume_id
        self.device = device

    #Reqeust Generators
    def _obj_to_json(self):
        body = {
                "volumeAttachment": {
                    "volumeId": self.volume_id,
                    "device": self.device,

                 }
               }
        return json.dumps(body)

    def _obj_to_xml(self):
        '''
        <?xml version="1.0" encoding="UTF-8"?>
        <volumeAttachment
            xmlns="http://docs.openstack.org/compute/api/v1.1"
            volumeId="volume_id"
            device="device"/>
        '''
        pass

    @classmethod
    def _json_to_obj(cls, serialized_str):
        '''
            Handles both the single and list version of the Volume
            call, obviating the need for separate domain objects for "Volumes"
            and "Lists of Volumes" responses.
        '''
        json_dict = json.loads(serialized_str)

        is_list = True if json_dict.get('volumeAttachments') else False
        vdict_list = []

        if is_list:
            for v in json_dict.get('volumeAttachments'):
                vdict_list.append(v)
        else:
            vdict_list.append(json_dict.get('volumeAttachment'))

        ret = []
        for vdict in vdict_list:
            if vdict:
                volattach = VolumeAttachment(volume_id=vdict.get('volumeId'), device=vdict.get('device'))
                volattach.id = vdict.get('id')
                volattach.server_id = vdict.get('serverId')
                ret.append(volattach)

        if is_list:
            return ret
        elif ret:
            return ret[0]
        else:
            cls._log.error("Unable to deserialize json properly.  Returning empty domain object")
            return None

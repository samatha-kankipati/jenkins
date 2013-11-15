from ccengine.domain.base_domain import BaseMarshallingDomain
import json


class VncConsole(BaseMarshallingDomain):

    def __init__(self, vnc_type=None, url=None):
        self.type = vnc_type
        self.url = url

    @classmethod
    def _json_to_obj(cls, serialized_str):

        json_dict = json.loads(serialized_str)
        console_dict = json_dict.get('console')
        console = VncConsole(vnc_type=console_dict.get('type'),
                             url=console_dict.get('url'))
        return console

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        raise NotImplemented

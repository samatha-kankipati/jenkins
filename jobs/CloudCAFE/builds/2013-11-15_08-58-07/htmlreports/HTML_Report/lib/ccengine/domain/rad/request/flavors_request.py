import json

from ccengine.domain.base_domain import BaseMarshallingDomain


class FlavorsRequest(BaseMarshallingDomain):

    """
    @summary: Request Domain Object for flavors Web Service.
    """

    def __init__(self, device_id=None, ingredient_skus=None, desc=None):
        self.device_id = device_id
        self.ingredient_skus = ingredient_skus
        self.desc = desc

    def _obj_to_json(self):
        flavor_req_obj = {}
        if self.device_id is not None:
            flavor_req_obj["platform"] = self.device_id
        if self.ingredient_skus is not None:
            flavor_req_obj["ingredient_skus"] = self.ingredient_skus
        if self.desc is not None:
            flavor_req_obj["desc"] = self.desc
        req_payload = {}
        req_payload["payload"] = {"params": flavor_req_obj}
        req_payload_json = json.dumps(req_payload)
        return req_payload_json

    def __repr__(self):
        return str(self.__dict__)

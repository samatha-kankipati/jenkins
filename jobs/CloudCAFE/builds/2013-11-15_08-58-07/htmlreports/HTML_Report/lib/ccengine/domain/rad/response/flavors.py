import json

from ccengine.domain.base_domain import BaseMarshallingDomain


class FlavorsResponse(BaseMarshallingDomain):

    """
    @summary: Response Domain Object for flavors Web Service.
    """

    @classmethod
    def _json_to_obj(cls, serialized_str):
        """
        @summary: De-serialization method from json
        @param serialized_str: Flavors Response in JSON format
        @return: List of Flavor Objects
        """
        ret = None
        json_dict = json.loads(serialized_str)
        if "data" in json_dict.keys():
            flavor_list = []
            if type(json_dict.get("data")) is list:
                for flavor in json_dict["data"]:
                    if (set(flavor.keys()) != {"_id",
                                               "ingredient_skus",
                                               "platform",
                                               "desc"}):
                        raise Exception("Issue in deserializing Flavor Object:\
                            The properties in Flavor response are incorrect\
                            for Flavor id {0}".format(flavor["_id"]))
                    flavor_obj = Flavor(flavor["_id"],
                                        flavor["ingredient_skus"],
                                        flavor["platform"],
                                        flavor["desc"])
                    flavor_list.append(flavor_obj)
            elif type(json_dict.get("data")) is dict:
                flavor = json_dict.get("data")
                if (set(flavor.keys()) != {"_id",
                                           "ingredient_skus",
                                           "platform",
                                           "desc"}):
                    raise Exception("Issue in deserializing Flavor Object :\
                        The properties in the Flavor response are incorrect")
                flavor_obj = Flavor(flavor["_id"],
                                    flavor["ingredient_skus"],
                                    flavor["platform"],
                                    flavor["desc"])
                flavor_list.append(flavor_obj)
            ret = flavor_list
        else:
            ret = json_dict
        return ret

    def __repr__(self):
        return str(self.__dict__)


class Flavor:

    """
    @summary: Flavor Domain Object.
    """

    def __init__(self, id_val, ingredient_skus, device_id, desc):
        self.id_val = id_val
        self.ingredient_skus = ingredient_skus
        self.device_id = device_id
        self.desc = desc

    def __eq__(self, other):
        if type(other) is type(self):
            return self.__dict__ == other.__dict__
        return False

    def __hash__(self):
        return super.__hash__(self)

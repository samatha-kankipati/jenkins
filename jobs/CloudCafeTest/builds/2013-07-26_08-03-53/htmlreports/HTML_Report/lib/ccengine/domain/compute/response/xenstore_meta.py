from ccengine.domain.base_domain import BaseMarshallingDomain
import xml.etree.ElementTree as ET
import json
from ccengine.common.constants.compute_constants import Constants
from ccengine.domain.compute.metadata import Metadata


class Xenmeta(BaseMarshallingDomain):
    """
    @summary: Represents XenMeta domain object
    """
    ROOT_TAG = 'meta'

    def __init__(self, str_xenmeta):
        if str_xenmeta is not None:
            for key, value in str_xenmeta.items():
                setattr(self, key, value)

    @classmethod
    def _str_to_dict(cls, str_xenmeta):
        '''Returns dict of all xenstore metadata
        passed in.'''
        xenmeta = Xenmeta
        ret = {}
        meta_child = {}
        ls_xenmeta = str_xenmeta.split('\n')
        for each in ls_xenmeta:
            newpair_ls = each.split("=")
            if newpair_ls[0].startswith('hostname'):
                ret[(newpair_ls[0]).replace(' ', '')] = ((newpair_ls[1]).replace('"', '')).replace(' ', '')
            if newpair_ls[0].startswith(' meta'):
                meta_child[(newpair_ls[0]).replace(' ', '')] = ((newpair_ls[1]).replace('"', '')).replace(' ', '')
            if newpair_ls[0].startswith('server'):
                ret[(newpair_ls[0]).replace(' ', '')] = ((newpair_ls[1]).replace('"', '')).replace(' ', '')
            if newpair_ls[0].startswith('service_type'):
                ret[(newpair_ls[0]).replace(' ', '')] = ((newpair_ls[1]).replace('"', '')).replace(' ', '')
            if newpair_ls[0].startswith('created'):
                ret[(newpair_ls[0]).replace(' ', '')] = ((newpair_ls[1]).replace('"', '')).replace(' ', '')
            if newpair_ls[0].startswith('status'):
                ret[(newpair_ls[0]).replace(' ', '')] = ((newpair_ls[1]).replace('"', '')).replace(' ', '')
            if newpair_ls[0].startswith('task_state'):
                ret[(newpair_ls[0]).replace(' ', '')] = ((newpair_ls[1]).replace('"', '')).replace(' ', '')
            if newpair_ls[0].startswith('vm_state'):
                ret[(newpair_ls[0]).replace(' ', '')] = ((newpair_ls[1]).replace('"', '')).replace(' ', '')
            if newpair_ls[0].startswith('power_state'):
                ret[(newpair_ls[0]).replace(' ', '')] = ((newpair_ls[1]).replace('"', '')).replace(' ', '')
            if newpair_ls[0].startswith('image'):
                ret[(newpair_ls[0]).replace(' ', '')] = ((newpair_ls[1]).replace('"', '')).replace(' ', '')
            if newpair_ls[0].startswith('flavor'):
                ret[(newpair_ls[0]).replace(' ', '')] = ((newpair_ls[1]).replace('"', '')).replace(' ', '')
            if newpair_ls[0].startswith('access'):
                ret[(newpair_ls[0]).replace(' ', '')] = ((newpair_ls[1]).replace('"', '')).replace(' ', '')

        setattr(xenmeta, 'metadata', Metadata._dict_to_obj(meta_child))
        return xenmeta._dict_to_obj(ret)

    @classmethod
    def _dict_to_obj(cls, dict_xenmeta):
        '''Helper method to turn dictionary into Xenmeta instance.'''

        return Xenmeta(dict_xenmeta)

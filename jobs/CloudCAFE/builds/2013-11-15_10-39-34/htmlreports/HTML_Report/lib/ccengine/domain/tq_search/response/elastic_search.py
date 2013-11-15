from datetime import datetime
import json
import os
import time

from ccengine.common.tools.datatools import string_to_datetime, \
    convert_date_from_cst_to_utc_date
from ccengine.common.tools.equality_tools import EqualityTools
from ccengine.domain.base_domain import BaseDomain
from ccengine.domain.base_domain import BaseMarshallingDomain
from ccengine.domain.core.response.core import Core
from ccengine.domain.tq_search.response.account_services import AccountServices


class ElasticSearch(BaseMarshallingDomain):

    def __init__(self, total=None):

        super(ElasticSearch, self).__init__()
        self.total = total

    @classmethod
    def _json_to_obj(cls, serialized_str):
        ret = ElasticSearch()
        json_dict = json.loads(serialized_str)
        response = json_dict.get("hits")
        if response is not None:
            ret.hit_list = response.get("hits")
            ret.total = response.get("total")
        return ret

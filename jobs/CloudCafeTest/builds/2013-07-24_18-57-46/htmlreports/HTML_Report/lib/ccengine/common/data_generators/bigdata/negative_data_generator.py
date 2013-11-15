from ccengine.common.data_generators.data_generator import DataGenerator
from ccengine.domain.types import LavaClusterTypes
from datetime import datetime
from ccengine.providers.configuration import MasterConfigProvider as _MCP


class InvalidProfilePassword(DataGenerator):
        def __init__(self):
            self.test_records = []
            self.test_records.append({"prof_password": "Password1"})
            self.test_records.append({"prof_password": "password#1"})
            self.test_records.append({"prof_password": "PASSWORD1"})
            self.test_records.append({"prof_password": "PASSWORD1"})


class ClusterCreateErrors(DataGenerator):
        def __init__(self):
            self.test_records = []
            self.test_records.append({"name": "invalid-flavor",
                                      "count": 1,
                                      "type": "hadoop_cdh3",
                                      "flavor": 23})
            self.test_records.append({"name": "invalid-cluster-type",
                                      "count": 1,
                                      "type": "invalid-type",
                                      "flavor": "small"})
            self.test_records.append({"name": "invalid-count",
                                      "count": -1,
                                      "type": "invalid-type",
                                      "flavor": "small"})


class ResizeDataErrors(DataGenerator):
        def __init__(self):
                self.test_records = [
                    {'new_size': 2, 'error': ""},
                    {'new_size': -1, 'error': ""},
                    {'new_size': 0, 'error': ""}]

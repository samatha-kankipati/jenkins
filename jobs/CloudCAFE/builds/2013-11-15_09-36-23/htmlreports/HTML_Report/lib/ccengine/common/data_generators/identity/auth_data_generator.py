from ccengine.common.data_generators.data_generator import DataGenerator
from ccengine.domain.types import LavaClusterTypes
from datetime import datetime
from ccengine.providers.configuration import MasterConfigProvider

class AuthPasswordData(DataGenerator):
    def __init__(self):
        self.test_records = []
        stamp = datetime.now().microsecond
        cluster_name = "auth_functional_%s" %stamp
        self.test_records.append({"false_password":'00000000',
                                  "false_username":'@1234567'})
        self.test_records.append({"false_password":'',
                                  "false_username":''})
        self.test_records.append({"false_password":'Pass1',
                                  "false_username":'@'})
        self.test_records.append({"false_password":'!@#$%^&*()',
                                  "false_username":' 1Afarsf'})
        self.test_records.append({"false_password":'102102101031013010311031',
                                  "false_username":'Ricardo0000000000000!'})

from ccengine.common.data_generators.data_generator import DataGenerator
from ccengine.domain.types import LavaClusterTypes
from ccengine.providers.configuration import MasterConfigProvider as _MCP

import time
import random


class LavaMiscFTPFileDataGenerator():
    def __init__(self):
        self.cluster_prefix = "lava_functional_%s" % (stamp)

class SCPTransfer(DataGenerator):
    def __init__(self):
        self.test_records = []
        config = _MCP()
        stamp = time.mktime(time.localtime())
        file_name="out-{0}.dat".format(
            stamp)
        upload_file_path = "/user/{0}/{1}".format(
            config.lava_api.USER_NAME,
            stamp)
        self.test_records.append({"dest_file_path": file_name})
        self.test_records.append({"dest_file_path": upload_file_path})

class LavaAPIDataGenerator(DataGenerator):
    def __init__(self):
        config = _MCP()
        if config.lava_api.FLAVOR == "None":
            flavors = ["tiny", "small", "medium", "large"]
            flavor = flavors[random.randint(0, len(flavors) - 1)]
        else:
            flavor = config.lava_api.FLAVOR
        self.test_records = []
        cluster_size = random.randint(2, 10)
        stamp = time.mktime(time.localtime())
        cluster_name = "lava_test_{0}".format(int(stamp))
        self.test_records.append({"cluster_name": cluster_name,
                                  "cluster_type": LavaClusterTypes.HADOOP_HDP,
                                  "cluster_flavor": flavor,
                                  "cluster_size": cluster_size})

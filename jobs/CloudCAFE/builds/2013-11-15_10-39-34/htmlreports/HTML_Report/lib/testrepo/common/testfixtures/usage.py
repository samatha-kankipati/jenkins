'''
@summary: Testfixture for usage
@copyright: Copyright (c) 2013 Rackspace US, Inc.
'''
import csv
import json
import os

from ccengine.clients.atomhopper import CBSAtomHopperClient
from ccengine.clients.atomhopper import NovaAtomHopperClient
from ccengine.clients.atomhopper import LegacyAtomHopperClient
from ccengine.clients.identity.v1_1.rax_auth_admin_api import \
    IdentityAdminClient
from testrepo.common.testfixtures.fixtures import BaseTestFixture
from ccengine.common.dataset_generators import DatasetList
from ccengine.common.tools.datatools import CLOUDCAFE_DATA_DIRECTORY


class BaseUsageFixture(BaseTestFixture):

    @classmethod
    def setUpClass(cls):
        super(BaseUsageFixture, cls).setUpClass()

        #Create auth v1.1 admin api client for pulling account data
        endpoint = cls.config.identity_api.authentication_endpoint
        ser_format = cls.config.misc.serializer
        deser_format = cls.config.misc.deserializer
        admin_user = cls.config.identity_api.username
        admin_password = cls.config.identity_api.password

        cls.identity_v1_client = IdentityAdminClient(
            url=endpoint, user=admin_user, password=admin_password,
            serialize_format=ser_format, deserialize_format=deser_format)
        resp = cls.identity_v1_client.authenticate_password(admin_user,
                                                            admin_password)
        cls.token = resp.entity.token.id

    @classmethod
    def tearDownClass(cls):
        super(BaseUsageFixture, cls).tearDownClass()


class NovaUsageFixture(BaseUsageFixture):
    filename = "nova_atomhopper.csv"

    @classmethod
    def setUpClass(cls):
        super(NovaUsageFixture, cls).setUpClass()
        cls.atomhopper_client = NovaAtomHopperClient(
            cls.config.compute_api.atom_hopper_url, cls.token)

    @classmethod
    def tearDownClass(cls):
        super(NovaUsageFixture, cls).tearDownClass()


class CBSUsageFixture(BaseUsageFixture):
    filename = "cbs_atomhopper.csv"

    @classmethod
    def setUpClass(cls):
        super(CBSUsageFixture, cls).setUpClass()
        cls.atomhopper_client = CBSAtomHopperClient(
            cls.config.volumes_api.atom_feed_url, cls.token)

    @classmethod
    def tearDownClass(cls):
        super(CBSUsageFixture, cls).tearDownClass()


class LegacyUsageFixture(BaseUsageFixture):
    filename = "legacy_atomhopper.csv"

    @classmethod
    def setUpClass(cls):
        super(LegacyUsageFixture, cls).setUpClass()
        cls.atomhopper_client = LegacyAtomHopperClient(
            cls.config.legacyserv.atom_feed_url, cls.token)

    @classmethod
    def tearDownClass(cls):
        super(LegacyUsageFixture, cls).tearDownClass()


class CSVMetricsWriter(object):
    def __init__(self, path, headers, clear_log=False):
        self.path = path
        self.col = len(headers)
        self.writerow(headers, clear_log)

    def writerow(self, row_list, clean=False):
        if len(row_list) != self.col:
            raise Exception('Wrong number of rows')
        if clean:
            fp = open(self.path, "wb")
        else:
            fp = open(self.path, "ab")
        csv_writer = csv.writer(
            fp, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow(row_list)
        fp.close()


class CSVDataGenerator(DatasetList):
    def __init__(self, filename):
        fp = open(os.path.join(CLOUDCAFE_DATA_DIRECTORY, filename), "rbU")
        csv_reader = csv.reader(fp, delimiter=',', quotechar='"')
        list_of_rows = [row for row in csv_reader]
        headers = list_of_rows.pop(0)
        for test, row in enumerate(list_of_rows):
            dic = {}
            for col, header in enumerate(headers):
                try:
                    dic[header] = row[col] or None
                except IndexError:
                    dic[header] = None

            self.append_new_dataset(str(test), dic)

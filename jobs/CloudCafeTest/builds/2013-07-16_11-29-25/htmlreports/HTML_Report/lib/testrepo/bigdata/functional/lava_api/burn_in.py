'''
@summary: Tests Lava (Big Data) REST API
@copyright: Copyright (c) 2012 Rackspace US, Inc.
'''
import json
from ccengine.common.connectors import rest
from ccengine.providers.bigdata.lava_api import LavaAPIProvider as _LavaAPIProvider
from ccengine.domain.types import LavaClusterTypes
from ccengine.common.reporting.prettytable import PrettyTable
from testrepo.common.testfixtures.fixtures import BaseTestFixture
from ccengine.domain.types import LavaClusterStatusTypes as _LavaClusterStatusTypes

import csv
import random
from datetime import datetime
import time
from unittest2.suite import TestSuite


class BurnIn(BaseTestFixture):
    '''
    This class contains burn-in kind of tests.
    These are not parameterized and need to be able to run them independantly.
    '''

    def print_pretty_table(self, records):
        table = PrettyTable(fields=records[0])
        for i in xrange(1, len(records)):
            table.add_row(records[i])
        print "\n#{0}".format(table)

    def get_time(self):
        return time.asctime(time.localtime(time.time()))

    def test_simultaneous_cluster_creations(self):
        number_of_random_clusters = int(self.config.lava_api.
                                        MAX_SIMULTANEOUS_CLUSTERS)
        lava_provider = _LavaAPIProvider(self.config)
        lava_client = lava_provider.lava_client
        responses = {}
        start_times = {}
        end_times = {}
        results = []
        for i in xrange(0, number_of_random_clusters):
            create_time = datetime.now()
            stamp = create_time.microsecond
            cluster_name = "lava_burn_in_#{0}".format(stamp)
            api_response = lava_client.Clusters.\
                create(cluster_name, 2,
                       LavaClusterTypes.HADOOP_HDP,
                       lava_provider.get_flavor_id("small"))
            responses[cluster_name] = api_response
            start_times[cluster_name] = self.get_time()

        # Wait until all clusters are built
        max_time = time.time() + \
            int(self.config.lava_api.BULK_CLUSTER_CREATE_TIMEOUT)
        clusters_still_building = number_of_random_clusters
        while(time.time() < max_time and clusters_still_building > 0):
            clusters_still_building = number_of_random_clusters
            for cluster_name in responses.keys():
                response = responses[cluster_name]
                if response.status_code == 200:
                    cluster_id = response.entity.id
                    api_response = lava_client.Clusters.get_info(cluster_id)
                    cluster = api_response.entity
                    responses[cluster_name] = api_response
                    if cluster.status in [_LavaClusterStatusTypes.BUILD,
                                          _LavaClusterStatusTypes.CONFIGURING,
                                          _LavaClusterStatusTypes.CONFIGURED]:
                        continue
                    elif cluster.status in [_LavaClusterStatusTypes.ACTIVE,
                                            _LavaClusterStatusTypes.ERROR]:
                        clusters_still_building = clusters_still_building - 1
                        if cluster_name not in end_times:
                            end_times[cluster_name] = self.get_time()
                else:
                    clusters_still_building = clusters_still_building - 1
                    if cluster_name not in end_times:
                        end_times[cluster_name] = self.get_time()
                    time.sleep(30)

        results.append(["Cluster_name", "status", "message",
                        "start time", "end time"])
        for cluster_name in responses.keys():
            response = responses[cluster_name]
            if response.status_code == 200:
                cluster = response.entity
                if cluster.status == _LavaClusterStatusTypes.ERROR:
                    results.append([cluster_name,
                                    cluster.status,
                                    cluster.fault,
                                    start_times[cluster_name],
                                    end_times[cluster_name]])
                else:
                    results.append([cluster_name, cluster.status, "",
                                    start_times[cluster_name],
                                    end_times[cluster_name]])
                lava_client.Clusters.delete(cluster.id)
            else:
                results.append([cluster_name, "", response.content,
                                start_times[cluster_name],
                                end_times[cluster_name]])
        self.print_pretty_table(results)

    def test_repeated_cluster_creation(self):
        lava_provider = _LavaAPIProvider(self.config)
        lava_client = lava_provider.lava_client
        results = []
        results.append(["cluster name", "end status", "message",
                        "start time", "end time"])
        for i in xrange(0,
                        int(self.config.lava_api.REPEATED_CLUSTER_CREATION)):
            stamp = datetime.now().microsecond
            cluster_name = "lava_burn_in_%s" % stamp
            api_response = lava_client.Clusters.\
                create(cluster_name, 2,
                       LavaClusterTypes.HADOOP_HDP,
                       lava_provider.get_flavor_id("small"))
            start_time = self.get_time()
            if api_response.status_code == 200:
                wait_response = lava_provider.wait_for_cluster_status(
                    api_response.entity.id, _LavaClusterStatusTypes.ACTIVE,
                    timeout=1000)
                if wait_response.ok:
                    results.append([cluster_name,
                                    wait_response.response.entity.status,
                                    "",
                                    start_time,
                                    self.get_time()])
                else:
                    results.append([cluster_name,
                                    wait_response.response.entity.status,
                                    wait_response.response.entity.fault,
                                    start_time,
                                    self.get_time()])
                api_response = lava_client.Clusters.delete(
                    wait_response.response.entity.id)
            else:
                results.append([cluster_name, "", api_response.content,
                                start_time, self.get_time()])
        self.print_pretty_table(results)

    def test_progresive_resize_cluster(self):
        lava_provider = _LavaAPIProvider(self.config)
        lava_client = lava_provider.lava_client
        results = []
        results.append(["cluster name", "size", "resize", "end status",
                        "start time", "end time"])
        # Create a cluster
        stamp = datetime.now().microsecond
        cluster_name = "lava_burn_in_%s" % stamp
        api_response = lava_client.Clusters.create(
            cluster_name, 1, LavaClusterTypes.HADOOP_HDP,
            lava_provider.get_flavor_id("small"))
        if api_response.status_code == 200:
            wait_response = lava_provider.wait_for_cluster_status(
                api_response.entity.id, _LavaClusterStatusTypes.ACTIVE)
            if wait_response.ok:
                cluster = wait_response.response.entity
                # resize the cluster again and again
                cluster_resize_max = int(self.config.lava_api.
                                         PROGRESSIVE_CLUSTER_RESIZE_MAX)
                cluster_resize_factor = int(self.config.lava_api.
                                            PROGRESSIVE_CLUSTER_RESIZE_FACTOR)
                for i in xrange(2, cluster_resize_max, cluster_resize_factor):
                    size = cluster.count
                    response = lava_client.Clusters.resize(cluster.id, i)
                    start_time = self.get_time()
                    if response.status_code == 200:
                        response = lava_provider.wait_for_cluster_status(
                            cluster.id, _LavaClusterStatusTypes.ACTIVE)
                        cluster = wait_response.response.entity
                        results.append([cluster_name,
                                        size,
                                        i,
                                        cluster.status,
                                        start_time,
                                        self.get_time()])
                        if cluster.status != _LavaClusterStatusTypes.ACTIVE:
                            break
                    else:
                        results.append([cluster.id,
                                        size,
                                        i,
                                        response.content,
                                        start_time,
                                        self.get_time()])
                        break
            # Delete the cluster
            api_response = lava_client.Clusters.delete(api_response.entity.id)
            self.print_pretty_table(results)

    def test_progressive_cluster_creations(self):
        results = []
        results.append(["cluster_id", "size", "end status", "response",
                        "start time", "end time"])
        lava_provider = _LavaAPIProvider(self.config)
        lava_client = lava_provider.lava_client
        cluster_create_max = int(self.config.lava_api.
                                 PROGRESSIVE_CLUSTER_CREATE_MAX)
        cluster_create_factor = int(self.config.lava_api.
                                    PROGRESSIVE_CLUSTER_CREATE_FACTOR)
        for i in xrange(1, cluster_create_max, cluster_create_factor):
            stamp = datetime.now().microsecond
            cluster_name = "lava_burn_in_%s" % stamp
            api_response = lava_client.Clusters.\
                create(cluster_name, i,
                       LavaClusterTypes.HADOOP_HDP,
                       lava_provider.get_flavor_id("small"))
            start_time = self.get_time()
            if api_response.status_code == 200 and \
                    api_response.entity.status == _LavaClusterStatusTypes.BUILD:
                created_cluster = api_response.entity
                wait_response = lava_provider.wait_for_cluster_status(
                    created_cluster.id, _LavaClusterStatusTypes.ACTIVE)
                if wait_response.ok:
                    created_cluster = wait_response.response.entity
                    results.append([created_cluster.id,
                                    i,
                                    created_cluster.status,
                                    "",
                                    start_time,
                                    self.get_time()])
                    api_response = lava_client.Clusters.delete(
                        created_cluster.id)
                    continue
                else:
                    results.append([created_cluster.id, i,
                                    "",
                                    wait_response.response.entity.fault,
                                    start_time,
                                    self.get_time()])
                    break
            else:
                results.append([created_cluster.id,
                                i,
                                "",
                                api_response.content,
                                start_time,
                                self.get_time()])
                break
        self.print_pretty_table(results)
'''
@summary: Provider class for Bandwidth tests
@note: Inherits ComputeAPIProvider; overrides some of it's methods
@copyright: Copyright (c) 2012-2013 Rackspace US, Inc.
'''
from datetime import datetime, timedelta
import json
import sys

from ccengine.providers.compute.compute_api import ComputeAPIProvider
from ccengine.providers.auth.auth_api import AuthProvider as _AuthProvider
from ccengine.providers.stacktach.stacktachdb_provider import \
    StackTachDBProvider as _StackTachDBProvider
from ccengine.clients.remote_instance.instance_client import \
    LinuxClient
from ccengine.domain.compute.bandwidth.exists_event_queue import \
    ExistsEventQueue
from ccengine.domain.types import NovaServerStatusTypes as ServerStatus
from ccengine.common.tools.datagen import rand_name
from ccengine.common.tools.datatools import gb_to_bytes
from ccengine.common.constants.compute_constants import Constants


class BandwidthComputeAPIProvider(ComputeAPIProvider):
    '''
    @summary: Provider Module for the Compute REST API
    @note: Should be the primary interface to a test case or external tool.
    @copyright: Copyright (c) 2012 Rackspace US, Inc.
    '''

    def __init__(self, config, logger=None):

        if config is None:
            self.provider_log.warning('empty (=None) config recieved in init')
            # Load configuration from default.conf
            self.config = _AuthProvider
        else:
            self.config = config

        super(BandwidthComputeAPIProvider, self).__init__(config=self.config)

        self.stacktachdb_provider = _StackTachDBProvider(self.config)
        self.interval_time = self.config.compute_api.build_interval
        self.timeout = self.config.compute_api.server_status_timeout
        self.env_name = self.config.compute_api.env_name

    def rebuild_and_await(self, server_id, image_ref):
        '''
        @summary:  Rebuild instance and wait for server status ACTIVE
        @return:  Rebuilt server entity object, start and end times
            for the wait response
        @note: Overrides method in ComputeAPIProvider
        '''

        resp = self.servers_client.rebuild(server_id, image_ref)
        assert resp.status_code is 202
        start_time_wait_resp = (datetime.utcnow()
                                .strftime(Constants.DATETIME_FORMAT))
        wait_response = self.wait_for_server_status(
                            server_id, ServerStatus.ACTIVE)
        end_time_wait_resp = (datetime.utcnow()
                              .strftime(Constants.DATETIME_FORMAT))

        (self.stacktachdb_provider
            .wait_for_launched_at(
                server_id,
                interval_time=self.interval_time,
                timeout=self.timeout))

        rebuilt_server = wait_response.entity
        return (rebuilt_server,
                start_time_wait_resp,
                end_time_wait_resp)

    def resize_and_await(self, server_id, new_flavor):
        '''
        @summary:  Resize instance and wait for server status VERIFY RESIZE
        @return:  Resized server entity object
        @note: Overrides method in ComputeAPIProvider
        @todo: Implement override on test creation
        '''

        resp = self.servers_client.resize(server_id, new_flavor)
        assert resp.status_code is 202
        start_time_wait_resp = (datetime.utcnow()
                                .strftime(Constants.DATETIME_FORMAT))
        wait_response = self.wait_for_server_status(
                            server_id, ServerStatus.VERIFY_RESIZE)
        end_time_wait_resp = (datetime.utcnow()
                              .strftime(Constants.DATETIME_FORMAT))

        (self.stacktachdb_provider
            .wait_for_launched_at(
                server_id,
                interval_time=self.interval_time,
                timeout=self.timeout))

        resized_server = wait_response.entity
        return (resized_server,
                start_time_wait_resp,
                end_time_wait_resp)

    def resize_and_confirm(self, server_id, new_flavor):
        '''
        @summary:  Resize instance then confirm resize.
            Wait for server status ACTIVE
        @return:  (Confirmed) Resized server entity object
        @note: Overrides method in ComputeAPIProvider
        @todo: Implement override on test creation
        '''

        (_,
         start_time_wait_resp,
         end_time_wait_resp) = self.resize_and_await(server_id, new_flavor)
        resp = self.servers_client.confirm_resize(server_id)
        assert resp.status_code is 204
        wait_response = self.wait_for_server_status(server_id,
                                                    ServerStatus.ACTIVE)
        resized_server = wait_response.entity
        return (resized_server,
                start_time_wait_resp,
                end_time_wait_resp)

    def resize_and_revert(self, server_id, new_flavor):
        '''
        @summary:  Resize instance then revert resize.
            Wait for server status ACTIVE
        @return:  (Reverted) Resized server entity object
        @note: Overrides method in ComputeAPIProvider
        @todo: Implement override on test creation
        '''
        (_,
         start_time_wait_resp,
         end_time_wait_resp) = self.resize_and_await(server_id, new_flavor)
        resp = self.servers_client.revert_resize(server_id)
        assert resp.status_code is 202
        resized_server = self.wait_for_server_status(server_id,
                                                     ServerStatus.ACTIVE)
        revert_start_time_wait_resp = (datetime.utcnow()
                                       .strftime(Constants.DATETIME_FORMAT))
        wait_response = self.wait_for_server_status(
                            server_id, ServerStatus.VERIFY_RESIZE)
        revert_end_time_wait_resp = (datetime.utcnow()
                                     .strftime(Constants.DATETIME_FORMAT))

        (self.stacktachdb_provider
            .wait_for_launched_at(
                server_id,
                interval_time=self.interval_time,
                timeout=self.timeout))
        reverted_resized_server = wait_response.entity
        return (resized_server,
                start_time_wait_resp,
                end_time_wait_resp,
                reverted_resized_server,
                revert_start_time_wait_resp,
                revert_end_time_wait_resp)

    def do_bandwidth_server_to_client(self, server, gb_file_size):
        '''
        @summary: Generates bandwidth from server to client
        @param server: Instance object of the server
        @type server: Instance
        @param gb_file_size: Size of file in Gigabytes
        @type gb_file_size: Float
        @return: True is bandwidth generation is successful,
            Exception otherwise
        @rtype: Boolean

        '''

        ip_addr = self.get_public_ip_address(server)
        linux_client = LinuxClient(ip_address=ip_addr,
                                   server_id=server.id,
                                   os_distro="",
                                   username="root",
                                   password=server.adminPass)
        client_filepath = ("/var/tmp/{0}{1}"
                           .format(rand_name('file'), rand_name('.')))
        server_filepath = ("/root/{0}{1}"
                           .format(rand_name('file'), rand_name('.')))

        try:
            (linux_client
             .generate_bandwidth_from_server_to_client(
                    public_ip_address=ip_addr,
                    gb_file_size=gb_file_size,
                    server_filepath=server_filepath,
                    client_filepath=client_filepath))
            return True
        except:
            raise

    def insert_exists_event(self, exists_type, server,
                            launched_at, test_name, test_type,
                            state_description=None,
                            audit_period_ending=None,
                            gb_file_size=0):
        '''
        @summary:  Inserts an exists event into the DB for later verification
        @param exists_type: The type of exists event
        @type exists: String
        @param server: Instance uuid id of the server
        @type server: String
        @param launched_at: Datetime of when the instance was launched
        @type launched_at: String
        @param audit_period_beginning: Datetime of when the instance's
            audit period began
        @type audit_period_beginning: String
        @param audit_period_ending: Datetime of when the instance's
            audit period ended
        @type audit_period_ending: String
        @param test_name: Name of the test that calls this method
        @type test_name: String
        @param test_type: Name of the collection  of tests
        @type test_type: String
        @param gb_file_size: Size of file in GB
        @type gb_file_size: Float
        @return:  True on successful insert, Exception otherwise
        @rtype: Boolean

        '''
        if exists_type == "immediate":
            bandwidth_usage = \
                json.dumps({'public': {'bw_in': 0, 'bw_out': 0},
                            'private': {'bw_in': 0, 'bw_out': 0}})
        elif exists_type == "periodic":
            bandwidth_usage = \
                json.dumps({'public': {'bw_in': 0,
                                       'bw_out': gb_to_bytes(gb_file_size)},
                            'private': {'bw_in': 0, 'bw_out': 0}})
            audit_period_ending = ((datetime.utcnow() + timedelta(days=1))
                                   .strftime(Constants.DATETIME_0AM_FORMAT))
        else:
            raise Exception("The exists_type is not a valid type or "
                            "gb_file_size is not correctly set. "
                            "exists_type: {0}"
                            "gb_file_size: {1}".format(exists_type,
                                                       str(gb_file_size)))

        try:
            ExistsEventQueue(server=server,
                             state_description=state_description,
                             audit_period_ending=audit_period_ending,
                             bandwidth_usage=bandwidth_usage,
                             test_name=test_name,
                             launched_at=launched_at,
                             test_type=test_type,
                             env_name=self.env_name).add_to_queue()
            return True
        except:
            e = sys.exc_info()[0]
            raise Exception("The exists event failed to be inserted "
                            "into the DB: {0}".format(e))

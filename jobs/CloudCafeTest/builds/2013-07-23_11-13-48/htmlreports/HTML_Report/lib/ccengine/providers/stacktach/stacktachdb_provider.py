import time

from ccengine.providers.base_provider import BaseProvider
from ccengine.clients.stacktach.stacktachdb_api import StackTachDBClient
from ccengine.common.exceptions.compute import TimeoutException


class StackTachDBProvider(BaseProvider):

    def __init__(self, config, logger=None):
        '''
        Sets config, sets up client, sets deserializer and serializer based
        on format defined in the config.
        '''
        super(StackTachDBProvider, self).__init__()
        self.config = config
        self.client = StackTachDBClient(config.stacktach.db_url,
                                        config.misc.serializer,
                                        config.misc.deserializer)

    def wait_for_launched_at(self, server_id, interval_time=10, timeout=200):
        '''
        @summary: Polls Launch launched_at field until it is populated
        '''

        launch_resp = self.client.list_launches_for_uuid(instance=server_id)
        launches = launch_resp.entity

        # Go through each of the launches and check that
        # the launched_at attribute exists and is populated
        for launch_obj in launches:
            found_launched_at = False
            time_waited = 0
            while ((not found_launched_at or
                    not hasattr(launch_obj, 'launched_at')) and
                    (time_waited <= timeout)):
                resp = (self.client
                        .list_launches_for_uuid(instance=server_id))
                items = resp.entity
                # Iterate over response and match on launch id
                items = [item for item in items if \
                         item.id == launch_obj.id]
                try:
                    found_launched_at = items[0].launched_at
                except:
                    pass
                time.sleep(interval_time)
                time_waited += interval_time
            if time_waited > timeout:
                raise TimeoutException("Timed Out. Server with uuid %s timed \
                                        out waiting for Launch entry \
                                        launched_at field to be populated \
                                        after %i seconds. response: %s"
                                        % server_id, timeout, launch_resp)
        return launch_resp

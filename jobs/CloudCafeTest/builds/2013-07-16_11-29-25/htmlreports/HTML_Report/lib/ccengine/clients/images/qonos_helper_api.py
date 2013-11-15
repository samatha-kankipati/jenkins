from ccengine.clients.base_client import BaseMarshallingClient


class QonosHelperClient(BaseMarshallingClient):

    _worker_suffix = '/worker'
    _scheduler_suffix = '/scheduler'

    def __init__(self, url, serialize_format, deserialize_format=None):

        super(QonosHelperClient, self).__init__(serialize_format,
                                                  deserialize_format)

        self.url = "{0}{1}".format(url, self._worker_suffix)

    def stop_workers(self, keys=None, values=None, requestslib_kwargs=None):

        full_url = "{0}/{1}".format(self.url, "stop")
        params = None
        if keys is not None and values is not None:
            # Params are passed as list of keys and values and converted to dict
            params = dict(zip(keys, values))
        return self.request("GET", full_url, params=params,
                            requestslib_kwargs=requestslib_kwargs)

    def start_worker(self, requestslib_kwargs=None):

        full_url = "{0}/{1}".format(self.url, "start")
        return self.request("GET", full_url,
                            requestslib_kwargs=requestslib_kwargs)

    def get_running_worker_count(self, requestslib_kwargs=None):

        full_url = "{0}/{1}".format(self.url, "running")
        return self.request("GET", full_url,
                            requestslib_kwargs=requestslib_kwargs)

    def get_running_scheduler_count(self, requestslib_kwargs=None):

        full_url = "{0}/{1}".format(self.url, "running")
        return self.request("GET", full_url,
                            requestslib_kwargs=requestslib_kwargs)

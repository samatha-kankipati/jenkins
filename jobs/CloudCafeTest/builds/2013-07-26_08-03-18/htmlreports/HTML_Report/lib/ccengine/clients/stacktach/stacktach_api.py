from ccengine.domain.stacktach.response.stacktach_api import \
        StackTachEntity as ResponseEntity
from ccengine.clients.base_client import BaseMarshallingClient


class StackTachClient(BaseMarshallingClient):

    def __init__(self, url, serialize_format, deserialize_format=None):
        super(StackTachClient, self).__init__(serialize_format,
                                              deserialize_format)
        self.url = url
        ct = ''.join(['application/', self.serialize_format])
        accept = ''.join(['application/', self.deserialize_format])
        self.default_headers['Content-Type'] = ct
        self.default_headers['Accept'] = accept

    def get_event_names(self, requestslib_kwargs=None):
        '''
        @summary: Retrieves Event Names that are known
        @return: List of event names
        @rtype:  Response Object
        '''

        '''
            GET
            stacky/events/
        '''
        url = ''.join([self.url, '/stacky/events/'])
        return self.request('GET', url, response_entity_type=ResponseEntity,
                            requestslib_kwargs=requestslib_kwargs)

    def get_host_names(self, requestslib_kwargs=None):
        '''
        @summary: Retrieves Host Names that are known
        @return: List of host names
        @rtype:  Response Object
        '''

        '''
            GET
            stacky/hosts/
        '''
        url = ''.join([self.url, '/stacky/hosts/'])
        return self.request('GET', url, response_entity_type=ResponseEntity,
                            requestslib_kwargs=requestslib_kwargs)

    def get_deployments(self, requestslib_kwargs=None):
        '''
        @summary: Retrieves Deployments that are known
        @return: List of Deployments
        @rtype:  Response Object
        '''

        '''
            GET
            stacky/deployments/
        '''
        url = ''.join([self.url, '/stacky/deployments/'])
        return self.request('GET', url, response_entity_type=ResponseEntity,
                            requestslib_kwargs=requestslib_kwargs)

    def get_timings_summary(self, requestslib_kwargs=None):
        '''
        @summary: Retrieves summarized timings for all events
        @return: List of timings
        @rtype:  Response Object
        '''

        '''
            GET
            stacky/summary/
        '''
        url = ''.join([self.url, '/stacky/summary/'])
        return self.request('GET', url, response_entity_type=ResponseEntity,
                            requestslib_kwargs=requestslib_kwargs)

    def get_timings_for_uuid(self, uuid, requestslib_kwargs=None):
        '''
        @summary: Retrieves summarized timings for a given server
        @param uuid: The uuid of an existing instance.
        @type uuid: String
        @return: List of timings for the server
        @rtype:  Response Object
        '''

        '''
            GET
            stacky/timings/uuid/?uuid={uuid}
        '''
        params = {'uuid': uuid}
        url = ''.join([self.url, '/stacky/timings/uuid/'])
        return self.request('GET', url, params=params,
                            response_entity_type=ResponseEntity,
                            requestslib_kwargs=requestslib_kwargs)

    def get_timings_for_event_name(self, event, requestslib_kwargs=None):
        '''
        @summary: Retrieves timings for a given event name
        @param event: The name of an event
        @type event: String
        @return: List of timings for the event name
        @rtype:  Response Object
        '''

        '''
            GET
            stacky/timings/?name={event}
        '''
        params = {'name': event}
        url = ''.join([self.url, '/stacky/timings/'])
        return self.request('GET', url, params=params,
                            response_entity_type=ResponseEntity,
                            requestslib_kwargs=requestslib_kwargs)

    def get_events_for_uuid(self, uuid, requestslib_kwargs=None):
        '''
        @summary: Retrieves events related to a given server
        @param uuid: The uuid of an existing instance.
        @type uuid: String
        @return: List of events for the server
        @rtype:  Response Object
        '''

        '''
            GET
            stacky/uuid/?uuid={uuid}
        '''
        params = {'uuid': uuid}
        url = ''.join([self.url, '/stacky/uuid/'])
        return self.request('GET', url, params=params,
                            response_entity_type=ResponseEntity,
                            requestslib_kwargs=requestslib_kwargs)

    def get_events_for_request_id(self, request_id, requestslib_kwargs=None):
        '''
        @summary: Retrieves events related to a given request id
        @param request_id:  An identifier of an event given by the API
        @type request_id: String
        @return: List of events for the request id
        @rtype:  Response Object
        '''

        '''
            GET
            stacky/request/?request_id={request_id}
        '''
        params = {'request_id': request_id}
        url = ''.join([self.url, '/stacky/request/'])
        return self.request('GET', url, params=params,
                            response_entity_type=ResponseEntity,
                            requestslib_kwargs=requestslib_kwargs)

    def get_kpi(self, requestslib_kwargs=None):
        '''
        @summary: Retrieves key performance indicators
        @return: List of key performance indicators
        @rtype:  Response Object
        '''

        '''
            GET
            stacky/kpi/
        '''
        url = ''.join([self.url, '/stacky/kpi/'])
        return self.request('GET', url, response_entity_type=ResponseEntity,
                            requestslib_kwargs=requestslib_kwargs)

    def get_kpi_for_tenant_id(self, tenant_id, requestslib_kwargs=None):
        '''
        @summary: Retrieves key performance indicators for a tenant
        @param tenant_id:  The id of an existing tenant.
        @type tenant_id: String
        @return: List of key performance indicators for a tenant
        @rtype:  Response Object
        '''

        '''
            GET
            stacky/kpi/{tenant_id}/
        '''
        url = ''.join([self.url, '/stacky/kpi/', tenant_id])
        return self.request('GET', url, response_entity_type=ResponseEntity,
                            requestslib_kwargs=requestslib_kwargs)

    def get_watch_events(self, deployment_id, requestslib_kwargs=None):
        '''
        @todo XXXFN - need to find out more about this since it is
         being polled in stacky
        @summary: Retrieves current events coming from a given deloyment
        @param deployment_id:  An identifier of a deployment
        @type deployment_id: String
        @return: List of events for a deployment
        @rtype:  Response Object
        '''

        '''
            GET
            stacky/watch/{deployment_id}/
        '''
        url = ''.join([self.url, '/stacky/watch/', deployment_id])
        return self.request('GET', url, response_entity_type=ResponseEntity,
                            requestslib_kwargs=requestslib_kwargs)

    def get_event_id_details(self, event_id, requestslib_kwargs=None):
        '''
        @todo XXXFN - the response is only formatted for command line
        @summary: Retrieves details of a given event
        @param event_id:  An identifier of an event within the StackTach DB
        @type event_id: String
        @return: Details of an event
        @rtype:  Response Object
        '''

        '''
            GET
            stacky/show/{event_id}/
        '''
        url = ''.join([self.url, '/stacky/show/', event_id])
        return self.request('GET', url,
                            requestslib_kwargs=requestslib_kwargs)

    def get_reports(self, requestslib_kwargs=None):
        '''
        @summary: Retrieves a list of available reports
        @return: List of reports
        @rtype:  Response Object
        '''

        '''
            GET
            stacky/reports/
        '''
        url = ''.join([self.url, '/stacky/reports/'])
        return self.request('GET', url,
                            requestslib_kwargs=requestslib_kwargs)

    def get_report_details(self, report_id, requestslib_kwargs=None):
        '''
        @summary: Retrieves detailed report
        @param report_id:  An identifier of a report
        @type report_id: String
        @return: Detailed report
        @rtype:  Response Object
        '''

        '''
            GET
            stacky/report/{report_id}/
        '''
        url = ''.join([self.url, '/stacky/report/', str(report_id)])
        return self.request('GET', url,
                            requestslib_kwargs=requestslib_kwargs)

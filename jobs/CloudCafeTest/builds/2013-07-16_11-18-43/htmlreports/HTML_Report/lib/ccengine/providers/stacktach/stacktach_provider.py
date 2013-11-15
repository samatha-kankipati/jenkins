from ccengine.providers.base_provider import BaseProvider
from ccengine.clients.stacktach.stacktach_api import StackTachClient


class StackTachProvider(BaseProvider):

    def __init__(self, config, logger):
        '''
        Sets config, sets up client, sets deserializer and serializer based
        on format defined in the config.
        '''
        super(StackTachProvider, self).__init__()
        self.config = config
        self.client = StackTachClient(self.config.stacktach.url,
                                      self.config.misc.serializer,
                                      self.config.misc.deserializer)

    def get_uuid_from_event_id_details(self, event_id='1'):
        '''
        @summary: Gets the uuid from the event id details
        @param event_id: The event_id in Stacky
        @type event_id: String
        @return: uuid
        @rtype: String
        '''
        response = self.client.get_event_id_details(event_id)
        return response.json[2]

    def get_request_id_from_event_id_details(self, event_id='1'):
        '''
        @summary: Gets the request_id from the event id details
        @param event_id: The event_id in Stacky
        @type event_id: String
        @return: request_id
        @rtype: String
        '''
        response = self.client.get_event_id_details(event_id)
        return response.json[0][-1][1]

    def get_tenant_id_from_event_id_details(self, event_id='1'):
        '''
        @summary: Gets the tenant_id from the event id details
        @param event_id: The event_id in Stacky
        @type event_id: String
        @return: tenant_id
        @rtype: String
        '''
        response = self.client.get_event_id_details(event_id)
        my_list = response.json[1].split()
        tenant_id_index = my_list.index('"tenant_id":') + 1
        tenant_id = str(my_list[tenant_id_index][1:-2])
        return tenant_id

    def get_report_id_by_report_name_from_reports(self, report_name):
        '''
        @summary: Gets the report id by report name from a
            list of available reports
        @param report_name: Name of the report
        @type report_name: String
        @return: report_id
        @rtype: String
        '''
        response = self.client.get_reports()
        report_id = -1
        for row in response.json[1:]:
            if row[4] == report_name:
                report_id = row[0]
        if report_id == -1:
            msg = ("{0} report was not found in reports list."
                   .format(report_name))
            self.provider_log.critical(msg)
            raise Exception(msg)
        else:
            return report_id

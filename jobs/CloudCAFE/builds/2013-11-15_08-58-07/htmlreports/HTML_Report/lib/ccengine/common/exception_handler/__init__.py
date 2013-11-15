from ccengine.common.exceptions import compute as exceptions
import xml.etree.ElementTree as ET
import json
from ccengine.domain.base_domain import BaseMarshallingDomain

ns = "http://docs.openstack.org/compute/api/v1.1"


class ExceptionHandler:

    error_codes_list = [400, 401, 403, 404, 405, 409, 413, 415, 500, 501, 503]

    def check_for_errors(self, resp, serialize_format):

        if resp.status_code not in self.error_codes_list:
            return

        if resp.text != "":
            resp_body_dict = self._parse_resp_body(resp.text, serialize_format)

        if resp.status_code == 400:
            raise exceptions.BadRequest(resp_body_dict['badRequest']['message'])

        if resp.status_code == 401:
            raise exceptions.Unauthorized()

        if resp.status_code == 413:
            if 'overLimit' in resp_body_dict:
                message = resp_body_dict['overLimit']['message']
            else:
                message = 'Rate or absolute limit exceeded'
            raise exceptions.OverLimit(message)

        if resp.status_code in (500, 501):
            message = ''
            if 'computeFault' in resp_body_dict:
                message = resp_body_dict['computeFault']['message']
            if 'cloudServersFault' in resp_body_dict:
                message = resp_body_dict['cloudServersFault']['message']
            if 'x-compute-request-id' in resp:
                message += ' x-compute-request-id ' + resp['x-compute-request-id']
            raise exceptions.ComputeFault(message)

        if resp.status_code == 404:
            raise exceptions.ItemNotFound()

        if resp.status_code == 409:
            message = ''
            if 'conflictingRequest' in resp_body_dict:
                message = resp_body_dict['conflictingRequest']['message']
            if 'inProgress' in resp_body_dict:
                message = resp_body_dict['inProgress']['message']
            raise exceptions.ActionInProgress(message)

        if resp.status_code == 405:
            raise exceptions.BadMethod()

        if resp.status_code == 403:
            raise exceptions.Forbidden()

        if resp.status_code == 503:
            raise exceptions.ServiceUnavailable()

        if resp.status_code == 415:
            raise exceptions.BadMediaType()

    def _parse_resp_body(self, resp_body, serialize_format):
        if serialize_format != 'json':
            element = ET.fromstring(resp_body)
            BaseMarshallingDomain._remove_namespace(element, ns)
            return {element.tag: {'message': element.find('message').text}}
        return json.loads(resp_body)

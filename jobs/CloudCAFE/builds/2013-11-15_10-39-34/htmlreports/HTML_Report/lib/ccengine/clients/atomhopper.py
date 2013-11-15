import uuid

from ccengine.clients.base_client import BaseMarshallingClient
from ccengine.domain.atomhopper.response import AtomFeed
from ccengine.domain.atomhopper.requests import CBSUsageEvent
from ccengine.domain.atomhopper.requests import LegacyUsageEvent
from ccengine.domain.atomhopper.requests import NovaExistsEvent
from ccengine.domain.atomhopper.requests import NovaCUFExistsEvent

#from xml.etree import ElementTree


class AtomHopperClient(BaseMarshallingClient):

    def __init__(self, atom_feed_url, token=None, serialize_format='xml',
                 deserialize_format='xml'):
        self.atom_feed_url = atom_feed_url
        super(AtomHopperClient, self).__init__(serialize_format,
                                               deserialize_format)
        self.token = token
        if token is not None:
            self.default_headers['X-Auth-Token'] = token
        self.url = atom_feed_url

    def get_preconstructed_feed(self, url, requestslib_kwargs=None):
        requestslib_kwargs = requestslib_kwargs or {}
        return self.request(
            'GET', url, response_entity_type=AtomFeed, requestslib_kwargs=None)

    def get_feed(self, url=None, limit=None, search=None, params=None,
                 requestslib_kwargs=None):
        """
        @summary: Returns an iterable atom feed.
        @param url: the url used to get the atom feed (used for overriding the
                    instance's default self.atom_feed_url on a per-call basis)
        @type url: String
        @param limit: limits the results per page returned by the API. Added
                      to the Requests params dictionary
        @type limit: Int
        @param search: A string sent to the api. Added to the Requests params
                       dictionary
        @type search: String
        @param params: The query string paramters.
        @type params: Dictionary
        @return: The atom feed domain object.
        @rtype: Object(AtomFeed)
        """

        #Set 'limit' and 'search' in the 'params' dictionary unless those keys
        #already exist in 'params'.
        params = dict({'limit': limit, 'search': search}, **(params or {}))

        #Use the url that was set when this client was instantiated unless
        #another url is passed in to override it.
        url = url or self.atom_feed_url

        return self.request(
            'GET', url, params=params, response_entity_type=AtomFeed,
            requestslib_kwargs=requestslib_kwargs)

    def add_event(self, url=None, entity=None, requestslib_kwargs=None):
        """
        @summary: Posts an event to atom feed
        @param url: the url used to get the atom feed (used for overriding the
                    instance's default self.atom_feed_url on a per-call basis)
        @type url: String
        @param entity: Domain object for given product
        @type entity: Object(BaseMarshallingDomain)
        @return: The atom feed request response.
        @rtype: Object(Response)
        """
        url = url or self.atom_feed_url
        headers = {"content-type": "application/atom+{0}".format(
            self.serialize_format)}
        return self.request(
            'POST', url, request_entity=entity, headers=headers,
            requestslib_kwargs=requestslib_kwargs)


class NovaAtomHopperClient(AtomHopperClient):
    def add_event(
            self, tenant_id, option_id, flavor, datacenter, region, message_id,
            instance_id, audit_period_beginning, audit_period_ending,
            bw_in_public="0", bw_out_public="0", bw_in_private="0",
            bw_out_private="0", memory_mb="512MB", display_name="Fake Server"):
        """
        @summary: Posts an event to atom feed
        @return: The atom feed request response.
        @rtype: Object(Response)
        """
        entity = NovaExistsEvent(
            datacenter, region, message_id, audit_period_beginning,
            tenant_id, bw_in_public, bw_out_public, bw_in_private,
            bw_out_private, memory_mb, audit_period_ending, display_name,
            instance_id, option_id, flavor)

        return super(NovaAtomHopperClient, self).add_event(
            url=self.atom_feed_url, entity=entity, requestslib_kwargs=None)


class NovaCUFAtomHopperClient(AtomHopperClient):
    def add_event(
            self, datacenter, region, message_id, tenant_id, flavor_id,
            flavor_name, status, instance_id, audit_period_beginning,
            audit_period_ending, bw_in=0, bw_out=0, is_redhat="false",
            is_mssql="false", is_mssqlweb="false", is_windows="false",
            is_selinux="false", is_managed="false"):
        """
        @summary: Posts an event to atom feed
        @return: The atom feed request response.
        @rtype: Object(Response)
        """
        entity = NovaCUFExistsEvent(
            datacenter, region, message_id, tenant_id, flavor_id,
            flavor_name, status, instance_id, audit_period_beginning,
            audit_period_ending, bw_in, bw_out, is_redhat, is_mssql,
            is_mssqlweb, is_windows, is_selinux, is_managed)

        return super(NovaCUFAtomHopperClient, self).add_event(
            url=self.atom_feed_url, entity=entity, requestslib_kwargs=None)


class CBSAtomHopperClient(AtomHopperClient):
    def add_event(
            self, tenant_id, start_time, end_time, resource_id, message_type,
            region="ORD", datacenter="ORD1", environment="PROD",
            message_id=str(uuid.uuid4()), version="1",
            service_code="CloudBlockStorage", resource_type="VOLUME",
            snapshot=None, provisioned=None, vol_type=None):
        """
        @summary: Posts an event to atom feed
        @return: The atom feed request response.
        @rtype: Object(Response)
        """

        entity = CBSUsageEvent(
            tenant_id, start_time, end_time, resource_id, message_type, region,
            datacenter, environment, message_id, version, service_code,
            resource_type, snapshot, provisioned, vol_type)

        return super(CBSAtomHopperClient, self).add_event(
            url=self.atom_feed_url, entity=entity, requestslib_kwargs=None)


class LegacyAtomHopperClient(AtomHopperClient):
    def add_event(
            self, tenant_id, message_id, resource_id, datacenter, region,
            start_time, end_time, flavor, title="E2ECloud Server Uptime",
            version='1', service_code='CloudServers', resource_type='SLICE',
            bandwidth_in='0', bandwidth_out='0', extra_public_ips='1',
            extra_private_ips='1', is_redhat='false', is_mssql='false',
            is_mssqlweb='false', is_windows='false', is_selinux='false',
            is_managed='false'):

        """
        @summary: Posts an event to atom feed
        @return: The atom feed request response.
        @rtype: Object(Response)
        """
        entity = LegacyUsageEvent(
            title, tenant_id, message_id, resource_id, datacenter,
            region, start_time, end_time, version, service_code, resource_type,
            bandwidth_in, bandwidth_out, flavor, extra_public_ips,
            extra_private_ips, is_redhat, is_mssql, is_mssqlweb, is_windows,
            is_selinux, is_managed)

        return super(LegacyAtomHopperClient, self).add_event(
            url=self.atom_feed_url, entity=entity, requestslib_kwargs=None)

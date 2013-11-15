import re
import dateutil.parser

from ccengine.clients.atomhopper import AtomHopperClient as _AtomHopperClient
from ccengine.providers.base_provider import BaseProvider, ProviderActionResult
from ccengine.providers.auth.auth_api import AuthProvider as _AuthProvider
from ccengine.providers.identity.v2_0.identity_api import\
    IdentityAPIProvider as _IdentityAPIProvider
from ccengine.common.tools.datatools import string_to_datetime


class AtomHopperProvider(BaseProvider):
    SEARCH_FUTURE = 'previous'
    SEARCH_PAST = 'next'

    def __init__(self, url, config, username=None, api_key=None,
                 password=None):
        '''
            Requires a URL which should be the atom hopper feed url for
            whichever product is creating this provider
            Accepts a config for future comptability, doesn't use it for now
            Accepts auth credentials to auth an admin user to read atom hopper
            feeds.
        '''
        super(AtomHopperProvider, self).__init__()
        self.config = config

        serialize_format = None
        deserialize_format = None

        try:
            serialize_format = self.config.atomhopper.serializer
            deserialize_format = self.config.atomhopper.deserializer
        except:
            pass

        serialize_format = serialize_format or \
            self.config.misc.serializer
        deserialize_format = deserialize_format or \
            self.config.misc.deserializer

        #Configure auth/identity
        if (config.identity_api.api_key is not None or
                config.identity_api.password is not None):
            self.identity_api_provider = _IdentityAPIProvider(self.config)
            self.identity_data = self.identity_api_provider.authenticate()
            self.auth_token = self.identity_data.response.entity.token.id
        else:
            self.auth_provider = _AuthProvider(self.config)
            self.auth_data = self.auth_provider.authenticate()
            self.auth_token = self.auth_data.token.id

        self.feed_url = url
        self.client = _AtomHopperClient(self.feed_url, self.auth_token,
                                        serialize_format,
                                        deserialize_format)

    def latest_feed(self, limit=None):
        limit = limit or 100
        return self.client.get_feed(limit=limit).entity

    def next_feed(self, atom_feed_domain_object):
        url = atom_feed_domain_object.next
        if url is not None:
            return self.client.get_preconstructed_feed(url=url).entity
        else:
            return None

    def previous_feed(self, atom_feed_domain_object):
        url = atom_feed_domain_object.previous
        if url is not None:
            return self.client.get_preconstructed_feed(url=url).entity
        else:
            return None

    def events_by_tenantId(self, tenantId, days_back=1, limit=1000):
        search = '+tid:%s' % tenantId
        r = self.client.get_feed(limit=limit, search=search)
        return self._sort_events(r.entity.events)

    def events_by_tenantId_par(self, tenantId, days_back=1, limit=1000):
        provider_response = ProviderActionResult()
        search = '+tid:%s' % tenantId
        resp = self.client.get_feed(limit=limit, search=search)
        provider_response.response = resp
        provider_response.ok = resp.ok
        if resp.entity is not None:
            if getattr(resp.entity, 'events') is not None:
                provider_response.entity = self._sort_events(
                    resp.entity.events)
        else:
            provider_response.entity = None

        return provider_response

    def events_by_resourceId(self, resourceId, days_back=1, limit=1000):
        search = '+rid:%s' % resourceId
        r = self.client.get_feed(limit=limit, search=search)
        return self._sort_events(r.entity.events)

    def search_past_events_by_attribute(self, attribute, attribute_regex,
                                        cutoff_attribute=None,
                                        cutoff_regex=None,
                                        atom_feed_domain_object=None,
                                        results_per_feed=None):
        '''
        By default, searches from latest_feed(), backwards in time.
        search and cutoff values are interpreted as regular expressions.

        Attribute names come from the AtomEventDomainObjects on a per-product
        basis.  If you haven't created an AtomEventDomainObject for your
        product's atom feed, this isn't going to return any results.
        '''
        direction = self.SEARCH_PAST

        if atom_feed_domain_object is None:
            atom_feed_domain_object = self.latest_feed(limit=results_per_feed)

        return self._search_events_by_attribute(
                atom_feed_domain_object,
                attribute, attribute_regex,
                direction,
                cutoff_attribute=cutoff_attribute,
                cutoff_regex=cutoff_regex,
                results_per_feed=None)

    def search_future_events_by_attribute(self, attribute, attribute_regex,
                                          cutoff_attribute=None,
                                          cutoff_regex=None,
                                          atom_feed_domain_object=None,
                                          results_per_feed=None):
        '''
        This is usefull for searching forward in feeds from an older place
        in the feed.
        By default, searches from latest_feed(), forwards in time
        cutoff_value is interpreted as a regular expression (re.search())

        Attribute names come from the AtomEventDomainObjects on a per-product
        basis.  If you haven't created an AtomEventDomainObject for your
        product's atom feed, this isn't going to return any results.
        '''
        direction = self.SEARCH_FUTURE

        if atom_feed_domain_object is None:
            atom_feed_domain_object = self.latest_feed()

        return self._search_events_by_attribute(
                atom_feed_domain_object,
                attribute, attribute_regex,
                direction,
                cutoff_attribute=cutoff_attribute,
                cutoff_regex=cutoff_regex,
                results_per_feed=None)

    def _search_events_by_attribute(self, atom_feed_domain_object, attribute,
                                    attribute_regex, direction,
                                    cutoff_attribute=None, cutoff_regex=None,
                                    results_per_feed=None):
        '''
        Searches feeds forward or backward by iterating through 'next' and
        'previous' feed links.
        attribute and cutoff regex's are interpreted as regular expressions via
        re.search()
        Returns AtomEvent domain object when 'attribute' is found __eq__
        to 'attribute_value'
        Returns None when cutoff_attribute is found __eq__ to cutoff_value,
        or feed ends.

        Results per feed defaults to 100, but higher values are encouraged.
        Play with it until you find a time/performance balance you're happy
        with.
        '''
        feed = atom_feed_domain_object
        events = self._sort_events(feed.events)

        while True:
            for event in events:
                # Search for attrib
                if re.search(attribute_regex,
                             getattr(event, attribute, "")) is not None:
                    self.provider_log.info("Event with searched Regex \
                                            Found in AtomHopper Feed")
                    return event
                # Search for cutoff
                elif cutoff_attribute is not None:
                    if re.search(
                            cutoff_regex,
                            getattr(event, cutoff_attribute)) is not None:
                        return None

            if direction == self.SEARCH_FUTURE:
                feed = self.previous_feed(feed)

            elif direction == self.SEARCH_PAST:
                feed = self.next_feed(feed)

    def _sort_events(self, events, reverse=True):
        '''
        @summary: Given a list of events, return sorted list based on time
        @param events: List of events to be sorted
        @type events: list
        @param reverse: Sort order, ascending if False or descending if True
        @type reverse: boolean
        '''
        def get_compare_time(event):
            '''
            @note: if the event attribute for time is not listed below,
                you will need to add it
            '''
            if hasattr(event, 'eventTime') and event.eventTime is not None:
                return dateutil.parser.parse(event.eventTime)
            elif hasattr(event, 'startTime') and event.startTime is not None:
                return dateutil.parser.parse(event.startTime)
            elif hasattr(event, 'timestamp') and event.timestamp is not None:
                return dateutil.parser.parse(event.timestamp)
            else:
                return event
        ret = sorted(events, key=get_compare_time, reverse=reverse)
        return ret

    def search_compute_events_by_attribute(self,
                                           attribute,
                                           attribute_regex,
                                           atom_hopper_feed_limit=None,
                                           atom_hopper_pagination_limit=None):
        if atom_hopper_feed_limit is None:
            atom_hopper_feed_limit = self.config.\
                compute_api.atom_hopper_feed_limit
        feed = self.client.get_feed(self.feed_url,
                                    limit=atom_hopper_feed_limit).entity
        if atom_hopper_pagination_limit is None:
            atom_hopper_pagination_limit = self.config.compute_api.\
                atom_hopper_pagination_limit

        event_list = []
        for _ in range(int(atom_hopper_pagination_limit)):
            for event in feed.events:
                if hasattr(event.payload, attribute):
                    if re.search(attribute_regex,
                                 getattr(event.payload,
                                         attribute)) is not None:
                        event_list.append(event)
            feed = self.next_feed(feed)
        return event_list

    def get_events_by_audit_period(self, search_param,
                                   expected_audit_period_beginning,
                                   expected_audit_period_ending,
                                   atom_hopper_feed_limit=250,
                                   atom_hopper_pagination_limit=100):
        '''
        @summary: Given an audit period beginning/ending and event type as
            search param, fetches all the events; returns as list
        @param search_param: attribute on which feed will filtered on
            ex:  "+compute.instance.exists" or "+tid:12345"
        @type search_param: string
        @param expected_audit_period_beginning: The starting time
            of audit period
        @type expected_audit_period_beginning: datetime object
        @param expected_audit_period_ending: The ending time of audit period
        @type expected_audit_period_ending: datetime object
        @param atom_hopper_feed_limit: The max number of events to be
            returned in a feed
        @type atom_hopper_feed_limit: int
        @param atom_hopper_pagination_limit: The max number of feeds to be
            looped through
        @type atom_hopper_pagination_limit: int
        @note:  The events should have a payload section or this will fail
        '''
        found_last_entry_in_feed_within_audit_period = False
        feed_count = 0
        event_list = []
        feed = self.client.get_feed(self.feed_url,
                                    limit=atom_hopper_feed_limit,
                                    search=('{0}{1}'
                                            .format('+', search_param))).entity
        while not found_last_entry_in_feed_within_audit_period and\
                feed_count <= atom_hopper_pagination_limit:
            events = self._sort_events(feed.events)
            for event in events:
                if (hasattr(event.payload, 'audit_period_beginning') and
                        hasattr(event.payload, 'audit_period_ending')):
                    actual_audit_period_beginning = string_to_datetime(
                                    event.payload.audit_period_beginning)
                    actual_audit_period_ending = string_to_datetime(
                                    event.payload.audit_period_ending)
                    if (actual_audit_period_beginning >=
                        expected_audit_period_beginning and
                        actual_audit_period_ending <=
                            expected_audit_period_ending):
                        event_list.append(event)
                    elif (actual_audit_period_beginning <
                          expected_audit_period_beginning):
                        found_last_entry_in_feed_within_audit_period = True
                        break
            feed = self.next_feed(feed)
            feed_count += 1
        return event_list

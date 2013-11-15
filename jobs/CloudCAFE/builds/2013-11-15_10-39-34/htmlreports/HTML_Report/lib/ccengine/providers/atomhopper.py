from dateutil.parser import parse
import re
import time

from ccengine.clients.atomhopper import AtomHopperClient
from ccengine.common.exceptions.compute import TimeoutException
from ccengine.common.tools.datatools import string_to_datetime
from ccengine.providers.base_provider import BaseProvider
from ccengine.providers.identity.v2_0.identity_api import IdentityAPIProvider


class AtomHopperProvider(BaseProvider):
    """
    Creates an AtomHopper Client using either the provided auth token,
    user credentials, or configuration default (non-admin) user

    """
    SEARCH_FUTURE = 'previous'
    SEARCH_PAST = 'next'

    def __init__(
            self, url, config, username=None, api_key=None, password=None,
            auth_token=None):

        super(AtomHopperProvider, self).__init__()
        self.config = config
        #Set serialization/deserialization formats
        self.serialize_format = self.config.atomhopper.serializer
        self.deserialize_format = self.config.atomhopper.deserializer
        #Set auth token
        self.auth_token = None
        if auth_token is not None:
            self.auth_token = auth_token
        elif username is not None:
            #Get an auth token using the provided credentials
            identity_api_provider = IdentityAPIProvider(self.config)
            identity_api_provider.client = identity_api_provider.get_client(
                username=username, api_key=api_key, password=password)
            self.auth_token = identity_api_provider.get_token(
                username=username, password=password, api_key=api_key)
        else:
            #Auth with the default config non-admin user and get the auth token
            identity_api_provider = IdentityAPIProvider(self.config)
            auth_data = identity_api_provider.authenticate()
            self.auth_token = auth_data.entity.token.id

        if self.auth_token is None:
            self.provider_log.warning(
                "No valid auth token could be found/retrieved.  Continuing "
                "initialization of AtomHopper client with no auth token.")

        self.feed_url = url
        self.client = AtomHopperClient(
            self.feed_url, self.auth_token, self.serialize_format,
            self.deserialize_format)

    def latest_feed(self, limit=100):
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

    def events_by_tenant_id(self, tenant_id, days_back=1, limit=1000):
        search = '+tid:{0}'.format(tenant_id)
        r = self.client.get_feed(limit=limit, search=search)
        return self._sort_events(r.entity.events)

    def events_by_resource_id(self, resource_id, days_back=1, limit=1000):
        search = '+rid:{0}'.format(resource_id)
        r = self.client.get_feed(limit=limit, search=search)
        return self._sort_events(r.entity.events)

    def search_past_events_by_attribute(
            self, attribute, attribute_regex, cutoff_attribute=None,
            cutoff_regex=None, atom_feed_domain_object=None,
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
            atom_feed_domain_object, attribute, attribute_regex, direction,
            cutoff_attribute=cutoff_attribute, cutoff_regex=cutoff_regex,
            results_per_feed=None)

    def search_future_events_by_attribute(
            self, attribute, attribute_regex, cutoff_attribute=None,
            cutoff_regex=None, atom_feed_domain_object=None,
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
            atom_feed_domain_object, attribute, attribute_regex, direction,
            cutoff_attribute=cutoff_attribute, cutoff_regex=cutoff_regex,
            results_per_feed=None)

    def _search_events_by_attribute(
            self, atom_feed_domain_object, attribute, attribute_regex,
            direction, cutoff_attribute=None, cutoff_regex=None,
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
                attrib_result = re.search(
                    attribute_regex, getattr(event, attribute, ""))
                if attrib_result is not None:
                    self.provider_log.debug(
                        "Event with searched Regex Found in AtomHopper Feed")
                    return event

                # Search for cutoff
                elif cutoff_attribute is not None:
                    if re.search(
                            cutoff_regex,
                            getattr(event, cutoff_attribute, "")) is not None:
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
                return parse(event.eventTime)
            elif hasattr(event, 'startTime') and event.startTime is not None:
                return parse(event.startTime)
            elif hasattr(event, 'timestamp') and event.timestamp is not None:
                return parse(event.timestamp)
            else:
                return event
        ret = sorted(events, key=get_compare_time, reverse=reverse)
        return ret

    def search_compute_events_by_attribute(
            self, attribute, attribute_regex, atom_hopper_feed_limit=None,
            atom_hopper_pagination_limit=None, date_break=None):
        """
        @summary:  Search compute events by a given attribute
        @return: List of events
        @rtype: List
        @param attribute: The attribute type to search for in event
            e.g., "id"
        @type attribute: String
        @param attribute_regex: The contents of the attribute being searched
            e.g., "0573832d-f8f9-4a77-b654-685f2a14813"
        @param atom_hopper_feed_limit: The max number of events to be
            returned in a feed
        @type atom_hopper_feed_limit: Int
        @param atom_hopper_pagination_limit: The max number of feeds to be
            looped through
        @type atom_hopper_pagination_limit: Int
        @param date_break:  The date time of to break from paging through
            the feed based on the published date of an entry
        @type datetime: datetime
        @note:  The events should have a payload section or this will fail


        """
        atom_hopper_feed_limit = atom_hopper_feed_limit or \
            self.config.compute_api.atom_hopper_feed_limit
        atom_hopper_pagination_limit = atom_hopper_pagination_limit or \
            self.config.compute_api.atom_hopper_pagination_limit

        feed = self.client.get_feed(
            self.feed_url, limit=atom_hopper_feed_limit).entity
        if feed is None:
            self.provider_log.debug(
                "Call to get atomhopper feed returned empty or "
                "non-deserializable result")
            return None

        event_list = []
        for _ in range(int(atom_hopper_pagination_limit)):
            events = self._sort_events(feed.events)
            for event in events:
                try:
                    if hasattr(event.payload, attribute):
                        if re.search(
                            attribute_regex, getattr(
                                event.payload, attribute)) is not None:
                            event_list.append(event)
                except (TypeError, AttributeError) as err:
                    self.provider_log.error(
                        "{err_msg!s}\nevent:{event}\npayload:{payload}"
                        .format(err_msg=err, event=event,
                                payload=vars(event.payload)))
            if date_break:
                if (string_to_datetime(events[0].published) <
                        date_break):
                    break
            feed = self.next_feed(feed)

        self.provider_log.info("\nnumber of actual events: {0}".format(
            len(event_list)))
        for event in event_list:
            self.provider_log.info("\nevent_type: {0}".format(
                event.event_type))
            self.provider_log.info("event: {0}".format(
                event))

        return event_list

    def get_events_by_audit_period(
            self, search_param, expected_audit_period_beginning,
            expected_audit_period_ending, atom_hopper_feed_limit=250,
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
        search = '+{0}'.format(search_param)
        feed = self.client.get_feed(
            self.feed_url, limit=atom_hopper_feed_limit, search=search).entity

        if feed is None:
            self.provider_log.debug(
                "Call to get atomhopper feed returned empty or "
                "non-deserializable result")
            return None

        while not found_last_entry_in_feed_within_audit_period and\
                feed_count <= atom_hopper_pagination_limit:
            events = self._sort_events(feed.events)
            for event in events:
                if (hasattr(event.payload, 'audit_period_beginning') and
                        hasattr(event.payload, 'audit_period_ending')):
                    try:
                        actual_audit_period_beginning = string_to_datetime(
                            event.payload.audit_period_beginning)
                        actual_audit_period_ending = string_to_datetime(
                            event.payload.audit_period_ending)
                    except TypeError:
                        self.provider_log.error(
                            "Missing audit_period_beginning or "
                            "audit_period_ending.\nevent:{event}"
                            "\npayload:{payload}.".format(
                                event=event,
                                payload=vars(event.payload)))
                        continue
                    if (actual_audit_period_beginning >=
                        expected_audit_period_beginning and
                        actual_audit_period_ending <=
                            expected_audit_period_ending):
                        event_list.append(event)
                    elif (actual_audit_period_beginning <
                          expected_audit_period_beginning and
                          string_to_datetime(events[0].published) <
                          expected_audit_period_beginning):
                        found_last_entry_in_feed_within_audit_period = True
                        break
            feed = self.next_feed(feed)
            feed_count += 1
        return event_list

    def wait_for_atomhopper_timestamp(self, wait_for_target_timestamp,
                                      atom_hopper_feed_limit=5):
        """
        @summary:  Wait for latest AtomHopper timestamp to become later
            than a given timestamp
        @return:  True if timestamp found, None if no feed found
        @param wait_for_target_timestamp: The timestamp to wait for to pass
        @type wait_for_target_timestamp: Datetime
        @param atom_hopper_feed_limit: The max number of events to be
            returned in a feed
        @type atom_hopper_feed_limit: Int
        """

        time_waited = 0
        wait_interval = self.config.atomhopper.wait_interval
        wait_timeout = self.config.atomhopper.wait_timeout
        while (True):
            feed = self.client.get_feed(
                self.feed_url, limit=atom_hopper_feed_limit).entity
            if feed is None:
                self.provider_log.debug(
                    "Call to get atomhopper feed returned empty or "
                    "non-deserializable result")
                return None
            events = self._sort_events(feed.events, True)
            self.provider_log.info(
                "\nwait_for_timestamp: {0}".format(
                    wait_for_target_timestamp.strftime("%Y-%m-%dT%H:%M:%S")))

            for event in events:
                self.provider_log.info(
                    "event_timestamp: {0}".format(event.timestamp))
                if (string_to_datetime(event.timestamp) >=
                        wait_for_target_timestamp):
                    self.provider_log.info(
                        "Found timestamp after {0} seconds!"
                        .format(time_waited))
                    return True
            if time_waited > wait_timeout:
                raise TimeoutException("Timed out while waiting for "
                                       "AtomHopper to update.")
            self.provider_log.info(
                "Event timestamp not later than given timestamp, waiting {0} "
                "seconds before trying again".format(wait_interval))
            time.sleep(wait_interval)
            time_waited += wait_interval

    def wait_for_atomhopper_event(self, wait_for_event_type, attribute,
                                  attribute_regex, atom_hopper_feed_limit=5):
        """
        @summary:  Wait for latest AtomHopper event for a given attribute to
            become appear in the Atom Hopper feed
        @param wait_for_event_type: Event Type to wait for
        @type wait_for_event_type: String
        @param attribute: The attribute type to search for in event
            e.g., "instance_id"
        @type attribute: String
        @param attribute_regex: The contents of the attribute being searched
            e.g., "0573832d-f8f9-4a77-b654-685f2a14813"
        @param atom_hopper_feed_limit: The max number of events to be
            returned in a feed
        @type atom_hopper_feed_limit: Int
        @return: True if event found, None if no feed found
        """

        time_waited = 0
        wait_interval = self.config.atomhopper.wait_interval
        wait_timeout = self.config.atomhopper.wait_timeout

        search = '+{0}'.format(wait_for_event_type)
        while (True):
            feed = self.client.get_feed(self.feed_url,
                                        limit=atom_hopper_feed_limit,
                                        search=search).entity
            if feed is None:
                self.provider_log.debug(
                    "Call to get atomhopper feed returned empty or "
                    "non-deserializable result")
                return None
            events = self._sort_events(feed.events, True)
            self.provider_log.info(
                "wait_for_event: {0}".format(wait_for_event_type))

            for event in events:
                try:
                    if hasattr(event.payload, attribute):
                        self.provider_log.info(
                            "{0}: {1}".format(
                                event.event_type,
                                getattr(event.payload, attribute)))
                        if re.search(
                            attribute_regex, getattr(
                                event.payload, attribute)) is not None:
                            self.provider_log.info(
                                "Found event: {0} for {1}: {2} after "
                                "{3} seconds!".format(wait_for_event_type,
                                                      attribute,
                                                      attribute_regex,
                                                      time_waited))
                            return True
                except (TypeError, AttributeError) as err:
                    self.provider_log.error(
                        "{err_msg!s}\nevent:{event}\npayload:{payload}"
                        .format(err_msg=err, event=event,
                                payload=vars(event.payload)))
            if time_waited > wait_timeout:
                raise TimeoutException(
                    "Timed out while waiting for the events to post to "
                    " Atom Hopper. wait_for_event_type: "
                    "{0} attribute: {1} attribute_regex: {2} time_waited: {3}"
                    .format(wait_for_event_type, attribute,
                            attribute_regex, time_waited))
            self.provider_log.info(
                "Did not find event: {0} for {1}: {2}, waiting {3}"
                " seconds before trying again".format(wait_for_event_type,
                                                      attribute,
                                                      attribute_regex,
                                                      wait_interval))
            time.sleep(wait_interval)
            time_waited += wait_interval

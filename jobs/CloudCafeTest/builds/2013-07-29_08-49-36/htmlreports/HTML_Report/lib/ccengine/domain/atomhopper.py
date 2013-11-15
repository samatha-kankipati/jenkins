# from ccengine.domain.server_events import ComputeAtomPayload
from ccengine.domain.base_domain import BaseMarshallingDomain
from ccengine.domain.base_domain import BaseDomain

import json
from xml.etree import ElementTree


class AtomFeed(BaseMarshallingDomain):

    def __init__(self, event_list=None):
        # request attribs
        # None, requests are made only via paramaterized urls

        # response attribs
        self.events = event_list or []
        self.title = None
        self.self = None
        self.current = None
        self.previous = None
        self.next = None
        self.last = None

    # Response Deserializers
    @classmethod
    def _json_to_obj(cls, serialized_string):
        afobj = AtomFeed()
        root = json.loads(serialized_string)
        feed = root['feed']
        event_elements = feed['entries']
        if feed is not None:
            for key, value in feed.items():
                setattr(afobj, key, value)
            for link in feed.get('links'):
                rel = None
                href = None
                for key, value in link.iteritems():
                    if key == 'rel':
                        rel = value
                    if key == 'href':
                        href = value
                    if (rel is not None) and (href is not None):
                        setattr(afobj, rel, href)
        else:
            cls._log.info('Atom feed is empty (=None)')
        if event_elements is not None:
            for entry in event_elements:
                content = entry.get('content')
                event = content.get('children')[0]
                event_data = json.loads(event)
                if 'nova/events' or 'glance/events' in afobj.title:
                        afobj.events.append(NovaAtomEvent(**event_data))
                else:
                    cls._log.warning('Event Type Not Supported: %s'
                                                         % str(event_data.tag))

        return afobj

    @classmethod
    def _xml_to_obj(cls, serialized_string):
        '''
            Until someone clever figures out something better, you'll
            have to add an if statement here to support different
            event types, as defined by the title of the atomfeed:
        '''
        afobj = AtomFeed()
        root = ElementTree.XMLID(serialized_string)
        feed = root[0]
        event_elements = root[1]
        for child in feed.getchildren():
            rel = None
            href = None
            for item_tuple in child.items():
                if 'rel' in item_tuple:
                    rel = item_tuple[1]
                if 'href' in item_tuple:
                    href = item_tuple[1]
                if (rel is not None) and (href is not None):
                    setattr(afobj, rel, href)
        if feed is not None:
            ft = feed.find('%s}title' % feed.tag.split('}')[0])
            if ft is not None:
                afobj.title = ft.text
        else:
            cls._log.info('Atom feed is empty (=None)')

        if event_elements is not None:
            for ee in event_elements:
                event_data = event_elements[ee]
                if 'cbs/events' in afobj.title:
                    afobj.events.append(BlockStorageAtomEvent(event_data))
                if 'lbaas/events' in afobj.title:
                    afobj.events.append(LoadBalancersAtomEvent(event_data))
                if 'files/events' in afobj.title:
                    afobj.events.append(LoadBalancersAtomEvent(event_data))
                if 'namespace/feed' in afobj.title:
                    afobj.events.append(IdentityAtomEvent(event_data))
                # elif 'your/product' in afobj.title :
                #     afobj.events.append(YourProductAtomEvent(event_data))
                else:
                    cls._log.warning('Event Type Not Supported: %s'
                                                     % str(event_data.tag))
        if 'nova/events' in afobj.title or 'glance/events' in afobj.title:
            cls._remove_namespace(feed, 'http://www.w3.org/2005/Atom')
            events = []
            for entry in feed.findall('entry'):
                event = entry.find('content')
                event_data = json.loads(event.text)
                afobj.events.append(NovaAtomEvent(**event_data))

        return afobj

'''
@TODO: Decide if these product-specific atom events should be defined here
       or somewhere else (AtomEvent domain objects folder maybe?)
'''


class BlockStorageAtomEvent(BaseDomain):

    def __init__(self, event_data):
        self.dataCenter = event_data.get('dataCenter')
        self.resourceId = event_data.get('resourceId')
        self.region = event_data.get('region')
        self.tenantId = event_data.get('tenantId')
        self.version = event_data.get('version')
        self.startTime = event_data.get('startTime')
        self.endTime = event_data.get('endTime')
        self.type = event_data.get('type')
        self.id = event_data.get('id')

        class _Product(object):

            def __init__(self, event_data):
                self.resourceType = None
                self.version = None
                self.snapshot = None
                self.serviceCode = None
        self.product = _Product()

        product_data = event_data.getchildren()
        for p in product_data:
            if 'product' in p.tag:
                self.product.resourceType = p.get('resourceType')
                self.product.version = p.get('version')
                self.product.snapshot = p.get('snapshot')
                self.product.serviceCode = p.get('serviceCode')
                self.cdnBandwidthOut = p.get('serviceCode')


class LoadBalancersAtomEvent(BaseDomain):

    def __init__(self, event_data):
        self.dataCenter = event_data.get('dataCenter')
        self.resourceId = event_data.get('resourceId')
        self.region = event_data.get('region')
        self.tenantId = event_data.get('tenantId')
        self.version = event_data.get('version')
        self.startTime = event_data.get('startTime')
        self.endTime = event_data.get('endTime')
        self.type = event_data.get('type')
        self.id = event_data.get('id')
        self.eventTime = event_data.get('eventTime')

        class _Product(BaseDomain):

            def __init__(self):
                self.avgConcurrentConnections = None
                self.avgConcurrentConnectionsSsl = None
                self.bandWidthIn = None
                self.bandWidthOut = None
                self.bandWidthInSsl = None
                self.bandWidthOutSsl = None
                self.numPolls = None
                self.numVips = None
                self.resourceType = None
                self.serviceCode = None
                self.sslMode = None
                self.status = None
                self.version = None
                self.vipType = None

        self.product = _Product()
        product_data = event_data.getchildren()
        for p in product_data:
            if 'product' in p.tag:
                self.product.avgConcurrentConnections = \
                                              p.get('avgConcurrentConnections')
                self.product.avgConcurrentConnectionsSsl = \
                                           p.get('avgConcurrentConnectionsSsl')
                self.product.bandWidthIn = p.get('bandWidthIn')
                self.product.bandWidthOut = p.get('bandWidthOut')
                self.product.bandWidthInSsl = p.get('bandWidthInSsl')
                self.product.bandWidthOutSsl = p.get('bandWidthOutSsl')
                self.product.numPolls = p.get('numPolls')
                self.product.numVips = p.get('numVips')
                self.product.resourceType = p.get('resourceType')
                self.product.serviceCode = p.get('serviceCode')
                self.product.sslMode = p.get('sslMode')
                self.product.status = p.get('status')
                self.product.version = p.get('version')
                self.product.vipType = p.get('vipType')


class CloudFilesAtomEvent(BaseDomain):

    def __init__(self, event_data):
        self.dataCenter = event_data.get('dataCenter')
        self.region = event_data.get('region')
        self.startTime = event_data.get('startTime')
        self.end_time = event_data.get('endTime')
        self.tenantId = event_data.get('tenantId')
        self.type = event_data.get('type')
        self.version = event_data.get('version')

        class _Product(object):

            def __init__(self, event_data):
                self.costops = None
                self.disk = None
                self.freeops = None
                self.serviceCode = None
                self.version = None

        self.product = _Product()
        product_data = event_data.getchildren()
        for p in product_data:
            if 'product' in p.tag:
                self.product.resourceType = p.get('resourceType')
                self.product.version = p.get('version')
                self.product.snapshot = p.get('snapshot')
                self.product.serviceCode = p.get('serviceCode')
                self.product.version = p.get('version')


class NovaAtomEvent(BaseMarshallingDomain):

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

        class _Payload(object):

            def __init__(self, **kwargs):
                for key, value in kwargs.items():
                    setattr(self, key, value)

        class _Image_Meta(object):

            def __init__(self, **kwargs):
                for key, value in kwargs.items():
                    setattr(self, key, value)

        class _Bandwidth(object):

            def __init__(self, **kwargs):
                for key, value in kwargs.items():
                    setattr(self, key, value)

        if self.payload is not None:
            self.payload = _Payload(**self.payload)
            if self.payload.image_meta is not None:
                self.payload.image_meta = \
                    _Image_Meta(**self.payload.image_meta)
            if self.payload.bandwidth is not None:
                self.payload.bandwidth = _Bandwidth(**self.payload.bandwidth)


class IdentityAtomEvent(BaseDomain):

    def __init__(self, event_data):
        self.dataCenter = event_data.get('dataCenter')
        self.environment = event_data.get('environment')
        self.eventTime = event_data.get('eventTime')
        self.id = event_data.get('id')
        self.region = event_data.get('region')
        self.resourceId = event_data.get('resourceId')
        self.resourceName = event_data.get('resourceName')
        self.type = event_data.get('type')
        self.version = event_data.get('version')

        class _Product(object):

            def __init__(self):
                self.displayName = None
                self.migrated = None
                self.resourceType = None
                self.roles = None
                self.serviceCode = None
                self.version = None

        self.product = _Product()
        product_data = event_data.getchildren()

        for p in product_data:
            if 'product' in p.tag:
                self.product.displayName = p.get('displayName')
                self.product.migrated = p.get('migrated')
                self.product.resourceType = p.get('resourceType')
                self.product.roles = p.get('roles')
                self.product.groups = p.get('groups')
                self.product.serviceCode = p.get('serviceCode')
                self.product.version = p.get('version')

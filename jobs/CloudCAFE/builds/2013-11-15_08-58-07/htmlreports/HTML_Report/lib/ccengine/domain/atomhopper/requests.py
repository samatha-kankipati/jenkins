import json
import uuid
import xml.etree.ElementTree as ET

from ccengine.domain.base_domain import BaseMarshallingDomain

LEGACY_BANDWIDTH = "E2ECloud server BandWidth"
LEGACY_RHEL = "E2E Cloud Server RHEL Count"
LEGACY_UPTIME = "E2ECloud Server Uptime"


class NovaExistsEvent(BaseMarshallingDomain):
    def __init__(
            self, datacenter, region, message_id, audit_period_beginning,
            tenant_id, bw_in_public, bw_out_public, bw_in_private,
            bw_out_private, memory_mb, audit_period_ending, display_name,
            instance_id, option_id, flavor):
        self.datacenter = datacenter
        self.region = region
        self.message_id = message_id
        self.audit_period_beginning = audit_period_beginning
        self.tenant_id = tenant_id
        self.bw_in_public = bw_in_public
        self.bw_out_public = bw_out_public
        self.bw_in_private = bw_in_private
        self.bw_out_private = bw_out_private
        self.memory_mb = memory_mb
        self.audit_period_ending = audit_period_ending
        self.display_name = display_name
        self.instance_id = instance_id
        self.flavor = flavor
        self.option_id = option_id

    def _obj_to_xml(self):
        entry = ET.Element('entry')
        entry = self._set_xml_attrs(
            entry, {"xmlns": "http://www.w3.org/2005/Atom"})

        title = ET.Element('title')
        title.text = "compute.instance.exists"
        entry.append(title)

        message_id = ET.Element('id')
        message_id.text = self.message_id
        entry.append(message_id)

        summary = ET.Element('summary')
        summary.text = "compute.instance.exists"
        entry.append(summary)

        category = ET.Element('category')
        category = self._set_xml_attrs(
            category, {"term": "compute.instance.exists"})
        entry.append(category)

        category = ET.Element('category')
        category = self._set_xml_attrs(
            category, {"term": "DATACENTER={0}".format(self.datacenter)})
        entry.append(category)

        category = ET.Element('category')
        category = self._set_xml_attrs(
            category, {"term": "REGION={0}".format(self.region)})
        entry.append(category)

        content = ET.Element('content')

        dic = {}
        dic["event_type"] = "compute.instance.exists"
        dic["timestamp"] = "2013-05-11 23:25:01.262380"
        dic["message_id"] = self.message_id
        dic["priority"] = "INFO"
        dic["publisher_id"] = "compute.c-10-23-209-59"

        #set root dictionary payload dic
        payload = {}
        payload["audit_period_beginning"] = self.audit_period_beginning
        payload["tenant_id"] = self.tenant_id
        payload["memory_mb"] = self.memory_mb
        payload["audit_period_ending"] = self.audit_period_ending
        payload["display_name"] = self.display_name
        payload["instance_id"] = self.instance_id
        payload["state_description"] = ""
        payload["original_image_ref_url"] = ""
        payload["availability_zone"] = None
        payload["ephemeral_gb"] = 0
        payload["instance_type_id"] = self.flavor
        payload["deleted_at"] = None
        payload["reservation_id"] = "r-rfk5hiqs"
        payload["user_id"] = "162190"
        payload["state"] = "active"
        payload["launched_at"] = "2013-05-21 11:49:00"
        payload["metadata"] = []
        payload["ramdisk_id"] = ""
        payload["access_ip_v6"] = "2001:4801:7817:0072:391e:e4b3:ff10:0cd0"
        payload["disk_gb"] = 20
        payload["access_ip_v4"] = "67.207.152.70"
        payload["kernel_id"] = ""
        payload["base_image_ref_url"] = ""
        payload["host"] = "c-10-23-209-59"
        payload["image_ref_url"] = "http://10.24.18.73:9292/images/"\
                                   "0790c8c7-1bbe-470c-9403-88883982b5fb"
        payload["created_at"] = "2013-05-11 23:23:06"
        payload["instance_type"] = "{0}Standard Instance".format(
            self.memory_mb)
        payload["vcpus"] = "1"
        payload["architecture"] = None
        payload["os_type"] = "linux"

        #set payload bandwidth dic
        bandwidth = {}
        bandwidth["public"] = {"bw_in": self.bw_in_public,
                               "bw_out": self.bw_out_public}
        bandwidth["private"] = {"bw_in": self.bw_in_private,
                                "bw_out": self.bw_out_private}
        payload["bandwidth"] = bandwidth

        #set image_meta bandwidth dic
        image_meta = {}
        image_meta["os_distro"] = "centos"
        image_meta["com.rackspace__1__visible_core"] = 1
        image_meta["com.rackspace__1__build_rackconnect"] = "1"
        image_meta["image_type"] = "base"
        image_meta["org.openstack__1__os_version"] = "12.04"
        image_meta["org.openstack__1__os_distro"] = "com.ubuntu"
        image_meta["rax_managed"] = "false"
        image_meta["os_version"] = "6.3"
        image_meta["com.rackspace__1__visible_rackconnect"] = "1"
        image_meta["rax_options"] = "0"
        image_meta["auto_disk_config"] = "True"
        image_meta["com.rackspace__1__options"] = self.option_id
        image_meta["com.rackspace__1__visible_managed"] = "1"
        image_meta["com.rackspace__1__build_core"] = "1"
        image_meta["arch"] = "x86-64"
        image_meta["os_type"] = "linux"
        image_meta["org.openstack__1__architecture"] = "x86-64"
        image_meta["com.rackspace__1__build_managed"] = "1"
        payload["image_meta"] = image_meta
        dic["payload"] = payload

        content.text = json.dumps(dic)
        content = self._set_xml_attrs(content, {"type": "application/json"})
        entry.append(content)
        return ET.tostring(entry)


class NovaCUFExistsEvent(BaseMarshallingDomain):
    def __init__(self, datacenter, region, message_id, tenant_id, flavor_id,
                 flavor_name, status, instance_id, audit_period_beginning,
                 audit_period_ending, bw_in, bw_out, is_redhat, is_mssql,
                 is_mssqlweb, is_windows, is_selinux, is_managed):
        self.datacenter = datacenter
        self.region = region
        self.message_id = message_id
        self.tenant_id = tenant_id
        self.flavor_id = flavor_id
        self.flavor_name = flavor_name
        self.status = status
        self.instance_id = instance_id
        self.audit_period_beginning = audit_period_beginning
        self.audit_period_ending = audit_period_ending
        self.bw_in = bw_in
        self.bw_out = bw_out
        self.is_redhat = is_redhat
        self.is_mssql = is_mssql
        self.is_mssqlweb = is_mssqlweb
        self.is_windows = is_windows
        self.is_selinux = is_selinux
        self.is_managed = is_managed

    def _obj_to_xml(self):
        entry = ET.Element('entry')
        entry = self._set_xml_attrs(
            entry, {"xmlns": "http://www.w3.org/2005/Atom"})

        title = ET.Element('title')
        title.text = "Server"
        entry.append(title)

        content = ET.Element('content')
        content = self._set_xml_attrs(
            content, {"type": "application/xml"})
        entry.append(content)

        event = ET.Element('event')
        event = self._set_xml_attrs(
            event, {"xmlns": "http://docs.rackspace.com/core/event",
                    "xmlns:nova": "http://docs.rackspace.com/event/nova",
                    "type": "USAGE",
                    "version": "1",
                    "tenantId": "{0}".format(self.tenant_id),
                    "id": "{0}".format(self.message_id),
                    "resourceId": "{0}".format(self.instance_id),
                    "dataCenter": "{0}".format(self.datacenter),
                    "region": "{0}".format(self.region),
                    "startTime": "{0}".format(self.audit_period_beginning),
                    "endTime": "{0}".format(self.audit_period_ending)})
        content.append(event)

        product = ET.Element('nova:product')
        product = self._set_xml_attrs(
            product, {"version": "1",
                      "serviceCode": "CloudServersOpenStack",
                      "resourceType": "SERVER",
                      "flavorId": "{0}".format(self.flavor_id),
                      "flavorName": "{0}".format(self.flavor_name),
                      "status": "{0}".format(self.status),
                      "isRedHat": "{0}".format(self.is_redhat),
                      "isMSSQL": "{0}".format(self.is_mssql),
                      "isMSSQLWeb": "{0}".format(self.is_mssqlweb),
                      "isWindows": "{0}".format(self.is_windows),
                      "isSELinux": "{0}".format(self.is_managed),
                      "isManaged": "{0}".format(self.is_managed),
                      "bandwidthIn": "{0}".format(self.bandwidthIn),
                      "bandwidthOut": "{0}".format(self.bandwidthOut)})
        event.append(product)
        return ET.tostring(entry)


class CBSUsageEvent(BaseMarshallingDomain):
    def __init__(
            self, tenant_id, start_time, end_time, resource_id, message_type,
            region, datacenter, environment, message_id, version, service_code,
            resource_type, snapshot, provisioned, vol_type):

        self.tenant_id = tenant_id
        self.start_time = start_time
        self.end_time = end_time
        self.resource_id = resource_id
        self.message_type = message_type
        self.region = region
        self.datacenter = datacenter
        self.environment = environment
        self.message_id = message_id
        self.version = version
        self.service_code = service_code
        self.resource_type = resource_type
        self.snapshot = snapshot
        self.provisioned = provisioned
        self.vol_type = vol_type

    def _obj_to_xml(self):
        entry = ET.Element('entry')
        entry = self._set_xml_attrs(
            entry, {"xmlns": "http://www.w3.org/2005/Atom"})

        title = ET.Element('title')
        title.text = "CBS Usage"
        entry.append(title)

        message_id = ET.Element('id')
        message_id.text = "urn:uuid:{0}".format(self.message_id)
        entry.append(message_id)

        #tenant ID example 5821894
        category = ET.Element('category')
        category = self._set_xml_attrs(
            category, {"term": "tid:{0}".format(self.tenant_id)})
        entry.append(category)

        #region DFW, ORD
        category = ET.Element('category')
        category = self._set_xml_attrs(
            category, {"term": "rgn:{0}".format(self.region)})
        entry.append(category)

        #datacenter DFW2, ORD1.....
        category = ET.Element('category')
        category = self._set_xml_attrs(
            category, {"term": "dc:{0}".format(self.datacenter)})
        entry.append(category)

        #this is normally a volume ID but can be set to testvolume
        category = ET.Element('category')
        category = self._set_xml_attrs(
            category, {"term": "rid:{0}".format(self.resource_id)})
        entry.append(category)

        #message type cloudblockstorage.snapshot.volume.usage or
        #cloudblockstorage.cbs.volume.usage
        category = ET.Element('category')
        category = self._set_xml_attrs(
            category, {"term": "{0}".format(self.message_type)})
        entry.append(category)

        #Start creating content
        content = ET.Element('content')
        content = self._set_xml_attrs(content, {"type": "application/xml"})

        #start creating content sub tree event
        event = ET.Element('event')
        dic = {}
        dic["xmlns"] = "http://docs.rackspace.com/core/event"
        if self.message_type == "cloudblockstorage.cbs.volume.usage":
            dic["xmlns:cbs"] = "http://docs.rackspace.com/usage/cbs"
        elif self.message_type == "cloudblockstorage.snapshot.volume.usage":
            dic["xmlns:cbs"] = "http://docs.rackspace.com/usage/cbs/snapshot"
        else:
            raise Exception("Message type should be "
                            "cloudblockstorage.snapshot.volume.usage or "
                            "cloudblockstorage.cbs.volume.usage")
        dic["dataCenter"] = self.datacenter
        dic["endTime"] = self.end_time
        dic["environment"] = self.environment
        dic["id"] = self.message_id
        dic["region"] = self.region
        dic["resourceId"] = self.resource_id
        dic["startTime"] = self.start_time
        dic["tenantId"] = self.tenant_id
        dic["type"] = "USAGE"
        dic["version"] = self.version
        event = self._set_xml_attrs(event, dic)

        #Start creating event subtree product
        product = ET.Element('cbs:product')
        dic = {}
        dic["resourceType"] = self.resource_type
        dic["serviceCode"] = self.service_code
        if self.message_type == "cloudblockstorage.cbs.volume.usage":
            dic["provisioned"] = self.provisioned
            dic["type"] = self.vol_type
        elif self.message_type == "cloudblockstorage.snapshot.volume.usage":
            dic["snapshot"] = self.snapshot

        dic["version"] = self.version
        product = self._set_xml_attrs(product, dic)

        #add product to event
        event.append(product)
        #add event to content
        content.append(event)
        #add content to entry
        entry.append(content)

        return ET.tostring(entry)


class LegacyUsageEvent(BaseMarshallingDomain):
    def __init__(
            self, title, tenant_id, message_id, resource_id, datacenter,
            region, start_time, end_time, version, service_code, resource_type,
            bandwidth_in, bandwidth_out, flavor, extra_public_ips,
            extra_private_ips, is_redhat, is_mssql, is_mssqlweb, is_windows,
            is_selinux, is_managed):

        self.title = title
        self.tenant_id = tenant_id
        self.message_id = message_id
        self.resource_id = resource_id
        self.datacenter = datacenter
        self.region = region
        self.start_time = start_time
        self.end_time = end_time
        self.version = version
        if self.title == LEGACY_BANDWIDTH:
            self.product = LegacyBandwidthProduct(
                version, service_code, resource_type, bandwidth_in,
                bandwidth_out)
        elif self.title == LEGACY_RHEL:
            self.product = LegacyRHELProduct(version, service_code)
        elif self.title == LEGACY_UPTIME:
            self.product = LegacyUptimeProduct(
                version, service_code, resource_type, flavor, extra_public_ips,
                extra_private_ips, is_redhat, is_mssql, is_mssqlweb,
                is_windows, is_selinux, is_managed)
        else:
            raise TypeError("Invalid Event Type {0}".format(self.title))

    def _obj_to_xml(self):

        entry = ET.Element('entry')
        entry = self._set_xml_attrs(
            entry, {"xmlns": "http://www.w3.org/2005/Atom"})

        #create title
        title = ET.Element('title')
        title.text = self.title
        entry.append(title)

        #create content
        content = ET.Element('content')
        content = self._set_xml_attrs(content, {"type": "application/xml"})

        #create event
        event = ET.Element('event')
        e_att = {}
        e_att["xmlns"] = 'http://docs.rackspace.com/core/event'
        if self.title == LEGACY_BANDWIDTH:
            e_att["xmlns:cs"] = 'http://docs.rackspace.com'\
                '/event/servers/bandwidth'
        elif self.title == LEGACY_RHEL:
            e_att["xmlns:rh"] = 'http://docs.rackspace.com/event/RHEL'
        elif self.title == LEGACY_UPTIME:
            e_att["xmlns:cs"] = 'http://docs.rackspace.com/event/servers'
        e_att["version"] = self.version
        e_att["tenantId"] = self.tenant_id
        e_att["id"] = self.message_id
        e_att["resourceId"] = self.resource_id
        e_att["type"] = "USAGE"
        e_att["dataCenter"] = self.datacenter
        e_att["region"] = self.region
        e_att["startTime"] = self.start_time
        e_att["endTime"] = self.end_time
        event = self._set_xml_attrs(event, e_att)
        event.append(self.product.get_xml_obj())
        content.append(event)
        entry.append(content)

        return ET.tostring(entry)


class LegacyUptimeProduct(BaseMarshallingDomain):
    def __init__(
            self, version, service_code, resource_type, flavor,
            extra_public_ips, extra_private_ips, is_redhat, is_mssql,
            is_mssqlweb, is_windows, is_selinux, is_managed):
        self.version = version
        self.service_code = service_code
        self.resource_type = resource_type
        self.flavor = flavor
        self.extra_public_ips = extra_public_ips
        self.extra_private_ips = extra_private_ips
        self.is_redhat = is_redhat
        self.is_mssql = is_mssql
        self.is_mssqlweb = is_mssqlweb
        self.is_windows = is_windows
        self.is_selinux = is_selinux
        self.is_managed = is_managed

    def get_xml_obj(self):
        product = ET.Element('cs:product')
        attribs = {}
        attribs['version'] = self.version
        attribs['serviceCode'] = self.service_code
        attribs['resourceType'] = self.resource_type
        attribs['flavor'] = self.flavor
        attribs['extraPublicIPs'] = self.extra_public_ips
        attribs['extraPrivateIPs'] = self.extra_private_ips
        attribs['isRedHat'] = self.is_redhat
        attribs['isMSSQL'] = self.is_mssql
        attribs['isMSSQLWeb'] = self.is_mssqlweb
        attribs['isWindows'] = self.is_windows
        attribs['isSELinux'] = self.is_selinux
        attribs['isManaged'] = self.is_managed
        product = self._set_xml_attrs(product, attribs)
        return product


class LegacyBandwidthProduct(BaseMarshallingDomain):
    def __init__(self, version, service_code, resource_type, bandwidth_in,
                 bandwidth_out):
        self.version = version
        self.service_code = service_code
        self.resource_type = resource_type
        self.bandwidth_in = bandwidth_in
        self.bandwidth_out = bandwidth_out

    def get_xml_obj(self):
        product = ET.Element('cs:product')
        attribs = {}
        attribs['version'] = self.version
        attribs['serviceCode'] = self.service_code
        attribs['resourceType'] = self.resource_type
        attribs['bandwidthIn'] = self.bandwidth_in
        attribs['bandwidthOut'] = self.bandwidth_out
        product = self._set_xml_attrs(product, attribs)
        return product


class LegacyRHELProduct(BaseMarshallingDomain):
    def __init__(self, version, service_code):
        self.version = version
        self.service_code = service_code

    def get_xml_obj(self):
        product = ET.Element('rh:product')
        attribs = {}
        attribs['version'] = self.version
        attribs['serviceCode'] = self.service_code
        product = self._set_xml_attrs(product, attribs)
        return product

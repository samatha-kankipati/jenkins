import json

from ccengine.domain.base_domain import BaseMarshallingDomain


class Device(BaseMarshallingDomain):
    """@summary: Represents the Device Domain Object"""

    def __init__(self, status_number=None, product_number=None,
                 leased_to_own=None, billing_notes=None, server_name=None,
                 computer_number=None, datacenter_number=None,
                 creation_date=None, primary_dns=None, product_id=None,
                 modification_date=None, customer_number=None,
                 enc_primary_userid=None, datacenter=None,
                 port_number=None, icon_file=None, comments=None,
                 comp_val_servertypeid=None, rba_login_method=None,
                 final_setup=None, rba_root_access=None, final_monthly=None,
                 gateway=None, cntr_xref_contract_server=None,
                 enc_root_password=None, contract_term=None,
                 sec_last_mod=None, server_parts=None, sec_created=None,
                 enc_rack_password=None, enc_primary_userid_password=None,
                 status=None, referal_code=None, secondary_dns=None,
                 account=None, enc_webmin_port=None, enc_webmin_password=None,
                 server_nickname=None, config_built_by_id=None,
                 xref_computer_rotation_cycle=None, due_to_support_date=None,
                 enc_notes=None, mntr_monitorednodeid=None, due_date=None,
                 device_contents=None, cert_xref_comp_cert=None,
                 server_xref_custom_monitor=None, enc_cvuser_password=None,
                 comp_ssh_key_pair=None, switch_number=None,
                 enc_rba_login_user_password=None, enc_rba_login_user=None,
                 storage=None):
        self.status_number = status_number
        self.product_number = product_number
        self.leased_to_own = leased_to_own
        self.billing_notes = billing_notes
        self.server_name = server_name
        self.computer_number = computer_number
        self.datacenter_number = datacenter_number
        self.creation_date = creation_date
        self.primary_dns = primary_dns
        self.product_id = product_id
        self.modification_date = modification_date
        self.customer_number = customer_number
        self.enc_primary_userid = enc_primary_userid
        self.datacenter = datacenter
        self.port_number = port_number
        self.icon_file = icon_file
        self.comments = comments
        self.comp_val_server_typeid = comp_val_servertypeid
        self.rba_login_method = rba_login_method
        self.final_setup = final_setup
        self.rba_root_access = rba_root_access
        self.final_monthly = final_monthly
        self.gateway = gateway
        self.cntr_xref_contract_server = cntr_xref_contract_server
        self.enc_root_password = enc_root_password
        self.contract_term = contract_term
        self.sec_last_mod = sec_last_mod
        self.server_parts = server_parts
        self.sec_created = sec_created
        self.enc_rack_password = enc_rack_password
        self.enc_primary_userid_password = enc_primary_userid_password
        self.status = status
        self.referal_code = referal_code
        self.secondary_dns = secondary_dns
        self.account = account
        self.enc_webmin_port = enc_webmin_port
        self.enc_webmin_password = enc_webmin_password
        self.server_nickname = server_nickname
        self.config_built_by_id = config_built_by_id
        self.xref_computer_rotation_cycle = xref_computer_rotation_cycle
        self.due_to_support_date = due_to_support_date
        self.enc_notes = enc_notes
        self.mntr_monitored_nodeid = mntr_monitorednodeid
        self.due_date = due_date
        self.device_contents = device_contents
        self.cert_xref_comp_cert = cert_xref_comp_cert
        self.server_xref_custom_monitor = server_xref_custom_monitor
        self.enc_cvuser_password = enc_cvuser_password
        self.comp_ssh_key_pair = comp_ssh_key_pair
        self.switch_number = switch_number
        self.enc_rba_login_user_password = enc_rba_login_user_password
        self.enc_rba_login_user = enc_rba_login_user
        self.storage = storage

    @classmethod
    def _json_to_obj(cls, serialized_str):
        ret = None
        json_dict = json.loads(serialized_str)
        device = cls._dict_to_obj(json_dict['device'])
        if device.server_parts is not None:
            device.server_parts = ServerParts._json_to_obj(device.server_parts)
        if device.cert_xref_comp_cert is not None:
            device.cert_xref_comp_cert = \
                CertXrefCompCert._json_to_obj(device.cert_xref_comp_cert)
        return device

    @classmethod
    def _dict_to_obj(cls, device_dict):

        for key in device_dict.keys():
            device_dict[key.lower()] = device_dict.pop(key)
        device = Device(**device_dict)
        if device.cntr_xref_contract_server is not None:
            device.cntr_xref_contract_server = \
                CntrXrefContractServer._dict_to_obj(
                    device.cntr_xref_contract_server
                )
        if device.xref_computer_rotation_cycle is not None:
            device.xref_computer_rotation_cycle = \
                XrefComputerRotationCycle._dict_to_obj(
                    device.xref_computer_rotation_cycle
                )
        if device.device_contents is not None:
            device.device_contents = \
                DeviceContents._dict_to_obj(device.device_contents)
        if device.server_xref_custom_monitor is not None:
            device.server_xref_custom_monitor = \
                ServerXrefCustomMonitor._dict_to_obj(
                    device.server_xref_custom_monitor
                )
        return device


class Devices(Device):
    """@summary: Represents a list of devices"""

    @classmethod
    def _json_to_obj(cls, serialized_str):
        devices = []
        json_dict = json.loads(serialized_str)
        for device in json_dict['devices']:
            device_list = cls._dict_to_obj(device)
            devices.append(device_list)
        return devices


class CntrXrefContractServer(BaseMarshallingDomain):
    """@summary: CNTR_xref_Contract_Server Response Object for Device."""
    def __init__(self, creation_date=None, cntr_contractid=None,
                 modification_date=None):
        self.creation_date = creation_date
        self.cntr_contractid = cntr_contractid
        self.modification_date = modification_date

    @classmethod
    def _dict_to_obj(self, cntr_dict):
        for key in cntr_dict.keys():
                cntr_dict[key.lower()] = cntr_dict.pop(key)
        return CntrXrefContractServer(**cntr_dict)


class XrefComputerRotationCycle(BaseMarshallingDomain):
    """@summary: xref_computer_rotation_cycle Response Object for Device"""
    def __init__(self, creation_date=None, modification_date=None,
                 rotation_cycle_number=None):
        self.creation_date = creation_date
        self.rotation_cycle_number = rotation_cycle_number
        self.modification_date = modification_date

    @classmethod
    def _dict_to_obj(self, xref_dict):
        return XrefComputerRotationCycle(**xref_dict)


class DeviceContents(BaseMarshallingDomain):
    """@summary: device_contents Response Object for Device."""
    def __init__(self, creation_date=None, modification_date=None,
                 slot_num=None, container=None):
        self.creation_date = creation_date
        self.modification_date = modification_date
        self.slot_num = slot_num
        self.container = container

    @classmethod
    def _dict_to_obj(self, device_dict):
        return DeviceContents(**device_dict)


class CertXrefCompCert(BaseMarshallingDomain):
    """@summary: CERT_xref_Comp_Cert Response Object for Device."""
    def __init__(self, creation_date=None, modification_date=None,
                 certificate_id=None):
        self.creation_date = creation_date
        self.modification_date = modification_date
        self.certificate_id = certificate_id

    @classmethod
    def json_to_obj(cls, json_dict):
        cert_xref_comp_cert_list = []
        for cert_dict in json_dict:
            cert_obj = cls._dict_to_obj(cert_dict)
            cert_xref_comp_cert_list.append(cert_obj)
        return cert_xref_comp_cert_list

    @classmethod
    def _dict_to_obj(cls, cert_dict):
        return CertXrefCompCert(**cert_dict)


class ServerXrefCustomMonitor(BaseMarshallingDomain):
    """@summary: server_xref_custom_monitor Response Object for Device."""
    def __init__(self, custom_monitor_id=None, creation_date=None,
                 parent_monitor=None, notes=None, modification_date=None):
        self.creation_date = creation_date
        self.custom_monitor_id = custom_monitor_id
        self.modification_date = modification_date
        self.notes = notes
        self.parent_monitor = parent_monitor

    @classmethod
    def _dict_to_obj(self, server_xref_dict):
        return ServerXrefCustomMonitor(**server_xref_dict)


class ServerParts(BaseMarshallingDomain):
    """@summary: Server_parts Response Object for Device."""
    def __init__(self, request_part=None, modification_date=None,
                 sec_created=None, product_price=None, product_sku=None,
                 creation_date=None, product_label=None, product_page=None,
                 sec_last_mod=None):
        self.request_part = request_part
        self.modification_date = modification_date
        self.sec_created = sec_created
        self.product_sku = product_sku
        self.creation_date = creation_date
        self.product_label = product_label
        self.product_page = product_page
        self.sec_last_mod = sec_last_mod

    @classmethod
    def _json_to_obj(cls, json_dict):
        server_parts_list = []
        for server_part_dict in json_dict:
            server_part = cls._dict_to_obj(server_part_dict)
            server_parts_list.append(server_part)
        return server_parts_list

    @classmethod
    def _dict_to_obj(cls, server_part_dict):
        return ServerParts(**server_part_dict)


import json

from ccengine.domain.base_domain import BaseMarshallingDomain


class AccountDetails(BaseMarshallingDomain):
    def __init__(self, primary_contact_id, create_date, cloud_accounts,
                 status_id, support_team_name, status_name,
                 emergency_instructions):
        super(AccountDetails, self).__init__()
        self.primary_contact_id = primary_contact_id
        self.create_date = create_date
        self.cloud_accounts = cloud_accounts
        self.status_id = status_id
        self.support_team_name = support_team_name
        self.status_name = status_name
        self.emergency_instructions = emergency_instructions

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        return AccountDetails(
            primary_contact_id=json_dict['primary_contact_id'],
            create_date=json_dict['create_date'],
            cloud_accounts=json_dict['cloud_accounts'],
            status_id=json_dict['status_id'],
            support_team_name=json_dict['support_team_name'],
            status_name=json_dict['status_name'],
            emergency_instructions=
                json_dict['emergency_instructions'])


class Contact(BaseMarshallingDomain):
    def __init__(self, nps_survey, emails, name, phones, contact_id, role_id,
                 individual_primary_id):
        super(Contact, self).__init__()
        self.nps_survey = nps_survey
        self.emails = emails
        self.name = name
        self.phones = phones
        self.contact_id = contact_id
        self.role_id = role_id
        self.individual_primary_id = individual_primary_id

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        ret = []
        if "contacts" in json_dict.keys():
            contacts_list = json_dict.get('contacts')
            for contact in contacts_list:
                contact_obj = Contact(nps_survey=contact['nps_survey'],
                                      emails=contact['emails'],
                                      name=contact['name'],
                                      phones=contact['phones'],
                                      contact_id=contact['contact_id'],
                                      role_id=contact['role_id'],
                                      individual_primary_id=contact[
                                          'individual_primary_id'])
                ret.append(contact_obj)
        else:
            ret.append(Contact(nps_survey=json_dict['nps_survey'],
                               emails=json_dict['emails'],
                               name=json_dict['name'],
                               phones=json_dict['phones'],
                               contact_id=json_dict['contact_id'],
                               role_id=json_dict['role_id'],
                               individual_primary_id=
                               json_dict['individual_primary_id']))
        return ret


class Inventory(BaseMarshallingDomain):
    def __init__(self, site_id, ipv4_gateway, id, parts, os, datacenter,
                 type, status, permissions, name):
        super(Inventory, self).__init__()
        self.site_id = site_id
        self.ipv4_gateway = ipv4_gateway
        self.id = id
        self.parts = parts
        self.os = os
        self.datacenter = datacenter
        self.type = type
        self.status = status
        self.permissions = permissions
        self.name = name

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        ret = []
        if 'inventory' in json_dict.keys():
            for device in json_dict.get('inventory'):
                s = Inventory(site_id=device['site_id'],
                              ipv4_gateway=
                              device['primary_ipv4_gateway'],
                              id=device['id'], parts=device['parts'],
                              os=device['os'],
                              datacenter=device['datacenter'],
                              type=device['type'],
                              status=device['status'],
                              permissions=device['permissions'],
                              name=device['name'])
                ret.append(s)
            return ret
        else:
            return Inventory(site_id=json_dict['site_id'],
                             ipv4_gateway=json_dict['primary_ipv4_gateway'],
                             id=json_dict['id'], parts=json_dict['parts'],
                             os=json_dict['os'],
                             datacenter=json_dict['datacenter'],
                             type=json_dict['type'],
                             status=json_dict['status'],
                             permissions=json_dict['permissions'],
                             name=json_dict['name'])


class Server(BaseMarshallingDomain):
    def __init__(self, site_id, ipv4_gateway, id, parts, os,
                 datacenter, type, status, permissions, name, account_number):
        super(Server, self).__init__()
        self.site_id = site_id
        self.ipv4_gateway = ipv4_gateway
        self.id = id
        self.parts = parts
        self.os = os
        self.datacenter = datacenter
        self.type = type
        self.status = status
        self.permissions = permissions
        self.name = name
        self.account_number = account_number

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        if 'servers' in json_dict.keys():
            ret = []
            for server in json_dict.get('servers'):
                s = Server(site_id=server['site_id'],
                           ipv4_gateway=server['primary_ipv4_gateway'],
                           id=server['id'], parts=server['parts'],
                           os=server['os'],
                           datacenter=server['datacenter'],
                           type=server['type'],
                           status=server['status'],
                           permissions=server['permissions'],
                           name=server['name'],
                           account_number=server['account_number'])
                ret.append(s)
            return ret
        else:
            return Server(site_id=json_dict['site_id'],
                          ipv4_gateway=json_dict['primary_ipv4_gateway'],
                          id=json_dict['id'], parts=json_dict['parts'],
                          os=json_dict['os'],
                          datacenter=json_dict['datacenter'],
                          type=json_dict['type'],
                          status=json_dict['status'],
                          permissions=json_dict['permissions'],
                          name=json_dict['name'],
                          account_number=json_dict['account_number'])


class Network(BaseMarshallingDomain):
    def __init__(self, site_id, ipv4_gateway, id, parts, os, datacenter, type,
                 status, permissions, name, account_number):
        super(Network, self).__init__()
        self.site_id = site_id
        self.ipv4_gateway = ipv4_gateway
        self.id = id
        self.parts = parts
        self.os = os
        self.datacenter = datacenter
        self.type = type
        self.status = status
        self.permissions = permissions
        self.name = name
        self.account_number = account_number

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        if 'network' in json_dict.keys():
            ret = []
            for network in json_dict.get('network'):
                s = Network(site_id=network['site_id'],
                            ipv4_gateway=network['primary_ipv4_gateway'],
                            id=network['id'],
                            parts=network['parts'],
                            os=network['os'],
                            datacenter=network['datacenter'],
                            type=network['type'],
                            status=network['status'],
                            permissions=network['permissions'],
                            name=network['name'],
                            account_number=network['account_number'])
                ret.append(s)
            return ret
        else:
            return Network(site_id=json_dict['site_id'],
                           ipv4_gateway=json_dict['primary_ipv4_gateway'],
                           id=json_dict['id'], parts=json_dict['parts'],
                           os=json_dict['os'],
                           datacenter=json_dict['datacenter'],
                           type=json_dict['type'],
                           status=json_dict['status'],
                           permissions=json_dict['permissions'],
                           name=json_dict['name'],
                           account_number=json_dict['account_number'])


class Service(BaseMarshallingDomain):
    def __init__(self, site_id, ipv4_gateway, id, parts, os, datacenter, type,
                 status, permissions, name, account_number):
        super(Service, self).__init__()
        self.site_id = site_id
        self.ipv4_gateway = ipv4_gateway
        self.id = id
        self.parts = parts
        self.os = os
        self.datacenter = datacenter
        self.type = type
        self.status = status
        self.permissions = permissions
        self.name = name
        self.account_number = account_number

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        if 'services' in json_dict.keys():
            ret = []
            for service in json_dict.get('services'):
                s = Service(site_id=service['site_id'],
                            ipv4_gateway=service['primary_ipv4_gateway'],
                            id=service['id'],
                            parts=service['parts'],
                            os=service['os'],
                            datacenter=service['datacenter'],
                            type=service['type'],
                            status=service['status'],
                            permissions=service['permissions'],
                            name=service['name'],
                            account_number=service['account_number'])
                ret.append(s)
            return ret
        else:
            return Service(site_id=json_dict['site_id'],
                           ipv4_gateway=json_dict['primary_ipv4_gateway'],
                           id=json_dict['id'], parts=json_dict['parts'],
                           os=json_dict['os'],
                           datacenter=json_dict['datacenter'],
                           type=json_dict['type'],
                           status=json_dict['status'],
                           permissions=json_dict['permissions'],
                           name=json_dict['name'],
                           account_number=json_dict['account_number'])


class Storage(BaseMarshallingDomain):
    def __init__(self, site_id, ipv4_gateway, id, parts, os, datacenter, type,
                 status, permissions, name, account_number):
        super(Storage, self).__init__()
        self.site_id = site_id
        self.ipv4_gateway = ipv4_gateway
        self.id = id
        self.parts = parts
        self.os = os
        self.datacenter = datacenter
        self.type = type
        self.status = status
        self.permissions = permissions
        self.name = name
        self.account_number = account_number

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        if 'storage' in json_dict.keys():
            ret = []
            for storage in json_dict.get('storage'):
                s = Storage(site_id=storage['site_id'],
                            ipv4_gateway=storage['primary_ipv4_gateway'],
                            id=storage['id'],
                            parts=storage['parts'],
                            os=storage['os'],
                            datacenter=storage['datacenter'],
                            type=storage['type'],
                            status=storage['status'],
                            permissions=storage['permissions'],
                            name=storage['name'],
                            account_number=storage['account_number'])
                ret.append(s)
            return ret
        else:
            return Storage(site_id=json_dict['site_id'],
                           ipv4_gateway=json_dict['primary_ipv4_gateway'],
                           id=json_dict['id'], parts=json_dict['parts'],
                           os=json_dict['os'],
                           datacenter=json_dict['datacenter'],
                           type=json_dict['type'],
                           status=json_dict['status'],
                           permissions=json_dict['permissions'],
                           name=json_dict['name'],
                           account_number=json_dict['account_number'])


class SupportDevice(BaseMarshallingDomain):
    def __init__(self, site_id, ipv4_gateway, id, parts, os, datacenter, type,
                 status, permissions, name,
                 account_number, platform_model_description):
        super(SupportDevice, self).__init__()
        self.site_id = site_id
        self.ipv4_gateway = ipv4_gateway
        self.id = id
        self.parts = parts
        self.os = os
        self.datacenter = datacenter
        self.type = type
        self.status = status
        self.permissions = permissions
        self.name = name
        self.account_number = account_number

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        if 'support' in json_dict.keys():
            ret = []
            for support in json_dict.get('support'):
                s = SupportDevice(site_id=support['site_id'],
                                  ipv4_gateway=support['primary_ipv4_gateway'],
                                  id=support['id'],
                                  parts=support['parts'],
                                  os=support['os'],
                                  datacenter=support['datacenter'],
                                  type=support['type'],
                                  status=support['status'],
                                  permissions=support['permissions'],
                                  name=support['name'],
                                  account_number=support['account_number'],
                                  platform_model_description=support[
                                      'platform_model_description'])
                ret.append(s)
            return ret
        else:
            return SupportDevice(site_id=json_dict['site_id'],
                                 ipv4_gateway=json_dict[
                                     'primary_ipv4_gateway'],
                                 id=json_dict['id'],
                                 parts=json_dict['parts'],
                                 os=json_dict['os'],
                                 datacenter=json_dict['datacenter'],
                                 type=json_dict['type'],
                                 status=json_dict['status'],
                                 permissions=json_dict['permissions'],
                                 name=json_dict['name'],
                                 account_number=json_dict['account_number'],
                                 platform_model_description=json_dict[
                                     'platform_model_description'])


class Device(BaseMarshallingDomain):
    def __init__(self, site_id, primary_username, child_devices, primary_ip,
                 admin_password, datacenter, account_number, name):
        super(Device, self).__init__()
        self.site_id = site_id
        self.primary_username = primary_username
        self.child_devices = child_devices
        self.primary_ip = primary_ip
        self.admin_password = admin_password
        self.datacenter = datacenter
        self.account_number = account_number
        self.name = name

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        return Device(json_dict['site_id'], json_dict['primary_username'],
                      json_dict['child_devices'], json_dict['primary_ip'],
                      json_dict['admin_password'], json_dict['datacenter'],
                      json_dict['account_number'], json_dict['name'])


class Tickets(BaseMarshallingDomain):
    def __init__(self, status, description, created, modified, devices,
                 ticket_number, is_solved, is_closed, subject):
        self.status = status
        self.description = description
        self.created = created
        self.modified = modified
        self.devices = devices
        self.ticket_number = ticket_number
        self.is_solved = is_solved
        self.is_closed = is_closed
        self.subject = subject

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        if 'tickets' in json_dict.keys():
            ret = []
            for ticket in json_dict.get('tickets'):
                s = Tickets(status=ticket['status'],
                            description=ticket['description'],
                            created=ticket['created'],
                            modified=ticket['modified'],
                            devices=ticket['devices'],
                            ticket_number=ticket['ticket_number'],
                            is_closed=ticket['is_closed'],
                            is_solved=ticket['is_solved'],
                            subject=ticket['subject'])
                ret.append(s)
            return ret


class TicketStatus(BaseMarshallingDomain):
    def __init__(self, is_terminal, description, is_new, is_solved, id,
                 is_closed, name):
        self.is_terminal = is_terminal
        self.description = description
        self.is_new = is_new
        self.is_solved = is_solved
        self.id = id
        self.is_closed = is_closed
        self.name = name


class TicketRecipient(BaseMarshallingDomain):
    def __init__(self, is_employee, employee_userid, contact_id, role_id,
                 role_name, contact_name):
        self.is_employee = is_employee
        self.employee_userid = employee_userid
        self.contact_id = contact_id
        self.role_id = role_id
        self.role_name = role_name
        self.contact_name = contact_name

    @classmethod
    def _json_to_obj(cls, serialized_str):
        recipients = []
        json_dict = json.loads(serialized_str)
        for recipient in json_dict:
            ticket_recipient = TicketRecipient(recipient['is_employee'],
                                               recipient['employee_userid'],
                                               recipient['contact_id'],
                                               recipient['role_id'],
                                               recipient['role_name'],
                                               recipient['contact_name'])
            recipients.append(ticket_recipient)
        return recipients


class TicketMessage(BaseMarshallingDomain):
    def __init__(self, source_contact, privatizer, recipients, is_customer,
                 text, attachments, source, private, ticket_number, id,
                 account_number):
        self.source_contact = source_contact
        self.privatizer = privatizer
        self.recipients = recipients
        self.is_customer = is_customer
        self.text = text
        self.attachments = attachments
        self.source = source
        self.private = private
        self.ticket_number = ticket_number
        self.id = id
        self.account_number = account_number

    @classmethod
    def _json_to_obj(cls, serialized_str):
        ticket_messages = []
        json_dict = json.loads(serialized_str)
        if "ticket_messages" in json_dict.keys():
            for message in json_dict['ticket_messages']:
                message = TicketMessage(
                    message['source_contact'], message['privatizer'],
                    message['recipients'], message['is_customer'],
                    message['text'], message['attachments'], message['source'],
                    message['private'], message['ticket_number'],
                    message['id'],
                    message['account_number'])
                ticket_messages.append(message)
        return ticket_messages


class Ticket(BaseMarshallingDomain):
    def __init__(self, status, has_open_subtickets, subcategory,
                 classification, recipients, number, private, is_closeable,
                 subtickets, category, severity, created, messages, modified,
                 devices, queue, account_number, subject):
        self.status = status
        self.has_open_subtickets = has_open_subtickets
        self.subcategory = subcategory
        self.classification = classification
        self.recipients = recipients
        self.number = number
        self.private = private
        self.is_closeable = is_closeable
        self.subtickets = subtickets
        self.category = category
        self.severity = severity
        self.created = created
        self.messages = messages
        self.modified = modified
        self.devices = devices
        self.queue = queue
        self.account_number = account_number
        self.subject = subject

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        recipients = []
        messages = []
        if "status" in json_dict.keys():
            status = TicketStatus(json_dict['status']['is_terminal'],
                                  json_dict['status']['description'],
                                  json_dict['status']['is_new'],
                                  json_dict['status']['is_solved'],
                                  json_dict['status']['id'],
                                  json_dict['status']['is_closed'],
                                  json_dict['status']['name'])

        if "recipients" in json_dict.keys():
            if (len(json_dict.get('recipients')) > 0):
                for recipient in json_dict.get('recipients'):
                    ticket_recipient = TicketRecipient(
                        recipient['is_employee'],
                        recipient['employee_userid'],
                        recipient['contact_id'],
                        recipient['role_id'],
                        recipient['role_name'],
                        recipient['contact_name'])
                    recipients.append(ticket_recipient)

        if "messages" in json_dict.keys():
            if (len(json_dict.get('messages')) > 0):
                for message in json_dict.get('messages'):
                    ticket_message = TicketMessage(
                        message['source_contact'], message['privatizer'],
                        message['recipients'], message['is_customer'],
                        message['text'], message['attachments'],
                        message['source'], message['private'],
                        message['ticket_number'], message['id'],
                        message['account_number'])
                    messages.append(ticket_message)

        return Ticket(status, json_dict.get('has_open_subtickets'),
                      json_dict.get('subcategory'),
                      json_dict.get('classification'), recipients,
                      json_dict.get('number'),
                      json_dict.get('private'),
                      json_dict.get('is_closeable'),
                      json_dict.get('subtickets'),
                      json_dict.get('category'),
                      json_dict.get('severity'),
                      json_dict.get('created'),
                      messages,
                      json_dict.get('modified'),
                      json_dict.get('devices'),
                      json_dict.get('queue'),
                      json_dict.get('account_number'),
                      json_dict.get('subject'))


class File(BaseMarshallingDomain):
    def __init__(self, name, links, bytes, last_modified, file_id,
                 content_type, device_id):
        self.name = name
        self.links = links
        self.bytes = bytes
        self.last_modified = last_modified
        self.file_id = file_id
        self.content_type = content_type
        self.device_id = device_id

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        if "files" in json_dict.keys():
            ret = []
            for file in json_dict.get("files"):
                s = File(name=file['name'], links=file['links'],
                         bytes=file['bytes'],
                         last_modified=file['last_modified'],
                         file_id=file['file_id'],
                         content_type=file['content_type'],
                         device_id=file['device_id'])
                ret.append(s)
            return ret
        else:
            return File(name=json_dict['name'], links=json_dict['links'],
                        bytes=json_dict['bytes'],
                        last_modified=json_dict['last_modified'],
                        file_id=json_dict['file_id'],
                        content_type=json_dict['content_type'],
                        device_id=json_dict['device_id'])


class Permission(BaseMarshallingDomain):
    def __init__(self, item_type_id, permission_type_id, item_type_name,
                 contact_id, account_number, permission_name, item_id, id):
        self.item_type_id = item_type_id
        self.permission_type_id = permission_type_id
        self.item_type_name = item_type_name
        self.contact_id = contact_id
        self.account_number = account_number
        self.permission_name = permission_name
        self.item_id = item_id
        self.id = id

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        if "permissions" in json_dict.keys():
            ret = []
            for permission in json_dict.get("permissions"):
                s = Permission(item_type_id=permission['item_type_id'],
                               permission_type_id=permission[
                                   'permission_type_id'],
                               item_type_name=permission['item_type_name'],
                               contact_id=permission['contact_id'],
                               account_number=permission['account_number'],
                               permission_name=permission['permission_name'],
                               item_id=permission['item_id'],
                               id=permission['id'])
                ret.append(s)
            return ret
        else:
            return Permission(item_type_id=json_dict['item_type_id'],
                              permission_type_id=json_dict[
                                  'permission_type_id'],
                              item_type_name=json_dict['item_type_name'],
                              contact_id=json_dict['contact_id'],
                              account_number=json_dict['account_number'],
                              permission_name=json_dict['permission_name'],
                              item_id=json_dict['item_id'], id=json_dict['id'])


class Password(BaseMarshallingDomain):
    def __init__(self, password, event, id, is_current, rotation_is_scheduled,
                 time_stamp):
        self.admin_password = password
        self.event = event
        self.id = id
        self.is_current = is_current
        self.rotation_is_scheduled = rotation_is_scheduled
        self.time_stamp = time_stamp

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        if "admin_passwords" in json_dict.keys():
            ret = []
            for password in json_dict.get("admin_passwords"):
                s = Password(password['admin_password'],
                             password['event'],
                             password['id'],
                             password['is_current'],
                             password['rotation_is_scheduled'],
                             password['timestamp'])
                ret.append(s)
            return ret
        else:
            return Password(password=json_dict['admin_password'],
                            event=json_dict['event'],
                            is_current=json_dict['is_current'],
                            rotation_is_scheduled=json_dict[
                                'rotation_is_scheduled'],
                            time_stamp=json_dict['time_stamp'])


class CloudAccount(BaseMarshallingDomain):
    def __init__(self, name, cloud_account_number, manager, team,
                 has_rack_connect,
                 has_consolidated_invoicing):
        self.name = name
        self.cloud_account_number = cloud_account_number
        self.manager = manager
        self.team = team
        self.has_rack_connect = has_rack_connect
        self.has_consolidated_invoicing = has_consolidated_invoicing

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        return CloudAccount(json_dict['name'],
                            json_dict['cloud_account_number'],
                            json_dict['manager'],
                            json_dict['team'],
                            json_dict['has_rack_connect'],
                            json_dict['has_consolidated_invoicing'])

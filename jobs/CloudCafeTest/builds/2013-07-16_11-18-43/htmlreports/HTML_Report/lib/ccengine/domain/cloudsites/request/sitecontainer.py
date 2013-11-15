from ccengine.domain.base_domain import BaseMarshallingDomain
import json
import xml.etree.ElementTree as ET


class SiteContainer(BaseMarshallingDomain):

    def __init__(self, site=None, database=None, application=None):
        self.site = site
        self.database = database
        self.application = application

    def _obj_to_json(self):
        ret = {'siteContainer': {'site': self.site._obj_to_json(),
                           'database': self.database._obj_to_json(),
                           'application': self.application._obj_to_json()}}
        ret = json.dumps(ret)
        return ret

    def _obj_to_xml(self):
        element = ET.Element('siteContainer')
        site_ele = ET.Element('site')
        db_ele = ET.Element('database')
        app_ele = ET.Element('application')
        if self.site is not None:
            site_ele.text = self.site
        if self.database is not None:
            db_ele.text = self.datbase
        if self.application is not None:
            app_ele.text = self.application
        element.append(site_ele)
        element.append(db_ele)
        element.append(app_ele)
        ret = ET.tostring(element)
        return ret


class Site(BaseMarshallingDomain):

    def __init__(self, fqdn, clientId=None, legacySiteId=None,
                 legacyEmail=None):
        self.fqdn = fqdn
        self.clientId = clientId
        self.legacySiteId = legacySiteId
        self.legacyEmail = legacyEmail

    def _obj_to_json(self):
        ret = {'site': {'fqdn': self.fqdn,
                           'clientId': self.clientId,
                           'legacySiteId': self.legacySiteId,
                           'legacyEmail': self.legacyEmail}}
        return ret

    def _obj_to_xml(self):
        element = ET.Element('site')
        fqdn_ele = ET.Element('fqdn')
        client_ele = ET.Element('clientId')
        ls_ele = ET.Element('legacySiteId')
        le_ele = ET.Element('legacayEmail')
        if self.clientId is not None:
            client_ele.text = self.clientId
        if self.legacySiteId is not None:
            ls_ele.text = self.legacySiteId
        if self.legacyEmail is not None:
            le_ele.text = self.legacyEmail
        fqdn_ele.text = self.fqdn
        element.append(fqdn_ele)
        element.append(client_ele)
        element.append(ls_ele)
        element.append(le_ele)
        return element


class Database(BaseMarshallingDomain):

    def __init__(self, name, user, password):
        self.name = name
        self.user = user
        self.password = password

    def _obj_to_json(self):
        ret = {'database': {'name': self.name,
                           'user': self.user,
                           'password': self.password}}
        return ret

    def _obj_to_xml(self):
        element = ET.Element('database')
        name_ele = ET.Element('name')
        user_ele = ET.Element('user')
        pass_ele = ET.Element('password')
        name_ele.text = self.name
        user_ele.text = self.user
        pass_ele.text = self.password
        element.append(name_ele)
        element.append(user_ele)
        element.append(pass_ele)
        return element


class Application(BaseMarshallingDomain):

    def __init__(self, type, title, username, emailAddress, password):
        self.type = type
        self.title = title
        self.username = username
        self.emailAddress = emailAddress
        self.password = password

    def _obj_to_json(self):
        ret = {'application': {'type': self.type,
                           'title': self.title,
                           'username': self.username,
                           'emailAddress': self.emailAddress,
                           'password': self.password}}
        return ret

    def _obj_to_xml(self):
        element = ET.Element('application')
        type_ele = ET.Element('type')
        title_ele = ET.Element('title')
        user_ele = ET.Element('username')
        email_ele = ET.Element('emailAddress')
        pass_ele = ET.Element('password')
        type_ele.text = self.type
        title_ele.text = self.title
        user_ele.text = self.username
        email_ele.text = self.emailAddress
        pass_ele.text = self.password
        element.append(type_ele)
        element.append(title_ele)
        element.append(user_ele)
        element.append(email_ele)
        element.append(pass_ele)
        return element

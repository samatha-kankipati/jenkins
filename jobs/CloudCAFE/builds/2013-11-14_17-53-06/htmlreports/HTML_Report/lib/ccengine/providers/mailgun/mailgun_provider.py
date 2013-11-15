from ccengine.clients.mailgun.mailgun_api import MailgunClient
from ccengine.providers.base_provider import BaseProvider


class MailgunProvider(BaseProvider):

    def __init__(self, config, logger=None):
        """
        Sets up client based on parameters taken from config
        @todo: add support for files=MultiDict
        """
        super(MailgunProvider, self).__init__()
        self.config = config
        base_url = self.config.mailgun.api_url
        domain = self.config.mailgun.domain_name
        url = "{base_url}/{domain}".format(base_url=base_url,
                                           domain=domain)
        api_key = self.config.mailgun.api_key
        self.mailgun_client = MailgunClient(url=url,
                                            api_key=api_key)

    def send_simple_message(self, from_user, to, cc=None, bcc=None,
                            subject=None, text=None, html=None):
        """
        Sends a plain text/html message
        """
        resp = self.mailgun_client.send_message(from_user=from_user,
                                                to=to, cc=cc, bcc=bcc,
                                                subject=subject,
                                                text=text,
                                                html=html)
        assert resp.status_code == 200, \
            ('Unexpected send message response with status code '
             '{0}, reason: {1}, content: {2}.'.format(
                resp.status_code, resp.reason, resp.content))
        return resp.entity

    def send_scheduled_message(self, from_user, to, o_deliverytime,
                               cc=None, bcc=None, subject=None, text=None,
                               html=None):
        """
        Sends a plain text/html message with a delivery time set
        """
        resp = self.mailgun_client.send_message(from_user=from_user,
                                                to=to,
                                                o_deliverytime=o_deliverytime,
                                                cc=cc, bcc=bcc,
                                                subject=subject,
                                                text=text,
                                                html=html)
        assert resp.status_code == 200, \
            ('Unexpected send message response with status code '
             '{0}, reason: {1}, content: {2}.'.format(
                resp.status_code, resp.reason, resp.content))
        return resp.entity

    def send_attachment_message(self, from_user, to, attachment, cc=None,
                                bcc=None, subject=None, text=None, html=None):
        """
        Sends a message with attachments
        """
        resp = self.mailgun_client.send_message(from_user=from_user,
                                                to=to, attachment=attachment,
                                                cc=cc, bcc=bcc,
                                                subject=subject,
                                                text=text,
                                                html=html)
        assert resp.status_code == 200, \
            ('Unexpected send message response with status code '
             '{0}, reason: {1}, content: {2}.'.format(
                resp.status_code, resp.reason, resp.content))
        return resp.entity

    def send_inline_image_message(self, from_user, to, inline, html, cc=None,
                                  bcc=None, subject=None, text=None):
        """
        Sends a message with an inline image
        Mailgun assigns content-id to each image passed via inline API
        parameter, so it can be referenced in HTML part.
        e.g.
        inline (fileloc) is "files/test.jpg"
        "html": '<html>Inline image here: <img src="cid:test.jpg"></html>'
        """
        resp = self.mailgun_client.send_message(from_user=from_user,
                                                to=to, inline=inline,
                                                cc=cc, bcc=bcc,
                                                subject=subject,
                                                text=text,
                                                html=html)
        assert resp.status_code == 200, \
            ('Unexpected send message response with status code '
             '{0}, reason: {1}, content: {2}.'.format(
                resp.status_code, resp.reason, resp.content))
        return resp.entity

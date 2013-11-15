from ccengine.domain.mailgun.response.message_response import MailgunEntity
from ccengine.domain.mailgun.request.message_request import SendMessageItem
from ccengine.clients.base_client import BaseMarshallingClient


class MailgunClient(BaseMarshallingClient):

    def __init__(self, url, api_key,
                 serialize_format='dict', deserialize_format='json'):
        super(MailgunClient, self).__init__(
            serialize_format, deserialize_format)
        self.url = url
        # Mailgun requires content-type headers to be x-www-form-urlencoded
        # This requires a serialization type of dict (not json)
        ct = '{content_type}/{content_subtype}'.format(
            content_type='application',
            content_subtype='x-www-form-urlencoded')
        accept = '{content_type}/{content_subtype}'.format(
            content_type='application',
            content_subtype=self.deserialize_format)
        self.default_headers['Content-Type'] = ct
        self.default_headers['Accept'] = accept
        self.auth = ('api', api_key)

    def send_message(self, from_user, to, cc=None, bcc=None, subject=None,
                     text=None, html=None, attachment=None, inline=None,
                     o_tag=None, o_campaign=None, o_dkim=None,
                     o_deliverytime=None, o_testmode=None, o_tracking=None,
                     o_tracking_clicks=None, o_tracking_opens=None,
                     h_x_my_header=None, v_my_var=None,
                     requestslib_kwargs=None):
        """
        @summary: Sends an email
        @param from_user: Email address for From header
        @param to: Email address of the recipient(s).
            Example: "Bob <bob@host.com>". You can use commas to separate
            multiple recipients.
        @type to:  string
        @param cc: Same as To but for Cc
        @type cc:  string
        @param bcc: Same as To but for Bcc
        @type bcc:  string
        @param subject: Message subject
        @type subject:  string
        @param text: Body of the message. (text version)
        @type text:  string
        @param html: Body of the message. (HTML version)
        @type html:  string
        @param attachment: File attachment. You can post multiple attachment
            values. Important: You must use multipart/form-data encoding when
            sending attachments.
        @type attachment:  string
        @param inline: Attachment with inline disposition. Can be used to
            send inline images. You can post multiple inline values.
        @type inline:  string
        @param o_tag: Tag string.
        @type o_tag:  string
        @param o_campaign: Id of the campaign the message belongs to.
        @type o_campaign:  string
        @param o_dkim: Enables/disables DKIM signatures on per-message basis.
            Pass yes or no
        @type o_dkim:  string
        @param o_deliverytime: Desired time of delivery.
        @type o_deliverytime:  string
        @param o_testmode: Enables sending in test mode. Pass yes if needed.
        @type o_testmode:  string
        @param o_tracking: Toggles tracking on a per-message basis.
            Pass yes or no.
        @type o_tracking:  string
        @param o_tracking_clicks: Toggles clicks tracking on a per-message
            basis. Has higher priority than domain-level setting.
            Pass yes, no or htmlonly.
        @type o_tracking_clicks:  string
        @param o_tracking_opens: Toggles opens tracking on a per-message
            basis. Has higher priority than domain-level setting.
            Pass yes or no.
        @type o_tracking_opens:  string
        @param h_x_my_header: h: prefix followed by an arbitrary value allows
            to append a custom MIME header to the message (X-My-Header in
            this case). For example, h:Reply-To to specify Reply-To address.
        @type h_x_my_header:  string
        @param v_my_var: v: prefix followed by an arbitrary name allows to
            attach a custom JSON data to the message.
        @type v_my_var:  string
        @return: Status message on outcome of request
        @rtype:  Response Object
        @notes: http://documentation.mailgun.com/api-sending.html
        """
        """
            POST
            v2/{domain_name}/messages
            e.g., "https://api.mailgun.net/v2/computeqe1.mailgun.org/messages"
        """
        url = '{base_url}/messages'.format(base_url=self.url)
        requestslib_kwargs = {'auth': self.auth}
        send_message_request_object = SendMessageItem(
            from_user=from_user, to=to, cc=cc, bcc=bcc, subject=subject,
            text=text, html=html, attachment=attachment, inline=inline,
            o_tag=o_tag, o_campaign=o_campaign, o_dkim=o_dkim,
            o_deliverytime=o_deliverytime, o_testmode=o_testmode,
            o_tracking=o_tracking, o_tracking_clicks=o_tracking_clicks,
            o_tracking_opens=o_tracking_opens, h_x_my_header=h_x_my_header,
            v_my_var=v_my_var)
        send_message_response = self.request(
            'POST', url,
            response_entity_type=MailgunEntity,
            request_entity=send_message_request_object,
            requestslib_kwargs=requestslib_kwargs)
        return send_message_response

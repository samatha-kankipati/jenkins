'''
@summary: Provider Module for the Compute Volume API
@note: Should be the primary interface to a test case or external tool.
@copyright: Copyright (c) 2012 Rackspace US, Inc.
'''
from time import time, sleep

from ccengine.clients.compute.volume_attachments_api import\
    VolumeAttachmentsAPIClient

from ccengine.providers.identity.v2_0.identity_api import IdentityAPIProvider

from ccengine.providers.base_provider import\
    BaseProvider as _BaseProvider, \
    ProviderActionResult as _ProviderActionResult


class VolumeAttachmentsAPIProvider(_BaseProvider):
    def __init__(self, config):
        super(VolumeAttachmentsAPIProvider, self).__init__()
        self.config = config

        #Get Identity info
        self.identity_provider = IdentityAPIProvider(self.config)
        resp = self.identity_provider.authenticate()
        self.auth_data = resp.entity
        self.auth_token = self.auth_data.token.id

        volume_attachments_service = self.auth_data.serviceCatalog.get_service(
            self.config.volume_attachments_api.identity_service_name)

        self.volume_attachments_region = (
            self.config.volume_attachments_api.region)

        self.volume_attachments_url = volume_attachments_service.get_endpoint(
            self.volume_attachments_region).publicURL

        self.tenant_id = volume_attachments_service.get_endpoint(
            self.volume_attachments_region).tenantId

        self.volume_attachments_api_client = VolumeAttachmentsAPIClient(
            self.volume_attachments_url, self.auth_token, self.tenant_id,
            self.config.misc.serializer, self.config.misc.deserializer)

        #Backward compatability for older tests
        self.client = self.volume_attachments_api_client

    def wait_for_volume_attachment_to_propagate(
            self, attachment_id, server_id, timeout=60, wait_period=5):

        endtime = time() + int(timeout)
        while time() < endtime:

            resp = self.client.get_volume_attachment_details(
                attachment_id, server_id)

            if resp.ok:
                return True

            sleep(wait_period)
        else:
            return False

    def detach_volume_confirmed(
            self, attachment_id, server_id, timeout=320, wait_period=10):
        """
        Wait for 404 return code.
        NOTE:  The hypervisor won't accept a delete request against a volume
        attachment until the volume is no longer in use by the file system.
        Since there's no way to ask the api if the volume is still in use
        or not, the only way to guarantee a delete is to spam deletes
        until you get a 2XX response.  (If you're nice, you'll stop spamming
        at this point and poll the attachment info until you get a 404,)
        You could also wait for the volume's status to change to
        available, but that's outside the scope of this provider.
        """
        self.provider_log.info(
            "Detaching volume and confirming attachment delete")
        provider_response = _ProviderActionResult()
        time_waited = 0

        #Spam deletes until the delete is acknowledged
        attached = True
        self.provider_log.info(
            "Spamming deletes until a positive response or a 404 is recieved.")
        while attached:
            attachment_del_resp = self.client.delete_volume_attachment(
                attachment_id, server_id)
            provider_response.response = attachment_del_resp

            if attachment_del_resp.status_code == 404:
                self.provider_log.info(
                    "Attachment delete verified, 404 recieved")
                provider_response.ok = True
                return provider_response

            elif attachment_del_resp.ok:
                self.provider_log.info(
                    "Positive response received - Attachment delete accpeted."
                    " Waiting for confirmation")
                attached = False

            elif (attachment_del_resp.status_code != 404) and (
                not attachment_del_resp.ok):
                self.provider_log.info(
                    "Volume attachment delete request refused, spamming "
                    "deletes...")
            else:
                self.provider_log.info(
                    "An unexpected status code was retruned while trying to "
                    "delete the volume attachment: {0}".format(
                        attachment_del_resp.status_code))
                break

            if time_waited >= timeout:
                self.provider_log.info(
                    "Delete timed out. Last response to a delete was"
                    " {0}".format(attachment_del_resp.status_code))
                provider_response.ok = False
                return provider_response

            sleep(wait_period)
            time_waited += wait_period

        #Only gets here if it got a 2XX response in the previous loop.
        #This spams info requests until the api says the attachment is gone
        #(404)
        self.provider_log.info(
            "Checking volume attachment status until 404 is recieved to "
            "confirm delete.")

        while True:
            attachment_info_resp = self.client.get_volume_attachment_details(
                attachment_id, server_id)
            provider_response.response = attachment_info_resp

            if attachment_info_resp.status_code == 404:
                self.provider_log.info(
                    "Attachment delete verified, 404 recieved")
                provider_response.ok = True
                return provider_response

            elif (attachment_info_resp.status_code != 404) and (
                    not attachment_info_resp.ok):
                self.provider_log.info(
                    "Unexpected status code recieved while waiting for 404 "
                    "from GET on volume attachment.  Unable to verify that "
                    "volume is detached from server")
                provider_response.ok = False
                return provider_response

            elif attachment_info_resp.ok:
                self.provider_log.info(
                    "Volume attachment still exists, waiting for delete to"
                    " finish.")

            if time_waited >= timeout:
                self.provider_log.error(
                    "Delete confirmation timed out. Last response to an info"
                    " request was {0}".format(
                        attachment_info_resp.status_code))
                provider_response.ok = False
                return provider_response

            sleep(wait_period)
            time_waited += wait_period

        return provider_response

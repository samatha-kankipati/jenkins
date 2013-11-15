import subprocess
import re
from ccengine.common.constants.compute_constants import Constants


class PingException(Exception):
    pass


class PingClient(object):
    """
    @summary: Client to ping windows or linux servers
    """
    @classmethod
    def ping(cls, ip, ip_address_version_for_ssh=4, count=3):
        """
        @summary: Ping a server with an IP
        @param ip: IP address to ping
        @type ip: string
        @param ip_address_version_for_ssh: IP version 4 or 6
        @type: int (default 4)
        @param count: Packets to transmit
        @type: int (default 3)
        @return: packet loss percent or None if not found in the ping response
        @rtype: int or None
        """
        '''
        Porting only Linux OS
        '''
        ping_command = Constants.PING_IPV6_COMMAND_LINUX \
            if ip_address_version_for_ssh == 6 \
                else Constants.PING_IPV4_COMMAND_LINUX

        # packet count value of 3 comes with the constants
        if count != 3:
            ping_items = ping_command.split(' ')[:2]
            ping_items.append(count)
            ping_command = '{0} {1} {2} '.format(*ping_items)
        command = ping_command + ip
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        out, error = process.communicate()

        try:
            packet_loss_percent = re.search(Constants.PING_PACKET_LOSS_REGEX,
                                            out).group(1)
        except:
            # If there is no match, raise an exception
            msg = 'Failed to ping IP {0}. ERROR: {1}'.format(ip, error)
            raise PingException(msg)
        return int(packet_loss_percent)

    @classmethod
    def ping_using_remote_machine(cls, remote_client, ping_ip_address,
                                  count=3):
        """
        @summary: Ping a server using a remote machine
        @param remote_client: Remote machine client
        @type: ccengine.common.connectors.ssh.SSHConnector or
               ccengine.common.tools.wmi_helper.WmiHelper instance
        @param ip: IP address to ping
        @type ip: string
        @param count: Packets to transmit
        @type: int (default 3)
        @return: packet loss percent or None if not found in the ping response
        @rtype: int or None
        """
        command = Constants.PING_IPV4_COMMAND_LINUX

        # packet count value of 3 comes with the constants
        if count != 3:
            ping_items = command.split(' ')[:2]
            ping_items.append(count)
            command = '{0} {1} {2} '.format(*ping_items)
        ping_response = remote_client.exec_command(command + ping_ip_address)

        try:
            packet_loss_percent = re.search(Constants.PING_PACKET_LOSS_REGEX,
                                            ping_response).group(1)
        except:
            if hasattr(remote_client, 'host'):
                client_ip = getattr(remote_client, 'host')
            elif hasattr(remote_client, 'ip'):
                client_ip = getattr(remote_client, 'ip')
            else:
                client_ip = ''
            msg = 'Failed to ping IP {0} from remote server {1}'.format(
                ping_ip_address, client_ip)
            raise PingException(msg)
        return int(packet_loss_percent)

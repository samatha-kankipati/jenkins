import subprocess
import re
from ccengine.common.constants.compute_constants import Constants

class PingClient(object):
    """
    @summary: Client to ping windows or linux servers 
    """
    @classmethod
    def ping(cls, ip, ip_address_version_for_ssh):
        """
        @summary: Ping a server with a IP
        @param ip: IP address to ping
        @type ip: string
        @return: True if the server was reachable, False otherwise
        @rtype: bool
        """
        '''
        Porting only Linux OS
        '''
        ping_command = Constants.PING_IPV6_COMMAND_LINUX if ip_address_version_for_ssh == 6 else Constants.PING_IPV4_COMMAND_LINUX
        command = ping_command + ip
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        process.wait()
        try:
            packet_loss_percent = re.search(Constants.PING_PACKET_LOSS_REGEX,
                                    process.stdout.read()).group(1)
        except:
            # If there is no match, fail
            return False
        return packet_loss_percent != '100'

    @classmethod
    def ping_using_remote_machine(cls, remote_client, ping_ip_address):
        """
        @summary: Ping a server using a remote machine
        @param remote_client: Client to remote machine
        @param ip: IP address to ping
        @type ip: string
        @return: True if the server was reachable, False otherwise
        @rtype: bool
        """
        command = Constants.PING_IPV4_COMMAND_LINUX
        ping_response = remote_client.exec_command(command + ping_ip_address)
        packet_loss_percent = re.search(Constants.PING_PACKET_LOSS_REGEX, ping_response).group(1)
        return packet_loss_percent != '100'

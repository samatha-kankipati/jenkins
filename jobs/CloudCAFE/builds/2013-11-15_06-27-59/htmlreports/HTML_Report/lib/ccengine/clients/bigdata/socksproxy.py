from ccengine.domain.compute.novashell import SEPARATOR, NovaShellResponse
from ccengine.common.connectors.commandline import CommandLineConnector, CommandLineResponse


class SocksProxyClient(CommandLineConnector):
    '''
    This class starts and stops the socks proxy client with the
    given credentials. It automatically adds the host proxy to the known hosts
    and removes it from the known hosts once done.
    
    @proxy_host IP for the proxy
    @username   assumes user has ssh access to the proxy host.
                @@@Password support not yet implemented@@@.
    @proxy_port defaulted to 4000    
    '''
    
    def __init__(self, proxy_host, username, id_file, proxy_port=4000):
        super(SocksProxyClient, self).__init__("")
        self.proxy_host = proxy_host
        self.username = username
        self.proxy_port = proxy_port
        self.os_response = None
        self.id_file=id_file
        
    def start_socks_proxy(self):
        '''
        Adds the proxy host to known hosts and then starts a socks proxy
        '''
        socks_string = "ssh -N -D {0} -o StrictHostKeyChecking=no {1}@{2}"\
                       " -i {3}".format(
            str(self.proxy_port),
            self.username,
            self.proxy_host,
            self.id_file
            )
        self.os_response = self.__send__(
            socks_string,wait_for_process_to_be_complete=False)
        if len(self.os_response.StandardError) != 0:
            return False
        if len(self.os_response.StandardOut) != 0:
            return False
        if self.os_response.process_id is None:
            return False
        return True
        
    def end_socks_proxy(self):
        '''
        Kills the socks proxy and removes it from the known hosts.
        '''
        self.__send__("kill -9 {0}".format(self.os_response.process_id))
        self.__send__("ssh-keygen -R '{0}'".format(self.proxy_host))
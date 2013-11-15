"""
traffic_gen.py
(C) 2013 - Rackspace Hosting, Inc.
Author: Christopher Hunt

Purpose: To use external mechanisms to generate traffic.
    Currently defined mechanisms: wget, socket

    To add additional mechanisms, need to create:
        _parse_{mechanism}_output
        _build_{mechanism}_cmd

"""
import re


class TrafficGen(object):
    """
    Simplify the use of external mechanisms to generate traffic.
        Currently defined mechanisms: wget, socket
    """
    def __init__(self, destination, resource=None, user=None, pswd=None,
                 protocol='FTP', timeout=5, retries=3,
                 connection_method='wget', connection_exe='wget'):
        self.destination = destination
        self.user = user
        self.password = pswd
        self.protocol = protocol
        self.conn_method = connection_method.lower()
        self.conn_exe = connection_exe
        self.resource = resource
        self.last_cmd = ''
        self.timeout = timeout
        self.retries = retries

    def __str__(self):
        return self.build_cmd()

    @property
    def cmd(self):
        """
        Builds the external command based on set attributes
        @return: (String) - The executable's command line
        """
        return self.build_cmd()

    def build_cmd(self, resource=None, options=''):
        """
        Builds the command, based on the executable attribute.
        @param resource: URL or file to GET
        @param options: Any additional options for the external mechanism
        @return: (String) - The executable's command line
        """
        fn_name = '_build_{exe}_cmd'.format(exe=self.conn_method)
        return getattr(self, fn_name)(resource=resource, options=options)

    def parse_output(self, output):
        """
        Parses the output using the external mechanism's specific parsing
        implementation
        @param output: (string) - Output from execution of external command
        @return: Tuple of (bytes tx, bytes rx)
        """
        fn_name = '_parse_{exe}_output'.format(exe=self.conn_method)
        return getattr(self, fn_name)(output=output)

    def _parse_socket_output(self, output):
        """
        Parses output from socket_traffic.py (or a string '<rx>:<tx>')
        @param output: String output from external output
        @return: Tuple of (bytes tx, bytes rx)
        """
        tx_bytes = rx_bytes = 0

        # Sample text for pattern:
        # 29:1048892
        sock_pattern = re.compile(r'(?P<rx>\d+):(?P<tx>\d+)[\s\n]*')

        match = sock_pattern.search(output)
        if match is not None:
            tx_bytes = int(match.group('rx'))
            rx_bytes = int(match.group('tx'))
        return tx_bytes, rx_bytes

    def _parse_wget_output(self, output):
        """
        Parse output from wget
        @param output: String output from external output
        @return: Tuple of (bytes tx, bytes rx)
        """
        # Not Implemented
        return NotImplemented

    def _build_socket_cmd(self, resource=None, options=None):
        """
        Builds the command line for socket_traffic.py
        @param resource: URL to retrieve
        @param options: Any additional options to be specified
        @return: (String) The executable's command line
        """
        resource = resource or self.resource

        # FTP is not supported for sockets
        if self.protocol.lower() == 'ftp':
            return None

        # Construct the command line
        cmd_format = '{executable} --address {address} --url {resource}'
        if self.protocol.lower() == 'https':
            cmd_format += ' --ssl'
        if options is not None:
            cmd_format += ' {options}'.format(options=options)

        self.last_cmd = cmd_format.format(executable=self.conn_exe,
                                          address=self.destination,
                                          resource=resource)
        return self.last_cmd

    def _build_wget_cmd(self, resource=None, options=''):
        """
        Build the command line for wget
        @param resource: URL or file to retrieve
        @param options: Any additional options for wget
        @return: (String) wget's command line
        """
        authentication = ''
        resource = resource or self.resource
        protocol = self.protocol.lower()

        # Add option to:
        # -r: store response in host-directory ./<svr_ip_addr>/file
        # -q: quiet (output contains control chars which can crash
        #      SSH connection)
        if protocol in ['ftp', 'http']:
            if options == '':
                options = '-rq'
            elif options.find('r') == -1:
                options = options.replace('-', '-rq')

            # Add timeout and retry options
            options += ' --timeout {timeout}'.format(timeout=self.timeout)
            options += ' --tries {retries}'.format(retries=self.retries)

        # For FTP, add authentication
        if protocol == 'ftp':
            if self.user is not None and self.password is not None:
                auth_tags = '--user={user} --password={pswd}'
                authentication = auth_tags.format(user=self.user,
                                                  pswd=self.password)

        # Build command line
        cmd_format = ('{executable} {options} {authentication} '
                      '{protocol}://{host}/{resource}')
        self.last_cmd = cmd_format.format(executable=self.conn_exe,
                                          options=options,
                                          authentication=authentication,
                                          protocol=self.protocol.lower(),
                                          host=self.destination,
                                          resource=resource)
        return self.last_cmd

"""
usage_tracking.py

(C) 2013 - Rackspace Hosting, Inc.

Purpose: To track the number of bytes transmitted in various modes
    (modes are customizable). The class uses a multi-key dictionary
     to track traffic based on 'mode', baseline vs actual bandwidth, and
     direction (e.g. - transmit and receive). Stats can be collected directly
     from 'ifconfig', or can be manually added.

Note: Currently implemented for Linux only (based on ifconfig formatting)

Methods:
    def add_traffic_type(traffic_type)
    def get_interface_baseline(interface=None, traffic_type=None)
    def get_current_bandwidth(traffic_type=None)
    def update_bandwidth_manual(traffic_type=None, rx_bytes=0, tx_bytes=0)
    def update_bandwidth(traffic_type=None, interface=None,
                         rx_bytes=0, tx_bytes=0)

"""
import re


class UsageTracking(object):
    """
    Track the number of bytes transmitted for various traffic types. The class
    uses a multi-key dictionary to track traffic based on 'mode', baseline vs
    actual bandwidth, and direction (e.g. - transmit and receive)

    """
    primary_traffic_type = 'std_traffic'
    mappings = ['rx', 'tx']

    # Mappings are order dependent on ifconfig output.
    # Typically RX is listed first, then TX
    IFCFG_REGEX = re.compile(
        r'bytes\:(?P<{0}>\d+).*bytes\:(?P<{1}>\d+)'.format(*mappings),
        re.IGNORECASE)

    def __init__(self, connection, interface=None, ip_addr=None, logger=None):
        """
        Initialization
        @param connection: active connection to remote system (e.g. ssh object)
        @param interface: physical interface to monitor
        @param ip_addr: ip address of interface (used to determine physical IF)
        @param logger: (OPTIONAL) Logging facility to log data/msgs.
        @return: None
        """
        self.bandwidth = {self.primary_traffic_type:
                          dict(baseline={self.mappings[0]: 0,
                                         self.mappings[1]: 0},
                               bandwidth={self.mappings[0]: 0,
                                          self.mappings[1]: 0})}
        self.connection = connection
        self.log = logger

        # Verify there is enough information to determine where to gather stats
        assert (interface is not None or ip_addr is not None), \
            'Need to specify IP or interface when instantiating UsageTracking'

        # If an IP is specified, get the IP's interface
        if interface is None and ip_addr is not None:
            self.interface = self._get_interface_from_ip(ip_address=ip_addr)
            assert self.interface is not None, \
                "Unable to find interface with IP '{ip}'.".format(ip=ip_addr)
        else:
            self.interface = interface

    def _get_interface_from_ip(self, ip_address):
        """
        @param ip_address: IP Address to use to get the interface
        @return: (string) Interface assigned the specified IP address
        """

        # Get the ifconfig information
        output, _ = self.connection.exec_shell_command_wait_for_prompt(
            cmd='ifconfig')

        # Parse the output for the specified IP; if found, get the previous
        # line (contains the name of the physical interface)
        results = output.split('\r\n')
        for line_num in xrange(len(results)):
            if results[line_num].find(ip_address) != -1:
                target_line = results[line_num - 1]
                break

        # D'Oh!! No IP address matching the specified IP was found
        else:
            if self.log is not None:
                err_msg = 'Unable to find IP address {ip} in output:\n{output}'
                self.log.error(err_msg.format(ip=ip_address, output=output))
            return ''

        # Sample match:
        # eth1      Link encap:Ethernet  HWaddr fe:ed:fa:00:29:64
        pattern = re.compile(r'^(?P<interface>[\w\d]+)\s+')

        # Check the interface line for the name of the interface
        match = pattern.search(target_line)
        if match is not None:
            return match.group('interface')

        if self.log is not None:
            err_msg = ('Unable to find IP address {ip} in output line:\n'
                       '{output}')
            self.log.error(err_msg.format(ip=ip_address, output=target_line))
        return ''

    def add_traffic_type(self, traffic_type):
        """
        Add a traffic type for tracking bandwidth. (Adds key and basic tracking
        substructure to the overall tracking structure)
        @param traffic_type: (string) Name of traffic type. e.g. - SSH
        @return: (Boolean) T/F
            True = traffic type added
            False = Error or traffic type already exists
        """
        if traffic_type not in self.bandwidth.keys():
            self.bandwidth[traffic_type] = dict()
            for type_ in ['bandwidth', 'baseline']:
                self.bandwidth[traffic_type][type_] = {self.mappings[0]: 0,
                                                       self.mappings[1]: 0}
            return True
        return False

    def get_interface_baseline(self, interface=None, traffic_type=None):
        """
        Get the current interface stats to establish a baseline from ifconfig
        @param interface: (OPTIONAL) name of interface to get baseline stats
        @param traffic_type: (OPTIONAL) traffic_type to store baseline
        @return: (dict)  keys:traffic types, sub_keys: rx/tx keywords
                         values: RX/TX stats of interface
        """
        interface = interface or self.interface
        traffic_type = traffic_type or self.primary_traffic_type

        # Get the stats for the interface
        baseline = self._read_interface_bandwidth(interface=interface)
        if baseline:
            if traffic_type not in self.bandwidth.keys():
                self.bandwidth[traffic_type] = dict()
            self.bandwidth[traffic_type]['baseline'] = baseline

        # No baseline results were found
        elif self.log is not None:
            err = 'Unable to get baseline stats for interface \'{interface}\''
            self.log.error(err.format(interface=interface))
        return baseline

    def get_current_bandwidth(self, traffic_type=None):
        """
        Get the bandwidth stats stored for the specified traffic_type
        @param traffic_type: (OPTIONAL) - name of traffic_type to report stats
        @return: (dict) - Dictionary of rx/tx stats
        """
        traffic_type = traffic_type or self.primary_traffic_type
        if traffic_type in self.bandwidth.keys():
            return self.bandwidth[traffic_type]['bandwidth']
        return None

    def update_bandwidth_manual(self, traffic_type=None, rx_bytes=0,
                                tx_bytes=0):
        """
        Update the stats manually (does not use ifconfig)
        @param traffic_type: Traffic Type to update
        @param rx_bytes: Number of bytes to increment the rx by
        @param tx_bytes: Number of bytes to increment the tx by
        @return: (dict) - Number of bytes incremented for rx/tx
        """
        traffic_type = traffic_type or self.primary_traffic_type
        delta = dict(rx=rx_bytes, tx=tx_bytes)

        # Error check before updating results
        if traffic_type not in self.bandwidth.keys():
            if self.log is not None:
                types = self.bandwidth.keys()
                err_msg = ('Traffic Type \'{traffic_type}\' is not recognized.'
                           '\nKnown types: {types!s}')
                self.log.error(err_msg.format(traffic_type=traffic_type,
                                              types=types))
            return dict()

        # Update bandwidth byte count
        for direction in delta.keys():
            self.bandwidth[traffic_type]['bandwidth'][direction] += \
                delta[direction]
        return delta

    def update_bandwidth(self, traffic_type=None, interface=None,
                         rx_bytes=-1, tx_bytes=-1):
        """
        Update the bandwidth. Will increment manually if either the rx/tx_bytes
        parameters are specified. Otherwise, it will poll ifconfig, determine
        the delta from the baseline, and add the difference to the bandwidth
        metric.
        @param traffic_type: (OPTIONAL) - Traffic type to update rx/tx metrics
        @param interface: (OPTIONAL) - Interface to use to gather stats
        @param rx_bytes: (OPTIONAL) - Number of bytes to increment the rx count
        @param tx_bytes: (OPTIONAL) - Number of bytes to increment the tx count
        @return: (dict) - Number of bytes incremented for rx/tx
        """

        # Manually update if rx/tx was specified
        if rx_bytes != -1 or tx_bytes != -1:
            # Zero any unset parameters (so it does not affect the counts)
            if rx_bytes == -1:
                rx_bytes = 0
            if tx_bytes == -1:
                tx_bytes = 0
            return self.update_bandwidth_manual(traffic_type=traffic_type,
                                                rx_bytes=rx_bytes,
                                                tx_bytes=tx_bytes)

        # Update any unspecified parameters and get the latest BW stats
        traffic_type = traffic_type or self.primary_traffic_type
        interface = interface or self.interface
        updated_bandwidth = self._read_interface_bandwidth(interface=interface)

        delta = dict()
        for direction in self.mappings:
            delta[direction] = 0

        # Error check before updating results
        if not updated_bandwidth:
            return dict()

        if traffic_type not in self.bandwidth.keys():
            if self.log is not None:
                types = self.bandwidth.keys()
                err_msg = ('Traffic Type \'{traffic_type}\' is not recognized'
                           '\nKnown Types: {types!s}')
                self.log.error(err_msg.format(traffic_type=traffic_type,
                                              types=types))
            return dict()

        # Update bandwidth byte count by taking latest byte count and
        # subtracting the baseline byte count (for the specified traffic_type)
        for direction in self.mappings:
            current_bw = self.bandwidth[traffic_type]['bandwidth'][direction]
            curr_diff_from_baseline = \
                (updated_bandwidth[direction] -
                 self.bandwidth[traffic_type]['baseline'][direction])

            diff = curr_diff_from_baseline - current_bw
            delta[direction] = diff
            self.bandwidth[traffic_type]['bandwidth'][direction] += diff
        return delta

    def _read_interface_bandwidth(self, interface=None):
        """
        Get the bandwidth count from the interface via ifconfig
        @param interface: (OPTIONAL) Interface to use to get stats
        @return: (dict) - RX/TX stats of interface
        """
        interface = interface or self.interface
        bandwidth = dict()

        cmd_fmt = 'ifconfig {interface} | grep -i bytes'
        cmd = cmd_fmt.format(interface=interface)

        # Execute command on remote system
        output, std_err = self.connection.exec_shell_command_wait_for_prompt(
            cmd=cmd)
        results = self.IFCFG_REGEX.search(output)
        if results is not None:
            for type_ in self.mappings:
                bandwidth[type_] = int(results.group(type_))

        # If you get here, the routine was unable to parse out the results
        elif self.log is not None:
            err = 'No interface results were found for {interface}:\n{output}'
            self.log.error(err.format(interface=interface, output=output))
            if std_err is not None:
                self.log.error('Error from cmd: {err}'.format(err=std_err))
        return bandwidth

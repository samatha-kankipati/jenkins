from ccengine.common.tools.equality_tools import EqualityTools


class Partition:
    """
    @summary: Represents a Disk Partition
    """
    def __init__(self, name, size, type):
        self.name = name
        self.size = size
        self.type = type

    def __eq__(self, other):
        """
        @summary: Overrides the default equals
        @param other: Partition object to compare with
        @type other: Partition
        @return: True if Partition objects are equal, False otherwise
        @rtype: bool
        """
        return EqualityTools.are_objects_equal(self, other)

    def __ne__(self, other):
        """
        @summary: Overrides the default not-equals
        @param other: Partition object to compare with
        @type other: Partition
        @return: True if Partition objects are not equal, False otherwise
        @rtype: bool
        """
        return not self == other

    def __repr__(self):
        """
        @summary: Return string representation of Partition
        @return: String representation of Partition
        @rtype: string
        """
        return "Partition Name : %s, Size: %s, Type : %s" % (self.name, self.size, self.type)


class DiskSize:
    """
    @summary: Represents a Disk Size
    """

    def __init__(self, value, unit, leeway_for_disk_size=2):
        self.value = float(value)
        self.unit = unit
        self.leeway_for_disk_size = leeway_for_disk_size

    def __eq__(self, other):
        """
        @summary: Overrides the default equals
        @param other: DiskSize object to compare with
        @type other: DiskSize
        @return: True if DiskSize objects are equal, False otherwise
        @rtype: bool
        """
        return self.unit == other.unit and EqualityTools.are_sizes_equal(
                                           self.value, other.value,
                                           self.leeway_for_disk_size)

    def __ne__(self, other):
        """
        @summary: Overrides the default not-equals
        @param other: DiskSize object to compare with
        @type other: DiskSize
        @return: True if DiskSize objects are not equal, False otherwise
        @rtype: bool
        """
        return not self == other

    def __repr__(self):
        """
        @summary: Return string representation of DiskSize
        @return: String representation of DiskSize
        @rtype: string
        """
        return "Disk Size : %s %s" % (self.value, self.unit)

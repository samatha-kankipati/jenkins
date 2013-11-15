from ccengine.common.tools.equality_tools import EqualityTools


class FileDetails:
    """
    @summary: Represents File details
    """
    def __init__(self, absolute_permissions, content, name):
        self.absolute_permissions = absolute_permissions
        self.content = content
        self.name = name

    def __eq__(self, other):
        return EqualityTools.are_objects_equal(self, other)

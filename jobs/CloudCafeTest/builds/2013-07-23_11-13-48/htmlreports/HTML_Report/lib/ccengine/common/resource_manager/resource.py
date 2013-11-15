class Resource:
    """
    @summary: Keeps details of a resource like server or image and how to delete it.
    """

    def __init__(self, resource_id, delete_function):
        self.resource_id = resource_id
        self.delete_function = delete_function

    def delete(self):
        """
        @summary: Deletes the resource
        """
        self.delete_function(self.resource_id)

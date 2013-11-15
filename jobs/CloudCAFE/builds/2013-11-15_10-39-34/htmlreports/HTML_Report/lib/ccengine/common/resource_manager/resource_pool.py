from ccengine.common.resource_manager.resource import Resource


class ResourcePool:
    """
    @summary: Pool of resources to be tracked for deletion.
    """
    def __init__(self):
        self.resources = []

    def add(self, resource_id, delete_function):
        """
        @summary: Adds a resource to the resource pool
        @param resource_id: Unique identifier of resource
        @type resource_id: string
        @param delete_function: The function to be called to delete a server
        @type delete_function: Function Pointer
        """
        self.resources.append(Resource(resource_id, delete_function))

    def release(self):
        """
        @summary: Delete all the resources in the Resource Pool
        """
        for resource in self.resources:
            try:
                resource.delete()
            except:
                pass

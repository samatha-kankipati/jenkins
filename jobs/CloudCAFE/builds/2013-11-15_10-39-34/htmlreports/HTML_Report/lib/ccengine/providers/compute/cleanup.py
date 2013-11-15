from ccengine.providers.compute.compute_api import ComputeAPIProvider\
                                                 as _ComputeAPIProvider
from ccengine.providers.configuration import MasterConfigProvider as _MCP

config = _MCP()
compute_provider = _ComputeAPIProvider(config)

"""Deletes all servers"""
servers = compute_provider.servers_client.list_servers_with_detail()

for server in servers.entity:
    compute_provider.servers_client.delete_server(server.id)
    print 'deleting server ' + server.id

"""Deletes all images"""
images = compute_provider.images_client.list_images_with_detail()

for image in images.entity:
    if hasattr(image.metadata, "instance_uuid"):
        compute_provider.images_client.delete_image(image.id)
        print 'deleting image ' + image.id

keypairs = compute_provider.keypairs_client.list_keypairs()

for keypair in keypairs.entity:
    compute_provider.keypairs_client.delete_keypair(keypair.name)
    print 'deleting keypair ' + keypair.name
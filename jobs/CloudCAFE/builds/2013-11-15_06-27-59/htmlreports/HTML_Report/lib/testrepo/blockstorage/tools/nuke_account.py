'''
@summary: Lunr API Volume Smoke Tests - Create, List, Get Info, Update, Delete Volume.
@copyright: Copyright (c) 2012 Rackspace US, Inc.
'''
from testrepo.common.testfixtures.blockstorage.compute_integration import \
    ComputeIntegrationFixture


class VolumeAttachmentsAPISmoke(ComputeIntegrationFixture):
    '''
    @summary: Lunr API Volume Smoke Tests - Create, List, Get Info, Update,
    Delete Volume.
    '''
    @classmethod
    def setUpClass(cls):
        super(VolumeAttachmentsAPISmoke, cls).setUpClass()

    def test_nuke_account(self):
        print '\n'
        trouble_servers = []
        trouble_snapshots = []
        trouble_volumes = []
    #Get all servers
        resp = self.compute_provider.servers_client.list_servers()
        servers = resp.entity or []
        #Try to delete all attachments
        for server in servers:
            print "Deleting server attachments for {0}".format(server.id)
            resp = self.volume_attachments_provider.client.\
                get_server_volume_attachments(server.id)
            server_attachments = resp.entity or []
            print "(failed with {0})".format(resp.status_code) if not resp.ok else "(suceeded)"
            try:
                for server_attachment in server_attachments:
                    print "Deleting attachment {0}".format(
                        server_attachment.id)
                    resp = self.volume_attachments_provider.\
                        client.delete_volume_attachment(
                            server_attachment.id, server.id)
                    print "(failed with {0})".format(resp.status_code) if not resp.ok else "(suceeded)"
            except:
                pass

            try:
                print "Deleting attachment {0}".format(server_attachments.id)
                resp = self.volume_attachments_provider.client.\
                    delete_volume_attachment(server_attachments.id, server.id)
                print "(failed with {0})".format(resp.status_code) if not resp.ok else "(suceeded)"
            except:
                pass

        #Delete all servers
        for server in servers:
            print "Deleting server {0}".format(server.id)
            resp = self.compute_provider.servers_client.delete_server(server.id)
            print "(failed with {0}: )".format(resp.status_code, resp.msg) if not resp.ok else "(suceeded)"
            if not resp.ok:
                trouble_servers.append(server.id)

    #Delete all Snapshots
        resp = self.volumes_provider.volumes_client.list_all_snapshots()
        snapshots = resp.entity or []
        for snapshot in snapshots:
            print "Deleting snapshot {0}".format(snapshot.id)
            resp = self.volumes_provider.volumes_client.delete_snapshot(snapshot.id)
            print "(failed with {0})".format(resp.status_code) if not resp.ok else "(suceeded)"
            if not resp.ok:
                trouble_snapshots.append(snapshot.id)

    #Delete all Volumes
        resp = self.volumes_provider.volumes_client.list_all_volumes()
        volumes = resp.entity or []
        for volume in volumes:
            print "Deleting volume {0}".format(volume.id)
            resp = self.volumes_provider.volumes_client.delete_volume(volume.id)
            print "(failed with {0})".format(resp.status_code) if not resp.ok else "(suceeded)"
            if not resp.ok:
                trouble_volumes.append(volume.id)

        account_clean = True
        if trouble_servers:
            account_clean = False
            print '\n\nTrouble Servers:'
            for id_ in trouble_servers:
                print id_

        if trouble_snapshots:
            account_clean = False
            print '\n\nTrouble Snapshots:'
            for id_ in trouble_snapshots:
                print id_

        if trouble_volumes:
            account_clean = False
            print '\n\nTrouble Volumes:'
            for id_ in trouble_volumes:
                print id_

        assert account_clean, 'Unable to clean account.  There where issues'

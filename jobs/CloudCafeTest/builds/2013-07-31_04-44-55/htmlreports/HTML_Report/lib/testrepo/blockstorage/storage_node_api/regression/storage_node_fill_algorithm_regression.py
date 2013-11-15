'''
@summary: Functional Lunr API Volume Smoke Tests
@copyright: Copyright (c) 2012 Rackspace US, Inc.
'''
import json
from datetime import datetime
from ccengine.clients.blockstorage import storage_node_api_client
from testrepo.common.testfixtures.blockstorage import LunrAPIFixture
from ccengine.domain.blockstorage.lunr_api import VolumeType as \
        _VolumeTypeDomainObject


class LunrVolumeFunctionalTest(LunrAPIFixture):
    '''
        @summary: Functional Lunr API Volume Smoke Tests

        Setup.
        Create two user accounts
        Create lunr clients for both accounts

        Get supported volumes types
        Get list of all storage nodes and create clients for them

        Create two volumes for each storage node in the environment
        Capture the volume data to delete them later

        Test Validation
        Get list of all volumes on each storage node for each account
        Verify that there are only two volumes per node per account
    '''
    @classmethod
    def setUpClass(cls):
        super(LunrVolumeFunctionalTest, cls).setUpClass()
        cls.total_users = None
        cls.volumes_per_node_per_user = None
        cls.expected_volumes_per_node = None
        cls.expected_volumes_per_node_type = None
        cls.node_clients = None
        cls.volume_types = None
        cls.user_clients = None

    @classmethod
    def create_user_clients(cls, num):
        cls.user_clients = []
        #Create N users (and their respective clients)
        for n in range(int(num)):
            cls.user_clients.append(cls.LunrAPIProvider.create_user_client())
        return cls.user_clients

    @classmethod
    def create_node_clients(cls):
        cls.node_clients = []
        cls.vtypes = json.loads(cls.admin_client.VolumeTypes.list().content)
        node_resp = cls.LunrAPIProvider.lunr_api_client.Nodes.list()
        nodes = json.loads(node_resp.content)
        for n in nodes:
            if n['status'] == 'ACTIVE':
                nc = storage_node_api_client.\
                        StorageNodeAPIClient(cls.config.storage_node_api.ssl,
                                n['hostname'], n['port'], name=n['name'])
                nc.volume_type_name = n['volume_type_name']
                nc.name = n['name']
                cls.node_clients.append(nc)
            else:
                cls.fixture_log.warning("WARNING: Node {0} is {1}".format(
                        str(n['name']), str(n['status'])))
                print "\nWARNING: Node {0} is {1}".format(str(n['name']),
                                                          str(n['status']))
        return cls.node_clients

    @classmethod
    def create_volume_type_list(cls):
        api_response = cls.admin_client.VolumeTypes.list()
        cls.volume_types = cls.LunrAPIProvider.\
                convert_json_to_domain_object_list(
                json.loads(api_response.content), _VolumeTypeDomainObject)
        return cls.volume_types

    @classmethod
    def list_all_accounts(cls):
        accts = json.loads(cls.admin_client.Accounts.list().content)
        return accts

    @classmethod
    def delete_all_accounts(cls):
        accts = cls.list_all_accounts()
        for acct in accts:
            r = cls.admin_client.Accounts.delete(acct['id'])
            if not r.ok:
                print 'Error deleting account: %s' % str(acct['id'])

    @classmethod
    def list_all_volumes_on_all_nodes(cls):
        #List all volumes on all nodes
        all_volumes = []
        for n in cls.node_clients:
            vol_dict = json.loads(n.Volumes.list().content)
            if vol_dict:
                for vol in vol_dict:
                    all_volumes.append(vol_dict)
        return all_volumes

    @classmethod
    def delete_all_volumes_on_all_nodes(cls):
        for node in cls.node_clients:
            #Get node volumes
            r = node.Volumes.list()
            volumes = json.loads(r.content)
            for v in volumes:
                r = cls.admin_client.Volumes.delete(v['id'])
                if not r.ok and r.status_code != 404:
                    print 'Unable to delete volume {0} on node {1}'.format(v['id'], node.name)

    @classmethod
    def list_all_volumes_for_account_for_node(cls, user_account, node):
        #Get list of all volumes for account
        account_volumes = json.loads(user_account.Volumes.list().content)
        account_volumes = [acct_vol for acct_vol in account_volumes if acct_vol['account_id']==user_account.account_id]
        node_volumes = json.loads(node.Volumes.list().content)
        intersection_list = []

        class volume_info(object):
            def __init__(self, volume_id, account_info, node_info):
                self.node_info = node_info
                self.account_info = account_info
                self.volume_id = volume_id

        for account_vol in account_volumes:
            for node_vol in node_volumes:
                if account_vol['id'] == node_vol['id']:
                    intersection_list.append(volume_info(node_vol['id'], account_vol, node_vol))

        return intersection_list

    @classmethod
    def list_all_volumes_for_created_accounts_for_node(cls, node):
        vol_list = []
        for user in cls.user_clients:
            r = cls.list_all_volumes_for_account_for_node(user, node)
            for v in r:
                vol_list.append(v)
        return vol_list

    @classmethod
    def list_all_volumes_for_created_accounts_for_all_nodes(cls):
        vol_list = []
        for user in cls.user_clients:
            for node in cls.node_clients:
                r = cls.list_all_volumes_for_account_for_node(user, node)
                for v in r:
                    vol_list.append(v)
        return vol_list

    @classmethod
    def delete_all_created_accounts(cls):
        print 'Deleting all created accounts'
        for user in cls.user_clients:
            cls.delete_all_volumes_on_all_nodes()
            r = cls.admin_client.Accounts.delete(user.account_id)
            if not r.ok:
                print 'Unable to delete account {0}'.format(user.account_name)

    @classmethod
    def delete_all_volumes_for_all_created_accounts(cls):
        print 'Deleting all volumes for all created accounts'
        for user in cls.user_clients:
            r = user.Volumes.list()
            volumes = json.loads(r.content)
            for v in volumes:
                r = cls.admin_client.Volumes.delete(v['id'])
                if not r.ok and r.status_code != 404:
                    print 'Unable to delete volume {0}'.format(v['id'])

    @classmethod
    def create_volumes_for_all_created_accounts_for_each_node_type(cls):
        '''
            Creates X volumes, where x = # of nodes * volumes_per_node_per_user
        '''
        for user in cls.user_clients:
            for vtype in cls.volume_types:
                for n in range(cls.volumes_per_node_per_user):
                    expected_name = "TestVolume_%d" % datetime.now().microsecond
                    expected_size = 1
                    r = user.Volumes.create(expected_name, expected_size, vtype.name)
                    assert r.ok

    @classmethod
    def create_volumes_for_all_created_accounts_for_all_nodes(cls):
        '''
            Creates X volumes, where x = # of node TYPES * volumes_per_node_per_user
        '''
        for user in cls.user_clients:
                for node in cls.node_clients:
                    for n in range(cls.volumes_per_node_per_user):
                        expected_name = "TestVolume_%d" % datetime.now().microsecond
                        expected_size = 1
                        r = user.Volumes.create(expected_name, expected_size, node.volume_type_name)
                        assert r.ok

    @classmethod
    def paramaterized_setup(cls, **kwargs):
        '''
            Creates volumes_per_node_per_user * (total node count) of volumes
            for each of total_users number of users
        '''
        #Set up test vars
        cls.total_users = kwargs['total_users']
        cls.volumes_per_node_per_user = kwargs['volumes_per_node_per_user']

        #Gather environment data and setup node clients
        cls.node_clients = cls.create_node_clients()
        cls.volume_types = cls.create_volume_type_list()

        #Create accounts and account clients
        cls.user_clients = cls.create_user_clients(cls.total_users)

        #Create volumes according to paramater input
        if kwargs.get('account_level_broad_fill', None) == True:
            cls.create_volumes_for_all_created_accounts_for_all_nodes()
            cls.expected_volumes_per_node = cls.volumes_per_node_per_user * cls.total_users

        elif kwargs.get('node_level_deep_fill', None) == True:
            cls.create_volumes_for_all_created_accounts_for_each_node_type()
            cls.expected_volumes_per_node_type = cls.volumes_per_node_per_user * cls.total_users

    def setUp(self):
        #Add cleanups for the stuff that's gonna happen in the paramaterized_setup
        self.addCleanup(self.delete_all_created_accounts)
        self.addCleanup(self.delete_all_volumes_for_all_created_accounts)

    '''TESTS'''
    def test_account_level_broad_fill(self):
        self.paramaterized_setup(total_users=5, volumes_per_node_per_user=4,
                                 account_level_broad_fill=True)
        passed = True
        for user in self.user_clients:
            header_printed = False
            print '\n{0}'.format(user.account_id)
            for node in self.node_clients:
                vol_info_list = self.list_all_volumes_for_account_for_node(user, node)
                if len(vol_info_list) != self.volumes_per_node_per_user:
                    if not header_printed:
                        s1 = '{0:^15}'.format('Storage') + '{0:^16}'.format('Observed') + '    ' + '{0:^16}'.format('Expected')
                        s2 = '{0:^15}'.format('Node') + '{0:^16}'.format('Volume Count') + ' != ' + '{0:^16}'.format('Volume Count')
                        print '\n' + s1 + '\n' + s2
                        header_printed = True
                    s = '{0:>15}'.format(node.name) + ': ' + '{0:^14}'.format(len(vol_info_list)) + ' != ' + '{0:^16}'.format(self.volumes_per_node_per_user)
                    print s
                    passed = False
                else:
                    s = '{0:>15}'.format(node.name) + ': ' + '{0:^14}'.format(len(vol_info_list)) + ' == ' + '{0:^16}'.format(self.volumes_per_node_per_user)
                    print s
        assert passed, 'The volume count of one or more storage nodes did not match the expected count of volumes for that account'

    def test_node_level_deep_fill(self):
        self.paramaterized_setup(total_users=20, volumes_per_node_per_user=1, node_level_deep_fill = True)
        passed = True
        for vtype in self.volume_types:
            full_node_found = False
            header_printed = False
            for node in self.node_clients:
                if node.volume_type_name == vtype.name:
                    volumes = self.list_all_volumes_for_created_accounts_for_node(node)
                    if len(volumes) == self.expected_volumes_per_node_type:
                        if full_node_found == True:
                            if not header_printed:
                                s1 = '{0:^15}'.format('Storage') + '{0:^16}'.format('Observed') + '    ' + '{0:^16}'.format('Expected')
                                s2 = '{0:^15}'.format('Node') + '{0:^16}'.format('Volume Count') + ' != ' + '{0:^16}'.format('Volume Count')
                                print '\n' + s1 + '\n' + s2
                                header_printed = True
                            print 'More than one node was found containing volumes for the %s volume type' % str(vtype.name)
                            s = '{0:>15}'.format(node.name) + ': ' + '{0:^14}'.format(len(volumes)) + ' != ' + '{0:^16}'.format(self.expected_volumes_per_node_type)
                            print s
                            passed = False
                        else:
                            full_node_found = True
            if full_node_found != True:
                print 'No node was found containing %s volumes (expected) for the %s volume type' % (str(self.expected_volumes_per_node_type), str(vtype.name))
                passed = False
        assert passed, 'The volume count of one or more storage nodes did not match the expected count'

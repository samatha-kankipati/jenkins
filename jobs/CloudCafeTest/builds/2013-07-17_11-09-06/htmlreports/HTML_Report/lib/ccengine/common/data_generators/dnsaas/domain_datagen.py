import ccengine.common.tools.datagen as datagen


class SmokeData():
    def __init__(self):

        self.random = datagen.random_string('whoisthis')
        self.name = '{0}.com'.format(self.random)
        self.emailAddress = 'mail@{0}'.format(self.name)
        self.ttl = 3600
        self.comment = 'creating a Domain'
        self.name_list = [self.name, self.name]
        self.subname_list = ['sub1.{0}'.format(self.name),
                             'sub2.{0}'.format(self.name)]
        self.type_list = ['A', 'A']
        self.data_list = ['192.0.2.17', '192.0.2.18']
        self.ttl_list = [3600, 5400]
        self.comment_list = ['just do it', 'just do it again']


class RecordData():
    def __init__(self):
        self.rcname = datagen.random_string('example')
        self.random = datagen.random_string('recordzone')
        self.name = '{0}.com'.format(self.random)
        self.cname = '{0}.com'.format(self.rcname)
        self.emailAddress = 'mail@{0}'.format(self.name)
        self.ttl = 3600
        self.comment = datagen.random_string('creating a Domain')
        domain_name = self.name
        c_domain_name = 'www.{0}'.format(self.name)
        self.name_list = [domain_name,
                          domain_name,
                          c_domain_name,
                          domain_name]
        self.type_list = ['A', 'AAAA', 'CNAME', 'TXT']
        self.data_list = ['192.0.2.6',
                          '4321:0:1:2:3:4:567:89ab',
                          self.cname,
                          'Some example text']
        self.ttl_list = [3600, 5400, 5200, 3600]
        self.comment_list = ['this is comment for A record',
                             'this is comment for AAAA record',
                             'this is comment for CNAME record',
                             'this is comment for TXT record']
        self.updated_comment = ['this is updated A record',
                                'this is also updated AAAA record',
                                'this is also updated CNAME record',
                                'this is also updated TXT record']
 
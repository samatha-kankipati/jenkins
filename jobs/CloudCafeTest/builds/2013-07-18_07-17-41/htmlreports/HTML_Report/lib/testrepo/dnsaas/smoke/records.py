from testrepo.common.testfixtures.dnsaas import RecordFixture
import json


class SmokeTest(RecordFixture):

    def test_records(self):
        name_list = self.name_list
        type_list = self.type_list
        data_list = self.data_list
        ttl_list = self.ttl_list
        comment_list = self.comment_list
        updated_comment = self.updated_comment
        domain_id = self.domain_id
        api_response = self.domain_provider.record_client.\
            create_record(name_list=name_list,
                          type_list=type_list,
                          data_list=data_list,
                          ttl_list=ttl_list,
                          comment_list=comment_list,
                          domain_id=domain_id)
        errStr = " Create Record call  failed with error: \
            {0} and status code {1}: \n '{2}"
        self.assertEquals(api_response.status_code, 202,
                          errStr.format(api_response.reason,
                                      api_response.status_code,
                                      json.loads(api_response.content)))
        callback = self.domain_provider.\
            test_wait_for_status(api_response)
        self.assertEquals(callback, 'COMPLETED')

        api_response = self.domain_provider.record_client.\
            list_records(domain_id)
        errStr = " list record call failed with error: \
            {0} and status code {1}: \n '{2}"
        self.assertEquals(api_response.status_code, 200,
                          errStr.format(api_response.reason,
                                      api_response.status_code,
                                      json.loads(api_response.content)))

        records = api_response.entity
        record_id_list = []
        for record in records:
            record_id = record.id
            if record.type != 'NS':
                record_id_list.append(record_id)
            api_response_rec = self.domain_provider.record_client.\
                list_records_id(domain_id, record_id)
            errStr = " list record call failed with error: \
            {0} and status code {1}: \n '{2}"
            self.assertTrue(api_response.ok,
                            errStr.format(api_response_rec.reason,
                                          api_response_rec.status_code,
                                          json.loads(api_response_rec.content)))
        #update records
        api_response = self.domain_provider.record_client.\
            update_record_id(name_list=name_list,
                             id_list=record_id_list,
                             data_list=data_list,
                             ttl_list=ttl_list,
                             comment_list=updated_comment,
                             domain_id=domain_id)

        callback = self.domain_provider.\
            test_wait_for_status(api_response)
        self.assertEquals(callback, 'COMPLETED')
        errStr = " Update Record call  failed with error: \
            {0} and status code {1}: \n '{2}"
        self.assertEquals(api_response.status_code, 202,
                          errStr.format(api_response.reason,
                                        api_response.status_code,
                                        json.loads(api_response.content)))

        for record in records:
            record_id = record.id
            if record.type != 'NS':
                api_response_rec = self.domain_provider.record_client.\
                    delete_records_id(domain_id, record_id)
                errStr = " Delete Record call  failed with error: \
                    {0} and status code {1}: \n '{2}"
                self.assertEquals(api_response.status_code, 202,
                    errStr.format(api_response.reason,
                                  api_response.status_code,
                                  json.loads(api_response.content)))
                callback = self.domain_provider.\
                    test_wait_for_status(api_response_rec)
                self.assertEquals(callback, 'COMPLETED')

    def test_srv_records(self):
        domain_name = self.name_domain
        name_list = [domain_name, domain_name,
                     '_ftp._tcp.{0}'.format(domain_name),
                     '_sip._tcp.{0}'.format(domain_name)]
        type_list = ['MX', 'MX', 'SRV', 'SRV']
        data_list = ['mail.{0}.'.format(domain_name),
                     'mail.{0}.'.format(domain_name),
                     '1 3443 ftp.{0}.'.format(domain_name),
                     '1 3444 sip.{0}.'.format(domain_name)]
        priority_list = [5, 10, 15, 30]
        ttl_list = [3600, 5400, 5200, 3000]
        comment_list = ['this is comment for MX record',
                        'this is comment for MX record',
                        'this is comment for SRV record',
                        'this is comment for SRV record']
        updated_comment = ['this is updated comment for MX record',
                           'this is updated comment for MX record',
                           'this is updated comment for SRV record',
                           'this is updated comment for SRV record']
        domain_id = self.domain_id
        api_response = self.domain_provider.record_client.\
            create_record(name_list=name_list,
                          type_list=type_list,
                          data_list=data_list,
                          ttl_list=ttl_list,
                          priority_list=priority_list,
                          comment_list=comment_list,
                          domain_id=domain_id)
        errStr = " Create Record call  failed with error: \
            {0} and status code {1}: \n '{2}"
        self.assertEquals(api_response.status_code, 202,
            errStr.format(api_response.reason,
                          api_response.status_code,
                          json.loads(api_response.content)))
        callback = self.domain_provider.\
            test_wait_for_status(api_response)
        self.assertEquals(callback, 'COMPLETED')

        api_response = self.domain_provider.record_client.\
            list_records(domain_id)

        errStr = " list record call failed with error: \
            {0} and status code {1}: \n '{2}"
        self.assertEquals(api_response.status_code, 200,
                          errStr.format(api_response.reason,
                                        api_response.status_code,
                                        json.loads(api_response.content)))
        records = api_response.entity
        record_id_list = []
        for record in records:
            record_id = record.id
            if record.type != 'NS':
                record_id_list.append(record_id)
            api_response_rec = self.domain_provider.record_client.\
                list_records_id(domain_id, record_id)
            errStr = " list record call failed with error: \
            {0} and status code {1}: \n '{2}"
            self.assertTrue(api_response.ok,
                            errStr.format(api_response_rec.reason,
                                          api_response_rec.status_code,
                                          json.loads(api_response_rec.content)))
        api_response = self.domain_provider.record_client.\
            update_record_id(name_list=name_list,
                             id_list=record_id_list,
                             data_list=data_list,
                             ttl_list=ttl_list,
                             priority_list=priority_list,
                             comment_list=updated_comment,
                             domain_id=domain_id)
        errStr = " Update Record call  failed with error: \
            {0} and status code {1}: \n '{2}"
        self.assertEquals(api_response.status_code, 202,
                          errStr.format(api_response.reason,
                                        api_response.status_code,
                                        json.loads(api_response.content)))
        callback = self.domain_provider.\
            test_wait_for_status(api_response)
        self.assertEquals(callback, 'COMPLETED')

        for record in records:
            record_id = record.id
            if record.type != 'NS':
                api_response_rec = self.domain_provider.record_client.\
                    delete_records_id(domain_id, record_id)
                errStr = " Delete Record call  failed with error: \
                    {0} and status code {1}: \n '{2}"
                self.assertEquals(api_response.status_code, 202,
                    errStr.format(api_response.reason,
                                  api_response.status_code,
                                  json.loads(api_response.content)))
                callback = self.domain_provider.\
                    test_wait_for_status(api_response_rec)
                self.assertEquals(callback, 'COMPLETED')

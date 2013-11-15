from testrepo.common.testfixtures.stacktach import StackTachDBFixture
from ccengine.common.decorators import attr


class StackTachDBTest(StackTachDBFixture):

    default_not_none_msg = "The response entity is not NONE"

    @classmethod
    def setUpClass(cls):
        super(StackTachDBTest, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        super(StackTachDBTest, cls).tearDownClass()

    @attr(type='negative')
    def test_get_invalid_launch(self):
        '''
        @summary: Verify that Get an Invalid Launch ID fails
        '''

        response = self.stacktachdb_provider.client.get_launch('aa')

        self.assertFalse(response.ok,
                         self.msg.format("status code",
                                         "Not a 2xx Success response",
                                         response.status_code,
                                         response.reason,
                                         response.content))
        self.assertIsNone(response.entity, self.default_not_none_msg)

    @attr(type='negative')
    def test_get_invalid_delete(self):
        '''
        @summary: Verify that Get a Invalid Delete ID fails
        '''

        response = self.stacktachdb_provider.client.get_delete('aa')

        self.assertFalse(response.ok,
                         self.msg.format("status code",
                                         "Not a 2xx Success response",
                                         response.status_code,
                                         response.reason,
                                         response.content))
        self.assertIsNone(response.entity, self.default_not_none_msg)

    @attr(type='negative')
    def test_get_invalid_exist(self):
        '''
        @summary: Verify that Get Invalid Exist ID fails
        '''

        response = self.stacktachdb_provider.client.get_exist('aa')

        self.assertFalse(response.ok,
                         self.msg.format("status code",
                                         "Not a 2xx Success response",
                                         response.status_code,
                                         response.reason,
                                         response.content))
        self.assertIsNone(response.entity, self.default_not_none_msg)

    @attr(type='negative')
    def test_get_launches_by_invalid_date_min(self):
        '''
        @summary: Verify that Get Launches by invalid minimum date fails
        '''

        response = (self.stacktachdb_provider
                    .client
                    .get_launches_by_date_min(launched_at_min="$#@!"))

        self.assertFalse(response.ok,
                         self.msg.format("status code",
                                         "Not a 2xx Success response",
                                         response.status_code,
                                         response.reason,
                                         response.content))
        self.assertIsNone(response.entity, self.default_not_none_msg)

    @attr(type='negative')
    def test_get_launches_by_invalid_date_max(self):
        '''
        @summary: Verify that Get Launches by invalid maximum date fails
        '''

        response = (self.stacktachdb_provider
                    .client
                    .get_launches_by_date_max(launched_at_max="$#@!"))

        self.assertFalse(response.ok,
                         self.msg.format("status code",
                                         "Not a 2xx Success response",
                                         response.status_code,
                                         response.reason,
                                         response.content))
        self.assertIsNone(response.entity, self.default_not_none_msg)

    @attr(type='negative')
    def test_get_launches_by_invalid_date_min_and_invalid_date_max(self):
        '''
        @summary: Verify that Get Launches by invalid minimum and
            invalid maximum date fails
        '''

        response = (self.stacktachdb_provider
                    .client
                    .get_launches_by_date_min_and_date_max(
                    launched_at_min="$#@!",
                    launched_at_max="$#@!"))

        self.assertFalse(response.ok,
                         self.msg.format("status code",
                                         "Not a 2xx Success response",
                                         response.status_code,
                                         response.reason,
                                         response.content))
        self.assertIsNone(response.entity, self.default_not_none_msg)

    @attr(type='negative')
    def test_get_deletes_by_invalid_date_min(self):
        '''
        @summary: Verify that Get Deletes by invalid minimum date fails
        '''

        response = (self.stacktachdb_provider
                    .client
                    .get_deletes_by_date_min(deleted_at_min="$#@!"))

        self.assertFalse(response.ok,
                         self.msg.format("status code",
                                         "Not a 2xx Success response",
                                         response.status_code,
                                         response.reason,
                                         response.content))
        self.assertIsNone(response.entity, self.default_not_none_msg)

    @attr(type='negative')
    def test_get_deletes_by_invalid_date_max(self):
        '''
        @summary: Verify that Get Deletes by invalid maximum date fails
        '''

        response = (self.stacktachdb_provider
                    .client
                    .get_deletes_by_date_max(deleted_at_max="$#@!"))

        self.assertFalse(response.ok,
                         self.msg.format("status code",
                                         "Not a 2xx Success response",
                                         response.status_code,
                                         response.reason,
                                         response.content))
        self.assertIsNone(response.entity, self.default_not_none_msg)

    @attr(type='negative')
    def test_get_deletes_by_invalid_date_min_and_invalid_date_max(self):
        '''
        @summary: Verify that Get Deletes by invalid minimum and
            invalid maximum date fails
        '''

        response = (self.stacktachdb_provider
                    .client
                    .get_deletes_by_date_min_and_date_max(
                    deleted_at_min="$#@!",
                    deleted_at_max="$#@!"))

        self.assertFalse(response.ok,
                         self.msg.format("status code",
                                         "Not a 2xx Success response",
                                         response.status_code,
                                         response.reason,
                                         response.content))
        self.assertIsNone(response.entity, self.default_not_none_msg)

    @attr(type='negative')
    def test_list_launches_for_invalid_uuid(self):
        '''
        @summary: Verify that List Launches by uuid fails
        '''

        response = (self.stacktachdb_provider.client
                    .list_launches_for_uuid(instance="$#@!"))

        self.assertFalse(response.ok,
                         self.msg.format("status code",
                                         "Not a 2xx Success response",
                                         response.status_code,
                                         response.reason,
                                         response.content))
        self.assertIsNone(response.entity, self.default_not_none_msg)

    @attr(type='negative')
    def test_list_deletes_for_invalid_uuid(self):
        '''
        @summary: Verify that List Deletes by uuid fails

        '''

        response = (self.stacktachdb_provider.client
                    .list_deletes_for_uuid(instance="$#@!"))

        self.assertFalse(response.ok,
                         self.msg.format("status code",
                                         "Not a 2xx Success response",
                                         response.status_code,
                                         response.reason,
                                         response.content))
        self.assertIsNone(response.entity, self.default_not_none_msg)

    @attr(type='negative')
    def test_list_exists_for_invalid_uuid(self):
        '''
        @summary: Verify that List Exists by uuid fails

        '''

        response = (self.stacktachdb_provider.client
                    .list_exists_for_uuid(instance="$#@!"))

        self.assertFalse(response.ok,
                         self.msg.format("status code",
                                         "Not a 2xx Success response",
                                         response.status_code,
                                         response.reason,
                                         response.content))
        self.assertIsNone(response.entity, self.default_not_none_msg)

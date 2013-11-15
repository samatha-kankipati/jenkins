from ccengine.clients.identity.v2_0.rax_auth_admin_api \
    import IdentityAdminClient


class IdentityServiceClient(IdentityAdminClient):

    USERS = 'users'
    SOFT_DELETED = 'softDeleted'

    def delete_user_hard(self, userId, requestslib_kwargs=None):

        '''
        @summary: Delete user by id hard
        @param userId: The user id
        @type userId type: String
        @return: User Delete information
        @rtype: Response Object
        '''

        '''
            DELETE
            v2.0/softDeleted/users/{userId}
        '''
        url = '{0}/{1}/{2}/{3}'.format(self.base_url, self.SOFT_DELETED,
                                       self.USERS, userId)
        server_response = \
            self.delete(url, requestslib_kwargs=requestslib_kwargs)
        return server_response

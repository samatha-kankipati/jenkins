from ccengine.clients.identity.v2_0.rax_auth_admin_api \
    import IdentityAdminClient


class IdentityServiceClient(IdentityAdminClient):

    USERS = 'users'
    SOFT_DELETED = 'softDeleted'

    def delete_user_hard(self, user_id, requestslib_kwargs=None):

        '''
        @summary: Delete user by id hard
        @param user_id: The user id
        @type user_id type: String
        @return: User Delete information
        @rtype: Response Object
        '''

        '''
            DELETE
            v2.0/softDeleted/users/{user_id}
        '''
        url = '{0}/{1}/{2}/{3}'.format(self.base_url, self.SOFT_DELETED,
                                       self.USERS, user_id)
        server_response = \
            self.delete(url, requestslib_kwargs=requestslib_kwargs)
        return server_response

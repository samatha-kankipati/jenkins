import inspect
import os


class LBaasRBACroles(object):
    """
    This class helps facilate RBAC testing for LBaaS. It reads in a
    data file (response codes for each role based on the API), and
    provides each test the ability:
        + to determine which API is testing based on the calling test's name
        + to determine what roles are to be tested
        + to get the expected response code for each role
        + to execute the test and return errors, if any.
    """

    CLOUD_CAFE_TEST_CONFIG_ENV_VAR = 'CLOUDCAFE_TEST_CONFIG'

    def __init__(self, fixture, data_file=None):
        self.fixture = fixture

        if data_file is None:
            data_file = self._get_data_file_from_config()
        self.data_file = data_file
        log_msg = '*** RBAC DATA FILE: {0}'
        self.fixture.fixture_log.info(log_msg.format(data_file))
        self.users_list = 'Not set until build_role_data executes'

        self.roles = self.build_role_data(data_file=self.data_file)

    def build_role_data(self, data_file):
        """
        Reads and stores the data file.

        The format of the data file should be:
          + roles | <role1> | <role2> | ... |
          # COMMENTS (ignored)
          api_name | <code for role1> | <code for role2> | ...

        Blank lines are also ignored.

        Paramters:
            data_file: Path/Name of data file

        Return Value:
            Dictionary: key=api_name,
                        value=Dictionary(keys=<roles>, values=<response codes>)
        """
        with open(data_file, "r") as DATA:
            all_roles = DATA.readlines()

        roles = dict()
        for line in all_roles:
            # Skip any comments or short lines
            if line.startswith('#') or len(line) < 5:
                continue

            # Get the defined roles
            if line.startswith('+'):
                line = line.replace('+', '')
                data_columns = [x.strip().lower() for x in line.split('|')]
                self.users_list = data_columns[1:]
                continue

            # Process the data
            each_role = dict()
            data = [x.strip() for x in line.split("|")]
            for role, permission in zip(data_columns[1:], data[1:]):
                each_role[role] = int(permission)
            roles[data[0]] = each_role

        return roles

    def get_role_response_codes(self, api):
        """
        Return the dictionary of user/response codes corresponding
        to the specified API.

        Parameters:
            api - Name of API to get responses.
        Return Values:
            Dictionary for API. If API DNE, empty dictionary.
        """
        try:
            return self.roles[api]
        except KeyError:
            return dict()

    def get_api_name(self, test_prefix='test_rbac_'):
        """
        Determines caller, and parses out API name from caller name.
        (Assumes caller has desired API name in its name)

        Parameter: If the caller function has a prefix before the API name
        to be called.

        Return Value: String - Name of API
        """
        caller = 1
        function_name = 3
        api_function = inspect.stack()[caller][function_name]
        return api_function.replace(test_prefix, '')

    def validate_roles(self, roles, api, api_args=None, lb_id=None,
                       check_lb_active=False, delete_lb=False):
        """
        Loops through provided roles, invoking the client API, then
        checks actual response against expected response.

        Paramters:
            roles - Dictionary of key: role, value: response code.
            api - Name of client API to invoke
            api_args - Dictionary of keyword argument (and their values) to
                pass to the target API. If a list of dictionaries is passed,
                each tested role will use an element (=dictionary) of the list.
                (Role/api_list order cannot be maintained, since the roles are
                pulled from a dictionary).
            lb_id - The load balancer ID to validate against if checking
                status or deleting. (Used when creating or using an LB not
                created by the fixture).
            check_lb_active - If True, will wait until the LB status is ACTIVE
                before continueing.
            delete_lb - Add LB id to the fixture's list of LBs to delete.

        Return Value:
            List - list of errors encountered. If no errors were encountered,
               returns an empty list.
        """
        result_msg = "\n\n*** {0!s}: Expected: '{1!s}'  Actual: '{2!s}' *** \n"
        err_msg = "{0!s}: Expected: '{1!s}'  Actual: '{2!s}'"
        test_start = "\n\n\n<==== START TESTING ROLE: {0} ====>\n\n"
        test_end = "\n\n\n<==== END TESTING ROLE: {0} ====>\n\n"
        error_msgs = list()
        role_idx = 0
        log = self.fixture.fixture_log

        if lb_id is None:
            log.info('Defaulting to rbac_lb id')
            lb_id = self.fixture.rbac_lb.id

        if api_args is None:
            api_args = dict()

        if isinstance(api_args, list):
            args_list = api_args
        else:
            args_list = list()

        # Test each role specified
        for role, status in roles.iteritems():
            self.fixture.fixture_log.info(test_start.format(role.upper()))

            if args_list:
                api_args = args_list[role_idx]
                role_idx += 1

            # Call target API with provided arguments, store error if
            # response code does not match.

            client = getattr(self.fixture, role)
            if client is None:
                msg = "CLIENT object is NONE for '{0}'"
                log.error(msg.format(role))
                error_msgs.append(msg.format(role))
                continue

            response = getattr(client, api)(**api_args)
            self.fixture.fixture_log.info(
                result_msg.format(role.upper(), status, response.status_code))
            if int(response.status_code) != status:
                error_msgs.append(err_msg.format(role.upper(), status,
                                                 response.status_code))
            if check_lb_active:
                self.fixture.lbaas_provider.wait_for_status(lb_id)

            if delete_lb:
                self.fixture.lbs_to_delete.append(lb_id)

            self.fixture.fixture_log.info(test_end.format(role.upper()))

        return error_msgs

    def _get_data_file_from_config(self):
        # Convert relative data file path to correct OS nomenclature
        data_filename = self.fixture.config.lbaas_api.rbac_roles_data_file
        data_filename = os.sep.join(data_filename.split('/'))

        # Get the base CCAFE directory
        config_path = os.environ[self.CLOUD_CAFE_TEST_CONFIG_ENV_VAR]
        path_parts = config_path.split(os.sep)
        base_ccafe_dir = os.sep.join(path_parts[:len(path_parts) - 3])

        # Return the location of the data file
        return os.sep.join([base_ccafe_dir, data_filename])

from testrepo.common.testfixtures.core import CoreFixture
from ccengine.common.decorators import attr


class TestCtkapiSchema(CoreFixture):
    """
    This contains all the test verification on CTKAPI Schema(
    number of modules available, number of classes on each module,
    number of methods available in each class
    """
    @classmethod
    def setUpClass(cls):
        super(TestCtkapiSchema, cls).setUpClass()

    @attr(type='smoke')
    def test_the_modules_available_for_ctkapi(self):
        """
        @summary : Verify the number of modules available in CTKAPI
        - In future the value might change
        """
        response = self.core_client.get_module_details()
        expected_modules = 28
        self.assertTrue(len(response.entity) == expected_modules,
                        "Numbers of modules got changed.")

    @attr(type='regression')
    def test_class_available_for_account_module(self):
        """
        @summary : Verify the classes available in CTKAPI Account Module
        """
        module = "Account"
        response = self.core_client.get_class_details(module)
        expected_classes = ["Account", "AccountAttributeDBAServices",
                            "AccountDomainInfo", "AccountFlag",
                            "AccountParserHandler", "AccountServiceLevelUpdates",
                            "AssignmentRotation", "CloudAccount",
                            "CustomerAccountContact", "CustomerRole",
                            "CustomerType", "HighProfile", "MarketSector",
                            "MonitoringURL", "MonitoringURLLog",
                            "MonitoringURLType", "Network", "Product", "Region",
                            "Role", "SECCompanyType", "SegmentContacts",
                            "SegmentMemberRole", "ServiceLevel", "Status",
                            "SupportTerritory", "Team", "TeamLog",
                            "TeamMemberRole", "TeamRole", "TextFieldType",
                            "Type", "TypedTextField"]
        self.assertTrue(response.entity == expected_classes,
                        "Numbers of classes on Account module got changed")

    @attr(type='regression')
    def test_class_available_for_contact_module(self):
        """
        @summary: Verify the classes available in CTKAPI Contact Module
        """
        module = "Contact"
        response = self.core_client.get_class_details(module)
        expected_classes = ["Address", "Away", "Contact", "ContactPhoneType",
                            "Country", "CustomerPhone", "CustomerSecret",
                            "Department", "Email", "EmailType", "Org", "Phone",
                            "PhoneType", "Role", "Secret"]
        self.assertTrue(response.entity == expected_classes,
                        "Numbers of classes on Contact module got changed")

    @attr(type='regression')
    def test_class_available_for_ticket_module(self):
        """
        @summary: Verify the classes available in CTKAPI Ticket Module
        """
        module = "Ticket"
        response = self.core_client.get_class_details(module)
        expected_classes = ["Action", "ApprovalStatus", "Assignment",
                             "Category", "Classification", "CombinedLog",
                             "Difficulty", "Message", "NPSSurvey", "Priority",
                             "Product", "ProductSuite", "Queue", "QueueGroup",
                             "QueueRole", "Recipient", "RequiredApproval",
                             "Schedule", "Severity", "Sort", "Source",
                             "SphereOfSupport", "State", "Status", "StatusType",
                             "Subcategory", "Ticket", "TicketCloseableValue",
                             "TicketParserHandler", "TicketSurvey",
                             "TicketSurveyQuestion", "Work", "WorkCost",
                             "WorkType", "WorkUnit"]
        self.assertTrue(response.entity == expected_classes,
                        "Numbers of classes on Ticket module got changed")

    @attr(type='regression')
    def test_class_available_for_Computer_module(self):
        """
        @summary: Verify the classes available in CTKAPI Computer Module
        """
        module = "Computer"
        response = self.core_client.get_class_details(module)
        expected_classes = ["BuildError", "BuildErrorSevType", "BuildErrorType",
                             "ClientToSite", "ClientToSiteLog", "ClientToSiteUser",
                             "Computer", "ComputerCustomMonitor", "ComputerLog",
                             "ComputerOffline", "ComputerParserHandler",
                             "ComputerPasswordViewLog", "CustomMonitor",
                             "DASISCSIConfig", "DASMonitoringServer", "DRACInfo",
                             "DedicatedSanRaidLevel", "DisasterRecoveryInfo",
                             "DiskGroup", "DiskType", "DriveConfig",
                             "HostISCSIConfig", "HotSpares", "IdentityHostname",
                             "LeasedLineCarrier", "LeasedLineMedium",
                             "ManagedStorage", "MethodPasswordRequest",
                             "NetworkInterface", "Part", "Platform",
                             "PlatformLog", "PlatformLogType", "RPACluster",
                             "SSHKeyPair", "SSHKeyPairLog", "ServerACL",
                             "ServerLink", "ServerLinkType", "ServerMigration",
                             "ServerRelabel", "ServerService", "SharedStorage",
                             "SiteToSite", "SiteToSiteLog", "SiteToSitePhase",
                             "SiteToSiteTraffic", "Status", "StatusGroup",
                             "StatusLog", "StorageDAS", "StorageDASDiskGroup",
                             "StorageDASRaidLevel", "UsageType"]
        self.assertTrue(response.entity == expected_classes,
                        "Numbers of classes on Ticket module got changed")

    @attr(type='regression')
    def test_class_available_for_Contract_module(self):
        """
        @summary: Verify the classes available in CTKAPI Contract Module
        """
        module = "Contract"
        response = self.core_client.get_class_details(module)
        expected_classes = ["Contract", "ContractModRequest", "ContractNote",
                            "ContractRenewal", "MasterTicket", "MasterTicketStep",
                            "MasterTicketStepType", "ServerPrice", "Work",
                            "WorkType"]
        self.assertTrue(response.entity == expected_classes,
                        "Numbers of classes on Ticket module got changed")

    @attr(type='regression')
    def test_methods_available_for_account_account(self):
        """
        @summary: Verify the number of methods available in Account.Account class
        """
        module = "Account"
        class_name = "Account"
        response = self.core_client.get_methods_in_a_class(module, class_name)
        expected_methods = 3
        self.assertTrue(len(response.entity) == expected_methods, "message")

    @attr(type='regression')
    def test_methods_available_for_computer_computer(self):
        """
        @summary: Verify the number of methods available in Computer.Computer class
        """
        module = "Computer"
        class_name = "Computer"
        response = self.core_client.get_methods_in_a_class(module, class_name)
        expected_methods = 18
        self.assertTrue(len(response.entity) == expected_methods, "message")

    @attr(type='regression')
    def test_methods_available_for_computer_part(self):
        """
        @summary: Verify the number of methods available in Computer.Part class
        """
        module = "Computer"
        class_name = "Part"
        response = self.core_client.get_methods_in_a_class(module, class_name)
        expected_methods = 3
        self.assertTrue(len(response.entity) == expected_methods, "message")

    @attr(type='regression')
    def test_methods_available_for_contract_contract(self):
        """
        @summary: Verify the number of methods available in Contract.Contract class
        """
        module = "Contract"
        class_name = "Contract"
        response = self.core_client.get_methods_in_a_class(module, class_name)
        expected_methods = 3
        self.assertTrue(len(response.entity) == expected_methods, "message")

    @attr(type='regression')
    def test_methods_available_for_network_zone(self):
        """
        @summary: Verify the number of methods available in Network.Zone class
        """
        module = "Network"
        class_name = "Zone"
        response = self.core_client.get_methods_in_a_class(module, class_name)
        expected_methods = 2
        self.assertTrue(len(response.entity) == expected_methods, "message")

    @attr(type='regression')
    def test_methods_available_for_ticket_queue(self):
        """
        @summary: Verify the number of methods available in Ticket.Queue class
        """
        module = "Ticket"
        class_name = "Queue"
        response = self.core_client.get_methods_in_a_class(module, class_name)
        expected_methods = 3
        self.assertTrue(len(response.entity) == expected_methods, "message")

    @attr(type='regression')
    def test_methods_available_for_ticket_ticket(self):
        """
        @summary: Verify the number of methods available in Ticket.Ticket class
        """
        module = "Ticket"
        class_name = "Ticket"
        response = self.core_client.get_methods_in_a_class(module, class_name)
        expected_methods = 6
        self.assertTrue(len(response.entity) == expected_methods, "message")

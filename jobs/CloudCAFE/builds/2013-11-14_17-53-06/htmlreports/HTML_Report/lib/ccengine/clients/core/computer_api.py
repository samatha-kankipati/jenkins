from ccengine.clients.core.core_api import CoreAPIClient


class ComputerAPIClient(CoreAPIClient):
    """
    Client for Computer related queries in CTK API
    """
    def __init__(self, url, auth_token, serialize_format=None,
                 deserialize_format=None):
        super(ComputerAPIClient, self).__init__(url, auth_token,
                                                serialize_format,
                                                deserialize_format)
        self.class_name = "Computer.Computer"

    def get_computer_details(self, computer, attributes):
        '''
        @summary: Get Computer Details
        @param computer: Computer ID
        @type computer: String
        @param attributes: Attribute Details
        @type attributes: List or Dictionary
        '''
        response = self.query(class_name=self.class_name,
                              load_arg=computer,
                              attributes=attributes)
        return response

    def update_computer(self, computer, attribute_name, attribute_value):
        '''
        @summary: Update Computer's Attributes
        @param computer: Computer ID
        @type computer: String
        @param attributeName: The name of the Attribute
        @type attributeName: string
        @param attributeValue: The value of the attribute to be set
        @type attributeValue: The type of the attribute as attributeName
        @return: List with update status and server id
        @rtype: List
        '''
        response = self.set_attribute(class_name=self.class_name,
                                      load_arg=computer,
                                      attribute_name=attribute_name,
                                      attribute_value=attribute_value)
        return response

    def add_aggexnet_vlan(self, computer, vlan=None):
        """
        @summary: Adds an AggExNet Zone to a server.
        @param computer: Computer Id
        @type computer: Integer
        @param vlan: Vlan zone
        @type vlan: String
        @rtype: Boolean
        """
        load_arg = computer
        args = [vlan]
        response = self.query(load_arg=load_arg,
                              class_name=self.class_name,
                              method="addAggExNetVlan",
                              args=args)
        return response

    def add_das_disk_group(
            self, computer, disk_group_id, raid_level, disk_count, disk_size):
        """
        @summary: Add a DAS Disk Group to this device.
        @param computer: Computer Id
        @type computer: Integer
        @param disk_group_id:DAS Disk Group Id
        @type disk_group:String
        @param raid_level: RAID Level
        @type raid_level: String
        @param disk_count: Disk Count
        @type disk_count: String
        @param disk_size: Disk Size
        @type disk_size: String
        @rtype: Returns CTKAPI external class
        """
        load_arg = computer
        args = [disk_group_id, raid_level, disk_count, disk_size]
        response = self.query(load_arg=load_arg,
                              class_name=self.class_name,
                              method="addDASDiskGroup",
                              args=args)
        return response

    def add_das_iscsi_conf(self, computer, ip_address, das_switch_port,
                           das_port, das_iqn, vlan_id):
        """
        @summary: Add a DAS ISCSI config to this device
        @param computer: Computer Id
        @type computer: Integer
        @param ip_address:IP Address
        @type ip_address:String
        @param das_switch_port: DAS Switch Port
        @type das_switch_port: String
        @param das_port: DAS port
        @type das_port: String
        @param das_iqn: DAS IQN
        @type das_iqn: String
        @param vlan_id: VLAN Id
        @type vlan_id: String
        @rtype: Returns CTKAPI external class
        """
        load_arg = computer
        args = [ip_address, das_switch_port, das_port, das_iqn, vlan_id]
        response = self.query(load_arg=load_arg,
                              class_name=self.class_name,
                              method="addDASISCSIConf",
                              args=args)
        return response

    def add_dedicated_san(self, computer, lun_id, raid_level, mount_point,
                          hlu, disk_type, capacity, hosts, storage_array):
        """
        @summary: Add a dedicated san / Aggregate Product Storage
        @param computer: Computer Id
        @type computer: Integer
        @param lun_id:LUN ID
        @type lun_id:Int
        @param raid_level: RAID level
        @type raid_level: String
        @param mount_point: Mount Point
        @type mount_point: String
        @param hlu:hlu
        @type hlu:Int
        @param disk_type: Disk Type
        @type disk_type: String
        @param capacity: Capacity
        @type capacity: Float
        @param hosts:Hosts
        @type hosts:String
        @param storage_array:Storage Array
        @type storage_array:String
        @rtype: CTK object
        """
        load_arg = computer
        args = [lun_id, raid_level, mount_point, hlu, disk_type, capacity,
                hosts, storage_array]
        response = self.query(load_arg=load_arg,
                              class_name=self.class_name,
                              method="addDedicatedSan",
                              args=args)
        return response

    def add_hot_spare(self, computer, quantity, slot, size):
        """
        @summary: Add a hot spare to this device
        @param computer: Computer Id
        @type computer: Integer
        @param quantity:Quantity
        @type quantity:Int
        @param slot: Slot
        @type slot: String
        @param size: Size
        @type size: String
        """
        load_arg = computer
        args = [quantity, slot, size]
        response = self.query(load_arg=load_arg,
                              class_name=self.class_name,
                              method="addHotSpare",
                              args=args)
        return response

    def add_host_iscsi_conf(self, computer, ip_address, host, port,
                            host_iqn, pci_slot):
        """
        @summary: Add a Host ISCSI config to this device
        @param computer: Computer Id
        @type computer: Integer
        @param ip_address:IP address
        @type ip_address:String
        @param host: Host
        @type host: String
        @param port: Port
        @type port: String
        @param host_iqn:Host IQN
        @type host_iqn:String
        @param pci_slot: PCI Slot
        @type pci_slot: String
        @rtype: CTKAPI external class
        """
        load_arg = computer
        args = [ip_address, host, port, host_iqn, pci_slot]
        response = self.query(load_arg=load_arg,
                              class_name=self.class_name,
                              method="addHostISCSIConf",
                              args=args)
        return response

    def add_rpa_cluster_config(self, computer, target_lun_id, source_lun_id,
                               raid_level, mount_point, hlu, disk_type,
                               capacity, hosts, storage_array):
        """
        @summary: Add a Host ISCSI config to this device
        @param computer: Computer Id
        @type computer: Integer
        @param target_lun_id:LUN ID
        @type target_lun_id:Int
        @param source_lun_id: Source lun id
        @type source_lun_id: Int
        @param raid_level: RAID Level
        @type raid_level: String
        @param mount_point: Mount Point
        @type mount_point: String
        @param hlu:hlu
        @type hlu:Int
        @param disk_type: Disk Type
        @type disk_type: String
        @param capacity: Capacity
        @type capacity: Float
        @param hosts:Hosts
        @type hosts:String
        @param storage_array:Storage Array
        @type storage_array:String
        """
        load_arg = computer
        args = [target_lun_id, source_lun_id, raid_level,
                mount_point, hlu, disk_type, capacity, hosts, storage_array]
        response = self.query(load_arg=load_arg,
                              class_name=self.class_name,
                              method="addRPAClusterConfig",
                              args=args)
        return response

    def add_replace_part(self, computer, sku, skunit):
        """
        @summary: If there already is a sku with the skunit given
        (checks for skunit.name and skunit.mapping)- this will replace it,
        otherwise just adds the sku
        @param computer: Computer Id
        @type computer: Integer
        @param sku:LUN ID
        @type sku:Int
        @param skunit: skunit
        @type skunit: String
        """
        load_arg = computer
        args = [sku, skunit]
        response = self.query(load_arg=load_arg,
                              class_name=self.class_name,
                              method="addReplacePart",
                              args=args)
        return response

    def add_managed_storage(self, computer, lun_id, uuid, raid_level,
                            storage_group_name, storage_array, purpose,
                            host_name, capacity):
        """
        @summary:Adds Managed Storage for Device
        @param computer: Computer Id
        @type computer: Integer
        @param lun_id:Lun ID
        @type lun_id:String
        @param uuid: Reason
        @type uuid: String
        @param raid_level: RAID level
        @type raid_level: String
        @param storage_group_name:Storage Group Name
        @type storage_group_name:Int
        @param storage_array:Storage Array
        @type storage_array: String
        @param purpose: Purpose
        @type purpose: String
        @param host_name:host name
        @type host_name:String
        @param capacity:capacity
        @type capacity:Float
        """
        load_arg = computer
        args = [lun_id, uuid, raid_level, storage_group_name, storage_array,
                purpose, host_name, capacity]
        response = self.query(load_arg=load_arg,
                              class_name=self.class_name,
                              method="addManagedStorage",
                              args=args)
        return response

    def change_status(self, computer, new_status, reason=None, ticket_num=None,
                      migr_days=None, new_migr_server=None,
                      offline_reason=None, old_mrr=None, new_mrr=None,
                      mrr_currency=None, contract_id=None,
                      included_bandwidth=None):
        """
        @summary: Changes status for device, all activator rules are activated.
        @param computer: Computer Id
        @type computer: Integer
        @param new_status:New Status
        @type new_status:String
        @param reason: Reason
        @type reason: String
        @param ticket_num: Ticket Number
        @type ticket_num: String
        @param migr_days:migr days
        @type migr_days:Int
        @param new_migr_server:New MigrServer
        @type new_migr_server: String
        @param offline_reason: Offline Reason
        @type offline_reason: String
        @param old_mrr:old mrr
        @type old_mrr:String
        @param new_mrr:New MRR
        @type new_mrr:String
        @param mrr_currency:MRR Currency
        @type mrr_currency:String
        """
        load_arg = computer
        args = [new_status]
        keyword_args = {"reason": reason, "contract_id": contract_id,
                        "included_bandwidth": included_bandwidth,
                        "ticket_num": ticket_num,
                        "migr_days": migr_days,
                        "new_migr_server": new_migr_server,
                        "offline_reason": offline_reason,
                        "old_mrr": old_mrr,
                        "new_mrr": new_mrr,
                        "mrr_currency": mrr_currency}
        response = self.query(load_arg=load_arg,
                              class_name=self.class_name,
                              method="changeStatus",
                              args=args,
                              keyword_args=keyword_args)
        return response

    def clone(self, computer, name=None, account=None, datacenter=None):
        """
        @summary: Copy all of this server's attributes to a new computer object
        @param computer: Computer Id
        @type computer: Integer
        @param account:Account
        @type account:String
        @param datacenter: DataCenter
        @type datacenter:String
        """
        load_arg = computer
        args = [name, account, datacenter]
        response = self.query(load_arg=load_arg,
                              class_name=self.class_name,
                              method="clone",
                              args=args)
        return response

    def get_networks(self, computer):
        """
        @summary: Returns a dictionary object providing the vlan, ip,
        and network for each type of network associated with this device.
        @param computer: Computer Id
        @type computer: Integer
        @return: Network details of a server
        @rtype: Dictionary
        """
        load_arg = computer
        response = self.query(load_arg=load_arg,
                              class_name=self.class_name,
                              method="getNetworks",
                              args=[]
                              )
        return response

    def get_skus_and_labels(self, computer):
        """
        @summary: Returns a list of 4-tuples containing:
        (SKU, label, display_label, description)
        for this computer's parts. For convenience, the list will be sorted by
        SKU number.
        @param computer: Computer Id
        @type computer: Integer
        @return: List of SKUs of a computer
        @rtype: List
        """
        load_arg = computer
        response = self.query(load_arg=load_arg,
                              class_name=self.class_name,
                              method="getSKUsAndLabels",
                              args=[]
                              )
        return response

    def get_valid_skus_and_labels(self, computer):
        """
        @summary: Returns a list of skunits, and a list of skus for
        each skunit and information about each one.
        @param computer: Computer Id
        @type computer: Integer
        @return: List of SKU units of a computer
        @rtype: List
        """
        load_arg = computer
        response = self.query(load_arg=load_arg,
                              class_name=self.class_name,
                              method="getValidSkunitsAndSkus",
                              )
        return response

    def remove_managed_storage(self, computer, ms):
        """
        @summary: Remove the managed storage object from this computer
        @param computer: Computer Id
        @type computer: Integer
        @param ms: Managed Storage
        @type ms: String
        """
        load_arg = computer
        response = self.query(load_arg=load_arg,
                              class_name=self.class_name,
                              method="removeManagedStorage",
                              )
        return response

    def remove_part(self, computer, skunit_name, product=None):
        """
        @summary: ServerParts are unique in sku/computer_number/label
        combinations.This handles things like multiple harddrives of the
        same sku attached to a computer.
        If removed a part- will return the part- else None
        @param computer: Computer Id
        @type computer: Integer
        @param skunit_name: SKUnit Name
        @type skunit_name: String
        @param product: Product
        @type product:String
        """
        load_arg = computer
        args = [skunit_name, product]
        response = self.query(load_arg=load_arg,
                              class_name=self.class_name,
                              method="removePart",
                              args=args)
        return response

    def status_change_notice(self, computer, new_status):
        """
        @summary: given a new status send off the right ticket
        @param computer: Computer Id
        @type computer: Integer
        @param new_status: Status Name
        @type new_status: String
        """
        load_arg = computer
        args = [new_status]
        response = self.query(load_arg=load_arg,
                              class_name=self.class_name,
                              method="statusChangeNotice",
                              args=args)
        return response

    def virtual_machine_on_off(self, computer, new_status, send_notice=True,
                               suspended_if_vm_inactive=0):
        """
        @summary: This will change the status and attempt to turn the
        vm off or on via the VCC. Depending on the success on that it will
        either suspend or wait_suspend the status.
        @param computer:Computer Id
        @type computer:Integer
        @param new_status:Status Name
        @type new_status:String
        @param send_notice:Send Notice
        @type send_notice:String
        @param suspend_if_vm_inactive: Suspend key
        @type suspend_if_vm_inactive:Boolean
        """
        load_arg = computer
        args = [new_status, send_notice, suspended_if_vm_inactive]
        response = self.query(load_arg=load_arg,
                              class_name=self.class_name,
                              method="virtualMachineOnOff",
                              args=args)
        return response

    def get_computer_status_details(self):
        """
        @summary: Get all the statuses available in the computer.status
        value table
        @return: List of Computer status with status id
        @rtype: List of list
        """
        class_name = "Computer.Status"
        response = self.get_values(class_name)
        return response

    def get_computer_attribute(self, load_value, attribute=None):
        """
        @summary: Get Attribute value of an Computer module
        @param attributes: Attribute name of Computer module
        @type attributes: string
        @param load_value: id of a computer
        @type load_value: integer
        @return: attribute value
        @rtype: List/String
        """
        if attribute is None:
            attribute = ["account"]
        response = self.get_attribute(class_name=self.class_name,
                                      load_value=load_value,
                                      attribute=attribute)
        return response

    def set_sales_rep(self, computer, employee_num):
        """
        @summary: It sets the sales representative details for a given computer,
        otherwise gives valid exception with error message
        @param computer: Computer Id
        @type computer: Integer
        @param employee_num: employee_num
        @type employee_num:Integer
        @return: Success status
        @rtype: Boolean
        """
        load_arg = computer
        args = [employee_num]
        response = self.query(load_arg=load_arg,
                              class_name=self.class_name,
                              method="setSalesRep",
                              args=args)
        return response

    def get_computer_attributes_using_computerwhere(
            self, where_conditions, attribute=None, limit=None, offset=None):
        """
        @summary: Get Attributes of an Computer
        @param where_conditions: Values of where conditions
        @type where_conditions: List
        @param attribute: Attribute of CTK Objects
        @type attributes: List or dictionary of attribute name-value pairs
        @param limit: Effective limit on returned query
        @type limit: integer
        @param offset: Effective offset of returned query
        @type offset: integer
        @return: Given computer attributes
        @rtype: String/List
        """
        if attribute is None:
            attribute = ["number"]
        response = self.list(class_name=self.class_name,
                             where_class="Computer.ComputerWhere",
                             where_conditions=where_conditions,
                             attributes=attribute,
                             limit=limit, offset=offset)
        return response

    def add_attribute(
            self, server_parts_id, attr_id, val, part_derived_from=None):
        """
        @summary: Add attribute to computer part
        @param server_parts_id: Id of part
        @type server_parts_id: Integer
        @param attr_id: attibute id of a part
        @type attr_id: integer
        @param val: val
        @type val: string
        @param part_derived_from: computer part it is derived from
        @type part_derived_from:  Integer
        """
        class_name = "Computer.Part"
        load_arg = server_parts_id
        args = [attr_id, val, part_derived_from]
        response = self.query(load_arg=load_arg,
                              class_name=class_name,
                              method="addAttribute",
                              args=args)
        return response

    def remove_attribute(self, server_parts_id, attr_id, value=None):
        """
        @summary: remove attribute from computer part
        @param server_parts_id: Id of part
        @type server_parts_id: Integer
        @param attr_id: attibute id of a part
        @type attr_id: integer
        @param val: val
        @type val: string
        """
        class_name = "Computer.Part"
        load_arg = server_parts_id
        args = [attr_id, value]
        response = self.query(load_arg=load_arg,
                              class_name=class_name,
                              method="removeAttribute",
                              args=args)
        return response

    def get_computeroffline_attributes_using_computerofflinewhere(
            self, where_conditions, attribute=None, limit=None, offset=None):
        """
        @summary: Get Attributes of an Computer
        @param where_conditions: Values of where conditions
        @type where_conditions: Array
        @param attribute: Attribute of Computer.Computer class
        @type attribute: List or dictionary of attribute name-value pairs
        @param limit: Effective limit on returned query
        @type limit: integer
        @param offset: Effective offset of returned query
        @type offset: integer
        """
        if attribute is None:
            attribute = ["number"]
        response = self.list(class_name=self.class_name,
                             where_class="Computer.ComputerOfflineWhere",
                             where_conditions=where_conditions,
                             attributes=attribute,
                             limit=limit, offset=offset)
        return response

    def get_managedstorage_attribute(self, load_value, attribute=None):
        """
        @summary: Get Attribute value of an Computer module
        @param attributes: Attribute name of Computer module
        @type attributes: string
        @param load_value: id of a computer
        @type load_value: integer
        """
        if attribute is None:
            attribute = ["storage_group_name"]
        response = self.get_attribute(class_name="Computer.ManagedStorage",
                                      load_value=load_value,
                                      attribute=attribute)
        return response

'''
@summary: Classes and Utilities that provide low level connectivity to the Nova Command Line Client
@note: Should be consumed/exposed by a L{ccengine.persisters}, a L{ccengine.clients} or a L{ccengine.common.connectors} class, 
should rarely be used directly by any other object or process 
@copyright: Copyright (c) 2012 Rackspace US, Inc.
'''
from ccengine.common.reporting.prettytable import PrettyTable
from ccengine.domain.base_domain import BaseDomain

'''
======================================================
            NAMESPACE CONSTANTS
======================================================
@todo: Remove the HACK of hardcoding config values
'''
SEPARATOR = "~"   # Used to parse nova client output

class NovaShellResponse(PrettyTable):
    '''
    @summary: Base class for any Nova Client Reponse
    @ivar CLIResponse: The original Nova Client Response
    @type CLIResponse: C{BaseCLIResponse}   
    @ivar IsError: True if this Response is a Nova Error
    @type IsError: C{bool}   
    @note: This class is dependent on a local installation of the Nova client process.
    '''
    def __init__(self, cli_response):
        '''
        @param cli_response: CLI Response from the L{novashellProvider} __send()
        @type cli_response: L{BaseCLIResponse}  
        '''
        self.IsError = False
        self.IsEmpty = False
        self.CLIResponse = cli_response
        try:
            if (cli_response.ReturnCode != 0):
                ''' This was a legit error of some kind '''
                self.IsError = True
                PrettyTable.__init__(self, fields=["NOVA EXCEPTION"])
            elif (len(cli_response.StandardOut) <= 0):
                ''' This is an empty response, many nova client create commands actually return nothing '''
                self.IsEmpty = True
                PrettyTable.__init__(self, fields=[])
            elif (("usage" in cli_response.StandardOut[0].split("~")[0])):
                ''' This was considered a bad NOVA command '''
                self.IsError = True
                self.CLIResponse.StandardOut = "ERROR: Un-supported Nova command.\n%s" % cli_response.StandardOut
                PrettyTable.__init__(self, fields=["NOVA EXCEPTION"])
            elif (len(cli_response.StandardOut[0].split("~")) <= 1 and ("ERROR" not in cli_response.StandardOut[0].split("~")[0])):
                ''' This is another permutation on the empty response '''
                self.IsEmpty = True
                PrettyTable.__init__(self, fields=[])
            elif (len(cli_response.StandardOut[0].split("~")) <= 1 and ("ERROR" in cli_response.StandardOut[0].split("~")[0])):
                ''' This is an error from NOVA '''
                self.IsError = True
                PrettyTable.__init__(self, fields=["NOVA EXCEPTION"])
            else:    
                PrettyTable.__init__(self, fields=cli_response.StandardOut[0].split("~"))
        except Exception, parse_exception:
                self.IsError = True
                self.CLIResponse.StandardOut = parse_exception
                PrettyTable.__init__(self, fields=["NOVA EXCEPTION"])
            
        ''' Run the initial load of this response object '''
        self.__load__()
        return

    def __load__(self):
        '''
        @summary: Builds this response from the internal bare_response
        @rtype: None
        '''
        try:
            if (len(self.fields) > 0):
#                for line in self.CLIResponse.StandardOut.splitlines():
                for line in self.CLIResponse.StandardOut:
                    if (line.split(SEPARATOR) != self.fields):
                        self.add_row(line.split(SEPARATOR))
        except Exception, load_exception:
            self.fields = []
            self.fields = ["NOVA EXCEPTION"] 
            self.set_fields(self.fields)
            self.widths = []
            self.aligns = []
            self.set_padding_width(1)
            self.rows = []
            self.cache = {}
            self.html_cache = {}
            self.add_row(load_exception)
        return
    
    def get_column(self, field_name):
        '''
        @summary: Pulls an entire column's data
        @param field_name: Name of the column 
        @type field_name: C{str}
        @return: List of all values for the column field_name  
        @rtype: C{list}
        '''
        fieldIndex = self.fields.index(field_name.replace(' ', ''))
        returnColumn = []
        
        if fieldIndex > -1:
            for row in self.rows:
                returnColumn.append(row[fieldIndex])
        return returnColumn
        
    def yield_rows(self):
        '''
        @summary: Allows iteration through rows with a generator
        @return: Dictionary with Columns as keys  
        @rtype: C{dict}
        '''        
        for x in range(0, len(self.rows)):
            yield (dict(zip(self.fields, self.rows[x])))
    
    def get_row(self, row_number):
        '''
        @summary: Pulls a specific row
        @param row_number: Number of the row. Between 0 and n. 
        @type row_number: C{str}
        @todo: random.choice can not be used because of novaResponse.rows format
        @return: Dictionary with Columns as keys  
        @rtype: C{dict}
        '''
        if 0 <= row_number < len(self.rows):
            return dict(zip(self.fields, self.rows[row_number]))
        else:
            return dict(zip(self.fields, []))
                
    def find_row(self, field_name, field_value, contains_match=False):
        '''
        @summary: Finds a specific row based on a cell value 
        @param field_name: Name of the column 
        @type field_name: C{str}
        @param field_value: Value of the field  
        @type field_value: C{str}
        @param contains_match: return first match containing field_value
        @type contains_match: C{bool}
        @return: Dictionary with Columns as keys  
        @rtype: C{dict}
        '''
        searchColumn = self.get_column(field_name.replace(' ', ''))
        returnRow = {}

        try:
            ''' @todo: find_row COULD fail if searching for a duplicate value within a row '''
            if not contains_match:
                returnRow = self.get_row(searchColumn.index(field_value))
            else:
                for i, col in enumerate(searchColumn):
                    if field_value in col:
                        returnRow = self.get_row(i)
                        break
        except Exception:
            pass
            '''
            These are not the droids you were looking for...
            Move along.
            '''
        return returnRow

class ServerDomainObject(BaseDomain):
    '''
        @summary: Represents a Nova Shell Server
        @note: admin_password may be added dynamically when creating a server in NovaShellProvider
    '''
    __attrs__ = ['Status',
                 'Networks',
                 'ID',
                 'Name',
                 'admin_password']

class VolumeTypeDomainObject(BaseDomain):
    '''
        @summary: Represents a Nova Shell Volume Type
    '''
    __attrs__ = ['ID', 'Name']

class ImageDomainObject(BaseDomain):
    '''
        @summary: Represents a Nova Shell Image
    '''
    __attrs__ = ['ID',
                 'Name',
                 'Status',
                 'Server']


class FlavorDomainObject(BaseDomain):
    '''
        @summary: Represents a Nova Shell Flavor
    '''
    __attrs__ = ['ID',
                 'Name',
                 'Memory_MB',
                 'Disk',
                 'Ephemeral',
                 'Swap',
                 'VCPUs',
                 'RXTX_Factor']
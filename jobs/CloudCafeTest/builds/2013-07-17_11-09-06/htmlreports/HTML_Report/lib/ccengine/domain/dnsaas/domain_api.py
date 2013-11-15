#from ccengine.domain.base_domain import BaseMarshallingDomain
#from ccengine.domain.base_domain import BaseDomain
#import xml.etree.ElementTree as ET
#import json
#
#
#class Domain(BaseMarshallingDomain):
#   
#    
#    
#    def __init__(self, name=None, emailAddress=None, ttl=None,
#                comment=None, recordsList=None, records=None,
#                subdomains=None):
#        
#        #Common Attributes
#        self.name = name
#        self.emailAddress = emailAddress
#        self.ttl = ttl 
#        self.comment = comment
#        self.recordsList = recordsList
#        self.subdomains = subdomains
#     
#        
#
#         
#    #Request Generators
#    def _obj_to_json(self):
#        domain = {  
#              "name" : self.name,
#              "ttl" : self.ttl,
#              "emailAddress" : self.emailAddress }
#        if self.recordsList is not None:
#            domain['recordsList'] = self.recordsList
#        body = {'domains':[domain]}
#        return json.dumps(body)
#        
#    def _obj_to_xml(self):
#        pass
#    
#    #Response Deserializers
#    @classmethod
#    def _json_to_obj(cls, serialized_str):
#        pass
#    
#    #Response Deserializers
#    @classmethod
#    def _xml_to_obj(cls, serialized_str):
#        pass
#                
#         
                
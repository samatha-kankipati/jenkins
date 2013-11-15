__author__ = 'ram5454'
from ccengine.domain.base_domain import BaseMarshallingDomain
import json

class ContactInfo(BaseMarshallingDomain):
    def __init__(self, firstName=None, lastName=None, email=None,
                 phoneNumber=None, street=None,
                 city=None, state=None, zip=None,
                 country=None):

        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.phoneNumber = phoneNumber
        self.street = street
        self.city = city
        self.state = state
        self.zip = zip
        self.country = country


        '''
        #Response-only attributes
        self.id = volume_id
        self.attachments = attachments
        self.created_at = created_at
        self.status = status
        '''

    #Response Deserialize
    @classmethod
    def _json_to_obj(cls, serialized_str):


        j = json.loads(serialized_str)
        #firstName = j['accounts'][0]['PrimaryContactInfo']['firstName']
        firstName = j['PrimaryContactInfo']['firstName']
        lastName = j['PrimaryContactInfo']['lastName']
        email = j['PrimaryContactInfo']['email']
        phoneNumber = j['PrimaryContactInfo']['phoneNumber']
        street = j['PrimaryContactInfo']['street']
        city = j['PrimaryContactInfo']['city']
        state = j['PrimaryContactInfo']['state']
        zip = j['PrimaryContactInfo']['zip']
        country = j['PrimaryContactInfo']['country']

        return ContactInfo(firstName,lastName,email,phoneNumber,street,city,state,zip,country)


class UkDefectionResponse(BaseMarshallingDomain):

    def __init__(self, accountId=None, defectionIndex=None, behaviorValue=None,
                 noUsageValue=None, sliceValue=None,
                 tenureValue=None):

        self.accountId = accountId
        self.defectionIndex = defectionIndex
        self.behaviorValue = behaviorValue
        self.noUsageValue = noUsageValue
        self.sliceValue = sliceValue
        self.tenureValue = tenureValue


    @classmethod
    def _json_to_obj(cls, serialized_str):


        j = json.loads(serialized_str)
        accountId = j['indices'][0]['accountId']
        defectionIndex = j['indices'][0]['defectionIndex']
        behaviorValue = j['indices'][0]['behaviorValue']
        noUsageValue = j['indices'][0]['noUsageValue']
        sliceValue = j['indices'][0]['sliceValue']
        tenureValue = j['indices'][0]['tenureValue']

        return UkDefectionResponse(accountId, defectionIndex, behaviorValue, noUsageValue, sliceValue, tenureValue)

class UsDefectionResponse(BaseMarshallingDomain):

    def __init__(self, accountId=None, defectionIndex=None, behaviorValue=None,
                 noUsageValue=None, sliceValue=None,
                 tenureValue=None):

        self.accountId = accountId
        self.defectionIndex = defectionIndex
        self.behaviorValue = behaviorValue
        self.noUsageValue = noUsageValue
        self.sliceValue = sliceValue
        self.tenureValue = tenureValue


    @classmethod
    def _json_to_obj(cls, serialized_str):
        j = json.loads(serialized_str)
        accountId = j['indices'][0]['accountId']
        defectionIndex = j['indices'][0]['defectionIndex']
        behaviorValue = j['indices'][0]['behaviorValue']
        noUsageValue = j['indices'][0]['noUsageValue']
        sliceValue = j['indices'][0]['sliceValue']
        tenureValue = j['indices'][0]['tenureValue']

        return UsDefectionResponse(accountId, defectionIndex, behaviorValue, noUsageValue, sliceValue, tenureValue)

class UkDefectionResponse(BaseMarshallingDomain):

    def __init__(self, accountId=None, defectionIndex=None, behaviorValue=None,
                 noUsageValue=None, sliceValue=None,
                 tenureValue=None):

        self.accountId = accountId
        self.defectionIndex = defectionIndex
        self.behaviorValue = behaviorValue
        self.noUsageValue = noUsageValue
        self.sliceValue = sliceValue
        self.tenureValue = tenureValue


    @classmethod
    def _json_to_obj(cls, serialized_str):


        j = json.loads(serialized_str)
        accountId = j['indices'][0]['accountId']
        defectionIndex = j['indices'][0]['defectionIndex']
        behaviorValue = j['indices'][0]['behaviorValue']
        noUsageValue = j['indices'][0]['noUsageValue']
        sliceValue = j['indices'][0]['sliceValue']
        tenureValue = j['indices'][0]['tenureValue']

        return UkDefectionResponse(accountId, defectionIndex, behaviorValue, noUsageValue, sliceValue, tenureValue)

class DefectionRange(BaseMarshallingDomain):

    def __init__(self, accountId=None, defectionIndex=None):

        self.accountId = accountId
        self.defectionIndex = defectionIndex

    @classmethod
    def _json_to_obj(cls, serialized_str):

        j = json.loads(serialized_str)
        accountId = j['defectionIndices']['accountId']
        defectionIndex = j['defectionIndices']['defectionIndex']
        return DefectionRange(accountId, defectionIndex)

class PaginationByDate(BaseMarshallingDomain):

    def __init__(self, defectionIndex1=None, defectionIndexlast=None, accountId=None):

        self.defectionIndex1 = defectionIndex1
        self.defectionIndexlast = defectionIndexlast
        self.accountId = accountId

    @classmethod
    def _json_to_obj(cls, serialized_str):

        j = json.loads(serialized_str)
        length = len(j['indices'])
        defectionIndex1 = j['indices'][0]['defectionIndex']
        defectionIndexlast = j['indices'][length-1]['defectionIndex']
        accountId = j['indices'][0]['accountId']

        return PaginationByDate(defectionIndex1, defectionIndexlast, accountId)

class PaginationDateRange(BaseMarshallingDomain):

    def __init__(self, defectionIndex1=None, defectionIndexlast=None, accountId=None, ):

        self.defectionIndex1 = defectionIndex1
        self.defectionIndexlast = defectionIndexlast
        self.accountId = accountId

    @classmethod
    def _json_to_obj(cls, serialized_str):

        j = json.loads(serialized_str)
        length = len(j['indices'])
        defectionIndex1 = j['indices'][0]['defectionIndex']
        defectionIndexlast = j['indices'][length-1]['defectionIndex']
        accountId = j['indices'][0]['accountId']

        return PaginationDateRange(defectionIndex1, defectionIndexlast, accountId)
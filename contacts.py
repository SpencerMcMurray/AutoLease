#the variables set to string don't have to be neccesarily set to anything, treat them as empty variables
#cannot initialize empty variables in python
import base64
import random #for salt
import string
import requests
import json
import hashlib

'''
 * [the addContact function creates a public api user registration for an e-Transfer customer]
 * @param string access_token          [OAuth2 access token, the format is 'Bearer AccessToken']
 * @param string third_party_access_id [unique id that identifies a third party partner]
 * @param string request_id            [partner generated unique id for each request used for message tracking purposes]
 * @param string deviceId              [user device unique identifier]
 * @param string application_id        [user application unique identifier. This field is optional]
 * @param string api_registration_id   [unique identifier for the user api registration]
 * notification preferences (request body)
 * @param string contact_id            [unique identifier for the contact; not required in POST request]
 * @param string contact_name          [unique contact name to be provided for each contacts]
 * @param string contact_hash          [unique hash value to identify version of contact, not required in POST request]
 * @param string language              [language used to notify this contact. Values: en, fr]
 * @param string handle                [notification: handle can be an email address or a cellphone number]
 * @param string handle_type           [notification: email or sms]
 * @param boolean active               [notification: true or false]
'''
url2 = 'https://gateway-web.beta.interac.ca/publicapi/api/v2/'

def addContact(access_token, thirdPartyAccessId, requestId, deviceId, apiRegistrationId, emailID = 'string', contactName = 'string', application_id = 'string', api_registration_id = 'string', contact_id = 'string', contact_hash = 'string', language = 'en', handle = 'string', handle_type = 'string', active = True):

    dataPassed = {
        'contactId': "string",
        'contactName': contactName,
        'contactHash': "string",
        'language': "en",
        'notificationPreferences': [
            {
            'handle': emailID,
            'handleType': "email",
            'active': True
            }
        ]

    }        
  
    headers = {
        'accessToken':'Bearer ' + access_token,
        'thirdPartyAccessId': thirdPartyAccessId,
        'requestId': requestId,
        'deviceId': deviceId,
        'apiRegistrationId': apiRegistrationId,        
    }
    
    requestBody = json.dumps(dataPassed)
    response = requests.post(url2 + 'contacts',headers = headers,  json = dataPassed)
    dataRec = response.json()
    print('Post Contact Data: ')
    print(dataRec)
'''
* [getContacts retrieves all the contacts]
 * @param  string access_token         [OAuth2 access token, the format is 'Bearer AccessToken']
 * @param  string thirdpartyaccessid   [unique id that identifies a third party partner]
 * @param  string requestId            [partner generated unique id for each request used for message tracking purposes]
 * @param  string deviceId             [user device unique identifier]
 * @param  string apiRegistrationId    [unique identifier for the user api registration]
 * @param  integer maxResponseItems    [limits the max number of results]
 * @param  string fromLastUpdatedDate  [UTC datatime of contact used to retrieve only contacts updated from the specified dateTime; format is yyyy-MM-dd'T'HH:mm:ss.SSS'Z', e.g. '2016-09-11T16:12:12.000']
 * @param  integer offset              [offset is starting point of contacts filter; if offset is not provided it would be defaulted to zero]
 * @param  string sortBy               [contacts will be sorted based on sortBy column, if a value is provided. sortBy will be set to contactUpdatedDate if fromLastUpdatedDate. sortBy will be defaulted to contactName if no filters are specified]
 * @param  string orderBy              [order by is required if sort by is specified]
 * @param  string applicationId        [user application unique identifier]
 * @return string                       [a JSON string containing the contacts]
 * TODO: sortBy doesn't work
'''
def getContacts(access_token, thirdPartyAccessId, requestId, deviceId, apiRegistrationId, maxResponseItems='string', fromLastUpdatedDate='string', offset='string', sortBy='string', orderBy='string', applicationId='string'):
    headers = {
        'accessToken':'Bearer ' + access_token,
        'thirdPartyAccessId': thirdPartyAccessId,
        'requestId': requestId,
        'deviceId': deviceId,
        'apiRegistrationId': apiRegistrationId       
    }
    response = requests.get(url2 + 'contacts', headers = headers)
    dataRec = response.json()
    print('getContact Data: ')
    print(dataRec)
'''
* [putContact updates a contact for an e-Transfer customer, identified by its unique contactId]
 * @param  string contactId           [the unique identifier for the contact for the e-Transfer customer]
 * @param  string accessToken         [OAuth2 access token, the format is 'Bearer AccessToken']
 * @param  string thirdPartyAccessId  [unique id that identifies a third party partner]
 * @param  string requestId           [partner generated unique id for each request used for message tracking purposes]
 * @param  string deviceId            [user device unique identifier]
 * @param  string application_id      [user application unique identifier]
 * @param  string api_registration_id [unique identifier for the user api registration]
 * @param  string contact_name        [unique contact name to be provided for each contact]
 * @param  string contact_hash        [unique hash value to identify version of contact. It must be retrieved first through the getContacts function]
 * @param  string language            [Notifications: language]
 * @param  string handle              [Notifications: email address or phone number]
 * @param  string handle_type         [Notifications: email or sms]
 * @param  boolean active             [Notifications: true or false]
 * @return string                      [success / error message]

'''
def putContact(access_token, thirdPartyAccessId, requestId, deviceId, apiRegistrationId, emailID, contactName, contactID, contactHash):

    requestBody = {
        
        'contactId': "string",
        'contactName': contactName,
        'contactHash': contactHash,
        'language': "en",
        'notificationPreferences': [
            {
            'handle': emailID,
            'handleType': "email",
            'active': True
            }
        ]

    }        


    headers = {
        'accessToken': 'Bearer ' + access_token,
        'thirdPartyAccessId': thirdPartyAccessId,
        'requestId': requestId,
        'deviceId': deviceId,
        'apiRegistrationId': apiRegistrationId,
        
    }
    
    response = requests.put(url2 + 'contacts/' + contactID, headers = headers, json = requestBody)
    #data = response.json()
    #print('putContact Data: ')
    print(response.status_code)
    print(response.text)
    #print(data)

    #print(data)
'''
   * [deleteContact deletes a contact for an e-Transfer customer]
   * @param  string contactId          [the unique e-Transfer customer ID]
   * @param  string accessToken        [OAuth2 access token, the format is 'Bearer AccessToken'.]
   * @param  string Thirdpartyaccessid [unique id that identifies a third party partner]
   * @param  string Requestid          [partner generated unique id for each request used for message tracking purposes]
   * @param  string Deviceid           [user device unique identifier]
   * @param  string Apiregistrationid  [unique identifier for the user api registration]
   * @param  string applicationId      [user application unique identifier]
   * @return string                     [success or error message]
'''
def deleteContact(access_token, thirdPartyAccessId, requestId, deviceId, apiRegistrationId, contactID):
    headers = {
        'contactID': contactID,
        'accessToken':'Bearer ' + access_token,
        'thirdPartyAccessId': thirdPartyAccessId,
        'requestId': requestId,
        'deviceId': deviceId,
        'apiRegistrationId': apiRegistrationId       
    }
    response = requests.delete(url2 + 'contacts/' + '{}'.format(contactID), headers = headers)
    #data = response.json()
    print('deleteContact Data: ')
    print(response.status_code)
    print(response.text)
    #print(data)

'''
* [getContactThroughContactID retrieves the specific contact with the given id]
 * @param  string access_token         [OAuth2 access token, the format is 'Bearer AccessToken']
 * @param  string thirdpartyaccessid   [unique id that identifies a third party partner]
 * @param  string requestId            [partner generated unique id for each request used for message tracking purposes]
 * @param  string deviceId             [user device unique identifier]
 * @param  string apiRegistrationId    [unique identifier for the user api registration]
 * @param  integer maxResponseItems    [limits the max number of results]
 * @param  string fromLastUpdatedDate  [UTC datatime of contact used to retrieve only contacts updated from the specified dateTime; format is yyyy-MM-dd'T'HH:mm:ss.SSS'Z', e.g. '2016-09-11T16:12:12.000']
 * @param  integer offset              [offset is starting point of contacts filter; if offset is not provided it would be defaulted to zero]
 * @param  string sortBy               [contacts will be sorted based on sortBy column, if a value is provided. sortBy will be set to contactUpdatedDate if fromLastUpdatedDate. sortBy will be defaulted to contactName if no filters are specified]
 * @param  string orderBy              [order by is required if sort by is specified]
 * @param  string applicationId        [user application unique identifier]
 * @return string                       [a JSON string containing the contacts]
 
'''    
def getContactThroughContactID(access_token, thirdPartyAccessId, requestId, deviceId, apiRegistrationId, contactID):
    headers = {
        'contactID': contactID,
        'accessToken':'Bearer ' + access_token,
        'thirdPartyAccessId': thirdPartyAccessId,
        'requestId': requestId,
        'deviceId': deviceId,
        'apiRegistrationId': apiRegistrationId       
    }
    
    response = requests.get(url2 + 'contacts/' + contactID, headers = headers)
    print('get contact Data: ')
    print(response.status_code)
    print(response.text)
     
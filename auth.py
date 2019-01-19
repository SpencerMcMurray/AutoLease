'''
* [The authenticate function calls the access-tokens page to authenticate user]
* @param  string $salt                 [salt stored in config/config.php]
* @param  string $secretKey            [application secret key stored in config/config.php]
* @param  string $thirdpartyaccessid   [thirdpartyaccessid  stored in config/config.php]
* @return string $access_token         [returned JSON is stored in $contactId and $contactHash]
'''

import base64
import random #for salt
import string
import requests
import json
import hashlib

accessTokenUrl = 'https://gateway-web.beta.interac.ca/publicapi/api/v1/access-tokens'

def auth(salt, secretKeyString, thirdpartyaccessid):
    print(secretKeyString)
    headers = {
        #'Content-Type': application/json,
        'secretKey': secretKeyString,
        'salt': salt,
        'thirdpartyaccessid': thirdpartyaccessid      
    }
        
    response = requests.get(accessTokenUrl, headers = headers)
    code = response.status_code
    if code == 200:
        print('Successful response')                
    else:
        print('Error Encountered, code: {}'.format(response.status_code))
        if code == 400:
            print('Validation error.')
        elif code == 401:
            print('Unauthorized')
        else:
            print('unexpected error')
    # Get the response data as a python object.  Verify that it's a dictionary.
    data = response.json()
    print(type(data))
    print(data)
    return data.get('access_token') #return the access token

import base64
import random #for salt
import string
import requests
import json
import hashlib

from authentication import auth

from contacts import addContact
from contacts import getContacts
from contacts import putContact
from contacts import deleteContact
from contacts import getContactThroughContactID


from moneyRequests import decode_money_request_status
from moneyRequests import decode_notification_status
from moneyRequests import sendMoneyRequest
from moneyRequests import sendMoneyRequestOneTimeContact


from time import gmtime, strftime

url2 = 'https://gateway-web.beta.interac.ca/publicapi/api/v2/'

def main():
    
    secretKey  = 'NVgO3PKxvMe5sueJAIjFiRT72JPfbBUFKQViGqQCekM'
    salt = createSalt()
    keyAndSalt = salt + ':' + secretKey
    thirdPartyAccessid = 'CA1TAJktHqdaRvvA'
    requestId = 'requestID'
    deviceID = 'deviceID'
    apiRegistrationId = 'CA1ARDuFreeGEsCA'
    email = 'chaudherymanik@yahoo.com'
    name = 'bhai'
    contactID = 'CAb6354mWzEW'    
    encodedKey = encodeSecretKey(keyAndSalt)
    print(encodedKey)
    secretKeyString = encodedKey #need to
    access_token = auth(salt, secretKeyString, thirdPartyAccessid)
    toDate = '2018-05-20T16:12:12.000Z'

    randomID = '34674366743hsvgkjvgskvb'
    fromDate = '2018-05-16T16:12:12.000Z'
    referenceNumber = 'CA1MRqNhTkFJ'

    print('starting')

    auth(salt, encodedKey, thirdPartyAccessid)

    #addContact(access_token, thirdPartyAccessid, requestId, deviceID, apiRegistrationId, email, name)
    #getContacts(access_token, thirdPartyAccessid, requestId, deviceID, apiRegistrationId)
    #putContact(access_token, thirdPartyAccessid, requestId, deviceID, apiRegistrationId, email, name, contactID)
    #deleteContact(access_token, thirdPartyAccessid, requestId, deviceID, apiRegistrationId, contactID)
    #getContactThroughContactID(access_token, thirdPartyAccessid, requestId, deviceID, apiRegistrationId, contactID)
    
    
    #money
    
    #getMoneyRequest(access_token, thirdPartyAccessid, requestId, deviceID, apiRegistrationId, fromDate, toDate)
    #sendMoneyRequest(access_token, thirdPartyAccessid, requestId, deviceID, apiRegistrationId, fromDate, toDate)
    #sendMoneyRequestOneTimeContact(access_token, thirdPartyAccessid, requestId, deviceID, apiRegistrationId, fromDate, toDate)
    #cancelMoneyRequests(access_token, thirdPartyAccessid, requestId, deviceID, apiRegistrationId)
    #noticeMoneyRequest(referenceNumber, access_token, thirdPartyAccessid, requestId, deviceID, apiRegistrationId)
    #putMoneyRequest(referenceNumber, access_token, thirdPartyAccessid, requestId, deviceID,  apiRegistrationId, fromDate, toDate)
def encodeSecretKey(keyAndSalt):
    h = hashlib.sha256()
    h.update(keyAndSalt.encode())
    return base64.b64encode(h.digest()).decode("utf-8") 

def createSalt():
    ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    chars=[]
    for i in range(16):
        chars.append(random.choice(ALPHABET))
    
    return "".join(chars)

if __name__ == '__main__':
    main()
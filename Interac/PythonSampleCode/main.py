import base64
import random #for salt
import string
import requests
import json
import hashlib

import authentication as authentication
import contacts as contacts
import moneyRequests as moneyRequests

from datetime import datetime
from time import gmtime, strftime

url2 = 'https://gateway-web.beta.interac.ca/publicapi/api/v2/'

def main(email_id,amount):
    
    secretKey  = 'fiTCGMmgq91zdXUVH4TNgveOB2CpwCGMYD-5RduzJlo'
    salt = createSalt()
    keyAndSalt = salt + ':' + secretKey
    thirdPartyAccessid = 'CA1TAz4wCrnk8eyx'
    requestId = 'requestID'
    deviceID = 'deviceID'
    apiRegistrationId = 'CA1ARHQj3sb5KWYD'
    email = email_id
    name = 'soham'
    contactID = 'CA56aj6jHQQB'
    encodedKey = encodeSecretKey(keyAndSalt)
    toDate = '2019-01-21T16:12:12.000Z'
    randomID = '34674366743hsvgkjvgskvb'
    fromDate = '2019-01-20T16:12:12.000Z'
    referenceNumber = 'CAXnpT5h'

    print('starting')

    access_token = authentication.auth(salt, encodedKey, thirdPartyAccessid)

    # contacts.addContact(access_token, thirdPartyAccessid, requestId, deviceID, apiRegistrationId, email, name)
    # contacts.getContacts(access_token, thirdPartyAccessid, requestId, deviceID, apiRegistrationId)
    #contacts.putContact(access_token, thirdPartyAccessid, requestId, deviceID, apiRegistrationId, email, name, contactID)
    #contacts.deleteContact(access_token, thirdPartyAccessid, requestId, deviceID, apiRegistrationId, contactID)
    #contacts.getContactThroughContactID(access_token, thirdPartyAccessid, requestId, deviceID, apiRegistrationId, contactID)
    
    
    #money
    
    #moneyRequests.getMoneyRequest(access_token, thirdPartyAccessid, requestId, deviceID, apiRegistrationId, fromDate, toDate)
    # moneyRequests.sendMoneyRequest(access_token, thirdPartyAccessid, requestId, deviceID, apiRegistrationId, fromDate, toDate)
    moneyRequests.sendMoneyRequestOneTimeContact(access_token, thirdPartyAccessid, requestId, deviceID, apiRegistrationId, fromDate, toDate,amount)
    moneyRequests.getTranscationStatus()
    #moneyRequests.cancelMoneyRequests(access_token, thirdPartyAccessid, requestId, deviceID, apiRegistrationId)
    #moneyRequests.noticeMoneyRequest(referenceNumber, access_token, thirdPartyAccessid, requestId, deviceID, apiRegistrationId)
    #moneyRequests.putMoneyRequest(referenceNumber, access_token, thirdPartyAccessid, requestId, deviceID,  apiRegistrationId, fromDate, toDate)
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
    main("sohampathak991@icloud.com","100")
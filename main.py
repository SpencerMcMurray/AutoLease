import base64
import random #for salt
import hashlib

import authentication as authentication
import moneyRequests as moneyRequests

url2 = 'https://gateway-web.beta.interac.ca/publicapi/api/v2/'

def main(email_id,amount):
    
    secretKey  = 'k5PG9-GT0x016M-rKZPqpCPQYj2HFlLXTU8kJpQl5L8'
    salt = createSalt()
    keyAndSalt = salt + ':' + secretKey
    thirdPartyAccessid = 'CA1TAuUG9Ned35wF'
    requestId = 'requestID'
    deviceID = 'deviceID'
    apiRegistrationId = 'CA1ARFrD8x2J5U94'
    email = email_id
    name = 'soham'
    contactID = 'CA56aj6jHQQB'
    encodedKey = encodeSecretKey(keyAndSalt)
    toDate = '2019-01-23T16:12:12.000Z'
    randomID = '34674366743hsvgkjvgskvb'
    fromDate = '2019-01-22T16:12:12.000Z'
    referenceNumber = 'CAXnpT5h'

    print('starting')

    access_token = '3c1bec2a-4ddd-48c1-af6c-9935eab6096b'

    # contacts.addContact(access_token, thirdPartyAccessid, requestId, deviceID, apiRegistrationId, email, name)
    # contacts.getContacts(access_token, thirdPartyAccessid, requestId, deviceID, apiRegistrationId)
    #contacts.putContact(access_token, thirdPartyAccessid, requestId, deviceID, apiRegistrationId, email, name, contactID)
    #contacts.deleteContact(access_token, thirdPartyAccessid, requestId, deviceID, apiRegistrationId, contactID)
    #contacts.getContactThroughContactID(access_token, thirdPartyAccessid, requestId, deviceID, apiRegistrationId, contactID)

    
    #money

    #moneyRequests.getMoneyRequest(access_token, thirdPartyAccessid, requestId, deviceID, apiRegistrationId, fromDate, toDate)
    # moneyRequests.sendMoneyRequest(access_token, thirdPartyAccessid, requestId, deviceID, apiRegistrationId, fromDate, toDate)
    link=moneyRequests.sendMoneyRequestOneTimeContact(access_token, thirdPartyAccessid, requestId, deviceID, apiRegistrationId, fromDate, toDate, amount)
    print(link)
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
    main("sohampathak991@beta.inter.ac","100")

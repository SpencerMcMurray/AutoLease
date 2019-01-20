import base64
import random  # for salt
import hashlib
import time
import authentication as authentication
import moneyRequests as moneyRequests

url2 = 'https://gateway-web.beta.interac.ca/publicapi/api/v2/'


def main(email_id, amount):
    secretKey = 'k5PG9-GT0x016M-rKZPqpCPQYj2HFlLXTU8kJpQl5L8'
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
    toDate = '2019-01-20T16:12:12.000Z'
    randomID = '34674366743hsvgkjvgskvb'
    fromDate = '2019-01-18T16:12:12.000Z'
    referenceNumber = 'CAXnpT5h'
    print('starting')
    access_token = 'b51e7f6a-18ef-473d-afe7-b5abbd026d9c'

    # contacts.addContact(access_token, thirdPartyAccessid, requestId, deviceID, apiRegistrationId, email, name)
    # contacts.getContacts(access_token, thirdPartyAccessid, requestId, deviceID, apiRegistrationId)
    # contacts.putContact(access_token, thirdPartyAccessid, requestId, deviceID, apiRegistrationId, email, name, contactID)
    # contacts.deleteContact(access_token, thirdPartyAccessid, requestId, deviceID, apiRegistrationId, contactID)
    # contacts.getContactThroughContactID(access_token, thirdPartyAccessid, requestId, deviceID, apiRegistrationId, contactID)

<<<<<<< HEAD
    # money
    # moneyRequests.sendMoneyRequest(access_token, thirdPartyAccessid, requestId, deviceID, apiRegistrationId, fromDate, toDate)
    payload = moneyRequests.getMoneyRequest(access_token, thirdPartyAccessid,
                                            requestId, deviceID,
                                            apiRegistrationId, fromDate,
                                            toDate, 'CA1MRke7Zh83')
    status = moneyRequests.get_status_from_dict(payload)
    while (not (status is ("7") or status is ("8"))):
        print(status)
        payload = moneyRequests.getMoneyRequest(access_token,
                                                thirdPartyAccessid, requestId,
                                                deviceID, apiRegistrationId,
                                                fromDate, toDate, slug)
        link = moneyRequests.sendMoneyRequestOneTimeContact(access_token,
                                                            thirdPartyAccessid,
                                                            requestId,
                                                            deviceID,
                                                            apiRegistrationId,
                                                            fromDate, toDate,
                                                            amount)

        slug = link.split("/")[-1]
        time.sleep(20)
        status = moneyRequests.get_status_from_dict(payload)
        print(status)
    # print(ref)
    # print(moneyRequests.get_status_from_dict(ref))
    # while(moneyRequests.get_status_from_dict(ref)!='8' or moneyRequests.get_status_from_dict(ref)!='7'):
    #     ref = link.split("/")[-1]


=======
    
    #money

    print(moneyRequests.getMoneyRequest(access_token, thirdPartyAccessid, requestId, deviceID, apiRegistrationId, fromDate, toDate))
    # moneyRequests.sendMoneyRequest(access_token, thirdPartyAccessid, requestId, deviceID, apiRegistrationId, fromDate, toDate)
    link=moneyRequests.sendMoneyRequestOneTimeContact(access_token, thirdPartyAccessid, requestId, deviceID, apiRegistrationId, fromDate, toDate, amount)
    print(link)
>>>>>>> parent of e10795e... Created get status for reference number
def encodeSecretKey(keyAndSalt):
    h = hashlib.sha256()
    h.update(keyAndSalt.encode())
    return base64.b64encode(h.digest()).decode("utf-8")


def createSalt():
    ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    chars = []
    for i in range(16):
        chars.append(random.choice(ALPHABET))

    return "".join(chars)


if __name__ == '__main__':
    main("sohampathak991@icloud.com", "100")

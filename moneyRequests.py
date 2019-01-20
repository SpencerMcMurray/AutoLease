'''
-----------------------------------------------------variable defintions As written by Claudio in PHP code---------------------------------------------------------------
'''
#Money Requests
'''
decode_money_request_status returns the decoded value

 * param  string value          [this is the input value, an integer from 1 to 8]
 * return string decoded_value  [decoded value]

'''
import http.client
import base64
import random #for salt
import string
import requests
import json
import hashlib

#the following are replacements of switch is python

url2 = 'https://gateway-web.beta.interac.ca/publicapi/api/v2/'

def decode_money_request_status(value):
    decoded_value = ""
    
    if value == '1':
        decoded_value = 'Request Initiated'
    elif value == '2':
        decoded_value = 'Available To Be Fulfilled'
    elif value == '3':
        decoded_value = 'Request Fulfilled'   
    elif value == '4':
        decoded_value = 'Declined'
    elif value == '5':
        decoded_value = 'Cancelled'
    elif value == '6':
        decoded_value = 'Expired'
    elif value == '7':
        decoded_value = 'Deposit Failed'
    elif value == '8':
        decoded_value = 'Request Completed'
    
    return decoded_value

'''
decode_notification_status returns the decoded value]
 * param  string value          [this is the input value, an integer from 0 to 3]
 * return string decoded_value  [decoded value]

'''
def decode_notification_status(value):
    decoded_value = ''
    
    if value == 0:
        decoded_value = 'Sent'
    elif value == 1:
        decoded_value = 'Pending'
    elif value == 2:
        decoded_value = 'Pending Send Failure'
    elif value == 3:
        decoded_value = 'Delivery Failure'

    return decoded_value

#
# '''
#  * [sendMoneyRequest creates a money request for an e-Transfer customer]
#  * param  string accessToken                   [OAuth2 access token, the format is 'Bearer AccessToken']
#  * param  string thirdPartyAccessid            [unique id that identifies a third party partner]
#  * param  string requestId                     [partner generated unique id for each request used for message tracking purposes]
#  * param  string deviceId                      [user device unique identifier]
#  * param  string applicationId                 [user application unique identifier]
#  * param  string apiRegistrationId             [unique identifier for the user api registration]
#  * param  string referenceNumber               [unique identifier for the money request; this field should not be specified in the POST request]
#  * param  string sourceMoneyRequestId          [unique identifier of the money request in the originating system (1 to 64 characters length)]
#  * param  string requestFromContactId          [Unique identifier for the contact; required for permanent contact]
#  * param  string requestFromContactHash        [unique hash value to identify version of contact;required for permanent contact]
#  * param  string requestFromContacName         [contact name, required for onetime contact]
#  * param  string language                      [language used to notify this contact, required for onetime contact. Values: en, fr]
#  * param  string notificationPrefHandle        [Email address (format ab.ca) or mobile phone number ( format 123-222-7777 )]
#  * param  string notificationHandleType        [email, sms]
#  * param  string active                        [specifies if notifications will not be sent]
#  * param  string amount                        [the requested amount (it will be converted into double by the app)]
#  * param  string currency                      [the currency of the requested amount; only CAD is supported for now]
#  * param  string editableFulfillAmount         [flag indicating if the transfer amount can be different from the requested amount. Values: true, false. TODO: it seems like we can only set this field to false]
#  * param  string requesterMessage              [message from the requester. Max length: 400 characters]
#  * param  string invoiceNumber                 [number of the invoice to be paid. Max length: 120 characters]
#  * param  string dueDate                       [UTC date of the invoice is to be paid by; format is yyyy-MM-dd'T'HH:mm:ss.SSS'Z', e.g. '2016-09-11T16:12:12.000']
#  * param  string expiryDate                    [UTC datatime this money request is valid until; format is yyyy-MM-dd'T'HH:mm:ss.SSS'Z', e.g. '2016-09-11T16:12:12.000']
#  * param  string supressResponderNotifications [if flag is on, Interac will not send notifications to the intended responder; the requester is expected to handle the notification part themselves. Values: true, false. Values will be converted into boolean by the web app]
#  * param  string returnURL                     [return URL to redirect the Responder after the Money Request fulfillment]
#  * param  string creationDate                  [UTC datatime of creation for this request; this field should not be specified in POST or PUT requests; format is yyyy-MM-dd'T'HH:mm:ss.SSS'Z', e.g. '2016-09-11T16:12:12.000']
#  * param  integer status                       [Does not need to be provided at request creation time; this field should not be specified in POST or PUT requests. Values: REQUEST_INITIATED(1), AVAILABLE_TO_BE_FULFILLED(2), REQUEST_FULFILLED(3), DECLINED(4), CANCELLED(5), EXPIRED(6), DEPOSIT_FAILED(7), REQUEST_COMPLETED(8)]
#  * param  string fulfillAmount                 [the fulfilled amount; to not be specified in POST or PUT requests; present if status is completed. It will be converted into double by the web app]
#  * param  string responderMessage              [message from the responder; this field should not be specified in POST or PUT requests]
#  * param  integer notificationStatus           [indicates the status of the notifications sent to the recipient; this field should not be specified in POST or PUT requests | SENT(0) PENDING(1) PENDING_SEND_FAILURE(2) DELIVERY_FAILURE(3)]
#  * return string                                [JSON string containing the unique referenceNumber and the paymentGatewayUrl]
#
# '''
#
# def sendMoneyRequest(accessToken, thirdPartyAccessid, requestId, deviceId,  apiRegistrationId, fromDate, expiryDate , applicationId='string', sourceMoneyRequestId = 'string', referenceNumber = 'string', requestFromContactId = 'string',
# requestFromContactHash = 'string', requestFromContactName = 'string', language = 'en', notificationPrefHandle = 'string', notificationHandleType = 'string', active = 'string', amount = 'string', currency = 'string', editableFulfillAmount=False, requesterMessage = 'string',
# invoiceNumber = 'string', dueDate = 'string', supressResponderNotifications = 'string', returnURL = 'string', creationDate = 'string', status = 'string', fulfillAmount = 'string', responderMessage = 'string', notificationStatus = 'string'):
#
#
#     headerBody = {
#         'accessToken': 'Bearer ' + accessToken,
#         'thirdPartyAccessId': thirdPartyAccessid,
#         'requestId': 'requestID',
#         'deviceId': deviceId,
#         'apiRegistrationId': apiRegistrationId
#
#         }
#
#     dataPassed = {
#     	"referenceNumber" : referenceNumber,
#     	"sourceMoneyRequestId" : 'asfd',
#     	"requestedFrom" : {
#     		"contactId" : 'CArEgVW9BTXu',
#     		"contactHash" : '2214257a5dd76589f1236687548548a2',
#     		"contactName" : requestFromContactName,
#     		"language" : language,
#     		"notificationPreferences": [
#     			{
#         		"handle": "string",
#         		"handleType": "email",
#         		"active": True
#       			}
#     		]
#   		},
#
#   		"amount": 10,
#   		"currency": "CAD",
#  		"editableFulfillAmount": False,
#   		"requesterMessage": "string",
#   		"invoice": {
#    			"invoiceNumber": "string",
#     		"dueDate": expiryDate
#   		},
#
#   		"expiryDate": expiryDate,
#   		"supressResponderNotifications": True,
#   		"returnURL": "string",
#   		"creationDate": fromDate,
#   		"status": 0,
#   		"fulfillAmount": 0,
#   		"responderMessage": "string",
#   		"notificationStatus": 0
#     }
#     response = requests.post(url2 + 'money-requests/send/', headers = headerBody, json = dataPassed)
#     print(response.status_code)
#     dataRec = response.json()
#     print('sendMoneyRequest Data: ')
#     print(dataRec)
    


'''
 * [sendMoneyRequestOneTimeContact creates a money request but don't want to add them as a contact first or store that new phone number in your contact list]
 * param  string accessToken                   [OAuth2 access token, the format is 'Bearer AccessToken']
 * param  string thirdPartyAccessid            [unique id that identifies a third party partner]
 * param  string requestId                     [partner generated unique id for each request used for message tracking purposes]
 * param  string deviceId                      [user device unique identifier]
 * param  string applicationId                 [user application unique identifier]
 * param  string apiRegistrationId             [unique identifier for the user api registration]
 * param  string referenceNumber               [unique identifier for the money request; this field should not be specified in the POST request]
 * param  string sourceMoneyRequestId          [unique identifier of the money request in the originating system (1 to 64 characters length)]
 * param  string requestFromContacName         [contact name, required for onetime contact]
 * param  string language                      [language used to notify this contact, required for onetime contact. Values: en, fr]
 * param  string notificationPrefHandle        [Email address (format ab.ca) or mobile phone number ( format 123-222-7777 )]
 * param  string notificationHandleType        [email, sms]
 * param  string active                        [specifies if notifications will not be sent]
 * param  string amount                        [the requested amount (it will be converted into double by the app)]
 * param  string currency                      [the currency of the requested amount; only CAD is supported for now]
 * param  string editableFulfillAmount         [flag indicating if the transfer amount can be different from the requested amount. Values: true, false. TODO: it seems like we can only set this field to false]
 * param  string requesterMessage              [message from the requester. Max length: 400 characters]
 * param  string invoiceNumber                 [number of the invoice to be paid. Max length: 120 characters]
 * param  string dueDate                       [UTC date of the invoice is to be paid by; format is yyyy-MM-dd'T'HH:mm:ss.SSS'Z', e.g. '2016-09-11T16:12:12.000']
 * param  string expiryDate                    [UTC datatime this money request is valid until; format is yyyy-MM-dd'T'HH:mm:ss.SSS'Z', e.g. '2016-09-11T16:12:12.000']
 * param  string supressResponderNotifications [if flag is on, Interac will not send notifications to the intended responder; the requester is expected to handle the notification part themselves. Values: true, false. Values will be converted into boolean by the web app]
 * param  string returnURL                     [return URL to redirect the Responder after the Money Request fulfillment]
 * param  string creationDate                  [UTC datatime of creation for this request; this field should not be specified in POST or PUT requests; format is yyyy-MM-dd'T'HH:mm:ss.SSS'Z', e.g. '2016-09-11T16:12:12.000'
 * param  integer status                       [Does not need to be provided at request creation time; this field should not be specified in POST or PUT requests. Values: REQUEST_INITIATED(1), AVAILABLE_TO_BE_FULFILLED(2), REQUEST_FULFILLED(3), DECLINED(4), CANCELLED(5), EXPIRED(6), DEPOSIT_FAILED(7), REQUEST_COMPLETED(8)]
 * param  string fulfillAmount                 [the fulfilled amount; to not be specified in POST or PUT requests; present if status is completed. It will be converted into double by the web app]
 * param  string responderMessage              [message from the responder; this field should not be specified in POST or PUT requests]
 * param  integer notificationStatus           [indicates the status of the notifications sent to the recipient; this field should not be specified in POST or PUT requests | SENT(0) PENDING(1) PENDING_SEND_FAILURE(2) DELIVERY_FAILURE(3)]
 * return string                                [JSON string containing the unique referenceNumber and the paymentGatewayUrl]
'''


def sendMoneyRequestOneTimeContact(accessToken, thirdPartyAccessid, requestId, deviceId,  apiRegistrationId, fromDate, expiryDate , amount = 'string',email='string', applicationId='string',referenceNumber = 'string', sourceMoneyRequestId = 'string', requestFromContactName = 'string', language = 'en', notificationPrefHandle = 'string', notificationHandleType = 'string', active = 'string', currency = 'string', editableFulfillAmount='false', requesterMessage = 'string',
invoiceNumber = 'string', dueDate = 'string', supressResponderNotifications = 'string', returnURL = 'string', creationDate = 'string', status = 'string', fulfillAmount = 'string', responderMessage = 'string', notificationStatus = 'string'):

    headerBody = {        
        'accessToken': 'Bearer ' + accessToken,
        'thirdPartyAccessId': thirdPartyAccessid,
        'requestId': generateRandomString(),
        'deviceId': deviceId,
        'apiRegistrationId': apiRegistrationId

        }

    dataPassed = {
    	"referenceNumber" : referenceNumber,
    	"sourceMoneyRequestId" : generateRandomString(),
    	"requestedFrom" : {	
    		"contactName" : requestFromContactName,
    		"language" : language,
    		"notificationPreferences": [
    			{
        		"handle": "sohampathak991@beta.inter.ac",
        		"handleType": "email",
        		"active": True
      			}
    		]
  		},

  		"amount": amount,
  		"currency": "CAD",
 		"editableFulfillAmount": False,
  		"requesterMessage": "string",
  		"invoice": {
   			"invoiceNumber": "string",
    		"dueDate": expiryDate
  		},

  		"expiryDate": expiryDate,
  		"supressResponderNotifications": True,
  		"returnURL": "string",
  		"creationDate": fromDate,
  		"status": 0,
  		"fulfillAmount": 0,
  		"responderMessage": generateRandomString(),
  		"notificationStatus": 0
    }
    response = requests.post(url2 + 'money-requests/send/', headers = headerBody, json = dataPassed)
    print(response.status_code)
    dataRec = response.json()
    print('sendMoneyRequestOneTimeContact Data: ')
    # print(dataRec)
    return dataRec['paymentGatewayUrl']

#
# '''
#  [putMoneyRequest updates a money request for an e-Transfer customer]
#  * param  string requestReferenceNumber        [unique identifier for the money request; this field should not be specified in the POST request]
#  * param  string accessToken                   [OAuth2 access token, the format is 'Bearer AccessToken']
#  * param  string thirdPartyAccessId            [unique id that identifies a third party partner]
#  * param  string requestId                     [partner generated unique id for each request used for message tracking purposes]
#  * param  string deviceId                      [user device unique identifier]
#  * param  string applicationId                 [user application unique identifier]
#  * param  string apiRegistrationId             [unique identifier for the user api registration]
#  * param  string thirdPartyReferenceNumber     [same as requestReferenceNumber. Used in the request body]
#  * param  string sourceMoneyRequestId          [unique identifier of the money request in the originating system (1 to 64 characters length)]
#  * param  string requestFromContactId          [Unique identifier for the contact; required for permanent contact]
#  * param  string requestFromContactHash        [unique hash value to identify version of contact;required for permanent contact]
#  * param  string requestFromContacName         [contact name, required for onetime contact]
#  * param  string language                      [language used to notify this contact, required for onetime contact. Values: en, fr]
#  * param  string notificationPrefHandle        [Email address (format a@b.ca) or mobile phone number (format 123-222-7777)]
#  * param  string notificationHandleType        [email, sms]
#  * param  string active                        [specifies if notifications will not be sent]
#  * param  string amount                        [the requested amount (it will be converted into double by the app)]
#  * param  string currency                      [the currency of the requested amount; only CAD is supported for now]
#  * param  string editableFulfillAmount         [flag indicating if the transfer amount can be different from the requested amount. Values: true, false. TODO: it seems like we can only set this field to false]
#  * param  string requesterMessage              [message from the requester. Max length: 400 characters]
#  * param  string invoiceNumber                 [number of the invoice to be paid. Max length: 120 characters]
#  * param  string dueDate                       [UTC date of the invoice is to be paid by; format is yyyy-MM-dd'T'HH:mm:ss.SSS'Z', e.g. '2016-09-11T16:12:12.000']
#  * param  string expiryDate                    [UTC datatime this money request is valid until; format is yyyy-MM-dd'T'HH:mm:ss.SSS'Z', e.g. '2016-09-11T16:12:12.000']
#  * param  string supressResponderNotifications [if flag is on, Interac will not send notifications to the intended responder; the requester is expected to handle the notification part themselves. Values: true, false. Values will be converted into boolean by the web app]
#  * param  string returnURL                     [return URL to redirect the Responder after the Money Request fulfillment]
#  * param  string creationDate                  [UTC datatime of creation for this request; this field should not be specified in POST or PUT requests; format is yyyy-MM-dd'T'HH:mm:ss.SSS'Z', e.g. '2016-09-11T16:12:12.000']
#  * param  integer status                       [Does not need to be provided at request creation time; this field should not be specified in POST or PUT requests. Values: REQUEST_INITIATED(1), AVAILABLE_TO_BE_FULFILLED(2), REQUEST_FULFILLED(3), DECLINED(4), CANCELLED(5), EXPIRED(6), DEPOSIT_FAILED(7), REQUEST_COMPLETED(8)]
#  * param  string fulfillAmount                 [the fulfilled amount; to not be specified in POST or PUT requests; present if status is completed. It will be converted into double by the web app]
#  * param  string responderMessage              [message from the responder; this field should not be specified in POST or PUT requests]
#  * param  integer notificationStatus           [indicates the status of the notifications sent to the recipient; this field should not be specified in POST or PUT requests | SENT(0) PENDING(1) PENDING_SEND_FAILURE(2) DELIVERY_FAILURE(3)]
#  * return string                                [message returned]
#
# '''
# def putMoneyRequest(referenceNumber, accessToken, thirdPartyAccessid, requestId, deviceId,  apiRegistrationId, fromDate, expiryDate, thirdPartyReferenceNumber = 'string', applicationId='string', sourceMoneyRequestId = 'string', requestFromContactId = 'string',
# requestFromContactHash = 'string', requestFromContactName = 'string', language = 'en', notificationPrefHandle = 'string', notificationHandleType = 'string', active = 'string', amount = 'string', currency = 'string', editableFulfillAmount=False, requesterMessage = 'string',
# invoiceNumber = 'string', dueDate = 'string', supressResponderNotifications = 'string', returnURL = 'string', creationDate = 'string', status = 'string', fulfillAmount = 'string', responderMessage = 'string', notificationStatus = 'string'):
#     thirdPartyReferenceNumber = referenceNumber
#     headerBody = {
#         'accessToken': 'Bearer ' + accessToken,
#         'thirdPartyAccessId': thirdPartyAccessid,
#         'requestId': requestId,
#         'deviceId': deviceId,
#         'apiRegistrationId': apiRegistrationId
#
#         }
#
#     dataPassed = {
#     	"referenceNumber" : referenceNumber,
#     	#"thirdPartyReferenceNumber": thirdPartyReferenceNumber,
#     	"sourceMoneyRequestId" : sourceMoneyRequestId,
#     	"requestedFrom" : {
#     		"contactId" : 'CArEgVW9BTXu',
#     		"contactHash" : '2214257a5dd76589f1236687548548a2',
#     		"contactName" : requestFromContactName,
#     		"language" : language,
#     		"notificationPreferences": [
#     			{
#         		"handle": "string",
#         		"handleType": "email",
#         		"active": True
#       			}
#     		]
#   		},
#
#   		"amount": 10,
#   		"currency": "CAD",
#  		"editableFulfillAmount": False,
#   		"requesterMessage": "string",
#   		"invoice": {
#    			"invoiceNumber": "string",
#     		"dueDate": expiryDate
#   		},
#
#   		"expiryDate": expiryDate,
#   		"supressResponderNotifications": True,
#   		"returnURL": "string",
#   		"creationDate": fromDate,
#   		"status": 0,
#   		"fulfillAmount": 5,
#   		"responderMessage": "string",
#   		"notificationStatus": 0
#     }
#
#     response = requests.put(url2 + 'money-requests/send/' + referenceNumber, headers = headerBody, json = dataPassed)
#     print('Updated money request: ')
#     print(response.status_code)
#
#     print(response.text)
#
#     return (response.text)
#
# '''
#  * [noticeMoneyRequest re-sends a money request notice]
#  * @param  string referenceNumber    [unique identifier for the money request; this field should not be specified in the POST request]
#  * @param  string accessToken        [OAuth2 access token, the format is 'Bearer AccessToken]
#  * @param  string thirdPartyAccessId [unique id that identifies a third party partner]
#  * @param  string requestId          [partner generated unique id for each request used for message tracking purposes]
#  * @param  string deviceId           [user device unique identifier]
#  * @param  string applicationId      [user application unique identifier]
#  * @param  string apiRegistrationId  [unique identifier for the user api registration]
#  * @return string msg                [Returned message depends on the HTTP code (204 is a successful response)]
#
# '''
# def noticeMoneyRequest(referenceNumber, accessToken, thirdPartyAccessId, requestId, deviceId, apiRegistrationId, applicationId = ''):
#     headerBody = {
#         'accessToken': 'Bearer ' + accessToken,
#         'thirdPartyAccessId': thirdPartyAccessId,
#         'requestId': generateRandomString(),
#         'deviceId': deviceId,
#         'apiRegistrationId': apiRegistrationId
#         }
#
#     response = requests.patch(url2 + 'money-requests/send/' + referenceNumber + '/notice', headers = headerBody)
#     print(response.status_code)
#     dataRec = response.json()
#     print('noticeMoneyRequest Data: ')
#     print(dataRec)
#
# '''
#  * [cancelMoneyRequests cancels a money request]
#  * @param  string referenceNumber    [unique identifier for the money request; this field should not be specified in the POST request]
#  * @param  string accessToken        [OAuth2 access token, the format is 'Bearer AccessToken']
#  * @param  string thirdPartyAccessId [unique id that identifies a third party partner]
#  * @param  string requestId          [partner generated unique id for each request used for message tracking purposes]
#  * @param  string deviceId           [user device unique identifier]
#  * @param  string apiRegistrationId  [unique identifier for the user api registration]
#  * @param  string cancellationReason [the cancellation reason, contained in the request body JSON string]
#  * @param  string applicationId      [user application unique identifier]
#  * @return string                     [success or error message]
#
# '''
#
# def cancelMoneyRequests(accessToken, thirdPartyAccessId, requestId, deviceId, apiRegistrationId, cancellationReason = 'just like that', applicationId = 'null', referenceNumber = 'CA1MR8NYCXXr'):
#     headerBody = {
#         'accessToken': 'Bearer ' + accessToken,
#         'thirdPartyAccessId': thirdPartyAccessId,
#         'requestId': generateRandomString(),
#         'deviceId': deviceId,
#         'apiRegistrationId': apiRegistrationId
#         }
#
#     dataIn = {
#         'cancellationReason': 'aise hee kara'
#     }
#
#     response = requests.patch(url2 + 'money-requests/send/' + referenceNumber + '/cancel', headers = headerBody, json = dataIn)
#     print(response.status_code)
#
#     print('cancelMoneyRequest Data: ')
#     dataRec = response.json()
#     print(dataRec)
#
#
# '''
# retrieves all money requests
#
#
#  * [getMoneyRequests retrieves all money requests]
#  * string accessToken          [OAuth2 access token, the format is 'Bearer AccessToken']
#  * string Thirdpartyaccessid   [unique id that identifies a third party partner]
#  * string Requestid            [partner generated unique id for each request used for message tracking purposes]
#  * string deviceId             [user device unique identifier]
#  * string ApiRegistrationId    [unique identifier for the user api registration]
#  * string fromDate             [UTC datatime format is yyyy-MM-dd'T'HH:mm:ss.SSS'Z', e.g. '2016-09-11T16:12:12.000'; this parameter is mandatory if sourceMoneyRequestId or referenceNumber is not given.]
#  * TODO: in original documentation page "fromDate" and "toDate" must be in this format: <2018-02-01T16:12:12.721Z>
#  * string toDate               [UTC datatime format is yyyy-MM-dd'T'HH:mm:ss.SSS'Z', e.g. '2016-09-11T16:12:12.000'; this parameter is mandatory if sourceMoneyRequestId or referenceNumber is not given]
#  * integer maxResponseItems    [if offset is provided then maxResponse items is required; all ( OR maximum set by interac system ) items are returned if this field is absent]
#  * integer offset              [offset is starting point of money-requests filter; if offset is not provided it would be defaulted to zero]
#  * string sortBy               [money-requests will be sorted based on sortBy column. Options: creationDate]
#  * string orderBy              [order by is required if sort by is specified. Options: desc and asc]
#  * string sourceMoneyRequestId [unique identifier of the money request in the originating system (1 to 64 characters length)]
#  * string referenceNumber      [unique identifier for the money request; this field should not be specified in the POST request]
#  * string applicationId        [user application unique identifier]
#  * return string                       [JSON string with all the existing money requests]
#  * Important to get rid of contact id and hash id and specify the email for request
# '''
# def getMoneyRequest(access_token, thirdPartyAccessId, requestId, deviceId, apiRegistrationId, fromDate = 'string',  toDate='string', maxResponseItems='string', offset='string', sortBy='string', orderBy='string', sourceMoneyRequestId='string', referenceNumber='string', applicationId='string', params = ''):
#
#     params = ''
#
#     if fromDate != 'string':
#         if len(params) == 0:
#             params += ('?fromDate=' + fromDate)
#         else:
#             params += ('&fromDate=' + fromDate)
#
#     if toDate != 'string':
#         if len(params) == 0:
#             params += ('?toDate=' + toDate)
#         else:
#             params += ('&toDate=' + toDate)
#
#     if maxResponseItems != 'string':
#         if len(params) == 0:
#             params += ('?maxResponseItems=' + maxResponseItems)
#         else:
#             params += ('&maxResponseItems=' + maxResponseItems)
#
#     if offset != 'string':
#         if len(params) == 0:
#             params += ('?offset=' + offset)
#         else:
#             params += ('&offset=' + offset)
#
#     if sortBy != 'string':
#         if len(params) == 0:
#             params += ('?sortBy=' + sortBy)
#         else:
#             params += ('&sortBy=' + sortBy)
#
#     if orderBy != 'string':
#         if len(params) == 0:
#             params += ('?referenceNumber=' + referenceNumber)
#         else:
#             params += ('&referenceNumber=' + referenceNumber)
#
#     if sourceMoneyRequestId != 'string':
#         if len(params) == 0:
#             params += ('?sourceMoneyRequestId=' + sourceMoneyRequestId)
#         else:
#             params += ('&sourceMoneyRequestId=' + sourceMoneyRequestId)
#
#     if referenceNumber != 'string':
#         if len(params) == 0:
#             params += ('?referenceNumber=' + referenceNumber)
#         else:
#             params += ('&referenceNumber=' + referenceNumber)
#
#     if applicationId != 'string':
#         if len(params) == 0:
#             params += ('?applicationId=' + applicationId)
#         else:
#             params += ('&applicationId=' + applicationId)
#
#     print(params)
#
#     headerBody = {
#         'accessToken': 'Bearer ' + access_token,
#         'thirdPartyAccessId': thirdPartyAccessId,
#         'requestId': requestId,
#         'deviceId': deviceId,
#         'apiRegistrationId': apiRegistrationId
#         }
#
#     #response = requests.get(url2 + 'money-requests'+'/send' + str(params), headers = headers)
#     response = requests.get(url2+'money-requests'+'/send' + params, headers = headerBody)
#     print('retrieved money requests: ')
#     print(response.status_code)
#     print(response.text)
#
#     return (response.text)

# def getTranscationStatus():
#
#     url = "https://gateway-web.beta.interac.ca/publicapi/api/v2/money-requests/send"
#
#     # querystring = {"referenceNumber":referenceNumber}
#     querystring = {"toDate": "2019-02-21T16:12:12.000Z", "fromDate": "2019-01-2T16:12:12.000Z"}
#     payload = "{\n\t\n}"
#     headers = {
#         'Content-Type':"application/json",
#         'accessToken':"Bearer 406d2f45-263d-4dbd-ad08-8176907cab25",
#         'thirdPartyAccessId':"CA1TAuUG9Ned35wF",
#         'apiRegistrationId':"CA1ARFrD8x2J5U94",
#         'requestId':"asdf",
#         'deviceId':"asdf",
#         'cache-control':"no-cache",
#         'Postman-Token':"9a730192-d4eb-4805-869a-6e7a83a0c211"
#     }
#     response = requests.request("GET", url, data = payload, headers = headers,  params = querystring)
#     return response.json()


def generateRandomString():
    firstGate = random.randint(0,3)
    if firstGate == 0:
        secondGate = str(random.randint(0,10))
    elif firstGate == 1:
        secondGate = chr(random.randint(65,91))
    else:
        secondGate = chr(random.randint(97,123))
    return secondGate
'''
* [The authenticate function calls the access-tokens page to authenticate user]
* @param  string $salt                 [salt stored in config/config.php]
* @param  string $secretKey            [application secret key stored in config/config.php]
* @param  string $thirdpartyaccessid   [thirdpartyaccessid  stored in config/config.php]
* @return string $access_token         [returned JSON is stored in $contactId and $contactHash]
'''
import requests
import base64
import random #for salt
import string
import json
import hashlib

url2 = 'https://gateway-web.beta.interac.ca/publicapi/api/v2/'

def auth(salt, secretKeyString, thirdpartyaccessid):
    print(secretKeyString)
    headers = {
        #'Content-Type': application/json,
        'secretKey': secretKeyString,
        'salt': salt,
        'thirdpartyaccessid': thirdpartyaccessid      
    }
        
    response = requests.get('https://gateway-web.beta.interac.ca/publicapi/api/v1/access-tokens', headers = headers)
    code = response.status_code
    if code == 200:
        print('Successful response')                
    else:
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
from adal import AuthenticationContext
import requests
import json

AUTHORITY = 'https://login.microsoftonline.com/8fb1f5b2-a2b4-409c-bcd6-21a3f3aad0d6'
WORKBENCH_API_URL = 'https://blockchain-voiqlc-api.azurewebsites.net/'
RESOURCE = '27c00335-188f-4c3f-a47c-4c825bf4f12c'
CLIENT_APP_Id = '2a525ae3-8712-4273-9ee9-9318d92028b6' # service ID
CLIENT_SECRET = 'tZ:FVbBdsHoasBoPay4*[C+Avw7eRy11'# KEY

auth_context = AuthenticationContext(AUTHORITY)

if __name__ == '__main__':
    try:
        # Acquiring the token
        SESSION = requests.Session()
        #token = auth_context.acquire_token_with_authorization_code()
        token = auth_context.acquire_token_with_client_credentials(RESOURCE, CLIENT_APP_Id, CLIENT_SECRET)
        #print(token)
        SESSION.headers.update({'Authorization': 'Bearer ' + token['accessToken']})

        print(SESSION.get(WORKBENCH_API_URL+ 'api/v1/contracts?workflowId=1').json())
        #print(SESSION.post(WORKBENCH_API_URL+ 'api/v2/contracts/16/actions', json= data1))
        SESSION.close()
    except Exception as error:
        print("error")
        print (error)

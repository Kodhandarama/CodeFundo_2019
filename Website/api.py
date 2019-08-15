from adal import AuthenticationContext
import requests
import json

AUTHORITY = 'https://login.microsoftonline.com/6d6fbafa-d99a-400e-b093-41d4a2553990'
WORKBENCH_API_URL = 'https://stallions-wfhynd-api.azurewebsites.net/'
RESOURCE = '60a51ac4-abac-41e3-ab5c-3090b749b45c'
CLIENT_APP_Id = '40abb33e-a30a-4985-80a6-3372aa605d17'
#CLIENT_APP_Id = 'f3f00be6-4952-4a22-ae80-0d3ba99dbd89'
CLIENT_SECRET = 'O3U=U4mgk8CYBb?PkOI6oL.rucS_tJ?y'
#CLIENT_SECRET = '3jX.U]@dLGx59T]UwC2LmP=fnF+A4Z7Z'

auth_context = AuthenticationContext(AUTHORITY)

if __name__ == '__main__':
    try:
        # Acquiring the token
        SESSION = requests.Session()
        #token = auth_context.acquire_token_with_authorization_code()
        token = auth_context.acquire_token_with_client_credentials(RESOURCE, CLIENT_APP_Id, CLIENT_SECRET)
        #print(token)
        SESSION.headers.update({'Authorization': 'Bearer ' + token['accessToken']})
        data = {
            "workflowFunctionId": 9,
            "workflowActionParameters": [
                {
                   "name": "Constituency ID",
                    "value": "10"
                },
                {
                    "name": "Candidates",
                    "value":"[1,2,4]"
                } 
            ]
        }
        data1 = {
            "workflowFunctionId":20,
            "workflowActionParameters":[
            ]
        }
        #print(SESSION.get(WORKBENCH_API_URL+ 'api/v2/contracts/17/actions').json())
        print(SESSION.post(WORKBENCH_API_URL+ 'api/v2/contracts/16/actions', json= data1))
        SESSION.close()
    except Exception as error:
        print("error")
        print (error)

from adal import AuthenticationContext
import requests

AUTHORITY = 'https://login.microsoftonline.com/purushothamansyadavgmail.onmicrosoft.com'
WORKBENCH_API_URL = 'https://stallions-vjyuwl-api.azurewebsites.net'
RESOURCE = '701336a4-6d01-4bda-9395-7e864834f535'
CLIENT_APP_Id = 'c6466833-3bb5-4925-a47b-216e34c5b713'
CLIENT_SECRET = 'i9E0YDGNTpSYgBmxS73lM5ljmeBrMY+DF9K/k53dYRc='

auth_context = AuthenticationContext(AUTHORITY)

if __name__ == '__main__':
    try:
        # Acquiring the token
        token = auth_context.acquire_token_with_client_credentials(RESOURCE, CLIENT_APP_Id, CLIENT_SECRET)
        headers = {'Authorization': 'Bearer ' + token['accessToken']}
        data = {
            "externalID": ['d2434c2d-a648-4f94-bdal-d408c50bac79'],
            "firstName": ['Shashank'],
            "lastName" : ['MG'],
            "emailAddress": ['abcd']
        }
        # Making call to Workbench
        #requests.post(WORKBENCH_API_URL + '/api/v1/users',json = data ,headers=headers)
        response = requests.get(WORKBENCH_API_URL + '/api/v1/contracts?workflowId=1', headers=headers)
        print(response.json()['contracts'][0])
        for x in response.json()['contracts'][0]:
            print(x)
    except Exception as error:
        print (error)
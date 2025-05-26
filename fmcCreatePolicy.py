import requests
import json
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url = 'https://fmcrestapisandbox.cisco.com'
login_url = '/api/fmc_platform/v1/auth/generatetoken'
headers = {'content-Type': 'application/json'}
user = 'tfakeye7'
pw = #(password goes here)

login_response = requests.post(
    f'{url}{login_url}',
    auth=(user,pw),
    verify=False
)
# Parse out the headers
resp_headers = login_response.headers
# Grab the token from the headers
token = resp_headers.get('X-auth-access-token', default=None)
# Set the token in the headers to be used in the next call
headers['X-auth-access-token']=token

########## CREATE POLICY with Default rule of IPS ##########
pol_url = '/api/fmc_config/v1/domain/e276abec-e0f2-11e3-8169-6d9ed49b625f/policy/accesspolicies'

payload = {
  "type": "AccessPolicy",
  "name": "TakeOff Policy 101",
  "description": "TakeOff demo policy",
  "defaultAction": {
    "action": "BLOCK"
  }
}

pol_response = requests.post(
    f'{url}{pol_url}',
    headers=headers,
    data=json.dumps(payload),
    verify=False
).json()
print(' ******* POLICY CREATED ******* ')
print(json.dumps(pol_response, indent=2, sort_keys=True))
print(' ******* POLICY CREATED ******* ')
print('')
policyId = pol_response['id']

policy_url = f'/api/fmc_config/v1/domain/e276abec-e0f2-11e3-8169-6d9ed49b625f/policy/accesspolicies/{policyId}'

########## Add Rules to monitor files for Malware ##########
rules_url = f'{policy_url}/accessrules'
rules_payload = {
    "sendEventsToFMC": True,
    "action": "ALLOW",
    "enabled": True,
    "type": "AccessRule",
    "name": "TakeOff Malware Rule",
    "sendEventsToFMC": False,
    "logFiles": False,
    "logBegin": False,
    "logEnd": False,
    "variableSet": {
        "name": "Default Set",
        "id": "VariableSetUUID",
        "type": "VariableSet"
    },
    "filePolicy": {
        "type": "FilePolicy",
        "id": "filePolicyUuid",
        "name": "filePolicyName"
    }
}

rules_response = requests.post(
    f'{url}{rules_url}',
    headers=headers,
    data=json.dumps(rules_payload),
    verify=False
).json()

print(' ******* RULES CREATED ******* ')
print(json.dumps(rules_response, indent=2, sort_keys=True))
print(' ******* RULES CREATED ******* ')
print('')

### CLEAN UP ###
print(' ******* Deleting Policy ******* ')

del_response = requests.delete(
    f'{url}{policy_url}',
    headers=headers,
    verify=False
)
print(del_response)

print(' ******* Deleting Policy ******* ')

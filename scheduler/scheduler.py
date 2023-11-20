import requests, os, json, yaml
from warnings import filterwarnings
from urllib3.exceptions import InsecureRequestWarning

filterwarnings("ignore", category=InsecureRequestWarning)

def trigger_pipeline(host, token, pipeline_dict):
  endpoint = 'https://' + host + ':2746/api/v1/workflows/default'

  payload = {}
  payload['workflow'] = pipeline_dict
  payload['namespace'] = 'default'
  payload['serverDryRun'] = False
  payload = json.dumps(payload)

  auth = 'Bearer ' + token
  headers = {
    'Authorization': auth,
    'Content-Type': 'application/json'
  }

  response = requests.post(endpoint, headers=headers, data=payload, verify=False)
  if response.status_code == 200:
    print("Request successful")
  else:
    print(f"Request failed with status code {response.status_code}")
    print(response.text)


def main():
  host = os.environ.get('HOST', 'localhost')
  token = os.environ.get('BEARER_TOKEN')

  with open('../pipeline/full-pipeline.yaml', 'r') as file:
    full_pipeline = yaml.safe_load(file)

  trigger_pipeline(host, token, full_pipeline)

if __name__ == '__main__':
  main()

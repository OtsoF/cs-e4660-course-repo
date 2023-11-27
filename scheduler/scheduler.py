import requests, os, json, yaml, glob
from warnings import filterwarnings
from urllib3.exceptions import InsecureRequestWarning
from sqlalchemy import create_engine
import pandas as pd
from sklearn.metrics import accuracy_score
import joblib

filterwarnings("ignore", category=InsecureRequestWarning)

def get_last_trained_id(engine):
  conn = engine.connect()
  try:
    df = pd.read_sql('SELECT id FROM last_trained_id;', conn)
    return df['id'].values[0]
  except:
    print("Error getting last trained id")
    return 0
  finally:
    conn.close()

def get_current_accuracy(engine):
  conn = engine.connect()
  ac = 0
  try:
    df = pd.read_sql('SELECT accuracy FROM accuracy;', conn)
    return float(df['accuracy'].values[0])
  except:
    print("Error getting accuracy")
    return 0
  finally:
    conn.close()

def get_newest_model(directory):
  files = glob.glob(os.path.join(directory, '*'))
  if not files:
    print("No model found")
    exit(1)
  newest_file = max(files, key=os.path.getctime)
  model = joblib.load(newest_file)
  return model


def get_accuracies():
  host = os.environ.get('DB_HOST')
  database = os.environ.get('DB_NAME')
  user = os.environ.get('DB_USER')
  password = os.environ.get('DB_PASS')
  model_file_path = os.environ.get('MODEL_FILE_PATH')
  table = 'insurance_prep'
  col_names = ['ps_ind_02_cat', 'ps_ind_01', 'ps_ind_03', 'ps_ind_15',
      'ps_car_01_cat', 'ps_car_06_cat']

  print("Getting new data from database...")
  ae = create_engine(f'postgresql+psycopg2://{user}:{password}@{host}/{database}')
  last_id = get_last_trained_id(ae)
  get_data_query = f"SELECT {','.join(col_names)} FROM {table} WHERE id > {last_id};"
  ae_conn = ae.connect()
  df = pd.read_sql(get_data_query, ae_conn)
  if df.empty:
    print("No new data found")
    exit(0)
  ae_conn.close()

  print('Getting model')
  model = get_newest_model(model_file_path)

  print("Checking accuracy")
  new_data_accuracy = accuracy_score(df['ps_ind_02_cat'], model.predict(df.drop(['ps_ind_02_cat'], axis=1)))
  current_accuracy = get_current_accuracy(ae)
  print(f"Accuracy on new data : {new_data_accuracy}, current accuracy : {current_accuracy}")

  #return new_data_accuracy, current_accuracy
  return 0.88, 0.90

def get_carbon_intensity():
  print("Checking carbon intensity")
  url  = "https://api-access.electricitymaps.com/free-tier/carbon-intensity/latest?zone=DE"
  headers = {
    'auth-token': os.environ.get('ELECTRICITY_MAPS_TOKEN')
  }
  response = requests.get(url, headers=headers)

  if response.status_code != 200:
    print(f"Request failed with status code {response.status_code}")
    print(response.text)
    return -1
  response_json = response.json()
  carbon_intensity = int(response_json['carbonIntensity'])
  print(f"Carbon intensity : {carbon_intensity}")
  return carbon_intensity

def check_if_pipeline_should_run():
  print("Checking if pipeline should run")
  new_accuracy, current_accuracy = get_accuracies()
  max_accuracy_decrease = float(os.environ.get('MAX_ACCURACY_DECREASE', 0.05))
  low_accuracy_decrease = float(os.environ.get('LOW_ACCURACY_DECREASE', 0.01))
  carbon_intensity_threshold = float(os.environ.get('CARBON_INTENSITY_THRESHOLD', 200))

  if new_accuracy < current_accuracy - max_accuracy_decrease:
    print("Accuracy decreased too much re-train immediately")
    return True
  elif new_accuracy < current_accuracy - low_accuracy_decrease:
    print("Accuracy decreased below first threshold, check carbon intensity")
    if get_carbon_intensity() < carbon_intensity_threshold:
      print("Low carbon intensity, re-train")
      return True
    else:
      print("High carbon intensity, do not re-train yet")
      return False

def trigger_pipeline(host, token, pipeline_dict):
  print("Triggering pipeline")
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
  pipeline_path = os.environ.get('PIPELINE_PATH')
  print(f"Using pipeline {pipeline_path}")

  with open(pipeline_path, 'r') as file:
    full_pipeline = yaml.safe_load(file)

  if check_if_pipeline_should_run():
    trigger_pipeline(host, token, full_pipeline)

if __name__ == '__main__':
  main()

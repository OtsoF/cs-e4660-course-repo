import psycopg2, os, time, random
import numpy as np
import pandas as pd
import joblib
from datetime import datetime
from sqlalchemy import create_engine
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

def meaningless_computation(n):
  comp_time = n / 1000
  print(f"Doing meaningless computation for {comp_time} seconds")
  start_time = time.time()
  while time.time() - start_time < comp_time:
    matrix_size = 50
    matrix_a = np.random.rand(matrix_size, matrix_size)
    matrix_b = np.random.rand(matrix_size, matrix_size)
    result = np.dot(matrix_a, matrix_b)
    # x = random.random()
    # y = random.random()
    # res = x * y

def set_last_id(engine, df):
  conn = engine.connect()
  new_last_id =  df['id'].max()
  if np.isnan(new_last_id):
    print("is nan")
    return
  print(f"NEW LAST ID: {new_last_id}")
  id_df = pd.DataFrame( {'id': [ new_last_id ]} )
  id_df.to_sql('last_trained_id', conn, if_exists='replace', index=False)
  conn.close()

def set_accuracy(engine, accuracy):
  conn = engine.connect()
  accuracy_df = pd.DataFrame( {'accuracy': [ accuracy ]} )
  accuracy_df.to_sql('accuracy', conn, if_exists='replace', index=False)
  conn.close()

def main():
  host = os.environ.get('DB_HOST')
  database = os.environ.get('DB_NAME')
  user = os.environ.get('DB_USER')
  password = os.environ.get('DB_PASS')
  model_file_path = os.environ.get('MODEL_FILE_PATH')
  fake_computation = os.environ.get('FAKE_COMPUTATION')
  table = 'insurance_prep'
  col_names = ['id', 'ps_ind_02_cat', 'ps_ind_01', 'ps_ind_03', 'ps_ind_15',
      'ps_car_01_cat', 'ps_car_06_cat']
  get_data_query = f"SELECT {','.join(col_names)} FROM {table};"

  print("Getting data from database...")
  ae = create_engine(f'postgresql+psycopg2://{user}:{password}@{host}/{database}')
  ae_conn = ae.connect()
  df = pd.read_sql(get_data_query, ae_conn)
  ae_conn.close()

  X = df.drop(['ps_ind_02_cat', 'id'], axis=1)
  y = df['ps_ind_02_cat']

  X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 42)

  model = RandomForestClassifier(n_estimators=100, random_state=0)

  print("Training model...")
  model.fit(X_train, y_train)
  set_last_id(ae, df)
  if fake_computation == 'true':
    meaningless_computation(df.shape[0])
  
  model_accuracy = accuracy_score(y_test, model.predict(X_test))
  set_accuracy(ae, model_accuracy)
  print("Trained model with accuracy : {0:0.4f}".format(model_accuracy))

  print("Saving model...")
  ts = datetime.now().strftime("%Y-%m-%d-%H%M-%S")
  model_file = f'{model_file_path}/model_{ts}.pkl'
  joblib.dump(model, model_file)
  print(f"Dumped model to file : {model_file}")

if __name__ == '__main__':
  main()
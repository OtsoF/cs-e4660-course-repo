import psycopg2, os
import numpy as np
import pandas as pd
import joblib
from datetime import datetime
from sqlalchemy import create_engine
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

def main():
  host = os.environ.get('DB_HOST')
  database = os.environ.get('DB_NAME')
  user = os.environ.get('DB_USER')
  password = os.environ.get('DB_PASS')
  model_file_path = os.environ.get('MODEL_FILE_PATH')
  table = 'car_data_preprocessed'
  get_data_query = f"SELECT buying, maint, doors, persons, lug_boot, car_safety, class FROM {table};"
  col_names = ['buying', 'maint', 'doors', 'persons', 'lug_boot', 'car_safety', 'class']

  print("Getting data from database...")
  ae = create_engine(f'postgresql+psycopg2://{user}:{password}@{host}/{database}')
  ae_conn = ae.connect()
  df = pd.read_sql(get_data_query, ae_conn)
  ae_conn.close()

  df.columns = col_names

  X = df.drop(['class'], axis=1)
  y = df['class']

  X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.33, random_state = 42)

  model = RandomForestClassifier(random_state=0)

  print("Training model...")
  model.fit(X_train, y_train)

  print("Trained model with accuracy : {0:0.4f}".format(accuracy_score(y_test, model.predict(X_test))))

  print("Saving model...")
  ts = datetime.now().strftime("%Y-%m-%d-%H%M-%S")
  model_file = f'{model_file_path}/model_{ts}.pkl'
  joblib.dump(model, model_file)
  print(f"Dumped model to file : {model_file}")

if __name__ == '__main__':
  main()
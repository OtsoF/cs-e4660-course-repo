import psycopg2, os
import pandas as pd
from sqlalchemy import create_engine
import numpy as np

def get_last_id(engine):
  conn = engine.connect()
  try:
    df = pd.read_sql('SELECT id FROM last_prep_id;', conn)
    print(f"OLD LAST ID: {df['id'].values[0]}")
    return df['id'].values[0]
  except:
    print("OLD LAST ID: 0")
    return 0
  finally:
    conn.close()

def set_last_id(engine, df):
  conn = engine.connect()
  new_last_id =  df['id'].max()
  if np.isnan(new_last_id):
    return
  print(f"NEW LAST ID: {new_last_id}")
  id_df = pd.DataFrame( {'id': [ new_last_id ]} )
  id_df.to_sql('last_prep_id', conn, if_exists='replace', index=False)
  conn.close()

def main():
  host = os.environ.get('DB_HOST')
  database = os.environ.get('DB_NAME')
  user = os.environ.get('DB_USER')
  password = os.environ.get('DB_PASS')

  table = 'insurance'
  table_preprocessed = f'{table}_prep'
  col_names = ['id', 'ps_ind_02_cat', 'ps_ind_01', 'ps_ind_03', 'ps_ind_15',
      'ps_car_01_cat', 'ps_car_06_cat']
  


  print("Getting data from database...")
  ae = create_engine(f'postgresql+psycopg2://{user}:{password}@{host}/{database}')
  ae_conn = ae.connect()
  last_id = get_last_id(ae)
  get_data_query = f"SELECT {','.join(col_names)} FROM {table} WHERE id > {last_id};"
  df = pd.read_sql(get_data_query, ae_conn)
  ae_conn.close()

  print("Preprocessing data...")
  df = df[ col_names ].dropna()


  print("Exporting preprocessed data to db...")
  ae_conn = ae.connect()
  df.to_sql(table_preprocessed, ae_conn, if_exists='append', index=False)
  set_last_id(ae, df)
  ae_conn.close()
  
if __name__ == "__main__":
  main()
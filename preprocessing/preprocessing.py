import psycopg2, os
import pandas as pd
from sqlalchemy import create_engine


def main():
  host = os.environ.get('DB_HOST')
  database = os.environ.get('DB_NAME')
  user = os.environ.get('DB_USER')
  password = os.environ.get('DB_PASS')
  table = 'insurance'
  table_preprocessed = f'{table}_prep'
  col_names = ['target', 'ps_ind_01', 'ps_ind_02_cat', 'ps_ind_03',
       'ps_ind_04_cat', 'ps_ind_05_cat', 'ps_ind_14', 'ps_ind_15',
       'ps_car_01_cat', 'ps_car_02_cat','ps_car_03_cat', 'ps_car_06_cat']
  get_data_query = f"SELECT {','.join(col_names)} FROM {table} where;"


  print("Getting data from database...")
  ae = create_engine(f'postgresql+psycopg2://{user}:{password}@{host}/{database}')
  ae_conn = ae.connect()
  df = pd.read_sql(get_data_query, ae_conn)
  ae_conn.close()

  print("Preprocessing data...")
  df = df[ col_names ].dropna()

  print("Exporting preprocessed data to db...")
  ae_conn = ae.connect()
  df.to_sql(table_preprocessed, ae_conn, if_exists='replace', index=False)
  ae_conn.close()
  
if __name__ == "__main__":
  main()
import os, psycopg2
import pandas as pd
from sqlalchemy import create_engine

def main():
  host = os.environ.get('DB_HOST')
  database = os.environ.get('DB_NAME')
  user = os.environ.get('DB_USER')
  password = os.environ.get('DB_PASS')
  csv_path = os.environ.get('CSV_PATH')
  n_rows = os.environ.get('N_ROWS', 'all')
  start_row = os.environ.get('START_ROW', '0')
  table = 'insurance'
  
  print(f'Importing data into {database}.{table} on {host}...')

  ae = create_engine(f'postgresql+psycopg2://{user}:{password}@{host}/{database}')
  ae_conn = ae.connect()
  if n_rows == 'all':
    df = pd.read_csv(csv_path)
  elif start_row == "0":
    df = pd.read_csv(csv_path, nrows=int(n_rows))
  else: 
    df = pd.read_csv(csv_path, nrows=int(n_rows), skiprows=range(1,int(start_row) + 1))

  df.to_sql(table, ae_conn, if_exists='append', index=False)
  ae_conn.close()

  print(f"Data successfully imported into {database}.{table}.")



if __name__ == "__main__":
  main()
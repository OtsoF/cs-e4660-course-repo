import os, psycopg2
import pandas as pd
from sqlalchemy import create_engine

def main():
  host = os.environ.get('DB_HOST')
  database = os.environ.get('DB_NAME')
  user = os.environ.get('DB_USER')
  password = os.environ.get('DB_PASS')
  csv_path = os.environ.get('CSV_PATH')
  n_rows = os.environ.get('N_ROWS')
  table = 'insurance'
  
  print(f'Importing data into {database}.{table} on {host}...')

  ae = create_engine(f'postgresql+psycopg2://{user}:{password}@{host}/{database}')
  ae_conn = ae.connect()
  if n_rows == None:
    df = pd.read_csv(csv_path)
  else: 
    df = pd.read_csv(csv_path, nrows=int(n_rows))

  df.to_sql(table, ae_conn, if_exists='replace', index=False)
  ae_conn.close()

  print(f"Data successfully imported into {database}.{table}.")



if __name__ == "__main__":
  main()
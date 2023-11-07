import psycopg2, os
import pandas as pd
import category_encoders as ce
from sqlalchemy import create_engine
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)


def main():
  host = os.environ.get('DB_HOST')
  database = os.environ.get('DB_NAME')
  user = os.environ.get('DB_USER')
  password = os.environ.get('DB_PASS')
  table = 'car_data'
  table_preprocessed = f'{table}_preprocessed'
  get_data_query = f"SELECT buying, maint, doors, persons, lug_boot, car_safety, class FROM {table};"
  col_names = ['buying', 'maint', 'doors', 'persons', 'lug_boot', 'car_safety', 'class']
  
  # encoder config
  df_unique = pd.read_csv('unique.csv', header=None)
  df_unique.columns = col_names
  encoder = ce.OrdinalEncoder(cols=['buying', 'maint', 'doors', 'persons', 'lug_boot', 'car_safety'])
  encoder.fit(df_unique)

  print("Getting data from database...")
  ae = create_engine(f'postgresql+psycopg2://{user}:{password}@{host}/{database}')
  ae_conn = ae.connect()
  df = pd.read_sql(get_data_query, ae_conn)
  ae_conn.close()

  print("Preprocessing data...")
  df.columns = col_names
  df = encoder.transform(df)

  print("Exporting preprocessed data to db...")
  ae_conn = ae.connect()
  df.to_sql(table_preprocessed, ae_conn, if_exists='replace', index=False)
  ae_conn.close()
  
if __name__ == "__main__":
  main()
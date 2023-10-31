import psycopg2, os
import pandas as pd
import category_encoders as ce

def execute_sql(connection, cursor, sql):
  try:
    cursor.execute(sql)
    connection.commit()
  except Exception as e:
    print(f"Error executing SQL: {e}")
    connection.rollback()
    exit(1)

def import_data(connection, df, table):
  try:
    df.to_sql(table, connection, if_exists='replace', index=False)
    connection.commit()
  except Exception as e:
    connection.rollback()
    print(f"Error importing data: {e}")
    exit(1)

def main():
  host = os.environ.get('DB_HOST')
  database = os.environ.get('DB_NAME')
  user = os.environ.get('DB_USER')
  password = os.environ.get('DB_PASS')
  table = 'car_data'
  table_preprocessed = f'{table}_preprocessed'
  create_table_query = f"""
  CREATE TABLE IF NOT EXISTS {table_preprocessed} (
    id SERIAL PRIMARY KEY,
    buying INTEGER,
    maint INTEGER,
    doors INTEGER,
    persons INTEGER,
    lug_boot INTEGER,
    car_safety INTEGER,
    class VARCHAR
  );
  """
  get_data_query = f"SELECT buying, maint, doors, persons, lug_boot, car_safety, class FROM {table};"

  try:
    conn = psycopg2.connect(host=host, database=database, user=user, password=password)
    cur = conn.cursor()
    execute_sql(conn, cur, create_table_query)

    df = pd.read_sql(get_data_query, conn)
    col_names = ['buying', 'maint', 'doors', 'persons', 'lug_boot', 'car_safety', 'class']
    df.columns = col_names

    encoder = ce.OrdinalEncoder(cols=['buying', 'maint', 'doors', 'persons', 'lug_boot', 'car_safety'])
    df = encoder.fit_transform(df)
    import_data(conn, df, table_preprocessed)
  except psycopg2.Error as error:
    print(error)
    exit(1)
  
if __name__ == "__main__":
  main()
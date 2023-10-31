import psycopg2, os, csv


def execute_sql(connection, cursor, sql):
  try:
    cursor.execute(sql)
    connection.commit()
  except Exception as e:
    print(f"Error executing SQL: {e}")
    connection.rollback()
    exit(1)

def main():
  host = os.environ.get('DB_HOST')
  database = os.environ.get('DB_NAME')
  user = os.environ.get('DB_USER')
  password = os.environ.get('DB_PASS')
  table = 'car_data'
  create_table_query = f"""
  CREATE TABLE IF NOT EXISTS {table} (
    id SERIAL PRIMARY KEY,
    buying VARCHAR,
    maint VARCHAR,
    doors VARCHAR,
    persons VARCHAR,
    lug_boot VARCHAR,
    car_safety VARCHAR,
    class VARCHAR
  );
  """

  print(f'Importing data into {database}.{table} on {host}...')

  try:
    conn = psycopg2.connect(host=host, database=database, user=user, password=password)
    cur = conn.cursor()
    execute_sql(conn, cur, create_table_query)

  except psycopg2.Error as error:
    print(error)
    exit(1)

  try:
      with open('/app/car.data', 'r') as csv_file:
          reader = csv.reader(csv_file)
          for row in reader:
              # SQL query to insert a row from the CSV into the PostgreSQL table
              insert_query = f"INSERT INTO {table} (buying, maint, doors, persons, lug_boot, car_safety, class) VALUES (%s, %s, %s, %s, %s, %s, %s);"
              cur.execute(insert_query, row)
      conn.commit()
      print(f"Data successfully imported into {table}.")
  except Exception as e:
      conn.rollback()
      print(f"Error importing data: {e}")


if __name__ == "__main__":
  main()
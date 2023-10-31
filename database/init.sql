
CREATE TABLE car_data (
  id SERIAL PRIMARY KEY,
  buying VARCHAR,
  maint VARCHAR,
  doors VARCHAR,
  persons VARCHAR,
  lug_boot VARCHAR,
  car_safety VARCHAR,
  class VARCHAR
);

CREATE TABLE car_data_encoded (
  id SERIAL PRIMARY KEY,
  buying INTEGER,
  maint INTEGER,
  doors INTEGER,
  persons INTEGER,
  lug_boot INTEGER,
  car_safety INTEGER,
  class INTEGER
);
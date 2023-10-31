# Data Preprocessing

The mock data preprocessor simply takes the data in the postgres database, encodes it using an ordinal encoder and imports it back into the database into a new table.

## Building

`docker build -t preprocessing .`

## Deploying

`kubectl apply -f preprocessing-job.yaml`
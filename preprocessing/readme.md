# Data Preprocessing

The mock data preprocessor simply takes the data in the postgres database, encodes it using an ordinal encoder and imports it back into the database into a new table.

## Local testing

```bash
kubectl port-forward my-database-cluster-1 5432:5432

DB_HOST="127.0.0.1" DB_NAME="app" DB_USER="app" \
DB_PASS="D75VgwL1vAzrvelvT7MCUJsQvdZPfrTDbs0CyQ9TCr1x6lPHtTZAd12SJzUsxsoD" \
python preprocessing.py
```

## Building

`docker build -t preprocessing .`

## Deploying

`kubectl apply -f preprocessing-job.yaml`
`kubectl delete -f preprocessing-job.yaml`
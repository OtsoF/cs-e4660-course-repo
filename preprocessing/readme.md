# Data Preprocessing

The mock data preprocessor simply takes the data in the postgres database, ~~encodes it using an ordinal encoder~~ selects a subset of columns and drops rows with missing values and imports it back into the database into a new table. The last processed id is stored in the database, so when the preprocessing is run the next time, it won't re-process already preprocessed rows.

## Local testing

```bash
kubectl port-forward my-database-cluster-1 5432:5432

DB_HOST="127.0.0.1" DB_NAME="app" DB_USER="app" \
DB_PASS="$(kubectl get secrets/my-database-cluster-app --template={{.data.password}} | base64 -D)" \
python preprocessing.py
```

## Building

`docker build -t preprocessing .`

## Deploying

`kubectl apply -f preprocessing-job.yaml`
`kubectl delete -f preprocessing-job.yaml`
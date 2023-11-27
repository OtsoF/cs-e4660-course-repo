# Data fetch

This mock data fetcher acts as the data importer, importing data from external sources into the ML pipeline. In reality, the data is baked into the data-fetch container, which inserts this data into the Postgres database to be used by the downstream steps of the ML pipeline.

## Local testing

```bash
kubectl port-forward my-database-cluster-1 5432:5432

DB_HOST="127.0.0.1" DB_NAME="app" DB_USER="app" \
DB_PASS="$(kubectl get secrets/my-database-cluster-app --template={{.data.password}} | base64 -D)" \
MODEL_FILE_PATH="data" CSV_PATH="./AutoInsuranceClaim.csv" N_ROWS="10" START_ROW="0" \
python fetch.py

# clean database
kubectl exec -it my-database-cluster-1 -- psql -d app -c "drop table insurance;" && \
kubectl exec -it my-database-cluster-1 -- psql -d app -c "drop table insurance_prep;" && \
kubectl exec -it my-database-cluster-1 -- psql -d app -c "drop table last_prep_id;" && \
kubectl exec -it my-database-cluster-1 -- psql -d app -c "drop table last_trained_id;" &&\
kubectl exec -it my-database-cluster-1 -- psql -d app -c "drop table accuracy;"
```

## Building

`docker build -t data-fetch .`

## Deploying

`kubectl apply -f data-fetch-job.yaml`
`kubectl delete -f data-fetch-job.yaml`
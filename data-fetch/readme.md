# Data fetch

This mock data fetcher acts as the data importer, importing data from external sources into the ML pipeline. In reality, the data is baked into the data-fetch container, which inserts this data into the Postgres database to be used by the downstream steps of the ML pipeline.

## Building

`docker build -t data-fetch .`

## Deploying

`kubectl apply -f data-fetch-job.yaml`
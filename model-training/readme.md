# Model training

Here, a randomforest classifier is trainer with default hyperparameters. The resulting model is stored on a kubernetes node filesystem volume, which acts as a mock blob storage. 

## Local testing

```bash
kubectl port-forward my-database-cluster-1 5432:5432

DB_HOST="127.0.0.1" DB_NAME="app" DB_USER="app" \
DB_PASS="$(kubectl get secrets/my-database-cluster-app --template={{.data.password}} | base64 -D)" \
MODEL_FILE_PATH="data" \
python training.py
```

## Building

`docker build -t model-training .`

## Deploying

`kubectl apply -f model-training-job.yaml`
`kubectl delete -f model-training-job.yaml`
# Model training

Here, a randomforest classifier is trainer with default hyperparameters. The resulting model is stored on a kubernetes node filesystem volume, which acts as a mock blob storage. The accuracy and last id used in training are stored in the database. These are used by scheduler, to determine what new data the existing model hasn't been trained on and the accuracy of the existing model is on the data it was trained on.

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
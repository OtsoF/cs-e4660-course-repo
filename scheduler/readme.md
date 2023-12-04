# Scheduler

The scheduler checks the carbon intensity of the electric grid and the current model performance on new data. If the model performance is below a preset limit (`LOW_ACCURACY_DECREASE` env var), the scheduler will trigger the pipeline if the carbon intensity is low. If the model performance is below another preset limit (`MAX_ACCURACY_DECREASE` env var), the pipeline will be triggered immediately. The scheduler is run periodically with a CronWorkflow.

The carbon intensity is fetched using the [Electricity Maps api](https://app.electricitymaps.com/). I'm using a personal account with a free tier subscription to the api. The authentication configuration to the api can be seen below.


## Configuration

### Authentication with argo

Note: this is here as a poc (for when I set up the pipeline at work). For now the local Argo is configured without authentication.

```bash
# Create token for auth
kubectl apply -f - <<EOF
apiVersion: v1
kind: Secret
metadata:
  name: default.service-account-token
  annotations:
    kubernetes.io/service-account.name: default
type: kubernetes.io/service-account-token
EOF
```

### Authentication with Electricity Maps

```bash
kubectl create secret generic electricity-maps-token \
--from-literal='token=wu5iP7DGWGwPpUYx8rTDuoZrOrsF61wR'
```

## Local testing

```bash
DB_HOST="127.0.0.1" DB_NAME="app" DB_USER="app" \
DB_PASS="$(kubectl get secrets/my-database-cluster-app --template={{.data.password}} | base64 -D)" \
MODEL_FILE_PATH="../model-training/data" \
MAX_ACCURACY_DECREASE="0.05" SCHEDULE_DECREASE="0.00" \
CARBON_INTENSITY_THRESHOLD="800" \
PIPELINE_PATH="../pipeline/train-and-deploy-pipeline.yaml" HOST="localhost" \
BEARER_TOKEN=$(kubectl get secret default.service-account-token --template={{.data.token}} | base64 -D) \
ELECTRICITY_MAPS_TOKEN="$(kubectl get secret electricity-maps-token --template={{.data.token}} | base64 -D)" \
python scheduler.py
```

## Building


`docker build -t scheduler .`

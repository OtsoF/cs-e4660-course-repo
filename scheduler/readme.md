# Scheduler

The scheduler checks the carbon intensity of the electric grid and the current model performance on new data. If the model performance is below a preset medium_decrease limit, the scheduler will trigger the pipeline if the carbon intensity is low. If the model performance is below a critical_decrease limit, the pipeline will be triggered immediately. The scheduler is run periodically with a CronWorkflow.

## Authentication configuration

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

## Local testing

```bash
PIPELINE_PATH="../pipeline/train-and-deploy-pipeline.yaml" HOST="localhost" \
BEARER_TOKEN=$(kubectl get secret default.service-account-token -o=jsonpath='{.data.token} | base64 --decode') \
python scheduler.py
```

## Building


`docker build -t scheduler .`

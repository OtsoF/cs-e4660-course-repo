# Scheduler


## Authentication configuration

Note: this is here for future purposes (when I set up the pipeline at work). For now the local Argo is configured without authentication.

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
PIPELINES=""
BEARER_TOKEN=$(kubectl get secret default.service-account-token -o=jsonpath='{.data.token} | base64 --decode') \
python scheduler.py
```
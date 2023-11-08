# Argo Workflows

## Installation

```bash
# namespace 
kubectl create namespace argo´

# installation
kubectl apply -n argo -f https://github.com/argoproj/argo-workflows/releases/download/v3.4.13/install.yaml

# path deployment to disable non-functioning auth
kubectl patch deployment \
  argo-server \
  --namespace argo \
  --type='json' \
  -p='[{"op": "replace", "path": "/spec/template/spec/containers/0/args", "value": [
  "server",
  "--auth-mode=server"
]}]'


# port forward ui
kubectl -n argo port-forward deployment/argo-server 2746:2746


# uninstall (not tested)
kubectl delete -n argo -f https://github.com/argoproj/argo-workflows/releases/download/v3.4.13/install.yaml
```
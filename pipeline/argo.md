# Argo Workflows

## Installation

```bash
# namespace 
kubectl create namespace argo

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

# create admin clusterrolebinding. This is bad in real instance but good in the testbed, since we don't need to configure RBAC
kubectl create clusterrolebinding serviceaccounts-cluster-admin \
  --clusterrole=cluster-admin \
  --group=system:serviceaccounts
clusterrolebinding.rbac.authorization.k8s.io/serviceaccounts-cluster-admin created
otsofriman@MACDEVICE-SP65X pipeline % kubectl create clusterrolebinding serviceaccounts-cluster-admin \
  --clusterrole=cluster-admin \
  --group=system:serviceaccounts


# uninstall (not tested)
kubectl delete -n argo -f https://github.com/argoproj/argo-workflows/releases/download/v3.4.13/install.yaml
```
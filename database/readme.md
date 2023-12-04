# Database

THe database solution is a relational database PostgreSQL. It is deployed onto the cluster using a Kubernetes operator. The following is used to install the operator and database cluster defined in `./database-config.yaml`


```bash
# Install operator & CRDs (custom resource definitions)
kubectl apply -f https://raw.githubusercontent.com/cloudnative-pg/cloudnative-pg/release-1.21/releases/cnpg-1.21.0.yaml

# install datable "cluster"
kubectl apply -f database-config.yaml
```

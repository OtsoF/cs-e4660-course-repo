# Monitoring & Metrics

Monitoring & metrics use the popular prometheus + grafana stack. There are some limitations using it on docker desktop. Mainly, the node_exporter requires `hostToContainer` mount propagation, which is not supported by docker desktop https://docs.docker.com/storage/bind-mounts/#configure-bind-propagation. For this reason some metrics, and more crucially, some metadata eg. pod name & container name are missing from some metrics. For this reason, getting metrics requires knowing the pod & container UUIDS. Due to this, a lot of the default Grafana dashboards don't work. For our purposes we only use the `container_cpu_usage_seconds_total` metric, which is queried directly through grafana. This is because we are interested in power consumption and, based on how cpu scheduling works, this metric shows how long the container utilized the cpu (one core) for in total. To calculate power usage we'd need to estimate kWh/cpu-core*s. For metrics comparison here, we don't estimate that and instead treat it as an unknown quantity x when doing comparisons.


## Collecting the metrics

The following commands show how to get the pod id and utilize that to get metrics from prometheus.

```bash
#get pod id
kubectl get pod -o jsonpath='{.metadata.uid}' <pod-name>

# place pod id in this query
container_cpu_usage_seconds_total{id="/kubepods/kubepods/burstable/pod<pod-id>"}
```

## Collected metrics

We collected metics for the scenario described in the root README.md. The collected metrics and plots are in `metrics.ipynb`.

## Configuration

```bash
# setup (in cloned https://github.com/prometheus-operator/kube-prometheus.git dir)
# Note: the "mountPropagation: HostToContainer" lines in nodeExporter-daemonset.yaml are commented out.
kubectl apply --server-side -f manifests/setup
kubectl wait \
	--for condition=Established \
	--all CustomResourceDefinition \
	--namespace=monitoring
kubectl apply -f manifests/

# port forward 
kubectl -n monitoring port-forward deployment/grafana 3000:3000 # not used
kubectl -n monitoring port-forward svc/prometheus-k8s 9090

# teardown
kubectl delete --ignore-not-found=true -f manifests/ -f manifests/setup
```

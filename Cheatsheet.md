Open a new bash shell inside a container:
```
docker exec -it <mycontainer> bash
```
---
Creating a **GKE** (Google Kubernetes Engine) **cluster** using Cloud Shell:
```
gcloud config set project <project-id>
gcloud config set compute/zone <compute-zone>
gcloud container clusters create <cluster-name> --num-nodes=<n>
```
After creating the cluster, you need to get authentication credentials to interact with the it:
```
gcloud container clusters get-credentials <cluster-name>
```
This command configures `kubectl` to use the cluster you created.

Deploy an application to Kubernetes (using YAML file):
```
kubectl apply -f <filename>.yaml
```
For simpler deployments:
```
kubectl create deployment <kube-name> --image=<image-name>:<tag>
kubectl expose deployment <kube-name> --type LoadBalancer --port 80 --target-port 8080
```
To tear it down:
```
kubectl delete service <kube-name>
kubectl delete -f <filename>.yaml
gcloud container clusters delete <cluster-name>
```
---
Useful Kubernetes commands (inspection):
```
kubectl get pods
kubectl get services
kubectl get service <kube-name>
kubectl describe deployment
kubectl exec -ti <pod-name> curl localhost:<port>
```
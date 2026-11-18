# Cluster Docker / Kubernetes: Deployment y ReplicaSet

Tarea: primer Pod (nginx) y luego Deployment + ReplicaSet con Grafana en minikube.

## Estructura
- `01-pod/first_pod_nginx.yml`: Pod nginx (clase)
- `02-grafana/grafana-deployment.yml`: Deployment (3 replicas, RollingUpdate)
- `02-grafana/grafana-service.yml`: Service NodePort (30300)
- `03-replicaset-demo/replicaset-demo.yml`: ReplicaSet solo, para comparar

## Flujo
```bash
# 1. Cluster
minikube start --driver=docker
kubectl get nodes

# 2. Pod nginx
kubectl apply -f 01-pod/first_pod_nginx.yml
kubectl expose pod myfirstpod --type=NodePort --port=80
minikube service myfirstpod

# 3. Grafana con Deployment y ReplicaSet
kubectl apply -f 02-grafana/
kubectl get deployment,replicaset,pods
minikube service grafana-service   # login admin / admin

# 4. Pruebas
kubectl delete pod <pod>                                            # autorreparacion
kubectl scale deployment grafana-deployment --replicas=5            # escalado
kubectl set image deployment/grafana-deployment grafana=grafana/grafana:11.0.0   # rolling update
kubectl rollout history deployment/grafana-deployment
kubectl rollout undo deployment/grafana-deployment                  # rollback

# 5. ReplicaSet sin Deployment (no guarda historial)
kubectl apply -f 03-replicaset-demo/replicaset-demo.yml
kubectl rollout history rs/grafana-rs-demo
kubectl delete -f 03-replicaset-demo/replicaset-demo.yml
```

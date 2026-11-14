# Ejecutar DESPUES de instalar Docker Desktop (ver LEEME-DOCKER.md)
# Uso: powershell -ExecutionPolicy Bypass -File .\ejecutar-todo.ps1
$ErrorActionPreference = 'Stop'
function Paso($t){ Write-Host "`n=== $t ===" -ForegroundColor Cyan }

Paso "0. Instalar minikube y kubectl si faltan"
if(-not (Get-Command minikube -EA SilentlyContinue)){ winget install -e --id Kubernetes.minikube --accept-source-agreements --accept-package-agreements }
if(-not (Get-Command kubectl  -EA SilentlyContinue)){ winget install -e --id Kubernetes.kubectl  --accept-source-agreements --accept-package-agreements }
$env:Path = [Environment]::GetEnvironmentVariable('Path','Machine') + ';' + [Environment]::GetEnvironmentVariable('Path','User')

Paso "1. Iniciar cluster"
minikube start --driver=docker
kubectl get nodes

Paso "2. POD nginx (clase)"
kubectl apply -f .\01-pod\first_pod_nginx.yml
kubectl wait --for=condition=Ready pod/myfirstpod --timeout=120s
kubectl get pod myfirstpod -o wide
kubectl expose pod myfirstpod --type=NodePort --port=80
kubectl get svc myfirstpod
Write-Host ">> Ejecute 'minikube service myfirstpod' y tome captura de la pantalla Welcome to nginx" -ForegroundColor Yellow

Paso "3. Deployment + ReplicaSet de Grafana"
kubectl apply -f .\02-grafana\
kubectl rollout status deployment/grafana-deployment --timeout=300s
kubectl get deployment,replicaset,pods,svc -l app=grafana
kubectl get svc grafana-service

Paso "4. Pruebas de ReplicaSet"
Write-Host "4a. Auto-recuperacion: borrar un pod"
$p = (kubectl get pods -l app=grafana -o name | Select-Object -First 1)
kubectl delete $p
kubectl get pods -l app=grafana
Write-Host "4b. Escalar a 5"
kubectl scale deployment grafana-deployment --replicas=5
kubectl get rs,pods -l app=grafana
Write-Host "4c. Rolling update"
kubectl set image deployment/grafana-deployment grafana=grafana/grafana:11.0.0
kubectl rollout status deployment/grafana-deployment
kubectl get rs -l app=grafana
kubectl rollout history deployment/grafana-deployment
Write-Host "4d. Rollback"
kubectl rollout undo deployment/grafana-deployment
kubectl get rs -l app=grafana
kubectl scale deployment grafana-deployment --replicas=3

Paso "5. Exponer Grafana"
Write-Host ">> Ejecute 'minikube service grafana-service' (login admin / admin) y tome captura" -ForegroundColor Yellow

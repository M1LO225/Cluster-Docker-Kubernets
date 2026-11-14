$env:Path = [Environment]::GetEnvironmentVariable('Path','Machine') + ';' + [Environment]::GetEnvironmentVariable('Path','User')
$ErrorActionPreference = 'Continue'
Set-Location $PSScriptRoot
$edge = 'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
$tmp = Join-Path $env:TEMP 'k8s-cap'; New-Item -ItemType Directory -Force $tmp | Out-Null

function Cap($file, $cmds) {
  $txt = ''
  foreach ($c in $cmds) {
    $out = (Invoke-Expression "$c 2>&1" | Out-String)
    $txt += "PS C:\Users\emife\Desktop\Cluster> $c`r`n$out`r`n"
  }
  $h = [System.Net.WebUtility]::HtmlEncode($txt)
  $lines = ($txt -split "`n").Count
  $html = "<html><meta charset='utf-8'><body style='background:#0c0c0c;color:#ccc;font:15px Consolas,monospace;margin:0;padding:16px'><pre style='margin:0'>$h</pre></body></html>"
  $p = Join-Path $tmp "$file.html"; [IO.File]::WriteAllText($p, $html, [Text.UTF8Encoding]::new($false))
  $h2 = [Math]::Max(300, $lines * 20 + 50)
  & $edge --headless --disable-gpu --window-size=1280,$h2 --screenshot="$PSScriptRoot\capturas\$file.png" "file:///$($p -replace '\\','/')" 2>$null | Out-Null
  Start-Sleep 2
}
function Wait-Grafana { kubectl rollout status deployment/grafana-deployment --timeout=300s | Out-Null }

Cap '01-cluster' @('minikube status', 'kubectl get nodes')
Cap '02-pod-running' @('kubectl get pods -o wide', 'kubectl get svc myfirstpod')
Wait-Grafana
Cap '04-deployment-rs' @('kubectl get deployment,replicaset,pods -l app=grafana', 'kubectl get svc grafana-service')

$p = (kubectl get pods -l app=grafana -o name | Select-Object -First 1)
kubectl delete $p | Out-Null
Cap '05-self-healing' @("kubectl get pods -l app=grafana")
Wait-Grafana
kubectl scale deployment grafana-deployment --replicas=5 | Out-Null
Wait-Grafana
Cap '06-scale' @('kubectl get deployment,replicaset -l app=grafana', 'kubectl get pods -l app=grafana')
kubectl set image deployment/grafana-deployment grafana=grafana/grafana:11.0.0 | Out-Null
Wait-Grafana
Cap '07-rolling-update' @('kubectl get replicaset -l app=grafana', 'kubectl rollout history deployment/grafana-deployment')
kubectl rollout undo deployment/grafana-deployment | Out-Null
Wait-Grafana
kubectl scale deployment grafana-deployment --replicas=3 | Out-Null
Wait-Grafana
Cap '08-rollback' @('kubectl get replicaset -l app=grafana', 'kubectl get pods -l app=grafana')
Write-Host 'Listo: capturas en .\capturas'

$env:Path = [Environment]::GetEnvironmentVariable('Path','Machine') + ';' + [Environment]::GetEnvironmentVariable('Path','User')
Set-Location $PSScriptRoot
$edge = 'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
$tmp = Join-Path $env:TEMP 'k8s-cap'; New-Item -ItemType Directory -Force $tmp | Out-Null
function Cap($file, $cmds) {
  $txt = ''
  foreach ($c in $cmds) { $out = (Invoke-Expression "$c 2>&1" | Out-String); $txt += "PS C:\Users\emife\Desktop\Cluster> $c`r`n$out`r`n" }
  $h = [System.Net.WebUtility]::HtmlEncode($txt); $lines = ($txt -split "`n").Count
  $html = "<html><meta charset='utf-8'><body style='background:#0c0c0c;color:#ccc;font:15px Consolas,monospace;margin:0;padding:16px'><pre style='margin:0'>$h</pre></body></html>"
  $p = Join-Path $tmp "$file.html"; [IO.File]::WriteAllText($p, $html, [Text.UTF8Encoding]::new($false))
  & $edge --headless --disable-gpu --window-size=1400,([Math]::Max(300, $lines*20+50)) --screenshot="$PSScriptRoot\capturas\$file.png" "file:///$($p -replace '\\','/')" 2>$null | Out-Null
  Start-Sleep 2
}
kubectl rollout status deployment/grafana-deployment --timeout=300s | Out-Null
$rs = (kubectl get rs -l app=grafana -o jsonpath='{.items[?(@.spec.replicas>0)].metadata.name}')
$cols = 'OWNER-KIND:.metadata.ownerReferences[0].kind,OWNER:.metadata.ownerReferences[0].name'
Cap '10-owner-references' @('kubectl get deployment grafana-deployment', "kubectl get rs $rs -o custom-columns=RS:.metadata.name,$cols", "kubectl get pods -l app=grafana -o custom-columns=POD:.metadata.name,$cols")
kubectl apply -f .\03-replicaset-demo\replicaset-demo.yml | Out-Null
Start-Sleep 25
Cap '11-replicaset-solo' @('kubectl get rs,pods -l app=grafana-rs-demo -o wide', 'kubectl rollout history rs/grafana-rs-demo')
kubectl delete rs grafana-rs-demo | Out-Null
Write-Host 'Listo'

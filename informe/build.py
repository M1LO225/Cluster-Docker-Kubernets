# Genera Informe_Tarea_K8s_Grafana.pdf (HTML -> PDF con Edge + numeración con PyMuPDF)
# Uso: python build.py
import os, re, subprocess, html, pymupdf

ROOT = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(ROOT)
CAP = os.path.join(REPO, 'capturas')
EDGE = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
OUT = os.path.join(REPO, 'Informe_Tarea_K8s_Grafana.pdf')
STUDENT = 'Nombre del estudiante'   # <- cambia aquí tu nombre
HEADER = 'Grafana en Kubernetes · Deployment y ReplicaSet'

def read(p):
    return open(os.path.join(REPO, p), encoding='utf-8').read().rstrip()

def code(s):
    return '<pre class="code">' + html.escape(s) + '</pre>'

fig_n = [0]
def fig(name, caption, width=100):
    fig_n[0] += 1
    return (f'<div class="fig"><img src="file:///{CAP.replace(chr(92), "/")}/{name}.png" style="width:{width}%">'
            f'<div class="cap">Figura {fig_n[0]}. {caption}</div></div>')

def analisis(n, text):
    return f'<p><b>Análisis de la Figura {n}:</b> {text}</p>'

tab_n = [0]
def table(caption, head, rows, widths=None):
    tab_n[0] += 1
    h = f'<div class="tcap">Tabla {tab_n[0]}. {caption}</div><table>'
    if widths:
        h += '<colgroup>' + ''.join(f'<col style="width:{w}%">' for w in widths) + '</colgroup>'
    h += '<tr>' + ''.join(f'<th>{c}</th>' for c in head) + '</tr>'
    for r in rows:
        h += '<tr>' + ''.join(f'<td>{c}</td>' for c in r) + '</tr>'
    return h + '</table>'

# (nivel, titulo)
HEADINGS = []
def H(level, title):
    HEADINGS.append((level, title))
    return f'<h{level}>{title}</h{level}>'

def body():
    HEADINGS.clear(); fig_n[0] = 0; tab_n[0] = 0
    b = []
    a = b.append
    a(H(1, '1. Resumen ejecutivo'))
    a('<p>En este trabajo se desplegó <b>Grafana</b>, una plataforma de visualización y monitoreo, sobre un clúster local de Kubernetes (minikube). Antes de eso se creó el primer Pod de la clase (<code>myfirstpod</code>, imagen nginx) y se comprobó que respondía en el navegador. Grafana, en cambio, se gestionó con un <b>Deployment</b>, que crea y controla un <b>ReplicaSet</b> encargado de mantener tres réplicas en ejecución. La plataforma se expuso fuera del clúster con un <b>Service de tipo NodePort</b> (puerto 30300).</p>')
    a('<p>Sobre ese despliegue se hicieron cinco pruebas: relación de propiedad Deployment → ReplicaSet → Pod, autorreparación al eliminar un Pod, escalado horizontal de 3 a 5 réplicas, actualización continua de versión (10.4.2 → 11.0.0) con su reversión (<i>rollback</i>), y una comparación con un ReplicaSet creado sin Deployment. <b>Todas las pruebas funcionaron como se esperaba</b> y Grafana siguió respondiendo desde el navegador. Los manifiestos, las capturas y este informe están en el repositorio público indicado en la portada.</p>')

    a(H(1, '2. Introducción y objetivos'))
    a('<p>En clase se creó un Pod de nginx y se expuso con <code>kubectl expose pod ... --type=NodePort</code>. Un Pod suelto sirve para aprender, pero no es adecuado para un servicio real: si falla o se elimina, Kubernetes no lo vuelve a crear, no se puede escalar y no hay forma de actualizarlo sin cortar el servicio. En esta tarea se usan los controladores <b>ReplicaSet</b> y <b>Deployment</b> sobre una plataforma distinta a la vista en clase.</p>')
    a(H(2, '2.1 Objetivo general'))
    a('<p>Desplegar y exponer Grafana en un clúster de Kubernetes aplicando los conceptos de Deployment y ReplicaSet, y demostrar con evidencias su funcionamiento y sus ventajas frente a un Pod individual.</p>')
    a(H(2, '2.2 Objetivos específicos'))
    a('<ol><li>Crear el Pod de nginx de la clase y verificar su acceso desde el navegador.</li><li>Definir en archivos YAML el Deployment y el Service de Grafana.</li><li>Exponer Grafana fuera del clúster con un Service NodePort.</li><li>Evidenciar la relación de propiedad entre Deployment, ReplicaSet y Pods.</li><li>Comprobar la autorreparación, el escalado, la actualización continua y el <i>rollback</i>.</li><li>Comparar un ReplicaSet independiente con uno gestionado por un Deployment.</li><li>Identificar los usos de la plataforma y las ventajas de desplegarla de esta manera.</li></ol>')

    a(H(1, '3. Marco teórico'))
    a(H(2, '3.1 Kubernetes'))
    a('<p>Kubernetes (K8s) es una plataforma de código abierto para orquestar contenedores: automatiza su despliegue, escalado y administración. Se trabaja con una <b>configuración declarativa</b>: el usuario describe el estado deseado en un YAML y el clúster se encarga de alcanzarlo y mantenerlo.</p>')
    a(H(2, '3.2 Pod'))
    a('<p>Es la unidad básica de ejecución. Agrupa uno o más contenedores que comparten red y almacenamiento y siempre corre en un nodo. Un Pod creado directamente no se recrea si se elimina.</p>')
    a(H(2, '3.3 ReplicaSet'))
    a('<p>Garantiza que exista siempre un número determinado de Pods idénticos, seleccionados por etiquetas. Si un Pod desaparece, crea otro; si sobran, elimina los excedentes. Solo controla la <b>cantidad</b>, no las versiones.</p>')
    a(H(2, '3.4 Deployment'))
    a('<p>Es un controlador de más alto nivel que crea y administra ReplicaSets. Añade la gestión de versiones: actualización continua (<i>RollingUpdate</i>), historial de revisiones y reversión. Cada cambio en la plantilla del Pod genera un ReplicaSet nuevo y conserva el anterior para poder volver atrás.</p>')
    a(H(2, '3.5 Service'))
    a('<p>Da una dirección estable a un conjunto de Pods y reparte el tráfico entre ellos. El tipo <b>NodePort</b> abre un puerto en el nodo (rango 30000–32767) para llegar al servicio desde fuera del clúster.</p>')
    a(H(2, '3.6 Grafana'))
    a('<p>Plataforma de código abierto para crear paneles (<i>dashboards</i>) a partir de métricas, logs y otras fuentes de datos. Tiene interfaz web en el puerto 3000 y un endpoint de salud (<code>/api/health</code>).</p>')

    a(H(1, '4. Selección de la plataforma'))
    a('<p>La tarea permitía elegir entre Elasticsearch, Redis, MongoDB, Grafana u otra. Se eligió <b>Grafana</b> por tres razones: (1) tiene interfaz web, por lo que la exposición se puede demostrar con una captura en el navegador; (2) es <i>stateless</i> en su uso básico, así que se puede replicar sin volúmenes ni configuración de clúster de datos; y (3) consume pocos recursos, importante en un equipo personal con minikube. Las bases de datos como MongoDB o Elasticsearch necesitan almacenamiento persistente y suelen desplegarse con StatefulSet, que está fuera del alcance de esta tarea.</p>')

    a(H(1, '5. Entorno de trabajo'))
    a(table('Entorno y herramientas', ['Componente', 'Versión / detalle'], [
        ['Sistema operativo anfitrión', 'Windows 11 Home'],
        ['Motor de contenedores', 'Docker Desktop (motor 29.9.3, backend WSL2)'],
        ['Clúster', 'minikube v1.39.0, driver Docker, un nodo (control-plane)'],
        ['Kubernetes', 'servidor v1.37.0, cliente kubectl v1.36.1, runtime containerd 2.3.4'],
        ['IP del nodo', '192.168.49.2'],
        ['Imagen de Grafana', 'grafana/grafana:10.4.2 (actualizada a 11.0.0 en la prueba)'],
        ['Imagen de nginx', 'nginx:1.27'],
    ], [32, 68]))

    a(H(1, '6. Arquitectura de la solución'))
    a('<p>El Deployment mantiene un ReplicaSet y este, tres Pods de Grafana. El Service NodePort selecciona los Pods por la etiqueta <code>app=grafana</code> y reparte el tráfico entre ellos. Al actualizar la imagen, el Deployment crea un ReplicaSet nuevo y reduce el anterior de forma gradual.</p>')
    a('''<div class="diag">
<div class="box usr">Navegador<br><small>localhost:3000</small></div><div class="ar">→</div>
<div class="box svc">Service NodePort<br><small>grafana-service · 30300 → 3000</small></div><div class="ar">→</div>
<div class="stack"><div class="box dep">Deployment<br><small>grafana-deployment</small></div><div class="ar v">↓</div><div class="box rs">ReplicaSet<br><small>grafana-deployment-69cf9745b8</small></div><div class="ar v">↓</div><div class="pods"><div class="box pod">Pod 1</div><div class="box pod">Pod 2</div><div class="box pod">Pod 3</div></div></div>
</div><div class="cap">Figura 1. Arquitectura: Service → Deployment → ReplicaSet → Pods</div>''')
    fig_n[0] += 1

    a(H(1, '7. Configuración de los manifiestos'))
    a(H(2, '7.1 Pod de nginx (clase)'))
    a('<p>Archivo <code>01-pod/first_pod_nginx.yml</code>. Define un Pod con un único contenedor nginx en el puerto 80.</p>')
    a(code(read('01-pod/first_pod_nginx.yml')))
    a(H(2, '7.2 Deployment'))
    a('<p>Archivo <code>02-grafana/grafana-deployment.yml</code>. Define 3 réplicas, la estrategia <i>RollingUpdate</i> (máximo 1 Pod no disponible y 1 adicional durante el cambio), límites de recursos y una <i>readiness probe</i> sobre <code>/api/health</code>, de modo que un Pod solo recibe tráfico cuando Grafana ya responde.</p>')
    a(code(read('02-grafana/grafana-deployment.yml')))
    a(H(2, '7.3 Service NodePort'))
    a('<p>Archivo <code>02-grafana/grafana-service.yml</code>. Selecciona los Pods con <code>app: grafana</code> y los publica en el puerto 30300 del nodo.</p>')
    a(code(read('02-grafana/grafana-service.yml')))
    a(H(2, '7.4 ReplicaSet independiente (solo para comparación)'))
    a('<p>Archivo <code>03-replicaset-demo/replicaset-demo.yml</code>. Es un ReplicaSet creado directamente, sin Deployment, con 2 réplicas de Grafana 10.4.2. Se usó solo para la prueba de comparación y se eliminó después.</p>')
    a(code(read('03-replicaset-demo/replicaset-demo.yml')))

    a(H(1, '8. Desarrollo y evidencias'))
    a(H(2, '8.1 Clúster'))
    a('<p>Con Docker Desktop en funcionamiento se inició el clúster con <code>minikube start --driver=docker</code> y se comprobó el estado del nodo.</p>')
    a(fig('01-cluster', 'Estado de minikube y del nodo', 85))
    a(analisis(fig_n[0], 'minikube muestra el plano de control, el kubelet y el API server en <code>Running</code>, y <code>kubectl get nodes</code> lista un nodo <code>minikube</code> en estado <code>Ready</code> con la versión v1.37.0. El clúster está listo para recibir los recursos.'))
    a(H(2, '8.2 Primer Pod (nginx)'))
    a('<p>Se aplicó el YAML con <code>kubectl apply -f first_pod_nginx.yml</code> y se expuso con <code>kubectl expose pod myfirstpod --type=NodePort --port=80</code>, tal como se hizo en clase.</p>')
    a(fig('02-pod-running', 'Pod myfirstpod en ejecución y su Service NodePort', 100))
    a(analisis(fig_n[0], '<code>myfirstpod</code> está en <code>1/1 Running</code>, con IP interna 10.244.0.18 dentro del nodo <code>minikube</code>. El Service <code>myfirstpod</code> es de tipo NodePort y publica el puerto 80 en el 31591. (En la misma captura aparecen también tres Pods de Grafana, ya desplegados en ese momento.)'))
    a(fig('03-nginx-welcome', 'Página de bienvenida de nginx servida por el Pod', 80))
    a(analisis(fig_n[0], 'el navegador muestra «Welcome to nginx!», lo que confirma que el Pod responde y que el Service lo expone. Como el driver Docker en Windows no permite llegar a la IP del nodo directamente, el acceso para la captura se hizo con <code>kubectl port-forward</code> hacia <code>localhost:8081</code>.'))
    a(H(2, '8.3 Despliegue de Grafana'))
    a('<p>Se aplicaron los dos manifiestos con <code>kubectl apply -f .\\02-grafana\\</code> y se esperó con <code>kubectl rollout status</code> a que las réplicas estuvieran listas.</p>')
    a(fig('04-deployment-rs', 'Deployment, ReplicaSet, Pods y Service de Grafana', 90))
    a(analisis(fig_n[0], 'el Deployment <code>grafana-deployment</code> muestra <code>3/3</code> listos y disponibles. Existe un ReplicaSet activo (<code>grafana-deployment-69cf9745b8</code>) con 3 réplicas deseadas, actuales y listas, y otro anterior con 0 réplicas (consecuencia de pruebas posteriores). Los tres Pods están en <code>Running</code> y el Service <code>grafana-service</code> es NodePort <code>3000:30300</code>.'))
    a(H(2, '8.4 Exposición y acceso a la plataforma'))
    a(fig('09-grafana-web', 'Pantalla de inicio de sesión de Grafana v10.4.2', 85))
    a(analisis(fig_n[0], 'el navegador abre la pantalla «Welcome to Grafana» y el pie de página indica la versión v10.4.2, la misma imagen definida en el Deployment. Esto demuestra la cadena navegador → Service NodePort 30300 → Pod :3000. Para esta captura el acceso se hizo con <code>kubectl port-forward svc/grafana-service 3000:3000</code>; también funciona con <code>minikube service grafana-service</code>. Las credenciales iniciales son las predeterminadas de Grafana (<code>admin</code>/<code>admin</code>), válidas solo para este laboratorio.'))
    a(H(2, '8.5 Relación Deployment → ReplicaSet → Pod'))
    a('<p>Cada objeto guarda en <code>ownerReferences</code> quién es su dueño. Se consultó esa propiedad en el ReplicaSet y en los Pods.</p>')
    a(fig('10-owner-references', 'Propietarios (ownerReferences) del ReplicaSet y de los Pods', 100))
    a(analisis(fig_n[0], 'el ReplicaSet <code>grafana-deployment-69cf9745b8</code> tiene como propietario al Deployment <code>grafana-deployment</code>, y los tres Pods tienen como propietario a ese ReplicaSet. La cadena de propiedad se confirma, y por eso al borrar el Deployment se borran también sus ReplicaSets y Pods.'))
    a(H(2, '8.6 Autorreparación (ReplicaSet)'))
    a('<p>Se eliminó un Pod con <code>kubectl delete pod</code> y se listaron los Pods inmediatamente.</p>')
    a(fig('05-self-healing', 'Pod nuevo creado tras eliminar uno', 85))
    a(analisis(fig_n[0], 'a pesar de haber eliminado un Pod, siguen existiendo tres. Dos tienen más de 80 s de vida y el tercero, <code>…-rcxgl</code>, tiene 1 s y todavía está en <code>0/1</code>: es el reemplazo que creó el ReplicaSet. Pasa a <code>1/1</code> cuando la <i>readiness probe</i> confirma que Grafana responde. Un Pod suelto como el de nginx no se habría recreado.'))
    a(H(2, '8.7 Escalado horizontal'))
    a('<p>Se escaló con <code>kubectl scale deployment grafana-deployment --replicas=5</code>.</p>')
    a(fig('06-scale', 'Escalado del Deployment de 3 a 5 réplicas', 95))
    a(analisis(fig_n[0], 'el Deployment pasa a <code>5/5</code> y el mismo ReplicaSet (<code>69cf9745b8</code>) sube a 5 réplicas deseadas, actuales y listas. Los dos Pods nuevos tienen 13 s de vida. No se creó ningún ReplicaSet nuevo, porque cambiar el número de réplicas no modifica la plantilla del Pod.'))
    a(H(2, '8.8 Actualización continua (RollingUpdate)'))
    a('<p>Se cambió la imagen con <code>kubectl set image deployment/grafana-deployment grafana=grafana/grafana:11.0.0</code> y se esperó con <code>kubectl rollout status</code>.</p>')
    a(fig('07-rolling-update', 'ReplicaSets e historial tras la actualización a 11.0.0', 95))
    a(analisis(fig_n[0], 'la actualización dejó activo el ReplicaSet <code>547db96b99</code> (imagen 11.0.0) con 5/5 réplicas y el ReplicaSet anterior (<code>69cf9745b8</code>) con 0, pero conservado. El historial lista las revisiones 3 y 4. Durante el cambio, con <code>maxSurge: 1</code> y <code>maxUnavailable: 1</code>, los Pods se reemplazaron de uno en uno sin dejar el servicio sin réplicas.'))
    a(H(2, '8.9 Reversión (rollback)'))
    a('<p>Se volvió a la versión anterior con <code>kubectl rollout undo deployment/grafana-deployment</code> y se redujo de nuevo a 3 réplicas.</p>')
    a(fig('08-rollback', 'Estado tras el rollback y el escalado a 3 réplicas', 95))
    a(analisis(fig_n[0], 'el ReplicaSet <code>69cf9745b8</code> (Grafana 10.4.2) vuelve a tener las réplicas activas (3/3) y el de 11.0.0 queda en 0. Se reutilizó el ReplicaSet existente en lugar de crear uno nuevo. Los Pods en <code>Completed</code> son los que se retiraron del conjunto durante el cambio y el escalado, y desaparecen después.'))
    a(H(2, '8.10 Comparación: ReplicaSet sin Deployment'))
    a('<p>Se creó un ReplicaSet directamente con el archivo <code>replicaset-demo.yml</code> y se consultó su historial.</p>')
    a(fig('11-replicaset-solo', 'ReplicaSet independiente y su historial', 100))
    a(analisis(fig_n[0], 'el ReplicaSet <code>grafana-rs-demo</code> mantiene 2 Pods de Grafana 10.4.2 (2/2 listos). Sin embargo, <code>kubectl rollout history</code> responde «no history viewer has been implemented for ReplicaSet.apps»: un ReplicaSet no guarda revisiones ni permite <i>rollback</i>. Si se cambiara la imagen de su plantilla, solo afectaría a los Pods creados después, lo que dejaría versiones mezcladas. Por eso en la práctica se usa un Deployment y no ReplicaSets directos.'))

    a(H(1, '9. Resultados'))
    ok = '✓'
    a(table('Resumen de pruebas', ['N.º', 'Prueba', 'Resultado esperado', 'Resultado obtenido', 'Estado'], [
        ['1', 'Pod nginx', 'Pod Running y página de nginx', 'myfirstpod 1/1 Running; «Welcome to nginx!»', ok],
        ['2', 'Despliegue', 'Deployment 3/3, ReplicaSet y Service creados', 'Deployment 3/3, RS 69cf9745b8, NodePort 3000:30300', ok],
        ['3', 'Exposición', 'Grafana accesible desde el navegador', 'Pantalla de login de Grafana v10.4.2', ok],
        ['4', 'Propiedad de objetos', 'Deployment → ReplicaSet → Pod', 'ownerReferences confirman la cadena', ok],
        ['5', 'Autorreparación', 'El Pod eliminado se reemplaza', 'Pod nuevo creado en 1 s; siempre 3 Pods', ok],
        ['6', 'Escalado', '5 réplicas con el mismo ReplicaSet', 'RS 69cf9745b8 con 5/5', ok],
        ['7', 'RollingUpdate', 'Nuevo RS con 11.0.0, sin caída', 'RS 547db96b99 5/5; anterior con 0; revisiones 3 y 4', ok],
        ['8', 'Rollback', 'Volver a 10.4.2', 'Se reactivó RS 69cf9745b8 con 3/3', ok],
        ['9', 'ReplicaSet solo', 'No guarda historial', '«no history viewer… for ReplicaSet.apps»', ok],
    ], [6, 17, 28, 39, 10]))

    a(H(1, '10. Usos de la plataforma'))
    a(H(2, '10.1 Casos de uso de Grafana'))
    a('<ul><li><b>Monitoreo de infraestructura:</b> paneles de CPU, memoria y red de servidores y clústeres, normalmente con Prometheus como fuente de datos.</li><li><b>Observabilidad de aplicaciones:</b> métricas, logs (Loki) y trazas (Tempo) en un mismo lugar.</li><li><b>Alertas:</b> avisos por correo, Slack u otros canales cuando una métrica pasa un umbral.</li><li><b>Paneles de negocio:</b> visualización de datos de bases de datos como MySQL, PostgreSQL o Elasticsearch.</li><li><b>Monitoreo de pipelines CI/CD:</b> tiempos de despliegue, tasa de fallos y frecuencia de entregas, relacionado con el despliegue continuo visto en clase.</li></ul>')
    a(H(2, '10.2 Aporte de Deployment y ReplicaSet a estos usos'))
    a(table('Ventajas de desplegar con Deployment y ReplicaSet', ['Necesidad', 'Cómo la resuelven'], [
        ['Alta disponibilidad', 'El ReplicaSet mantiene N réplicas y recrea las que fallan (prueba 5).'],
        ['Más carga de usuarios', 'Escalado con <code>kubectl scale</code> o con un HPA según CPU (prueba 6).'],
        ['Actualizar sin cortar el servicio', 'RollingUpdate reemplaza los Pods gradualmente (prueba 7).'],
        ['Volver atrás ante un error', '<code>rollout undo</code> reactiva el ReplicaSet anterior (prueba 8).'],
        ['Reparto de tráfico', 'El Service balancea entre todas las réplicas listas.'],
        ['Trazabilidad', '<code>rollout history</code> guarda las revisiones; encaja en un pipeline de CD.'],
    ], [32, 68]))

    a(H(1, '11. Dificultades encontradas y soluciones'))
    a(table('Dificultades y soluciones', ['Situación', 'Causa', 'Solución aplicada'], [
        ['Docker Desktop no se instalaba: «Installation failed. One prerequisite is not fulfilled»', 'Faltaba WSL y la plataforma de máquina virtual de Windows; la instalación por usuario no puede activarlas.', 'Ejecutar <code>wsl --install --no-distribution</code> como administrador, reiniciar y reinstalar con «All-users installation».'],
        ['<code>docker</code>, <code>kubectl</code> y <code>minikube</code> «no se reconocen» justo después de instalarlos', 'La sesión de PowerShell abierta tenía el PATH anterior a la instalación.', 'Recargar el PATH desde el registro de Windows o abrir una terminal nueva.'],
        ['La IP 192.168.49.2 no abre desde Windows', 'Con el driver Docker el nodo está en una red interna de Docker no accesible desde el anfitrión.', 'Usar <code>minikube service</code> o <code>kubectl port-forward</code> (la terminal debe quedar abierta).'],
        ['En una primera ejecución <code>myfirstpod</code> ya no existía al volver a comprobar', 'Un Pod suelto no tiene controlador que lo recree si desaparece (justo la limitación que motiva la tarea).', 'Se volvió a crear con <code>kubectl apply</code> y se tomaron las capturas después.'],
        ['Caracteres raros («Ã³») en las capturas de consola', 'El script se leyó con la codificación equivocada por la tilde en el nombre de la carpeta.', 'Se quitó la ruta con tilde del texto que se imprime en las capturas.'],
    ], [30, 34, 36]))

    a(H(1, '12. Conclusiones'))
    a('<ul><li>Un Pod suelto, como el de nginx, funciona pero no se recupera ni se puede escalar. El ReplicaSet resuelve la cantidad de réplicas y el Deployment añade el manejo de versiones.</li><li>La autorreparación se vio en la práctica: al eliminar un Pod de Grafana, el ReplicaSet creó otro en un segundo y el servicio no se interrumpió.</li><li>El Deployment crea un ReplicaSet por cada versión y conserva los anteriores, lo que hace posible el <i>rollback</i> inmediato.</li><li>Un ReplicaSet creado solo no guarda historial, por lo que en la práctica conviene siempre usar Deployments.</li><li>Con el driver Docker en Windows hay que usar túnel o <i>port-forward</i> para llegar a los Services desde el navegador.</li></ul>')

    a(H(1, '13. Recomendaciones y trabajo futuro'))
    a('<ul><li>Guardar la configuración de Grafana (fuentes de datos y paneles) en un ConfigMap y las credenciales en un Secret, en vez de usar las predeterminadas.</li><li>Añadir un volumen persistente si se quieren conservar los paneles creados desde la interfaz.</li><li>Configurar un HorizontalPodAutoscaler para escalar según la CPU.</li><li>Conectar Prometheus como fuente de datos y mostrar métricas reales del clúster.</li><li>Automatizar el despliegue con un pipeline de CD (por ejemplo GitHub Actions), siguiendo lo visto en la asignatura.</li></ul>')

    a(H(1, '14. Referencias'))
    a('<ul><li>Material de clase: «Intro Kubernetes K8S», «Intro Docker» e «Intro Entrega Continua (CD)».</li><li>Kubernetes Documentation. Deployments. https://kubernetes.io/docs/concepts/workloads/controllers/deployment/</li><li>Kubernetes Documentation. ReplicaSet. https://kubernetes.io/docs/concepts/workloads/controllers/replicaset/</li><li>Kubernetes Documentation. Service. https://kubernetes.io/docs/concepts/services-networking/service/</li><li>minikube Documentation. https://minikube.sigs.k8s.io/docs/</li><li>Grafana Labs. Grafana documentation. https://grafana.com/docs/grafana/latest/</li></ul>')

    a(H(1, 'Anexo A. Estructura del repositorio'))
    a(code('''Cluster-Docker-Kubernets/
├── 01-pod/first_pod_nginx.yml
├── 02-grafana/
│   ├── grafana-deployment.yml
│   └── grafana-service.yml
├── 03-replicaset-demo/replicaset-demo.yml
├── capturas/                  (evidencias 01 a 11)
├── informe/                   (logo y script que genera este PDF)
├── ejecutar-todo.ps1          (crea el Pod, Grafana y las pruebas)
├── generar-capturas.ps1       (capturas de consola 01 a 08)
├── generar-capturas-extra.ps1 (capturas 10 y 11)
├── LEEME-DOCKER.md
├── INFORME.md
└── Informe_Tarea_K8s_Grafana.pdf'''))
    a(H(1, 'Anexo B. Guía rápida de ejecución'))
    a(code('''# 1. Con Docker Desktop abierto, en la carpeta del repositorio:
powershell -ExecutionPolicy Bypass -File .\\ejecutar-todo.ps1

# 2. Acceder a las aplicaciones
kubectl port-forward pod/myfirstpod 8081:80            # http://localhost:8081
kubectl port-forward svc/grafana-service 3000:3000     # http://localhost:3000

# 3. Limpiar
kubectl delete -f .\\02-grafana\\
kubectl delete pod,svc myfirstpod
minikube stop'''))
    return '\n'.join(b)

CSS = '''
@page { size: A4; margin: 25mm 25mm 25mm 25mm; }
body { font-family: Calibri, 'Segoe UI', sans-serif; font-size: 11pt; color:#000; line-height:1.3; margin:0; }
p, li { text-align: justify; }
h1 { color:#A30F2D; font-size:16pt; margin:22px 0 8px; break-after: avoid; }
h2 { color:#A30F2D; font-size:13pt; margin:16px 0 6px; break-after: avoid; }
code { font-family: Consolas, monospace; font-size:9.5pt; color:#8B102A; }
pre.code { font-family: Consolas, monospace; font-size:8.5pt; background:#F2F2F2; border:1px solid #DDD; padding:8px 10px; white-space:pre-wrap; margin:6px 0 10px; color:#222; break-inside: avoid; }
table { border-collapse:collapse; width:100%; font-size:10pt; margin:2px 0 14px; }
th { background:#A30F2D; color:#fff; text-align:left; padding:5px 8px; }
td { padding:5px 8px; border-bottom:1px solid #E5E5E5; vertical-align:top; }
tr:nth-child(even) td { background:#FBEFF1; }
tr { break-inside: avoid; }
.tcap { font-weight:bold; font-size:10pt; color:#555; margin:10px 0 4px; break-after: avoid; }
.fig { text-align:center; margin:10px 0 8px; break-inside: avoid; }
.fig img { border:1px solid #CCC; }
.cap { font-size:9pt; font-style:italic; color:#555; margin-top:3px; text-align:center; }
.cover { text-align:center; page-break-after: always; padding-top:20px; }
.cover img.logo { width:200px; margin-top:20px; }
.cover .fac { font-weight:bold; font-size:13pt; color:#555; margin-top:30px; }
.cover .sub { font-size:12pt; color:#555; margin-top:4px; }
.cover h1.t { font-size:26pt; color:#A30F2D; margin:50px 0 6px; padding-bottom:10px; border-bottom:2px solid #B9C7DC; line-height:1.15; }
.cover .desc { font-style:italic; font-size:13pt; margin:10px 30px 60px; }
.meta { width:80%; margin:0 auto; text-align:left; }
.meta td { border:0; background:none !important; padding:4px 10px 4px 0; font-size:11pt; }
.meta td:first-child { color:#A30F2D; font-weight:bold; width:25%; }
.toc { page-break-after: always; }
.toc h1 { margin-top:0; }
.toc .l { display:flex; align-items:baseline; font-size:10.5pt; margin:3px 0; }
.toc .l .d { flex:1; border-bottom:1px dotted #888; margin:0 6px; }
.toc .l2 { padding-left:18px; }
.diag { display:flex; align-items:center; justify-content:center; gap:8px; margin:10px 0 2px; font-size:10pt; }
.box { border:1.5px solid #A30F2D; border-radius:6px; padding:7px 9px; text-align:center; background:#FBEFF1; }
.box small { color:#555; font-size:8pt; }
.usr { background:#eee; border-color:#888; } .pod { background:#fff; padding:6px 8px; }
.ar { font-size:18pt; color:#A30F2D; } .ar.v { text-align:center; font-size:14pt; line-height:1; }
.stack { display:flex; flex-direction:column; align-items:center; gap:2px; }
.pods { display:flex; gap:6px; }
'''

def toc_html(pages):
    out = ['<div class="toc"><h1>Contenido</h1>']
    for lvl, t in HEADINGS:
        pg = pages.get(t, '')
        cls = 'l l2' if lvl == 2 else 'l'
        out.append(f'<div class="{cls}"><span>{t}</span><span class="d"></span><span>{pg}</span></div>')
    out.append('</div>')
    return '\n'.join(out)

def cover():
    logo = f'file:///{ROOT.replace(chr(92), "/")}/logo.png'
    return f'''<div class="cover"><img class="logo" src="{logo}">
<div class="fac">FACULTAD DE INGENIERÍA Y CIENCIAS APLICADAS</div>
<div class="sub">Informe técnico sobre la configuración de clusters</div>
<h1 class="t">Despliegue de Grafana en Kubernetes con Deployment y ReplicaSet</h1>
<div class="desc">Configuración, exposición y verificación de alta disponibilidad, escalado, actualización continua y rollback en un clúster minikube</div>
<table class="meta"><tr><td>Estudiante</td><td>{STUDENT}</td></tr><tr><td>Asignatura</td><td>Procesos de Software</td></tr><tr><td>Docente</td><td>Mónica Sánchez</td></tr><tr><td>Fecha</td><td>14 de noviembre de 2026</td></tr><tr><td>Repositorio</td><td>https://github.com/M1LO225/Cluster-Docker-Kubernets</td></tr></table></div>'''

def render(pages):
    b = body()
    doc = f'<!doctype html><html><head><meta charset="utf-8"><title>Informe K8s Grafana</title><style>{CSS}</style></head><body>{cover()}{toc_html(pages)}{b}</body></html>'
    p = os.path.join(ROOT, '_informe.html')
    open(p, 'w', encoding='utf-8').write(doc)
    tmp = os.path.join(ROOT, '_raw.pdf')
    subprocess.run([EDGE, '--headless', '--disable-gpu', '--no-pdf-header-footer', f'--print-to-pdf={tmp}', 'file:///' + p.replace('\\', '/')],
                   stderr=subprocess.DEVNULL, check=True)
    return tmp

def find_pages(pdf):
    d = pymupdf.open(pdf); pages = {}
    for t, _ in [(h[1], h[0]) for h in HEADINGS]:
        key = re.sub(r'<[^>]+>', '', t)
        for i in range(2, len(d)):   # saltar portada e índice
            txt = d[i].get_text()
            if any(line.strip() == html.unescape(key) for line in txt.splitlines()):
                pages[t] = i + 1; break
    return pages

if __name__ == '__main__':
    render({})                       # pasada 1: calcular el índice
    tmp = os.path.join(ROOT, '_raw.pdf')
    # el índice ocupa páginas fijas (portada=1, contenido=2..n); se calcula con la pasada 1 y se repite
    pages = find_pages(tmp)
    render(pages)
    pages2 = find_pages(tmp)
    if pages2 != pages:
        render(pages2)
    d = pymupdf.open(tmp)
    for i, pg in enumerate(d):
        if i == 0:
            continue
        r = pg.rect
        txt = f'{HEADER}   |   Página {i+1}'
        tw = pymupdf.get_text_length(txt, fontname='helv', fontsize=8.5)
        pg.insert_text(((r.width - tw) / 2 + 150, r.height - 30), txt, fontname='helv', fontsize=8.5, color=(0.33, 0.33, 0.33))
    d.save(OUT)
    print('OK', OUT, len(d), 'paginas')
    for f in ('_informe.html', '_raw.pdf'):
        try: os.remove(os.path.join(ROOT, f))
        except OSError: pass

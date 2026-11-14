# Arreglar el error de instalación de Docker Desktop

Causa: Windows no tiene WSL ni la "Plataforma de máquina virtual", y la instalación
"por usuario" no puede activarlos (requiere administrador).

## Solución (elige UNA)
**A) Recomendada**
1. Abre PowerShell **como administrador** (clic derecho > Ejecutar como administrador).
2. Ejecuta: `wsl --install --no-distribution`
3. **Reinicia el PC.**
4. Vuelve a ejecutar el instalador de Docker Desktop y elige **"All-users installation"**.

**B)** Ejecuta el instalador y elige "All-users installation" (activa la función solo, pide permisos de administrador y reinicia).

## Si sigue fallando
- Activa la virtualización en la BIOS/UEFI (Intel VT-x / AMD SVM) y revisa en el Administrador de tareas > Rendimiento > CPU que diga "Virtualización: Habilitada".
- Comprueba con `wsl --status` y `wsl --update`.

## Después
Abre Docker Desktop (espera a que diga "Engine running") y ejecuta `ejecutar-todo.ps1`.

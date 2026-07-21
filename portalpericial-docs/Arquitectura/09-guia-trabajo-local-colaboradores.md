# Guía de trabajo local para colaboradores

## Portal Pericial

Esta guía explica cómo preparar una computadora para trabajar localmente en Portal Pericial y cómo enviar cambios mediante GitHub.

Está dirigida a una persona que ya tiene Visual Studio Code instalado y conoce las operaciones básicas de Git.

---

# 1. Reglas de trabajo

- El código fuente oficial se encuentra en GitHub.
- Los cambios se realizan localmente, no directamente en producción.
- No se trabaja dentro de `htdocs`.
- No se comparte la clave privada SSH.
- No se agregan archivos `.env` al repositorio.
- Cada cambio se realiza en una rama propia.
- Los cambios se integran mediante un Pull Request.
- El despliegue a producción se realiza después de revisar y unir el Pull Request.

---

# 2. Herramientas necesarias

Verificar desde PowerShell:

```powershell
git --version
code --version
python --version
ssh -V
```

Versiones utilizadas por el proyecto:

- Python 3.12.
- Git actualizado.
- Visual Studio Code.
- OpenSSH incluido en Windows 11.

Si `python` no se reconoce, instalar Python 3.12 y marcar durante la instalación:

```text
Add Python to PATH
```

Extensiones recomendadas para Visual Studio Code:

- Python, publicada por Microsoft.
- Pylance, publicada por Microsoft.

---

# 3. Acceso a GitHub

El colaborador debe utilizar su propia cuenta de GitHub.

La persona administradora del repositorio debe agregarlo como colaborador en:

```text
GitHub → Repository → Settings → Collaborators
```

El colaborador debe aceptar la invitación antes de intentar publicar una rama.

Configurar su identidad de Git:

```powershell
git config --global user.name "Nombre Apellido"
git config --global user.email "correo-utilizado-en-github@example.com"
```

Verificar:

```powershell
git config --global user.name
git config --global user.email
```

---

# 4. Clonar el proyecto

## Opción A - Desde Visual Studio Code

1. Abrir Visual Studio Code.
2. Presionar `Ctrl + Shift + P`.
3. Ejecutar `Git: Clone`.
4. Pegar:

```text
https://github.com/marianagil68/cursoperitos.git
```

5. Elegir una carpeta local.
6. Abrir el repositorio clonado cuando Visual Studio Code lo solicite.

## Opción B - Desde PowerShell

```powershell
cd C:\ruta\donde\guardar\el\proyecto

git clone https://github.com/marianagil68/cursoperitos.git

cd cursoperitos

code .
```

---

# 5. Estructura principal

```text
cursoperitos/
├── LandingPage/
│   ├── index.html
│   ├── gracias.html
│   ├── assets/
│   ├── css/
│   └── js/
│
├── PortalPericial/
│   ├── app/
│   ├── tests/
│   ├── requirements.txt
│   └── run.py
│
└── portalpericial-docs/
```

- `LandingPage`: frontend público.
- `PortalPericial`: backend Flask.
- `portalpericial-docs`: documentación técnica.

---

# 6. Preparar Python

Abrir una terminal de PowerShell en Visual Studio Code:

```text
Terminal → New Terminal
```

Ejecutar:

```powershell
cd PortalPericial

python -m venv .venv

.\.venv\Scripts\Activate.ps1

python -m pip install --upgrade pip

pip install -r requirements.txt
```

Cuando el entorno está activo, la terminal muestra normalmente:

```text
(.venv)
```

## Si PowerShell no permite activar el entorno

Si aparece un error relacionado con la ejecución de scripts, consultar primero con la persona administradora del equipo.

La configuración habitual para el usuario actual es:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

Después cerrar y volver a abrir PowerShell.

---

# 7. Archivo privado `.env`

El backend necesita un archivo:

```text
PortalPericial/.env
```

Este archivo contiene credenciales de PostgreSQL y SMTP.

Debe recibirse mediante un canal seguro, por ejemplo:

- gestor de contraseñas;
- archivo cifrado;
- transferencia directa acordada con la administradora.

Nunca debe:

- enviarse a GitHub;
- incluirse en un commit;
- pegarse en documentación;
- compartirse en un chat público.

Verificar que Git lo ignore:

```powershell
git status --short
```

El archivo `.env` no debe aparecer en la salida.

---

# 8. Acceso SSH propio

Cada colaborador debe tener su propia clave SSH. No se comparte la clave de otra persona.

Crear una clave:

```powershell
ssh-keygen -t ed25519 -C "nombre-colaborador-portalpericial"
```

Archivos generados:

```text
C:\Users\USUARIO\.ssh\id_ed25519
C:\Users\USUARIO\.ssh\id_ed25519.pub
```

- `id_ed25519` es privada y nunca debe compartirse.
- `id_ed25519.pub` es pública y debe enviarse a la administradora del servidor.

La administradora asignará un usuario SSH propio.

Hasta que ese usuario exista, no debe utilizarse el acceso de `root` ni la clave privada de otra persona.

---

# 9. Abrir el túnel de PostgreSQL

El backend local utiliza el puerto local `5433` para acceder a PostgreSQL mediante SSH.

Abrir una terminal exclusiva para el túnel:

```powershell
ssh -N -L 5433:127.0.0.1:5432 -p 5650 USUARIO_SSH@149.50.152.230
```

Reemplazar `USUARIO_SSH` por el usuario asignado por la administradora.

La terminal permanece abierta y normalmente no muestra mensajes.

Mientras esa ventana esté abierta:

```text
localhost:5433 → PostgreSQL del servidor
```

Para cerrar el túnel:

```text
Ctrl + C
```

---

# 10. Ejecutar el backend

Abrir una segunda terminal:

```powershell
cd C:\ruta\cursoperitos\PortalPericial

.\.venv\Scripts\Activate.ps1

python run.py
```

El backend queda disponible en:

```text
http://127.0.0.1:5000
```

Prueba rápida:

```text
http://127.0.0.1:5000/api/eventos
```

Para detenerlo:

```text
Ctrl + C
```

---

# 11. Ejecutar la landing

Abrir una tercera terminal:

```powershell
cd C:\ruta\cursoperitos\LandingPage

python -m http.server 8080 --bind 127.0.0.1
```

Abrir:

```text
http://127.0.0.1:8080
```

Para detenerla:

```text
Ctrl + C
```

---

# 12. Ejecutar las pruebas automáticas

Con el entorno virtual activo:

```powershell
cd C:\ruta\cursoperitos\PortalPericial

python -m pytest -q
```

Las pruebas automáticas actuales no deben enviar correos reales.

No continuar con un commit si alguna prueba falla.

---

# 13. Crear una rama de trabajo

Antes de comenzar:

```powershell
cd C:\ruta\cursoperitos

git switch main

git pull --ff-only

git switch -c feature/descripcion-corta
```

Ejemplos:

```text
feature/mejora-formulario
feature/nueva-charla
fix/error-validacion-email
docs/actualiza-guia
```

No trabajar directamente sobre `main` cuando participan varias personas.

---

# 14. Guardar los cambios

Revisar:

```powershell
git status
git diff
```

Preparar solamente los archivos relacionados:

```powershell
git add ruta-del-archivo
```

Ejemplos:

```powershell
git add LandingPage
git add PortalPericial
git add portalpericial-docs
```

Crear el commit:

```powershell
git commit -m "Describe brevemente el cambio"
```

Publicar la rama:

```powershell
git push -u origin feature/descripcion-corta
```

La primera publicación puede solicitar autenticación en GitHub.

---

# 15. Crear un Pull Request

Desde GitHub:

1. Abrir el repositorio.
2. Seleccionar la rama publicada.
3. Elegir `Compare & pull request`.
4. Explicar qué se modificó.
5. Indicar cómo se probó.
6. Solicitar revisión.

No desplegar el cambio antes de que el Pull Request sea aprobado e integrado en `main`.

---

# 16. Actualizar una rama existente

Si `main` recibió cambios mientras se trabajaba:

```powershell
git switch main
git pull --ff-only
git switch feature/descripcion-corta
git merge main
```

Si aparecen conflictos, resolverlos con cuidado y volver a ejecutar las pruebas.

No utilizar:

```text
git reset --hard
```

sin comprender exactamente qué cambios se perderán.

---

# 17. Advertencia sobre datos y correos reales

El entorno local actual se conecta a la base de datos real y utiliza el SMTP real.

Una prueba manual puede:

- crear personas;
- crear inscripciones;
- crear auditorías;
- enviar correos al administrador;
- enviar correos al participante.

Antes de probar formularios manualmente:

- coordinar la prueba;
- utilizar una dirección controlada;
- usar alias de Gmail si corresponde, por ejemplo `nombre+prueba1@gmail.com`;
- recordar que cada alias es considerado un correo diferente por el backend;
- evitar datos personales de terceros.

Las pruebas automáticas con `pytest` utilizan simulaciones y no deben enviar correos.

---

# 18. Lo que no debe hacerse

- No editar directamente `htdocs`.
- No trabajar como `root`.
- No compartir claves privadas SSH.
- No publicar `.env`.
- No agregar contraseñas al código.
- No modificar producción antes de integrar el cambio en `main`.
- No hacer `push --force` sobre `main`.
- No instalar dependencias sin actualizar `requirements.txt`.
- No enviar correos reales sin avisar.

---

# 19. Lista de verificación antes de un Pull Request

- [ ] La rama comenzó desde un `main` actualizado.
- [ ] Los cambios corresponden a una sola tarea.
- [ ] No aparece `.env` en `git status`.
- [ ] No se incluyeron contraseñas ni claves.
- [ ] La landing fue probada localmente si cambió el frontend.
- [ ] El backend fue probado si cambió Python.
- [ ] `python -m pytest -q` finaliza correctamente.
- [ ] La documentación fue actualizada si cambió el funcionamiento.
- [ ] El mensaje del commit describe el cambio.
- [ ] El Pull Request explica cómo se verificó.

---

# 20. Flujo resumido de cada jornada

```text
Actualizar main
        ↓
Crear una rama
        ↓
Abrir túnel SSH
        ↓
Levantar backend y landing
        ↓
Modificar y probar
        ↓
Ejecutar pytest
        ↓
Commit
        ↓
Push de la rama
        ↓
Pull Request
        ↓
Revisión
        ↓
Integración en main
        ↓
Despliegue controlado
```

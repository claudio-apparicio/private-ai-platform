# FND-1 — Entorno de desarrollo (Windows)

Fecha: 2026-11-18  
Tarea: preparar el entorno de desarrollo en Windows.  
Git no se inicializó en este paso.

## Versiones

| Componente | Versión | Detalle |
| --- | --- | --- |
| Windows | 10.0.26200 (build 26200) | Microsoft Windows 11 Pro for Workstations, 64 bits |
| WSL | 3.0.5.0 | Kernel 6.18.58.1-1; WSLg 1.0.79; versión predeterminada 2; distribución predeterminada `docker-desktop` |
| Git | 2.54.0.windows.1 | Disponible en PATH; repositorio todavía no inicializado |
| Python | 3.14.5 | `py -3.14` → `C:\Python314\python.exe` |
| Docker | 29.9.3 | Cliente y servidor; contexto `desktop-linux` |
| Cursor | 3.27.22 | Commit `b1aa50cb6db84fd3e8c808259cb172ea73425c10`, x64 |

## Paso 2 — `docker run --rm hello-world`

```text
Unable to find image 'hello-world:latest' locally
latest: Pulling from library/hello-world
4f55086f7dd0: Pulling fs layer
4f55086f7dd0: Download complete
4f55086f7dd0: Pull complete
d5e71e642bf5: Download complete
Digest: sha256:1e4c05b897a751332ce85c7e9449da2d93514ea2dea6dbb0e2753c9e949b2bfa
Status: Downloaded newer image for hello-world:latest

Hello from Docker!
This message shows that your installation appears to be working correctly.

To generate this message, Docker took the following steps:
 1. The Docker client contacted the Docker daemon.
 2. The Docker daemon pulled the "hello-world" image from the Docker Hub.
    (amd64)
 3. The Docker daemon created a new container from that image which runs the
    executable that produces the output you are currently reading.
 4. The Docker daemon streamed that output to the Docker client, which sent it
    to your terminal.

To try something more ambitious, you can run an Ubuntu container with:
 $ docker run -it ubuntu bash

Share images, automate workflows, and more with a free Docker ID:
 https://hub.docker.com/

For more examples and ideas, visit:
 https://docs.docker.com/get-started/
```

Código de salida: 0.

## Paso 6 — `.venv\Scripts\python scripts\check_env.py`

```text
Python: 3.14.5 (tags/v3.14.5:5607950, May 10 2026, 10:43:50) [MSC v.1944 64 bit (AMD64)]
Ejecutable: D:\Claudio Trabajo\Proyectos\private-ai-platform\.venv\Scripts\python.exe
Entorno virtual: True
httpx: 0.28.1
```

Código de salida: 0. `httpx` 0.28.1 se instaló solo dentro de `.venv` (`python -m pip install httpx`).

## Criterio de aceptación

**Criterio:** un contenedor de prueba corre y un script de Python se ejecuta en un entorno virtual.

**Estado:** cumplido.

**Motivo:** `docker run --rm hello-world` terminó con código 0 e imprimió `Hello from Docker!`. `scripts/check_env.py`, lanzado con `.venv\Scripts\python`, reportó Python 3.14.5, el ejecutable del entorno virtual del proyecto, `Entorno virtual: True` y `httpx` 0.28.1.

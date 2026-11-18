# ADR-0007: Entorno de desarrollo: Windows nativo con Python 3.14, Docker Desktop y Cursor

- **Estado:** Aceptada
- **Fecha:** 2026-11-18
- **Relacionadas:** ADR-0002, ADR-0003
- **Evidencia:** [FND-1](../../sprint-log/2026-11-18-fnd-1-entorno.md)

## Contexto

Hay dos equipos disponibles:

| Equipo | Procesador | RAM | Disco | GPU |
| --- | --- | --- | --- | --- |
| PC principal (Windows 11 Pro for Workstations) | AMD Ryzen 5 5600G, 6 núcleos | 11,9 GB utilizables | SSD 240 GB + SSD 1 TB | Integrada, sin GPU dedicada |
| HP ENVY m6 (2013) | Intel Core i5-4200U, 2 núcleos | 8 GB | Rígido 750 GB, 5400 rpm | Integrada |

El plan v1 suponía desarrollar en la HP con Linux. Producción va a ser Linux, en contenedores.

En la PC ya estaban instalados WSL 2, Git, Python 3.14, Docker Desktop, VS Code y Cursor.

## Alternativas

1. **Desarrollar en la HP con Linux.**
2. **Desarrollar en la PC dentro de WSL 2**, con el código en el sistema de archivos de Linux.
3. **Desarrollar en la PC en Windows nativo**, con los servicios (PostgreSQL, Ollama) en Docker Desktop sobre WSL 2.

## Decisión

Se elige la opción 3.

- **Python 3.14**, con un entorno virtual `.venv` por proyecto. No se usa 3.15 por ahora.
- **Docker Desktop con backend WSL 2** para los servicios y para Docker Compose.
- **Código en el SSD de 1 TB**, en `D:\Claudio Trabajo\Proyectos`.
- **Cursor** es el único editor y asistente para el desarrollo. Las decisiones, los ADR, la revisión de evidencia y la validación comercial se orquestan desde un Proyecto de Claude.
- **La HP** se reinstala con Ubuntu Server y queda como servidor de ensayo antes del Sprint 5, para probar el despliegue en Linux real.

## Justificación

- La PC tiene tres veces los núcleos de la HP, discos SSD y más memoria. La HP no corre modelos útiles.
- Todo lo necesario ya estaba instalado y verificado (FND-1). Empezar no costó horas de instalación.
- Windows nativo es el entorno que ya se conoce y donde Cursor funciona sin configuración extra. Las diferencias con Linux quedan cubiertas porque los servicios corren en contenedores Linux, y el despliegue se ensaya en la HP con Ubuntu Server.
- Python 3.15 salió el 9 de octubre de 2026. Todavía hay librerías sin paquetes para esa versión, y vLLM documenta soporte hasta 3.14.

## Consecuencias

- **A favor:** el desarrollo arrancó el mismo día, sin costo.
- **En contra:** hay diferencias entre Windows y Linux, como las rutas y los finales de línea. Antes del primer código (MOD-1) se agrega un `.gitattributes` que fije los finales de línea.
- **En contra:** con 11,9 GB de RAM, Docker, PostgreSQL, Ollama y Cursor compiten por la memoria. En el Sprint 1 se fija un tope de memoria para WSL en `.wslconfig`.
- **En contra:** sin GPU dedicada, los modelos locales son chicos y lentos. La calidad de la demo viene de los modelos por API (ADR-0002).
- **Revisión:** el paso a Python 3.15 se evalúa al cierre de los 90 días.

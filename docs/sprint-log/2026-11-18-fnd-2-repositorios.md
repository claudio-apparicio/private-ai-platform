# FND-2 — Repositorios

Fecha: 2026-11-18  
Tarea: crear el repositorio público del producto y el repositorio privado de negocio.

Los commits usan el correo `280126165+claudio-apparicio@users.noreply.github.com`.

## Visibilidad

`gh repo view private-ai-platform --json name,visibility,url`

```json
{"name":"private-ai-platform","url":"https://github.com/claudio-apparicio/private-ai-platform","visibility":"PUBLIC"}
```

`gh repo view private-ai-business --json name,visibility,url`

```json
{"name":"private-ai-business","url":"https://github.com/claudio-apparicio/private-ai-business","visibility":"PRIVATE"}
```

## Árbol de carpetas

Sin `.git` ni `.venv`. Este archivo queda en `docs/sprint-log/` con el commit de evidencia.

### private-ai-platform

```text
private-ai-platform/
- .gitignore
- backend/
  - .gitkeep
- data/
  - sample-docs/
    - .gitkeep
- deploy/
  - .gitkeep
- docs/
  - architecture/
    - adr/
      - README.md
  - evaluation/
    - .gitkeep
  - operations/
    - .gitkeep
  - product/
    - .gitkeep
  - sprint-log/
    - 2026-11-18-fnd-1-entorno.md
    - 2026-11-18-fnd-2-repositorios.md
- frontend/
  - .gitkeep
- README.md
- scripts/
  - check_env.py
```

### private-ai-business

```text
private-ai-business/
- .gitignore
- discovery/
  - .gitkeep
- offer/
  - .gitkeep
- prospects/
  - .gitkeep
- README.md
```

## Criterio de aceptación

**Criterio:** dos repositorios en GitHub, el público con README y carpeta de ADR.

**Estado:** cumplido.

**Motivo:** `private-ai-platform` es público (`https://github.com/claudio-apparicio/private-ai-platform`) y contiene `README.md` y `docs/architecture/adr/`. `private-ai-business` es privado (`https://github.com/claudio-apparicio/private-ai-business`). No se agregó licencia ni un ADR de decisión.

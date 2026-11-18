# Architecture Decision Records

Un ADR (Architecture Decision Record) documenta una decisión de arquitectura que es difícil de revertir. Deja por escrito el contexto, las alternativas que se consideraron y qué consecuencias tiene la opción elegida.

Los ADR de este proyecto viven en esta carpeta, un archivo por decisión.

## Plantilla

```markdown
# ADR-NNNN: Título

## Contexto

## Alternativas

## Decisión

## Justificación

## Consecuencias
```

## Índice

| ADR | Título | Estado |
| --- | --- | --- |
| [0001](0001-producto-inicial.md) | Producto inicial: asistente de conocimiento de una sola instalación | Aceptada |
| [0002](0002-acceso-a-modelos.md) | Acceso a modelos por una interfaz compatible con OpenAI | Propuesta |
| [0003](0003-postgresql-pgvector.md) | PostgreSQL con pgvector como única base de datos | Aceptada |
| [0004](0004-rag-propio.md) | Pipeline de RAG escrito a mano, sin frameworks al inicio | Aceptada |
| [0005](0005-registro-de-uso.md) | Registro de uso propio en PostgreSQL; Langfuse se evalúa en el Sprint 5 | Propuesta |
| [0006](0006-repositorios.md) | Repositorio público para el producto y privado para el negocio | Aceptada |
| [0007](0007-entorno-de-desarrollo.md) | Entorno de desarrollo: Windows nativo con Python 3.14, Docker Desktop y Cursor | Aceptada |
| 0008 | Licencia del repositorio público | Pendiente |

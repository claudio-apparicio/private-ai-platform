# ADR-0003: PostgreSQL con pgvector como única base de datos

- **Estado:** Aceptada (viene del plan v1)
- **Fecha:** 2026-11-16
- **Relacionadas:** ADR-0004, ADR-0005

## Contexto

El sistema guarda documentos, fragmentos, vectores, usuarios, permisos y el registro de uso de los modelos. El volumen del MVP es chico: 20 documentos de prueba y, como mucho, algunos miles de fragmentos.

El backlog incluye borrar un documento con todo lo derivado (SEG-3), permisos por base de conocimiento (SEG-1) y backup con restauración probada (OPS-5). La máquina de desarrollo tiene 11,9 GB de RAM.

## Alternativas

1. **PostgreSQL para los datos y una base vectorial aparte** (Qdrant).
2. **PostgreSQL con la extensión pgvector** para datos y vectores en la misma base.

## Decisión

Se elige la opción 2: PostgreSQL con pgvector, en la imagen Docker oficial de pgvector. La versión de pgvector se fija al levantar la base en el Sprint 1. La referencia hoy es la 0.8.7, que requiere Postgres 13 o superior ([README de pgvector](https://github.com/pgvector/pgvector)).

## Justificación

- Una sola base para datos, vectores y registro de uso.
- Borrar un documento y sus fragmentos y vectores es una sola transacción.
- Los permisos por base de conocimiento se aplican en la misma consulta SQL que busca los vectores. No hay que sincronizar dos sistemas.
- Hay un solo backup y una sola restauración que probar.
- Menos contenedores y menos memoria en una máquina de 11,9 GB.
- pgvector ofrece índices HNSW e IVFFlat y permite búsqueda híbrida, que alcanza para este volumen.

## Consecuencias

- **A favor:** arquitectura simple y operación de una sola base.
- **En contra:** hay que aprender SQL, el diseño de las tablas y los índices vectoriales.
- **Revisión:** si la evaluación (EVA-2) muestra un límite de calidad o de velocidad atribuible a pgvector, se reevalúa una base vectorial dedicada con esos números.

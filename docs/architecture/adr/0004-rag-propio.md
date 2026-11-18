# ADR-0004: Pipeline de RAG escrito a mano, sin frameworks al inicio

- **Estado:** Aceptada (viene del plan v1)
- **Fecha:** 2026-11-16
- **Relacionadas:** ADR-0001, ADR-0003

## Contexto

El pipeline de RAG (extraer el texto, fragmentarlo, generar embeddings, buscar, armar el prompt y citar la fuente) es el corazón del producto y lo que el portfolio tiene que mostrar construido. Hay frameworks y plataformas que lo resuelven listo.

## Alternativas

1. **LangChain o LlamaIndex** como framework del pipeline.
2. **Dify** u otra plataforma completa de aplicaciones con LLM.
3. **Pipeline propio con librerías puntuales:** Docling para extraer el texto con su estructura, el cliente de modelos de ADR-0002 y SQL sobre pgvector para la búsqueda.

## Decisión

Se elige la opción 3. LangChain y LlamaIndex no se usan al inicio, y Dify no se usa.

Docling se usa para extraer el texto de PDF y DOCX. Tiene licencia MIT y la gobernanza de LF AI & Data.

## Justificación

- Un pipeline escrito a mano se entiende de punta a punta y se puede explicar en una entrevista técnica.
- Da control directo sobre las citas (documento y página) y sobre la respuesta "no está en los documentos" (RAG-2 y RAG-3).
- Tiene menos dependencias que puedan cambiar o romperse entre versiones.
- Dify reemplazaría justo lo que el portfolio tiene que mostrar construido.

## Consecuencias

- **A favor:** aprendizaje real y código propio que se puede defender.
- **En contra:** hay más código que escribir y mantener.
- **En contra:** las funciones avanzadas (re-ranking, consultas en varios pasos, agentes) cuestan más de construir.
- **Revisión:** si una función concreta del backlog lleva más de un sprint hacerla a mano y un framework la resuelve, se evalúa sumarlo para esa función, con un ADR propio.

# ADR-0005: Registro de uso propio en PostgreSQL; Langfuse se evalúa en el Sprint 5

- **Estado:** Propuesta. Se acepta al cerrar MOD-3, cuando cada llamada quede registrada en PostgreSQL.
- **Fecha:** 2026-11-16
- **Relacionadas:** ADR-0002, ADR-0003

## Contexto

Medir tokens, latencia y costo por llamada es parte del producto: el cliente tiene que ver cuánto cuesta y cuánto tarda. También es la base de la evaluación (EVA-2) y del tablero de uso (OPS-4).

Existen herramientas de observabilidad para LLM, como Langfuse, que registran cada llamada y cada paso del pipeline.

## Alternativas

1. **Langfuse autoalojado.**
2. **Langfuse en la nube del proveedor.**
3. **Una tabla propia en PostgreSQL** con una fila por llamada al modelo.

## Decisión

Se propone la opción 3. Cada llamada guarda, como mínimo: fecha y hora, proveedor, modelo, tokens de entrada y de salida, latencia, costo y si terminó bien o con error.

Langfuse se evalúa en el Sprint 5, con el sistema ya funcionando.

## Justificación

- La tabla vive en la base que ya existe (ADR-0003): no suma piezas.
- Langfuse tiene el núcleo con licencia MIT, pero autoalojarlo suma ClickHouse, Redis y almacenamiento de objetos ([Langfuse](https://langfuse.com/resources/engineering/clarifications)). Es demasiado para una máquina de 11,9 GB y una sola persona en el Sprint 1.
- La versión en la nube enviaría consultas y fragmentos a un tercero más, en contra de los niveles de privacidad de ADR-0002.
- Para el tablero de uso alcanza con sumar y agrupar esa tabla.

## Consecuencias

- **A favor:** cero dependencias nuevas, y los datos de uso quedan en la base del cliente.
- **En contra:** no hay trazas de cada paso del RAG ni una interfaz de análisis lista. El tablero mínimo se construye en OPS-4.
- **Revisión:** en el Sprint 5 se decide si Langfuse aporta lo suficiente como para justificar sus piezas extra.

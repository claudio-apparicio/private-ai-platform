# MOD-1 — Primer modelo por API

Fecha: 2026-11-25  
Tarea: llamar a un modelo por API desde Python y medir tokens, latencia y costo.

## Configuración de OpenRouter

ZDR obligatorio en los cinco grupos (All other models, Anthropic, OpenAI, Google, SpaceXSI), con "ZDR only" donde se puede elegir. Entrenamiento con datos apagado en los cuatro interruptores. Clave `private-ai-platform-dev` con tope de USD 10 por mes, más estricto que el techo de USD 30 por mes del ADR-0002.

`scripts/check_key.py` antes de las tres llamadas (código de salida 0):

```text
limit: 10
limit_reset: monthly
limit_remaining: 10
usage: 0
```

`scripts/check_key.py` después de las tres llamadas (código de salida 0):

```text
limit: 10
limit_reset: monthly
limit_remaining: 10
usage: 0
```

El endpoint de la clave sigue reportando `usage: 0`. El costo de cada llamada quedó en `data/runs/model_calls.csv` (USD 0.000038, 0.000033 y 0.000022).

## Archivos

- `.cursorignore`: ignora `.env`.
- `.gitignore`: ignora `.env` y `data/runs/` (las mediciones locales no se versionan; en MOD-3 pasan a PostgreSQL).
- `requirements.txt`: `httpx==0.28.1` y `python-dotenv==1.2.4`.
- `.env.example`: `OPENROUTER_API_KEY`, `OPENROUTER_BASE_URL` y `DEFAULT_MODEL`. Se versiona.
- `scripts/ask_model.py`: una llamada de chat, resumen en pantalla y una fila en el CSV.
- `scripts/check_key.py`: imprime solo `limit`, `limit_reset`, `limit_remaining` y `usage`.
- `scripts/list_zdr_models.py`: hasta 30 modelos con retención cero, ordenados por precio de entrada.
- `docs/sprint-log/2026-11-25-mod-1-primer-modelo.md`: este log.

`.env` no se versiona.

## Ejecuciones

Tres llamadas separadas a `scripts/ask_model.py --model openai/gpt-oss-20b`, con el prompt por defecto. Las tres terminaron con código de salida 0.

| timestamp_utc | modelo resuelto | proveedor | tokens de entrada | tokens de salida | costo USD | latencia ms |
| --- | --- | --- | --- | --- | --- | --- |
| 2026-11-25T13:16:49Z | openai/gpt-oss-20b | Amazon Bedrock | 86 | 211 | 0.000038 | 2606 |
| 2026-11-25T13:16:54Z | openai/gpt-oss-20b | Amazon Bedrock | 86 | 181 | 0.000033 | 917 |
| 2026-11-25T13:16:59Z | openai/gpt-oss-20b | AkashML | 86 | 231 | 0.000022 | 2565 |

Texto de la primera respuesta:

```text
La generación aumentada por recuperación (RAG, por sus siglas en inglés) es un enfoque de IA que combina un motor de búsqueda que recupera documentos relevantes de una gran base de conocimiento con un modelo de generación de lenguaje. El modelo primero identifica fragmentos de texto que mejor respondan a la pregunta o contexto, y luego utiliza esa información recuperada para generar una respuesta más precisa y confiable. Este método permite a los sistemas generar contenido sustantivo y verificado, reduciendo errores y mejorando la fiabilidad de la información producida.
```

## Hallazgos

(a) Desde el 18/10/2026 Google exige Safety Retention y OpenAI va a exigirla cuando Azure deje de ofrecer ZDR. Con ZDR only, el catálogo se reduce a Anthropic por Bedrock y Vertex y a modelos de pesos abiertos en proveedores con ZDR.

(b) `list_zdr_models.py` ordena por precio de entrada y la lista queda llena de embeddings y rerankers. Para MOD-2 hay que filtrar a modelos de chat.

(c) El mismo modelo se resolvió en dos proveedores: Amazon Bedrock (llamadas 1 y 2) y AkashML (llamada 3). La latencia varió entre 917 y 2606 ms con el mismo proveedor, y el costo por llamada depende del proveedor. Para EVA-2 hay que registrar el proveedor (el CSV ya lo hace) y fijarlo con `provider.order` o `provider.only` cuando la comparación lo requiera. Tres llamadas no alcanzan para sacar conclusiones de latencia.

## Criterio de aceptación

**Criterio:** un script responde una pregunta y guarda las tres medidas.

**Estado:** cumplido.

**Motivo:** las tres ejecuciones de `scripts/ask_model.py --model openai/gpt-oss-20b` terminaron con código 0, imprimieron la respuesta y una línea con tokens, costo y latencia. `data/runs/model_calls.csv` tiene tres filas con `status=ok`, tokens de entrada y de salida, `cost_usd` y `latency_ms`.

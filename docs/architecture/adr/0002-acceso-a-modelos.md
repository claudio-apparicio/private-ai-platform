# ADR-0002: Acceso a modelos por una interfaz compatible con OpenAI

- **Estado:** Propuesta. Se acepta al cerrar MOD-2, cuando la misma pregunta se responda con tres modelos cambiando solo un parámetro.
- **Fecha:** 2026-11-16
- **Relacionadas:** ADR-0001, ADR-0005, ADR-0007

## Contexto

El MVP tiene que comparar varios modelos en calidad, latencia y costo, y ofrecer un modelo local como opción. La PC de desarrollo no tiene GPU dedicada (ADR-0007), así que los modelos con calidad de demo corren por API. Durante la validación hay un tope de gasto de USD 30 por mes.

Vender "IA privada" usando APIs de terceros es una contradicción si no se dice con claridad qué sale de la empresa.

## Alternativas

1. **SDK propio de cada proveedor** (OpenAI, Anthropic, Gemini), con una clave y un formato por proveedor.
2. **LiteLLM como proxy propio**, que unifica proveedores, claves y presupuestos.
3. **OpenRouter para modelos por API y Ollama para el modelo local**, ambos detrás del formato de chat de OpenAI, con un cliente propio delgado.

## Decisión

Se propone la opción 3.

- El backend habla un solo formato. La URL base, la clave y el nombre del modelo salen de la configuración.
- OpenRouter se usa con retención cero activada y tope de gasto de hasta USD 30 por mes. La clave de desarrollo arranca con un tope de USD 10 por mes. Configurado y verificado en MOD-1 ([sprint-log](../../sprint-log/2026-11-25-mod-1-primer-modelo.md)).
- Ollama cubre el nivel local (MOD-4).
- LiteLLM queda diferido. Las APIs directas de cada proveedor se usan solo si un cliente lo pide.

El producto declara tres niveles de privacidad y nunca llama privado a un nivel que envía datos afuera sin decirlo:

| Nivel | Dónde corre el modelo | Qué sale de la empresa | Cuándo conviene |
| --- | --- | --- | --- |
| 1. API con retención cero | Proveedor externo, solo endpoints sin retención | La consulta y los fragmentos, en tránsito | Datos internos no regulados; prioridad en calidad y costo |
| 2. Nube del cliente | Modelo abierto en la cuenta cloud del cliente | Nada sale de su cuenta | Datos sensibles y equipo con experiencia en cloud |
| 3. Local | Servidor propio del cliente | Nada | Exigencia regulatoria o contractual, con volumen que pague el hardware |

## Justificación

- Una clave y un formato dan acceso a muchos modelos. Cambiar de modelo es cambiar un parámetro, que es justo lo que pide la evaluación (EVA-2).
- Ollama también ofrece una API compatible con OpenAI, así que el nivel local no necesita otro código.
- LiteLLM hoy duplica lo que hace OpenRouter, concentra todas las credenciales en un solo lugar y tuvo dos versiones maliciosas publicadas en PyPI en marzo de 2026 ([JFrog](https://research.jfrog.com/post/litellm-compromised-teampcp/)).

## Consecuencias

- **A favor:** comparar modelos es trivial y el código no depende de ningún proveedor.
- **En contra:** OpenRouter es un intermediario más que ve el tráfico del nivel 1. Como el formato es estándar, salir de OpenRouter es cambiar la URL base y la clave.
- **En contra:** las funciones propias de cada proveedor que no existen en el formato común quedan afuera.
- **En contra:** desde el 18/10/2026 Google exige Safety Retention (el proveedor puede guardar pedidos solo para prevenir abusos), y OpenAI la va a exigir cuando Azure deje de ofrecer ZDR. Con "ZDR only", el nivel 1 queda limitado a Anthropic por Bedrock y Vertex y a modelos de pesos abiertos en proveedores con ZDR. En MOD-2 se decide si algún grupo admite Safety Retention y cómo se le explica al cliente.
- **Pendiente:** LiteLLM se reconsidera, con versión fijada, cuando hagan falta presupuestos y claves por cliente.

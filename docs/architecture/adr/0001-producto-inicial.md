# ADR-0001: Producto inicial: asistente de conocimiento de una sola instalación

- **Estado:** Aceptada
- **Fecha:** 2026-11-16
- **Relacionadas:** ADR-0002 (niveles de privacidad), ADR-0006

## Contexto

El proyecto busca tres resultados en 90 días: aprender a construir sistemas de IA, dejar un portfolio verificable y validar si existe un servicio vendible de "IA privada" para empresas. Lo hace una sola persona, con unas 20 horas por semana y sin clientes todavía.

La lista inicial de ideas incluía multi-tenant, conectores a Drive o SharePoint, agentes, automatizaciones e integraciones con CRM o ERP. Todo eso junto no entra en siete sprints.

## Alternativas

1. **Plataforma multi-tenant administrada (SaaS).** Una sola instalación compartida entre clientes.
2. **Asistente con agentes y automatizaciones.** Flujos con MCP, n8n o Activepieces que actúan sobre otros sistemas.
3. **Asistente de conocimiento de una sola instalación.** El cliente carga sus documentos y el asistente responde con citas a la fuente, en una instalación propia por cliente.

## Decisión

Se elige la opción 3.

Dentro del MVP:

- Carga de PDF, DOCX y TXT.
- Búsqueda semántica y chat con citas a la fuente (documento y página).
- Selector entre modelos por API y uno local.
- Uso, latencia y costo por llamada.
- Login simple y una base de conocimiento.
- Despliegue con Docker Compose.

Fuera hasta tener un piloto: multi-tenant e infraestructura administrada, conectores a Google Drive o SharePoint, agentes, automatizaciones y MCP, integraciones con CRM o ERP, SSO y permisos finos por documento.

Durante el desarrollo solo se usan documentos públicos o sintéticos. Ningún documento real de un cliente entra antes de pasar las pruebas de seguridad del Sprint 6.

## Justificación

- Es un caso de uso que se evalúa con números propios: si la cita es correcta, si el fragmento correcto aparece entre los primeros, si el asistente avisa cuando la respuesta no está en los documentos.
- Una instalación por cliente ya aísla los datos de cada uno sin construir multi-tenant.
- Lo que se vende es implementación y operación, no la licencia del código. Un producto acotado se instala, se explica y se cotiza.
- Cabe en siete sprints y deja una demo concreta en los Sprints 4 y 5.

## Consecuencias

- **A favor:** alcance claro, demo visible y criterios de aceptación medibles.
- **En contra:** cada cliente nuevo es un despliegue nuevo, con su costo de operación. Multi-tenant se reevalúa recién con dos o más clientes en infraestructura compartida.
- **En contra:** sin conectores, los documentos se cargan a mano.
- **Riesgo:** que el mercado pida justamente lo que quedó afuera. Se mide en las entrevistas de descubrimiento (COM-2).

# ADR-0006: Repositorio público para el producto y privado para el negocio

- **Estado:** Aceptada el 2026-11-16. Implementada en FND-2 el 2026-11-18.
- **Fecha:** 2026-11-16
- **Relacionadas:** ADR-0001

## Contexto

El portfolio necesita código visible para que un tercero pueda verificar el trabajo. El lado comercial produce información que no puede ser pública: notas de entrevistas con datos de personas, lista de prospectos, precios y propuestas.

El plan v1 tenía un solo repositorio con el negocio y el código juntos.

## Alternativas

1. **Un solo repositorio con todo** (plan v1).
2. **Privado hasta el MVP**, y se abre cuando haya una demo.
3. **Privado siempre**: el portfolio muestra la demo y los case studies, no el código.
4. **Dos repositorios:** uno público para el producto y uno privado para el negocio.

## Decisión

Se elige la opción 4.

- Público: [private-ai-platform](https://github.com/claudio-apparicio/private-ai-platform). Código, documentación, ADR, evaluación y evidencia de cada sprint.
- Privado: private-ai-business. Descubrimiento, prospectos y oferta comercial.

Los commits usan el email noreply de GitHub para no exponer el email personal.

## Justificación

- El repositorio público es evidencia del trabajo desde el primer día, y cada sprint deja algo verificable.
- Las notas de entrevistas tienen datos de personas y de empresas. No pueden ser públicas, por respeto a los entrevistados y por la Ley 25.326 de protección de datos personales.
- Lo que se vende es implementación y operación, no la licencia del código. Mostrar el código no regala el negocio.

## Consecuencias

- **A favor:** portfolio verificable sin exponer información comercial.
- **En contra:** todo lo que entra al repositorio público queda en su historial. Nunca se suben claves, archivos `.env` ni documentos reales. El `.gitignore` ya excluye `.env`.
- **En contra:** hay dos repositorios que mantener.
- **Pendiente:** la licencia del repositorio público se decide en el ADR-0008. Hasta entonces el código es visible, pero sin licencia nadie tiene permiso de reutilizarlo.

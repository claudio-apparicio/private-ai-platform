# ADR-0008: Licencia Apache 2.0 para el repositorio público

- **Estado:** Aceptada
- **Fecha:** 2026-11-18
- **Relacionadas:** ADR-0001, ADR-0006

## Contexto

El repositorio `private-ai-platform` es público desde el 18 de noviembre de 2026 (ADR-0006). Sin licencia, el código se puede ver pero nadie tiene permiso de usarlo, modificarlo ni redistribuirlo.

El modelo de negocio vende implementación y operación, no la licencia del código (ADR-0001). El repositorio también es la pieza central del portfolio, y lo van a revisar clientes potenciales y empresas que evalúan contratar.

## Alternativas

1. **Sin licencia.** El código es visible pero no reutilizable.
2. **MIT.** Permisiva y muy breve. Permite usar, modificar y vender manteniendo el aviso de autoría. No trata las patentes de forma explícita.
3. **Apache 2.0.** Permisiva, con los mismos permisos que MIT, más una cesión explícita de patentes y la obligación de indicar los cambios hechos a los archivos.
4. **AGPL 3.0.** Copyleft de red. Quien modifique el software y lo ofrezca como servicio tiene que publicar sus cambios.

## Decisión

Se elige Apache 2.0. El texto completo va en el archivo `LICENSE` de la raíz, y el README indica la licencia.

## Justificación

- El valor del negocio está en implementar y operar, no en el código. Conviene que el código circule sin fricción.
- Apache 2.0 es una licencia que los equipos legales de las empresas suelen aprobar sin objeciones, y la cesión de patentes da más seguridad que MIT a quien la adopta.
- AGPL protege contra un competidor que venda el producto cerrado, pero muchas empresas prohíben usar software AGPL. Esa restricción afectaría justamente a los clientes y empleadores que el portfolio busca.
- Sin licencia, el repositorio no es open source y se ve incompleto como portfolio.

## Consecuencias

- **A favor:** cualquiera puede probar, estudiar y adoptar el código, incluidos clientes y empleadores.
- **En contra:** un tercero puede reutilizar el código, incluso con fines comerciales, siempre que conserve el aviso de autoría y la licencia.
- **A tener en cuenta:** las dependencias que se sumen tienen que tener licencias compatibles con Apache 2.0. Se revisa al agregar cada una.
- **Revisión:** si el negocio pasa a vender licencias de software, esta decisión se revisa con un abogado. Este ADR no es asesoramiento legal.

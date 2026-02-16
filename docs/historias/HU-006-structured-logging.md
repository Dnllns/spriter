# HU-006: Registro Estructurado para Depuración y Trazabilidad

| Campo | Valor |
| --- | --- |
| **Estado** | `completada` |
| **Tipo** | `infraestructura` |
| **Prioridad** | `alta` |
| **Estimación** | 1 Punto |
| **Huv** | Como desarrollador, quiero un sistema de logs estructurados para poder depurar errores y trazar peticiones de forma eficiente en entornos de desarrollo y producción. |

## Contexto
Actualmente el proyecto carece de una configuración de logging centralizada. Los errores se ven en la consola de forma plana, lo que dificulta la extracción de métricas o la trazabilidad de peticiones específicas (Correlation IDs).

## Criterios de Aceptación

### AC-006-01: Configuración de Structlog
- **Descripción**: El sistema debe utilizar `structlog` para generar logs en formato JSON (producción) y formato legible (desarrollo).
- **Validación técnica**:
  - [x] Los logs deben incluir: timestamp, nivel de log, nombre del logger y mensaje.

### AC-006-02: Middleware de Trazabilidad (Request ID)
- **Descripción**: Cada petición HTTP debe generar un `request_id` único que se incluya en todos los logs generados durante el ciclo de vida de esa petición.
- **Validación técnica**:
  - [x] El `request_id` debe devolverse en los headers de la respuesta (`X-Request-ID`).

### AC-006-03: Integración con Excepciones
- **Descripción**: El manejador global de excepciones debe registrar el error estructurado, incluyendo el stack trace si es necesario.
- **Validación técnica**:
  - [x] Los errores 500 deben registrarse con nivel ERROR e información del contexto.

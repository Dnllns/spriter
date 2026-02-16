# HU-005: Mejoras de Robusticidad y Paginación en API de Sprites

## Metadata

| Campo | Valor |
| --- | --- |
| **Estado** | `en_progreso` |
| **Tipo** | `refactor` |
| **Prioridad** | `media` |
| **Estimación** | 2 Puntos |

## Objetivo
Quiero [Consumidor de API] poder [paginar los resultados de búsqueda de sprites y recibir errores estructurados] para [manejar grandes volúmenes de datos y errores de negocio de forma predecible].

## Contexto
Actualmente `list_sprites` acepta `limit` y `offset` pero no hay una validación estricta ni una respuesta paginada con metadatos. Además, el manejo de errores de persistencia debe traducirse a HTTP exceptions adecuadas.

## Criterios de Aceptación (AC)

### AC-005-01: Paginación Validada
- **Descripción**: El endpoint `GET /api/v1/sprites` debe validar que `limit` sea un entero positivo (máximo 100) y `offset` >= 0.
- **Validación técnica**:
  - [ ] Test unitario: `test_api_ac_005_01_pagination_validation`
  - Input: `limit=500` -> 422 Unprocessable Entity o ajuste automático.

### AC-005-02: Manejo Global de Errores de Dominio
- **Descripción**: Implementar un middleware o excepciones personalizadas para capturar errores de "Sprite no encontrado" o "Conflicto de versión" y devolver 404/409.
- **Validación técnica**:
  - [ ] Test unitario: `test_api_ac_005_02_error_mapping`

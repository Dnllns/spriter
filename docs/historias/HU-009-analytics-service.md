# HU-009: Servicio de Analíticas de Reproducción

## Objetivo
Implementar un servicio de analíticas (`AnalyticsService`) para registrar y visualizar el número de reproducciones ("plays") que tienen los sprites cuando se muestran desde el componente embebido `<spriter-player>`.

## Contexto
El componente `<spriter-player>` permite usar los sprites en otros sitios web. Sin embargo, no tenemos un registro de qué tan populares son o cuántas veces se visualizan estas animaciones. Contar con estas métricas aporta valor a la plataforma.

## Criterios de Aceptación (AC)

### AC-009-01: Dominio e Infraestructura
- Crear la entidad de dominio `SpriteAnalytics` (o campos en el Sprite). Lo mejor es una tabla separada para trackeo de eventos, por ejemplo `AnalyticsEvent` o un contador `play_count` en Sprite (optaremos por un contador simple en `Sprite` por ahora, incrementado atómicamente).
- Mejor aún, como pide un servicio, creemos un `AnalyticsService` y un puerto `AnalyticsRepository`.

### AC-009-02: Endpoint de tracking
- Un endpoint público (ej. `POST /api/v1/analytics/sprites/{sprite_id}/play`) que reciba un ping e incremente el contador.
- Este endpoint debe ser accesible vía CORS y no debe requerir autenticación OIDC estricta (ya que se lanza desde players embebidos anónimos).

### AC-009-03: Web Component
- El `<spriter-player>` debe hacer un hit (fetch POST) a este endpoint cuando inicie la primera reproducción de la animación, o cuando cargue.

### AC-009-04: API de Estadísticas
- El listado de sprites (`GET /sprites`) y detalle deben devolver el `play_count`.
- Añadir tests (Unit y E2E) para garantizar el funcionamiento correcto de las analíticas.

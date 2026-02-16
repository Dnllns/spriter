# HU-004: API de Simulación de Sprites

## Metadata

| Campo | Valor |
| --- | --- |
| **Estado** | `completada` |
| **Tipo** | `feature` |
| **Prioridad** | `alta` |
| **Estimación** | 3 Puntos |

## Objetivo
Quiero [Frontend Client] poder [enviar una configuración de animación y un tiempo transcurrido] para [recibir el índice del frame actual y su progreso inter-frame].

## Contexto
El frontend necesita sincronizar la visualización del sprite con la lógica del servidor (Single Source of Truth) o al menos validar la lógica de simulación. Esta API expone la lógica de dominio `SimulatorService` definida en la Fase 2.

## Criterios de Aceptación (AC)

### AC-004-01: Endpoint Calculation
- **Descripción**: El endpoint `POST /simulate` acepta un objeto `Animation` (o sus parámetros) y un `elapsed_ms`, y retorna `FrameResult`.
- **Validación técnica**:
  - [x] Test unitario/integración: `test_api_ac_004_01_calculate_frame`
  - Input: `{"animation": {...}, "elapsed_ms": 150, "config": {"loop": true}}`
  - Output: `{"frame_index": 1, "frame_progress": 0.5, "is_finished": false}`

### AC-004-02: Manejo de Errores
- **Descripción**: El endpoint debe manejar casos inválidos limpiamente.
- **Validación técnica**:
  - [x] Test unitario: `test_api_ac_004_02_invalid_input`
  - Input: `elapsed_ms` negativo -> 422 Unprocessable Entity o manejo específico.

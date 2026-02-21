# HU-010: Explorador de Frames

## Objetivo
Implementar una sección en la UI ("Sprite Library") que permita visualizar de forma individual todos los frames de un sprite seleccionado, permitiendo una inspección detallada de las animaciones.

## Contexto
Actualmente los sprites se ven como una sola imagen (o miniatura) en el dashboard o se simulan. No hay una forma de ver la "hoja de contactos" (contact sheet) o los frames individuales extraídos para validar si el troceado es correcto.

## Criterios de Aceptación (AC)

### AC-010-01: Vista de Librería
- Implementar la funcionalidad de navegación a `library-view`.
- Si no hay un sprite seleccionado, mostrar un estado vacío.

### AC-010-02: Renderizado de Frames
- Al seleccionar un sprite (o pasarle un ID a la vista), obtener su detalle.
- Renderizar en un grid cada frame individual de la versión más reciente.
- Mostrar metadatos del frame (índice, dimensiones).

### AC-010-03: Integración Dashboard
- Añadir un botón o link "Inspect" en las tarjetas del dashboard que lleve directamente a la librería con el sprite seleccionado.

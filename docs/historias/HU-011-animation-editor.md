# HU-011: Animation Sequence Editor

Como desarrollador de juegos, quiero poder editar y crear secuencias de animación directamente desde mi navegador para poder ajustar el timing y el orden de los frames sin tener que re-subir el archivo.

### Criterios de Aceptación

1. **[AC-011-01]** Se debe proporcionar una interfaz de "Editor de Animaciones" accesible desde el dashboard.
2. **[AC-011-02]** El editor debe permitir previsualizar los frames individuales de un sprite.
3. **[AC-011-03]** El usuario debe poder crear una nueva animación dándole un nombre (ej. "walk", "jump").
4. **[AC-011-04]** El usuario debe poder arrastrar o seleccionar frames para añadirlos a una secuencia.
5. **[AC-011-05]** Se debe poder ajustar el `duration` (ms) por cada frame de la animación.
6. **[AC-011-06]** Los cambios deben guardarse en el backend actualizando la metadata de la versión actual del sprite.

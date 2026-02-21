# HU-008: Flags de Visibilidad y Optimización Móvil

## Objetivo
Implementar el flag `is_public` en los sprites y optimizar el diseño base para resolución de pantallas pequeñas (Mobile CSS).

## Contexto
El sistema no tenía soporte para decidir la visibilidad de un sprite en el dashboard y el grid del frontend se rompía en resoluciones menores a 768px.

## Criterios de Aceptación (AC)

### AC-008-01: Flag is_public
- `Sprite` incluye un campo `is_public` booleano.
- La base de datos guarda este campo.
- Las requests para listar soportan este modelo.

### AC-008-02: Optimización Móvil
- El diseño bajo la media query `max-width: 768px` pasa a ser vertical en el dashboard.
- La navegación reacciona adecuadamente eliminando el border e implementando scroll X.

---
name: Pull Request Template
about: Template for pull requests adhering to HU/AC process.
title: ''
labels: ''
assignees: ''
---

## Historia de Usuario
HU-XXX

## Contexto
<!-- Explicación breve de lo que se resuelve en este PR -->

## Acceptance Criteria cubiertos
- [ ] AC-XXX-YY: [Descripción corta]
- [ ] AC-XXX-ZZ: [Descripción corta]

## Tests
- [ ] Unitarios: `uv run pytest tests/unit/test_ac_xxx_yy.py`
- [ ] Integración: `uv run pytest tests/integration/test_hu_xxx.py`

## Checklist (Mandatorio)
- [ ] Commits siguen formato `feat: desc [HU-XXX][AC-XXX-YY]`
- [ ] `uv run pytest` pasa al 100%
- [ ] `uv run ruff check .` no reporta errores
- [ ] `uv.lock` actualizado (si aplica)
- [ ] ADR creado/actualizado (si hubo cambios de arquitectura)

## Screenshots / Evidencia (Opcional)
<!-- Si es visual o un cambio complejo, añadir imagen o log -->

# PROCESO OFICIAL DE DESARROLLO (GitHub)

## 0. Principio rector (inamovible)

> **Nada se desarrolla sin HU.**
> **Nada se fusiona sin PR.**
> **Nada se acepta sin AC + tests.**
> **Nada se decide sin ADR.**

---

## 1. Historias de Usuario (HU)

* **Formato obligatorio**: `docs/historias/HU-XXX.md`
* Cada HU define:
  * objetivo
  * contexto
  * criterios de aceptación (AC)
* Una HU = una unidad funcional cerrable

---

## 2. Acceptance Criteria (AC)

* Identificador obligatorio: `AC-XXX-YY`
* Cada AC:
  * es verificable
  * tiene al menos un test
* Un AC puede tener su propia rama si es necesario

---

## 3. Ramas (obligatorias)

### 3.1 Regla

> **Todo cambio va en una rama. Prohibido commitear a `main`.**

### 3.2 Naming obligatorio

```
<tipo>/HU-XXX[-AC-YY]-descripcion_corta
```

Ejemplos:
* `feature/HU-023-auth-login`
* `fix/HU-023-AC-02-invalid-credentials`

Tipos permitidos:
* `feature`
* `fix`
* `refactor`
* `test`
* `docs`
* `ci`

---

## 4. Commits (Conventional Commits + HU/AC)

### 4.1 Formato obligatorio

```
<type>(<scope>): <subject> [HU-XXX][AC-XXX-YY]
```

Ejemplo:
```
feat(auth): add jwt login [HU-023][AC-023-01]
```

### 4.2 Reglas duras

* ❌ Commit sin `[HU-XXX]` → inválido
* ❌ Cambio funcional sin AC → inválido
* Dependencias **solo** vía `uv`

---

## 5. uv (entorno y dependencias)

* `uv` es obligatorio
* Prohibido usar `pip`, `poetry`, `pipenv`
* Cambios de dependencias:
  ```bash
  uv add <paquete>
  ```
* Commit separado:
  ```
  chore(deps): add fastapi [HU-023]
  ```

---

## 6. Tests (contrato de aceptación)

* Cada AC tiene al menos un test
* Naming obligatorio:

```python
def test_<contexto>_ac_023_01():
    ...
```

* Ejecución estándar:
```bash
uv run pytest
```

---

## 7. Pull Request (PR) — Solicitud de fusión

### 7.1 Regla

> **Toda rama se integra exclusivamente mediante PR.**

### 7.2 Título del PR

```
<type>(<scope>): <resumen> [HU-XXX]
```

### 7.3 Template obligatorio

Ver `.github/PULL_REQUEST_TEMPLATE.md`

---

## 8. Labels (obligatorios)

### 8.1 Labels mínimas

* `HU:XXX`
* `AC:XXX-YY`
* `backend` / `frontend` / `infra`
* `estado:en_progreso | estado:bloqueado | estado:listo`
* `tipo:feature | fix | refactor | test | docs`

### 8.2 Uso obligatorio en:

* Issues
* Pull Requests

---

## 9. ADR (Architecture Decision Records)

### 9.1 Cuándo es obligatorio un ADR

* Cambio arquitectónico
* Decisión tecnológica
* Cambio de patrón o contrato

### 9.2 Formato

`docs/adr/ADR-XXX.md`

Contenido mínimo:
* Contexto
* Decisión
* Alternativas descartadas
* Consecuencias

### 9.3 Regla

> **PR con impacto arquitectónico sin ADR → rechazado**

---

## 10. Merge a `main`

Un PR **solo puede fusionarse** si:

* Todos los AC están cubiertos
* Tests pasan
* Commits válidos
* Labels correctas
* ADR presente si aplica

---

## 11. Cierre de HU

Una HU se considera cerrada solo si:

* Todos sus PR están mergeados
* Todos sus AC están testeados
* Estado marcado como `completada`

---

## 12. Regla final

> **GitHub es el registro de hechos.**
> **Las HU definen el porqué.**
> **Los AC definen el qué.**
---

## 13. Project Memory Stack (Cognitive Persistence)

Este proyecto mantiene una "memoria" estricta para colaboradores humanos y Pautas de IA.

* **`AI_MANIFEST.md`**: Visión inmutable.
* **`docs/STATE.md`**: Estado actual (Dashboard).
* **`docs/adr/`**: Registro de decisiones.
* **`docs/historias/`**: Definición de valor (Why).

> **Mantén estos archivos sincronizados.**

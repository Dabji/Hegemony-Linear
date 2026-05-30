# Contributing | Contribuir

**[Espanol](#espanol) | [English](#english)**

---

<h2 id="espanol">Espanol</h2>

Gracias por tu interes en contribuir a **Hegemony Linear**.

## Alcance del proyecto

Este repositorio prioriza:

- Claridad academica del metodo numerico.
- Separacion entre frontend React, API FastAPI y motor de dominio Python.
- Cambios pequenos, probados y faciles de revisar.
- Documentacion bilingue cuando el cambio afecta uso publico.

## Configuracion local

```powershell
cd D:\Desarrollo\Proyectos\UPB\Hegemony-Linear
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt

cd frontend
fnm use 24.14.0
npm.cmd install
Copy-Item .env.example .env
```

## Flujo de trabajo

1. Crea un fork o una rama desde `main`.
2. Usa una rama descriptiva: `feat/nombre-corto`, `fix/nombre-corto` o `docs/nombre-corto`.
3. Mantiene el cambio enfocado en un objetivo.
4. Agrega o actualiza pruebas si cambia comportamiento.
5. Ejecuta verificacion antes del Pull Request.

## Commits

Usa Conventional Commits:

```text
feat(api): add income sensitivity endpoint
fix(frontend): correct worker assignment bounds
docs(readme): update deployment links
test(engine): cover tax calculation edge cases
```

## Verificacion

```powershell
cd D:\Desarrollo\Proyectos\UPB\Hegemony-Linear
python -m pytest

cd frontend
fnm use 24.14.0
npm.cmd run build
```

## Pull Requests

Incluye:

- Resumen claro del cambio.
- Evidencia de pruebas o build.
- Capturas si cambia interfaz.
- Notas de despliegue si cambia API, variables de entorno o configuracion.

---

<h2 id="english">English</h2>

Thank you for considering a contribution to **Hegemony Linear**.

## Project scope

This repository prioritizes:

- Academic clarity for the numerical method.
- Clear separation between React frontend, FastAPI backend and Python domain engine.
- Small, tested and reviewable changes.
- Bilingual documentation for public-facing usage changes.

## Local setup

```powershell
cd D:\Desarrollo\Proyectos\UPB\Hegemony-Linear
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt

cd frontend
fnm use 24.14.0
npm.cmd install
Copy-Item .env.example .env
```

## Workflow

1. Fork the repository or create a branch from `main`.
2. Use a descriptive branch: `feat/short-name`, `fix/short-name` or `docs/short-name`.
3. Keep each change focused on one goal.
4. Add or update tests when behavior changes.
5. Run verification before opening a Pull Request.

## Commits

Use Conventional Commits:

```text
feat(api): add income sensitivity endpoint
fix(frontend): correct worker assignment bounds
docs(readme): update deployment links
test(engine): cover tax calculation edge cases
```

## Verification

```powershell
cd D:\Desarrollo\Proyectos\UPB\Hegemony-Linear
python -m pytest

cd frontend
fnm use 24.14.0
npm.cmd run build
```

## Pull Requests

Include:

- Clear summary.
- Test or build evidence.
- Screenshots for UI changes.
- Deployment notes if API, environment variables or configuration changed.

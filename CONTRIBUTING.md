# 🤝 Guía de Contribución / Contributing Guide

---

# 🇪🇸 Español

Gracias por tu interés en contribuir a **Hegemony Linear**.

Este proyecto fue desarrollado como entrega académica de **Análisis Numérico (UPB)** y como proyecto de portafolio. Las contribuciones deben preservar la claridad del modelo matemático, la separación entre frontend/backend y la experiencia de juego.

## Alcance del Proyecto

Este repositorio prioriza:

- Claridad académica del método Newton-Raphson.
- Separación entre frontend React, API FastAPI y motor de dominio en Python.
- Cambios pequeños, probados y fáciles de revisar.
- Documentación clara en español e inglés cuando el cambio afecta el uso público.
- Seguridad básica en validación, configuración y manejo de variables de entorno.

## Configuración Local

```powershell
cd D:\Desarrollo\Proyectos\UPB\Hegemony-Linear
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

cd frontend
fnm use 24.14.0
npm.cmd install
Copy-Item .env.example .env
```

## Flujo de Trabajo

1. Crea un fork o una rama desde `main`.
2. Usa una rama semántica: `feat/nombre-corto`, `fix/nombre-corto`, `docs/nombre-corto` o `test/nombre-corto`.
3. Mantén el cambio enfocado en un solo objetivo.
4. Agrega o actualiza pruebas si cambia comportamiento.
5. Actualiza documentación si cambia API, despliegue, variables de entorno o experiencia de usuario.
6. Ejecuta la verificación antes de abrir un Pull Request.

## Convención de Commits

Usa **Conventional Commits**:

```text
feat(api): add income sensitivity endpoint
fix(frontend): correct worker assignment bounds
docs(readme): update deployment links
test(engine): cover tax calculation edge cases
chore(deps): update frontend lockfile
```

## Verificación

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
- Capturas si cambia la interfaz.
- Notas de despliegue si cambia API, configuración o variables de entorno.
- Riesgos conocidos o decisiones técnicas relevantes.

---
---

# 🇺🇸 English

Thank you for considering a contribution to **Hegemony Linear**.

This project was developed as an academic deliverable for **Numerical Analysis (UPB)** and as a portfolio project. Contributions should preserve the clarity of the mathematical model, the frontend/backend separation and the game experience.

## Project Scope

This repository prioritizes:

- Academic clarity for the Newton-Raphson method.
- Clear separation between React frontend, FastAPI backend and Python domain engine.
- Small, tested and reviewable changes.
- Clear documentation in Spanish and English when public usage changes.
- Basic security in validation, configuration and environment variable handling.

## Local Setup

```powershell
cd D:\Desarrollo\Proyectos\UPB\Hegemony-Linear
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

cd frontend
fnm use 24.14.0
npm.cmd install
Copy-Item .env.example .env
```

## Workflow

1. Fork the repository or create a branch from `main`.
2. Use a semantic branch: `feat/short-name`, `fix/short-name`, `docs/short-name` or `test/short-name`.
3. Keep each change focused on one goal.
4. Add or update tests when behavior changes.
5. Update documentation when API, deployment, environment variables or user experience changes.
6. Run verification before opening a Pull Request.

## Commit Convention

Use **Conventional Commits**:

```text
feat(api): add income sensitivity endpoint
fix(frontend): correct worker assignment bounds
docs(readme): update deployment links
test(engine): cover tax calculation edge cases
chore(deps): update frontend lockfile
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
- Deployment notes if API, configuration or environment variables changed.
- Known risks or relevant technical decisions.

# 🚀 Guía de Despliegue / Deployment Guide

---

# 🇪🇸 Español

## Arquitectura de Despliegue

| Servicio | Proveedor | URL |
|---|---|---|
| Frontend React/Vite | Vercel | https://hegemony-linear.vercel.app/ |
| Backend FastAPI | Render | https://hegemony-fastapi-backend.onrender.com/ |
| Swagger UI | Render | https://hegemony-fastapi-backend.onrender.com/docs |

## Backend en Render

Configuración recomendada:

```text
Name: hegemony-fastapi-backend
Runtime: Python
Plan: Free
Build Command: python -m pip install -r requirements.txt
Start Command: python -m uvicorn backend.main:app --host 0.0.0.0 --port $PORT
```

El archivo `render.yaml` ya contiene esta configuración:

```yaml
services:
  - type: web
    name: hegemony-fastapi-backend
    runtime: python
    plan: free
    buildCommand: python -m pip install -r requirements.txt
    startCommand: python -m uvicorn backend.main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.9
```

Checks de producción:

```text
https://hegemony-fastapi-backend.onrender.com/
https://hegemony-fastapi-backend.onrender.com/api/health
https://hegemony-fastapi-backend.onrender.com/docs
```

## Frontend en Vercel

Configuración recomendada:

```text
Root Directory: frontend
Framework Preset: Vite
Build Command: npm run build
Output Directory: dist
```

Variable de entorno:

```text
VITE_API_URL=https://hegemony-fastapi-backend.onrender.com
```

`frontend/vercel.json` mantiene el fallback de SPA para que las rutas internas respondan desde `index.html`.

## Problemas Comunes

| Síntoma | Revisión |
|---|---|
| La app abre pero no calcula | Verifica `VITE_API_URL` en Vercel. |
| La primera respuesta del backend tarda | Render Free puede dormir el servicio después de inactividad. |
| Error de CORS | Confirma que el origen de Vercel esté permitido en `backend/main.py`. |
| Vercel no encuentra el build | Confirma que `Root Directory` sea `frontend`. |

---
---

# 🇺🇸 English

## Deployment Architecture

| Service | Provider | URL |
|---|---|---|
| React/Vite frontend | Vercel | https://hegemony-linear.vercel.app/ |
| FastAPI backend | Render | https://hegemony-fastapi-backend.onrender.com/ |
| Swagger UI | Render | https://hegemony-fastapi-backend.onrender.com/docs |

## Backend on Render

Recommended settings:

```text
Name: hegemony-fastapi-backend
Runtime: Python
Plan: Free
Build Command: python -m pip install -r requirements.txt
Start Command: python -m uvicorn backend.main:app --host 0.0.0.0 --port $PORT
```

Production checks:

```text
https://hegemony-fastapi-backend.onrender.com/
https://hegemony-fastapi-backend.onrender.com/api/health
https://hegemony-fastapi-backend.onrender.com/docs
```

## Frontend on Vercel

Recommended settings:

```text
Root Directory: frontend
Framework Preset: Vite
Build Command: npm run build
Output Directory: dist
```

Environment variable:

```text
VITE_API_URL=https://hegemony-fastapi-backend.onrender.com
```

`frontend/vercel.json` keeps the SPA fallback so internal routes resolve through `index.html`.

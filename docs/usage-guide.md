# 🎬 Guía de Uso y Demo / Usage and Demo Guide

---

# 🇪🇸 Español

## Objetivo de la Demo

Mostrar cómo una experiencia de juego puede ocultar un método numérico real. El jugador toma decisiones de economía política; el backend calcula el ingreso mínimo requerido con Newton-Raphson y el frontend lo presenta como una consecuencia narrativa.

## Flujo Recomendado

1. Abrir https://hegemony-linear.vercel.app/.
2. Mostrar las cuatro clases: Clase Trabajadora, Clase Capitalista, Clase Media y Estado.
3. Explicar que cada turno modifica una parte distinta de la economía.
4. En la Clase Trabajadora, ajustar población, meta de prosperidad y asignación de obreros.
5. Ejecutar **Calcular Ingreso Mínimo Necesario**.
6. Mostrar el modal narrativo con el ingreso requerido.
7. Abrir **Modo profesor** para explicar raíz, error, iteraciones y convergencia.
8. Entrar a https://hegemony-fastapi-backend.onrender.com/docs para mostrar el endpoint `POST /api/calculate-income`.

## Guion Sugerido para Video

```text
1. Presentación: Hegemony Linear es un simulador hotseat académico.
2. Problema: la Clase Trabajadora necesita saber si sus ingresos cubren bienestar.
3. Modelo: el backend resuelve f(I) = W(I) - S*.
4. Método: Newton-Raphson aproxima la raíz I*.
5. Juego: el usuario ve decisiones y consecuencias, no una calculadora aislada.
6. Evidencia: el modo profesor muestra iteraciones y convergencia.
7. Arquitectura: React/Vite consume FastAPI, desplegados en Vercel y Render.
8. Cierre: el proyecto combina UX, API, pruebas y análisis numérico.
```

## Comandos Locales

Backend:

```powershell
cd D:\Desarrollo\Proyectos\UPB\Hegemony-Linear
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```

Frontend:

```powershell
cd D:\Desarrollo\Proyectos\UPB\Hegemony-Linear\frontend
fnm use 24.14.0
npm.cmd install
Copy-Item .env.example .env
npm.cmd run dev -- --host 127.0.0.1 --port 5173
```

---
---

# 🇺🇸 English

## Demo Objective

Show how a game experience can hide a real numerical method. The player makes political economy decisions; the backend computes the required minimum income with Newton-Raphson and the frontend turns it into a narrative consequence.

## Recommended Flow

1. Open https://hegemony-linear.vercel.app/.
2. Show the four classes: Working Class, Capitalist Class, Middle Class and State.
3. Explain that each active turn changes a different part of the economy.
4. In Working Class, adjust population, prosperity target and worker allocation.
5. Run **Calcular Ingreso Mínimo Necesario**.
6. Show the narrative result modal.
7. Open **Modo profesor** to explain root, error, iterations and convergence.
8. Open https://hegemony-fastapi-backend.onrender.com/docs to show `POST /api/calculate-income`.

## Suggested Video Script

```text
1. Intro: Hegemony Linear is an academic hotseat simulator.
2. Problem: the Working Class needs to know whether income covers welfare.
3. Model: the backend solves f(I) = W(I) - S*.
4. Method: Newton-Raphson approximates the root I*.
5. Game: the user sees decisions and consequences, not an isolated calculator.
6. Evidence: teacher mode shows iterations and convergence.
7. Architecture: React/Vite consumes FastAPI, deployed on Vercel and Render.
8. Closing: the project combines UX, API, tests and numerical analysis.
```

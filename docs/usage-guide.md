# Usage and Demo Guide | Guia de Uso y Demo

**[Espanol](#espanol) | [English](#english)**

---

<h2 id="espanol">Espanol</h2>

## Objetivo de la demo

Mostrar como una experiencia de juego puede ocultar un metodo numerico real. El jugador toma decisiones de economia politica; el backend calcula el ingreso minimo requerido con Newton-Raphson y el frontend lo presenta como una consecuencia narrativa.

## Flujo recomendado

1. Abrir https://hegemony-linear.vercel.app/.
2. Mostrar las cuatro clases: Clase Trabajadora, Clase Capitalista, Clase Media y Estado.
3. Explicar que el turno activo modifica una parte distinta de la economia.
4. En Clase Trabajadora, ajustar poblacion, meta de prosperidad y asignacion de obreros.
5. Ejecutar **Calcular Ingreso Minimo Necesario**.
6. Mostrar el modal narrativo con el ingreso requerido.
7. Abrir **Modo profesor** para explicar raiz, error, iteraciones y convergencia.
8. Entrar a https://hegemony-fastapi-backend.onrender.com/docs para mostrar el endpoint `POST /api/calculate-income`.

## Guion sugerido para video

```text
1. Presentacion: Hegemony Linear es un simulador hotseat academico.
2. Problema: la Clase Trabajadora necesita saber si sus ingresos cubren bienestar.
3. Modelo: el backend resuelve f(I) = W(I) - S*.
4. Metodo: Newton-Raphson aproxima la raiz I*.
5. Juego: el usuario ve decisiones y consecuencias, no una calculadora suelta.
6. Evidencia: el modo profesor muestra iteraciones y convergencia.
7. Arquitectura: React/Vite consume FastAPI, desplegados en Vercel y Render.
8. Cierre: el proyecto combina UX, API, pruebas y analisis numerico.
```

## Comandos locales

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

<h2 id="english">English</h2>

## Demo objective

Show how a game experience can hide a real numerical method. The player makes political economy decisions; the backend computes the required minimum income with Newton-Raphson and the frontend turns it into a narrative consequence.

## Recommended flow

1. Open https://hegemony-linear.vercel.app/.
2. Show the four classes: Working Class, Capitalist Class, Middle Class and State.
3. Explain that each active turn changes a different part of the economy.
4. In Working Class, adjust population, prosperity target and worker allocation.
5. Run **Calcular Ingreso Minimo Necesario**.
6. Show the narrative result modal.
7. Open **Modo profesor** to explain root, error, iterations and convergence.
8. Open https://hegemony-fastapi-backend.onrender.com/docs to show `POST /api/calculate-income`.

## Suggested video script

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

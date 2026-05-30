# 🎓 Cómo se Construyó Hegemony Linear / How Hegemony Linear Was Built

---

# 🇪🇸 Español

Bienvenido a la guía educativa de **Hegemony Linear**.

Este proyecto fue creado como una entrega académica para la materia de **Análisis Numérico** en la **Universidad Pontificia Bolivariana (UPB)**. Su objetivo principal es demostrar que un método numérico no tiene que vivir aislado en una calculadora: también puede integrarse dentro de una experiencia interactiva, visual y cercana a un escenario de toma de decisiones.

En este caso, el método seleccionado fue **Newton-Raphson**, aplicado al cálculo del ingreso mínimo que necesita la **Clase Trabajadora** para alcanzar una meta de prosperidad dentro de una simulación económica inspirada en dinámicas de economía política.

---

## 🎯 El Reto Académico

La pregunta central del proyecto fue:

> ¿Cómo usar un método numérico real dentro de una experiencia de juego sin que el usuario sienta que está usando una calculadora tradicional?

Para responderla, el proyecto combina tres capas:

- **Experiencia de juego:** un tablero hotseat con clases sociales, salarios, impuestos y bienes.
- **Modelo matemático:** una función de bienestar que depende del ingreso disponible.
- **Motor numérico:** Newton-Raphson para encontrar la raíz de la ecuación.

---

## 🧮 El Modelo Numérico

El backend resuelve la ecuación:

```text
f(I) = W(I) - S*
```

Donde:

- `I` es el ingreso bruto de la Clase Trabajadora.
- `W(I)` es la función de bienestar calculada a partir de comida, salud, educación y ocio.
- `S*` es la meta de prosperidad definida para la ronda.

El objetivo es encontrar el valor de `I` que hace que:

```text
f(I) = 0
```

En otras palabras: encontrar el ingreso mínimo que permite que el bienestar calculado iguale la meta de prosperidad.

---

## ⚙️ Paso 1: Separar el Dominio del Framework

El primer paso fue construir el motor en Python sin depender directamente de FastAPI ni de React.

La lógica principal vive en:

```text
hegemony_calculator/
├── core/       # Modelos, bienestar y métodos numéricos
├── engine/     # Reglas de simulación económica
├── services/   # Servicios de cálculo y validación
└── data/       # Datos base del tablero
```

Esta separación permite probar el modelo matemático sin levantar el servidor web y sin abrir el navegador.

> **Aprendizaje clave:** antes de construir una interfaz, conviene aislar la lógica que realmente define el comportamiento del sistema.

---

## 🧠 Paso 2: Implementar Newton-Raphson

Newton-Raphson aproxima una raíz usando la fórmula:

```text
I(n+1) = I(n) - f(I(n)) / f'(I(n))
```

En el proyecto, cada iteración guarda:

- Número de iteración.
- Estimación actual.
- Valor de la función.
- Error relativo.
- Valor de la derivada.

Esto permite que el resultado no sea una caja negra: el **Modo profesor** puede mostrar cómo converge el método paso a paso.

> **Aprendizaje clave:** un buen proyecto académico no solo entrega el resultado, también permite explicar cómo se obtuvo.

---

## 🎮 Paso 3: Convertir Matemática en Experiencia de Juego

El jugador no ve inicialmente la fórmula `f(I) = W(I) - S*`. En cambio, interactúa con:

- Salarios ofrecidos.
- Impuestos.
- Precios de salud y educación.
- Comida disponible.
- Meta de prosperidad.
- Asignación de obreros.

Cuando ejecuta el cálculo, la aplicación transforma el resultado numérico en una consecuencia narrativa:

```text
La Clase Trabajadora necesita al menos 407.96V para cubrir comida, impuestos y alcanzar su meta de prosperidad.
```

> **Aprendizaje clave:** la misma matemática puede presentarse de forma técnica para el profesor y de forma narrativa para el usuario.

---

## 🌐 Paso 4: Exponer el Motor con FastAPI

El backend se implementó con **FastAPI** para convertir el motor numérico en una API REST.

Endpoint principal:

```http
POST /api/calculate-income
```

Este endpoint recibe el estado económico del tablero y responde con:

- `I_star`: raíz calculada.
- `required_income`: ingreso mínimo requerido.
- `converged`: estado de convergencia.
- `iterations`: número de iteraciones.
- `final_error`: error final.
- `history`: historial de iteraciones.
- `narrative`: explicación lista para la interfaz.

> **Aprendizaje clave:** una API bien diseñada permite que el frontend consuma matemática compleja sin duplicar reglas de negocio.

---

## ⚛️ Paso 5: Construir el Frontend con React

El frontend fue construido con **React + Vite + Tailwind CSS**.

La interfaz incluye:

- Tablero hotseat.
- Selector de clases.
- Panel de estado económico.
- Asignación de trabajadores.
- Modal narrativo de resultados.
- Panel docente con gráfica de convergencia.

Para visualizar las iteraciones se usó **Recharts**, permitiendo que el método Newton-Raphson sea entendible de forma visual.

> **Aprendizaje clave:** una buena interfaz puede convertir resultados numéricos en decisiones comprensibles.

---

## 🧪 Paso 6: Verificar el Motor con Pruebas

El proyecto incluye pruebas automatizadas con **Pytest** para validar:

- Método de bisección.
- Método de Newton-Raphson.
- Modelo de bienestar.
- Cálculo de impuestos.
- Validación de parámetros.
- Integración del motor de juego.

Comando de verificación:

```powershell
python -m pytest
```

> **Aprendizaje clave:** los métodos numéricos deben probarse con casos controlados, porque pequeños errores pueden cambiar por completo el resultado.

---

## 🚀 Paso 7: Despliegue Público

El proyecto se separó en dos servicios:

| Servicio | Plataforma | URL |
|---|---|---|
| Frontend | Vercel | https://hegemony-linear.vercel.app/ |
| Backend | Render | https://hegemony-fastapi-backend.onrender.com/ |

Esta separación evita mezclar responsabilidades:

- Vercel sirve la aplicación React.
- Render ejecuta la API FastAPI.
- El frontend se comunica con el backend usando `VITE_API_URL`.

> **Aprendizaje clave:** separar frontend y backend facilita el despliegue, la depuración y la escalabilidad.

---

## 🧩 Qué Puede Aprender un Estudiante

Este proyecto es útil para estudiar:

- Aplicación real de Newton-Raphson.
- Diseño de funciones de bienestar.
- Separación entre dominio, API e interfaz.
- Validación de datos con Pydantic.
- Consumo de APIs desde React.
- Visualización de convergencia numérica.
- Pruebas unitarias e integración.
- Despliegue moderno con Vercel y Render.

---

## 🧪 Ejercicios Sugeridos

Si quieres extender el proyecto, intenta:

1. Agregar comparación visual entre Newton-Raphson, bisección y secante.
2. Crear un endpoint para simular varios escenarios de impuestos.
3. Añadir una gráfica de sensibilidad entre salario, impuestos y prosperidad.
4. Implementar una dificultad por ronda que cambie la meta `S*`.
5. Crear pruebas para casos donde Newton-Raphson no converge.
6. Agregar una explicación paso a paso dentro del Modo profesor.

---

## 💡 Reflexión Final

Construir **Hegemony Linear** demostró que los métodos numéricos pueden enseñarse más allá de ejercicios aislados. Al integrarlos en una simulación interactiva, el estudiante no solo calcula una raíz: entiende por qué esa raíz importa dentro de un sistema económico.

La lección principal es que la ingeniería de software puede convertir teoría matemática en experiencias comprensibles, verificables y desplegadas para usuarios reales.

---
---

# 🇺🇸 English

Welcome to the educational guide for **Hegemony Linear**.

This project was created as an academic deliverable for the **Numerical Analysis** course at **Universidad Pontificia Bolivariana (UPB)**. Its main goal is to show that a numerical method does not need to live inside an isolated calculator: it can be integrated into an interactive, visual and decision-oriented experience.

The selected method was **Newton-Raphson**, applied to calculate the minimum income required for the **Working Class** to reach a prosperity target inside a political economy simulation.

---

## 🎯 The Academic Challenge

The central question was:

> How can a real numerical method be used inside a game experience without making the user feel like they are using a traditional calculator?

The answer combines three layers:

- **Game experience:** a hotseat board with social classes, wages, taxes and goods.
- **Mathematical model:** a welfare function based on disposable income.
- **Numerical engine:** Newton-Raphson to find the root of the equation.

---

## 🧮 The Numerical Model

The backend solves:

```text
f(I) = W(I) - S*
```

Where:

- `I` is the gross income of the Working Class.
- `W(I)` is the welfare function calculated from food, health, education and leisure.
- `S*` is the prosperity target for the round.

The goal is to find the value of `I` where:

```text
f(I) = 0
```

That means finding the minimum income that makes calculated welfare match the prosperity target.

---

## ⚙️ Step 1: Separate Domain Logic from Frameworks

The numerical engine was built in Python without depending directly on FastAPI or React.

Core logic lives in:

```text
hegemony_calculator/
├── core/       # Models, welfare and numerical methods
├── engine/     # Economic simulation rules
├── services/   # Calculation and validation services
└── data/       # Base board data
```

This separation makes it possible to test the mathematical model without starting the web server or opening the browser.

> **Key takeaway:** before building an interface, isolate the logic that truly defines system behavior.

---

## 🧠 Step 2: Implement Newton-Raphson

Newton-Raphson approximates a root with:

```text
I(n+1) = I(n) - f(I(n)) / f'(I(n))
```

Each iteration stores:

- Iteration number.
- Current estimate.
- Function value.
- Relative error.
- Derivative value.

This makes the result explainable: **Teacher mode** can show how the method converges step by step.

> **Key takeaway:** a strong academic project should not only return the answer, it should explain how the answer was obtained.

---

## 🎮 Step 3: Turn Mathematics into Gameplay

The player does not initially see `f(I) = W(I) - S*`. Instead, the player interacts with:

- Offered wages.
- Taxes.
- Health and education prices.
- Available food.
- Prosperity target.
- Worker allocation.

When the calculation runs, the application transforms the numerical result into a narrative consequence.

> **Key takeaway:** the same mathematics can be presented technically for the teacher and narratively for the user.

---

## 🌐 Step 4: Expose the Engine with FastAPI

The backend uses **FastAPI** to expose the numerical engine as a REST API.

Main endpoint:

```http
POST /api/calculate-income
```

The endpoint receives the board's economic state and responds with the calculated root, convergence state, iteration count, final error, history and narrative explanation.

> **Key takeaway:** a well-designed API lets the frontend consume complex mathematics without duplicating business rules.

---

## ⚛️ Step 5: Build the Frontend with React

The frontend was built with **React + Vite + Tailwind CSS**.

The interface includes:

- Hotseat board.
- Class selector.
- Economic state panel.
- Worker allocation.
- Narrative result modal.
- Teacher panel with convergence chart.

**Recharts** is used to visualize iterations, making Newton-Raphson easier to understand.

> **Key takeaway:** a good interface can turn numerical outputs into understandable decisions.

---

## 🧪 Step 6: Verify the Engine with Tests

The project includes **Pytest** coverage for:

- Bisection method.
- Newton-Raphson method.
- Welfare model.
- Tax calculation.
- Parameter validation.
- Game engine integration.

Verification command:

```powershell
python -m pytest
```

> **Key takeaway:** numerical methods need controlled tests because small mistakes can completely change the result.

---

## 🚀 Step 7: Public Deployment

The project is deployed as two services:

| Service | Platform | URL |
|---|---|---|
| Frontend | Vercel | https://hegemony-linear.vercel.app/ |
| Backend | Render | https://hegemony-fastapi-backend.onrender.com/ |

This separation keeps responsibilities clear:

- Vercel serves the React application.
- Render runs the FastAPI backend.
- The frontend communicates with the backend through `VITE_API_URL`.

---

## 🧩 What Students Can Learn

This project is useful for studying:

- Real Newton-Raphson application.
- Welfare function design.
- Domain/API/UI separation.
- Data validation with Pydantic.
- API consumption from React.
- Numerical convergence visualization.
- Unit and integration testing.
- Modern deployment with Vercel and Render.

---

## 🧪 Suggested Exercises

Try extending the project by:

1. Adding a visual comparison between Newton-Raphson, bisection and secant.
2. Creating an endpoint for multiple tax scenarios.
3. Adding a sensitivity chart between wage, taxes and prosperity.
4. Implementing round difficulty by changing the target `S*`.
5. Creating tests for non-convergence cases.
6. Adding a step-by-step explanation inside Teacher mode.

---

## 💡 Final Reflection

Building **Hegemony Linear** showed that numerical methods can be taught beyond isolated exercises. By integrating them into an interactive simulation, students do not just calculate a root: they understand why that root matters inside an economic system.

The main lesson is that software engineering can turn mathematical theory into understandable, verifiable and deployed experiences for real users.

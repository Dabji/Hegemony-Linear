# Hegemony Game

Videojuego web en Python inspirado en *Hegemony: Lead Your Class to Victory*. El jugador toma decisiones de clase, asigna obreros, compra bienes, propone leyes y atraviesa rondas de produccion, elecciones y puntuacion.

El motor de analisis numerico existe, pero es invisible para el jugador. Los cinco metodos de busqueda de raices calculan internamente el ingreso minimo necesario para alcanzar una meta de Prosperidad; la interfaz lo traduce a consecuencias narrativas de juego.

## Experiencia

- Intro con seleccion de clase y numero de jugadores.
- Tablero principal con empresas privadas, empresas publicas, politicas y ronda actual.
- Acciones contextuales: asignar obreros, comprar comida, salud, educacion u ocio, hacer huelga y proponer leyes.
- Produccion automatica: salarios, impuestos, bienes producidos y necesidades de comida.
- Elecciones con cubos, influencia y cambio de politica.
- Puntuacion de ronda con PV, prosperidad y narrativa.
- Panel docente colapsable: tabla de los cinco metodos, raiz `I*`, grafica de `f(I)` y convergencia.

## Arquitectura

```text
hegemony_calculator/
|-- core/
|   |-- models.py
|   |-- welfare.py
|   `-- methods/
|-- engine/
|   |-- game_engine.py
|   |-- income_solver.py
|   |-- tax_calculator.py
|   |-- production.py
|   |-- elections.py
|   `-- ai_players.py
|-- ui/
|   |-- app.py
|   |-- screens/
|   `-- components/
`-- data/
```

El paquete `hegemony_calculator` contiene todo: nucleo numerico, motor de juego, datos y experiencia Streamlit.

## Requisitos

- Python 3.11 o superior
- Probado con Python 3.13 usando el Python incluido en pgAdmin

## Instalacion

Si tienes Python en `PATH`:

```powershell
python -m pip install -r requirements.txt
```

Si usas el Python de pgAdmin:

```powershell
& "C:\Program Files\PostgreSQL\18\pgAdmin 4\python\python.exe" -m pip install --user -r requirements.txt
```

## Ejecucion

La forma mas simple es:

```powershell
python app.py
```

Si tu terminal no reconoce `python`, usa el interprete de pgAdmin:

```powershell
& "C:\Program Files\PostgreSQL\18\pgAdmin 4\python\python.exe" app.py
```

Tambien puedes lanzar Streamlit directamente:

```powershell
& "C:\Program Files\PostgreSQL\18\pgAdmin 4\python\python.exe" -m streamlit run app.py
```

## Pruebas

```powershell
& "C:\Program Files\PostgreSQL\18\pgAdmin 4\python\python.exe" -m pytest
```

## Regla de diseno

Si el jugador tiene que saber que es `f(I)`, el diseno fallo. Si entiende que necesita mas ingreso, mejores politicas o mas bienes para prosperar, el diseno funciono.

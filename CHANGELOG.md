# 📦 Changelog

Todos los cambios relevantes de **Hegemony Linear** se documentan en este archivo.

---

## [v1.0.0] - 2026-05-30

### 🚀 Lanzamiento Oficial

Primera versión estable del simulador web **Hegemony Linear**, desarrollado como proyecto académico de **Análisis Numérico (UPB)**. Esta versión consolida la experiencia hotseat, el frontend React/Vite, el backend FastAPI y el motor Newton-Raphson para calcular el ingreso mínimo necesario de la Clase Trabajadora.

### ✨ Añadido

- Frontend público desplegado en Vercel: https://hegemony-linear.vercel.app/.
- Backend FastAPI público desplegado en Render: https://hegemony-fastapi-backend.onrender.com/.
- Documentación interactiva de API con Swagger UI.
- Motor numérico con Newton-Raphson expuesto en `POST /api/calculate-income`.
- Modo profesor con raíz calculada, error final, convergencia e iteraciones.
- README bilingüe con capturas reales del despliegue.
- Documentación Open Source: MIT License, Code of Conduct, Contributing y Security Policy.
- Plantillas de Issues y Pull Requests para GitHub.

### 🛠️ Cambiado

- Reestructuración del README para presentación de portafolio y publicación Open Source.
- Actualización de `frontend/.env.example` para apuntar al backend productivo.
- Optimización del build Vite separando chunks de gráficas e iconografía.
- Ajuste de `pytest.ini` para usar caché local del repositorio.
- Limpieza de dependencias Python enfocadas en FastAPI y el motor numérico.

### 🧹 Eliminado

- UI legacy local que ya no forma parte del producto desplegado.
- Configuración de Netlify no utilizada.
- Artefactos `__pycache__` previamente versionados.
- Documentación interna de configuración de GitHub que no debía publicarse.

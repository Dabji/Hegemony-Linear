# 🔒 Política de Seguridad / Security Policy

---

# 🇪🇸 Español

## Versiones Soportadas

| Versión | Estado |
|---|---|
| `main` | Soportada |
| Releases anteriores | Mejor esfuerzo |

## Reportar una Vulnerabilidad

Si encuentras una vulnerabilidad en **Hegemony Linear**, **no abras un issue público**. Reporta el problema de forma privada al propietario del repositorio o mediante una GitHub Security Advisory privada.

Incluye, si es posible:

- Descripción clara del problema.
- Pasos para reproducirlo.
- Impacto estimado.
- Evidencia técnica, capturas o payloads de prueba.
- Entorno donde ocurrió el problema.

## Alcance

Son reportes válidos:

- Errores de CORS o exposición no intencional de orígenes.
- Validación insuficiente de payloads en la API FastAPI.
- Exposición de secretos, tokens o variables de entorno.
- Dependencias vulnerables con impacto real.
- Fallos que permitan alterar resultados del motor numérico fuera de las validaciones esperadas.

## Fuera de Alcance

- Reportes sin pasos de reproducción.
- Vulnerabilidades en servicios externos no controlados por este repositorio.
- Problemas derivados de configuraciones locales inseguras fuera del proyecto.

No publiques datos sensibles, tokens, credenciales ni información personal en issues, Pull Requests o comentarios públicos.

---
---

# 🇺🇸 English

## Supported Versions

| Version | Status |
|---|---|
| `main` | Supported |
| Older releases | Best effort |

## Reporting a Vulnerability

If you find a vulnerability in **Hegemony Linear**, **do not open a public issue**. Report it privately to the repository owner or through a private GitHub Security Advisory.

Include, when possible:

- Clear problem description.
- Reproduction steps.
- Estimated impact.
- Technical evidence, screenshots or test payloads.
- Environment where the issue occurred.

## Scope

Valid reports include:

- CORS mistakes or unintended origin exposure.
- Insufficient payload validation in the FastAPI backend.
- Exposure of secrets, tokens or environment variables.
- Vulnerable dependencies with real impact.
- Failures that allow numerical engine results to be altered outside expected validation rules.

## Out of Scope

- Reports without reproduction steps.
- Vulnerabilities in external services not controlled by this repository.
- Issues caused by insecure local configurations outside the project.

Do not publish sensitive data, tokens, credentials or personal information in issues, Pull Requests or public comments.

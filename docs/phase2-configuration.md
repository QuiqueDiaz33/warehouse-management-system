# Configuración externa de la Fase 2

El repositorio no almacena tokens ni contraseñas. Antes de activar el pipeline completo deben configurarse estos valores en GitHub.

## Variables del repositorio

- `API_BASE_URL`: URL HTTPS del backend desplegado en QA.
- `SONAR_ORGANIZATION`: identificador de la organización en SonarCloud.
- `SONAR_PROJECT_KEY`: clave del proyecto en SonarCloud.

## Secrets del repositorio

- `SONAR_TOKEN`: token de análisis generado en SonarCloud.
- `API_TEST_USERNAME`: usuario exclusivo de automatización con permisos de solo lectura cuando sea posible.
- `API_TEST_PASSWORD`: contraseña de esa cuenta.

## Protección de ambientes

Crear los ambientes de GitHub `qa` y `production`. El ambiente `production` debe requerir aprobación manual. El job `Deployment gate` no despliega por sí mismo: confirma que todas las etapas previas aprobaron y deja preparada la compuerta para agregar el mecanismo de despliegue autorizado.

## Quality gate

El quality gate debe incluir, como mínimo, ausencia de hallazgos Blocker y Critical en código nuevo y cobertura informada para los módulos modificados. La primera ejecución se conserva como línea base con bugs, vulnerabilidades, code smells, duplicación y deuda técnica. No se declara el gate aprobado hasta que SonarCloud publique un resultado real.

## Reglas de rama

En `qa` y `main`, marcar como requerido el check agregado por el workflow `Phase 2 quality pipeline`. El merge queda bloqueado automáticamente si compilación, unitarias, quality gate o Newman fallan.

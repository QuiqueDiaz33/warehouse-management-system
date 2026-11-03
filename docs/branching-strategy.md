# Estrategia de ramas y promoción

## Ramas permanentes

- `dev`: integración diaria. Recibe cambios desde ramas `feature/*` mediante pull request.
- `qa`: versión candidata para pruebas funcionales, de API, análisis estático y carga.
- `main`: versión aprobada para producción.

## Flujo de cambios

1. Cada cambio comienza en una rama `feature/*` creada desde `dev`.
2. La rama se integra a `dev` mediante pull request y con el pipeline aprobado.
3. La promoción a QA se realiza mediante un pull request `dev -> qa`.
4. La promoción a producción se realiza mediante un pull request `qa -> main`.
5. No se permiten cambios directos sobre `qa` o `main`.

## Criterios obligatorios

- Todo pull request debe describir objetivo, alcance y evidencia de validación.
- Los checks de compilación, pruebas unitarias, análisis estático y pruebas de API deben aprobar antes del merge.
- Los merges hacia `qa` y `main` deben estar bloqueados por reglas de protección de rama si falla un check requerido.
- Una revisión efectiva debe señalar riesgos, cobertura, diseño o errores concretos; una aprobación sin observaciones no se registra como revisión técnica efectiva.
- Los defectos encontrados en QA regresan a una rama `fix/*` creada desde `dev`; no se corrigen directamente en `qa`.
- La promoción a `main` requiere evidencia de pruebas de carga y aceptación del ambiente QA.

## Evidencia mínima por pull request

- Enlace al pipeline aprobado.
- Resumen de pruebas nuevas o modificadas.
- Resultado de cobertura de los módulos críticos afectados.
- Resultado del quality gate.
- Resultado Newman cuando cambie un endpoint o flujo de negocio.
- Revisor y observaciones atendidas. En un proyecto individual, la autoevaluación se identifica expresamente como tal y no se presenta como revisión externa.

## Configuración esperada en GitHub

Para `qa` y `main`:

- Require a pull request before merging.
- Require status checks to pass before merging.
- Require branches to be up to date before merging.
- Bloquear force pushes y eliminaciones.

Los checks requeridos deben corresponder a los nombres publicados por `.github/workflows/ci.yml`.

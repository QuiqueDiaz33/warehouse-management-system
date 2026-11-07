# Estado verificable de la Fase 2

Fecha de corte: 4 de noviembre de 2026.

## E9. Estrategia de ramas y control de cambios

- Estrategia `feature/* -> dev -> qa -> main` documentada.
- Promociones realizadas mediante pull requests y pipeline aprobado.
- PR de promoción a producción: `#11`, merge `00c7447`.
- La revisión externa exigida no puede acreditarse como autoevaluación. El
  proyecto es individual y esta limitación debe presentarse al docente.
- Falta conservar captura de las reglas de protección de `qa` y `main`.

## E10. Pruebas unitarias

- 60 pruebas backend y 3 frontend aprobadas: 63 en total.
- Uso documentado de dobles en más de tres pruebas.
- Ejecución automatizada dentro del pipeline.
- Cobertura actual documentada en `docs/coverage-evidence.md`.
- Incremento demostrado: línea base medida en el commit `d8dedde` (0 %, sin
  suite unitaria); los seis módulos críticos suben entre +32 y +100 pp.

## E11. Pruebas de API

- Colección Postman versionada con 26 solicitudes (135 aserciones) y flujo de ventas encadenado que incluye línea de venta, reserva y liberación de stock.
- Ejecución Newman automatizada y aprobada en el pipeline.
- El informe final debe incluir el flujo encadenado y una captura del reporte
  Newman generado como artefacto.

## E12. Análisis estático

- SonarCloud integrado y Quality Gate aprobado en el pipeline #24.
- Estado inicial (d8dedde) y actual (fe04865) documentados en
  [static-analysis.md](static-analysis.md), con datos de la API de SonarCloud.
- Sin hallazgos Blocker ni Critical. Los dos Minor de CORS en backend/main.py
  se corrigieron; los valores finales se registran tras el análisis de main.

## E13. Integración y despliegue continuo

- Seis etapas en orden: build, unitarias, SonarCloud con quality gate, Postman,
  compuerta y despliegue a Azure.
- El despliegue corre con cada push a main mediante OIDC. El primero se ejecutó
  el 6 de noviembre con el commit c760deb, con smoke test aprobado.
- Detalle en [deployment.md](deployment.md).

## E14. Pruebas de carga

- Escenario k6 ejecutado sobre Azure con dos endpoints críticos.
- Rampa a 50 usuarios y cinco minutos sostenidos.
- Promedio, p95, throughput y error documentados.
- Comparado con RNF-01 y RNF-02 de E1: no se cumplen. El p95 fue 29.6 s frente
  a un máximo de 3 s y la tasa de error 24.66 % frente a 1 %.

## E15. Video

- Pendiente grabar el video final, máximo diez minutos.
- Debe mostrar el pipeline completo, Quality Gate, Newman, k6 y conclusiones.

## E16. Bitácora individual

- Borrador versionado en `docs/individual-log-enrique-morales.md`.
- Debe revisarse y exportarse al formato final requerido para la entrega.

## Bloqueos que requieren evidencia externa

1. revisión efectiva de otro integrante en un proyecto individual;
2. porcentaje de cobertura base de E2;
3. métricas iniciales históricas de SonarCloud;
4. decisión sobre despliegue automático o promoción manual;
5. enlace definitivo del video en YouTube.

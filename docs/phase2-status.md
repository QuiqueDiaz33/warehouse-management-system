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

- 39 pruebas backend y 3 frontend aprobadas: 42 en total.
- Uso documentado de dobles en más de tres pruebas.
- Ejecución automatizada dentro del pipeline.
- Cobertura actual documentada en `docs/coverage-evidence.md`.
- Pendiente: demostrar el incremento de 20 puntos contra una línea base
  porcentual de E2.

## E11. Pruebas de API

- Colección Postman versionada con 15 solicitudes.
- Ejecución Newman automatizada y aprobada en el pipeline.
- El informe final debe incluir el flujo encadenado y una captura del reporte
  Newman generado como artefacto.

## E12. Análisis estático

- SonarCloud integrado y Quality Gate aprobado en el pipeline #24.
- Pendiente: tabla verificable del estado inicial y final con bugs,
  vulnerabilidades, code smells, duplicación y deuda técnica.
- No se registran valores inventados si el dashboard inicial no fue capturado.

## E13. Integración y despliegue continuo

- Orden actual: build, unitarias, Sonar/Quality Gate, Postman y compuerta.
- Pipeline #24 aprobado en `main` en 2 minutos 35 segundos.
- La etapa `Deployment gate` no ejecuta un despliegue a Azure; solo confirma
  que las validaciones previas pasaron. Falta automatizar el despliegue o
  documentar y obtener aceptación para una promoción manual.

## E14. Pruebas de carga

- Escenario k6 ejecutado sobre Azure con dos endpoints críticos.
- Rampa a 50 usuarios y cinco minutos sostenidos.
- Promedio, p95, throughput y error documentados.
- Conclusión: el plan F1 no cumple los objetivos de rendimiento definidos.

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

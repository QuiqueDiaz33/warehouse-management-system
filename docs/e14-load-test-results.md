# E14. Resultados de pruebas de carga

## Escenario ejecutado

- Fecha: 3 de noviembre de 2026.
- Ambiente: API desplegada en Azure App Service, plan Linux F1.
- Herramienta: k6 2.3.0.
- Endpoints críticos: `GET /items/` y `GET /stock/`.
- Carga: rampa de 0 a 50 usuarios virtuales durante 1 minuto, 50 usuarios sostenidos durante 5 minutos y descenso durante 30 segundos.
- Autenticación: cuenta de prueba suministrada mediante variables de entorno.

## Comparación con los requerimientos no funcionales de E1

Los objetivos vienen de la sección 1.5 del entregable E1 (WLMS_Fase_1_E1-E5.docx).

| Requerimiento de E1 | Qué pide | Resultado medido | Cumple |
| --- | --- | ---: | --- |
| RNF-01, tiempo de respuesta | El 95 % de las lecturas en 2 s o menos | p95 de 29,563.64 ms | No |
| RNF-01, tiempo máximo | Ninguna lectura por encima de 5 s | Hubo timeouts en ambos endpoints | No |
| RNF-02, percentil 95 bajo carga | p95 de 3 s como máximo | p95 de 29,563.64 ms | No |
| RNF-02, tasa de error | 1 % como máximo | 24.66 % | No |

| Métrica reportada | Valor |
| --- | ---: |
| Tiempo de respuesta promedio | 8,582.38 ms |
| Percentil 95 | 29,563.64 ms |
| Throughput | 4.934 solicitudes por segundo |
| Tasa de error | 24.66 % |

La ejecución generó 2,072 solicitudes y completó 1,026 iteraciones. Se registraron 511 solicitudes fallidas. La tasa de aserciones aprobadas fue 75.34 %.

El escenario de E14 no es idéntico al de RNF-02: la rúbrica pide 50 usuarios virtuales durante 5 minutos y E1 definió 20 usuarios durante 10 minutos. La prueba se hizo con el escenario de la rúbrica, que tiene más del doble de usuarios concurrentes. Con esa carga ningún indicador queda cerca del límite: el p95 es casi diez veces el máximo permitido y la tasa de error es veinticuatro veces mayor.

## Conclusión

El sistema no cumple los requerimientos no funcionales de rendimiento RNF-01 y RNF-02 definidos en E1. Durante la rampa inicial respondió con normalidad, pero al aproximarse a 50 usuarios virtuales aumentaron los tiempos de espera y aparecieron timeouts en ambos endpoints. La capacidad del plan gratuito F1 es insuficiente para sostener esta carga con los límites establecidos. Para confirmar el comportamiento con exactamente 20 usuarios durante 10 minutos, como lo define RNF-02, se recomienda repetir la prueba con ese escenario además del de la rúbrica.

Antes de repetir la prueba se recomienda utilizar un plan con mayor capacidad, habilitar métricas de App Service y PostgreSQL, revisar el uso de conexiones y analizar los endpoints con mayor latencia. El resultado no invalida la funcionalidad comprobada por las pruebas unitarias y de API; demuestra una limitación de rendimiento bajo carga concurrente.

Los archivos completos `summary.json` y `summary-export.json` se conservaron localmente en `load-tests/results/`. Esa carpeta no se versiona porque contiene resultados generados por cada ejecución.

# E14. Resultados de pruebas de carga

## Escenario ejecutado

- Fecha: 3 de noviembre de 2026.
- Ambiente: API desplegada en Azure App Service, plan Linux F1.
- Herramienta: k6 2.3.0.
- Endpoints críticos: `GET /items/` y `GET /stock/`.
- Carga: rampa de 0 a 50 usuarios virtuales durante 1 minuto, 50 usuarios sostenidos durante 5 minutos y descenso durante 30 segundos.
- Autenticación: cuenta de prueba suministrada mediante variables de entorno.

## Criterios evaluados

| Indicador | Objetivo | Resultado | Estado |
| --- | ---: | ---: | --- |
| Tiempo promedio | Menor a 1,000 ms | 8,582.38 ms | No cumple |
| Percentil 95 | Menor a 2,000 ms | 29,563.64 ms | No cumple |
| Tasa de error | Menor a 1 % | 24.66 % | No cumple |
| Throughput | Informativo | 4.934 solicitudes/s | Registrado |

La ejecución generó 2,072 solicitudes y completó 1,026 iteraciones. Se registraron 511 solicitudes fallidas. La tasa de aserciones aprobadas fue 75.34 %.

## Conclusión

El sistema no cumple los objetivos de rendimiento definidos para el escenario mínimo de E14. Durante la rampa inicial respondió con normalidad, pero al aproximarse a 50 usuarios virtuales aumentaron los tiempos de espera y aparecieron timeouts en ambos endpoints. La capacidad del plan gratuito F1 es insuficiente para sostener esta carga con los límites establecidos.

Antes de repetir la prueba se recomienda utilizar un plan con mayor capacidad, habilitar métricas de App Service y PostgreSQL, revisar el uso de conexiones y analizar los endpoints con mayor latencia. El resultado no invalida la funcionalidad comprobada por las pruebas unitarias y de API; demuestra una limitación de rendimiento bajo carga concurrente.

Los archivos completos `summary.json` y `summary-export.json` se conservaron localmente en `load-tests/results/`. Esa carpeta no se versiona porque contiene resultados generados por cada ejecución.

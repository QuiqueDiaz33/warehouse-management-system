# Pruebas de carga E14

El escenario `wlms-load.js` autentica una cuenta de prueba y ejercita dos endpoints críticos de lectura: `/items/` y `/stock/`.

## Ejecución

Las credenciales se reciben exclusivamente mediante variables de entorno:

```text
k6 run -e BASE_URL=https://<api> -e WLMS_USERNAME=<usuario> -e WLMS_PASSWORD=<contraseña> load-tests/wlms-load.js
```

El escenario aumenta de 0 a 50 usuarios virtuales durante un minuto, sostiene 50 usuarios durante cinco minutos y reduce la carga durante 30 segundos.

## Métricas y criterio

- Tiempo promedio: menor a 1000 ms.
- Percentil 95: menor a 2000 ms.
- Tasa de error: menor a 1 %.
- Throughput: se registra como `http_reqs/s` en el resumen de k6.

Después de ejecutar contra QA, el archivo `load-tests/results/summary.json` debe conservarse como artefacto del pipeline. La conclusión académica debe comparar promedio, p95, throughput y errores contra los requerimientos no funcionales definidos en E1; no debe declararse cumplimiento antes de contar con resultados reales.

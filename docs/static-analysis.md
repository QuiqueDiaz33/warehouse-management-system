# Análisis estático con SonarCloud (E12)

El análisis corre en la tercera etapa del [pipeline](../.github/workflows/ci.yml), después de las pruebas unitarias, y recibe los reportes de cobertura del backend y del frontend. La etapa espera el resultado del quality gate y falla si no se aprueba, así que un gate rechazado bloquea el merge hacia qa y main.

Proyecto en SonarCloud: [QuiqueDiaz33_warehouse-management-system](https://sonarcloud.io/project/overview?id=QuiqueDiaz33_warehouse-management-system)

## Estado inicial y estado actual

El primer análisis se hizo el 2 de noviembre de 2026 sobre el commit d8dedde, que es el último antes de la Fase 2. El estado actual corresponde a la rama main en el commit fe04865, del 6 de noviembre.

| Métrica | Inicial (d8dedde) | Actual en main (fe04865) |
| --- | ---: | ---: |
| Bugs | 0 | 0 |
| Vulnerabilidades | 1 | 1 |
| Code smells | 1 | 1 |
| Duplicación | 4.1 % | 5.3 % |
| Deuda técnica | 30 min | 30 min |
| Security hotspots | 0 | 0 |
| Cobertura | sin dato | 33.3 % |
| Líneas de código | 3869 | 3049 |
| Hallazgos Blocker o Critical | 0 | 0 |
| Quality gate | sin gate configurado | aprobado |

La duplicación subió de 4.1 % a 5.3 % aunque no se agregó código duplicado. Lo que pasó es que el primer análisis se hizo sin configuración propia y revisó todo el repositorio. Después, en [sonar-project.properties](../sonar-project.properties), se limitó el análisis al backend y al código fuente del frontend, el total de líneas bajó de 3869 a 3049 y las mismas líneas duplicadas pasaron a pesar más en el porcentaje. En el código nuevo de la fase la duplicación es 0 %.

## Hallazgos

No hubo hallazgos de severidad Blocker ni Critical en ningún análisis, así que ese mínimo de la rúbrica se cumple sin cambios. Los dos hallazgos abiertos son de severidad Minor y están en la misma línea de [backend/main.py](../backend/main.py):

| Regla | Tipo | Severidad | Qué señala |
| --- | --- | --- | --- |
| python:S1313 | Code smell | Minor | Una dirección IP de la red local escrita en el código |
| python:S5332 | Vulnerabilidad | Minor | Ese mismo origen usa HTTP en lugar de HTTPS |

Los dos vienen del mismo origen de CORS, la IP 192.168.0.103 con el puerto de Vite, que se usaba para probar el frontend desde otro equipo de la red. Aunque no es obligatorio por su severidad, los corregí porque la solución es sencilla y deja el código sin vulnerabilidades abiertas.

## Remediación

Quité esa IP de los orígenes por defecto. En el código solo queda localhost para el servidor de desarrollo, y cualquier otro origen, como una IP de la red local o el frontend publicado, se agrega con la variable de entorno CORS_ORIGINS, que la aplicación ya leía. El App Service en Azure ya tiene esa variable configurada, así que el frontend publicado no se ve afectado.

Agregué una prueba en [tests/backend/test_cors.py](../tests/backend/test_cors.py) que falla si se vuelve a escribir una dirección de red en los orígenes por defecto.

El cambio llegó a main con el PR #22. En el análisis de main del 6 de noviembre, sobre el commit c760deb, vulnerabilidades y code smells bajaron de 1 a 0, la deuda técnica de 30 min a 0 min y la calificación de seguridad de B a A.

| Métrica | Inicial (d8dedde) | Antes de la corrección (fe04865) | Final (c760deb) |
| --- | ---: | ---: | ---: |
| Bugs | 0 | 0 | 0 |
| Vulnerabilidades | 1 | 1 | 0 |
| Code smells | 1 | 1 | 0 |
| Duplicación | 4.1 % | 5.3 % | 5.3 % |
| Deuda técnica | 30 min | 30 min | 0 min |
| Security hotspots | 0 | 0 | 0 |
| Cobertura | sin dato | 33.3 % | 33.3 % |
| Calificación de seguridad | B | B | A |
| Quality gate | sin gate | aprobado | aprobado |

## Quality gate

Se usa el gate por defecto de SonarCloud sobre el código nuevo. En el último análisis de main el resultado fue aprobado, con calificación A en confiabilidad, seguridad y mantenibilidad del código nuevo, duplicación de 0 % frente a un límite de 3 % y todos los security hotspots revisados.

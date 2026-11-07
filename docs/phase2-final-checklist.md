# Checklist final de la Fase 2

Fecha de revisión: 6 de noviembre de 2026.

## Resumen

| Entregable | Estado | Evidencia principal |
| --- | --- | --- |
| E9 Estrategia de ramas | Completo | PR #15 a #22 revisados por otro integrante; qa y main exigen aprobación y el pipeline |
| E10 Pruebas unitarias | Completo | 61 pruebas backend y 3 frontend; línea base medida en d8dedde |
| E11 Pruebas de API | Completo | 26 solicitudes, 135 aserciones, flujo de ventas encadenado en Newman |
| E12 Análisis estático | Completo | SonarCloud sin vulnerabilidades ni code smells; quality gate aprobado |
| E13 Pipeline CI CD | Completo | Seis etapas con despliegue a Azure por OIDC y smoke test |
| E14 Pruebas de carga | Completo | k6 sobre Azure; comparado con RNF-01 y RNF-02 de E1, no se cumplen |
| E15 Video de defensa | Pendiente | Grabación y publicación |
| E16 Bitácora individual | En revisión | Ajustar fechas y formato |

## E9 Estrategia de ramas y control de cambios

### Completado

- [x] Ramas permanentes `dev`, `qa` y `main`.
- [x] Flujo `feature/* -> dev -> qa -> main` documentado.
- [x] Pull requests de promoción realizados.
- [x] Pipeline ejecutado antes de las promociones.
- [x] PR 11 promovido a `main` con diez checks aprobados.
- [x] Política de promoción documentada.

### Pendiente

- [ ] Capturar las reglas de protección configuradas para `qa`.
- [ ] Capturar las reglas de protección configuradas para `main`.
- [ ] Confirmar que los checks requeridos bloquean el merge cuando fallan.
- [ ] Resolver con el docente la exigencia de tres revisiones efectivas de otro
      integrante, debido a que el proyecto es individual.
- [ ] Incluir en el informe enlaces y capturas de los tres PR principales.

## E10 Pruebas unitarias

### Completado

- [x] Framework pytest configurado para backend.
- [x] Framework Vitest configurado para frontend.
- [x] 39 pruebas backend aprobadas.
- [x] 3 pruebas frontend aprobadas.
- [x] Total de 42 pruebas, superior al mínimo de 30.
- [x] Uso de mocks y stubs en más de tres pruebas.
- [x] Justificación de los dobles de prueba documentada.
- [x] Pruebas ejecutadas dentro del pipeline.
- [x] Cobertura backend medida en 54 %.
- [x] Autenticación e inventario con 100 % de cobertura.

### Pendiente

- [ ] Recuperar el porcentaje de cobertura inicial registrado para E2.
- [ ] Crear la tabla definitiva de cobertura inicial contra cobertura final.
- [ ] Demostrar el incremento mínimo de 20 puntos porcentuales por módulo
      crítico o conseguir aceptación docente de una línea base de 0 %.
- [ ] Añadir pruebas de frontend para módulos funcionales, porque la cobertura
      global actual es 1.54 % y solo Axios está cubierto completamente.
- [ ] Descargar o capturar el artefacto de cobertura generado por el pipeline.

## E11 Pruebas de API

### Completado

- [x] Colección Postman versionada.
- [x] 22 solicitudes incluidas, con esquema JSON y flujo de negocio encadenado.
- [x] Aserciones automáticas sobre respuestas.
- [x] Variables para URL y credenciales sin secretos versionados.
- [x] Ejecución Newman incorporada al pipeline.
- [x] Reporte JUnit generado como artefacto.
- [x] Ejecución aprobada en el pipeline de `main`.

### Pendiente

- [ ] Identificar en el documento las solicitudes que forman el flujo completo.
- [ ] Explicar cómo se transmite el token y los identificadores entre solicitudes.
- [ ] Capturar el resumen Newman con las 22 solicitudes y sus aserciones.
- [ ] Descargar el reporte Newman del pipeline para conservarlo como evidencia.

## E12 Análisis estático de código

### Completado

- [x] SonarCloud integrado al pipeline.
- [x] Reportes de cobertura enviados a SonarCloud.
- [x] Quality Gate configurado.
- [x] Quality Gate aprobado en el pipeline 24.
- [x] Pipeline bloqueado si el análisis o el gate fallan.

### Pendiente

- [ ] Recuperar o capturar el estado inicial de SonarCloud.
- [ ] Registrar bugs iniciales y finales.
- [ ] Registrar vulnerabilidades iniciales y finales.
- [ ] Registrar code smells iniciales y finales.
- [ ] Registrar duplicación inicial y final.
- [ ] Registrar deuda técnica inicial y final.
- [ ] Confirmar expresamente que no quedan hallazgos Blocker o Critical.
- [ ] Preparar la tabla comparativa antes y después.
- [ ] Capturar la pantalla final del Quality Gate aprobado.

## E13 Pipeline de integración y despliegue continuo

### Completado

- [x] Build backend y frontend.
- [x] Validación de sintaxis Python.
- [x] Pruebas unitarias y cobertura.
- [x] SonarCloud y verificación de Quality Gate.
- [x] Pruebas Postman mediante Newman.
- [x] Ejecución secuencial mediante dependencias entre jobs.
- [x] Pipeline 24 aprobado en `main` en 2 minutos 35 segundos.
- [x] Acciones actualizadas para usar Node.js 24 de forma nativa.

### Pendiente

- [ ] Sustituir la compuerta simulada por un despliegue real a Azure o conseguir
      aceptación formal para una promoción manual.
- [ ] Configurar el secreto de publicación de Azure App Service si se automatiza
      el backend.
- [ ] Configurar el token de Azure Static Web Apps si se automatiza el frontend.
- [ ] Definir despliegue a QA y producción según rama y ambiente.
- [ ] Verificar la aplicación después del despliegue mediante smoke test.
- [ ] Ejecutar nuevamente el pipeline con las versiones actualizadas del workflow.
- [ ] Capturar el grafo completo del pipeline aprobado.

## E14 Pruebas de carga

### Completado

- [x] Herramienta k6 utilizada.
- [x] Dos endpoints críticos evaluados.
- [x] Rampa de 0 a 50 usuarios virtuales.
- [x] Carga sostenida durante cinco minutos.
- [x] Tiempo promedio registrado: 8582.38 ms.
- [x] Percentil 95 registrado: 29563.64 ms.
- [x] Throughput registrado: 4.934 solicitudes por segundo.
- [x] Tasa de error registrada: 24.66 %.
- [x] Comparación contra requerimientos no funcionales.
- [x] Conclusión documentada: el ambiente F1 no cumple los objetivos.
- [x] Resultados completos conservados localmente.

### Pendiente

- [ ] Capturar el resumen final de k6.
- [ ] Capturar el ambiente Azure utilizado durante la prueba.
- [ ] Incorporar ambas capturas al informe final.

## E15 Video de defensa

### Completado

- [x] Guion y distribución de tiempo preparados.

### Pendiente

- [ ] Grabar un video único de máximo diez minutos.
- [ ] Mostrar en vivo el pipeline completo.
- [ ] Mostrar y explicar el Quality Gate de SonarCloud.
- [ ] Mostrar la colección Postman y el resultado Newman.
- [ ] Mostrar las pruebas unitarias y la cobertura.
- [ ] Mostrar la ejecución o resultados de k6.
- [ ] Explicar por qué el ambiente no cumple E14.
- [ ] Explicar la contribución individual.
- [ ] Publicar el video en YouTube.
- [ ] Colocar el enlace final en el documento de entrega.

## E16 Bitácora individual

### Completado

- [x] Borrador de bitácora creado.
- [x] Actividades principales documentadas.
- [x] Dificultades documentadas.
- [x] Aprendizajes documentados.
- [x] Trabajo pendiente documentado.

### Pendiente

- [ ] Revisar fechas y redacción final.
- [ ] Ajustar el formato al utilizado en Fase 1.
- [ ] Exportar la versión definitiva a DOCX o PDF.
- [ ] Incorporarla al paquete final de entrega.

## Documento y paquete final

### Completado

- [x] Borrador DOCX de E9 a E16 generado.
- [x] Estado general documentado.
- [x] Evidencia de cobertura documentada.
- [x] Bitácora incluida en el borrador.
- [x] Guion del video incluido.

### Pendiente

- [ ] Completar las tablas históricas de cobertura y SonarCloud.
- [ ] Insertar capturas con título, fecha y explicación.
- [ ] Añadir enlaces a PR, pipeline, SonarCloud y video.
- [ ] Revisar visualmente todas las páginas del DOCX.
- [ ] Corregir paginación, tablas y saltos si fuera necesario.
- [ ] Exportar el documento final a PDF.
- [ ] Preparar una carpeta de entrega sin secretos ni archivos temporales.
- [ ] Verificar que todos los enlaces funcionen.

## Orden de cierre recomendado

1. Capturar GitHub, Newman, SonarCloud y k6.
2. Recuperar las líneas base de cobertura y SonarCloud.
3. Resolver la protección de ramas y la revisión individual.
4. Decidir y configurar el despliegue de E13.
5. Ejecutar el pipeline definitivo.
6. Finalizar el documento y la bitácora.
7. Grabar el video usando la ejecución definitiva.
8. Exportar el PDF y verificar el paquete de entrega.

# Bitácora individual de la Fase 2

**Proyecto:** WLMS — Aseguramiento de Calidad de Software  
**Autor:** Enrique Morales  
**Fecha de corte:** 4 de noviembre de 2026

Durante la Fase 2 trabajé de forma individual en la automatización y calidad
interna de WLMS. Definí y documenté el flujo de ramas `feature`, `dev`, `qa` y
`main`; preparé el pipeline de GitHub Actions; incorporé pruebas unitarias para
FastAPI y React; integré cobertura, SonarCloud y el Quality Gate; versioné una
colección Postman de quince solicitudes y configuré su ejecución mediante
Newman. También preparé y ejecuté el escenario de carga con k6 contra Azure,
utilizando dos endpoints críticos, una rampa hasta cincuenta usuarios virtuales
y cinco minutos de carga sostenida.

La suite actual ejecuta treinta y nueve pruebas de backend y tres de frontend. Las
pruebas usan dobles para aislar conexiones PostgreSQL, criptografía, generación
de tokens y solicitudes HTTP. El pipeline de producción asociado al merge
`00c7447` terminó correctamente en dos minutos y treinta y cinco segundos, con
compilación, pruebas unitarias, análisis Sonar, Quality Gate, pruebas de API y
compuerta de despliegue aprobados.

La principal dificultad fue construir automatización útil sin confundir los
niveles de prueba. Las pruebas unitarias se mantuvieron aisladas, Postman se
reservó para API y k6 para carga. Otra dificultad fue ejecutar cincuenta
usuarios virtuales sobre el plan gratuito F1: el promedio alcanzó 8,582.38 ms,
el percentil 95 alcanzó 29,563.64 ms y la tasa de error fue 24.66 %. El resultado
no cumplió los requerimientos no funcionales, pero permitió identificar y
documentar la limitación de capacidad del ambiente.

Aprendí que un pipeline aprobado no equivale necesariamente a despliegue
continuo: la etapa actual valida la promoción, pero todavía no publica los
artefactos en Azure. También confirmé que una mejora de cobertura debe
compararse contra una línea base verificable y no inferirse sin evidencia. Si
repitiera esta fase, conservaría desde la primera ejecución los reportes
históricos de cobertura y Sonar, configuraría las protecciones de rama antes de
crear los primeros pull requests y automatizaría el despliegue después de
estabilizar las compuertas de calidad.

Como trabajo pendiente quedan la evidencia histórica de cobertura y Sonar, la
decisión docente sobre revisiones externas en un proyecto individual, el
despliegue automático y la grabación del video final de defensa.

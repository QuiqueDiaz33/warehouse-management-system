# Estrategia de pruebas unitarias

## Alcance inicial

La primera base automatizada cubre autenticación JWT, autorización por roles,
configuración CORS, acceso a datos de autenticación, operaciones de artículos y
el cliente HTTP del frontend. Las pruebas de API y los flujos completos se
mantienen separados y se incorporarán mediante Postman/Newman.

## Dobles de prueba

Se usan `Mock` y `monkeypatch` para aislar dependencias que no pertenecen a la
unidad evaluada:

1. **Conexión y cursor PostgreSQL:** las pruebas de los routers sustituyen
   `get_connection`. Así verifican consultas, commits, rollbacks y traducción de
   errores sin modificar PostgreSQL ni depender de la red.
2. **Verificación de contraseñas:** las pruebas del endpoint de login sustituyen
   `verify_password`. El objetivo del router es decidir la respuesta según el
   resultado; el comportamiento criptográfico se prueba por separado en
   `test_auth.py`.
3. **Creación de JWT:** el endpoint de login sustituye `create_token` para
   comprobar exactamente los claims enviados y producir un resultado
   determinista. La firma y expiración real del token también se prueban por
   separado.
4. **Adaptador Axios:** las pruebas del frontend usan un adaptador local que
   devuelve una respuesta sintética. Esto permite inspeccionar el interceptor
   de autenticación sin enviar solicitudes HTTP reales.

Estos dobles convierten fallos externos en resultados repetibles y mantienen
las pruebas en el nivel unitario, en lugar de convertirlas en pruebas de API o
integración.

## Métricas

Los reportes se generan con `pytest-cov` para Python y el proveedor V8 de
Vitest para JavaScript. La comparación de incremento debe hacerse contra la
línea base registrada en E2, enfocándose en los módulos críticos definidos allí.


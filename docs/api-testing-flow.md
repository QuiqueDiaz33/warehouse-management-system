# E11. Pruebas de API: cobertura y flujo de negocio

Colección: `postman/WLMS-Phase2.postman_collection.json` (22 solicitudes, 111 aserciones).
Ejecución: etapa *Postman API tests* del pipeline mediante Newman, con reporte JUnit.

## Tipos de aserción

Cada solicitud valida tres aspectos:

| Aspecto | Cómo se valida |
| --- | --- |
| Código de respuesta | `pm.response.to.have.status(...)`; en recursos protegidos el código esperado depende del rol (200 o 403) |
| Esquema | `pm.response.to.have.jsonSchema(...)` con tipos y campos obligatorios en las 22 solicitudes |
| Contenido | Valores concretos: identidad del backend, token *bearer*, totales de línea, estados `Pending` y `Cancelled`, mensajes de regla de negocio |

Además, a nivel de colección se valida tiempo de respuesta menor a 3 s y tipo `application/json`.

## Flujo de negocio encadenado (compras)

| Paso | Solicitud | Dato que produce | Dato que consume |
| --- | --- | --- | --- |
| 04 | `POST /auth/login` | `accessToken` | credenciales (secretos de GitHub) |
| 05 | `GET /auth/me` | `userId`, `currentRole` | `accessToken` |
| 06 | `GET /items/` | `itemId`, `itemName` | `accessToken` |
| 16 | `POST /suppliers/` | `supplierId`, `supplierName` | nombre único por ejecución |
| 17 | `POST /purchase-orders/` | `poId` (estado `Pending`) | `supplierId`, `userId` |
| 18 | `POST /purchase-orders/lines` | línea 5 × 10 | `poId`, `itemId` |
| 19 | `GET /purchase-orders/{poId}` | verifica proveedor, ítem y total 50 | `poId`, `supplierName`, `itemName` |
| 20 | `POST /purchase-orders/cancel` | estado `Cancelled` | `poId` |
| 21 | `GET /purchase-orders/{poId}` | verifica `Cancelled` | `poId` |
| 22 | `POST /purchase-orders/cancel` | rechazo 400 por regla de negocio | `poId` |

La orden de prueba termina cancelada, por lo que no genera recepciones ni altera
el inventario. Cada ejecución deja un proveedor identificable con prefijo
`QA Newman`.

## Validación local

El 4 de noviembre de 2026 la colección se ejecutó contra el backend FastAPI y el
esquema de `SQL/` cargado en PostgreSQL 16 local: 22 solicitudes, 111
aserciones, 0 fallos.

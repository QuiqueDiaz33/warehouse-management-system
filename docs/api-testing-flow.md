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

## Flujo de negocio encadenado (ventas)

El usuario de pruebas del pipeline tiene rol **Logistics Staff**, por lo que el
flujo cubre el ciclo de vida de una orden de venta, que es el proceso que ese rol
opera en WLMS.

| Paso | Solicitud | Dato que produce | Dato que consume |
| --- | --- | --- | --- |
| 04 | `POST /auth/login` | `accessToken` | credenciales (secretos de GitHub) |
| 05 | `GET /auth/me` | `userId`, `currentRole` | `accessToken` |
| 09 | `GET /customers/` | `customerId`, `customerName` | `accessToken` |
| 16 | `POST /sales-orders/` | `soId` (`Pending`, `Unpaid`) | `customerId`, `userId` |
| 17 | `POST /sales-orders/advance` | estado `Processing` | `soId` |
| 18 | `GET /sales-orders/{soId}` | verifica cliente y estado | `soId`, `customerName` |
| 19 | `POST /sales-orders/cancel` | estado `Cancelled`, reservas liberadas | `soId` |
| 20 | `GET /sales-orders/{soId}` | verifica `Cancelled` | `soId` |
| 21 | `POST /sales-orders/advance` | rechazo 400: no se avanza una orden cancelada | `soId` |
| 22 | `POST /sales-orders/cancel` | rechazo 400: no se cancela dos veces | `soId` |

La orden no lleva líneas, por lo que no reserva ni altera inventario. Cada
ejecución deja una orden de venta cancelada.

## Hallazgo detectado durante el diseño del flujo

`POST /sales-orders/lines` responde **HTTP 500** con cualquier cuerpo. El modelo
`SOLineCreate` (`backend/schemas/sales_orders.py`) solo declara `so_id` y
`created_by`, mientras que el router usa `line.item_id`, `line.quantity` y
`line.unit_price`, lo que produce
`AttributeError: 'SOLineCreate' object has no attribute 'item_id'`.
Por eso el flujo no agrega líneas de venta.

**Estado: corregido.** El hallazgo se registró en la revisión del PR #15 y se
corrigió en un PR separado: `SOLineCreate` ahora declara `so_id`, `item_id`,
`quantity` (> 0) y `unit_price` (>= 0). Con datos válidos el endpoint responde
200 y reserva stock; con campos faltantes o inválidos responde 422 en lugar
de 500. Las pruebas están en `tests/backend/test_sales_order_lines.py`.

## Validación local

El 4 de noviembre de 2026 la colección se ejecutó contra el backend FastAPI y el
esquema de `SQL/` cargado en PostgreSQL 16 local, con un usuario
Logistics Staff y con un usuario Administrator: en ambos casos 22 solicitudes,
111 aserciones y 0 fallos.

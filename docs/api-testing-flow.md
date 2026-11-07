# E11. Pruebas de API: cobertura y flujo de negocio

Colección: `postman/WLMS-Phase2.postman_collection.json` (26 solicitudes, 135 aserciones).
Ejecución: etapa *Postman API tests* del pipeline mediante Newman, con reporte JUnit.

## Tipos de aserción

Cada solicitud valida tres aspectos:

| Aspecto | Cómo se valida |
| --- | --- |
| Código de respuesta | `pm.response.to.have.status(...)`; en recursos protegidos el código esperado depende del rol (200 o 403) |
| Esquema | `pm.response.to.have.jsonSchema(...)` con tipos y campos obligatorios en las 26 solicitudes |
| Contenido | Valores concretos: identidad del backend, token *bearer*, totales de línea, estados `Pending` y `Cancelled`, mensajes de regla de negocio |

Además, a nivel de colección se valida tiempo de respuesta menor a 3 s y tipo `application/json`.

## Flujo de negocio encadenado (ventas)

El usuario de pruebas del pipeline tiene rol Logistics Staff, así que el flujo recorre el ciclo de vida de una orden de venta, que es el proceso que opera ese rol. Cada paso usa datos que dejó el anterior.

| Paso | Solicitud | Qué produce | Qué usa |
| --- | --- | --- | --- |
| 04 | POST /auth/login | token de acceso | credenciales guardadas como secretos de GitHub |
| 05 | GET /auth/me | id y rol del usuario | token |
| 09 | GET /customers/ | cliente para la orden | token |
| 11 | GET /stock/ | un ítem con existencia y sus cantidades iniciales | token |
| 16 | POST /sales-orders/ | orden nueva en Pending y Unpaid | cliente y usuario |
| 17 | POST /sales-orders/lines | línea de 1 unidad a 12.50 y stock reservado | orden e ítem |
| 18 | POST /sales-orders/lines | rechazo 422 por cantidad con 3 decimales | orden |
| 19 | POST /sales-orders/lines | rechazo 422 por campos faltantes | orden |
| 20 | POST /sales-orders/advance | orden en Processing | orden |
| 21 | GET /sales-orders/{id} | verifica cliente, estado, línea y total de 12.50 | orden |
| 22 | POST /sales-orders/cancel | orden en Cancelled y reservas liberadas | orden |
| 23 | GET /stock/ | verifica que el stock vuelve a sus cantidades iniciales | cantidades del paso 11 |
| 24 | GET /sales-orders/{id} | verifica Cancelled | orden |
| 25 | POST /sales-orders/advance | rechazo 400, una orden cancelada no avanza | orden |
| 26 | POST /sales-orders/cancel | rechazo 400, no se cancela dos veces | orden |

La línea reserva una unidad y la cancelación la libera, y el paso 23 comprueba que el inventario termina igual que al inicio. Cada ejecución deja una orden cancelada que se puede identificar por el usuario de CI.

## Hallazgo detectado durante el diseño del flujo

`POST /sales-orders/lines` responde **HTTP 500** con cualquier cuerpo. El modelo
`SOLineCreate` (`backend/schemas/sales_orders.py`) solo declara `so_id` y
`created_by`, mientras que el router usa `line.item_id`, `line.quantity` y
`line.unit_price`, lo que produce
`AttributeError: 'SOLineCreate' object has no attribute 'item_id'`.
Por eso el flujo no agrega líneas de venta.

**Estado: corregido.** El hallazgo se registró en la revisión del PR #15 y se
corrigió en el PR #16:

- `SOLineCreate` declara `so_id`, `item_id`, `quantity` y `unit_price`.
  `quantity` y `unit_price` son `Decimal` con máximo 2 decimales, igual que
  `NUMERIC(12,2)` en la base; `quantity` debe ser > 0 y `unit_price` >= 0.
- La regla `unit_price >= 0` también quedó en la base: `SQL/Tables.sql` la
  incluye para bases nuevas y
  `SQL/migrations/2026-11-06_sales_order_lines_unit_price_check.sql` la agrega
  en bases existentes.
- Con datos válidos el endpoint responde 200 y reserva stock; con campos
  faltantes, valores fuera de rango o más de 2 decimales responde 422 sin
  llegar a la base.
- `tests/backend/test_sales_order_lines.py` prueba el modelo, la función y el
  endpoint por HTTP con `TestClient`.

La corrección llegó a Azure con el primer despliegue automático del 6 de noviembre, y desde entonces el flujo de Newman también agrega una línea de venta y prueba los rechazos 422.

## Validación local

El 4 de noviembre de 2026 la colección se ejecutó contra el backend FastAPI y el
esquema de `SQL/` cargado en PostgreSQL 16 local, con un usuario
Logistics Staff y con un usuario Administrator: en ambos casos 22 solicitudes,
111 aserciones y 0 fallos. El 6 de noviembre, con los pasos de línea de venta,
la misma validación dio 26 solicitudes, 135 aserciones y 0 fallos.

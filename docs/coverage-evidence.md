# E10. Evidencia de pruebas unitarias y cobertura

## Ejecución actual

La medición local del 4 de noviembre de 2026 se realizó con Python 3.13.15,
pytest 8.4.2, pytest-cov 7.0.0 y Vitest 5.1.0.

| Componente | Archivos de prueba | Pruebas aprobadas | Cobertura de líneas |
| --- | ---: | ---: | ---: |
| Backend | 5 | 39 | 54 % |
| Frontend | 1 | 3 | 1.54 % global |
| Total | 6 | 42 | No se combina porque las herramientas usan universos distintos |

El módulo `backend/auth.py`, el router `backend/routers/auth.py` y el router
`backend/routers/items.py` alcanzaron 100 % de cobertura. `backend/main.py`
alcanzó 96 %. En el frontend, `src/api/axios.js` alcanzó 100 % de líneas y
83.33 % de ramas.

## Dobles de prueba

Las pruebas emplean `monkeypatch`, objetos `Mock` y un adaptador sintético de
Axios para aislar PostgreSQL, verificación de contraseñas, creación de JWT y
solicitudes HTTP. La justificación detallada se conserva en
`docs/testing-strategy.md`.

## Comparación con la línea base

La Fase 1 identifica como críticos inventario, recepción, ventas/reserva,
despacho, autenticación/autorización y compras. Sin embargo, el informe de
Fase 1 disponible no registra un porcentaje de cobertura unitaria por módulo;
su sección 2.4 documenta reglas y automatización de datos. Por lo tanto, no se
declara artificialmente un incremento de 20 puntos porcentuales.

Para cerrar el criterio se requiere una de estas evidencias:

1. recuperar el reporte de cobertura usado como línea base en E2; o
2. obtener aceptación docente para usar 0 % como línea base, justificando que
   en Fase 1 no existía una suite unitaria versionada.

## Brecha por módulos críticos

| Módulo crítico | Archivo representativo | Cobertura actual | Estado |
| --- | --- | ---: | --- |
| Autenticación/autorización | `backend/auth.py` | 100 % | Cubierto |
| Inventario | `backend/routers/stock.py` | 100 % | Cubierto |
| Recepción | `backend/routers/grns.py` | 36 % | Parcial |
| Ventas/reserva | `backend/routers/sales_orders.py` | 32 % | Parcial |
| Despacho | `backend/routers/delivery_challans.py` | 32 % | Parcial |
| Compras | `backend/routers/purchase_orders.py` | 35 % | Parcial |

Las 42 pruebas satisfacen el mínimo numérico, pero la siguiente mejora debe
concentrarse en los módulos críticos con cobertura insuficiente.

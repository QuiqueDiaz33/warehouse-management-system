# E10. Evidencia de pruebas unitarias y cobertura

## Ejecución actual

La medición local del 4 de noviembre de 2026 se realizó con Python 3.13.15,
pytest 8.4.2, pytest-cov 7.0.0 y Vitest 5.1.0.

| Componente | Archivos de prueba | Pruebas aprobadas | Cobertura de líneas |
| --- | ---: | ---: | ---: |
| Backend | 6 | 60 | 55 % |
| Frontend | 1 | 3 | 1.54 % global |
| Total | 7 | 63 | No se combina porque las herramientas usan universos distintos |

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
despacho, autenticación/autorización y compras. Su sección 2.4 documenta reglas
y automatización de datos, pero no registra un porcentaje de cobertura de
código. Por eso la línea base se **midió** sobre el último commit anterior a la
Fase 2, en lugar de suponerse.

### Procedimiento reproducible

```bash
git worktree add ../wlms-baseline d8dedde   # último commit previo a Fase 2 (2 nov 2026)
cd ../wlms-baseline
git ls-files | grep -iE "test|spec"        # sin resultados: no existía suite unitaria
SECRET_KEY=x python -m pytest --cov=backend --cov-report=term   # "no tests ran", TOTAL 0 %
```

En ese commit no existe ningún archivo de pruebas ni configuración de
cobertura, y `pytest-cov` reporta 0 % en los 813 statements del backend. Ese
valor es la cobertura real del código en la línea base, no una suposición.

### Incremento por módulo crítico

| Módulo crítico | Archivo | Línea base (`d8dedde`) | Actual (`main`) | Incremento |
| --- | --- | ---: | ---: | ---: |
| Autenticación/autorización | `backend/auth.py` | 0 % | 100 % | +100 pp |
| Autenticación (router) | `backend/routers/auth.py` | 0 % | 100 % | +100 pp |
| Inventario | `backend/routers/stock.py` | 0 % | 100 % | +100 pp |
| Recepción | `backend/routers/grns.py` | 0 % | 36 % | +36 pp |
| Compras | `backend/routers/purchase_orders.py` | 0 % | 35 % | +35 pp |
| Ventas/reserva | `backend/routers/sales_orders.py` | 0 % | 44 % | +44 pp |
| Despacho | `backend/routers/delivery_challans.py` | 0 % | 32 % | +32 pp |

Todos los módulos críticos superan el incremento mínimo de 20 puntos
porcentuales. Como E2 no publicó la cifra en su sección 2.4, se informa al
docente la fuente de la línea base (commit `d8dedde`) para su validación.

-- Agrega en la base la misma regla que valida la API para unit_price (>= 0).
-- Aplicar una vez en las bases ya creadas; Tables.sql ya la incluye para bases nuevas.

-- 1. Verificar que no existan precios negativos (debe devolver 0).
SELECT COUNT(*) AS negative_prices
FROM sales_order_lines
WHERE unit_price < 0;

-- 2. Agregar la restricción si todavía no existe.
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM pg_constraint
        WHERE conname = 'sales_order_lines_unit_price_check'
    ) THEN
        ALTER TABLE sales_order_lines
            ADD CONSTRAINT sales_order_lines_unit_price_check CHECK (unit_price >= 0);
    END IF;
END;
$$;

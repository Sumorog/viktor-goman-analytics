-- Расчёт суммы начислений по договорам за период
-- Справочник тарифов + факт объёмов (обезличенные имена таблиц)

-- Предполагаемые таблицы:
-- contracts(contract_id, counterparty_id, valid_from, valid_to)
-- service_volumes(contract_id, service_code, period_month, qty, area_sqm)
-- tariff_rates(service_code, rate_from, rate_to, price, unit_code)  -- unit: kWh, sqm, place...

WITH volumes AS (
    SELECT
        v.contract_id,
        v.service_code,
        v.period_month,
        COALESCE(v.qty, 0)       AS qty,
        COALESCE(v.area_sqm, 0) AS area_sqm
    FROM service_volumes v
    WHERE v.period_month >= DATE '2024-01-01'
      AND v.period_month <  DATE '2024-04-01'
),
priced AS (
    SELECT
        vol.*,
        r.price,
        r.unit_code,
        CASE r.unit_code
            WHEN 'sqm'   THEN vol.area_sqm * r.price
            WHEN 'kWh'  THEN vol.qty * r.price
            WHEN 'place' THEN vol.qty * r.price
            WHEN 'unit'  THEN vol.qty * r.price
            ELSE vol.qty * r.price
        END AS amount_raw
    FROM volumes vol
    JOIN tariff_rates r
      ON r.service_code = vol.service_code
     AND vol.period_month >= r.rate_from
     AND vol.period_month <  COALESCE(r.rate_to, DATE '9999-12-31')
)
SELECT
    contract_id,
    service_code,
    SUM(amount_raw) AS total_amount,
    COUNT(*)        AS line_count
FROM priced
GROUP BY contract_id, service_code
ORDER BY contract_id, service_code;

-- Пример оконной функции: накопительная сумма по контракту внутри месяца
/*
SELECT
    contract_id,
    period_month,
    SUM(amount_raw) OVER (
        PARTITION BY contract_id, period_month
        ORDER BY service_code
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS running_total
FROM priced;
*/

-- =============================================================================
-- ОЭЗ «Технополис» — расчёт начислений по договорам за период (обезличено)
-- =============================================================================
-- Что считаем: денежную базу для выставления счетов резидентам по фактическим
--   объёмам (площадь, кВт·ч, места и т.д.) с учётом актуальной версии тарифа.
-- Контекст: портфель с выручкой ~5,5 млрд руб.; запросы подобного типа гонялись
--   ежемесячно перед закрытием периода в тарифном планировании.
-- =============================================================================

-- Предполагаемые таблицы (см. oas_table_glossary.md):
--   contracts, service_volumes, tariff_rates

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
-- Здесь JOIN к tariff_rates: без него нет цены и единицы измерения.
-- Условие по датам rate_from/rate_to — чтобы не подтянуть устаревший тариф
--   после пересмотра прейскуранта Департамента.
priced AS (
    SELECT
        vol.*,
        r.price,
        r.unit_code,
        CASE r.unit_code
            WHEN 'sqm'    THEN vol.area_sqm * r.price
            WHEN 'kWh'   THEN vol.qty * r.price
            WHEN 'place' THEN vol.qty * r.price
            WHEN 'unit'  THEN vol.qty * r.price
            ELSE vol.qty * r.price
        END AS amount_raw
    FROM volumes vol
    INNER JOIN tariff_rates r
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

-- =============================================================================
-- ОЭЗ — выручка (начисления) по сегменту резидента и виду услуги за месяц
-- =============================================================================
-- Зачем JOIN residents: в отчёте CFO нужна не только «выручка по услуге»,
--   но и вклад крупных vs малых резидентов — сегмент хранится в карточке.
-- Зачем JOIN contracts: service_volumes ссылается на contract_id; из договора
--   берём resident_id для связи с сегментом.
-- Что считаем: SUM(amount) после применения тарифа — аналог проведённых
--   начислений до разнесения по БУ.
-- =============================================================================

SELECT
    res.segment_code,
    vol.service_code,
    DATE_TRUNC('month', vol.period_month)::date AS period_month,
    COUNT(DISTINCT vol.contract_id)            AS contracts_cnt,
    SUM(
        CASE tr.unit_code
            WHEN 'sqm'    THEN vol.area_sqm * tr.price
            WHEN 'kWh'   THEN vol.qty * tr.price
            WHEN 'place' THEN vol.qty * tr.price
            WHEN 'unit'  THEN vol.qty * tr.price
            ELSE vol.qty * tr.price
        END
    ) AS revenue_amount
FROM service_volumes vol
-- JOIN contracts: получаем владельца договора (резидента) для сегментации.
INNER JOIN contracts c
    ON c.contract_id = vol.contract_id
   AND vol.period_month BETWEEN c.valid_from AND COALESCE(c.valid_to, DATE '9999-12-31')
-- JOIN residents: сегмент резидента (LARGE / MID / SMALL — коды обезличены).
INNER JOIN residents res
    ON res.resident_id = c.resident_id
-- JOIN tariff_rates: цена на дату периода (см. tariff_calculation.sql).
INNER JOIN tariff_rates tr
    ON tr.service_code = vol.service_code
   AND vol.period_month >= tr.rate_from
   AND vol.period_month <  COALESCE(tr.rate_to, DATE '9999-12-31')
WHERE vol.period_month = DATE '2024-03-01'
GROUP BY res.segment_code, vol.service_code, DATE_TRUNC('month', vol.period_month)
ORDER BY res.segment_code, revenue_amount DESC;

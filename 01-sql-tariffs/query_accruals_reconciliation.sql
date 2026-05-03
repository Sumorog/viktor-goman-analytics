-- =============================================================================
-- ОЭЗ — сверка: «наша» модель начислений vs стейджинг выгрузки из 1С
-- =============================================================================
-- Зачем JOIN между accruals_fact и accruals_1c_staging: найти расхождения
--   по сумме на уровне (contract, service, месяц) до проводок в бухгалтерии.
-- Что считаем: дельту сумм и список аномальных документов для разбора
--   аналитиком тарифов и интегратором 1С.
-- Примечание: в бою добавлялись фильтры по юрлицу и валюте; здесь упрощено.
-- =============================================================================

WITH our_side AS (
    SELECT
        f.contract_id,
        f.service_code,
        f.period_month,
        SUM(f.amount) AS amount_warehouse
    FROM accruals_fact f
    WHERE f.period_month = DATE '2024-03-01'
    GROUP BY f.contract_id, f.service_code, f.period_month
),
onec_side AS (
    SELECT
        s.contract_id,
        s.service_code,
        s.period_month,
        SUM(s.amount) AS amount_1c
    FROM accruals_1c_staging s
    WHERE s.period_month = DATE '2024-03-01'
    GROUP BY s.contract_id, s.service_code, s.period_month
)
SELECT
    COALESCE(o.contract_id, k.contract_id)     AS contract_id,
    COALESCE(o.service_code, k.service_code)   AS service_code,
    COALESCE(o.period_month, k.period_month)   AS period_month,
    COALESCE(o.amount_warehouse, 0)            AS amount_warehouse,
    COALESCE(k.amount_1c, 0)                   AS amount_1c,
    COALESCE(o.amount_warehouse, 0) - COALESCE(k.amount_1c, 0) AS delta_amount
FROM our_side o
-- FULL OUTER JOIN: важно пойти и «лишние» строки 1С, и пропуски в нашей модели.
FULL OUTER JOIN onec_side k
    ON o.contract_id = k.contract_id
   AND o.service_code = k.service_code
   AND o.period_month = k.period_month
WHERE ABS(COALESCE(o.amount_warehouse, 0) - COALESCE(k.amount_1c, 0)) > 0.01
ORDER BY ABS(COALESCE(o.amount_warehouse, 0) - COALESCE(k.amount_1c, 0)) DESC;

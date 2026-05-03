-- =============================================================================
-- Практика: собственные решения (обезличено), не из учебников
-- Контекст: финансы ОЭЗ / дебиторка / сверки — см. также 01-sql-tariffs, 06-debt-analysis
-- =============================================================================

-- -----------------------------------------------------------------------------
-- Задача A: дебиторка с просрочкой по когортам «месяц возникновения долга»
-- Зачем: CFO хотел видеть не только корзину 0-30-90+, но и «когда долг завис»,
--   чтобы таргетировать работу с контрагентами и шаблоны уведомлений.
-- Идея: первая дата просрочки по контракту → когорта; далее снимок задолженности
--   на отчётную дату в разрезе когорты и текущей глубины просрочки.
-- -----------------------------------------------------------------------------

WITH first_overdue AS (
    SELECT
        contract_id,
        DATE_TRUNC('month', MIN(day)) AS cohort_month
    FROM debt_balance_daily
    WHERE overdue_days > 0
    GROUP BY contract_id
),
snapshot AS (
    SELECT
        d.contract_id,
        fo.cohort_month,
        d.overdue_days,
        d.amount_outstanding
    FROM debt_balance_daily d
    JOIN first_overdue fo ON fo.contract_id = d.contract_id
    WHERE d.snapshot_date = DATE '2024-03-31'
)
SELECT
    cohort_month,
    CASE
        WHEN overdue_days <= 30 THEN '1-30'
        WHEN overdue_days <= 90 THEN '31-90'
        ELSE '90+'
    END AS delay_bucket,
    COUNT(*) AS contracts_cnt,
    SUM(amount_outstanding) AS amount_rub
FROM snapshot
GROUP BY 1, 2
ORDER BY 1, 2;


-- -----------------------------------------------------------------------------
-- Задача B: скользящая выручка по резиденту (аномалии перед закрытием месяца)
-- Зачем: выявить резидентов, у кого объём услуг «подпрыгнул» относительно
--   собственного среднего — до финальной выгрузки в 1С.
-- -----------------------------------------------------------------------------

WITH daily AS (
    SELECT
        resident_id,
        bill_date,
        SUM(amount) AS daily_amount
    FROM billing_lines
    WHERE bill_date >= CURRENT_DATE - INTERVAL '180 days'
    GROUP BY resident_id, bill_date
),
rolled AS (
    SELECT
        resident_id,
        bill_date,
        daily_amount,
        AVG(daily_amount) OVER (
            PARTITION BY resident_id
            ORDER BY bill_date
            ROWS BETWEEN 27 PRECEDING AND CURRENT ROW
        ) AS avg28,
        STDDEV_POP(daily_amount) OVER (
            PARTITION BY resident_id
            ORDER BY bill_date
            ROWS BETWEEN 27 PRECEDING AND CURRENT ROW
        ) AS sd28
    FROM daily
)
SELECT
    resident_id,
    bill_date,
    daily_amount,
    avg28,
    CASE
        WHEN sd28 IS NULL OR sd28 = 0 THEN NULL
        ELSE (daily_amount - avg28) / sd28
    END AS zscore_28d
FROM rolled
WHERE daily_amount > avg28 + 3 * COALESCE(sd28, 0)
ORDER BY zscore_28d DESC NULLS LAST;


-- -----------------------------------------------------------------------------
-- Задача C: дедупликация строк выгрузки 1С (оставить последнюю версию документа)
-- Зачем: интеграция шлёт повторы с тем же external_doc_id; в витрину должна
--   попасть одна строка на документ.
-- -----------------------------------------------------------------------------

WITH ranked AS (
    SELECT
        external_doc_id,
        contract_id,
        amount,
        loaded_at,
        ROW_NUMBER() OVER (
            PARTITION BY external_doc_id
            ORDER BY loaded_at DESC
        ) AS rn
    FROM accruals_1c_staging
)
SELECT external_doc_id, contract_id, amount, loaded_at
FROM ranked
WHERE rn = 1;

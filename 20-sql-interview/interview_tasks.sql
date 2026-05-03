-- Задачи с собеседований + решения
-- Уровень: middle аналитик

-- === ЗАДАЧА 1: Скользящее среднее ===
-- Есть таблица sales (date, amount). Нужно 7-дневное скользящее среднее.

-- Моё решение:
SELECT 
    date,
    amount,
    AVG(amount) OVER (
        ORDER BY date 
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) as moving_avg_7d
FROM sales
ORDER BY date;

-- Альтернатива (если пропуски в датах):
-- TODO: сделать через generate_series, но тяжело читается


-- === ЗАДАЧА 2: Процент от общего ===
-- Категории и их доля в выручке

SELECT 
    category,
    SUM(amount) as total,
    ROUND(
        SUM(amount) * 100.0 / SUM(SUM(amount)) OVER (), 
        2
    ) as pct_of_total
FROM sales
GROUP BY category;

-- Примечание: 100.0 чтобы не было integer division! Ловил баг.


-- === ЗАДАЧА 3: Первый и последний заказ клиента ===
-- retention аналитика

WITH ranked AS (
    SELECT 
        customer_id,
        order_date,
        amount,
        ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date) as rn_asc,
        ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date DESC) as rn_desc
    FROM orders
)
SELECT 
    customer_id,
    MAX(CASE WHEN rn_asc = 1 THEN order_date END) as first_order,
    MAX(CASE WHEN rn_desc = 1 THEN order_date END) as last_order,
    MAX(CASE WHEN rn_asc = 1 THEN amount END) as first_amount,
    MAX(CASE WHEN rn_desc = 1 THEN amount END) as last_amount
FROM ranked
WHERE rn_asc = 1 OR rn_desc = 1
GROUP BY customer_id;

-- TODO: проверить на клиентах с 1 заказом — дублируются?


-- === ЗАДАЧА 4: Месячная когорта ===
-- Cohort analysis: когда клиент пришёл, когда вернулся

WITH first_orders AS (
    SELECT 
        customer_id,
        DATE_TRUNC('month', MIN(order_date)) as cohort_month
    FROM orders
    GROUP BY customer_id
)
SELECT 
    fo.cohort_month,
    DATE_TRUNC('month', o.order_date) as order_month,
    COUNT(DISTINCT o.customer_id) as active_users,
    COUNT(DISTINCT o.customer_id) * 100.0 / COUNT(DISTINCT fo.customer_id) as retention_pct
FROM first_orders fo
JOIN orders o ON fo.customer_id = o.customer_id
GROUP BY 1, 2
ORDER BY 1, 2;

-- NOTE: на больших данных тормозит, нужны индексы по customer_id + order_date


-- === ЗАДАЧА 5: Найти дубликаты ===
-- Проверка качества данных

SELECT 
    contract_id,
    service_type,
    COUNT(*) as cnt
FROM billings
GROUP BY contract_id, service_type
HAVING COUNT(*) > 1;

-- Как чинить: оставить MAX(date) или суммировать — зависит от бизнес-логики
-- TODO: добавить пример чистки
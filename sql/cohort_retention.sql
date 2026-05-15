-- Когортный анализ: первая покупка клиента, месяцы удержания
WITH first_orders AS (
    SELECT c.customer_unique_id,
           MIN(o.order_purchase_timestamp) AS first_purchase
    FROM orders o
    JOIN customers c ON o.customer_id = c.customer_id
    WHERE o.order_status = 'delivered'
    GROUP BY c.customer_unique_id
),
cohort_data AS (
    SELECT 
        DATE_TRUNC('month', fo.first_purchase) AS cohort_month,
        DATE_TRUNC('month', o.order_purchase_timestamp) AS order_month,
        EXTRACT(YEAR FROM o.order_purchase_timestamp)*12 + EXTRACT(MONTH FROM o.order_purchase_timestamp) -
        (EXTRACT(YEAR FROM fo.first_purchase)*12 + EXTRACT(MONTH FROM fo.first_purchase)) AS month_number,
        c.customer_unique_id
    FROM orders o
    JOIN customers c ON o.customer_id = c.customer_id
    JOIN first_orders fo ON c.customer_unique_id = fo.customer_unique_id
    WHERE o.order_status = 'delivered'
)
SELECT cohort_month, month_number, COUNT(DISTINCT customer_unique_id) AS customers
FROM cohort_data
GROUP BY cohort_month, month_number
ORDER BY cohort_month, month_number;

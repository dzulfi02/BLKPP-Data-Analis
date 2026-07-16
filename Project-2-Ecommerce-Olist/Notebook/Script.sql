select * from public.customers c
select * from public.order_items oi
select * from public.order_payments op
select * from public.order_reviews r
select * from public.orders o
select * from public.products p
select * from public.sellers s 

--Average Review Berdasarkan Status Order
select
o.order_status,
round(avg(r.review_score), 2) as avg_review
from orders o 
join order_reviews r
on o.order_id = r.order_id
join customers c
on o.customer_id = c.customer_id
group by o.order_status
order by avg_review desc

--Status pengiriman berdasarkan rata - rata review 
SELECT
    CASE
        WHEN DATE(o.order_delivered_customer_date)
             < DATE(o.order_estimated_delivery_date)
            THEN 'Kecepetan'
        WHEN DATE(o.order_delivered_customer_date)
             = DATE(o.order_estimated_delivery_date)
            THEN 'Tepat Waktu'
        WHEN DATE(o.order_delivered_customer_date)
             > DATE(o.order_estimated_delivery_date)
            THEN 'Terlambat'
        ELSE 'Belum Dikirim'
    END AS status_pengiriman,
    round(cast(AVG(r.review_score)as numeric),1) 
    AS average_review,
    COUNT(o.order_id) AS total_order
FROM orders o
JOIN order_reviews r
    ON o.order_id = r.order_id
GROUP BY status_pengiriman
ORDER BY average_review DESC;

--Kota Customer dengan Jumlah Order Terbanyak
select c.customer_city,
count (o.order_id) as total_order
from public.orders o
join customers c
on o.customer_id = c.customer_id
group by c.customer_city
order by total_order desc
limit 10;

--Top Product Category Berdasarkan Revenue
select p.product_category_name,
round(cast(sum (op.payment_value)as numeric),2) 
as total_reveneu
from products p
join order_items oi
on p.product_id = oi.product_id
join order_payments op 
on oi.order_id = op.order_id
group by p.product_category_name 
order by total_reveneu desc
limit 10;


--Metode Pembayaran Paling Banyak Digunakan
select
op.payment_type,
count(o.order_id) as total_transaction
from orders o
join order_payments op
on o.order_id = op.order_id
join customers c
on o.customer_id = c.customer_id
group by op.payment_type
order by total_transaction desc;

--Seller dengan Revenue Tertinggi
select
s.seller_city,
ROUND(CAST(SUM(op.payment_value) AS NUMERIC), 2) 
AS total_revenue
from sellers s
join order_items oi
on oi.seller_id = s.seller_id
join order_payments op 
on oi.order_id = op.order_id
group by s.seller_city
order by total_revenue desc
limit 10;

--Kategori Produk yang Paling Banyak Terjual
select
p.product_category_name,
count(oi.product_id) as total_product_sold
from order_items oi
join products p
on oi.product_id = p.product_id
group by p.product_category_name
order by total_product_sold desc
limit 10;

--Revenue Berdasarkan State Customer
select
c.customer_state,
ROUND(CAST(SUM(op.payment_value) AS NUMERIC), 2) 
AS total_revenue
from orders o 
join customers c
on o.customer_id = c.customer_id
join order_payments op
on o.order_id = op.order_id
group by c.customer_state
order by total_revenue desc;

--Total order berdasarkan bulan
SELECT
    DATE_TRUNC(
        'month',
        CAST(o.order_purchase_timestamp 
        AS TIMESTAMP)
    ) AS bulan,
    COUNT(o.order_id) AS total_order
FROM orders o
JOIN customers c
    ON o.customer_id = c.customer_id
GROUP BY bulan
ORDER BY bulan DESC;

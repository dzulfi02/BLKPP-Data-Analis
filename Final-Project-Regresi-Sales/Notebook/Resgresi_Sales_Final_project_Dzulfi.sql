--1 Tren Penjualan Pertahun
select 
"year" as tahun,
count(distinct "Customers_id") as pelanggan,
sum("Sales") as penjualan
from regresi
group by "year";

--2 Tren Jumlah Pelanggan Pertahun
select 
"year" as tahun,
count(distinct "Customers_id") as pelanggan,
sum("Sales") as penjualan
from regresi
group by "year";

--3 Tren Penjualan Perbulan
SELECT
    DATE_TRUNC('month', "Date") AS bulan,
    SUM("Sales") AS total_sales
FROM regresi
GROUP BY DATE_TRUNC('month', "Date")
ORDER BY bulan;

--4 Tren Jumlah Pelanggan Perbulan
SELECT
    DATE_TRUNC('month', "Date") AS bulan,
	count(distinct"Customers_id") as pelanggan
FROM regresi
GROUP BY DATE_TRUNC('month', "Date")
ORDER BY bulan;

--5 Sales berdasarkan Dayofweek + promo
-- a berdasarkan penjualan
SELECT
       CASE
        WHEN "DayOfWeek" = 1 THEN 'Senin'
        WHEN "DayOfWeek" = 2 THEN 'Selasa'
        WHEN "DayOfWeek" = 3 THEN 'Rabu'
        WHEN "DayOfWeek" = 4 THEN 'Kamis'
        WHEN "DayOfWeek" = 5 THEN 'Jumat'
        WHEN "DayOfWeek" = 6 THEN 'Sabtu'
        WHEN "DayOfWeek" = 7 THEN 'Minggu'
    END AS day_name,
    AVG(CASE WHEN "Promo" = 0 THEN "Sales" END) AS no_promo,
    AVG(CASE WHEN "Promo" = 1 THEN "Sales" END) AS promo
FROM regresi
WHERE "Open" = 1
GROUP BY "DayOfWeek"
ORDER BY "DayOfWeek";

--b berdasarkan pelanggan
SELECT 
    CASE 
        WHEN "DayOfWeek" = 1 THEN '1 - Senin'
        WHEN "DayOfWeek" = 2 THEN '2 - Selasa'
        WHEN "DayOfWeek" = 3 THEN '3 - Rabu'
        WHEN "DayOfWeek" = 4 THEN '4 - Kamis'
        WHEN "DayOfWeek" = 5 THEN '5 - Jumat'
        WHEN "DayOfWeek" = 6 THEN '6 - Sabtu'
        WHEN "DayOfWeek" = 7 THEN '7 - Minggu'
    END AS "Hari",
    AVG("Customers_id") AS "Rata_Rata_Pelanggan"
FROM regresi
WHERE "Open" = 1
GROUP BY "DayOfWeek"
ORDER BY "DayOfWeek" ASC;

--c tren penjualan perhari
SELECT
    CASE
        WHEN "DayOfWeek" = 1 THEN 'Senin'
        WHEN "DayOfWeek" = 2 THEN 'Selasa'
        WHEN "DayOfWeek" = 3 THEN 'Rabu'
        WHEN "DayOfWeek" = 4 THEN 'Kamis'
        WHEN "DayOfWeek" = 5 THEN 'Jumat'
        WHEN "DayOfWeek" = 6 THEN 'Sabtu'
        WHEN "DayOfWeek" = 7 THEN 'Minggu'
    END AS nama_hari,
    AvG("Sales") AS total_sales
FROM regresi
GROUP BY "DayOfWeek"
ORDER BY total_sales DESC;

--6 Perbandingan Penjualan saat weekend
SELECT 
    CASE
        WHEN is_weekend = 1 THEN 'Weekend'
        WHEN is_weekend = 0 THEN 'Weekday'
    END AS status_promo,

    SUM("Sales") AS total_sales,
    AVG("Sales") AS avg_sales,
    AVG("Customers_id") AS avg_customer

FROM regresi
GROUP BY is_weekend;

--7 Perbandingan Penjualan saat harbolnas
SELECT 
    CASE
        WHEN event_harbolnas = 1 THEN 'Event Harbolnas'
        WHEN event_harbolnas = 0 THEN 'Bukan Harbolnas'
    END AS status_promo,

    SUM("Sales") AS total_sales,
    AVG("Sales") AS avg_sales,
    AVG("Customers_id") AS avg_customer

FROM regresi
GROUP BY event_harbolnas;

--8 Perbandingan Penjualan saat weekeend
SELECT 
    CASE
        WHEN is_weekend = 1 THEN 'Weekend'
        WHEN is_weekend = 0 THEN 'Weekday'
    END AS status_promo,

    SUM("Sales") AS total_sales,
    AVG("Sales") AS avg_sales,
    AVG("Customers_id") AS avg_customer

FROM regresi
GROUP BY is_weekend;

--9 Perbandingan penjualan saat promo
SELECT 
    CASE
        WHEN "Promo" = 1 THEN 'Promo'
        WHEN "Promo" = 0 THEN 'Tidak Promo'
    END AS status_promo,

    SUM("Sales") AS total_sales,
    AVG("Sales") AS avg_sales,
    AVG("Customers_id") AS avg_customer

FROM regresi
GROUP BY "Promo";

--10 Perbandingan Penjualan saat schoolholiday 
SELECT 
    CASE
        WHEN "SchoolHoliday" = 1 THEN 'Libur Sekolah'
        WHEN "SchoolHoliday" = 0 THEN 'Bukan Libur Sekolah'
    END AS status_promo,

    SUM("Sales") AS total_sales,
    AVG("Sales") AS avg_sales,
    AVG("Customers_id") AS avg_customer

FROM regresi
GROUP BY "SchoolHoliday";

--11 Perbandingan Penjualan saat Payday
SELECT 
    CASE
        WHEN is_payday_period = 1 THEN 'Hari Gajian'
        WHEN is_payday_period = 0 THEN 'Bukan Hari Gajian'
    END AS status_promo,

    SUM("Sales") AS total_sales,
    AVG("Sales") AS avg_sales,
    AVG("Customers_id") AS avg_customer

FROM regresi
GROUP BY is_payday_period;

--12 Store Ineficiency
--a berdasarkan sales
SELECT 
    "Store" As store_id,
    AVG("Customers_id") AS avg_customers,
    AVG("Sales") AS avg_sales
FROM regresi
GROUP BY "Store"
ORDER BY avg_sales DESC
limit 5;

--b berdasarkan pelanggan
SELECT 
    "Store" As store_id,
    AVG("Customers_id") AS avg_customers,
    AVG("Sales") AS avg_sales
FROM regresi
GROUP BY "Store"
ORDER BY avg_customers DESC
limit 5;

--c Korelasi efisiensi store
select 
store_avg_customer,
store_avg_sales
from regresi

-- weak positive correlation (korelasi positif lemah) -> semakin banyak customer, sales cenderung naik, tapi tidak selalu konsisten

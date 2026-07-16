
select * from public.online_retail t 

--INSIGHT
--Keterkaitan antar jumlah transaksi per negara
SELECT "Country",COUNT(*) AS Total_Count
FROM public.online_retail t  
GROUP BY "Country"
ORDER BY Total_Count DESC;

--Banyaknya produk yang terjual
select "StockCode","Description",SUM("Quantity") AS Total_Quantity
FROM public.online_retail t 
GROUP BY "StockCode","Description"
ORDER BY Total_Quantity DESC;

--Jumlah nominal pembelian per-negara
SELECT "Country",SUM("TotalPrice") AS Total_Revenue
FROM public.online_retail t 
GROUP BY "Country"
ORDER BY Total_Revenue DESC;

--Customer yang sering melakukan transaksi pembelian
SELECT "CustomerID","Country",SUM("TotalPrice") AS Total_Spent
FROM public.online_retail t  
GROUP BY "CustomerID","Country"
ORDER BY Total_Spent DESC;

--Melihat penjualan perhari
SELECT "InvoiceDate", SUM("Quantity") AS Total_Quantity
FROM public.online_retail t 
GROUP BY "InvoiceDate"
ORDER BY Total_Quantity DESC;

--Menghitung total transaksi yang berhasil dan dibatalkan
SELECT "Transaction_Status", COUNT(*) AS Total_Count
FROM public.online_retail t
GROUP BY "Transaction_Status"
ORDER BY Total_Count DESC;

--Produk yang sering dibatalkan transaksinya
SELECT "Description",
    SUM(CASE WHEN "Transaction_Status" = 'true' THEN 1 ELSE 0 END) AS Total_Gagal_Transactions
FROM public.online_retail t  
GROUP BY "Description"
ORDER BY Total_Gagal_Transactions DESC;

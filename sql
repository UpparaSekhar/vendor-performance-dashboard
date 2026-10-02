-- Total number of orders
SELECT COUNT(*) AS total_orders
FROM vendor_data;


-- Total purchase amount
SELECT SUM(Purchase_Amount) AS total_purchase_amount
FROM vendor_data;


-- Vendor performance
SELECT
    Vendor,
    COUNT(Order_ID) AS Orders,
    SUM(Purchase_Amount) AS Purchase_Amount,
    SUM(Quantity) AS Quantity,
    SUM(Defects) AS Defects
FROM vendor_data
GROUP BY Vendor;
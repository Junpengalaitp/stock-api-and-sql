-- Find all customers in Berlin (assuming Berlin, Germany)
SELECT CustomerID
,CustomerName
,ContactName
,Address
,City
,PostalCode
,Country
FROM Customers
WHERE Country = 'Germany'
AND City = 'Berlin';

-- Find all customers in Mexico City (assuming Mexico City, Mexico)
SELECT CustomerID
,CustomerName
,ContactName
,Address
,City
,PostalCode
,Country
FROM Customers
WHERE Country = 'Mexico'
AND City = 'Mexico City';

-- Find avg price of all products
SELECT AVG(Price) FROM Products;

-- Find number of products that Have price = 18
SELECT COUNT(ProductId)
FROM Products
WHERE Price = 18;

-- Find orders between 1996-08-01 and 1996-09-06
SELECT OrderID
,CustomerID
,EmployeeID,
OrderDate,
ShipperID
FROM Orders
WHERE OrderDate >= '1996-08-01'
AND OrderDate <= '1996-09-06';

-- Find customers with more than 3 orders
SELECT Customers.CustomerID
,CustomerName
,ContactName
,Address
,City
,PostalCode
,Country
FROM Customers
JOIN
(SELECT CustomerID, Count(OrderId)
FROM Orders
GROUP BY CustomerID
HAVING Count(OrderId) > 3) order3
ON Customers.CustomerID = order3.CustomerID;

-- Find all customers that are from the same city (I think this question is not very clear)
SELECT CustomerID
,CustomerName
,ContactName
,Address
,b.City
,PostalCode
,b.Country
FROM
(SELECT DISTINCT Country
,City
FROM Customers) a
LEFT JOIN Customers b
ON a.Country = b.Country
AND a.City = b.City

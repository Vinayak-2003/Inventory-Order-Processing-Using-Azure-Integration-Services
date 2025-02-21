CREATE TABLE dbo.order_details(
    [OrderID] UNIQUEIDENTIFIER PRIMARY KEY,
    [CustomerName] VARCHAR(100) NOT NULL,
    [OrderDate] DATETIME DEFAULT GETDATE(),
    [Product] VARCHAR(100),
    [TotalQuantity] INT NOT NULL,
    [Contact] VARCHAR(12) NOT NULL,
    [Email] VARCHAR(150) NOT NULL,
    [Address] VARCHAR(500) NOT NULL,
    [City] VARCHAR(50) NOT NULL,
    [TotalAmount] DECIMAL(10,2) NOT NULL,
    [PaymentMode] VARCHAR(20) NOT NULL
);

INSERT INTO dbo.order_details 
(OrderID, CustomerName, Product, TotalQuantity, Contact, Email, Address, City, PaymentMode)
VALUES (NEWID(), 'vinayak', 1, 1, '8078690336', 'vinayakkanchan03@gmail.com', '14, 25th floor, DLF', 'Gurgaon', 'Card');

{
    "customer_name": "vinayak",
    "product": "bottle",
    "total_quantity": 2,
    "contact": "9376837383",
    "email": "vinayak02@gmail.com",
    "address": "21, palm street",
    "city": "hyderabad",
    "payment_mode": "cash"
}

CREATE TABLE dbo.inventory_details(
    [ItemID] UNIQUEIDENTIFIER PRIMARY KEY,
    [ItemName] VARCHAR(50) NOT NULL,
    [ItemDescription] VARCHAR(100) NOT NULL,
    [AvailableQuantity] INT NOT NULL,
    [Price] DECIMAL(6,2) NOT NULL,
    [TotalCost] DECIMAL (10,2) NOT NULL,
    [Vendor] VARCHAR(50) NOT NULL,
    [VendorContact] VARCHAR(12) NOT NULL,
    [InsertedDatetime] DATETIME DEFAULT GETDATE(),
    [LastUpdatedDatetime] DATETIME DEFAULT GETDATE()
);

INSERT INTO dbo.inventory_details
(ItemID, ItemName, ItemDescription, AvailableQuantity, Price, TotalCost, Vendor, VendorContact)
VALUES (NEWID(), "bottle", "drinking water for hot and cold water", 12, 100, 1200, "cello", "983638361873")

{
    "item_id": "cuuiwwue89dw",
    "item_name": "bottle",
    "item_description": "drinking water for hot and cold water",
    "quantity": 12,
    "price": 100,
    "total_cost": 1200,
    "vendor": "cello",
    "vendor_contact": "9792773633"
}

SELECT AvailableQuantity FROM dbo.inventory_details WHERE ItemName = "";

SELECT AvailableQuantity, Price, TotalCost FROM dbo.inventory_details WHERE ItemName = "";

UPDATE TABLE dbo.inventory_details SET AvailableQuantity = (?), Price = (?), TotalCost = (?) WHERE ItemName = (?);

{
    "item_name": "bottle",
    "quantity": 12,
    "price": 100,
    "total_cost": 1200
}

DELETE FROM dbo.inventory_details WHERE ItemName = "";

{
    "item_name": "bottle"
}
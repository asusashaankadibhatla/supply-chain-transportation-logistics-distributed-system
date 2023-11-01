-- Suppliers table
CREATE TABLE Suppliers (
    SupplierID SERIAL PRIMARY KEY,
    SupplierName VARCHAR(255) NOT NULL,
    ContactInfo VARCHAR(255),
    SupplierStatus VARCHAR(50),
    PerformanceRating INT,
    LastReviewDate DATE,
    ContractStartDate DATE, -- fragment based on monthly partitions
    ContractEndDate DATE
);

-- Customers table
CREATE TABLE Customers (
    CustomerID SERIAL PRIMARY KEY,
    CustomerName VARCHAR(255) NOT NULL,
    ContactInfo VARCHAR(255),
    CustomerStatus VARCHAR(50),
    JoinDate DATE, -- fragment based on monthly partitions
    LastPurchaseDate DATE
);

-- Carriers table
CREATE TABLE Carriers (
    CarrierID SERIAL PRIMARY KEY,
    CarrierName VARCHAR(255) NOT NULL,
    ContactInfo VARCHAR(255),
    CarrierStatus VARCHAR(50),
    StartDate DATE, -- fragment based on monthly partitions
    EndDate DATE
);

-- Product Inventory table
CREATE TABLE ProductInventory (
    ProductID SERIAL PRIMARY KEY,
    ProductName VARCHAR(255) NOT NULL,
    QuantityOnHand INT NOT NULL,
    SupplierID INT,
    WarehouseLocation VARCHAR(255), -- fragment based on daily partitions
    LifecycleStatus VARCHAR(50),
    IsActive BOOLEAN,
    StartDate DATE, -- fragment based on daily partitions
    EndDate DATE,
    FOREIGN KEY (SupplierID) REFERENCES Suppliers(SupplierID)
);

-- Orders table
CREATE TABLE Orders (
    OrderID SERIAL PRIMARY KEY,
    CustomerID INT,
    OrderDate DATE NOT NULL,
    EstimatedDeliveryDate DATE,
    DeliveryDate DATE,
    OrderStatus VARCHAR(50),
    IsActive BOOLEAN,
    CreationDate DATE, -- fragment based on daily partitions
    CompletionDate DATE,
    ReturnDate DATE
    FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID)
);

-- Order Details table
CREATE TABLE OrderDetails (
    OrderDetailID SERIAL PRIMARY KEY,
    OrderID INT,
    ProductID INT,
    EstimatedDeliveryDate DATE,
    DeliveryDate DATE
    QuantityOrdered INT NOT NULL,
    PricePerUnit DECIMAL(10,2),
    ItemStatus VARCHAR(50),  
    ReturnDate DATE,
    FOREIGN KEY (OrderID) REFERENCES Orders(OrderID),
    FOREIGN KEY (ProductID) REFERENCES ProductInventory(ProductID)
);

-- Transportation table
CREATE TABLE Transportation (
    ShipmentID SERIAL PRIMARY KEY,
    CarrierID INT,
    DepartureDate DATE NOT NULL,
    ArrivalDate DATE,
    Route VARCHAR(255), -- fragments
    ShipmentStatus VARCHAR(50),
    IsActive BOOLEAN,
    CurrentLocation VARCHAR(255),
    LastUpdateTimestamp TIMESTAMP,
    ScheduledPickupDate DATE,
    ActualPickupDate DATE,
    FOREIGN KEY (CarrierID) REFERENCES Carriers(CarrierID)
);

-- Product Movements table
CREATE TABLE ProductMovements (
    MovementID SERIAL PRIMARY KEY,
    ProductID INT,
    SourceLocation VARCHAR(255),
    DestinationLocation VARCHAR(255),
    ExpectedArrival DATE,
    Status VARCHAR(50),
    Timestamp TIMESTAMP NOT NULL,
    ShipmentID INT,
    FOREIGN KEY (ProductID) REFERENCES ProductInventory(ProductID),
    FOREIGN KEY (ShipmentID) REFERENCES Transportation(ShipmentID)
);

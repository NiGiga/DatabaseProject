-- 1. Drop & Create database
DROP DATABASE IF EXISTS RestaurantDB;
CREATE DATABASE RestaurantDB;
USE RestaurantDB;

-- 2. Creazione tabelle principali

CREATE TABLE TableRestaurant (
    TableID INT PRIMARY KEY,
    Seats INT,
    Location VARCHAR(50),
    Status ENUM('Available', 'Occupied')
);

CREATE TABLE Employee (
    EmployeeID INT PRIMARY KEY,
    FirstName VARCHAR(50),
    LastName VARCHAR(50),
    Phone VARCHAR(20),
    Email VARCHAR(100),
    Role ENUM('Waiter', 'BarMan', 'Chef', 'Sue', 'Busboy', 'Manager')
);

CREATE TABLE Shift (
    ShiftID INT PRIMARY KEY,
    StartTime TIME,
    EndTime TIME,
    Date DATE
);

CREATE TABLE EmployeeShift (
    EmployeeID INT,
    ShiftID INT,
    PRIMARY KEY (EmployeeID, ShiftID),
    FOREIGN KEY (EmployeeID) REFERENCES Employee(EmployeeID),
    FOREIGN KEY (ShiftID) REFERENCES Shift(ShiftID)
);

CREATE TABLE MenuItem (
    ItemID INT PRIMARY KEY,
    Name VARCHAR(100),
    Description TEXT,
    Price DECIMAL(10,2),
    Availability ENUM('Yes', 'No')
);

CREATE TABLE Reservation (
    ReservationID INT PRIMARY KEY,
    CustomerName VARCHAR(100),
    CustomerPhone VARCHAR(20),
    Email VARCHAR(100),
    Date DATE,
    Time TIME,
    NumberOfGuests INT,
    Status ENUM('Confirmed', 'Cancelled'),
    TableID INT,
    EmployeeID INT,
    FOREIGN KEY (TableID) REFERENCES TableRestaurant(TableID),
    FOREIGN KEY (EmployeeID) REFERENCES Employee(EmployeeID)
);

CREATE TABLE OrderRestaurant (
    OrderID INT PRIMARY KEY,
    TableID INT,
    EmployeeID INT,
    OrderTime TIME,
    OrderAmount DECIMAL(10,2),
    FOREIGN KEY (TableID) REFERENCES TableRestaurant(TableID),
    FOREIGN KEY (EmployeeID) REFERENCES Employee(EmployeeID)
);

CREATE TABLE Contains (
    OrderID INT,
    ItemID INT,
    Quantity INT,
    PRIMARY KEY (OrderID, ItemID),
    FOREIGN KEY (OrderID) REFERENCES OrderRestaurant(OrderID),
    FOREIGN KEY (ItemID) REFERENCES MenuItem(ItemID)
);

CREATE TABLE CashRegister (
    BillID INT PRIMARY KEY,
    OrderID INT,
    BillTime TIME,
    TotalAmount DECIMAL(10,2),
    CashierID INT,
    FOREIGN KEY (OrderID) REFERENCES OrderRestaurant(OrderID),
    FOREIGN KEY (CashierID) REFERENCES Employee(EmployeeID)
);

-- Views

-- 1. Tavoli disponibili
CREATE VIEW AvailableTables AS
SELECT
    TableID,
    Seats,
    Location
FROM
    TableRestaurant
WHERE
    Status = 'Available';

-- 2. Ricavi giornalieri
CREATE VIEW DailySales AS
SELECT
    CURDATE() AS SalesDate,
    SUM(TotalAmount) AS TotalRevenue
FROM
    CashRegister
JOIN
    OrderRestaurant ON CashRegister.OrderID = OrderRestaurant.OrderID
WHERE
    OrderRestaurant.OrderTime BETWEEN '00:00:00' AND '23:59:59';

-- 3. Turni del personale
CREATE VIEW EmployeeShiftView AS
SELECT
    E.EmployeeID,
    E.FirstName,
    E.LastName,
    S.ShiftID,
    S.Date,
    S.StartTime,
    S.EndTime,
    E.Role
FROM
    EmployeeShift ES
JOIN
    Employee E ON ES.EmployeeID = E.EmployeeID
JOIN
    Shift S ON ES.ShiftID = S.ShiftID;

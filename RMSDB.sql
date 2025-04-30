-- CREA DATABASE E SELEZIONA
DROP DATABASE IF EXISTS RestaurantDB;
CREATE DATABASE RestaurantDB;
USE RestaurantDB;

-- CREA TABELLE (semplificato per chiarezza, già visto prima)
CREATE TABLE `Table` (
    TableID INT AUTO_INCREMENT PRIMARY KEY,
    Seats INT NOT NULL,
    Location VARCHAR(255),
    Status ENUM('Available', 'Occupied') DEFAULT 'Available'
);

CREATE TABLE Employee (
    EmployeeID INT AUTO_INCREMENT PRIMARY KEY,
    FirstName VARCHAR(100),
    LastName VARCHAR(100),
    Phone VARCHAR(20),
    Email VARCHAR(255),
    Role ENUM('Waiter', 'BarMan', 'Chef', 'SousChef', 'Busboy', 'Manager')
);

CREATE TABLE Shift (
    ShiftID INT AUTO_INCREMENT PRIMARY KEY,
    StartTime TIME,
    EndTime TIME,
    Date DATE
);

CREATE TABLE Reservation (
    ReservationID INT AUTO_INCREMENT PRIMARY KEY,
    CustomerName VARCHAR(100),
    CustomerPhone VARCHAR(20),
    Email VARCHAR(255),
    Date DATE,
    Time TIME,
    NumberOfGuests INT,
    Status ENUM('Confirmed', 'Cancelled') DEFAULT 'Confirmed',
    TableID INT,
    FOREIGN KEY (TableID) REFERENCES `Table`(TableID)
);

CREATE TABLE MenuItem (
    ItemID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(100),
    Description TEXT,
    Price DECIMAL(10,2),
    Availability BOOLEAN
);

CREATE TABLE `Order` (
    OrderID INT AUTO_INCREMENT PRIMARY KEY,
    TableID INT,
    EmployeeID INT,
    OrderTime DATETIME,
    TotalAmount DECIMAL(10,2),
    FOREIGN KEY (TableID) REFERENCES `Table`(TableID),
    FOREIGN KEY (EmployeeID) REFERENCES Employee(EmployeeID)
);

CREATE TABLE Contains (
    OrderID INT,
    ItemID INT,
    Quantity INT,
    PRIMARY KEY (OrderID, ItemID),
    FOREIGN KEY (OrderID) REFERENCES `Order`(OrderID),
    FOREIGN KEY (ItemID) REFERENCES MenuItem(ItemID)
);

CREATE TABLE Bill (
    BillID INT AUTO_INCREMENT PRIMARY KEY,
    OrderID INT,
    BillTime DATETIME,
    TotalAmount DECIMAL(10,2),
    FOREIGN KEY (OrderID) REFERENCES `Order`(OrderID)
);

-- DATI DI TEST

-- Tavoli
INSERT INTO `Table` (Seats, Location, Status) VALUES
(2, 'Main Hall', 'Available'),
(4, 'Balcony', 'Occupied'),
(6, 'Patio', 'Available');

-- Dipendenti
INSERT INTO Employee (FirstName, LastName, Phone, Email, Role) VALUES
('Alice', 'Rossi', '3331234567', 'alice.rossi@example.com', 'Waiter'),
('Marco', 'Verdi', '3349876543', 'marco.verdi@example.com', 'Chef'),
('Laura', 'Bianchi', '3355555555', 'laura.bianchi@example.com', 'Manager');

-- Turni
INSERT INTO Shift (StartTime, EndTime, Date) VALUES
('10:00:00', '14:00:00', '2025-05-01'),
('18:00:00', '22:00:00', '2025-05-01');

-- Menu
INSERT INTO MenuItem (Name, Description, Price, Availability) VALUES
('Pizza Margherita', 'Pomodoro, mozzarella e basilico', 8.50, TRUE),
('Pasta Carbonara', 'Pasta, uova, pancetta e pecorino', 10.00, TRUE),
('Tiramisù', 'Dolce tradizionale italiano', 5.00, TRUE);

-- Prenotazioni
INSERT INTO Reservation (CustomerName, CustomerPhone, Email, Date, Time, NumberOfGuests, Status, TableID) VALUES
('Giovanni Neri', '3398765432', 'giovanni.neri@mail.com', '2025-05-01', '12:30:00', 2, 'Confirmed', 1),
('Marta Gialli', '3381111222', 'marta.gialli@mail.com', '2025-05-01', '13:00:00', 4, 'Confirmed', 2);

-- Ordini
INSERT INTO `Order` (TableID, EmployeeID, OrderTime, TotalAmount) VALUES
(1, 1, '2025-05-01 12:35:00', 13.50),
(2, 1, '2025-05-01 13:05:00', 15.00);

-- Dettagli ordini
INSERT INTO Contains (OrderID, ItemID, Quantity) VALUES
(1, 1, 1),  -- Pizza
(1, 3, 1),  -- Tiramisù
(2, 2, 1),  -- Pasta
(2, 3, 1);  -- Tiramisù

-- Fatture
INSERT INTO Bill (OrderID, BillTime, TotalAmount) VALUES
(1, '2025-05-01 13:00:00', 13.50),
(2, '2025-05-01 13:30:00', 15.00);

-- 1. Drop & Create database
DROP DATABASE IF EXISTS RestaurantDB;
CREATE DATABASE RestaurantDB;
USE RestaurantDB;

-- 2. Creazione tabelle

CREATE TABLE TableRestaurant (
    TableID INT PRIMARY KEY,
    Seats INT,
    Location VARCHAR(50),
    Status VARCHAR(10) CHECK (Status IN ('Available', 'Occupied'))
);

CREATE TABLE RoomStaff (
    RSID INT PRIMARY KEY,
    FirstName VARCHAR(50),
    LastName VARCHAR(50),
    Phone VARCHAR(20),
    Email VARCHAR(100),
    Role VARCHAR(20) CHECK (Role IN ('Waiter', 'BarMan'))
);

CREATE TABLE KitchenStaff (
    KSID INT PRIMARY KEY,
    FirstName VARCHAR(50),
    LastName VARCHAR(50),
    Phone VARCHAR(20),
    Email VARCHAR(100),
    Role VARCHAR(20) CHECK (Role IN ('Chef', 'Sue', 'Busboy'))
);

CREATE TABLE Manager (
    ManagerID INT PRIMARY KEY,
    FirstName VARCHAR(50),
    LastName VARCHAR(50),
    Phone VARCHAR(20),
    Email VARCHAR(100)
);

CREATE TABLE Shift (
    ShiftID INT PRIMARY KEY,
    StartTime TIME,
    EndTime TIME,
    Date DATE
);

CREATE TABLE MenuItem (
    ItemID INT PRIMARY KEY,
    Name VARCHAR(100),
    Description TEXT,
    Price DECIMAL(10,2),
    Availability VARCHAR(3) CHECK (Availability IN ('Yes', 'No'))
);

CREATE TABLE Reservation (
    ReservationID INT PRIMARY KEY,
    CustomerName VARCHAR(100),
    CustomerPhone VARCHAR(20),
    Email VARCHAR(100),
    Date DATE,
    Time TIME,
    NumberOfGuests INT,
    Status VARCHAR(10) CHECK (Status IN ('Confirmed', 'Cancelled'))
);

CREATE TABLE OrderRestaurant (
    OrderID INT PRIMARY KEY,
    TableID INT,
    RSID INT,
    OrderTime TIME,
    OrderAmount DECIMAL(10,2),
    FOREIGN KEY (TableID) REFERENCES TableRestaurant(TableID),
    FOREIGN KEY (RSID) REFERENCES RoomStaff(RSID)
);

CREATE TABLE CashRegister (
    BillID INT PRIMARY KEY,
    OrderID INT,
    BillTime TIME,
    TotalAmount DECIMAL(10,2),
    FOREIGN KEY (OrderID) REFERENCES OrderRestaurant(OrderID)
);

-- 3. Tabelle relazioni

CREATE TABLE HasReservation (
    ReservationID INT,
    TableID INT,
    PRIMARY KEY (ReservationID, TableID),
    FOREIGN KEY (ReservationID) REFERENCES Reservation(ReservationID),
    FOREIGN KEY (TableID) REFERENCES TableRestaurant(TableID)
);

CREATE TABLE MakeReservation (
    ReservationID INT,
    RSID INT,
    PRIMARY KEY (ReservationID, RSID),
    FOREIGN KEY (ReservationID) REFERENCES Reservation(ReservationID),
    FOREIGN KEY (RSID) REFERENCES RoomStaff(RSID)
);

CREATE TABLE Contains (
    OrderID INT,
    ItemID INT,
    Quantity INT,
    PRIMARY KEY (OrderID, ItemID),
    FOREIGN KEY (OrderID) REFERENCES OrderRestaurant(OrderID),
    FOREIGN KEY (ItemID) REFERENCES MenuItem(ItemID)
);

CREATE TABLE AssignedToKitchen (
    KSID INT,
    ShiftID INT,
    PRIMARY KEY (KSID, ShiftID),
    FOREIGN KEY (KSID) REFERENCES KitchenStaff(KSID),
    FOREIGN KEY (ShiftID) REFERENCES Shift(ShiftID)
);

CREATE TABLE AssignedToRestaurant (
    RSID INT,
    ShiftID INT,
    PRIMARY KEY (RSID, ShiftID),
    FOREIGN KEY (RSID) REFERENCES RoomStaff(RSID),
    FOREIGN KEY (ShiftID) REFERENCES Shift(ShiftID)
);

CREATE TABLE MakesShifts (
    ManagerID INT,
    ShiftID INT,
    PRIMARY KEY (ManagerID, ShiftID),
    FOREIGN KEY (ManagerID) REFERENCES Manager(ManagerID),
    FOREIGN KEY (ShiftID) REFERENCES Shift(ShiftID)
);

CREATE TABLE Cashing (
    BillID INT,
    RSID INT,
    PRIMARY KEY (BillID, RSID),
    FOREIGN KEY (BillID) REFERENCES CashRegister(BillID),
    FOREIGN KEY (RSID) REFERENCES RoomStaff(RSID)
);

-- 4. Inserimento dati di esempio

-- Tavoli
INSERT INTO TableRestaurant VALUES (1, 4, 'Window', 'Available');
INSERT INTO TableRestaurant VALUES (2, 2, 'Center', 'Occupied');

-- Menu
INSERT INTO MenuItem VALUES (101, 'Margherita Pizza', 'Classic pizza with tomato and mozzarella', 8.50, 'Yes');
INSERT INTO MenuItem VALUES (102, 'Pasta Carbonara', 'Egg, cheese, pancetta, and pepper', 10.00, 'Yes');

-- Room Staff
INSERT INTO RoomStaff VALUES (1, 'Luca', 'Bianchi', '1234567890', 'luca@rest.it', 'Waiter');

-- Kitchen Staff
INSERT INTO KitchenStaff VALUES (1, 'Marco', 'Verdi', '0987654321', 'marco@rest.it', 'Chef');

-- Manager
INSERT INTO Manager VALUES (1, 'Chiara', 'Rossi', '111222333', 'chiara@rest.it');

-- Turni
INSERT INTO Shift VALUES (1, '10:00', '14:00', '2025-05-06');

-- Prenotazioni
INSERT INTO Reservation VALUES (1, 'Alice', '333444555', 'alice@email.com', '2025-05-07', '12:30', 2, 'Confirmed');

-- Relazioni prenotazione
INSERT INTO HasReservation VALUES (1, 1);
INSERT INTO MakeReservation VALUES (1, 1);

-- Ordini
INSERT INTO OrderRestaurant VALUES (1, 1, 1, '12:45', 18.50);
INSERT INTO Contains VALUES (1, 101, 1);
INSERT INTO Contains VALUES (1, 102, 1);

-- Cassa
INSERT INTO CashRegister VALUES (1, 1, '13:00', 18.50);
INSERT INTO Cashing VALUES (1, 1);

-- Assegnazioni turni
INSERT INTO AssignedToKitchen VALUES (1, 1);
INSERT INTO AssignedToRestaurant VALUES (1, 1);
INSERT INTO MakesShifts VALUES (1, 1);

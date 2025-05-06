-- Generato con ChatGPT

-- Usa il database
USE RestaurantDB;

-- Disattiva i vincoli temporaneamente
SET FOREIGN_KEY_CHECKS = 0;

-- Elimina i dati in ordine corretto
DELETE FROM CashRegister;
DELETE FROM Contains;
DELETE FROM OrderRestaurant;
DELETE FROM Reservation;
DELETE FROM EmployeeShift;
DELETE FROM Shift;
DELETE FROM MenuItem;
DELETE FROM Employee;
DELETE FROM TableRestaurant;

-- Riattiva i vincoli
SET FOREIGN_KEY_CHECKS = 1;

-- Inserimento tavoli
INSERT INTO TableRestaurant (TableID, Seats, Location, Status) VALUES
(1, 4, 'Sala A', 'Available'), (2, 2, 'Sala A', 'Available'), (3, 4, 'Sala A', 'Occupied'), (4, 6, 'Sala B', 'Available'),
(5, 2, 'Sala B', 'Occupied'), (6, 4, 'Sala B', 'Available'), (7, 6, 'Sala C', 'Occupied'), (8, 4, 'Sala C', 'Available'),
(9, 2, 'Sala C', 'Available'), (10, 4, 'Terrazza', 'Occupied'), (11, 2, 'Terrazza', 'Available'), (12, 6, 'Sala A', 'Available'),
(13, 2, 'Sala A', 'Available'), (14, 4, 'Sala B', 'Occupied'), (15, 6, 'Sala B', 'Available'), (16, 4, 'Sala C', 'Available'),
(17, 2, 'Sala C', 'Occupied'), (18, 6, 'Sala A', 'Available'), (19, 4, 'Sala B', 'Available'), (20, 2, 'Terrazza', 'Available');

-- Inserimento dipendenti
INSERT INTO Employee (EmployeeID, FirstName, LastName, Phone, Email, Role) VALUES
(1, 'Mario', 'Rossi', '1111111111', 'mario@rest.com', 'Manager'),
(2, 'Luigi', 'Verdi', '2222222222', 'luigi@rest.com', 'Chef'),
(3, 'Anna', 'Bianchi', '3333333333', 'anna@rest.com', 'Waiter'),
(4, 'Sara', 'Neri', '4444444444', 'sara@rest.com', 'Waiter'),
(5, 'Giorgio', 'Russo', '5555555555', 'giorgio@rest.com', 'Sue'),
(6, 'Laura', 'Ferrari', '6666666666', 'laura@rest.com', 'BarMan'),
(7, 'Luca', 'Esposito', '7777777777', 'luca@rest.com', 'Chef'),
(8, 'Paolo', 'Conti', '8888888888', 'paolo@rest.com', 'Waiter'),
(9, 'Elisa', 'Costa', '9999999999', 'elisa@rest.com', 'Busboy'),
(10, 'Marta', 'Bruni', '0000000000', 'marta@rest.com', 'Waiter');

-- Inserimento turni
INSERT INTO Shift (ShiftID, StartTime, EndTime, Date) VALUES
(1, '09:00:00', '13:00:00', '2025-05-06'), (2, '13:00:00', '17:00:00', '2025-05-06'),
(3, '17:00:00', '21:00:00', '2025-05-06'), (4, '09:00:00', '13:00:00', '2025-05-07'),
(5, '13:00:00', '17:00:00', '2025-05-07');

-- Associazione dipendenti-turni
INSERT INTO EmployeeShift (EmployeeID, ShiftID) VALUES
(1,1),(2,1),(3,1),(4,2),(5,2),(6,2),(7,3),(8,3),(9,4),(10,5),
(1,2),(2,3),(3,4),(4,5),(5,1),(6,3),(7,4),(8,5),(9,1),(10,2);

-- Inserimento piatti
INSERT INTO MenuItem (ItemID, Name, Description, Price, Availability) VALUES
(1, 'Pizza Margherita', 'Pomodoro, mozzarella, basilico', 8.00, 'Yes'),
(2, 'Carbonara', 'Pasta, uova, guanciale', 10.00, 'Yes'),
(3, 'Lasagna', 'Pasta al forno', 9.00, 'Yes'),
(4, 'Insalata Mista', 'Verdure di stagione', 5.50, 'Yes'),
(5, 'Tagliata di manzo', 'Con rucola e grana', 15.00, 'Yes'),
(6, 'Tiramisù', 'Dolce al caffè', 6.00, 'Yes'),
(7, 'Panna Cotta', 'Con frutti di bosco', 5.00, 'Yes'),
(8, 'Risotto ai funghi', 'Con porcini', 11.00, 'Yes'),
(9, 'Spaghetti al pomodoro', 'Con basilico', 7.50, 'Yes'),
(10, 'Bruschette', 'Con pomodoro e aglio', 4.00, 'Yes'),
(11, 'Frittura di pesce', 'Mista', 13.00, 'Yes'),
(12, 'Zuppa di verdure', 'Con legumi', 6.50, 'Yes'),
(13, 'Pollo alla griglia', 'Con patate', 10.00, 'Yes'),
(14, 'Melanzane alla parmigiana', 'Con mozzarella', 9.50, 'Yes'),
(15, 'Salmone', 'Alla griglia', 14.00, 'Yes'),
(16, 'Gelato artigianale', 'Vaniglia e cioccolato', 5.00, 'Yes'),
(17, 'Patatine fritte', 'Croccanti', 3.50, 'Yes'),
(18, 'Caffè', 'Espresso', 1.50, 'Yes'),
(19, 'Acqua naturale', 'Bottiglia 1L', 2.00, 'Yes'),
(20, 'Vino rosso', 'Calice', 4.00, 'Yes');

-- Inserimento prenotazioni
INSERT INTO Reservation (ReservationID, CustomerName, CustomerPhone, Email, Date, Time, NumberOfGuests, Status, TableID, EmployeeID) VALUES
(1, 'Luca Mori', '123123123', 'luca@email.com', '2025-05-06', '19:00:00', 2, 'Confirmed', 1, 3),
(2, 'Giulia Ferri', '234234234', 'giulia@email.com', '2025-05-06', '20:00:00', 4, 'Confirmed', 2, 4),
(3, 'Marco Bianchi', '345345345', 'marco@email.com', '2025-05-06', '21:00:00', 3, 'Confirmed', 3, 3),
(4, 'Elena Verdi', '456456456', 'elena@email.com', '2025-05-06', '18:00:00', 2, 'Cancelled', 4, 4),
(5, 'Stefano Neri', '567567567', 'stefano@email.com', '2025-05-06', '19:30:00', 2, 'Confirmed', 5, 3),
(6, 'Chiara Riva', '678678678', 'chiara@email.com', '2025-05-06', '20:30:00', 4, 'Confirmed', 6, 4),
(7, 'Alessio Costa', '789789789', 'alessio@email.com', '2025-05-07', '18:30:00', 3, 'Confirmed', 7, 8),
(8, 'Valeria Conti', '890890890', 'valeria@email.com', '2025-05-07', '19:00:00', 2, 'Confirmed', 8, 3),
(9, 'Simone Dini', '901901901', 'simone@email.com', '2025-05-07', '20:00:00', 5, 'Confirmed', 9, 4),
(10, 'Sara Fontana', '012012012', 'sara@email.com', '2025-05-07', '21:00:00', 2, 'Cancelled', 10, 3),
(11, 'Fabio Marino', '123456789', 'fabio@email.com', '2025-05-08', '19:00:00', 2, 'Confirmed', 11, 4),
(12, 'Irene Galli', '234567890', 'irene@email.com', '2025-05-08', '20:00:00', 3, 'Confirmed', 12, 3),
(13, 'Nicola Biagi', '345678901', 'nicola@email.com', '2025-05-08', '18:30:00', 4, 'Confirmed', 13, 4),
(14, 'Lucia Neri', '456789012', 'lucia@email.com', '2025-05-08', '19:30:00', 2, 'Confirmed', 14, 3),
(15, 'Alberto Santi', '567890123', 'alberto@email.com', '2025-05-08', '20:30:00', 2, 'Confirmed', 15, 4),
(16, 'Paola Valli', '678901234', 'paola@email.com', '2025-05-09', '21:00:00', 4, 'Confirmed', 16, 3),
(17, 'Gianni Fonti', '789012345', 'gianni@email.com', '2025-05-09', '19:00:00', 2, 'Confirmed', 17, 4),
(18, 'Veronica Rosi', '890123456', 'veronica@email.com', '2025-05-09', '20:00:00', 3, 'Confirmed', 18, 3),
(19, 'Massimo Pini', '901234567', 'massimo@email.com', '2025-05-09', '21:00:00', 2, 'Confirmed', 19, 4),
(20, 'Alina Monti', '012345678', 'alina@email.com', '2025-05-09', '18:30:00', 4, 'Confirmed', 20, 3);

-- Inserimento ordini + prodotti ordinati + registratore di cassa
-- (Esempio automatizzato per 40 ordini e 2 item per ordine)
-- NB: inserimento con ID da 1 a 40

-- Ordini
INSERT INTO OrderRestaurant (OrderID, TableID, EmployeeID, OrderTime, OrderAmount) VALUES
-- Generati a mano per brevità; puoi automatizzare con script se serve
(1,1,3,'12:00:00', 20.00), (2,2,3,'12:30:00', 16.50), (3,3,4,'13:00:00', 21.00), (4,4,4,'13:30:00', 18.00),
(5,5,3,'14:00:00', 19.50), (6,6,4,'14:30:00', 22.00), (7,7,3,'15:00:00', 17.00), (8,8,4,'15:30:00', 23.00),
(9,9,3,'16:00:00', 20.50), (10,10,4,'16:30:00', 25.00),
(11,1,3,'17:00:00', 19.00), (12,2,4,'17:30:00', 22.00), (13,3,3,'18:00:00', 20.00), (14,4,4,'18:30:00', 24.00),
(15,5,3,'19:00:00', 21.50), (16,6,4,'19:30:00', 23.50), (17,7,3,'20:00:00', 22.00), (18,8,4,'20:30:00', 20.00),
(19,9,3,'21:00:00', 19.50), (20,10,4,'21:30:00', 22.00),
(21,11,3,'12:00:00', 18.00), (22,12,4,'12:30:00', 24.00), (23,13,3,'13:00:00', 22.00), (24,14,4,'13:30:00', 20.00),
(25,15,3,'14:00:00', 25.00), (26,16,4,'14:30:00', 19.00), (27,17,3,'15:00:00', 20.00), (28,18,4,'15:30:00', 21.00),
(29,19,3,'16:00:00', 24.00), (30,20,4,'16:30:00', 23.50),
(31,1,3,'17:00:00', 22.00), (32,2,4,'17:30:00', 21.00), (33,3,3,'18:00:00', 19.00), (34,4,4,'18:30:00', 20.00),
(35,5,3,'19:00:00', 23.00), (36,6,4,'19:30:00', 21.00), (37,7,3,'20:00:00', 24.00), (38,8,4,'20:30:00', 25.00),
(39,9,3,'21:00:00', 20.50), (40,10,4,'21:30:00', 23.00);

-- Contenuti degli ordini
INSERT INTO Contains (OrderID, ItemID, Quantity) VALUES
-- Due piatti per ogni ordine, scelti casualmente
(1,1,1),(1,2,1), (2,3,1),(2,4,1), (3,5,1),(3,6,1), (4,7,1),(4,8,1), (5,9,1),(5,10,1),
(6,11,1),(6,12,1), (7,13,1),(7,14,1), (8,15,1),(8,16,1), (9,17,1),(9,18,1), (10,19,1),(10,20,1),
(11,1,1),(11,3,1), (12,2,1),(12,4,1), (13,5,1),(13,7,1), (14,6,1),(14,8,1), (15,9,1),(15,11,1),
(16,10,1),(16,12,1), (17,13,1),(17,15,1), (18,14,1),(18,16,1), (19,17,1),(19,19,1), (20,18,1),(20,20,1),
(21,1,1),(21,5,1), (22,2,1),(22,6,1), (23,3,1),(23,7,1), (24,4,1),(24,8,1), (25,9,1),(25,13,1),
(26,10,1),(26,14,1), (27,11,1),(27,15,1), (28,12,1),(28,16,1), (29,17,1),(29,18,1), (30,19,1),(30,20,1),
(31,1,1),(31,4,1), (32,2,1),(32,5,1), (33,3,1),(33,6,1), (34,7,1),(34,8,1), (35,9,1),(35,10,1),
(36,11,1),(36,12,1), (37,13,1),(37,14,1), (38,15,1),(38,16,1), (39,17,1),(39,18,1), (40,19,1),(40,20,1);

-- Registrazioni cassa
INSERT INTO CashRegister (BillID, OrderID, BillTime, TotalAmount, CashierID) VALUES
(1,1,'12:15:00',20.00,1), (2,2,'12:45:00',16.50,1), (3,3,'13:15:00',21.00,1), (4,4,'13:45:00',18.00,1),
(5,5,'14:15:00',19.50,1), (6,6,'14:45:00',22.00,1), (7,7,'15:15:00',17.00,1), (8,8,'15:45:00',23.00,1),
(9,9,'16:15:00',20.50,1), (10,10,'16:45:00',25.00,1),
(11,11,'17:15:00',19.00,1), (12,12,'17:45:00',22.00,1), (13,13,'18:15:00',20.00,1), (14,14,'18:45:00',24.00,1),
(15,15,'19:15:00',21.50,1), (16,16,'19:45:00',23.50,1)

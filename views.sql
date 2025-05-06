-- Views

-- 1
CREATE VIEW AvailableTables AS
SELECT
    TableID,
    Seats,
    Location
FROM
    TableRestaurant
WHERE
    Status = 'Available';

-- 2
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

-- 3
CREATE VIEW EmployeeShift AS
SELECT
    RS.RSID AS EmployeeID,
    RS.FirstName,
    RS.LastName,
    S.ShiftID,
    S.Date,
    S.StartTime,
    S.EndTime,
    'RoomStaff' AS Role
FROM
    AssignedToRestaurant AR
JOIN
    RoomStaff RS ON AR.RSID = RS.RSID
JOIN
    Shift S ON AR.ShiftID = S.ShiftID

UNION

SELECT
    KS.KSID AS EmployeeID,
    KS.FirstName,
    KS.LastName,
    S.ShiftID,
    S.Date,
    S.StartTime,
    S.EndTime,
    'KitchenStaff' AS Role
FROM
    AssignedToKitchen AK
JOIN
    KitchenStaff KS ON AK.KSID = KS.KSID
JOIN
    Shift S ON AK.ShiftID = S.ShiftID;

# Restaurant Management System Database – Overview

This project is a **Restaurant Management System Database** design that covers essential operations such as reservations, orders, employees, and menu management. It ensures data integrity through structured relationships and constraints.

## Scope

The database supports core functionalities to manage restaurant operations efficiently, including:

- **Tables**: Information about dining tables.
- **Employees**: Staff details and roles.
- **Shifts**: Employee work schedules.
- **Reservations**: Customer reservation tracking.
- **Menu**: Menu items with pricing and availability.
- **Orders**: Customer order records.

### Out of Scope

- Financial reports
- Supplier inventory management
- Customer loyalty programs

## Functional Requirements

- **Manage Tables**: Add, update, and remove tables.
- **Employee Management**: Add/update/remove employee details and assign shifts.
- **Handle Reservations**: Create, update, cancel, and confirm reservations.
- **Order Management**: Track customer orders and calculate totals.
- **Menu Management**: Add, update, and remove menu items.
- **Shift Scheduling**: Assign employees to shifts.
- **Real-Time Table Availability**: Check table availability.
- **Sales and Performance Tracking**: Generate sales and employee reports.

##

## Optimizations

### Indexes

- `check_table_number`: Speeds up table availability checks.
- `check_reservation_datetime`: Optimizes reservation searches.
- `filter_employee_role`: Improves role-based filtering.
- `check_shift_date & check_order_date`: Enhances scheduling and sales reports.

### Views

- **AvailableTables**: Provides real-time table availability.
- **DailySales**: Summarizes daily revenue.

## Limitations

- Assumes linear relationships (scalability concerns for large datasets).
- No flexible seating arrangements.
- No support for custom menu modifications.
- Employees cannot hold multiple roles in the same shift.

##

**Author**: Nicola Gigante


![Entity-Relationsip Diagram](ER_Diagram.jpeg)

# 📘 Data Dictionary – Entity

---

## 📦 Table
| Attribute | Data Type | Constraints     | Description                        |
|-----------|-----------|-----------------|------------------------------------|
| TableID   | INTEGER   | PK, NOT NULL    | Unique identifier for the table    |
| Seats     | INTEGER   | NOT NULL        | Number of available seats          |
| Location  | TEXT      | NULLABLE        | Table location (e.g., patio)       |
| Status    | TEXT      | DEFAULT 'free'  | Table status (e.g., free, occupied)|

---

## 👤 Employee (waiter, chef, manager)
| Attribute   | Data Type | Constraints     | Description                          |
|-------------|-----------|-----------------|--------------------------------------|
| EmployeeID  | INTEGER   | PK, NOT NULL    | Unique ID for the employee           |
| FirstName   | TEXT      | NOT NULL        | First name                           |
| LastName    | TEXT      | NOT NULL        | Last name                            |
| Phone       | TEXT      | NULLABLE        | Contact phone number                 |
| Email       | TEXT      | UNIQUE          | Company email                        |

---

## 🕑 Shift
| Attribute | Data Type | Constraints  | Description               |
|-----------|-----------|--------------|---------------------------|
| ShiftID   | INTEGER   | PK, NOT NULL | Unique shift identifier   |
| StartTime | TIME      | NOT NULL     | Start time of the shift   |
| EndTime   | TIME      | NOT NULL     | End time of the shift     |
| Date      | DATE      | NOT NULL     | Date of the shift         |

---

## 🔁 EmployeeShift
| Attribute   | Data Type | Constraints                        | Description                                |
|-------------|-----------|-------------------------------------|--------------------------------------------|
| EmployeeID  | INTEGER   | FK → Employee(EmployeeID)          | Assigned employee                          |
| ShiftID     | INTEGER   | FK → Shift(ShiftID)                | Associated shift                           |
| Role        | TEXT      | NULLABLE                           | Optional specific role in the shift        |
| **PK**      |           | (EmployeeID, ShiftID)              | Composite primary key                      |

---

## 📅 Reservation
| Attribute        | Data Type | Constraints                    | Description                                  |
|------------------|-----------|----------------------------------|----------------------------------------------|
| ReservationID    | INTEGER   | PK, NOT NULL                    | Unique reservation ID                        |
| CustomerName     | TEXT      | NOT NULL                        | Name of the customer                         |
| CustomerPhone    | TEXT      | NOT NULL                        | Customer's phone number                      |
| Date             | DATE      | NOT NULL                        | Reservation date                             |
| Time             | TIME      | NOT NULL                        | Reservation time                             |
| NumberOfGuests   | INTEGER   | NOT NULL                        | Number of guests                             |
| TableID          | INTEGER   | FK → Table(TableID)             | Reserved table                               |
| Status           | TEXT      | DEFAULT 'confirmed'             | Reservation status (e.g., confirmed, canceled)|

---

## 🧾 Order
| Attribute   | Data Type | Constraints                     | Description                                |
|-------------|-----------|----------------------------------|--------------------------------------------|
| OrderID     | INTEGER   | PK, NOT NULL                    | Unique order ID                            |
| TableID     | INTEGER   | FK → Table(TableID)             | Table where the order was made             |
| EmployeeID  | INTEGER   | FK → Employee(EmployeeID)       | Waiter who took the order                  |
| OrderTime   | DATETIME  | NOT NULL                        | Date and time of the order                 |
| TotalAmount | DECIMAL   | COMPUTED or NULL                | Total price (can be computed from items)   |

---

## 🍽️ MenuItem
| Attribute   | Data Type | Constraints     | Description                            |
|-------------|-----------|-----------------|----------------------------------------|
| ItemID      | INTEGER   | PK, NOT NULL    | Unique menu item ID                    |
| Name        | TEXT      | NOT NULL        | Name of the item                       |
| Description | TEXT      | NULLABLE        | Item description                       |
| Price       | DECIMAL   | NOT NULL        | Price                                  |
| Availability| BOOLEAN   | DEFAULT TRUE    | Whether the item is available          |

---

## 🍴 OrderItem
| Attribute   | Data Type | Constraints                     | Description                              |
|-------------|-----------|----------------------------------|------------------------------------------|
| OrderID     | INTEGER   | FK → Order(OrderID)             | ID of the related order                  |
| ItemID      | INTEGER   | FK → MenuItem(ItemID)           | ID of the ordered item                   |
| Quantity    | INTEGER   | NOT NULL                        | Quantity of the item ordered             |
| **PK**      |           | (OrderID, ItemID)               | Composite primary key                    |

---

# 🔗 Data Dictionary – Relationships

---

## HasReservation
| Property       | Value                                                                 |
|----------------|-----------------------------------------------------------------------|
| Entities       | Table (1,N) — Reservation (1,1)                                       |
| Description    | A table can have multiple reservations, but each reservation is for one table |
| Implementation | `Reservation.TableID` is a foreign key referencing `Table.TableID`    |

---

## ReceivesOrder
| Property       | Value                                                                 |
|----------------|-----------------------------------------------------------------------|
| Entities       | Table (0,N) — Order (1,1)                                             |
| Description    | A table can receive multiple orders, each order is linked to one table|
| Implementation | `Order.TableID` is a foreign key referencing `Table.TableID`          |

---

## TakesOrder
| Property       | Value                                                                 |
|----------------|-----------------------------------------------------------------------|
| Entities       | Employee (1,1) — Order (0,N)                                          |
| Description    | An employee (e.g., a waiter) can take many orders, each order is taken by one employee |
| Implementation | `Order.EmployeeID` is a foreign key referencing `Employee.EmployeeID` |

---

## AssignedTo
| Property       | Value                                                                |
|----------------|----------------------------------------------------------------------|
| Entities       | Employee (1,N) — Shift (1,N)                                         |
| Description    | Employees can be assigned to multiple shifts, and each shift can include multiple employees |
| Implementation | Implemented via the `EmployeeShift` join table                       |
| Join Table     | `EmployeeShift` (EmployeeID, ShiftID, Role, etc.)                    |


---

## Contains
| Property       | Value                                                                 |
|----------------|-----------------------------------------------------------------------|
| Entities       | Order (1,N) — MenuItem (1,N)                                          |
| Description    | An order can contain multiple menu items, and each menu item can appear in many orders |
| Implementation | Implemented via the `OrderItem` join table with FK to both `Order` and `MenuItem` |

---


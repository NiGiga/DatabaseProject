import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import add_order
import add_reservation
import delete_reservation
import edit_reservation
import edit_shift
import get_available_tables
import print_receipt
import show_menu
import show_shifts
import mysql.connector
from datetime import datetime
from decimal import Decimal


# ------------------------- FUNZIONI SPECIALI -------------------------
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Pidosh1998@",
        database="RestaurantDB"
    )

def add_reservation_gui():
    window = tk.Toplevel(root)
    window.title("Inserimento Prenotazione")
    window.geometry("400x400")

    entries = {}
    labels = [
        ("Nome cliente:", "name"),
        ("Telefono:", "phone"),
        ("Email:", "email"),
        ("Data prenotazione (YYYY-MM-DD):", "date"),
        ("Ora prenotazione (HH:MM):", "time"),
        ("Numero di ospiti:", "guests"),
        ("Numero tavolo:", "table")
    ]

    for label_text, key in labels:
        tk.Label(window, text=label_text).pack(pady=2)
        entry = tk.Entry(window)
        entry.pack()
        entries[key] = entry

    def submit():
        try:
            name = entries["name"].get().strip()
            phone = entries["phone"].get().strip()
            email = entries["email"].get().strip()
            date_str = entries["date"].get().strip()
            time_str = entries["time"].get().strip()
            guests = int(entries["guests"].get().strip())
            table_id = int(entries["table"].get().strip())

            datetime.strptime(date_str, "%Y-%m-%d")
            datetime.strptime(time_str, "%H:%M")

            conn = get_connection()
            cursor = conn.cursor()

            check_query = """
                SELECT 1 FROM Reservation
                WHERE TableID = %s AND Date = %s
                AND ABS(TIMESTAMPDIFF(MINUTE, Time, %s)) < 90
                AND Status = 'Confirmed'
            """
            cursor.execute(check_query, (table_id, date_str, time_str))
            if cursor.fetchone():
                messagebox.showerror("Tavolo occupato", "❌ Tavolo occupato per quell'orario.")
                return

            insert_query = """
                INSERT INTO Reservation (CustomerName, CustomerPhone, Email, Date, Time, NumberOfGuests, Status, TableID, EmployeeID)
                VALUES (%s, %s, %s, %s, %s, %s, 'Confirmed', %s, 3)
            """
            cursor.execute(insert_query, (name, phone, email, date_str, time_str, guests, table_id))
            conn.commit()
            messagebox.showinfo("Successo", "✅ Prenotazione aggiunta.")
        except Exception as e:
            messagebox.showerror("Errore", f"Errore durante l'inserimento: {e}")
        finally:
            cursor.close()
            conn.close()

    tk.Button(window, text="Inserisci Prenotazione", command=submit).pack(pady=10)

def show_available_tables_gui():
    window = tk.Toplevel(root)
    window.title("Controlla Tavoli Disponibili")
    window.geometry("500x400")

    tk.Label(window, text="Data (YYYY-MM-DD):").pack(pady=5)
    date_entry = tk.Entry(window)
    date_entry.pack(pady=5)

    tk.Label(window, text="Orario (HH:MM):").pack(pady=5)
    time_entry = tk.Entry(window)
    time_entry.pack(pady=5)

    output = tk.Text(window, height=15)
    output.pack(pady=10, fill="both", expand=True)

    def submit():
        date_str = date_entry.get().strip()
        time_str = time_entry.get().strip()
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            datetime.strptime(time_str, "%H:%M")

            conn = get_connection()
            cursor = conn.cursor(dictionary=True)

            query = """
                SELECT t.TableID, t.Seats, t.Location
                FROM TableRestaurant t
                WHERE t.Status = 'Available'
                AND t.TableID NOT IN (
                    SELECT r.TableID
                    FROM Reservation r
                    WHERE r.Date = %s
                    AND ABS(TIMESTAMPDIFF(MINUTE, r.Time, %s)) < 90
                    AND r.Status = 'Confirmed'
                )
            """
            cursor.execute(query, (date_str, time_str))
            results = cursor.fetchall()

            output.delete(1.0, tk.END)
            if results:
                output.insert(tk.END, f"\n✅ Tavoli disponibili per {date_str} alle {time_str}:\n\n")
                for row in results:
                    output.insert(tk.END, f"🪑 Tavolo ID: {row['TableID']} | Posti: {row['Seats']} | Posizione: {row['Location']}\n")
            else:
                output.insert(tk.END, "\n⚠️ Nessun tavolo disponibile per la data e ora specificata.\n")

            cursor.close()
            conn.close()

        except ValueError:
            messagebox.showerror("Errore", "Formato data o ora non valido.")

    tk.Button(window, text="Cerca", command=submit).pack(pady=10)

def show_report_gui():
    window = tk.Toplevel(root)
    window.title("Report Clienti e Incassi")
    window.geometry("500x300")

    tk.Label(window, text="Lascia vuoto per usare la data più recente disponibile.\n").pack()

    tk.Label(window, text="📅 Inserisci data inizio (YYYY-MM-DD):").pack()
    start_entry = tk.Entry(window)
    start_entry.pack(pady=5)

    tk.Label(window, text="📅 Inserisci data fine (YYYY-MM-DD):").pack()
    end_entry = tk.Entry(window)
    end_entry.pack(pady=5)

    output = tk.Text(window, height=10)
    output.pack(pady=10, fill="both", expand=True)

    def generate():
        start_date = start_entry.get().strip()
        end_date = end_entry.get().strip()

        conn = get_connection()
        cursor = conn.cursor()

        try:
            if not end_date:
                cursor.execute("SELECT MAX(Date) FROM Reservation")
                result = cursor.fetchone()[0]
                if result:
                    end_date = result.strftime("%Y-%m-%d")
                else:
                    output.insert(tk.END, "\nNessuna data trovata nel database.\n")
                    return
            if not start_date:
                start_date = end_date

            cursor.execute("""
                SELECT IFNULL(SUM(NumberOfGuests), 0)
                FROM Reservation
                WHERE Status = 'Confirmed' AND Date BETWEEN %s AND %s
            """, (start_date, end_date))
            guests = cursor.fetchone()[0]

            cursor.execute("""
                SELECT IFNULL(SUM(TotalAmount), 0)
                FROM CashRegister c
                JOIN OrderRestaurant o ON c.OrderID = o.OrderID
                WHERE o.OrderTime BETWEEN %s AND %s
            """, (start_date + " 00:00:00", end_date + " 23:59:59"))
            revenue = cursor.fetchone()[0]

            output.delete(1.0, tk.END)
            output.insert(tk.END, f"\n📆 Intervallo considerato: {start_date} ➡️ {end_date}\n")
            output.insert(tk.END, "\n📈 REPORT RISTORANTE\n")
            output.insert(tk.END, "-" * 40 + "\n")
            output.insert(tk.END, f"👥 Clienti serviti: {guests}\n")
            output.insert(tk.END, f"💶 Incasso totale: €{revenue:.2f}\n")
            output.insert(tk.END, "-" * 40 + "\n")

        except Exception as e:
            messagebox.showerror("Errore", f"Errore durante la generazione del report: {e}")
        finally:
            cursor.close()
            conn.close()

    tk.Button(window, text="Genera Report", command=generate).pack(pady=5)

def print_receipt_gui():
    window = tk.Toplevel(root)
    window.title("Stampa Ricevuta")
    window.geometry("400x250")

    tk.Label(window, text="🧾 RICERCA PRENOTAZIONE PER RICEVUTA").pack(pady=10)
    tk.Label(window, text="Cerca per:").pack()

    search_var = tk.StringVar()
    search_var.set("1")

    tk.Radiobutton(window, text="ID prenotazione", variable=search_var, value="1").pack(anchor="w")
    tk.Radiobutton(window, text="Nome cliente", variable=search_var, value="2").pack(anchor="w")
    tk.Radiobutton(window, text="Numero tavolo", variable=search_var, value="3").pack(anchor="w")

    input_entry = tk.Entry(window)
    input_entry.pack(pady=10)

    def execute():
        mode = search_var.get()
        value = input_entry.get().strip()

        if mode == "1":
            print_receipt.print_receipt_from_gui("ReservationID", value)
        elif mode == "2":
            print_receipt.print_receipt_from_gui("CustomerName", value)
        elif mode == "3":
            print_receipt.print_receipt_from_gui("TableID", value)
        else:
            messagebox.showerror("Errore", "Scelta non valida")

    tk.Button(window, text="Stampa Ricevuta", command=execute).pack(pady=10)

def show_menu_gui():
    window = tk.Toplevel(root)
    window.title("Menù del Ristorante")
    window.geometry("600x600")

    output = tk.Text(window)
    output.pack(fill="both", expand=True)

    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM MenuItem")
        items = cursor.fetchall()
        cursor.close()
        conn.close()

        output.insert(tk.END, "\n🔍 Visualizzazione del menù ristorante...\n")
        output.insert(tk.END, "\n🍽️ MENU DEL RISTORANTE\n\n")

        for item in items:
            output.insert(tk.END, f"🆔 ID: {item['ItemID']}\n")
            output.insert(tk.END, f"📛 Nome: {item['Name']}\n")
            output.insert(tk.END, f"📝 Descrizione: {item['Description']}\n")
            output.insert(tk.END, f"💶 Prezzo: €{item['Price']:.2f}\n")
            output.insert(tk.END, f"✅ Disponibilità: {'Disponibile' if item['Availability'] == 'Yes' else 'Non disponibile'}\n")
            output.insert(tk.END, "-" * 50 + "\n")

    except Exception as e:
        messagebox.showerror("Errore", f"Errore nel caricamento del menù: {e}")

# ------------------------ Autenticazione Manager ------------------------
def authenticate_manager(employee_id, password):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT Role FROM Employee
        WHERE EmployeeID = %s AND Password = %s
    """, (employee_id, password))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result and result[0] == "Manager"

# ------------------------ Gestione Turni GUI ------------------------
def edit_shift_gui():
    window = tk.Toplevel()
    window.title("Gestione Turni (Manager)")
    window.geometry("400x600")

    tk.Label(window, text="👮 AUTENTICAZIONE MANAGER PER GESTIONE TURNI", font=("Helvetica", 12, "bold")).pack(pady=10)

    tk.Label(window, text="🔑 Inserisci il tuo EmployeeID:").pack()
    id_entry = tk.Entry(window)
    id_entry.pack()

    tk.Label(window, text="🔐 Inserisci la tua password numerica:").pack()
    pwd_entry = tk.Entry(window, show="*")
    pwd_entry.pack()

    def proceed():
        manager_id = id_entry.get().strip()
        password = pwd_entry.get().strip()

        if not manager_id.isdigit() or not password.isdigit():
            messagebox.showerror("Errore", "EmployeeID e password devono essere numerici")
            return

        if not authenticate_manager(manager_id, password):
            messagebox.showerror("Accesso negato", "❌ Autenticazione fallita")
            return

        messagebox.showinfo("Accesso", "✅ Accesso autorizzato. Puoi gestire i turni.")
        show_shift_editor(window)

    tk.Button(window, text="Accedi", command=proceed).pack(pady=10)

def show_shift_editor(parent):
    frame = tk.Frame(parent)
    frame.pack(pady=10, fill="both", expand=True)

    tk.Label(frame, text="📅 Inserisci la data del turno (YYYY-MM-DD):").pack()
    date_entry = tk.Entry(frame)
    date_entry.pack()

    tk.Label(frame, text="🕒 Ora di inizio (HH:MM):").pack()
    start_entry = tk.Entry(frame)
    start_entry.pack()

    tk.Label(frame, text="🕒 Ora di fine (HH:MM):").pack()
    end_entry = tk.Entry(frame)
    end_entry.pack()

    tk.Label(frame, text="➕ Assegna dipendenti al turno (uno alla volta):").pack()
    emp_entry = tk.Entry(frame)
    emp_entry.pack()

    assigned = []
    log = tk.Text(frame, height=10)
    log.pack(pady=5)

    def add_employee():
        emp_id = emp_entry.get().strip()
        if emp_id.isdigit():
            assigned.append(int(emp_id))
            log.insert(tk.END, f"✅ Dipendente {emp_id} assegnato.\n")
            emp_entry.delete(0, tk.END)
        else:
            log.insert(tk.END, "⚠️ Inserire un ID numerico valido.\n")

    def save_shift():
        try:
            date_str = date_entry.get().strip()
            start_time = start_entry.get().strip()
            end_time = end_entry.get().strip()

            datetime.strptime(date_str, "%Y-%m-%d")
            datetime.strptime(start_time, "%H:%M")
            datetime.strptime(end_time, "%H:%M")

            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO Shift (StartTime, EndTime, Date)
                VALUES (%s, %s, %s)
            """, (start_time, end_time, date_str))
            conn.commit()

            shift_id = cursor.lastrowid

            for emp in assigned:
                cursor.execute("""
                    INSERT INTO EmployeeShift (EmployeeID, ShiftID)
                    VALUES (%s, %s)
                """, (emp, shift_id))
            conn.commit()
            log.insert(tk.END, "✅ Turno registrato e assegnato correttamente.\n")
            cursor.close()
            conn.close()
        except Exception as e:
            log.insert(tk.END, f"❌ Errore durante il salvataggio: {e}\n")

    tk.Button(frame, text="Assegna Dipendente", command=add_employee).pack(pady=5)
    tk.Button(frame, text="Salva Turno", command=save_shift).pack(pady=5)

# ------------------------ Fetch prenotazioni ------------------------
def fetch_reservations_by_field(field, value):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = f"""
        SELECT *
        FROM Reservation
        WHERE {field} LIKE %s AND Status = 'Confirmed'
    """
    like_value = ('%' + value + '%') if field not in ('ReservationID', 'TableID') else value
    cursor.execute(query, (like_value,))
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results

# ------------------------ GUI per modificare prenotazione ------------------------
def edit_reservation_gui():
    window = tk.Toplevel()
    window.title("Modifica Prenotazione")
    window.geometry("450x550")

    tk.Label(window, text="📝 MODIFICA PRENOTAZIONE", font=("Helvetica", 14, "bold")).pack(pady=10)
    tk.Label(window, text="🔍 Cerca prenotazione da modificare:").pack()

    search_var = tk.StringVar()
    search_var.set("1")

    tk.Radiobutton(window, text="1. Per ID", variable=search_var, value="1").pack(anchor="w")
    tk.Radiobutton(window, text="2. Per nome cliente", variable=search_var, value="2").pack(anchor="w")
    tk.Radiobutton(window, text="3. Per email cliente", variable=search_var, value="3").pack(anchor="w")

    input_entry = tk.Entry(window)
    input_entry.pack(pady=10)

    def find_and_edit():
        field_map = {"1": "ReservationID", "2": "CustomerName", "3": "Email"}
        field = field_map.get(search_var.get())
        value = input_entry.get().strip()

        reservations = fetch_reservations_by_field(field, value)
        if not reservations:
            messagebox.showerror("Errore", "❌ Nessuna prenotazione trovata.")
            return

        res = reservations[0]

        form = tk.Toplevel(window)
        form.title("Modifica Prenotazione")
        form.geometry("400x400")

        tk.Label(form, text=f"✏️ Modifica prenotazione ID {res['ReservationID']} per {res['CustomerName']}").pack(pady=5)

        fields = [
            ("Nome cliente", "CustomerName"),
            ("Telefono", "CustomerPhone"),
            ("Email", "Email"),
            ("Data", "Date"),
            ("Orario", "Time"),
            ("Ospiti", "NumberOfGuests"),
            ("Tavolo", "TableID")
        ]

        entries = {}
        for label, key in fields:
            tk.Label(form, text=f"{label} [{res[key]}]:").pack()
            e = tk.Entry(form)
            e.pack()
            entries[key] = e

        def save_changes():
            try:
                new_data = {}
                for label, key in fields:
                    val = entries[key].get().strip()
                    new_data[key] = val if val else res[key]

                new_data["NumberOfGuests"] = int(new_data["NumberOfGuests"])
                new_data["TableID"] = int(new_data["TableID"])

                conn = get_connection()
                cursor = conn.cursor()

                check_query = """
                    SELECT 1 FROM Reservation
                    WHERE TableID = %s AND Date = %s AND ReservationID != %s
                    AND ABS(TIMESTAMPDIFF(MINUTE, Time, %s)) < 90
                    AND Status = 'Confirmed'
                """
                cursor.execute(check_query, (new_data["TableID"], new_data["Date"], res["ReservationID"], new_data["Time"]))
                if cursor.fetchone():
                    messagebox.showerror("Tavolo occupato", "❌ Tavolo non disponibile a quell’orario.")
                    return

                cursor.execute("""
                    UPDATE Reservation
                    SET CustomerName=%s, CustomerPhone=%s, Email=%s,
                        Date=%s, Time=%s, NumberOfGuests=%s, TableID=%s
                    WHERE ReservationID=%s
                """, (
                    new_data["CustomerName"], new_data["CustomerPhone"], new_data["Email"],
                    new_data["Date"], new_data["Time"], new_data["NumberOfGuests"],
                    new_data["TableID"], res["ReservationID"]
                ))
                conn.commit()
                cursor.close()
                conn.close()
                messagebox.showinfo("Successo", "✅ Prenotazione modificata.")
                form.destroy()

            except Exception as e:
                messagebox.showerror("Errore", f"❌ Errore durante la modifica: {e}")

        tk.Button(form, text="Salva modifiche", command=save_changes).pack(pady=10)

    tk.Button(window, text="Cerca e Modifica", command=find_and_edit).pack(pady=10)

# ------------------------ GUI per cancellare prenotazione ------------------------
def delete_reservation_gui():
    window = tk.Toplevel()
    window.title("Elimina Prenotazione")
    window.geometry("450x350")

    tk.Label(window, text="🗑️ ELIMINA PRENOTAZIONE", font=("Helvetica", 14, "bold")).pack(pady=10)
    tk.Label(window, text="🔍 Cerca prenotazione da cancellare:").pack()

    search_var = tk.StringVar()
    search_var.set("1")

    tk.Radiobutton(window, text="1. Per ID", variable=search_var, value="1").pack(anchor="w")
    tk.Radiobutton(window, text="2. Per nome cliente", variable=search_var, value="2").pack(anchor="w")
    tk.Radiobutton(window, text="3. Per email cliente", variable=search_var, value="3").pack(anchor="w")

    input_entry = tk.Entry(window)
    input_entry.pack(pady=10)

    def search_and_delete():
        field_map = {"1": "ReservationID", "2": "CustomerName", "3": "Email"}
        field = field_map.get(search_var.get())
        value = input_entry.get().strip()

        reservations = fetch_reservations_by_field(field, value)
        if not reservations:
            messagebox.showerror("Errore", "❌ Nessuna prenotazione trovata.")
            return

        res = reservations[0]

        confirm = messagebox.askyesno("Conferma", f"🗑️ Conferma cancellazione prenotazione ID {res['ReservationID']} per {res['CustomerName']}?")
        if not confirm:
            messagebox.showinfo("Annullato", "❌ Operazione annullata.")
            return

        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Reservation WHERE ReservationID = %s", (res['ReservationID'],))
            conn.commit()
            cursor.close()
            conn.close()
            messagebox.showinfo("Successo", "✅ Prenotazione cancellata.")
        except Exception as e:
            messagebox.showerror("Errore", f"❌ Errore durante la cancellazione: {e}")

    tk.Button(window, text="Cerca e Cancella", command=search_and_delete).pack(pady=10)

# ------------------------ GUI per inserimento nuovo ordine ------------------------
def add_order_gui():
    window = tk.Toplevel()
    window.title("Inserimento Nuovo Ordine")
    window.geometry("400x600")

    tk.Label(window, text="🍽️ INSERIMENTO NUOVO ORDINE", font=("Helvetica", 14, "bold")).pack(pady=10)

    tk.Label(window, text="🪑 Inserisci ID del tavolo:").pack()
    table_entry = tk.Entry(window)
    table_entry.pack()

    tk.Label(window, text="👤 Inserisci ID del cameriere:").pack()
    waiter_entry = tk.Entry(window)
    waiter_entry.pack()

    output = tk.Text(window, height=15)
    output.pack(pady=10, fill="both", expand=True)

    def start_order():
        try:
            table_id = int(table_entry.get().strip())
            waiter_id = int(waiter_entry.get().strip())

            now = datetime.now().strftime("%H:%M:%S")

            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO OrderRestaurant (TableID, EmployeeID, OrderTime, OrderAmount)
                VALUES (%s, %s, %s, 0.0)
            """, (table_id, waiter_id, now))
            conn.commit()
            order_id = cursor.lastrowid
            output.insert(tk.END, f"\n🧾 Nuovo ordine ID {order_id} creato.\n")

            total = 0.0
            def add_item():
                nonlocal total
                total = Decimal('0.0')
                item_id = item_entry.get().strip()
                if not item_id:
                    cursor.execute("UPDATE OrderRestaurant SET OrderAmount = %s WHERE OrderID = %s", (total, order_id))
                    conn.commit()
                    output.insert(tk.END, f"\n💰 Totale ordine aggiornato: €{total:.2f}\n")
                    output.insert(tk.END, "✅ Ordine completato con successo.\n")
                    return

                qty = qty_entry.get().strip()
                if not qty.isdigit():
                    output.insert(tk.END, "⚠️ Quantità non valida.\n")
                    return

                qty = int(qty)
                cursor.execute("SELECT Price FROM MenuItem WHERE ItemID = %s", (item_id,))
                price = cursor.fetchone()
                if not price:
                    output.insert(tk.END, "⚠️ ID piatto non trovato.\n")
                    return
                subtotal = price[0] * qty
                cursor.execute("INSERT INTO Contains (OrderID, ItemID, Quantity) VALUES (%s, %s, %s)", (order_id, item_id, qty))
                conn.commit()
                output.insert(tk.END, f"✅ Aggiunto: Item {item_id} x{qty} (subtotale €{subtotal:.2f})\n")
                total += subtotal
                item_entry.delete(0, tk.END)
                qty_entry.delete(0, tk.END)

            # Inserimento piatti
            tk.Label(window, text="🍽️ Inserisci ID del piatto (o premi invio per terminare):").pack()
            item_entry = tk.Entry(window)
            item_entry.pack()

            tk.Label(window, text="🔢 Inserisci quantità:").pack()
            qty_entry = tk.Entry(window)
            qty_entry.pack()

            tk.Button(window, text="Aggiungi Piatto", command=add_item).pack(pady=10)

        except Exception as e:
            messagebox.showerror("Errore", f"❌ Errore durante l'inserimento dell'ordine: {e}")

    tk.Button(window, text="Crea Ordine", command=start_order).pack(pady=10)

# ------------------------ Visualizza turni dipendenti ------------------------
def show_shifts_gui():
    window = tk.Toplevel()
    window.title("Turni Dipendenti")
    window.geometry("600x500")

    tk.Label(window, text="📆 Visualizzazione turni dipendenti", font=("Helvetica", 14, "bold")).pack(pady=10)
    tk.Label(window, text="Vuoi visualizzare i turni di:").pack()

    choice = tk.StringVar()
    choice.set("1")

    tk.Radiobutton(window, text="1. Tutti i dipendenti", variable=choice, value="1").pack(anchor="w")
    tk.Radiobutton(window, text="2. Un solo dipendente", variable=choice, value="2").pack(anchor="w")

    tk.Label(window, text="Inserisci ID dipendente (se hai scelto 2):").pack()
    emp_entry = tk.Entry(window)
    emp_entry.pack(pady=5)

    output = tk.Text(window, height=20)
    output.pack(pady=10, fill="both", expand=True)

    def fetch_shifts():
        emp_id = emp_entry.get().strip()
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)

            if choice.get() == "2" and emp_id:
                cursor.execute("""
                    SELECT S.ShiftID, S.Date, S.StartTime, S.EndTime, 
                           E.EmployeeID, E.FirstName, E.LastName, E.Role
                    FROM Shift S
                    JOIN EmployeeShift ES ON S.ShiftID = ES.ShiftID
                    JOIN Employee E ON ES.EmployeeID = E.EmployeeID
                    WHERE E.EmployeeID = %s
                    ORDER BY S.Date, S.StartTime
                """, (emp_id,))
            else:
                cursor.execute("""
                    SELECT S.ShiftID, S.Date, S.StartTime, S.EndTime, 
                           E.EmployeeID, E.FirstName, E.LastName, E.Role
                    FROM Shift S
                    JOIN EmployeeShift ES ON S.ShiftID = ES.ShiftID
                    JOIN Employee E ON ES.EmployeeID = E.EmployeeID
                    ORDER BY S.Date, S.StartTime
                """)

            shifts = cursor.fetchall()
            cursor.close()
            conn.close()

            output.delete(1.0, tk.END)
            if not shifts:
                output.insert(tk.END, "❌ Nessun turno trovato.\n")
                return

            output.insert(tk.END, "\n📋 Elenco turni dei dipendenti:\n\n")
            for s in shifts:
                output.insert(tk.END, f"🆔 Shift ID: {s['ShiftID']}\n")
                output.insert(tk.END, f"👤 Dipendente: {s['FirstName']} {s['LastName']} (ID: {s['EmployeeID']} | Ruolo: {s['Role']})\n")
                output.insert(tk.END, f"📅 Data: {s['Date']}\n")
                output.insert(tk.END, f"🕒 Orario: {s['StartTime']} - {s['EndTime']}\n")
                output.insert(tk.END, "-" * 40 + "\n")

        except Exception as e:
            messagebox.showerror("Errore", f"Errore nel recupero dei turni: {e}")

    tk.Button(window, text="Visualizza Turni", command=fetch_shifts).pack(pady=10)

# ------------------------- DASHBOARD PRINCIPALE -------------------------
root = tk.Tk()
root.title("Dashboard Ristorante")
root.geometry("400x750")

# Titolo
tk.Label(root, text="✨ GESTIONE RISTORANTE ✨", font=("Helvetica", 16)).pack(pady=20)

# Pulsanti principali
tk.Button(root, text="🍽️ Visualizza Menù", width=30, command=show_menu_gui).pack(pady=5)
tk.Button(root, text="📊 Report Clienti & Incassi", width=30, command=show_report_gui).pack(pady=5)
tk.Button(root, text="🔄 Tavoli Disponibili", width=30, command=show_available_tables_gui).pack(pady=5)
tk.Button(root, text="📅 Nuova Prenotazione", width=30, command=add_reservation_gui).pack(pady=5)
tk.Button(root, text="✏️ Modifica Prenotazione", width=30, command=edit_reservation_gui).pack(pady=5)
tk.Button(root, text="❌ Cancella Prenotazione", width=30, command=delete_reservation_gui).pack(pady=5)
tk.Button(root, text="📋 Stampa Ricevuta", width=30, command=print_receipt_gui).pack(pady=5)
tk.Button(root, text="➕ Aggiungi Ordine", width=30, command=add_order_gui).pack(pady=5)
tk.Button(root, text="📆 Turni Dipendenti", width=30, command=show_shifts_gui).pack(pady=5)
tk.Button(root, text="✍️ Gestione Turni (Manager)", width=30, command=edit_shift_gui).pack(pady=5)

# Avvia la GUI
root.mainloop()

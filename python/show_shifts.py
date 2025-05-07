import mysql.connector


def get_connection():
    """
    Crea e restituisce una connessione attiva al database MySQL.
    """
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="UR_PSW",
        database="RestaurantDB"
    )


def show_shifts(employee_id=None):
    """
    Mostra i turni di lavoro dei dipendenti.

    Se viene passato un ID specifico (employee_id), mostra solo i turni
    relativi a quel dipendente. Altrimenti, mostra tutti i turni registrati.
    """
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        if employee_id:
            # Turni di un singolo dipendente
            query = """
                SELECT s.ShiftID, s.Date, s.StartTime, s.EndTime,
                       e.EmployeeID, e.FirstName, e.LastName, e.Role
                FROM Shift s
                JOIN EmployeeShift es ON s.ShiftID = es.ShiftID
                JOIN Employee e ON es.EmployeeID = e.EmployeeID
                WHERE e.EmployeeID = %s
                ORDER BY s.Date, s.StartTime
            """
            cursor.execute(query, (employee_id,))
        else:
            # Tutti i turni
            query = """
                SELECT s.ShiftID, s.Date, s.StartTime, s.EndTime,
                       e.EmployeeID, e.FirstName, e.LastName, e.Role
                FROM Shift s
                JOIN EmployeeShift es ON s.ShiftID = es.ShiftID
                JOIN Employee e ON es.EmployeeID = e.EmployeeID
                ORDER BY s.Date, s.StartTime
            """
            cursor.execute(query)

        shifts = cursor.fetchall()

        if not shifts:
            print("❌ Nessun turno trovato.")
            return

        print("\n📋 Elenco turni dei dipendenti:\n")
        for shift in shifts:
            print(f"🆔 Shift ID: {shift['ShiftID']}")
            print(f"👤 Dipendente: {shift['FirstName']} {shift['LastName']} "
                  f"(ID: {shift['EmployeeID']} | Ruolo: {shift['Role']})")
            print(f"📅 Data: {shift['Date']}")
            print(f"🕒 Orario: {shift['StartTime']} - {shift['EndTime']}")
            print("-" * 40)

    except mysql.connector.Error as err:
        print(f"❌ Errore database: {err}")
    finally:
        cursor.close()
        conn.close()


def main():
    """
    Funzione di avvio: chiede all'utente se vuole vedere tutti i turni
    o solo quelli di un dipendente specifico.
    """
    print("📆 Visualizzazione turni dipendenti\n")
    choice = input("Vuoi visualizzare i turni di (1) tutti o (2) un solo dipendente? ").strip()

    if choice == '1':
        show_shifts()
    elif choice == '2':
        try:
            emp_id = int(input("Inserisci l'ID del dipendente: ").strip())
            show_shifts(employee_id=emp_id)
        except ValueError:
            print("❌ L'ID deve essere un numero.")
    else:
        print("❌ Scelta non valida.")


# Esegui solo se lo script è chiamato direttamente
if __name__ == "__main__":
    main()

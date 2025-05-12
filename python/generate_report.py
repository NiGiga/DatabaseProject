import mysql.connector
from datetime import datetime

def get_connection():
    """
    Crea e restituisce una connessione al database.
    """
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="UR_PSW",
        database="RestaurantDB"
    )

def get_latest_date():
    """
    Recupera la data più recente in cui è stato registrato un pagamento
    basandosi sull'associazione con OrderRestaurant.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT MAX(r.Date)
        FROM CashRegister c
        JOIN OrderRestaurant o ON c.OrderID = o.OrderID
        JOIN Reservation r ON r.TableID = o.TableID AND r.EmployeeID = o.EmployeeID
    """)
    result = cursor.fetchone()[0]
    cursor.close()
    conn.close()

    if result:
        return result.strftime("%Y-%m-%d")  # ora sarà una data valida
    return None


def generate_report(start_date=None, end_date=None):
    """
    Genera un report sugli incassi e il numero di clienti in un intervallo di date.
    Se le date non sono specificate, usa l'ultimo giorno disponibile.
    """
    conn = get_connection()
    cursor = conn.cursor()

    try:
        if not end_date:
            end_date = get_latest_date()
            if not end_date:
                print("❌ Nessun dato disponibile nel database.")
                return
        if not start_date:
            start_date = end_date

        print(f"\n📆 Intervallo considerato: {start_date} ➡️ {end_date}")

        # Numero clienti confermati tra le date
        cursor.execute("""
            SELECT IFNULL(SUM(NumberOfGuests), 0)
            FROM Reservation
            WHERE Status = 'Confirmed'
              AND Date BETWEEN %s AND %s
        """, (start_date, end_date))
        total_customers = cursor.fetchone()[0]

        # Totale incassato tra le date
        cursor.execute("""
            SELECT IFNULL(SUM(TotalAmount), 0)
            FROM CashRegister cr
            JOIN OrderRestaurant o ON cr.OrderID = o.OrderID
            WHERE o.OrderTime BETWEEN %s AND %s
        """, (start_date + " 00:00:00", end_date + " 23:59:59"))
        total_revenue = cursor.fetchone()[0]

        # Stampa il report
        print("\n📈 REPORT RISTORANTE")
        print("-" * 40)
        print(f"👥 Clienti serviti: {total_customers}")
        print(f"💶 Incasso totale: €{total_revenue:.2f}")
        print("-" * 40)

    except mysql.connector.Error as err:
        print(f"❌ Errore nel database: {err}")
    finally:
        cursor.close()
        conn.close()

def main():
    print("📊 REPORT CLIENTI E INCASSI\n")
    print("Lascia vuoto per usare la data più recente disponibile.\n")

    # Input da utente (facoltativo)
    start_date = input("📅 Inserisci data inizio (YYYY-MM-DD): ").strip()
    end_date = input("📅 Inserisci data fine (YYYY-MM-DD): ").strip()

    # Validazione base formato
    try:
        if start_date:
            datetime.strptime(start_date, "%Y-%m-%d")
        else:
            start_date = None

        if end_date:
            datetime.strptime(end_date, "%Y-%m-%d")
        else:
            end_date = None
    except ValueError:
        print("❌ Formato data non valido. Usa YYYY-MM-DD.")
        return

    generate_report(start_date, end_date)

if __name__ == "__main__":
    main()


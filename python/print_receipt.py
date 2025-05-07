# Importa il modulo per la connessione al database MySQL
import mysql.connector

# Importa datetime per generare timestamp nella ricevuta
from datetime import datetime

# ------------------------------------------------------
# FUNZIONE: get_connection()
# Crea e restituisce una connessione al database MySQL
# ------------------------------------------------------
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",             # Utente del DB
        password="Pidosh1998@",  # Password del DB
        database="RestaurantDB"  # Nome del database da usare
    )

# -----------------------------------------------------------------
# FUNZIONE: fetch_reservations_by_field(field, value)
# Cerca prenotazioni confermate in base a un campo specifico (es. nome, email, ID)
# -----------------------------------------------------------------
def fetch_reservations_by_field(field, value):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = f"""
        SELECT ReservationID, CustomerName, Date, Time, Status, TableID
        FROM Reservation
        WHERE {field} LIKE %s AND Status = 'Confirmed'
    """
    # Se si cerca per campo testuale, usa LIKE con wildcard
    like_value = ('%' + value + '%') if field not in ('ReservationID', 'TableID') else value
    cursor.execute(query, (like_value,))
    results = cursor.fetchall()

    cursor.close()
    conn.close()
    return results

# --------------------------------------------------------------------
# FUNZIONE: fetch_reservations_by_table(table_id)
# Cerca tutte le prenotazioni confermate per uno specifico tavolo
# --------------------------------------------------------------------
def fetch_reservations_by_table(table_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT ReservationID, CustomerName, Date, Time, Status, TableID
        FROM Reservation
        WHERE TableID = %s AND Status = 'Confirmed'
    """
    cursor.execute(query, (table_id,))
    results = cursor.fetchall()

    cursor.close()
    conn.close()
    return results

# ---------------------------------------------------------------------
# FUNZIONE: fetch_receipt_items(table_id)
# Restituisce gli articoli ordinati da un tavolo, con quantità e subtotale
# ---------------------------------------------------------------------
def fetch_receipt_items(table_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT 
            mi.Name AS ItemName,                   -- Nome del piatto
            c.Quantity,                            -- Quantità ordinata
            mi.Price,                              -- Prezzo unitario
            (c.Quantity * mi.Price) AS Subtotal    -- Totale per riga
        FROM OrderRestaurant o
        JOIN Contains c ON o.OrderID = c.OrderID
        JOIN MenuItem mi ON c.ItemID = mi.ItemID
        WHERE o.TableID = %s
    """, (table_id,))
    items = cursor.fetchall()

    cursor.close()
    conn.close()
    return items

# -----------------------------------------------------
# FUNZIONE: print_receipt(reservation)
# Stampa a terminale una ricevuta dettagliata per la prenotazione data
# -----------------------------------------------------
def print_receipt(reservation):
    items = fetch_receipt_items(reservation["TableID"])
    total = sum(item["Subtotal"] for item in items)
    now = datetime.now()

    print("\n📄 RICEVUTA")
    print("-----------")
    print(f"🧾 Reservation ID: {reservation['ReservationID']}")
    print(f"👤 Cliente: {reservation['CustomerName']}")
    print(f"🪑 Tavolo: {reservation['TableID']}")
    print(f"🕒 Prenotazione: {reservation['Date']} alle {reservation['Time']}")
    print(f"🗓️ Stampato il: {now.strftime('%Y-%m-%d %H:%M:%S')}")
    print("-----------")
    print("🍽️ Ordini:")

    for item in items:
        print(f"- {item['ItemName']} x{item['Quantity']} @ €{item['Price']:.2f} = €{item['Subtotal']:.2f}")

    print("-----------")
    print(f"💰 TOTALE: €{total:.2f}")
    print("-----------")

# -----------------------------------------------------
# FUNZIONE PRINCIPALE: main()
# Interfaccia utente per cercare e stampare una ricevuta
# -----------------------------------------------------
def main():
    print("🧾 RICERCA PRENOTAZIONE PER RICEVUTA\n")

    # L’utente sceglie il criterio di ricerca
    mode = input("Cerca per (1) ID prenotazione, (2) Nome cliente, (3) Numero tavolo: ").strip()

    # Esegue la ricerca in base alla scelta
    if mode == '1':
        reservation_id = input("Inserisci ID prenotazione: ").strip()
        reservations = fetch_reservations_by_field("ReservationID", reservation_id)
    elif mode == '2':
        name = input("Inserisci nome cliente: ").strip()
        reservations = fetch_reservations_by_field("CustomerName", name)
    elif mode == '3':
        table_id = input("Inserisci numero tavolo: ").strip()
        reservations = fetch_reservations_by_table(table_id)
    else:
        print("❌ Opzione non valida.")
        return

    # Se nessuna prenotazione è trovata
    if not reservations:
        print("❌ Nessuna prenotazione attiva trovata.")
        return

    # Se ci sono più prenotazioni, chiedi all’utente quale stampare
    if len(reservations) > 1:
        print("\n🔎 Più prenotazioni trovate:")
        for idx, res in enumerate(reservations, 1):
            print(f"{idx}) ID: {res['ReservationID']} - Cliente: {res['CustomerName']} - Data: {res['Date']} - Ora: {res['Time']} - Tavolo: {res['TableID']}")
        sel = int(input("Seleziona il numero della prenotazione desiderata: "))
        reservation = reservations[sel - 1]
    else:
        reservation = reservations[0]

    # Stampa la ricevuta
    print_receipt(reservation)

# Punto di ingresso dello script
if __name__ == "__main__":
    main()

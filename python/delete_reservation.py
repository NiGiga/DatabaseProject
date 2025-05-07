# Importa il modulo per la connessione a MySQL
import mysql.connector

# ------------------------------------------------------------
# FUNZIONE: get_connection()
# Ritorna una connessione attiva al database RestaurantDB
# ------------------------------------------------------------
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Pidosh1998@",
        database="RestaurantDB"
    )

# ------------------------------------------------------------------
# FUNZIONE: find_reservations_by(field, value)
# Cerca le prenotazioni confermate in base a un campo specificato
# (es. ID, nome o email)
# ------------------------------------------------------------------
def find_reservations_by(field, value):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # Query dinamica che cerca per il campo specificato
    query = f"""
        SELECT * FROM Reservation
        WHERE {field} LIKE %s AND Status = 'Confirmed'
    """
    cursor.execute(query, (f"%{value}%",))  # Usa LIKE per trovare valori parziali
    results = cursor.fetchall()

    cursor.close()
    conn.close()
    return results

# ------------------------------------------------------------------
# FUNZIONE: delete_reservation()
# Consente all’utente di cercare e cancellare una prenotazione
# ------------------------------------------------------------------
def delete_reservation():
    print("🔍 Cerca prenotazione da cancellare:")
    print("1. Per ID")
    print("2. Per nome cliente")
    print("3. Per email cliente")
    choice = input("Scelta: ").strip()

    # Determina campo e valore di ricerca in base alla scelta
    if choice == '1':
        field = "ReservationID"
        value = input("Inserisci ID: ").strip()
    elif choice == '2':
        field = "CustomerName"
        value = input("Inserisci nome cliente: ").strip()
    elif choice == '3':
        field = "Email"
        value = input("Inserisci email cliente: ").strip()
    else:
        print("❌ Scelta non valida.")
        return

    # Cerca le prenotazioni corrispondenti
    reservations = find_reservations_by(field, value)

    if not reservations:
        print("❌ Nessuna prenotazione trovata.")
        return
    elif len(reservations) > 1:
        # Se ce ne sono più di una, l'utente sceglie quale cancellare
        print("\n🔎 Più prenotazioni trovate:")
        for idx, r in enumerate(reservations, 1):
            print(f"{idx}) ID: {r['ReservationID']} | Nome: {r['CustomerName']} | Data: {r['Date']} | Ora: {r['Time']} | Tavolo: {r['TableID']}")
        sel = int(input("Seleziona il numero della prenotazione da cancellare: "))
        res = reservations[sel - 1]
    else:
        res = reservations[0]  # Se ce n'è solo una, la seleziona direttamente

    # Mostra conferma prima della cancellazione
    print(f"\n🗑️ Conferma cancellazione prenotazione ID {res['ReservationID']} per {res['CustomerName']}")
    confirm = input("⚠️ Vuoi davvero cancellarla? (s/n): ").lower()
    if confirm != 's':
        print("❌ Operazione annullata.")
        return

    # Cancella la prenotazione dal database
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Reservation WHERE ReservationID = %s", (res['ReservationID'],))
    conn.commit()
    print("✅ Prenotazione cancellata.")

    cursor.close()
    conn.close()

# ------------------------------------------------------------
# AVVIO DEL PROGRAMMA
# ------------------------------------------------------------
if __name__ == "__main__":
    delete_reservation()

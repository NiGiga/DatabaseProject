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
        password="UR_PSW",
        database="RestaurantDB"
    )

# ----------------------------------------------------------------------------------
# FUNZIONE: print_available_tables(date_str, time_str)
# Mostra i tavoli liberi per una certa data e orario (±90 minuti)
# ----------------------------------------------------------------------------------
def print_available_tables(date_str, time_str):
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
    cursor.close()
    conn.close()

    print("\n📋 Tavoli disponibili a quell'ora:")
    for row in results:
        print(f"🪑 Tavolo ID: {row['TableID']} | Posti: {row['Seats']} | Posizione: {row['Location']}")
    if not results:
        print("❌ Nessun tavolo disponibile.")

# ----------------------------------------------------------------------------------
# FUNZIONE: find_reservations_by(field, value)
# Cerca prenotazioni confermate in base a un campo specifico (ID, nome o email)
# ----------------------------------------------------------------------------------
def find_reservations_by(field, value):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = f"""
        SELECT * FROM Reservation
        WHERE {field} LIKE %s AND Status = 'Confirmed'
    """
    cursor.execute(query, (f"%{value}%",))
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results

# ----------------------------------------------------------------------------------
# FUNZIONE PRINCIPALE: edit_reservation()
# Permette di modificare una prenotazione esistente, mantenendo i valori esistenti
# e verificando che il nuovo tavolo sia disponibile
# ----------------------------------------------------------------------------------
def edit_reservation():
    print("🔍 Cerca prenotazione da modificare:")
    print("1. Per ID")
    print("2. Per nome cliente")
    print("3. Per email cliente")
    choice = input("Scelta: ").strip()

    # Determina il campo e il valore di ricerca
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

    # Cerca la prenotazione in base al campo selezionato
    reservations = find_reservations_by(field, value)

    if not reservations:
        print("❌ Nessuna prenotazione trovata.")
        return
    elif len(reservations) > 1:
        # Se ci sono più risultati, chiedi all'utente quale vuole modificare
        print("\n🔎 Più prenotazioni trovate:")
        for idx, r in enumerate(reservations, 1):
            print(f"{idx}) ID: {r['ReservationID']} | Nome: {r['CustomerName']} | Data: {r['Date']} | Ora: {r['Time']} | Tavolo: {r['TableID']}")
        sel = int(input("Seleziona il numero della prenotazione da modificare: "))
        res = reservations[sel - 1]
    else:
        res = reservations[0]

    print(f"\n✏️ Modifica prenotazione ID {res['ReservationID']} per {res['CustomerName']}")

    # Input dei nuovi dati, se vuoti mantieni quelli esistenti
    new_name = input(f"Nome cliente [{res['CustomerName']}]: ").strip() or res['CustomerName']
    new_phone = input(f"Telefono [{res['CustomerPhone']}]: ").strip() or res['CustomerPhone']
    new_email = input(f"Email [{res['Email']}]: ").strip() or res['Email']
    new_date = input(f"Data [{res['Date']}]: ").strip() or str(res['Date'])
    new_time = input(f"Orario [{res['Time']}]: ").strip() or str(res['Time'])
    new_guests = input(f"Ospiti [{res['NumberOfGuests']}]: ").strip() or res['NumberOfGuests']
    new_table = input(f"Tavolo [{res['TableID']}]: ").strip() or res['TableID']

    # Converti ospiti e tavolo in interi, se possibile
    try:
        new_guests = int(new_guests)
        new_table = int(new_table)
    except ValueError:
        print("❌ Inserimento numerico non valido.")
        return

    # Controlla se il nuovo tavolo è disponibile per la nuova data e ora
    conn = get_connection()
    cursor = conn.cursor()

    check_query = """
        SELECT 1 FROM Reservation
        WHERE TableID = %s AND Date = %s AND ReservationID != %s
        AND ABS(TIMESTAMPDIFF(MINUTE, Time, %s)) < 90
        AND Status = 'Confirmed'
    """
    cursor.execute(check_query, (new_table, new_date, res['ReservationID'], new_time))
    if cursor.fetchone():
        print("❌ Tavolo non disponibile a quell’orario.")
        print_available_tables(new_date, new_time)
        return

    # Esegui l'aggiornamento della prenotazione
    update = """
        UPDATE Reservation
        SET CustomerName=%s, CustomerPhone=%s, Email=%s,
            Date=%s, Time=%s, NumberOfGuests=%s, TableID=%s
        WHERE ReservationID=%s
    """
    cursor.execute(update, (
        new_name, new_phone, new_email,
        new_date, new_time, new_guests, new_table, res['ReservationID']
    ))
    conn.commit()
    print("✅ Prenotazione modificata.")

    cursor.close()
    conn.close()

# ------------------------------------------------------------
# AVVIO DEL PROGRAMMA
# ------------------------------------------------------------
if __name__ == "__main__":
    edit_reservation()

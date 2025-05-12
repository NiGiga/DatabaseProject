# Importa i moduli necessari
import mysql.connector  # Per connettersi al database MySQL
from datetime import datetime  # Per lavorare con date e orari


# -------------------------------------------------------
# FUNZIONE: get_connection()
# Restituisce una connessione aperta al database MySQL
# -------------------------------------------------------
def get_connection():
    return mysql.connector.connect(
        host="localhost",  # Host locale
        user="root",  # Username MySQL
        password="UR_PSW@",  # Password MySQL
        database="RestaurantDB"  # Nome del database da usare
    )


# -------------------------------------------------------------------
# FUNZIONE: print_available_tables(date_str, time_str)
# Mostra i tavoli disponibili per una data e un orario specifici
# -------------------------------------------------------------------
def print_available_tables(date_str, time_str):
        # Connessione al database, inizio transizione
    conn = get_connection()
    conn.autocommit = False  # Disattiva autocommit
    cursor = conn.cursor(dictionary=True)

    # Query SQL: seleziona tutti i tavoli disponibili che NON hanno prenotazioni confermate entro ±90 minuti
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
    # Esegue la query con i parametri passati
    cursor.execute(query, (date_str, time_str))
    results = cursor.fetchall()

    # Chiude il cursore e la connessione
    cursor.close()
    conn.close()

    # Stampa i risultati trovati (se ce ne sono)
    print("\n📋 Tavoli disponibili a quell'ora:")
    for row in results:
        print(f"🪑 Tavolo ID: {row['TableID']} | Posti: {row['Seats']} | Posizione: {row['Location']}")
    if not results:
        print("❌ Nessun tavolo disponibile.")


# --------------------------------------------------------------------
# FUNZIONE: add_reservation()
# Permette all'utente di inserire una nuova prenotazione nel sistema
# --------------------------------------------------------------------
def add_reservation():
    # Input da parte dell'utente
    customer_name = input("Nome cliente: ")
    customer_phone = input("Telefono: ")
    email = input("Email: ")
    date_str = input("Data prenotazione (YYYY-MM-DD): ")
    time_str = input("Ora prenotazione (HH:MM): ")
    guests = int(input("Numero di ospiti: "))
    table_id = int(input("Numero tavolo: "))

    conn = get_connection()
    cursor = conn.cursor()

    try:
        # Controlla se il tavolo è già prenotato per quella data/ora
        check_query = """
            SELECT 1 FROM Reservation
            WHERE TableID = %s AND Date = %s
            AND ABS(TIMESTAMPDIFF(MINUTE, Time, %s)) < 90
            AND Status = 'Confirmed'
        """
        cursor.execute(check_query, (table_id, date_str, time_str))

        # Se il tavolo è occupato, mostra i tavoli liberi e interrompe
        if cursor.fetchone():
            print("❌ Tavolo occupato per quell'orario.")
            print_available_tables(date_str, time_str)
            return

        # Inserisce la nuova prenotazione nel database
        insert_query = """
            INSERT INTO Reservation (CustomerName, CustomerPhone, Email, Date, Time, NumberOfGuests, Status, TableID, EmployeeID)
            VALUES (%s, %s, %s, %s, %s, %s, 'Confirmed', %s, 3)
        """
        # ⚠️ EmployeeID impostato fisso a 3 (puoi modificarlo dinamicamente se necessario)
        cursor.execute(insert_query, (customer_name, customer_phone, email, date_str, time_str, guests, table_id))
        conn.commit()

        print("✅ Prenotazione aggiunta.")

    except Exception as e:
        # In caso di errore, stampa il messaggio
        print("❌ Errore:", e)

    finally:
        # Chiude connessione e cursore
        cursor.close()
        conn.close() # chiudo transizione e connessione


# -------------------------------
# AVVIO DEL PROGRAMMA
# -------------------------------
if __name__ == "__main__":
    add_reservation()

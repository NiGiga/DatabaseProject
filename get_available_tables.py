# Importa il modulo per connettersi al database MySQL
import mysql.connector

# Importa il modulo datetime per validare data e ora inserite
from datetime import datetime


# -------------------------------
# FUNZIONE: get_connection()
# Scopo: Stabilisce una connessione con il database RestaurantDB
# -------------------------------
def get_connection():
    return mysql.connector.connect(
        host="localhost",  # Indirizzo del server (localhost se locale)
        user="root",  # Nome utente per accedere al DB
        password="Pidosh1998@",  # Password utente MySQL
        database="RestaurantDB"  # Nome del database da utilizzare
    )


# -------------------------------------
# FUNZIONE: get_available_tables(date_str, time_str)
# Scopo: Restituisce i tavoli disponibili per una certa data e ora
# -------------------------------------
def get_available_tables(date_str, time_str):
    # Crea connessione al database
    conn = get_connection()
    cursor = conn.cursor()

    # Query SQL: seleziona tavoli disponibili che NON hanno prenotazioni confermate a quell'orario (±90 min)
    query = """
    SELECT t.TableID, t.Seats, t.Location
    FROM TableRestaurant t
    WHERE t.Status = 'Available'                         -- Il tavolo deve essere marcato come disponibile
    AND t.TableID NOT IN (
        SELECT r.TableID
        FROM Reservation r
        WHERE r.Date = %s                                -- Stessa data della richiesta
          AND ABS(TIMESTAMPDIFF(MINUTE, r.Time, %s)) < 90-- Controlla sovrapposizione entro 90 minuti
          AND r.Status = 'Confirmed'                     -- Solo le prenotazioni confermate occupano il tavolo
    );
    """

    # Esegue la query passando data e ora come parametri sicuri
    cursor.execute(query, (date_str, time_str))

    # Recupera i risultati (lista di tavoli disponibili)
    tables = cursor.fetchall()

    # Se ci sono tavoli disponibili, li stampa
    if tables:
        print(f"\n✅ Tavoli disponibili per {date_str} alle {time_str}:\n")
        for table in tables:
            print(f"🪑 Tavolo ID: {table[0]} | Posti: {table[1]} | Posizione: {table[2]}")
    else:
        print("\n⚠️ Nessun tavolo disponibile per la data e ora specificata.")

    # Chiude il cursore e la connessione
    cursor.close()
    conn.close()


# ------------------------------
# FUNZIONE PRINCIPALE
# Scopo: Chiede data e ora all’utente, valida il formato e mostra i tavoli liberi
# ------------------------------
def main():
    print("🔍 Controllo tavoli disponibili\n")

    # Input utente per data e ora
    date_input = input("Inserisci la data (YYYY-MM-DD): ").strip()
    time_input = input("Inserisci l'orario (HH:MM): ").strip()

    try:
        # Validazione formale di data e ora (per evitare crash)
        datetime.strptime(date_input, "%Y-%m-%d")
        datetime.strptime(time_input, "%H:%M")

        # Chiamata alla funzione che mostra i tavoli disponibili
        get_available_tables(date_input, time_input)

    except ValueError:
        # In caso di formato errato, stampa messaggio d’errore
        print("❌ Formato data o ora non valido. Riprova.")


# ------------------------------
# AVVIO DEL PROGRAMMA
# ------------------------------
if __name__ == "__main__":
    main()

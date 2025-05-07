import mysql.connector

# ------------------------------------------------------------
# FUNZIONE: get_connection()
# Scopo: crea e restituisce una connessione al database MySQL
# ------------------------------------------------------------
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Pidosh1998@",  # Modifica se usi credenziali diverse
        database="RestaurantDB"
    )

# ------------------------------------------------------------
# FUNZIONE: show_menu()
# Scopo: interroga la tabella MenuItem e stampa tutti gli item
#        del menù in modo formattato e leggibile
# ------------------------------------------------------------
def show_menu():
    # Ottieni connessione e cursore
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)  # Risultati come dizionari

    try:
        # Query SQL per ottenere tutte le voci del menù
        query = "SELECT ItemID, Name, Description, Price, Availability FROM MenuItem ORDER BY Name"
        cursor.execute(query)
        items = cursor.fetchall()  # Recupera tutti i risultati

        if not items:
            print("❌ Nessun item trovato nel menù.")
            return

        print("\n🍽️ MENU DEL RISTORANTE\n")

        # Ciclo sugli item per mostrarli uno a uno
        for item in items:
            print(f"🆔 ID: {item['ItemID']}")
            print(f"📛 Nome: {item['Name']}")
            print(f"📝 Descrizione: {item['Description']}")
            print(f"💶 Prezzo: €{item['Price']:.2f}")
            print(f"✅ Disponibilità: {'Disponibile' if item['Availability'] == 'Yes' else 'Non disponibile'}")
            print("-" * 50)

    except mysql.connector.Error as err:
        # Gestione errori SQL (connessione, query, ecc.)
        print(f"❌ Errore durante la lettura del menù: {err}")

    finally:
        # Chiude connessione e cursore, anche in caso di errore
        cursor.close()
        conn.close()

# ------------------------------------------------------------
# FUNZIONE PRINCIPALE
# Scopo: avvia la visualizzazione del menù
# ------------------------------------------------------------
def main():
    print("🔍 Visualizzazione del menù ristorante...\n")
    show_menu()

# Avvia il programma se eseguito direttamente
if __name__ == "__main__":
    main()

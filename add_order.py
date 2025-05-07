# Importa il modulo per connettersi a MySQL
import mysql.connector

# Importa datetime per generare automaticamente l'orario dell'ordine
from datetime import datetime

# --------------------------------------------------------
# FUNZIONE: get_connection()
# Ritorna una connessione aperta al database RestaurantDB
# --------------------------------------------------------
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Pidosh1998@",
        database="RestaurantDB"
    )

# --------------------------------------------------------
# FUNZIONE PRINCIPALE: add_order()
# Inserisce un nuovo ordine, i relativi piatti (con quantità)
# e aggiorna il totale dell’ordine in modo automatico.
# --------------------------------------------------------
def add_order():
    # Richiesta input all’utente: ID tavolo e ID cameriere
    table_id = input("🪑 Inserisci ID del tavolo: ").strip()
    employee_id = input("👤 Inserisci ID del cameriere: ").strip()

    # Connessione al database
    conn = get_connection()
    cursor = conn.cursor()

    try:
        # Ottiene l'orario attuale per registrare l'orario dell'ordine
        order_time = datetime.now().strftime("%H:%M:%S")

        # Inserisce un nuovo ordine nella tabella OrderRestaurant
        # L’importo totale (OrderAmount) verrà calcolato e aggiornato dopo
        insert_order = """
            INSERT INTO OrderRestaurant (TableID, EmployeeID, OrderTime, OrderAmount)
            VALUES (%s, %s, %s, 0)
        """
        cursor.execute(insert_order, (table_id, employee_id, order_time))

        # Recupera l'ID appena generato per l'ordine
        order_id = cursor.lastrowid
        print(f"\n🧾 Nuovo ordine ID {order_id} creato.")

        total = 0  # Variabile per accumulare il totale dell'ordine

        # Inserimento dei piatti (loop finché l’utente non preme invio senza inserire un ID)
        while True:
            item_id = input("\n🍽️ Inserisci ID del piatto (o premi invio per terminare): ").strip()
            if not item_id:
                break  # Esci dal ciclo se l’input è vuoto

            quantity = int(input("🔢 Inserisci quantità: "))

            # Recupera il prezzo del piatto da MenuItem
            cursor.execute("SELECT Price FROM MenuItem WHERE ItemID = %s", (item_id,))
            result = cursor.fetchone()

            if not result:
                print("❌ ID piatto non valido.")
                continue  # Salta all’iterazione successiva

            price = float(result[0])
            subtotal = price * quantity
            total += subtotal  # Accumula il totale

            # Inserisce il piatto ordinato nella tabella Contains
            cursor.execute(
                "INSERT INTO Contains (OrderID, ItemID, Quantity) VALUES (%s, %s, %s)",
                (order_id, item_id, quantity)
            )

            print(f"✅ Aggiunto: Item {item_id} x{quantity} (subtotale €{subtotal:.2f})")

        # Dopo aver inserito tutti i piatti, aggiorna OrderAmount con il totale calcolato
        cursor.execute(
            "UPDATE OrderRestaurant SET OrderAmount = %s WHERE OrderID = %s",
            (total, order_id)
        )

        # Salva tutte le modifiche nel database
        conn.commit()
        print(f"\n💰 Totale ordine aggiornato: €{total:.2f}")
        print("✅ Ordine completato con successo.")

    except Exception as e:
        # In caso di errore, annulla le modifiche e mostra il messaggio
        print("❌ Errore durante l'inserimento dell'ordine:", e)
        conn.rollback()

    finally:
        # Chiude cursor e connessione anche in caso di errore
        cursor.close()
        conn.close()

# --------------------------------------------------------
# AVVIO DEL PROGRAMMA
# --------------------------------------------------------
if __name__ == "__main__":
    add_order()

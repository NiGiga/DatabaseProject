import mysql.connector  
from datetime import datetime  
import tkinter as tk  # Libreria GUI per creare finestre e widget
from tkinter import messagebox  # Per mostrare messaggi pop-up

# Funzione per ottenere una connessione al database RestaurantDB
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="UR_PSW",  
        database="RestaurantDB"
    )

# Funzione che restituisce i piatti ordinati da un tavolo (con quantità, prezzo e subtotale)
def fetch_receipt_items(table_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)  # Risultati come dizionari (non tuple)

    # Query che recupera i piatti ordinati, le quantità e il subtotale per ciascun piatto
    cursor.execute("""
        SELECT 
            mi.Name AS ItemName,
            c.Quantity,
            mi.Price,
            (c.Quantity * mi.Price) AS Subtotal
        FROM OrderRestaurant o
        JOIN Contains c ON o.OrderID = c.OrderID
        JOIN MenuItem mi ON c.ItemID = mi.ItemID
        WHERE o.TableID = %s
    """, (table_id,))

    items = cursor.fetchall()  # Recupera tutti i risultati
    cursor.close()
    conn.close()
    return items  # Ritorna la lista di piatti

# Funzione che cerca prenotazioni in base a un campo (es. nome cliente) e valore
def fetch_reservations_by_field(field, value):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # Query dinamica che cerca prenotazioni confermate
    query = f"""
        SELECT ReservationID, CustomerName, Date, Time, Status, TableID
        FROM Reservation
        WHERE {field} LIKE %s AND Status = 'Confirmed'
    """

    # Usa LIKE per stringhe, oppure confronto diretto per ID numerici
    like_value = ('%' + value + '%') if field not in ('ReservationID', 'TableID') else value

    cursor.execute(query, (like_value,))
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results  # Ritorna lista di prenotazioni trovate

# Funzione che stampa una ricevuta in una finestra GUI (dato un campo e valore di ricerca)
def print_receipt_from_gui(field, value):
    reservations = fetch_reservations_by_field(field, value)

    # Se non ci sono prenotazioni → messaggio d’errore
    if not reservations:
        messagebox.showinfo("Nessuna prenotazione", "❌ Nessuna prenotazione trovata.")
        return

    # Se ci sono più prenotazioni simili → ambiguità
    if len(reservations) > 1:
        messagebox.showinfo("Errore", "Troppe prenotazioni trovate. Limita la ricerca.")
        return

    # Se c'è una sola prenotazione valida
    reservation = reservations[0]
    items = fetch_receipt_items(reservation["TableID"])  # Piatti ordinati da quel tavolo
    total = sum(item["Subtotal"] for item in items)  # Totale ordine
    now = datetime.now()  # Data e ora di stampa

    # Crea una nuova finestra con la ricevuta
    window = tk.Toplevel()
    window.title("📄 Ricevuta")
    window.geometry("450x500")

    # Area di testo per mostrare i contenuti della ricevuta
    receipt = tk.Text(window)
    receipt.pack(fill="both", expand=True)

    # Inserimento dei dati della ricevuta
    receipt.insert(tk.END, "\n📄 RICEVUTA\n")
    receipt.insert(tk.END, "-----------\n")
    receipt.insert(tk.END, f"🧾 Reservation ID: {reservation['ReservationID']}\n")
    receipt.insert(tk.END, f"👤 Cliente: {reservation['CustomerName']}\n")
    receipt.insert(tk.END, f"🪑 Tavolo: {reservation['TableID']}\n")
    receipt.insert(tk.END, f"🕒 Prenotazione: {reservation['Date']} alle {reservation['Time']}\n")
    receipt.insert(tk.END, f"🗓️ Stampato il: {now.strftime('%Y-%m-%d %H:%M:%S')}\n")
    receipt.insert(tk.END, "-----------\n")
    receipt.insert(tk.END, "🍽️ Ordini:\n")

    # Aggiunge ogni piatto alla ricevuta
    for item in items:
        receipt.insert(tk.END, f"- {item['ItemName']} x{item['Quantity']} @ €{item['Price']:.2f} = €{item['Subtotal']:.2f}\n")

    # Totale finale
    receipt.insert(tk.END, "-----------\n")
    receipt.insert(tk.END, f"💰 TOTALE: €{total:.2f}\n")
    receipt.insert(tk.END, "-----------\n")

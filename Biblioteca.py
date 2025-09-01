import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext
import sqlite3

def conectare_baza_date():
    """Conectează-te la baza de date SQLite."""
    conexiune = sqlite3.connect("biblioteca.db")
    cursor = conexiune.cursor()
    return conexiune, cursor

def creare_tabel():
    """Creează tabelul 'carti' dacă nu există."""
    conexiune, cursor = conectare_baza_date()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS carti (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titlu TEXT,
            autor TEXT,
            editura TEXT,
            an INTEGER
        )
    """)
    conexiune.commit()
    conexiune.close()

def adauga_carte(titlu, autor, editura, an):
    """Adaugă o carte nouă în baza de date."""
    conexiune, cursor = conectare_baza_date()
    cursor.execute("INSERT INTO carti (titlu, autor, editura, an) VALUES (?, ?, ?, ?)", (titlu, autor, editura, an))
    conexiune.commit()
    conexiune.close()

def vizualizare_carti():
    """Vizualizează toate cărțile din baza de date."""
    conexiune, cursor = conectare_baza_date()
    cursor.execute("SELECT * FROM carti")
    carti = cursor.fetchall()
    conexiune.close()
    if not carti:
        return "Nu există cărți în bibliotecă."
    else:
        rezultat = ""
        for carte in carti:
            rezultat += f"ID: {carte[0]}, Titlu: {carte[1]}, Autor: {carte[2]}, Editura: {carte[3]}, An: {carte[4]}\n"
        return rezultat

def cauta_carte(termen_cautare):
    """Caută cărți după titlu sau autor."""
    conexiune, cursor = conectare_baza_date()
    cursor.execute("SELECT * FROM carti WHERE titlu LIKE ? OR autor LIKE ?", ('%' + termen_cautare + '%', '%' + termen_cautare + '%'))
    carti = cursor.fetchall()
    conexiune.close()
    if not carti:
        return "Nu s-au găsit cărți."
    else:
        rezultat = ""
        for carte in carti:
            rezultat += f"ID: {carte[0]}, Titlu: {carte[1]}, Autor: {carte[2]}, Editura: {carte[3]}, An: {carte[4]}\n"
        return rezultat

def editeaza_carte(id_carte, titlu, autor, editura, an):
    """Editează informațiile unei cărți existente."""
    conexiune, cursor = conectare_baza_date()
    cursor.execute("UPDATE carti SET titlu = ?, autor = ?, editura = ?, an = ? WHERE id = ?", (titlu, autor, editura, an, id_carte))
    conexiune.commit()
    conexiune.close()

def sterge_carte(id_carte):
    """Șterge o carte din baza de date."""
    conexiune, cursor = conectare_baza_date()
    cursor.execute("DELETE FROM carti WHERE id = ?", (id_carte,))
    conexiune.commit()
    conexiune.close()

def adauga_carte_gui():
    titlu = titlu_entry.get()
    autor = autor_entry.get()
    editura = editura_entry.get()
    an = an_entry.get()
    adauga_carte(titlu, autor, editura, an)
    messagebox.showinfo("Succes", "Carte adăugată cu succes!")
    # Golim câmpurile
    titlu_entry.delete(0, tk.END)
    autor_entry.delete(0, tk.END)
    editura_entry.delete(0, tk.END)
    an_entry.delete(0, tk.END)

def vizualizare_carti_gui():
    rezultat = vizualizare_carti()
    afisare_text.delete(1.0, tk.END)
    afisare_text.insert(tk.END, rezultat)

def cauta_carte_gui():
    termen_cautare = simpledialog.askstring("Căutare", "Termen de căutare:")
    if termen_cautare:
        rezultat = cauta_carte(termen_cautare)
        afisare_text.delete(1.0, tk.END)
        afisare_text.insert(tk.END, rezultat)

def editeaza_carte_gui():
    id_carte = simpledialog.askinteger("Editare", "ID carte:")
    if id_carte:
        titlu = simpledialog.askstring("Editare", "Titlu nou:")
        autor = simpledialog.askstring("Editare", "Autor nou:")
        editura = simpledialog.askstring("Editare", "Editura nouă:")
        an = simpledialog.askinteger("Editare", "An nou:")
        editeaza_carte(id_carte, titlu, autor, editura, an)
        messagebox.showinfo("Succes", "Carte editată cu succes!")

def sterge_carte_gui():
    id_carte = simpledialog.askinteger("Ștergere", "ID carte:")
    if id_carte:
        sterge_carte(id_carte)
        messagebox.showinfo("Succes", "Carte ștearsă cu succes!")

# Interfața grafică
fereastra = tk.Tk()
fereastra.title("Biblioteca Personală")

# Etichete și câmpuri de intrare pentru adăugarea unei cărți
tk.Label(fereastra, text="Titlu:").grid(row=0, column=0)
titlu_entry = tk.Entry(fereastra)
titlu_entry.grid(row=0, column=1)

tk.Label(fereastra, text="Autor:").grid(row=1, column=0)
autor_entry = tk.Entry(fereastra)
autor_entry.grid(row=1, column=1)

tk.Label(fereastra, text="Editura:").grid(row=2, column=0)
editura_entry = tk.Entry(fereastra)
editura_entry.grid(row=2, column=1)

tk.Label(fereastra, text="An:").grid(row=3, column=0)
an_entry = tk.Entry(fereastra)
an_entry.grid(row=3, column=1)

# Butoane
tk.Button(fereastra, text="Adaugă carte", command=adauga_carte_gui).grid(row=4, column=0, columnspan=2, pady=10)
tk.Button(fereastra, text="Vizualizează cărți", command=vizualizare_carti_gui).grid(row=5, column=0, columnspan=2, pady=10)
tk.Button(fereastra, text="Caută carte", command=cauta_carte_gui).grid(row=6, column=0, columnspan=2, pady=10)
tk.Button(fereastra, text="Editează carte", command=editeaza_carte_gui).grid(row=7, column=0, columnspan=2, pady=10)
tk.Button(fereastra, text="Șterge carte", command=sterge_carte_gui).grid(row=8, column=0, columnspan=2, pady=10)

# Zona de afișare a rezultatelor
afisare_text = scrolledtext.ScrolledText(fereastra, width=50, height=10)
afisare_text.grid(row=9, column=0, columnspan=2, pady=10)

creare_tabel()
fereastra.mainloop()
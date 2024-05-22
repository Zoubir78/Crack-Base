import os
import cv2
import sqlite3
from sqlite3 import Error
import json
import base64
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog, StringVar
from PIL import Image, ImageTk
from datetime import datetime


def connect():
    # Créer une connexion à la base de données
    connection = sqlite3.connect("DB\\benfeld.db")
    print(f"Connected to the database {'benfeld.db'}")

    # Créer un curseur
    cursor = connection.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS images_benfeld (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            site TEXT NOT NULL,
            cote TEXT NOT NULL,  -- Nouvelle colonne pour le cote
            meteo TEXT NOT NULL,  -- Nouvelle colonne pour la meteo
            nom_image TEXT NOT NULL,
            image_json TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    ''')
    print("La table 'images_benfeld' a été créée avec succès.")

    # Créer une table 'json_data'
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS masques_benfeld (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data JSON NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    ''')
    print("La table 'masques_benfeld' a été créée avec succès.")

    # Save the changes
    connection.commit()

    return connection

def insert(conn, category, site, cote, meteo, nom_image, image_json, created_at=None, table="images"):
    # Insérer l'image dans la base de données
    try:
        if created_at is None:
            created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor = conn.cursor()
        cursor.execute(f'''
            INSERT INTO {table} (category, site, cote, meteo, nom_image, image_json, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (category, site, cote, meteo, nom_image, image_json, created_at))
        conn.commit()
    except sqlite3.Error as e:
        print(e)

def insert_json(conn, data, table="masques_benfeld"):
    try:
        created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor = conn.cursor()
        cursor.execute(f'''
            INSERT INTO {table} (data, created_at)
            VALUES (?, ?)
        ''', (json.dumps(data), created_at))
        conn.commit()
    except sqlite3.Error as e:
        print(e)

def select_site_details1(parent):
    top = tk.Toplevel(parent)
    top.title("Saisir les détails du site")

    site_var = StringVar()
    cote_var = StringVar()
    meteo_var = StringVar()

    ttk.Label(top, text="Veuillez entrer le nom du site :").pack(pady=5)
    site_entry = ttk.Entry(top, textvariable=site_var)
    site_entry.pack(pady=5)

    ttk.Label(top, text="Veuillez entrer le coté de prise :").pack(pady=5)
    cote_entry = ttk.Entry(top, textvariable=cote_var)
    cote_entry.pack(pady=5)

    ttk.Label(top, text="Veuillez entrer 'Cloudy' ou 'Sunny' :").pack(pady=5)
    meteo_entry = ttk.Entry(top, textvariable=meteo_var)
    meteo_entry.pack(pady=5)

    def confirm():
        site = site_var.get()
        cote = cote_var.get()
        meteo = meteo_var.get()
        if site and cote and meteo:
            top.destroy()

    confirm_button = ttk.Button(top, text="Confirmer", command=confirm)
    confirm_button.pack(pady=10)

    top.wait_window()  # Attendre que la fenêtre se ferme avant de continuer

    return site_var.get(), cote_var.get(), meteo_var.get()

def upload_images_benfeld(frame, category, table="images_benfeld"):
    conn = connect()

    site, cote, meteo = select_site_details1(frame.winfo_toplevel())  # Demander à l'utilisateur de saisir les détails

    if site and cote and meteo:
        root = tk.Tk()
        root.withdraw()
        folder_path = filedialog.askdirectory(title="Sélectionner un dossier avec des images")

        if folder_path:
            image_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f))]
            total_images = sum(1 for folder in image_files if os.path.isfile(os.path.join(folder, 'input.png')))
            frame.progress01['maximum'] = total_images

            for index, folder in enumerate(image_files):
                # Mettre à jour la barre de progression
                progress_percentage = (index + 1) / total_images * 100
                frame.progress01['value'] = progress_percentage
                frame.update()  # Mettre à jour l'interface graphique

                # Vérifier s'il y a un sous-dossier 'input.png'
                input_image_path = os.path.join(folder, 'input.png')
                if os.path.isfile(input_image_path):
                    # Importer l'image 'input.png'
                    with open(input_image_path, 'rb') as image_file:
                        image_bytes = image_file.read()
                    image_base64 = base64.b64encode(image_bytes).decode('utf-8')
                    image_json = {
                        "nom_image": 'input.png',
                        "image_base64": image_base64,
                        "cote": cote,
                        "meteo": meteo
                    }

                    # Insérer les données dans la table spécifiée avec le site, tube et sens choisis
                    insert(conn, category, site, cote, meteo, 'input.png', json.dumps(image_json), table=table)

                    # Afficher la progression actuelle dans la console
                    print(f"Progress: {progress_percentage}%")
                else:
                    print(f"Le dossier {folder} ne contient pas de fichier 'input.png'")

            # Assurez-vous que la barre de progression atteint 100% à la fin du traitement
            frame.progress01['value'] = 100
            frame.update()  # Mettre à jour l'interface graphique

            # Afficher un message de réussite
            messagebox.showinfo("Importation terminée", "Données importées avec succès!")

        conn.close()

def upload_masques_benfeld(frame, category):
    conn = connect()

    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(title="Select a JSON file", filetypes=[("JSON files", "*.json")], initialdir="export")

    if file_path:
        try:
            with open(file_path, 'r', encoding='utf-8') as json_file:
                data = json.load(json_file)
                table = "masques_benfeld"  # Vous pouvez adapter cela selon vos besoins

                insert_json(conn, data, table)

                messagebox.showinfo("Importation terminée", f"Le fichier {os.path.basename(file_path)} a été importé avec succès dans la base de données.")
        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur s'est produite lors de l'importation du fichier : {e}")
    
    conn.close()

def view_all(conn):
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM images')
        rows = cursor.fetchall()
        return rows
    except Error as e:
        print(e)
        return []

def view():
    try:
        connection = sqlite3.connect("DB\\benfeld.db")
        cursor = connection.cursor()
        # Utilisez une clause WHERE pour filtrer par catégorie
        cursor.execute("SELECT * FROM images_CC_C")
        data = cursor.fetchall()
        connection.close()
        return data if data else []  # Renvoyer les données ou une liste vide
    except sqlite3.Error as error:
        print("Error while connecting to SQLite", error)
        return None

def get_tables():
    try:
        connection = sqlite3.connect("DB\\benfeld.db")
        cursor = connection.cursor()
        # Récupérer la liste des tables dans la base de données
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        connection.close()
        return tables if tables else []  # Renvoyer les tables ou une liste vide
    except sqlite3.Error as error:
        print("Error while connecting to SQLite", error)
        return None
    

def display_image(image_path):
    image = cv2.imread(image_path)
    cv2.imshow('Image retrieved from the database', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def select_directory():
    root = tk.Tk()
    root.withdraw()
    directory = filedialog.askdirectory(title="Select Image Directory")
    return directory

def search(name=""):
    connection = sqlite3.connect("DB\\benfeld.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM images_CC_C WHERE Id = ?", (name,))
    output = cursor.fetchall()
    connection.close()
    return output

def delete(name):
    connection = sqlite3.connect("DB\\benfeld.db")
    cursor = connection.cursor()
    cursor.execute("DELETE FROM images_CC_C WHERE nom_image = ?", (name,))
    connection.commit()
    connection.close()


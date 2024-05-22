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
    # Create a connection to the database
    connection = sqlite3.connect("DB\\codebrim.db")
    print(f"Connected to the database {'codebrim.db'}")

    # Create a cursor
    cursor = connection.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS images_codebrim (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            site TEXT NOT NULL,
            type TEXT NOT NULL,  -- Nouvelle colonne pour le type
            nom_image TEXT NOT NULL,
            image_json TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    ''')
    print("Table 'images_codebrim' created successfully.")

    # Create the 'json_data' table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS masques_codebrim (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data JSON NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    ''')
    print("La table 'masques_codebrim' a été créée avec succès.")

    # Save the changes
    connection.commit()

    # Return the connection without closing the cursor here
    return connection

def insert(conn, category, site, type, nom_image, image_json, created_at=None, table="images"):
    # Insérer l'image dans la base de données
    try:
        if created_at is None:
            created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor = conn.cursor()
        cursor.execute(f'''
            INSERT INTO {table} (category, site, type, nom_image, image_json, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (category, site, type, nom_image, image_json, created_at))
        conn.commit()
    except sqlite3.Error as e:
        print(e)

def insert_json(conn, data, table="masques_codebrim"):
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

def select_site_details2(parent):
    top = tk.Toplevel(parent)
    top.title("Saisir les détails du site")

    site_var = StringVar()
    type_var = StringVar()

    ttk.Label(top, text="Veuillez entrer le nom du site :").pack(pady=5)
    site_entry = ttk.Entry(top, textvariable=site_var)
    site_entry.pack(pady=5)

    ttk.Label(top, text="Veuillez entrer le type de test :").pack(pady=5)
    type_entry = ttk.Entry(top, textvariable=type_var)
    type_entry.pack(pady=5)

    def confirm():
        site = site_var.get()
        type = type_var.get()
        if site and type:
            top.destroy()

    confirm_button = ttk.Button(top, text="Confirmer", command=confirm)
    confirm_button.pack(pady=10)

    top.wait_window()  # Attendre que la fenêtre se ferme avant de continuer

    return site_var.get(), type_var.get()

def upload_images_codebrim(frame, category, table="images_codebrim"):
    conn = connect()

    site, type = select_site_details2(frame.winfo_toplevel())  # Demander à l'utilisateur de saisir les détails

    if site and type:
        root = tk.Tk()
        root.withdraw()
        folder_path = filedialog.askdirectory(title="Sélectionner un dossier avec des images")

        if folder_path:
            image_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f))]
            total_images = sum(1 for folder in image_files if os.path.isfile(os.path.join(folder, 'input.png')))
            frame.progress02['maximum'] = total_images

            for index, folder in enumerate(image_files):
                # Mettre à jour la barre de progression
                progress_percentage = (index + 1) / total_images * 100
                frame.progress02['value'] = progress_percentage
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
                        "type": type
                    }

                    # Insérer les données dans la table spécifiée avec le site, tube et sens choisis
                    insert(conn, category, site, type, 'input.png', json.dumps(image_json), table=table)

                    # Afficher la progression actuelle dans la console
                    print(f"Progress: {progress_percentage}%")
                else:
                    print(f"Le dossier {folder} ne contient pas de fichier 'input.png'")

            # Assurez-vous que la barre de progression atteint 100% à la fin du traitement
            frame.progress02['value'] = 100
            frame.update()  # Mettre à jour l'interface graphique

            # Afficher un message de réussite
            messagebox.showinfo("Importation terminée", "Données importées avec succès!")

        conn.close()

def upload_masques_codebrim(frame, category):
    conn = connect()

    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(title="Select a JSON file", filetypes=[("JSON files", "*.json")], initialdir="export")

    if file_path:
        try:
            with open(file_path, 'r', encoding='utf-8') as json_file:
                data = json.load(json_file)
                table = "masques_codebrim"  # Vous pouvez adapter cela selon vos besoins

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


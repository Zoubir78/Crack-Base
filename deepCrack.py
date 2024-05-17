import os
import cv2
import sqlite3
from sqlite3 import Error
import json
import base64
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
from PIL import Image, ImageTk
from datetime import datetime


def connect():
    # Create a connection to the database
    connection = sqlite3.connect("DB\\deepCrack.db")
    print(f"Connected to the database {'deepCrack.db'}")

    # Create a cursor
    cursor = connection.cursor()

    # Créer la table 'test_img'
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS test_img (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            nom_image TEXT NOT NULL,
            image_json TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    ''')
    print("La table 'test_img' a été créée avec succès.")

    # Créer la table 'test_lab'
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS test_lab (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            nom_image TEXT NOT NULL,
            image_json TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    ''')
    print("La table 'test_lab' a été créée avec succès.")

    # Créer la table 'train_img'
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS train_img (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            nom_image TEXT NOT NULL,
            image_json TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    ''')
    print("La table 'train_img' a été créée avec succès.")

    # Créer la table 'train_lab'
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS train_lab (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            nom_image TEXT NOT NULL,
            image_json TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    ''')
    print("La table 'train_lab' a été créée avec succès.")

    # Save the changes
    connection.commit()

    # Return the connection without closing the cursor here
    return connection

def insert(conn, category, nom_image, image_json, table, created_at=None):
    # Insert the image into the specified table
    try:
        if created_at is None:
            created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        cursor = conn.cursor()
        cursor.execute(f'''
            INSERT INTO {table} (category, nom_image, image_json, created_at)
            VALUES (?, ?, ?, ?)
        ''', (category, nom_image, image_json, created_at))
        
        conn.commit()
    except Error as e:
        print(e)

def upload_images_deepCrack(category, tables):
    conn = connect()

    root = tk.Tk()
    root.withdraw()
    folder_path = filedialog.askdirectory(title="Select a folder with images")

    if folder_path:
        image_files = [f for f in os.listdir(folder_path) if f.endswith(('.jpg', '.png'))]

        # Mettre à jour le message sur le bouton
        messagebox.showinfo("Importation de données en cours", f"Patientez quelques secondes ...")

        for nom_image in image_files:
            image_path = os.path.join(folder_path, nom_image)

            # Open the image in binary mode
            with open(image_path, 'rb') as image_file:
                image_bytes = image_file.read()

            # Encode the image in base64
            image_base64 = base64.b64encode(image_bytes).decode('utf-8')

            # Create a JSON dictionary with image information
            image_json = {
                "nom_image": nom_image,
                "image_base64": image_base64
            }

            # Insert the image into each specified table
            for table in tables:
                print(f"Inserting into table: {table}")
                insert(conn, category, nom_image, json.dumps(image_json), table)

        # Mettre à jour le message sur le bouton après l'importation
        messagebox.showinfo("Importation de données terminée", f"Données importées avec succès!")

    conn.close()

def view_all(conn):
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM train_img')
        rows = cursor.fetchall()
        return rows
    except Error as e:
        print(e)
        return []

def view():
    try:
        connection = sqlite3.connect("DB\\deepCrack.db")
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
        connection = sqlite3.connect("DB\\deepCrack.db")
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
    connection = sqlite3.connect("DB\\deepCrack.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM images_CC_C WHERE Id = ?", (name,))
    output = cursor.fetchall()
    connection.close()
    return output

def delete(name):
    connection = sqlite3.connect("DB\\deepCrack.db")
    cursor = connection.cursor()
    cursor.execute("DELETE FROM images_CC_C WHERE nom_image = ?", (name,))
    connection.commit()
    connection.close()


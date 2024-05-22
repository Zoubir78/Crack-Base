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

def add_new_site():
    site_name = simpledialog.askstring("Nouveau site", "Entrez le nom du nouveau site:")
    if site_name:
        messagebox.showinfo("Site ajouté", f"Le site {site_name} a été ajouté avec succès.")
        # Ajoutez le code pour ajouter le nouveau site ici
    
def add_site_to_existing_database():
    response = messagebox.askyesno("Base de données existante", "Voulez-vous ajouter ce site à une base de données existante ?")
    if response:
        # Ajoutez le code pour obtenir la liste des bases de données existantes
        existing_databases = get_existing_databases()
        if existing_databases:
            # Afficher la liste des bases de données existantes et demander à l'utilisateur de choisir
            chosen_database = simpledialog.askstring("Choisir une Base de Données", "Choisissez une base de données existante:", initialvalue=existing_databases[0], listvalues=existing_databases)
            if chosen_database:
                # Ajoutez le code pour ajouter le site à la base de données existante choisie
                add_site_to_existing(chosen_database)
        else:
            messagebox.showinfo("Aucune Base de Données", "Aucune base de données existante n'a été trouvée.")
    else:
        # Ajoutez le code pour créer une nouvelle base de données
        create_new_database()

def get_existing_databases():

    pass

def add_site_to_existing(chosen_database):

    pass

def create_new_database():
   # Fonction pour créer une nouvelle base de données
    new_db_name = simpledialog.askstring("Nom de la Nouvelle Base de Données", "Entrez le nom de la nouvelle base de données:")
    if new_db_name:
        new_db_path = filedialog.asksaveasfilename(defaultextension=".db", filetypes=[("SQLite Database Files", "*.db")])

        if new_db_path:
            # Créer une connexion à la nouvelle base de données
            new_connection = sqlite3.connect(new_db_path)
            new_cursor = new_connection.cursor()

            # Enregistrez les modifications et fermez la connexion à la nouvelle base de données
            new_connection.commit()
            new_connection.close()

def create_table_in_database():
    # Fonction pour créer une nouvelle table dans la base de données existante
    db_path = filedialog.askopenfilename(defaultextension=".db", filetypes=[("SQLite Database Files", "*.db")])

    if db_path:
        # Créer une connexion à la base de données existante
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        # Demander le nom de la nouvelle table
        table_name = simpledialog.askstring("Nom de la Table", "Entrez le nom de la nouvelle table:")

        if table_name:
            # Demander les champs de la nouvelle table
            fields = simpledialog.askstring("Champs de la Table", "Entrez les champs de la nouvelle table (séparés par des virgules):")

            if fields:
                # Créer la nouvelle table
                create_table_query = f'''
                    CREATE TABLE IF NOT EXISTS {table_name} (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        {fields}
                    );
                '''
                cursor.execute(create_table_query)

                # Enregistrez les modifications et fermez la connexion à la base de données
                connection.commit()
                connection.close()

def add_data_to_database():
    # Fonction pour ajouter des données à la base de données
    db_path = filedialog.askopenfilename(defaultextension=".db", filetypes=[("SQLite Database Files", "*.db")])

    if db_path:
        # Créer une connexion à la base de données existante
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        # Demander à l'utilisateur les données à ajouter
        data_to_add = simpledialog.askstring("Ajouter des Données", "Entrez les données à ajouter (séparées par des virgules):")

        if data_to_add:
            # Diviser les données en une liste
            data_list = data_to_add.split(',')

            # Créer une requête d'insertion en fonction du nombre de données fournies
            placeholders = ', '.join(['?' for _ in data_list])
            insert_query = f'INSERT INTO votre_table ({", ".join(data_list)}) VALUES ({placeholders})'

            # Demander à l'utilisateur de confirmer l'ajout
            confirmation = messagebox.askyesno("Confirmation", f"Voulez-vous vraiment ajouter les données suivantes ?\n{data_list}")

            if confirmation:
                # Exécuter la requête d'insertion
                cursor.execute(insert_query, data_list)

                # Enregistrez les modifications et fermez la connexion à la base de données
                connection.commit()
                connection.close()

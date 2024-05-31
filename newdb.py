# -*- coding: utf-8 -*-
'''
Created on 2 avr. 2024
@author: Zoubeir Marouf
'''
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


def nouvelle_bdd(self):
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

def table_nouvelle_bdd(self):
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

def donnees_nouvelle_bdd(self):
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

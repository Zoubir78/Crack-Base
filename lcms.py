import os
import cv2
import sqlite3
import json
import base64
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, StringVar
from PIL import Image, ImageTk
from datetime import datetime

def connect():
    connection = sqlite3.connect("DB/lcms_database.db")
    print(f"Connecté à la base de données {'lcms_database.db'}")

    cursor = connection.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS images (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            site TEXT NOT NULL,
            tube TEXT NOT NULL,
            sens TEXT NOT NULL,
            hauteur INTEGER NOT NULL,
            angle INTEGER NOT NULL,
            nom_image TEXT NOT NULL,
            image_json TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    ''')
    print("Table 'images' créée avec succès.")

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS mat_files_img (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_name TEXT NOT NULL,
            file_data BLOB NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    ''')
    print("Table 'mat_files_img' créée avec succès.")

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS profondeur (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            site TEXT NOT NULL,
            tube TEXT NOT NULL,
            sens TEXT NOT NULL,
            hauteur INTEGER NOT NULL,
            angle INTEGER NOT NULL,
            nom_image TEXT NOT NULL,
            image_json TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    ''')
    print("Table 'profondeur' créée avec succès.")

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS mat_files_dep (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_name TEXT NOT NULL,
            file_data BLOB NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    ''')
    print("Table 'mat_files_dep' créée avec succès.")

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS masques (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data JSON NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    ''')
    print("Table 'masques' créée avec succès.")

    connection.commit()

    return connection

def insert(conn, category, site, tube, sens, hauteur, angle, nom_image, image_json, created_at=None, table="images"):
    try:
        if created_at is None:
            created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor = conn.cursor()
        cursor.execute(f'''
            INSERT INTO {table} (category, site, tube, sens, hauteur, angle, nom_image, image_json, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (category, site, tube, sens, hauteur, angle, nom_image, image_json, created_at))
        conn.commit()
    except sqlite3.Error as e:
        print(e)

def insert_json(conn, data, table="masques"):
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

def insert_mat(conn, file_name, file_data, table="mat_files"):
    try:
        created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor = conn.cursor()
        cursor.execute(f'''
            INSERT INTO {table} (file_name, file_data, created_at)
            VALUES (?, ?, ?)
        ''', (file_name, file_data, created_at))
        conn.commit()
    except sqlite3.Error as e:
        print(e)

def select_site_details(parent):
    top = tk.Toplevel(parent)
    top.title("Saisir les détails du site")

    site_var = StringVar()
    tube_var = StringVar()
    sens_var = StringVar()
    hauteur_var = StringVar()
    angle_var = StringVar()

    ttk.Label(top, text="Veuillez entrer le nom du site").pack(pady=5)
    site_entry = ttk.Entry(top, textvariable=site_var)
    site_entry.pack(pady=5)

    ttk.Label(top, text="Veuillez entrer le tube").pack(pady=5)
    tube_entry = ttk.Entry(top, textvariable=tube_var)
    tube_entry.pack(pady=5)

    ttk.Label(top, text="Veuillez entrer le sens de prise").pack(pady=5)
    sens_entry = ttk.Entry(top, textvariable=sens_var)
    sens_entry.pack(pady=5)

    ttk.Label(top, text="Veuillez entrer la hauteur (mm)").pack(pady=5)
    hauteur_entry = ttk.Entry(top, textvariable=hauteur_var)
    hauteur_entry.pack(pady=5)

    ttk.Label(top, text="Veuillez entrer l'angle (°)").pack(pady=5)
    angle_entry = ttk.Entry(top, textvariable=angle_var)
    angle_entry.pack(pady=5)

    def confirm():
        site = site_var.get()
        tube = tube_var.get()
        sens = sens_var.get()
        hauteur = hauteur_var.get()
        angle = angle_var.get()
        if site and tube and sens and hauteur and angle:
            top.destroy()
            return site, tube, sens, int(hauteur), int(angle)

    confirm_button = ttk.Button(top, text="Confirmer", command=confirm)
    confirm_button.pack(pady=10)

    top.wait_window()  # Attendre que la fenêtre se ferme avant de continuer

    return site_var.get(), tube_var.get(), sens_var.get(), hauteur_var.get(), angle_var.get()

def upload_lcms(frame, category, table="images"):
    conn = connect()
    
    site, tube, sens, hauteur, angle = select_site_details(frame.winfo_toplevel())  # Demander à l'utilisateur de saisir les détails

    if site and tube and sens and hauteur and angle:
        root = tk.Tk()
        root.withdraw()
        folder_path = filedialog.askdirectory(title="Select a folder with images")

        if folder_path:
            image_files = [f for f in os.listdir(folder_path) if f.endswith(('.jpg', '.png'))]
            total_images = len(image_files)
            frame.progress1['maximum'] = total_images

            for index, nom_image in enumerate(image_files):
                # Importer chaque image
                image_path = os.path.join(folder_path, nom_image)
                with open(image_path, 'rb') as image_file:
                    image_bytes = image_file.read()
                image_base64 = base64.b64encode(image_bytes).decode('utf-8')
                image_json = {
                    "nom_image": nom_image,
                    "image_base64": image_base64,
                    "tube": tube,
                    "sens": sens,
                    "hauteur": hauteur,
                    "angle": angle
                }

                # Insérer les données dans la table spécifiée avec le site, tube et sens choisis
                insert(conn, category, site, tube, sens, hauteur, angle, nom_image, json.dumps(image_json), table=table)

                # Afficher la progression actuelle dans la console
                print(f"Progress: {index + 1}/{total_images} - Imported: {nom_image}")

                # Mettre à jour la barre de progression après chaque importation de fichier
                progress_percentage = (index + 1) / total_images * 100
                frame.progress1['value'] = progress_percentage
                frame.update()  # Mettre à jour l'interface graphique

            # Assurez-vous que la barre de progression atteint 100% à la fin du traitement
            frame.progress1['value'] = 100
            frame.update()  # Mettre à jour l'interface graphique

            messagebox.showinfo("Importation terminée", f"{total_images} fichiers ont été importés avec succès dans la base de données.")

    conn.close()

def upload_lcms_mat(frame, category, table="mat_files_img"):
    conn = connect()

    root = tk.Tk()
    root.withdraw()
    folder_path = filedialog.askdirectory(title="Select a folder with Matlab files", initialdir="export")

    if folder_path:
        mat_files = [f for f in os.listdir(folder_path) if f.endswith('.mat')]
        total_files = len(mat_files)

        for index, file_name in enumerate(mat_files):
            file_path = os.path.join(folder_path, file_name)
            try:
                with open(file_path, 'rb') as mat_file:  # Ouvrir le fichier en mode binaire
                    file_data = mat_file.read()

                    insert_mat(conn, file_name, file_data, table)

                    # Afficher la progression actuelle dans la console
                    print(f"Progress: {index + 1}/{total_files} - Imported: {file_name}")

            except Exception as e:
                messagebox.showerror("Erreur", f"Une erreur s'est produite lors de l'importation du fichier {file_name} : {e}")

            # Mettre à jour la barre de progression après chaque importation de fichier
            progress_percentage = (index + 1) / total_files * 100
            frame.progress1['value'] = progress_percentage
            frame.update()  # Mettre à jour l'interface graphique

        # Assurez-vous que la barre de progression atteint 100% à la fin du traitement
        frame.progress1['value'] = 100
        frame.update()  # Mettre à jour l'interface graphique

        messagebox.showinfo("Importation terminée", f"{total_files} fichiers ont été importés avec succès dans la base de données.")

    conn.close()


def upload_depths(frame, category, table="profondeur"):
    conn = connect()
    
    site, tube, sens, hauteur, angle = select_site_details(frame.winfo_toplevel())  # Demander à l'utilisateur de saisir les détails

    if site and tube and sens and hauteur and angle:
        root = tk.Tk()
        root.withdraw()
        folder_path = filedialog.askdirectory(title="Select a folder with images")

        if folder_path:
            image_files = [f for f in os.listdir(folder_path) if f.endswith(('.jpg', '.png'))]
            total_images = len(image_files)
            frame.progress1['maximum'] = total_images

            for index, nom_image in enumerate(image_files):
                # Importer chaque image
                image_path = os.path.join(folder_path, nom_image)
                with open(image_path, 'rb') as image_file:
                    image_bytes = image_file.read()
                image_base64 = base64.b64encode(image_bytes).decode('utf-8')
                image_json = {
                    "nom_image": nom_image,
                    "image_base64": image_base64,
                    "tube": tube,
                    "sens": sens,
                    "hauteur": hauteur,
                    "angle": angle
                }

                # Insérer les données dans la table spécifiée avec le site, tube et sens choisis
                insert(conn, category, site, tube, sens, hauteur, angle, nom_image, json.dumps(image_json), table=table)

                # Afficher la progression actuelle dans la console
                print(f"Progress: {index + 1}/{total_images} - Imported: {nom_image}")

                # Mettre à jour la barre de progression après chaque importation de fichier
                progress_percentage = (index + 1) / total_images * 100
                frame.progress2['value'] = progress_percentage
                frame.update()  # Mettre à jour l'interface graphique

            # Assurez-vous que la barre de progression atteint 100% à la fin du traitement
            frame.progress2['value'] = 100
            frame.update()  # Mettre à jour l'interface graphique

            messagebox.showinfo("Importation terminée", f"{total_images} fichiers ont été importés avec succès dans la base de données.")

    conn.close()

def upload_depths_mat(frame, category, table="mat_files_dep"):
    conn = connect()

    root = tk.Tk()
    root.withdraw()
    folder_path = filedialog.askdirectory(title="Select a folder with Matlab files", initialdir="export")

    if folder_path:
        mat_files = [f for f in os.listdir(folder_path) if f.endswith('.mat')]
        total_files = len(mat_files)

        for index, file_name in enumerate(mat_files):
            file_path = os.path.join(folder_path, file_name)
            try:
                with open(file_path, 'rb') as mat_file:  # Ouvrir le fichier en mode binaire
                    file_data = mat_file.read()

                    insert_mat(conn, file_name, file_data, table)

                    # Afficher la progression actuelle dans la console
                    print(f"Progress: {index + 1}/{total_files} - Imported: {file_name}")

            except Exception as e:
                messagebox.showerror("Erreur", f"Une erreur s'est produite lors de l'importation du fichier {file_name} : {e}")

            # Mettre à jour la barre de progression après chaque importation de fichier
            progress_percentage = (index + 1) / total_files * 100
            frame.progress2['value'] = progress_percentage
            frame.update()  # Mettre à jour l'interface graphique

        # Assurez-vous que la barre de progression atteint 100% à la fin du traitement
        frame.progress2['value'] = 100
        frame.update()  # Mettre à jour l'interface graphique

        messagebox.showinfo("Importation terminée", f"{total_files} fichiers ont été importés avec succès dans la base de données.")

    conn.close()

def upload_masques(frame, category):
    conn = connect()

    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(title="Select a JSON file", filetypes=[("JSON files", "*.json")], initialdir="export")

    if file_path:
        try:
            with open(file_path, 'r', encoding='utf-8') as json_file:
                data = json.load(json_file)
                table = "masques"  # Vous pouvez adapter cela selon vos besoins

                insert_json(conn, data, table)

                messagebox.showinfo("Importation terminée", f"Le fichier {os.path.basename(file_path)} a été importé avec succès dans la base de données.")
        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur s'est produite lors de l'importation du fichier : {e}")
    
    conn.close()

def view():
    try:
        connection = sqlite3.connect("DB/lcms_database.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM images")
        data = cursor.fetchall()

        list_window = tk.Toplevel()
        list_window.title("Liste des entrées")
        list_window.geometry("800x600")

        tree = ttk.Treeview(list_window, columns=("category", "site", "tube", "sens", "nom_image", "image_json", "created_at"), show='headings')
        tree.heading("category", text="Category")
        tree.heading("site", text="Site")
        tree.heading("tube", text="Tube")
        tree.heading("sens", text="Sens")
        tree.heading("nom_image", text="Nom Image")
        tree.heading("image_json", text="Image JSON")
        tree.heading("created_at", text="Créé à")

        for row in data:
            tree.insert("", tk.END, values=row[1:])  # Ignore l'ID (row[0])

        tree.pack(expand=True, fill=tk.BOTH)

        connection.close()

    except sqlite3.Error as e:
        print(f"Une erreur s'est produite : {e}")
        messagebox.showerror("Erreur", f"Une erreur s'est produite lors de la visualisation des données : {e}")

def get_tables():
    try:
        connection = sqlite3.connect("DB/lcms_database.db")
        cursor = connection.cursor()
        # Récupérer la liste des tables dans la base de données
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        connection.close()
        return tables if tables else []  # Renvoyer les tables ou une liste vide
    except sqlite3.Error as error:
        print("Error while connecting to SQLite", error)
        return None

def view_all_data(self):
    try:
        connection = sqlite3.connect("DB/lcms_database.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM images")
        data = cursor.fetchall()
        connection.close()
        self.display_data(data)
    except sqlite3.Error as e:
        print(f"Une erreur s'est produite : {e}")
        messagebox.showerror("Erreur", f"Une erreur s'est produite lors de la visualisation des données : {e}")

def view_other_table_data(self, table_name):
    try:
        connection = sqlite3.connect("DB/lcms_database.db")
        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM {table_name}")
        data = cursor.fetchall()
        connection.close()
        self.display_data(data)
    except sqlite3.Error as e:
        print(f"Une erreur s'est produite : {e}")
        messagebox.showerror("Erreur", f"Une erreur s'est produite lors de la visualisation des données : {e}")

def search(self, name):
    connection = sqlite3.connect("DB/lcms_database.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM images WHERE nom_image LIKE ?", (f"%{name}%",))
    output = cursor.fetchall()
    connection.close()
    return output

def delete_data(self, name):
    connection = sqlite3.connect("DB/lcms_database.db")
    cursor = connection.cursor()
    cursor.execute("DELETE FROM images WHERE nom_image = ?", (name,))
    connection.commit()
    connection.close()

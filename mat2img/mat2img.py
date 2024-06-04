import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import scipy.io
import numpy as np
import matplotlib.pyplot as plt
import json

def load_mat_file():
    filename = filedialog.askopenfilename(title="Sélectionner un fichier MATLAB", filetypes=(("Fichiers MATLAB", "*.mat"), ("Tous les fichiers", "*.*")))
    if filename:
        mat_file = scipy.io.loadmat(filename)
        print("Clés disponibles dans le fichier .mat:", mat_file.keys())
        return mat_file, filename
    return None, None

def generate_image(mat_file):
    if mat_file:
        image_data = mat_file['A']
        if len(image_data.shape) == 2:
            plt.imshow(image_data, cmap='gray')
        elif len(image_data.shape) == 3:
            plt.imshow(image_data)
        
        # Définir les dimensions de la figure en pixels
        dpi = 100  # Points par pouce
        width, height = 500, 2080  # Dimensions de l'image en pixels
        figsize = width / dpi, height / dpi  # Taille de la figure en pouces
        plt.gcf().set_size_inches(figsize)
        
        plt.axis('off')
        plt.savefig('LcmsData_000002.png', dpi=dpi, bbox_inches='tight', pad_inches=0)
        print("L'image a été convertie et sauvegardée dans LcmsData_000002.png")

def export_json(mat_file, filename):
    if mat_file and filename:
        data_dict = {}
        for key in mat_file:
            # Ignorer les clés spéciales '__header__', '__version__', '__globals__'
            if not key.startswith('__'):
                data_dict[key] = mat_file[key].tolist()
        with open(filename.replace('.mat', '.json'), 'w') as json_file:
            json.dump(data_dict, json_file)
        print("Les données ont été exportées en format JSON dans le fichier correspondant")

# Créer la fenêtre principale
root = tk.Tk()
root.title("Outil de conversion de données MATLAB")
root.geometry("400x150")

# Style sombre pour ttk
style = ttk.Style(root)
root.tk.call("source", "azure.tcl")
root.tk.call("set_theme", "dark")

# Variables globales pour stocker mat_file et filename
mat_file = None
filename = None

# Fonction pour charger un fichier .mat
def load_and_generate():
    global mat_file, filename
    mat_file, filename = load_mat_file()
    if mat_file:
        generate_image(mat_file)

# Bouton pour charger un fichier .mat et générer l'image
load_button = ttk.Button(root, text="Charger un fichier MATLAB et générer l'image", command=load_and_generate)
load_button.pack(pady=10)

# Bouton pour exporter les données en format JSON
export_json_button = ttk.Button(root, text="Exporter les données JSON", command=lambda: export_json(mat_file, filename))
export_json_button.pack(pady=10)

# Exécuter la boucle principale
root.mainloop()

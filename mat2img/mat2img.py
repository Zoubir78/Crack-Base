import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import scipy.io
import numpy as np
import matplotlib.pyplot as plt
import json
import os

def load_mat_files():
    directory = filedialog.askdirectory(title="Sélectionner un dossier contenant les fichiers MATLAB")
    if directory:
        mat_files = []
        for filename in os.listdir(directory):
            if filename.endswith(".mat"):
                mat_file_path = os.path.join(directory, filename)
                mat_file = scipy.io.loadmat(mat_file_path)
                print("Clés disponibles dans le fichier", filename, ":", mat_file.keys())  # Ajout de cette ligne
                mat_files.append((mat_file, mat_file_path))
        if mat_files:
            return mat_files, directory
    return None, None

def generate_images(mat_files, output_dir):
    if mat_files:
        for mat_file, filename in mat_files:
            image_key = None
            for key in mat_file:
                if isinstance(mat_file[key], np.ndarray):
                    if len(mat_file[key].shape) in [2, 3]:
                        image_key = key
                        break
            
            if image_key:
                image_data = mat_file[image_key]
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
                output_filename = os.path.join(output_dir, f'{os.path.splitext(os.path.basename(filename))[0]}.png')
                plt.savefig(output_filename, dpi=dpi, bbox_inches='tight', pad_inches=0)
                print(f"L'image a été convertie et sauvegardée dans {output_filename}")
            else:
                print(f"Erreur: Aucune clé d'image trouvée dans le fichier {filename}")

#def export_jsons(mat_files, output_dir):
#    if mat_files and output_dir:
#        for mat_file, filename in mat_files:
#            data_dict = {}
#            for key in mat_file:
#                # Ignorer les clés spéciales '__header__', '__version__', '__globals__'
#                if not key.startswith('__'):
#                    data_dict[key] = mat_file[key].tolist()
#            json_filename = os.path.join(output_dir, f'{os.path.splitext(os.path.basename(filename))[0]}.json')
#            with open(json_filename, 'w') as json_file:
#                json.dump(data_dict, json_file)
#            print(f"Les données ont été exportées en format JSON dans {json_filename}")

# Créer la fenêtre principale
root = tk.Tk()
root.title("Outil de conversion de données MATLAB")
root.geometry("400x150")

# Style sombre pour ttk
style = ttk.Style(root)
root.tk.call("source", "azure.tcl")
root.tk.call("set_theme", "dark")

# Variables globales pour stocker mat_files et output_dir
mat_files = None
output_dir = None

# Fonction pour charger un dossier de fichiers .mat et générer les images
def load_and_generate():
    global mat_files, output_dir
    mat_files, output_dir = load_mat_files()
    if mat_files and output_dir:
        generate_images(mat_files, output_dir)
        #export_jsons(mat_files, output_dir)

# Bouton pour charger un dossier de fichiers .mat et générer les images
load_button = ttk.Button(root, text="Charger des fichiers MATLAB et générer les images", command=load_and_generate)
load_button.pack(pady=10)

# Exécuter la boucle principale
root.mainloop()

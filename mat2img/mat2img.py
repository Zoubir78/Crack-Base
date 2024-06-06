# -*- coding: utf-8 -*-
'''
Created on 1 juin 2024
@author: Zoubeir Marouf
'''
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import scipy.io
import numpy as np
import matplotlib.pyplot as plt
import json
import os
import sys
import subprocess
from multiprocessing import Pool, cpu_count

class RedirectText:
    def __init__(self, text_widget):
        self.output = text_widget

    def write(self, string):
        self.output.insert(tk.END, string)
        self.output.see(tk.END)
        self.output.update_idletasks()

    def flush(self):
        pass  # Not used but required by file-like interface

def load_mat_files():
    directory = filedialog.askdirectory(title="Sélectionner un dossier contenant les fichiers MATLAB")
    if directory:
        mat_files = []
        for filename in os.listdir(directory):
            if filename.endswith(".mat"):
                mat_file_path = os.path.join(directory, filename)
                mat_file = scipy.io.loadmat(mat_file_path)
                print("Clés disponibles dans le fichier", filename, ":", mat_file.keys())
                mat_files.append((mat_file, mat_file_path))
        if mat_files:
            return mat_files, directory
    return None, None

def save_image(data):
    mat_file, filename, output_dir = data
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
        width, height = 782, 2702  # Dimensions de l'image en pixels
        figsize = width / dpi, height / dpi  # Taille de la figure en pouces
        plt.gcf().set_size_inches(figsize)
        
        plt.axis('off')
        output_filename = os.path.join(output_dir, f'{os.path.splitext(os.path.basename(filename))[0]}.png')
        plt.savefig(output_filename, dpi=dpi, bbox_inches='tight', pad_inches=0)
        plt.close()
        print(f"L'image a été convertie et sauvegardée dans {output_filename}")
    else:
        print(f"Erreur: Aucune clé d'image trouvée dans le fichier {filename}")

def generate_images(mat_files, output_dir):
    if mat_files:
        # Utiliser multiprocessing pour paralléliser la génération des images
        with Pool(processes=cpu_count()) as pool:
            pool.map(save_image, [(mat_file, filename, output_dir) for mat_file, filename in mat_files])
        plt.close('all')  # Fermer toutes les figures ouvertes une fois que les images sont générées

def run_mat2img():
    chemin = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mat2img", "mat2img.py")
    process = subprocess.Popen(["python", chemin], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    def read_output():
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                print(output.strip())
            error = process.stderr.readline()
            if error:
                print(error.strip(), file=sys.stderr)
    
    root.after(100, read_output)

# Créer la fenêtre principale
root = tk.Tk()
root.title("Outil de conversion de données MATLAB")
root.geometry("700x600")

# Style sombre pour ttk
style = ttk.Style(root)
root.tk.call("source", "azure.tcl")
root.tk.call("set_theme", "dark")

# Zone de texte pour afficher la sortie du terminal
terminal_text = tk.Text(root, wrap="word", height=20)
terminal_text.pack(expand=True, fill="both")

# Rediriger stdout et stderr vers le widget Text
stdout_redirect = RedirectText(terminal_text)
stderr_redirect = RedirectText(terminal_text)
sys.stdout = stdout_redirect
sys.stderr = stderr_redirect

# Variables globales pour stocker mat_files et output_dir
mat_files = None
output_dir = None

# Fonction pour charger un dossier de fichiers .mat et générer les images
def load_and_generate():
    global mat_files, output_dir
    mat_files, output_dir = load_mat_files()
    if mat_files and output_dir:
        generate_images(mat_files, output_dir)
        run_mat2img()

# Bouton pour charger un dossier de fichiers .mat et générer les images
load_button = ttk.Button(root, text="Charger des fichiers MATLAB et générer les images", command=load_and_generate)
load_button.pack(pady=10)

# Exécuter la boucle principale
root.mainloop()

# Réinitialiser stdout et stderr à leurs valeurs par défaut
sys.stdout = sys.__stdout__
sys.stderr = sys.__stderr__





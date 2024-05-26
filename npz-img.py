# -*- coding: utf-8 -*-
'''
Created on 2 avr. 2024
@author: Zoubeir Marouf
'''
import tkinter as tk
from tkinter import filedialog, messagebox
import os
import numpy as np
import cv2
from tkinter import ttk
import threading

class NPZToImageConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("Convertisseur NPZ - Image")

        # Créer un bouton pour charger le dossier contenant les fichiers .npz
        self.load_button = tk.Button(root, text="Charger un dossier 'Depths'", command=self.load_input_directory)
        self.load_button.pack(pady=10)

        # Créer un bouton pour choisir le dossier de sortie
        self.output_button = tk.Button(root, text="Choisir un dossier de Sortie", command=self.choose_output_directory)
        self.output_button.pack(pady=5)

        # Créer un bouton pour lancer la conversion
        self.convert_button = tk.Button(root, text="Convertir", command=self.convert_npz_to_images)
        self.convert_button.pack(pady=10)

        # Initialiser la barre de progression
        self.progress_bar = ttk.Progressbar(root, orient='horizontal', length=200, mode='determinate')
        self.progress_bar.pack(pady=5)

        # Créer un label pour afficher le pourcentage de conversion en temps réel
        self.progress_label = tk.Label(root, text="")
        self.progress_label.pack(pady=5)

        # Créer un label pour afficher le statut de conversion
        self.status_label = tk.Label(root, text="")
        self.status_label.pack(pady=5)

        self.input_dir = ""
        self.output_dir = ""

    def load_input_directory(self):
        self.input_dir = filedialog.askdirectory()
        if not self.input_dir:
            return

        #messagebox.showinfo("Dossier d'Entrée", f"Dossier d'Entrée sélectionné : {self.input_dir}")

    def choose_output_directory(self):
        self.output_dir = filedialog.askdirectory()
        if not self.output_dir:
            return

        #messagebox.showinfo("Dossier de Sortie", f"Dossier de Sortie sélectionné : {self.output_dir}")

    def convert_npz_to_images(self):
        if not self.input_dir or not self.output_dir:
            messagebox.showerror("Erreur", "Veuillez sélectionner à la fois le dossier d'entrée et le dossier de sortie.")
            return

        try:
            file_list = [file_name for file_name in os.listdir(self.input_dir) if file_name.endswith('.npz')]
            total_files = len(file_list)

            self.progress_bar['maximum'] = total_files  # Définir le maximum de la barre de progression
            self.progress_bar['value'] = 0  # Réinitialiser la valeur de la barre de progression
            self.status_label.config(text="Conversion en cours...")  # Mettre à jour le statut de conversion

            threading.Thread(target=self.convert_files, args=(file_list,)).start()  # Démarrer le thread de conversion
        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur s'est produite : {str(e)}")

    def convert_files(self, file_list):
        count = 0
        for file_name in file_list:
            file_path = os.path.join(self.input_dir, file_name)
            data = np.load(file_path)  # Charger les données du fichier .npz

            for key, image in data.items():
                image_name = f"{file_name}_{key}.png"  # Nom de l'image à enregistrer
                image_path = os.path.join(self.output_dir, image_name)
                cv2.imwrite(image_path, image)  # Convertir et enregistrer l'image

            count += 1  # Incrémenter le compteur de fichiers convertis

            # Mettre à jour la barre de progression et le statut de conversion
            percentage = (count / len(file_list)) * 100
            self.progress_bar['value'] = count
            self.status_label.config(text=f"Conversion en cours... {int(percentage)}%")
            self.root.update_idletasks()

        # Afficher "Conversion terminée" une fois la conversion terminée
        self.status_label.config(text="Conversion terminée")

# Créer une fenêtre principale
root = tk.Tk()
app = NPZToImageConverter(root)
root.mainloop()

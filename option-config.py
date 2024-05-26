# -*- coding: utf-8 -*-
'''
Created on 2 avr. 2024
@author: Zoubeir Marouf
'''
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import ast
import re  # Importer le module re pour les expressions régulières

class ConfigModifierApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Configuration Modifier")
        self.root.geometry("800x400")

        # Variables pour stocker les options et leurs valeurs
        self.options = {}
        self.option_vars = {}

        # Créer un champ d'entrée pour spécifier le chemin vers le fichier de configuration
        self.config_path_label = tk.Label(root, text="Chemin vers le Fichier de Configuration :")
        self.config_path_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.config_path_entry = tk.Entry(root)
        self.config_path_entry.grid(row=0, column=1, padx=5, pady=5, sticky="we")

        # Créer un bouton pour parcourir et sélectionner le fichier de configuration
        self.browse_button = tk.Button(root, text="Parcourir", command=self.browse_config)
        self.browse_button.grid(row=0, column=2, padx=5, pady=5, sticky="e")

        # Frame pour afficher les options et leurs valeurs
        self.options_frame = ttk.LabelFrame(root, text="Options à Modifier")
        self.options_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

        # Créer un bouton pour appliquer les modifications
        self.apply_button = tk.Button(root, text="Sauvegarder les Modifications", command=self.apply_changes)
        self.apply_button.grid(row=0, column=3, padx=5, pady=5, sticky="e")

        # Créer un bouton pour réinitialiser les valeurs par défaut
        self.reset_button = tk.Button(root, text="Réinitialiser les Valeurs par Défaut", command=self.reset_defaults)
        self.reset_button.grid(row=1, column=3, padx=5, pady=5, sticky="e")

        # Créer un label pour afficher les messages d'état
        self.status_label = tk.Label(root, text="", fg="green")
        self.status_label.grid(row=2, column=0, columnspan=4, padx=5, pady=5, sticky="nsew")

        # Configurer le système de grille pour redimensionner les colonnes et les lignes
        root.columnconfigure(1, weight=1)
        root.rowconfigure(1, weight=1)

    def browse_config(self):
        # Ouvrir une boîte de dialogue pour parcourir et sélectionner le fichier de configuration
        file_path = filedialog.askopenfilename(filetypes=[("Python files", "*.py")])
        self.config_path_entry.delete(0, tk.END)
        self.config_path_entry.insert(0, file_path)

        # Analyser le fichier de configuration pour extraire les options et leurs valeurs
        self.parse_config(file_path)

    def parse_config(self, file_path):
        self.options = {}

        with open(file_path, 'r') as f:
            # Lire chaque ligne du fichier
            for line in f:
                # Supprimer les espaces et les caractères de nouvelle ligne
                line = line.strip()

                # Ignorer les lignes vides ou celles qui sont des commentaires
                if not line or line.startswith("#"):
                    continue

                # Vérifier si la ligne contient une assignation de variable
                if "=" in line:
                    # Séparer la ligne en nom d'option et valeur
                    option, value = line.split("=", 1)

                    # Ajouter l'option et sa valeur à notre dictionnaire
                    option = option.strip()
                    value = value.strip()
                    self.options[option] = value

        # Afficher les options dans la frame
        self.show_options()

    def show_options(self):
        # Nettoyer la frame pour afficher les nouvelles options
        for widget in self.options_frame.winfo_children():
            widget.destroy()

        # Déterminer le nombre de colonnes en fonction du nombre d'options
        num_options = len(self.options)
        num_columns = 3
        options_per_column = (num_options + num_columns - 1) // num_columns  # Arrondi supérieur

        # Créer des champs d'entrée pour chaque option
        for i, (option, value) in enumerate(self.options.items()):
            # Calculer la position de la colonne et de la ligne en fonction de l'indice de l'option
            col = i % num_columns
            row = i // num_columns

            # Label pour afficher le nom de l'option
            label = tk.Label(self.options_frame, text=option)
            label.grid(row=row, column=col*2, padx=5, pady=5, sticky="w")

            # Champ d'entrée pour modifier la valeur de l'option
            entry_var = tk.StringVar(value=value)
            entry = tk.Entry(self.options_frame, textvariable=entry_var, width=20)
            entry.grid(row=row, column=col*2 + 1, padx=5, pady=5, sticky="w")

            # Ajouter la variable d'option à notre dictionnaire pour y accéder plus tard
            self.option_vars[option] = entry_var

    def apply_changes(self):
        config_path = self.config_path_entry.get()

        if not config_path:
            messagebox.showerror("Erreur", "Veuillez spécifier le chemin du fichier de configuration.")
            return

        # Mettre à jour les valeurs des options avec celles saisies par l'utilisateur
        for option, var in self.option_vars.items():
            self.options[option] = var.get()

        # Lire le contenu du fichier de configuration
        with open(config_path, 'r') as f:
            content = f.read()

        # Modifier le contenu du fichier avec les nouvelles valeurs d'options
        for option, value in self.options.items():
            # Utiliser une expression régulière pour trouver et remplacer la valeur de l'option dans le contenu
            content = re.sub(rf"^\s*{re.escape(option)}\s*=\s*.*$", f"{option} = {value}", content, flags=re.MULTILINE)

        # Écrire les modifications dans le fichier de configuration
        with open(config_path, 'w') as f:
            f.write(content)

        # Mettre à jour l'affichage des options après avoir écrit dans le fichier
        self.parse_config(config_path)

        self.status_label.config(text="Modifications sauvegardées avec succès !", fg="green")


    def reset_defaults(self):
        # Remettre les valeurs par défaut pour toutes les options
        for option, var in self.option_vars.items():
            default_value = self.get_default_value(option)
            var.set(default_value)

    def get_default_value(self, option):
        # Définir les valeurs par défaut pour chaque option (à adapter selon votre besoin)
        default_values = {
            "lr": "1e-3",
            "momentum": "0.9",
            "weight_decay": "1e-4",
            # Ajouter d'autres options avec leurs valeurs par défaut
        }

        return default_values.get(option, "")

# Créer une fenêtre principale
root = tk.Tk()
app = ConfigModifierApp(root)
root.mainloop()

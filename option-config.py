# -*- coding: utf-8 -*-
'''
Created on 2 avr. 2024
@author: Zoubeir Marouf
'''
import tkinter as tk
from tkinter import messagebox, ttk
import re
import logging
import os
import json
import requests

# Configuration du système de log
log_directory = "logs"
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

# Créer un handler pour écrire les logs dans un fichier avec l'encodage UTF-8
file_handler = logging.FileHandler(os.path.join(log_directory, 'options_config.log'), encoding='utf-8')
file_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# Configurer le logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(file_handler)

# Charger les données JSON
def load_json(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            if not data:
                raise ValueError("Le fichier JSON est vide")
            return data
    except json.JSONDecodeError as e:
        raise ValueError(f"Erreur de chargement du fichier JSON: {e}")

file_path = r'C:\Users\z.marouf-araibi\Desktop\Crack-Base\models\models_json.json'
try:
    models_data = load_json(file_path)
    #print("Chargement réussi:", models_data)
except ValueError as e:
    #print(e)
    messagebox.showerror("Erreur", str(e))
    exit(1)

# Vérifiez si les données ont été chargées correctement
if not models_data:
    #print("Le fichier JSON est vide ou contient des données non valides.")
    messagebox.showerror("Erreur", "Le fichier JSON est vide ou contient des données non valides.")
    exit(1)

class ConfigModifierApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Configuration")
        self.root.geometry("410x600")

        # Style sombre pour ttk
        style = ttk.Style(self.root)
        self.root.tk.call("source", "azure.tcl")
        self.root.tk.call("set_theme", "dark")

        # Variables pour stocker les options et leurs valeurs
        self.options = {}
        self.option_vars = {}

        # Entry pour le chemin du fichier de config
        self.config_path_entry = tk.Entry(root)
        self.config_path_entry.insert(0, r"C:\Users\z.marouf-araibi\Desktop\Crack-Base\mmdetection\configs\my_custom\my_custom_config.py")
        self.config_path_entry.grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

        # Frame pour afficher les options et leurs valeurs
        self.options_frame = ttk.LabelFrame(root, text="Options à modifier")
        self.options_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

        # Créer un bouton pour réinitialiser les valeurs par défaut
        self.reset_button = tk.Button(root, text="Réinitialiser les valeurs par défaut", command=self.reset_defaults)
        self.reset_button.grid(row=2, column=0, padx=5, pady=5, sticky="w")

        # Créer un bouton pour sauvegarder les modifications
        self.save_button = tk.Button(root, text="Sauvegarder les modifications", command=self.apply_changes)
        self.save_button.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        # Créer un label pour afficher les messages d'état
        self.status_label = tk.Label(root, text="", fg="green")
        self.status_label.grid(row=3, column=0, columnspan=3, padx=5, pady=5, sticky="nsew")

        # Ajouter une liste déroulante pour sélectionner le modèle
        label = tk.Label(root, text="Choisir un modèle:")
        label.grid(row=4, column=0, padx=10, pady=10, sticky="w")

        model_names = [model["Model Name"] for model in models_data]
        self.combo = ttk.Combobox(root, values=model_names)
        self.combo.grid(row=4, column=1, padx=10, pady=10, sticky="w")
        self.combo.current(0)  # Sélectionne le premier élément par défaut

        # Ajouter une barre de progression
        self.progress_bar = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
        self.progress_bar.grid(row=5, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

        # Ajouter un label pour le pourcentage
        self.percentage = tk.StringVar()
        self.percentage_label = tk.Label(root, textvariable=self.percentage)
        self.percentage_label.grid(row=6, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

        # Ajouter un bouton pour lancer le téléchargement
        self.download_button = tk.Button(root, text="Télécharger", command=self.download_checkpoint)
        self.download_button.grid(row=7, column=0, columnspan=3, padx=10, pady=20, sticky="nsew")

        # Ajouter une liste déroulante pour les fichiers de checkpoint
        #checkpoint_label = tk.Label(root, text="Choisir un checkpoint:")
        #checkpoint_label.grid(row=8, column=0, padx=10, pady=10, sticky="w")

        #self.checkpoint_combo = ttk.Combobox(root, values=self.get_checkpoints())
        #self.checkpoint_combo.grid(row=8, column=1, padx=10, pady=10, sticky="w")

        # Configurer le système de grille pour redimensionner les colonnes et les lignes
        root.columnconfigure(1, weight=1)
        root.rowconfigure(1, weight=1)

        # Analyser le fichier de configuration pour extraire les options et leurs valeurs
        self.parse_config(self.config_path_entry.get())
        logger.info("Application démarrée et fichier de configuration analysé.")

    def get_checkpoints(self):
        checkpoint_dir = r'C:\Users\z.marouf-araibi\Desktop\Crack-Base\mmdetection\checkpoints'
        checkpoints = [f for f in os.listdir(checkpoint_dir) if f.endswith('.pth') or f.endswith('.pt')]
        return checkpoints

    def parse_config(self, file_path):
        self.options = {
            "model_type": "MaskRCNN",
            "backbone_type": "ResNet",
            "checkpoint": "resnet152-394f9c45.pth",
            "checkpoint_dir": 'C:/Users/z.marouf-araibi/Desktop/Crack-Base/mmdetection/checkpoints/',
            "loss_cls_weight": 1.0,
            "loss_bbox_weight": 1.0,
            "max_epochs": 12
        }

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            model_type_match = re.search(r"model\s*=\s*dict\s*\(.*type\s*=\s*'(\w+)'", content, re.DOTALL)
            if model_type_match:
                self.options["model_type"] = model_type_match.group(1)

            backbone_type_match = re.search(r"backbone\s*=\s*dict\s*\(.*type\s*=\s*'(\w+)'", content, re.DOTALL)
            if backbone_type_match:
                self.options["backbone_type"] = backbone_type_match.group(1)

            load_from_match = re.search(r"load_from\s*=\s*'([\w:/\\]+)'", content, re.DOTALL)
            if load_from_match:
                checkpoint_path = load_from_match.group(1)
                self.options["checkpoint"] = os.path.basename(checkpoint_path)
                self.options["checkpoint_dir"] = os.path.dirname(checkpoint_path)

            loss_cls_weight_match = re.search(r"loss_cls\s*=\s*dict\s*\(.*loss_weight\s*=\s*([\d.]+)", content, re.DOTALL)
            if loss_cls_weight_match:
                self.options["loss_cls_weight"] = float(loss_cls_weight_match.group(1))

            loss_bbox_weight_match = re.search(r"loss_bbox\s*=\s*dict\s*\(.*loss_weight\s*=\s*([\d.]+)", content, re.DOTALL)
            if loss_bbox_weight_match:
                self.options["loss_bbox_weight"] = float(loss_bbox_weight_match.group(1))

            max_epochs_match = re.search(r"runner\s*=\s*dict\s*\(.*max_epochs\s*=\s*(\d+)", content, re.DOTALL)
            if max_epochs_match:
                self.options["max_epochs"] = int(max_epochs_match.group(1))

            logger.info(f"Options extraites du fichier de configuration : {self.options}")

        except FileNotFoundError:
            logger.error(f"Le fichier de configuration {file_path} n'a pas été trouvé.")
            messagebox.showerror("Erreur", "Le fichier de configuration n'a pas été trouvé.")
        except Exception as e:
            logger.error(f"Une erreur s'est produite lors de l'analyse du fichier de configuration : {e}")
            messagebox.showerror("Erreur", f"Une erreur s'est produite lors de l'analyse du fichier de configuration : {e}")

        # Afficher les options dans la frame
        self.show_options()

    def show_options(self):
        # Nettoyer la frame pour afficher les nouvelles options
        for widget in self.options_frame.winfo_children():
            widget.destroy()

        # Model type
        model_label = tk.Label(self.options_frame, text="Model Type")
        model_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        model_var = tk.StringVar(value=self.options["model_type"])
        model_names = [model["Model Name"] for model in models_data]  # Obtenez les noms de modèles depuis models_data
        model_menu = ttk.Combobox(self.options_frame, textvariable=model_var, values=model_names)
        model_menu.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        self.option_vars["model_type"] = model_var

        # Backbone type
        backbone_label = tk.Label(self.options_frame, text="Backbone Type")
        backbone_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        backbone_var = tk.StringVar(value=self.options["backbone_type"])
        backbone_menu = ttk.Combobox(self.options_frame, textvariable=backbone_var, values=["ResNet", "EfficientNet", "HRNet"])
        backbone_menu.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        self.option_vars["backbone_type"] = backbone_var

        # Checkpoint
        checkpoint_label = tk.Label(self.options_frame, text="Checkpoint")
        checkpoint_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        checkpoint_var = tk.StringVar(value=self.options["checkpoint"])
        checkpoint_entry = ttk.Combobox(self.options_frame, width=35, textvariable=checkpoint_var, values=self.get_checkpoints())
        checkpoint_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        self.option_vars["checkpoint"] = checkpoint_var

        # Loss class weight
        loss_cls_weight_label = tk.Label(self.options_frame, text="Loss Class Weight")
        loss_cls_weight_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")
        loss_cls_weight_var = tk.DoubleVar(value=self.options["loss_cls_weight"])
        loss_cls_weight_spinbox = tk.Spinbox(self.options_frame, from_=0.0, to=10.0, increment=0.1, textvariable=loss_cls_weight_var)
        loss_cls_weight_spinbox.grid(row=3, column=1, padx=5, pady=5, sticky="w")
        self.option_vars["loss_cls_weight"] = loss_cls_weight_var

        # Loss bbox weight
        loss_bbox_weight_label = tk.Label(self.options_frame, text="Loss BBox Weight")
        loss_bbox_weight_label.grid(row=4, column=0, padx=5, pady=5, sticky="w")
        loss_bbox_weight_var = tk.DoubleVar(value=self.options["loss_bbox_weight"])
        loss_bbox_weight_spinbox = tk.Spinbox(self.options_frame, from_=0.0, to=10.0, increment=0.1, textvariable=loss_bbox_weight_var)
        loss_bbox_weight_spinbox.grid(row=4, column=1, padx=5, pady=5, sticky="w")
        self.option_vars["loss_bbox_weight"] = loss_bbox_weight_var

        # Max epochs
        max_epochs_label = tk.Label(self.options_frame, text="Max Epochs")
        max_epochs_label.grid(row=5, column=0, padx=5, pady=5, sticky="w")
        max_epochs_var = tk.IntVar(value=self.options["max_epochs"])
        max_epochs_spinbox = tk.Spinbox(self.options_frame, from_=1, to=150, textvariable=max_epochs_var)
        max_epochs_spinbox.grid(row=5, column=1, padx=5, pady=5, sticky="w")
        self.option_vars["max_epochs"] = max_epochs_var

    def save_config(self, file_path):
        try:
            # Mettre à jour les options avec les nouvelles valeurs des variables
            for key, var in self.option_vars.items():
                self.options[key] = var.get()

            # Construire le chemin complet du checkpoint
            checkpoint_name = self.options["checkpoint"]
            checkpoint_dir = self.options.get('checkpoint_dir', 'C:/Users/z.marouf-araibi/Desktop/Crack-Base/mmdetection/checkpoints/')
            full_checkpoint_path = os.path.join(checkpoint_dir, checkpoint_name)

            # Lire le contenu actuel du fichier de configuration
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            # Ouvrir le fichier en mode écriture pour appliquer les modifications
            with open(file_path, 'w', encoding='utf-8') as f:
                for line in lines:
                    if re.search(r"model\s*=\s*dict\s*\(.*type\s*=\s*'(\w+)'", line, re.DOTALL):
                        line = re.sub(r"type\s*=\s*'\w+'", f"type = '{self.options['model_type']}'", line)
                    elif re.search(r"backbone\s*=\s*dict\s*\(.*type\s*=\s*'(\w+)'", line, re.DOTALL):
                        line = re.sub(r"type\s*=\s*'\w+'", f"type = '{self.options['backbone_type']}'", line)
                    elif re.search(r"load_from\s*=\s*'[\w:/\\]+'", line, re.DOTALL):
                        line = re.sub(r"load_from\s*=\s*'[\w:/\\]+'", f"load_from = '{full_checkpoint_path}'", line)
                    elif re.search(r"runner\s*=\s*dict\s*\(.*max_epochs\s*=\s*(\d+)", line, re.DOTALL):
                        line = re.sub(r"max_epochs\s*=\s*\d+", f"max_epochs = {self.options['max_epochs']}", line)
                    elif re.search(r"loss_cls\s*=\s*dict\s*\(.*loss_weight\s*=\s*([\d.]+)", line, re.DOTALL):
                        line = re.sub(r"loss_weight\s*=\s*[\d.]+", f"loss_weight = {self.options['loss_cls_weight']}", line)
                    elif re.search(r"loss_bbox\s*=\s*dict\s*\(.*loss_weight\s*=\s*([\d.]+)", line, re.DOTALL):
                        line = re.sub(r"loss_weight\s*=\s*[\d.]+", f"loss_weight = {self.options['loss_bbox_weight']}", line)

                    f.write(line)

            self.status_label.config(text="Modifications appliquées avec succès!", fg="green")
            logger.info(f"Modifications sauvegardées dans le fichier {file_path}.")
            logger.info(f"Nouvelles valeurs des options : {self.options}")

        except Exception as e:
            logger.error(f"Une erreur s'est produite lors de l'application des modifications : {e}")
            messagebox.showerror("Erreur", f"Une erreur s'est produite lors de l'application des modifications: {e}")

    def apply_changes(self):
        config_path = self.config_path_entry.get()
        self.save_config(config_path)

    def reset_defaults(self):
        default_values = {
            "model_type": "MaskRCNN",
            "backbone_type": "ResNet",
            "checkpoint": "resnet152-394f9c45.pth",
            "max_epochs": 12,
            "loss_cls_weight": 1.0,
            "loss_bbox_weight": 1.0
        }

        for key, var in self.option_vars.items():
            var.set(default_values[key])

        self.status_label.config(text="Valeurs réinitialisées par défaut!", fg="green")
        logger.info("Valeurs réinitialisées par défaut.")
        logger.info(f"Valeurs réinitialisées à : {default_values}")

    def download_checkpoint(self):
        selected_model = self.combo.get()
        for model in models_data:
            if model["Model Name"] == selected_model:
                url = model["Checkpoint_link"]
                # Définir le répertoire de destination
                download_dir = r'C:\Users\z.marouf-araibi\Desktop\Crack-Base\mmdetection\checkpoints'
                # Extraire le nom du fichier à partir de l'URL
                filename = url.split("/")[-1]
                # Créer le chemin complet pour le fichier de destination
                file_path = os.path.join(download_dir, filename)

                try:
                    response = requests.get(url, stream=True)
                    response.raise_for_status()

                    total_size = int(response.headers.get('content-length', 0))
                    block_size = 1024  # 1 Kilobyte
                    downloaded_size = 0  # initialize counter

                    with open(file_path, 'wb') as f:
                        for chunk in response.iter_content(chunk_size=block_size):
                            if chunk:
                                f.write(chunk)
                                downloaded_size += len(chunk)
                                progress_value = (downloaded_size / total_size) * 100
                                self.progress_bar["value"] = progress_value
                                self.percentage.set(f"{progress_value:.0f}%")
                                self.root.update_idletasks()

                    self.status_label.config(text="Téléchargement terminé.", fg="green")
                    logger.info("Le fichier de poids a été téléchargé avec succès.")
                except Exception as e:
                    self.status_label.config(text=f"Erreur lors du téléchargement : {e}", fg="red")
                    logger.error(f"Erreur lors du téléchargement du fichier de poids : {e}")
                    
if __name__ == "__main__":
    root = tk.Tk()
    app = ConfigModifierApp(root)
    root.mainloop()

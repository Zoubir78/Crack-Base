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
        self.config_path_entry.insert(0, r"C:\Users\z.marouf-araibi\Desktop\dlta-ai\DLTA_AI_app\mmdetection\configs\my_custom\my_custom_config.py")

        # Frame pour afficher les options et leurs valeurs
        self.options_frame = ttk.LabelFrame(root, text="Options à modifier")
        self.options_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

        # Créer un bouton pour réinitialiser les valeurs par défaut
        self.reset_button = tk.Button(root, text="Réinitialiser les valeurs par défaut", command=self.reset_defaults)
        self.reset_button.grid(row=2, column=0, padx=5, pady=5, sticky="w")

        # Créer un bouton pour sauvegarder les modifications
        self.save_button = tk.Button(root, text="Sauvegarder les modifications", command=self.save_changes)
        self.save_button.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        # Créer un label pour afficher les messages d'état
        self.status_label = tk.Label(root, text="", fg="green")
        self.status_label.grid(row=3, column=0, columnspan=4, padx=5, pady=5, sticky="nsew")

        # Configurer le système de grille pour redimensionner les colonnes et les lignes
        root.columnconfigure(1, weight=1)
        root.rowconfigure(1, weight=1)

        # Analyser le fichier de configuration pour extraire les options et leurs valeurs
        self.parse_config(self.config_path_entry.get())
        logger.info("Application démarrée et fichier de configuration analysé.")

    def parse_config(self, file_path):
        self.options = {
            "model_type": "MaskRCNN",
            "backbone_type": "ResNet",
            "checkpoint": "torchvision://resnet18",      
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

            checkpoint_match = re.search(r"init_cfg\s*=\s*dict\s*\(.*checkpoint\s*=\s*'([\w:/]+)'", content, re.DOTALL)
            if checkpoint_match:
                self.options["checkpoint"] = checkpoint_match.group(1)

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
        model_menu = ttk.Combobox(self.options_frame, textvariable=model_var, values=["MaskRCNN", "cascade_MaskRCNN", "FasterRCNN"])
        model_menu.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        self.option_vars["model_type"] = model_var

        # Backbone type
        backbone_label = tk.Label(self.options_frame, text="Backbone Type")
        backbone_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        backbone_var = tk.StringVar(value=self.options["backbone_type"])
        backbone_menu = ttk.Combobox(self.options_frame, textvariable=backbone_var, values=["ResNet", "ResNet-50", "MMBNet"])
        backbone_menu.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        self.option_vars["backbone_type"] = backbone_var

        # Checkpoint
        checkpoint_label = tk.Label(self.options_frame, text="Checkpoint")
        checkpoint_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        checkpoint_var = tk.StringVar(value=self.options["checkpoint"])
        checkpoint_menu = ttk.Combobox(self.options_frame, textvariable=checkpoint_var, values=["torchvision://resnet18", "torchvision://resnet50", "torchvision://resnet101"])
        checkpoint_menu.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        self.option_vars["checkpoint"] = checkpoint_var

        # Max epochs
        max_epochs_label = tk.Label(self.options_frame, text="Max Epochs")
        max_epochs_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")
        max_epochs_var = tk.IntVar(value=self.options["max_epochs"])
        max_epochs_scale = tk.Scale(self.options_frame, variable=max_epochs_var, from_=1, to=150, orient=tk.HORIZONTAL)
        max_epochs_scale.grid(row=3, column=1, padx=5, pady=5, sticky="w")
        self.option_vars["max_epochs"] = max_epochs_var

        # Loss cls weight
        loss_cls_label = tk.Label(self.options_frame, text="Loss Class Weight")
        loss_cls_label.grid(row=4, column=0, padx=5, pady=5, sticky="w")
        loss_cls_var = tk.DoubleVar(value=self.options["loss_cls_weight"])
        loss_cls_scale = tk.Scale(self.options_frame, variable=loss_cls_var, from_=1.0, to=150.0, orient=tk.HORIZONTAL)
        loss_cls_scale.grid(row=4, column=1, padx=5, pady=5, sticky="w")
        self.option_vars["loss_cls_weight"] = loss_cls_var

        # Loss bbox weight
        loss_bbox_label = tk.Label(self.options_frame, text="Loss BBox Weight")
        loss_bbox_label.grid(row=5, column=0, padx=5, pady=5, sticky="w")
        loss_bbox_var = tk.DoubleVar(value=self.options["loss_bbox_weight"])
        loss_bbox_scale = tk.Scale(self.options_frame, variable=loss_bbox_var, from_=1.0, to=150.0, orient=tk.HORIZONTAL)
        loss_bbox_scale.grid(row=5, column=1, padx=5, pady=5, sticky="w")
        self.option_vars["loss_bbox_weight"] = loss_bbox_var

    def save_config(self, file_path):
        try:
            for key, var in self.option_vars.items():
                self.options[key] = var.get()

            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            with open(file_path, 'w', encoding='utf-8') as f:
                for line in lines:
                    if re.search(r"model\s*=\s*dict\s*\(.*type\s*=\s*'(\w+)'", line):
                        line = re.sub(r"type\s*=\s*'\w+'", f"type = '{self.options['model_type']}'", line)
                    elif re.search(r"backbone\s*=\s*dict\s*\(.*type\s*=\s*'(\w+)'", line):
                        line = re.sub(r"type\s*=\s*'\w+'", f"type = '{self.options['backbone_type']}'", line)
                    elif re.search(r"init_cfg\s*=\s*dict\s*\(.*checkpoint\s*=\s*'([\w:/]+)'", line):
                        line = re.sub(r"checkpoint\s*=\s*'[\w:/]+'", f"checkpoint = '{self.options['checkpoint']}'", line)
                    elif re.search(r"runner\s*=\s*dict\s*\(.*max_epochs\s*=\s*(\d+)", line):
                        line = re.sub(r"max_epochs\s*=\s*\d+", f"max_epochs = {self.options['max_epochs']}", line)
                    elif re.search(r"loss_cls\s*=\s*dict\s*\(.*loss_weight\s*=\s*([\d.]+)", line):
                        line = re.sub(r"loss_weight\s*=\s*[\d.]+", f"loss_weight = {self.options['loss_cls_weight']}", line)
                    elif re.search(r"loss_bbox\s*=\s*dict\s*\(.*loss_weight\s*=\s*([\d.]+)", line):
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
            "checkpoint": "torchvision://resnet18",
            "max_epochs": 12,
            "loss_cls_weight": 1.0,
            "loss_bbox_weight": 1.0
        }

        for key, var in self.option_vars.items():
            var.set(default_values[key])

        self.status_label.config(text="Valeurs réinitialisées par défaut!", fg="green")
        logger.info("Valeurs réinitialisées par défaut.")
        logger.info(f"Valeurs réinitialisées à : {default_values}")

    def save_changes(self):
        config_path = self.config_path_entry.get()
        self.save_config(config_path)
        logger.info("Modifications sauvegardées par l'utilisateur.")
        logger.info(f"Valeurs sauvegardées : {self.options}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ConfigModifierApp(root)
    root.mainloop()




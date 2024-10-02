import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import random
import torch
import numpy as np
import torch.nn as nn
import torchvision.transforms as transforms
from PIL import Image
import cv2
import os

# ---- Initialisation du modèle et des fonctions d'entraînement ----

def set_seed(seed=42):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False

set_seed()  # Fixer la graine aléatoire

class CustomCrackDetectionModel(nn.Module):
    def __init__(self):
        super(CustomCrackDetectionModel, self).__init__()
        self.conv1 = self.conv_block(3, 64)
        self.conv2 = self.conv_block(64, 128)
        self.conv3 = self.conv_block(128, 256)
        self.conv4 = self.conv_block(256, 512)
        self.conv5 = self.conv_block(512, 512)
        self.side_convs = nn.ModuleList([
            nn.Conv2d(64, 1, kernel_size=1),
            nn.Conv2d(128, 1, kernel_size=1),
            nn.Conv2d(256, 1, kernel_size=1),
            nn.Conv2d(512, 1, kernel_size=1),
            nn.Conv2d(512, 1, kernel_size=1)
        ])
        self.fuse_conv = nn.Conv2d(5, 1, kernel_size=1)

    def conv_block(self, in_channels, out_channels):
        return nn.Sequential(
            nn.Conv2d(in_channels, out_channels, kernel_size=3, padding=1),
            nn.BatchNorm2d(out_channels),
            nn.ReLU(),
            nn.Conv2d(out_channels, out_channels, kernel_size=3, padding=1),
            nn.BatchNorm2d(out_channels),
            nn.ReLU()
        )

    def forward(self, x):
        conv_outs = [self.conv1(x)]
        for conv in [self.conv2, self.conv3, self.conv4, self.conv5]:
            conv_outs.append(conv(conv_outs[-1]))
        side_outs = [side_conv(conv_out) for side_conv, conv_out in zip(self.side_convs, conv_outs)]
        fuse_input = torch.cat(side_outs, dim=1)
        return self.fuse_conv(fuse_input)

def load_pretrained_model(model_path):
    model = CustomCrackDetectionModel()
    model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')), strict=False)
    model.eval()
    return model

def preprocess_image(image_path, image_size=256):
    img = Image.open(image_path).convert('RGB')
    transform = transforms.Compose([
        transforms.Resize((image_size, image_size)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])
    ])
    img_tensor = transform(img).unsqueeze(0)
    return img_tensor

def postprocess_output(output_tensor, threshold=0.5):
    output_np = output_tensor.squeeze().detach().numpy()
    output_np = (output_np > threshold).astype(np.uint8) * 255
    return output_np

def detect_cracks(model, image_path, output_dir):
    img_tensor = preprocess_image(image_path)
    with torch.no_grad():
        output = model(img_tensor)

    output_raw = output.squeeze().detach().numpy()
    output_raw_filename = os.path.join(output_dir, 'Image_' + os.path.basename(image_path))
    cv2.imwrite(output_raw_filename, (output_raw * 255).astype(np.uint8))

    output_mask = postprocess_output(output)

    output_filename = os.path.join(output_dir, 'Mask_' + os.path.basename(image_path))
    cv2.imwrite(output_filename, output_mask)
    print(f"Sauvegardé dans : {output_filename}")

# ---- Interface graphique avec tkinter ----

def run_detection(selected_model, image_dir):
    if not selected_model or not image_dir:
        messagebox.showwarning("Erreur", "Veuillez sélectionner un modèle et un dossier d'images.")
        return

    model = load_pretrained_model(selected_model)
    output_dir = 'deepcrack/results/'
    os.makedirs(output_dir, exist_ok=True)

    for img_file in os.listdir(image_dir):
        image_path = os.path.join(image_dir, img_file)
        if os.path.isfile(image_path):
            detect_cracks(model, image_path, output_dir)

    messagebox.showinfo("Terminé", "Détection des fissures terminée ! Les résultats sont sauvegardés dans le dossier 'deepcrack/results/'.")

def select_model():
    model_path = filedialog.askopenfilename(title="Sélectionner un modèle", filetypes=(("Fichiers .pth", "*.pth"),))
    model_entry.delete(0, tk.END)
    model_entry.insert(0, model_path)

def select_image_folder():
    folder_selected = filedialog.askdirectory(title="Sélectionner le dossier des images")
    folder_entry.delete(0, tk.END)
    folder_entry.insert(0, folder_selected)

# Création de l'interface
window = tk.Tk()
window.title("Détection des fissures")

# Style sombre pour ttk
style = ttk.Style(window)
window.tk.call("source", "azure.tcl")
window.tk.call("set_theme", "dark")

# Sélection du modèle
tk.Label(window, text="Modèle pré-entraîné :").grid(row=0, column=0, padx=10, pady=10)
model_entry = tk.Entry(window, width=50)
model_entry.grid(row=0, column=1, padx=10, pady=10)
model_button = tk.Button(window, text="Parcourir", command=select_model)
model_button.grid(row=0, column=2, padx=10, pady=10)

# Sélection du dossier d'images
tk.Label(window, text="Dossier des images :").grid(row=1, column=0, padx=10, pady=10)
folder_entry = tk.Entry(window, width=50)
folder_entry.grid(row=1, column=1, padx=10, pady=10)
folder_button = tk.Button(window, text="Parcourir", command=select_image_folder)
folder_button.grid(row=1, column=2, padx=10, pady=10)

# Bouton pour lancer le traitement
start_button = tk.Button(window, text="Démarrer", command=lambda: run_detection(model_entry.get(), folder_entry.get()))
start_button.grid(row=2, column=1, padx=10, pady=20)

# Lancer l'interface graphique
window.mainloop()

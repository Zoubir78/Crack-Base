import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import json
import requests

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

file_path = r'C:\Users\z.marouf-araibi\Desktop\Crack-Base\models_menu\models_json.json'
try:
    models_data = load_json(file_path)
    print("Chargement réussi:", models_data)
except ValueError as e:
    print(e)

# Vérifiez si les données ont été chargées correctement
if not models_data:
    print("Le fichier JSON est vide ou contient des données non valides.")
    messagebox.showerror("Erreur", "Le fichier JSON est vide ou contient des données non valides.")
    exit(1)

# Fonction pour télécharger le fichier de checkpoint
def download_checkpoint():
    selected_model = combo.get()
    for model in models_data:
        if model["Model Name"] == selected_model:
            url = model["Checkpoint_link"]
            filename = url.split("/")[-1]
            try:
                response = requests.get(url, stream=True)
                response.raise_for_status()
                total_size = int(response.headers.get('content-length', 0))
                block_size = 8192

                progress_bar["maximum"] = total_size
                downloaded_size = 0

                with open(filename, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=block_size):
                        if chunk:
                            f.write(chunk)
                            downloaded_size += len(chunk)
                            progress_bar["value"] = downloaded_size
                            percentage.set(f"{(downloaded_size / total_size) * 100:.0f}%")
                            root.update_idletasks()

                messagebox.showinfo("Succès", f"Téléchargement terminé: {filename}")
            except requests.exceptions.RequestException as e:
                messagebox.showerror("Erreur", f"Erreur de téléchargement: {e}")
            break

# Créer la fenêtre principale
root = tk.Tk()
root.title("Téléchargeur de Checkpoint")

# Ajouter une liste déroulante
label = tk.Label(root, text="Choisir un modèle:")
label.pack(pady=10)

model_names = [model["Model Name"] for model in models_data]
combo = ttk.Combobox(root, values=model_names)
combo.pack(pady=10)
combo.current(0)  # Sélectionne le premier élément par défaut

# Ajouter une barre de progression
progress_bar = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
progress_bar.pack(pady=10)

# Ajouter un label pour le pourcentage
percentage = tk.StringVar()
percentage_label = tk.Label(root, textvariable=percentage)
percentage_label.pack(pady=10)

# Ajouter un bouton pour lancer le téléchargement
button = tk.Button(root, text="Télécharger", command=download_checkpoint)
button.pack(pady=20)

# Lancer la boucle principale de l'interface graphique
root.mainloop()

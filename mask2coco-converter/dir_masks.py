import os
import shutil
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from tkinter import messagebox

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Copie des images masque")
        self.geometry("400x250")

        self.source_dir = tk.StringVar()
        self.destination_dir = tk.StringVar()

        self.progress_var = tk.DoubleVar()

        # Entry pour afficher les chemins sélectionnés
        tk.Label(self, text="Répertoire source:").pack()
        self.source_entry = tk.Entry(self, textvariable=self.source_dir)
        self.source_entry.pack()
        tk.Button(self, text="Sélectionner", command=self.select_source_directory).pack()

        tk.Label(self, text="Répertoire destination:").pack()
        self.destination_entry = tk.Entry(self, textvariable=self.destination_dir)
        self.destination_entry.pack()
        tk.Button(self, text="Sélectionner", command=self.select_destination_directory).pack()

        self.progress_bar = ttk.Progressbar(self, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(fill="x", padx=10, pady=5)

        self.copy_button = tk.Button(self, text="Copier les images", command=self.copy_mask_images)
        self.copy_button.pack()

    def select_source_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.source_dir.set(directory)

    def select_destination_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.destination_dir.set(directory)

    def copy_mask_images(self):
        source_dir = self.source_dir.get()
        destination_dir = self.destination_dir.get()

        if source_dir and destination_dir:
            if not os.path.exists(destination_dir):
                os.makedirs(destination_dir)

            # Compter uniquement les fichiers masque "0.png" dans le répertoire source
            total_files = sum(1 for root, dirs, files in os.walk(source_dir) for file in files if file == "0.png")
            copied_files = 0

            for root, dirs, files in os.walk(source_dir):
                for file in files:
                    if file == "0.png":
                        source_file_path = os.path.join(root, file)
                        destination_file_name = self.get_next_filename(destination_dir, file)
                        destination_file_path = os.path.join(destination_dir, destination_file_name)
                        shutil.copyfile(source_file_path, destination_file_path)
                        copied_files += 1
                        progress_percentage = (copied_files / total_files) * 100
                        self.progress_var.set(progress_percentage)
                        self.update_idletasks()

            messagebox.showinfo("Terminé", "La copie des images est terminée.")
            self.open_destination_folder(destination_dir)
        else:
            messagebox.showerror("Erreur", "Veuillez sélectionner les répertoires source et destination.")

    def get_next_filename(self, destination_dir, filename):
        base_name, extension = os.path.splitext(filename)
        counter = 1
        new_filename = filename
        while os.path.exists(os.path.join(destination_dir, new_filename)):
            new_filename = f"{base_name}_{counter}{extension}"
            counter += 1
        return new_filename

    def open_destination_folder(self, destination_dir):
        os.startfile(destination_dir)

if __name__ == "__main__":
    app = Application()
    app.mainloop()


import cv2
import numpy as np
import os
from tkinter import filedialog, Tk, Label, Entry, Button, Checkbutton, IntVar, StringVar

def select_folder_and_options():
    root = Tk()
    root.title("Options d'image")
    root.geometry("400x200")

    folder_path = StringVar()

    def select_folder():
        selected_folder = filedialog.askdirectory()
        if selected_folder:
            folder_path.set(selected_folder)

    folder_label = Label(root, text="Dossier des images :")
    folder_label.pack()

    folder_entry = Entry(root, textvariable=folder_path, width=50)
    folder_entry.pack()

    select_folder_button = Button(root, text="Sélectionner le dossier", command=select_folder)
    select_folder_button.pack()

    decalage_label = Label(root, text="Entrez le décalage en pixels :")
    decalage_label.pack()

    decalage_entry = Entry(root)
    decalage_entry.pack()

    rotate_var = IntVar()
    rotate_check = Checkbutton(root, text="Appliquer une rotation de 180° aux images de la série '_I2'", variable=rotate_var)
    rotate_check.pack()

    def on_confirm():
        folder_selected = folder_path.get()
        try:
            decalage = int(decalage_entry.get())
        except ValueError:
            decalage = None

        if folder_selected and decalage is not None:
            apply_rotation = rotate_var.get() == 1
            root.destroy()
            merge_images(folder_selected, decalage, apply_rotation)
        else:
            print("Veuillez sélectionner un dossier et entrer un décalage valide.")

    confirm_button = Button(root, text="Confirmer", command=on_confirm)
    confirm_button.pack()

    root.mainloop()

def merge_images(image_folder, decalage, apply_rotation):
    # Liste pour stocker les images
    images_series1 = []
    images_series2 = []

    # Charger les images
    for filename in os.listdir(image_folder):
        if filename.endswith(".png"):
            filepath = os.path.join(image_folder, filename)
            img = cv2.imread(filepath)
            if img is not None:
                if "_I1" in filename:
                    images_series1.append(img)
                elif "_I2" in filename:
                    if apply_rotation:
                        img = cv2.rotate(img, cv2.ROTATE_180)
                    images_series2.append(img)

    if not images_series1 or not images_series2:
        print("Assurez-vous que les images sont correctement nommées avec '_I1' et '_I2'.")
        return

    # Assurez-vous que toutes les images ont la même taille
    for i in range(len(images_series1)):
        images_series1[i] = cv2.resize(images_series1[i], (images_series1[0].shape[1], images_series1[0].shape[0]))
    for i in range(len(images_series2)):
        images_series2[i] = cv2.resize(images_series2[i], (images_series1[0].shape[1], images_series1[0].shape[0]))

    # Collage des images côte à côte pour la première série
    result1 = np.concatenate(images_series1, axis=1)

    # Collage des images côte à côte pour la deuxième série
    result2 = np.concatenate(images_series2, axis=1)

    # Calculer la nouvelle largeur de l'image résultante en tenant compte du décalage
    new_width = max(result1.shape[1] + decalage, result2.shape[1] + decalage)

    # Créer une nouvelle image vide avec une hauteur supplémentaire pour le décalage
    new_height = result1.shape[0] + result2.shape[0]
    result = np.zeros((new_height, new_width, 3), dtype=np.uint8)

    # Placer la deuxième série d'images en haut avec le décalage
    result[:result2.shape[0], decalage:decalage + result2.shape[1]] = result2

    # Placer la première série d'images en dessous de la deuxième sans décalage
    result[result2.shape[0]:result2.shape[0] + result1.shape[0], :result1.shape[1]] = result1

    output_path = os.path.join(image_folder, 'image_collee_finale.jpg')
    cv2.imwrite(output_path, result)

    # Afficher un message de confirmation
    print(f'Image collée enregistrée avec succès à {output_path}.')

if __name__ == "__main__":
    select_folder_and_options()

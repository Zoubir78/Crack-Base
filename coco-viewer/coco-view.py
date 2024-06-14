# -*- coding: utf-8 -*-
'''
Created on 25 mai 2024
@author: Zoubeir Marouf
'''
import os
import json
import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt

def draw_boxes(ax, annotations, categories):
    """Dessine des boîtes englobantes avec les catégories sur l'image."""
    for annotation in annotations:
        bbox = annotation["bbox"]
        category_id = annotation["category_id"]
        category_name = categories.get(category_id, "cable")
        xmin, ymin, width, height = map(int, bbox)
        xmax = xmin + width
        ymax = ymin + height
        ax.add_patch(plt.Rectangle((xmin, ymin), width, height, fill=False, edgecolor="g", linewidth=2))
        ax.text(xmin, ymin - 10, category_name, fontsize=9, bbox=dict(facecolor='g', alpha=0.5))

def visualize_images_with_boxes(image_dir, annotations_file):
    """Visualise les images avec les boîtes englobantes et les catégories."""
    if not os.path.exists(image_dir):
        print(f"Image directory '{image_dir}' not found. Exiting...")
        return
    if not os.path.exists(annotations_file):
        print(f"Annotations file '{annotations_file}' not found. Exiting...")
        return
    
    with open(annotations_file, "r") as json_file:
        data = json.load(json_file)
    
    categories = {category["id"]: category["name"] for category in data.get("categories", [])}

    image_ids = [image_info["id"] for image_info in data.get("images", [])]
    if not image_ids:
        print("No image information found. Exiting...")
        return
    
    current_image_index = 0

    fig, ax = plt.subplots()
    ax.set_title('Image avec BBoxes')

    def show_image(image_id):
        ax.clear()  # Efface les annotations précédentes
        image_info = next((info for info in data.get("images", []) if info["id"] == image_id), None)
        if image_info:
            image_file = os.path.join(image_dir, image_info["file_name"])
            if os.path.exists(image_file):
                annotations = [annotation for annotation in data.get("annotations", []) if annotation["image_id"] == image_id]
                image = plt.imread(image_file)
                ax.imshow(image)
                draw_boxes(ax, annotations, categories)
                ax.set_title(image_info["file_name"])  # Affiche le nom du fichier image
                plt.draw()
            else:
                print(f"Image file not found: {image_file}")
        else:
            print("Image info not found.")

    show_image(image_ids[current_image_index])

    def on_key(event):
        nonlocal current_image_index
        if event.key == 'q':
            plt.close(fig)
            return
        elif event.key == 'right':
            current_image_index = (current_image_index + 1) % len(image_ids)
        elif event.key == 'left':
            current_image_index = (current_image_index - 1) % len(image_ids)
        show_image(image_ids[current_image_index])

    fig.canvas.mpl_connect('key_press_event', on_key)
    plt.show()

def select_folder():
    """Sélectionne un dossier contenant des images."""
    root = tk.Tk()
    root.withdraw()
    folder_path = filedialog.askdirectory(title="Select Image Folder")
    return folder_path

def select_annotations_file():
    """Sélectionne un fichier d'annotations JSON."""
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(title="Select Annotations File", filetypes=[("JSON files", "*.json")])
    return file_path

# Sélectionner le dossier contenant les images
image_dir = select_folder()
if not image_dir:
    print("No folder selected. Exiting...")
    exit()

# Sélectionner le fichier d'annotations JSON
annotations_file = select_annotations_file()
if not annotations_file:
    print("No annotations file selected. Exiting...")
    exit()

# Visualiser les images avec les boîtes englobantes et les catégories
visualize_images_with_boxes(image_dir, annotations_file)

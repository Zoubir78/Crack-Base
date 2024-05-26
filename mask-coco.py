# -*- coding: utf-8 -*-
'''
Created on 2 avr. 2024
@author: Zoubeir Marouf
'''
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
import os
import numpy as np
from PIL import Image
import json

def mask_to_coco(image_path, output_folder, category_id=1):
    # Open the image and process it
    mask_array = np.array(Image.open(image_path))
    non_zero_indices = np.where(mask_array != 0)
    num_annotations = len(non_zero_indices[0])

    annotations = []
    image_id = hash(os.path.basename(image_path)) % 100000  # Générer un ID unique basé sur le hash du nom de fichier
    for i in range(num_annotations):
        x, y = non_zero_indices[1][i], non_zero_indices[0][i]
        bbox = [x, y, 1, 1]  # x, y, width, height
        annotation = {
            "id": i + 1,
            "image_id": image_id,
            "category_id": category_id,
            "segmentation": [[]],  # Set segmentation as an empty list
            "area": 1,
            "bbox": bbox,
            "iscrowd": 0
        }
        annotations.append(annotation)

    image_info = {
        "id": image_id,
        "file_name": os.path.basename(image_path),
        "width": mask_array.shape[1],
        "height": mask_array.shape[0],
        "license": None,
        "flickr_url": "",
        "coco_url": "",
        "date_captured": None
    }

    # Convert int64 to native Python int
    mask_array = mask_array.astype(int)

    coco_format = {
        "info": {},
        "images": [image_info],
        "annotations": annotations,
        "licenses": [],
        "categories": [{"id": category_id, "name": "mask"}]
    }

    output_path = os.path.join(output_folder, f"{os.path.splitext(os.path.basename(image_path))[0]}.json")
    with open(output_path, "w") as f:
        json.dump(coco_format, f, indent=4, default=int)  # Use default=int to handle int64 serialization

def select_input_folder():
    global input_folder
    input_folder = filedialog.askdirectory()
    if input_folder:
        select_output_folder()

def select_output_folder():
    global output_folder
    output_folder = filedialog.askdirectory()
    if output_folder:
        convert_to_coco(input_folder, output_folder)

def convert_to_coco(input_folder, output_folder):
    files = os.listdir(input_folder)
    total_files = len(files)
    progress_var = tk.DoubleVar()
    progress_bar.config(variable=progress_var, maximum=total_files)
    progress_var.set(0)
    for i, file_name in enumerate(files):
        image_path = os.path.join(input_folder, file_name)
        mask_to_coco(image_path, output_folder)
        progress_var.set(i + 1)
        root.update_idletasks()  # Force GUI update
    # Show output folder after conversion
    show_output_folder(output_folder)

def show_output_folder(output_folder):
    os.startfile(output_folder)

root = tk.Tk()
root.title("Mask to COCO Converter")

progress_bar = ttk.Progressbar(root, maximum=100)
progress_bar.pack(fill="x")

select_input_folder_btn = tk.Button(root, text="Sélectionner le dossier d'entrée", command=select_input_folder)
select_input_folder_btn.pack(pady=10)

root.mainloop()
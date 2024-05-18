import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import json
from collections import OrderedDict
import datetime
import cv2
import numpy as np
from tqdm import tqdm

class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(NpEncoder, self).default(obj)

def remove_file_extension(file_name):
    return os.path.splitext(file_name)[0]

def create_sub_mask(mask, width, height):
    sub_mask_imgs = [np.zeros_like(mask) for _ in range(3)] # class: 0, 1, 2

    for i in range(width):
        for j in range(height):
            pixel_value = mask[i][j]
            if pixel_value in [0, 1, 2]:
                sub_mask_imgs[pixel_value][i][j] = 255
    
    return sub_mask_imgs

def get_coco_info():
    info = {
        'description': 'BCSS custom dataset',
        'url': 'https://www.kaggle.com/datasets/whats2000/breast-cancer-semantic-segmentation-bcss/data',
        'version': '1.0',
        'year': 2024,
        'contributor': '李晨愷',
        'data_created': str(datetime.datetime.now())
    }

    return info

def get_coco_licenses():
    licenses = [
        {
            'url': 'https://creativecommons.org/publicdomain/zero/1.0/',
            'id': 1,
            'name': 'CC0: Public Domain'
        }
    ]

    return licenses

def get_coco_image(file_name, height, width):
    image = {}
    image['license'] = 1
    image['file_name'] = file_name
    image['coco_url'] = '' 
    image['height'] = height 
    image['width'] = width 
    image['date_captured'] = str(datetime.datetime.now())
    image['flickr_url'] = ''
    image['id'] = int(remove_file_extension(file_name))

    return image

def get_coco_anno(annotations, file_name, mask, category_id, segm_id):

    _, thresh = cv2.threshold(mask, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    contours, _ = cv2.findContours(thresh, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)

    for contour in contours:
        annotation_info = {}
        segm_points =  contour.flatten().tolist()

        if len(segm_points) <= 4:
            continue

        annotation_info['segmentation'] = [segm_points]
        annotation_info['area'] = cv2.contourArea(contour)
        annotation_info['iscrowd'] = 0
        annotation_info['image_id'] = int(remove_file_extension(file_name))
        annotation_info['bbox'] = cv2.boundingRect(contour)
        annotation_info['category_id'] = category_id 

        annotation_info['id'] = segm_id

        segm_id += 1 
        annotations.append(annotation_info)

    return segm_id

def get_coco_categories():

    categories = [
        {
            'supercategory': 'cell',
            'id':1,
            'name': 'outside_roi'
        },
        {
            'supercategory': 'cell',
            'id':2,
            'name': 'tumor'
        },
        {
            'supercategory': 'cell',
            'id':3, 
            'name': 'stroma'
        }
    ]

    return categories

def masks_to_json(mask_dirpath, progress_bar, progress_label):
    coco_json = OrderedDict()

    info = get_coco_info()
    licenses = get_coco_licenses()
    categories = get_coco_categories()

    images = []
    annotations = [] 

    files = os.listdir(mask_dirpath)
    total_files = len(files)
    progress_bar["maximum"] = total_files

    segm_id = 1

    for file in tqdm(files, desc="Converting masks"):
        file_path = os.path.join(mask_dirpath, file)
        mask = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
        width, height = mask.shape

        image = get_coco_image(file, width, height)
        images.append(image)

        sub_masks = create_sub_mask(mask, width, height)
        for category_id, sub_mask in enumerate(sub_masks):
            segm_id = get_coco_anno(annotations, file, sub_mask, category_id, segm_id)
        
        progress_bar["value"] += 1
        progress_label.config(text=f"{progress_bar['value']/total_files*100:.0f}%")
        progress_bar.update()
        progress_label.update()

    coco_json['info'] = info
    coco_json['licenses'] = licenses
    coco_json['images'] = images
    coco_json['annotations'] = annotations
    coco_json['categories'] = categories

    with open('annotations.json', 'w', encoding='utf-8') as make_file:
        json.dump(coco_json, make_file, cls=NpEncoder, ensure_ascii=False, indent='\t')

def select_mask_directory():
    mask_dirpath = filedialog.askdirectory()
    if mask_dirpath:
        mask_dirpath_entry.delete(0, tk.END)
        mask_dirpath_entry.insert(0, mask_dirpath)

def convert_to_coco():
    mask_dirpath = mask_dirpath_entry.get()
    if not mask_dirpath:
        messagebox.showerror("Erreur", "Veuillez sélectionner le répertoire des masques.")
        return

    masks_to_json(mask_dirpath, progress_bar, progress_label)
    messagebox.showinfo("Conversion terminée", "La conversion en format COCO a été effectuée avec succès.")

root = tk.Tk()
root.title("Conversion de masques en format COCO")

mask_dirpath_entry = ttk.Entry(root, width=50)
mask_dirpath_entry.grid(row=0, column=0, padx=5, pady=5)

select_mask_dir_btn = ttk.Button(root, text="Sélectionner le dossier des masques", command=select_mask_directory)
select_mask_dir_btn.grid(row=0, column=1, padx=5, pady=5)

convert_btn = ttk.Button(root, text="Convertir en COCO", command=convert_to_coco)
convert_btn.grid(row=1, columnspan=2, padx=5, pady=5)

progress_label = ttk.Label(root, text="")
progress_label.grid(row=2, column=0, padx=5, pady=5)

progress_bar = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
progress_bar.grid(row=2, column=1, padx=5, pady=5)

root.mainloop()


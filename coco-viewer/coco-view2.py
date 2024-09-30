# -*- coding: utf-8 -*-
'''
Created on 25 mai 2024
@author: Zoubeir Marouf
'''
import json
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

# Fonction pour calculer la bounding box à partir des points du polygone
def calculate_bbox(points):
    x_coords = [p[0] for p in points]
    y_coords = [p[1] for p in points]
    xmin = min(x_coords)
    ymin = min(y_coords)
    width = max(x_coords) - xmin
    height = max(y_coords) - ymin
    return [xmin, ymin, width, height]

# Fonction pour convertir les annotations en format COCO
def convert_to_coco(json_data):
    coco_output = {
        "images": [],
        "annotations": [],
        "categories": []
    }

    image_id = 1
    annotation_id = 1

    # Ajouter l'image à la section "images" de COCO
    coco_output["images"].append({
        "file_name": json_data["imagePath"],
        "height": json_data["imageHeight"],
        "width": json_data["imageWidth"],
        "id": image_id
    })

    # Parcourir chaque forme annotée (cable, passe_cable, etc.)
    for shape in json_data["shapes"]:
        label = shape["label"]
        points = shape["points"]

        # Calcul de la bounding box
        bbox = calculate_bbox(points)

        # Segmentation (COCO attend une liste plate des points)
        segmentation = [coord for point in points for coord in point]

        # Ajouter les annotations à la section "annotations" de COCO
        coco_output["annotations"].append({
            "id": annotation_id,
            "image_id": image_id,
            "category_id": 1,  # Supposons une seule catégorie pour le moment
            "bbox": bbox,
            "segmentation": [segmentation],
            "area": bbox[2] * bbox[3],  # Largeur * Hauteur
            "iscrowd": 0
        })
        annotation_id += 1

    # Ajouter la catégorie (ici, nous supposerons que vous avez une catégorie "cable")
    coco_output["categories"].append({
        "id": 1,
        "name": "cable",  # Vous pouvez ajouter d'autres catégories ici
        "supercategory": "object"
    })

    return coco_output

# Fonction pour dessiner les boîtes englobantes et segmentations
def draw_boxes(ax, annotations, image_info):
    for annotation in annotations:
        bbox = annotation["bbox"]
        segmentation = annotation["segmentation"][0]
        # Extraire les points de la segmentation
        poly = np.array(segmentation).reshape((len(segmentation) // 2, 2))
        polygon = Polygon(poly, closed=True, edgecolor='r', fill=False, linewidth=2)
        ax.add_patch(polygon)

        # Dessiner la bounding box
        xmin, ymin, width, height = bbox
        ax.add_patch(plt.Rectangle((xmin, ymin), width, height, fill=False, edgecolor="g", linewidth=2))
        ax.text(xmin, ymin - 10, "cable", fontsize=9, bbox=dict(facecolor='g', alpha=0.5))

# Exemple d'utilisation
json_data = {
  "version": "0.4.10",
  "flags": {},
  "shapes": [
    {
      "label": "cable",
      "points": [
        [0.0, 1426.0], [61.0, 1361.0], [112.0, 1320.0], [201.0, 1233.0],
        [234.0, 1208.0], [271.0, 1194.0], [315.0, 1196.0], [344.0, 1209.0]
      ],
      "group_id": None,
      "shape_type": "polygon",
      "flags": {}
    },
    {
      "label": "passe_cable",
      "points": [
        [1491.0, 1917.0], [143.0, 703.0], [148.0, 669.0], [257.0, 268.0]
      ],
      "group_id": None,
      "shape_type": "polygon",
      "flags": {}
    }
  ],
  "imagePath": "TE_D_18064_H2870_A30_1_451500.png",
  "imageHeight": 2080,
  "imageWidth": 1500
}

# Conversion des annotations vers COCO
coco_annotations = convert_to_coco(json_data)

# Sauvegarder les annotations dans un fichier COCO
with open('annotations_coco.json', 'w') as f:
    json.dump(coco_annotations, f, indent=4)

# Visualisation (exemple d'image)
fig, ax = plt.subplots(1, figsize=(10, 10))
image = plt.imread(json_data["imagePath"])  # Charge l'image
ax.imshow(image)
draw_boxes(ax, coco_annotations["annotations"], coco_annotations["images"][0])
plt.show()


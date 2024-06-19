import os
import json

# Vérifier si le fichier d'annotation existe
ann_file = 'C:/Users/z.marouf-araibi/Desktop/mmdetection/configs/my_custom/grap/train/annotation_lcms_train.json'
if not os.path.exists(ann_file):
    print(f"Le fichier d'annotation n'existe pas : {ann_file}")
else:
    print(f"Le fichier d'annotation existe : {ann_file}")

# Vérifier si le répertoire d'images existe
img_prefix = 'C:/Users/z.marouf-araibi/Desktop/mmdetection/configs/my_custom/grap/train'
if not os.path.exists(img_prefix):
    print(f"Le répertoire d'images n'existe pas : {img_prefix}")
else:
    print(f"Le répertoire d'images existe : {img_prefix}")

with open(ann_file) as f:
    data = json.load(f)

# Vérifiez si des annotations existent
if 'annotations' in data and len(data['annotations']) > 0:
    print(f"Nombre d'annotations: {len(data['annotations'])}")
else:
    print("Aucune annotation trouvée dans le fichier.")
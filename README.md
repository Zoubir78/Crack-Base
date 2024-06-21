# Crack-Base

## À propos du projet 🚀

![carck-base](https://github.com/Zoubir78/Crack-Base/blob/master/carck-base.png)

Cette solution a été spécialement élaborée pour répondre aux exigences uniques du laboratoire ENDSUM. Toutefois, il est important de noter qu'aucun modèle ne peut s'adapter parfaitement à tous les projets étant donné la diversité des besoins. C'est pourquoi nous restons ouverts à l'évolution et à l'ajout de fonctionnalités supplémentaires pour mieux répondre à vos besoins spécifiques dans un futur proche.

## Construit Avec 
Les principaux frameworks/bibliothèques utilisés pour démarrer le projet :

- `os`
- `sys`
- `io`
- `cv2`
- `subprocess`
- `json`
- `tkinter`
- `Image`
- `ImageTk`
- `BytesIO`
- `Thread`
- `open_new`
- `datetime`
- `nbformat`
- `math`

## Prérequis
Voici les éléments dont vous avez besoin pour utiliser le logiciel et comment l'installer:
- `Python 3.12`
- `conda`

## Arborescence du projet

- Crack-Base/
#### coco-viewer
- ├── coco-viewer/
- │ └── cocoviewer.py
#### Databases
- ├── DB/
- │ ├── deepCrack.db
- │ ├── grandMare.db
- │ ├── lcms_database.db
- │ └── rdg.db
#### Export
- ├── export/
- │ ├── depth_data.json
- │ ├── images_data.json
- │ ├── images_data_deep.json
- │ └── images_data_rdg.json
#### Logs
- ├── logs/
- │ ├── equipements.log
- │ └── options_config.log
#### mask2coco
- ├── mask2coco/
- │ ├── mask2coco.py
- │ ├── dir_masks.py
- │ ├── visualize_mask2points.py
- │ └── analysis.py
#### mat2img
- ├── mat2img/
- │ └── mat2img.py
#### Pré-traitement
- ├── mmdetection/
- │ ├── checkpoints/
- │ └──└── mask_rcnn_r50_fpn_1x_coco.py
- │ └──└── resnet152-394f9c45.pth
- │ ├── configs/
- │ └──└── my_custom/
- │ └──└──└── my_custom_config.py (Zoubeir)
- │ └──└──└── my_custom_config_1.py (Nathan)
- │ ├── tools/
- │ └──└── train.py
- │ ├── choix-epoch.py
- │ └── resultat.py
- ├── models/
- │ └── models_json.json
#### SAM
- ├── output/
- ├── sam/
- │ ├── annotator.py
- │ └── categories.txt
#### Datasets
- ├── test/
- ├── train/
- ├── val/
#### work_dirs
- ├── work_dirs/
- │ ├── my_custom_config/
- │ ├──├── 20240611_100830.log
- │ ├──├── 20240611_100830.log.json
- │ └──└── my_custom_config.py
#### APP
- ├── app.py
- ├── annotation.py
- ├── option-config.py
- ├── requirements.txt

## Installation 🛠️
Instructions pour installer les dépendances et configurer le projet.

### Clonez le dépôt
```
git clone https://github.com/Zoubir78/Crack-Base.git
```
### Créez un environnement virtuel
```
python -m venv env
source env/bin/activate  # Sur Windows, utilisez `env\Scripts\activate.bat`
```
### Installez les dépendances Python 🤖
```
cd Crack-Base
```
```
pip install -r requirements.txt
```

## Utilisation 
Pour lancer l'application :
```
python app.py
```

- N'oubliez pas de créer deux dossiers, un pour les bases de données 'DB' et un autre pour les exports 'export'.
- Pour plus d'infos sur les modèles d'entrainement et le fichier de configuration, veuillez vous référer à la documentation de MMDetection. 🪄
[MMDetection] (https://mmdetection.readthedocs.io/en/3.x/get_started.html)

### Sauvegarde de l'environnement
Pour sauvegarder l'environnement de développement :
```
pip freeze requirements.txt
```

### Utilisation de conda (si vous utilisez Anaconda)
Si vous utilisez Anaconda, vous pouvez créer un environnement avec :
```
conda create --name myenv
conda activate myenv
```
Installez ensuite vos dépendances. Pour sauvegarder l'environnement :
```
conda env export > environment.yml
```
Pour recréer l'environnement à partir du fichier environment.yml :
```
conda env create -f environment.yml
```
En suivant ces étapes, vous pouvez sauvegarder et recréer l'environnement de développement de l'application facilement.

### Contribuer
Instructions pour contribuer au projet.

- Forkez le projet.
- Créez votre branche de fonctionnalité (git checkout -b fonctionnalite/NewFeature).
- Commitez vos modifications (git commit -m 'Ajout d'une nouvelle fonctionnalité').
- Pushez vers la branche (git push origin fonctionnalite/NewFeature).
- Ouvrez une Pull Request.

### Licence
MIT License

## Contact
Zoubeir MAROUF - marouf.zoubeir@gmail.com

Lien du projet : (https://github.com/Zoubir78/Crack-Base)

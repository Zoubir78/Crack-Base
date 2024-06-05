import warnings
from pathlib import Path
import mmcv
import numpy as np
import torch
from mmcv.ops import RoIPool
from mmcv.parallel import collate, scatter
from mmcv.runner import load_checkpoint
from mmdet.core import get_classes
from mmdet.datasets import replace_ImageToTensor
from mmdet.datasets.pipelines import Compose, LoadImageFromFile
from mmdet.models import build_detector
from PIL import Image
import os
import cv2
import json
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from shapely.geometry import Polygon
from mmdet.apis import init_detector, inference_detector


def troisD(chemin):
    imgs = np.array(Image.open(Path(chemin)))
    if len(imgs.shape) == 2:
        img = np.stack([imgs] * 3, axis=-1)
    else:
        img = imgs[:, :, :3]
    return img


def bbox_detect(result, seuil):
    bbox_det = []
    for label, bbox in enumerate(result):
        if not isinstance(bbox, list):
            continue

        for box in bbox:
            if isinstance(box, (list, np.ndarray)) and len(box) >= 5 and isinstance(box[-1], (float, np.floating)):
                if box[-1] > seuil:
                    bbox_det.append([label + 1] + list(box))

    return np.array(bbox_det)


def bbox_annot_det(chem, nom_image, nom_annot, seuil):
    chemin = os.path.join(chem, nom_image)
    img = troisD(chemin)
    result = inference_detector(model, img)
    bbox_det = bbox_detect(result, seuil)

    with open(nom_annot) as json_data:
        data_dict = json.load(json_data)

    bbox_annot = []
    for image in data_dict['images']:
        if image['file_name'] == nom_image:
            nom = image['id']
            break

    for annot in data_dict['annotations']:
        if annot['image_id'] == nom:
            bbox = annot['bbox']
            bbox_annot.append([annot['category_id'], bbox[0], bbox[1], bbox[0] + bbox[2], bbox[1] + bbox[3]])

    return np.array(bbox_annot), bbox_det


def calculate_iou(box_1, box_2):
    poly_1 = Polygon([(box_1[0], box_1[1]), (box_1[2], box_1[1]), (box_1[2], box_1[3]), (box_1[0], box_1[3])])
    poly_2 = Polygon([(box_2[0], box_2[1]), (box_2[2], box_2[1]), (box_2[2], box_2[3]), (box_2[0], box_2[3])])
    if not poly_1.is_valid or not poly_2.is_valid:
        return 0
    iou = poly_1.intersection(poly_2).area / poly_1.union(poly_2).area
    return iou


def iou_vt_detect(bbox_det, bbox_annot):
    acc = []
    for i in range(len(bbox_det)):
        for j in range(len(bbox_annot)):
            iou = calculate_iou(bbox_annot[j][1:], bbox_det[i][2:6])
            acc.append([i, j, iou])

    res = []
    ioumaxdet = []
    for i in range(0, len(acc), len(bbox_annot)):
        inter = acc[i]
        for j in range(0, len(bbox_annot)):
            if inter[2] < acc[i + j][2]:
                inter = acc[i + j]
        res.append(inter)
    for i in range(len(bbox_annot) - 1, len(acc), len(bbox_annot)):
        ioumaxdet.append(res[i])
    return ioumaxdet


def resultat(model, config, prefix, filename):
    results = {'img_prefix': prefix, 'jet_prefix': prefix, 'img_info': {'filename': filename}}
    transform = LoadImageFromFile()
    instance_ = transform(results)
    cfg = model.cfg
    device = next(model.parameters()).device
    cfg = cfg.copy()
    cfg.data.test.pipeline[0].type = 'LoadImageFromFile'
    cfg.data.test.pipeline = replace_ImageToTensor(cfg.data.test.pipeline)
    test_pipeline = Compose(cfg.data.test.pipeline)
    data = test_pipeline(instance_)
    newdata = {key: [d.data for d in data[key]] for key in data}

    data = newdata
    data['img_metas'] = [data['img_metas']]
    img = data['img'][0]

    if 'jet' in data:
        jet = data['jet'][0].unsqueeze(0)
        data['jet'][0] = jet

    img = img.unsqueeze(0)
    data['img'][0] = img

    if next(model.parameters()).is_cuda:
        data = scatter(data, [device])[0]
    else:
        for m in model.modules():
            assert not isinstance(m, RoIPool), 'CPU inference avec RoIPool n\'est pas supporté actuellement.'

    with torch.no_grad():
        results = model(return_loss=False, rescale=True, **data)

    return results


# Configuration des chemins et initialisation du modèle
chem = r"C:/Users/z.marouf-araibi/Desktop/dlta-ai/DLTA_AI_app/mmdetection/configs/my_custom/grap/train"
nom_annot = r"C:/Users/z.marouf-araibi/Desktop/dlta-ai/DLTA_AI_app/mmdetection/configs/my_custom/grap/train/annotation_lcms_train.json"
config_path = r"C:/Users/z.marouf-araibi/Desktop/dlta-ai/DLTA_AI_app/mmdetection/configs/my_custom/my_custom_config.py"
model_path = r"C:/Users/z.marouf-araibi/Desktop/dlta-ai/DLTA_AI_app/mmdetection/tools/work_dirs/my_custom_config/epoch_1.pth"

config = mmcv.Config.fromfile(config_path)
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = init_detector(config, model_path, device=device)

with open(nom_annot) as json_data:
    data_dict = json.load(json_data)

list_im = [i['file_name'] for i in data_dict['images']]

seuil_iou = 0.1
nbclass = [[i + 1, 0, 0, 0] for i in range(24)]
seuil = 0.3
fin = []

nom_classes = ['non_classee', 'cable', 'passe_cable', 'lumiere', 'joint', 'camera',
               'prisme_sos_telephone', 'bouche_incendie', 'reflecteur', 'prisme_issue_en_face',
               'indication_issue_de_secours', 'plaque_numerotee', 'issue_de_secours', 'plaque_anneau',
               'indication_id_sos', 'issue_sos_telephone', 'panneau_signalisation', 'coffrage',
               'boitier_elec', 'non_definie_1', 'non_definie_2', 'non_definie_3', 'non_definie_4',
               'non_definie_5']

for nom_image in list_im:
    chemin = os.path.join(chem, nom_image)
    img = troisD(chemin)
    result = resultat(model, config, chem, nom_image)
    
    if isinstance(result, tuple):
        result = result[0]
    
    bbox_det = bbox_detect(result, seuil)
    bbox_annot, _ = bbox_annot_det(chem, nom_image, nom_annot, seuil)

    acc1 = []
    for i in range(len(bbox_det)):
        for j in range(len(bbox_annot)):
            iou = calculate_iou(bbox_annot[j][1:], bbox_det[i][2:6])
            acc1.append([i, j, iou])

    ioumaxdet = iou_vt_detect(bbox_det, bbox_annot)
    vp, fp, fn, controle = [], [], [], []

    for j in ioumaxdet:
        if j[2] > seuil_iou:
            if bbox_det[j[0]][0] == bbox_annot[j[1]][0]:
                vp.append(j)
            else:
                fp.append(j)
        else:
            fp.append(j)
        controle.append(j[1])

    for i in range(len(bbox_annot)):
        if i not in controle:
            fn.append(bbox_annot[i])

    for j in nbclass:
        for i in vp:
            if bbox_det[i[0]][0] == j[0]:
                j[1] += 1
        for i in fp:
            if bbox_det[i[0]][0] == j[0]:
                j[2] += 1
        for i in fn:
            if i[0] == j[0]:
                j[3] += 1

    plt.figure(figsize=(10, 10))
    plt.imshow(img)
    ax = plt.gca()
    
    for bbox in bbox_det:
        rect = patches.Rectangle((bbox[2], bbox[3]), bbox[4] - bbox[2], bbox[5] - bbox[3], linewidth=1, edgecolor='r', facecolor='none')
        ax.add_patch(rect)
        ax.text(bbox[2], bbox[3] - 2, f'{nom_classes[int(bbox[0]) - 1]}: {bbox[6]:.2f}', fontsize=8, color='red', weight='normal', bbox=dict(facecolor='white', alpha=0.6))

    for bbox in bbox_annot:
        rect = patches.Rectangle((bbox[1], bbox[2]), bbox[3] - bbox[1], bbox[4] - bbox[2], linewidth=1, edgecolor='g', facecolor='none')
        ax.add_patch(rect)
        ax.text(bbox[1], bbox[2] - 2, f'{nom_classes[int(bbox[0]) - 1]}', fontsize=8, color='green', weight='normal', bbox=dict(facecolor='white', alpha=0.6))

    plt.title(f'{nom_image}')
    plt.axis('off')
    plt.show()

    stat = []
    for i, j in zip(nbclass, nom_classes):
        pre = i[1] / (i[1] + i[2]) if (i[1] + i[2]) != 0 else 0
        rap = i[1] / (i[1] + i[3]) if (i[1] + i[3]) != 0 else 0
        stat.append([i[0], j, pre, rap])

    fin.append(stat)

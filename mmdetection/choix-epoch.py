import json
from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt

# Chemins vers les fichiers JSON des différentes configurations
json_logs_intensite = [r"C:\Users\z.marouf-araibi\Desktop\dlta-ai\DLTA_AI_app\mmdetection\tools\work_dirs\my_custom_config\20220627_160712.log.json"]  # Intensite
json_logs_profondeur = [r"C:\Users\z.marouf-araibi\Desktop\Crack-Base\work_dirs\my_custom_config\\20220307_161221.log.json"]  # Profondeur
json_logs_fusion = [r"C:\Users\z.marouf-araibi\Desktop\Crack-Base\work_dirs\my_custom_config\20230717_094425.log.json"]  # Fusion

def process_logs(json_logs):
    log_dicts = [dict() for _ in json_logs]
    bbox_mAP = []
    segm_mAP = []
    loss = []
    loss_cls = []
    loss_bbox = []
    loss_mask = []
    for json_log, log_dict in zip(json_logs, log_dicts):
        with open(json_log, 'r') as log_file:
            for line in log_file:
                log = json.loads(line.strip())

                # skip lines without `epoch` field
                if 'epoch' not in log:
                    continue
                epoch = log.pop('epoch')
                if epoch not in log_dict:
                    log_dict[epoch] = defaultdict(list)
                for k, v in log.items():
                    log_dict[epoch][k].append(v)
                    if k == 'bbox_mAP':
                        bbox_mAP.append([epoch, v])
                    if k == 'segm_mAP':
                        segm_mAP.append([epoch, v])
                    if k == 'loss':
                        loss.append([epoch, v])
                    if k == 'loss_cls':
                        loss_cls.append([epoch, v])
                    if k == 'loss_bbox':
                        loss_bbox.append([epoch, v])
                    if k == 'loss_mask':
                        loss_mask.append([epoch, v])

    return bbox_mAP, segm_mAP, loss, loss_cls, loss_bbox, loss_mask

# Traiter les journaux pour chaque configuration
bbox_mAP_intensite, segm_mAP_intensite, loss_intensite, loss_cls_intensite, loss_bbox_intensite, loss_mask_intensite = process_logs(json_logs_intensite)
bbox_mAP_profondeur, segm_mAP_profondeur, loss_profondeur, loss_cls_profondeur, loss_bbox_profondeur, loss_mask_profondeur = process_logs(json_logs_profondeur)
bbox_mAP_fusion, segm_mAP_fusion, loss_fusion, loss_cls_fusion, loss_bbox_fusion, loss_mask_fusion = process_logs(json_logs_fusion)

def extract_map(bbox_mAP, segm_mAP):
    mAP = []
    for i, j in bbox_mAP:
        if i-1 < len(segm_mAP):
            mAP.append([i, j, segm_mAP[i-1][1]])
    return mAP

# Extraire les mAP
mAP_intensite = extract_map(bbox_mAP_intensite, segm_mAP_intensite)
mAP_profondeur = extract_map(bbox_mAP_profondeur, segm_mAP_profondeur)
mAP_fusion = extract_map(bbox_mAP_fusion, segm_mAP_fusion)

def plot_metrics(ax, x, y1, y2, label1, label2, title):
    ax.plot(x, y1, label=label1)
    ax.plot(x, y2, label=label2)
    ax.set_title(title)
    ax.legend()

fig, axs = plt.subplots(3, 2, figsize=(16, 16))

# Tracer les mAP
x_intensite = [i for i, j, k in mAP_intensite]
y1_intensite = [j for i, j, k in mAP_intensite]
y2_intensite = [k for i, j, k in mAP_intensite]

x_profondeur = [i for i, j, k in mAP_profondeur]
y1_profondeur = [j for i, j, k in mAP_profondeur]
y2_profondeur = [k for i, j, k in mAP_profondeur]

x_fusion = [i for i, j, k in mAP_fusion]
y1_fusion = [j for i, j, k in mAP_fusion]
y2_fusion = [k for i, j, k in mAP_fusion]

plot_metrics(axs[0, 0], x_intensite, y1_intensite, y2_intensite, "bbox_mAP", "segm_mAP", "Intensité mAP")
plot_metrics(axs[0, 1], x_profondeur, y1_profondeur, y2_profondeur, "bbox_mAP", "segm_mAP", "Profondeur mAP")
plot_metrics(axs[1, 0], x_fusion, y1_fusion, y2_fusion, "bbox_mAP", "segm_mAP", "Fusion mAP")

# Tracer les pertes
def plot_loss(ax, loss, loss_cls, loss_bbox, loss_mask, title):
    x = [i for i, j in loss]
    y_loss = [j for i, j in loss]
    y_loss_cls = [j for i, j in loss_cls]
    y_loss_bbox = [j for i, j in loss_bbox]
    y_loss_mask = [j for i, j in loss_mask]
    ax.plot(x, y_loss, label='Loss')
    ax.plot(x, y_loss_cls, label='Loss_cls')
    ax.plot(x, y_loss_bbox, label='Loss_bbox')
    ax.plot(x, y_loss_mask, label='Loss_mask')
    ax.set_title(title)
    ax.legend()

plot_loss(axs[1, 1], loss_intensite, loss_cls_intensite, loss_bbox_intensite, loss_mask_intensite, "Intensité Losses")
plot_loss(axs[2, 0], loss_profondeur, loss_cls_profondeur, loss_bbox_profondeur, loss_mask_profondeur, "Profondeur Losses")
plot_loss(axs[2, 1], loss_fusion, loss_cls_fusion, loss_bbox_fusion, loss_mask_fusion, "Fusion Losses")

plt.tight_layout()
plt.show()
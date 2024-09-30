import os
import cv2
import numpy as np
import codecs
import glob

def imread(path, load_size=0, load_mode=cv2.IMREAD_GRAYSCALE, convert_rgb=False, thresh=-1):
    im = cv2.imread(path, load_mode)
    if im is None:
        print(f"Error: Unable to load image at {path}")
        return None  # Retourner None si l'image ne peut pas être chargée
    
    if convert_rgb:
        im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
    if load_size > 0:
        im = cv2.resize(im, (load_size, load_size), interpolation=cv2.INTER_CUBIC)
    if thresh > 0:
        _, im = cv2.threshold(im, thresh, 255, cv2.THRESH_BINARY)
    return im

def get_image_pairs(data_dir, suffix_gt='label_viz', suffix_pred='fused'):
    gt_list = glob.glob(os.path.join(data_dir, f'*{suffix_gt}.png'))
    pred_list = [ll.replace(suffix_gt, suffix_pred) for ll in gt_list]
    
    # Vérification que les listes ont la même longueur
    assert len(gt_list) == len(pred_list), "Mismatch between ground truth and prediction images count."
    
    pred_imgs, gt_imgs = [], []
    for pred_path, gt_path in zip(pred_list, gt_list):
        pred_img = imread(pred_path)
        gt_img = imread(gt_path, thresh=127)
        
        if pred_img is not None and gt_img is not None:
            pred_imgs.append(pred_img)
            gt_imgs.append(gt_img)
        else:
            print(f"Skipping pair due to loading error: {pred_path} or {gt_path}")
    
    return pred_imgs, gt_imgs

def save_results(input_list, output_path):
    with codecs.open(output_path, 'w', encoding='utf-8') as fout:
        for ll in input_list:
            line = '\t'.join(['%.4f' % v for v in ll]) + '\n'
            fout.write(line)

# -*- coding: utf-8 -*-
'''
Created on 2 avr. 2024
@author: Zoubeir Marouf
'''
import random
import cv2
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import glob

image_file_list = glob.glob('/data/train/*')
mask_file_list = glob.glob('/data/train_mask/*')

# Redimensionner les images à une résolution de 224x224 pixels
resized_images = []
for image_file in image_file_list:
    image = cv2.imread(image_file)
    resized_image = cv2.resize(image, (224, 224))
    resized_images.append(resized_image)

print("Nombre d'images redimensionnées :", len(resized_images))

# Vérifier les dimensions d'une image redimensionnée
if resized_images:
    print("Dimensions de la première image redimensionnée :", resized_images[0].shape)

np.set_printoptions(threshold=np.inf, linewidth=np.inf)
image = resized_images[1]  # Utiliser l'image redimensionnée
mask_file = mask_file_list[1]
src = cv2.imread(mask_file, cv2.IMREAD_GRAYSCALE)  # Charger l'image en niveaux de gris directement

unique_value = np.unique(src)
print('unique_value:', unique_value)

sub_mask_imgs = [np.zeros_like(src) for _ in range(3)] # class: 0, 1, 2

# Parcourir les valeurs de pixel pour remplir les sous-masques d'image de chaque classe
for i in range(src.shape[0]):
    for j in range(src.shape[1]):
        pixel_value = src[i][j]
        if pixel_value == 0:
            sub_mask_imgs[0][i][j] = 255
        elif pixel_value == 255:
            sub_mask_imgs[1][i][j] = 255
        else:
            sub_mask_imgs[2][i][j] = 255

dst = np.zeros((src.shape[0], src.shape[1], 3), dtype=np.uint8)  # Modification pour créer une image couleur

# Dessiner les contours
for sub_mask_img in sub_mask_imgs:
    contours, _ = cv2.findContours(sub_mask_img, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)
    for contour in contours:
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        cv2.drawContours(dst, [contour], -1, color, 2)

fig, axs = plt.subplots(nrows=2, ncols=3, figsize=(12, 8))
fig.subplots_adjust(hspace=0.3, wspace=0.3)

titles = ['image', 'GrayScale mask', 'DrawContours', 'sub_mask: 0', 'sub_mask: 1', 'sub_mask: 2']
images = [image, src, dst] + sub_mask_imgs

for ax, title, image in zip(axs.flatten(), titles, images):
    ax.imshow(image, cmap=cm.gray if 'sub_mask' in title else None)
    ax.set_title(title)

plt.show()

# -*- coding: utf-8 -*-
'''
Created on 2 avr. 2024
@author: Zoubeir Marouf
'''

import numpy
import glob
import cv2
import matplotlib.pyplot as plt

def show_img(image_num, image_list, mask_list):

    image_path = image_list[image_num]
    mask_path = mask_list[image_num]

    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    mask = cv2.imread(mask_path)
    mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
    print(mask)
    print(numpy.unique(mask)) # print image class num 

    plt.imshow(image)
    plt.show()
    plt.imshow(mask)
    plt.show()


def check_class_distribution(mask_list):
    count_0 = 0
    count_1 = 0
    count_2 = 0

    for filename in mask_list:
        gray_image = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
        unique_value = numpy.unique(gray_image)

        if 0 in unique_value:
            count_0 += 1
        if 1 in unique_value:
            count_1 += 1
        if 2 in unique_value:
            count_2 += 1


    print('class 0(outside roi): ', count_0)
    print('class 1(tumor): ', count_1)
    print('class 2(stroma): ', count_2)

if __name__ == '__main__':

    image_path = 'data/train/*.png' # Chemin vers vos images
    mask_path = image_path.replace('/*.png', '_mask/*.png') # Modifier le chemin pour les masques

    image_list = glob.glob(image_path) 
    mask_list = glob.glob(mask_path)
    print(len(image_list), len(mask_list))

    show_img(1, image_list, mask_list)
    check_class_distribution(mask_list)

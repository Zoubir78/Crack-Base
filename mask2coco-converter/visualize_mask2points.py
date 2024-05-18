# %%
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
src = cv2.imread(mask_file)
src = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)


unique_value = np.unique(src)
print('unique_value:', unique_value)

sub_mask_imgs = [np.zeros_like(src) for _ in range(3)] # class: 0, 1, 2

# 픽셀 값별로 루프 돌며 각 클래스별 서브 마스크 이미지 채우기
for i in range(src.shape[0]):
    for j in range(src.shape[1]):
        pixel_value = src[i][j]
        if pixel_value == 0:
            sub_mask_imgs[0][i][j] = 255
        elif pixel_value == 255:
            sub_mask_imgs[1][i][j] = 255
        else:
            print("Pixel value out of range:", pixel_value)


dst = np.zeros((src.shape[0], src.shape[1]), dtype=np.uint8)

# draw contour
for sub_mask_img in sub_mask_imgs:
    contours, _ = cv2.findContours(sub_mask_img, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)
    for contour in contours:
        # print('-----')
        # print(contour)
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        cv2.drawContours(dst, [contour], -1, color, 2)


fig, _axs = plt.subplots(nrows=2, ncols=3)
fig.subplots_adjust(hspace=0.3, wspace=0.3)
axs = _axs.flatten()

axs[0].imshow(image)
axs[0].set_title('image')

axs[1].imshow(src, cmap=cm.gray)
axs[1].set_title('GrayScale mask')

axs[2].imshow(dst)
axs[2].set_title('DrawContours')

axs[3].imshow(sub_mask_imgs[0], cmap=cm.gray)
axs[3].set_title('sub_mask: 0')

axs[4].imshow(sub_mask_imgs[1], cmap=cm.gray)
axs[4].set_title('sub_mask: 1')

axs[5].imshow(sub_mask_imgs[2], cmap=cm.gray)
axs[5].set_title('sub_mask: 2')

plt.show()

# %%


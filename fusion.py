import os
import numpy as np
import scipy.io
import matplotlib.pyplot as plt
from scipy.signal import blackman
from numpy.fft import fft2, ifft2
from tkinter import Tk, filedialog

def Corel(im1, im2):
    # Taille image (à faire vérifier taille im1 == taille im2)
    nr, nc = im1.shape

    # Filtre 2D pour éviter les pb de bords
    f1 = blackman(nr)
    f2 = blackman(nc)
    f = np.outer(f1, f2)

    # Filtrage des entrées
    Image1 = im1 * f
    Image2 = im2 * f

    # Calcul de la corrélation dans Fourier
    I1 = fft2(Image1)
    I2 = np.conj(fft2(Image2))
    R = (I1 * I2) / np.abs(I1 * I2)
    correl = np.real(ifft2(R))

    # Recherche du pic de corrélation
    l, c = np.unravel_index(np.argmax(correl), correl.shape)
    r = correl[l, c]

    # Décalage origine (Matlab : origine=1) et traitement du signe
    if l <= nr / 2:
        l -= 1
    else:
        l -= nr + 1

    if c <= nc / 2:
        c -= 1
    else:
        c -= nc + 1

    return l, c, r

# Utilisation de tkinter pour sélectionner le dossier
root = Tk()
root.withdraw()  # Hide the main window

# Demander à l'utilisateur de sélectionner un dossier
print("Veuillez sélectionner le dossier contenant les images à fusionner.")
chemin_extract = filedialog.askdirectory()

if not chemin_extract:
    print("Aucun dossier sélectionné. Fin du programme.")
    exit()

print(f"Chemin sélectionné : {chemin_extract}")

# Création du dossier pour sauvegarder les images fusionnées
output_folder = os.path.join(chemin_extract, 'fusion_capteurs')
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Affichage du contenu du répertoire pour le debug
print(f"Contenu de {chemin_extract}:")
for root, dirs, files in os.walk(chemin_extract):
    level = root.replace(chemin_extract, '').count(os.sep)
    indent = ' ' * 4 * (level)
    print('{}{}/'.format(indent, os.path.basename(root)))
    subindent = ' ' * 4 * (level + 1)
    for f in files:
        print('{}{}'.format(subindent, f))

for numim in range(26, 27):  # (len(os.listdir(Path1))-1)
    nomfic1 = f'LcmsData_{numim+1:06d}'
    nomfic2 = f'LcmsData_{numim:06d}'
    
    # Construction des chemins de fichiers
    file1 = os.path.join(chemin_extract, 'Int_S1_', f'{nomfic1}.mat')
    file2 = os.path.join(chemin_extract, 'Int_S2_', f'{nomfic2}.mat')
    
    print(f"file1: {file1}")
    print(f"file2: {file2}")
    
    # Vérification de l'existence des fichiers
    if not os.path.isfile(file1):
        print(f"File not found: {file1}")
        continue
    if not os.path.isfile(file2):
        print(f"File not found: {file2}")
        continue
    
    # Chargement des données
    Mat1 = scipy.io.loadmat(file1)
    A = Mat1['A']
    
    Mat2 = scipy.io.loadmat(file2)
    B1 = Mat2['B']
    
    # Miroir et découpage
    A2_flip = np.flipud(A)  # Correction du miroir
    nr, nc = A2_flip.shape
    s = 149  # Largeur arbitraire de l'échantillon pour la corrélation
    sampleA2 = A2_flip[nr-s:nr, :]
    sampleB1 = B1[0:s+1, :]
    
    # S'assurer que les échantillons ont la même taille
    if sampleA2.shape != sampleB1.shape:
        min_rows = min(sampleA2.shape[0], sampleB1.shape[0])
        min_cols = min(sampleA2.shape[1], sampleB1.shape[1])
        sampleA2 = sampleA2[:min_rows, :min_cols]
        sampleB1 = sampleB1[:min_rows, :min_cols]
    
    # Calcul de la corrélation par FFT
    l, c, r = Corel(sampleB1, sampleA2)
    print(l, c, r)
    
    # Affichage des données de chaque capteur
    fig, axs = plt.subplots(1, 2, num=20)
    axs[0].imshow(A2_flip, cmap='gray')
    axs[0].set_title('Données Int capteur 1')
    axs[0].axis('off')

    axs[1].imshow(B1, cmap='gray')
    axs[1].set_title('Données Int capteur 2')
    axs[1].axis('off')

    plt.show()

    # Création d'une image blanche
    Finalimage = 255 * np.ones((nc + 2 * abs(c), 2 * nr))  # Utilisation de abs(c)
    Finalimage2 = 255 * np.ones((nc + 2 * abs(c), 2 * nr))  # Utilisation de abs(c)
    print(Finalimage.shape)
    print(Finalimage2.shape)

    # Remplissage de l'image blanche avec les données des deux capteurs
    Finalimage[abs(c):abs(c)+nc, nr:2*nr] = B1.T
    Finalimage[2*abs(c):2*abs(c)+nc, s+l:s+l+nr] = A2_flip.T

    Finalimage2[2*abs(c):2*abs(c)+nc, s+l:s+l+nr] = A2_flip.T
    Finalimage2[abs(c):abs(c)+nc, nr:2*nr] = B1.T

    # Fusion des deux images en prenant le maximum
    final = np.maximum(Finalimage2, Finalimage)
    
    # Sauvegarde de l'image fusionnée
    output_filename = os.path.join(output_folder, f'fusion_{numim:06d}.png')
    plt.imsave(output_filename, final, cmap='gray')

    plt.figure(5)
    plt.imshow(final, cmap='gray')
    plt.show()

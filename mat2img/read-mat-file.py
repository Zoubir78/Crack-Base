import scipy.io
import json
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# Charger le fichier .mat
mat = scipy.io.loadmat(r'LcmsData_000002.mat')

# Afficher les clés disponibles dans le fichier .mat
print("Clés disponibles dans le fichier MATLAB:")
print(mat.keys())

# Enregistrer toutes les variables dans un fichier JSON
variables_dict = {key: mat[key].tolist() for key in mat if not key.startswith('__')}

with open('variables.json', 'w') as f:
    json.dump(variables_dict, f)

# Afficher les données de chaque variable
for key, value in variables_dict.items():
    print(f"Données de la variable {key}:")
    print(value)

# Charger une image
image_path = r'LcmsData_000002.png'  # Remplacez par le chemin de votre image
img = mpimg.imread(image_path)

# Créer une figure avec plusieurs sous-graphiques
fig, ax = plt.subplots(len(variables_dict) + 1, 1, figsize=(14, 7 * (len(variables_dict) + 1)))

# Tracer les données de chaque variable
for i, (key, value) in enumerate(variables_dict.items()):
    ax[i].plot(value)
    ax[i].set_title(f'Données de la variable {key}')

# Afficher l'image dans le dernier sous-graphe
ax[len(variables_dict)].imshow(img)
ax[len(variables_dict)].axis('off')  # Masquer les axes pour l'image
ax[len(variables_dict)].set_title('Image')

# Afficher la figure
plt.tight_layout()
plt.show()

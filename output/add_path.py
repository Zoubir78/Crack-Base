import json

# Chemin du fichier JSON
file_path = r"C:\Users\z.marouf-araibi\Desktop\train\DEP\annotations.json"

# Lire le fichier JSON
with open(file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

# Accéder à la liste des images
images = data.get("images", [])

# Modifier chaque chemin de fichier pour ajouter "/DEP" après "/train"
for item in images:
    item['file_name'] = item['file_name'].replace("/train", "/train/DEP")

# Sauvegarder les modifications dans le fichier JSON
with open(file_path, 'w', encoding='utf-8') as file:
    json.dump(data, file, indent=4, ensure_ascii=False)

# Afficher le résultat modifié
print(json.dumps(data, indent=4, ensure_ascii=False))

import random
import torch
import numpy as np
import torch.nn as nn
import torchvision.transforms as transforms
from PIL import Image
import cv2
import os

def set_seed(seed=42):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False

set_seed()  # Fixer la graine aléatoire

class CustomCrackDetectionModel(nn.Module):
    def __init__(self):
        super(CustomCrackDetectionModel, self).__init__()
        # Blocks de convolution
        self.conv1 = self.conv_block(3, 64)
        self.conv2 = self.conv_block(64, 128)
        self.conv3 = self.conv_block(128, 256)
        self.conv4 = self.conv_block(256, 512)
        self.conv5 = self.conv_block(512, 512)

        # Couches de fusion
        self.side_convs = nn.ModuleList([
            nn.Conv2d(64, 1, kernel_size=1),
            nn.Conv2d(128, 1, kernel_size=1),
            nn.Conv2d(256, 1, kernel_size=1),
            nn.Conv2d(512, 1, kernel_size=1),
            nn.Conv2d(512, 1, kernel_size=1)
        ])
        
        # Convolution finale de fusion
        self.fuse_conv = nn.Conv2d(5, 1, kernel_size=1)

    def conv_block(self, in_channels, out_channels):
        return nn.Sequential(
            nn.Conv2d(in_channels, out_channels, kernel_size=3, padding=1),
            nn.BatchNorm2d(out_channels),
            nn.ReLU(),
            nn.Conv2d(out_channels, out_channels, kernel_size=3, padding=1),
            nn.BatchNorm2d(out_channels),
            nn.ReLU()
        )

    def forward(self, x):
        conv_outs = [self.conv1(x)]
        for conv in [self.conv2, self.conv3, self.conv4, self.conv5]:
            conv_outs.append(conv(conv_outs[-1]))

        side_outs = [side_conv(conv_out) for side_conv, conv_out in zip(self.side_convs, conv_outs)]
        fuse_input = torch.cat(side_outs, dim=1)
        return self.fuse_conv(fuse_input)

def load_pretrained_model(model_path):
    model = CustomCrackDetectionModel()
    model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')), strict=False)
    model.eval()  # Assurez-vous que le modèle est en mode évaluation
    return model

def preprocess_image(image_path, image_size=256):
    img = Image.open(image_path).convert('RGB')  # Convertir en RGB
    transform = transforms.Compose([
        transforms.Resize((image_size, image_size)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])  # Normalisation
    ])
    img_tensor = transform(img).unsqueeze(0)  # Ajouter une dimension pour le batch
    return img_tensor

def postprocess_output(output_tensor, threshold=0.5):
    output_np = output_tensor.squeeze().detach().numpy()  # Enlever les dimensions inutiles
    output_np = (output_np > threshold).astype(np.uint8) * 255  # Binarisation
    return output_np

def detect_cracks(model, image_path, output_dir):
    img_tensor = preprocess_image(image_path)
    with torch.no_grad():
        output = model(img_tensor)  # Passer l'image dans le modèle

    # Sauvegarde de la sortie brute
    output_raw = output.squeeze().detach().numpy()
    output_raw_filename = os.path.join(output_dir, 'Image_' + os.path.basename(image_path))
    cv2.imwrite(output_raw_filename, (output_raw * 255).astype(np.uint8))  # Multiplier par 255 pour la visualisation

    # Post-traitement
    output_mask = postprocess_output(output)

    # Sauvegarder le masque
    output_filename = os.path.join(output_dir, 'Mask_' + os.path.basename(image_path))
    cv2.imwrite(output_filename, output_mask)  # Sauvegarde le masque binaire
    print(f"Résultat sauvegardé : {output_filename}")

def main():
    model_path = '50_net_G.pth'  # Chemin vers le modèle pré-entraîné
    images_dir = 'images_test/'   # Dossier avec les images à tester
    output_dir = 'results/'       # Dossier de sortie pour les résultats

    os.makedirs(output_dir, exist_ok=True)  # Créer le dossier de sortie s'il n'existe pas
    model = load_pretrained_model(model_path)  # Charger le modèle

    for img_file in os.listdir(images_dir):
        image_path = os.path.join(images_dir, img_file)
        if os.path.isfile(image_path):  # Vérifier si c'est un fichier
            detect_cracks(model, image_path, output_dir)

if __name__ == '__main__':
    main()

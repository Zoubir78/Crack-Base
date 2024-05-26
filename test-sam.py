# -*- coding: utf-8 -*-
'''
Created on 20 avr. 2024
@author: Zoubeir Marouf
'''
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import torch
from segment_anything import SamPredictor, sam_model_registry
from segment_anything.utils.transforms import ResizeLongestSide
import numpy as np
import os

class MainApplication(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model_type = "vit_b"  # Remplacez par le type de modèle SAM que vous utilisez
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.target_length = 1024  # Longueur cible pour le redimensionnement
        
        self.actions = lambda: None
        self.actions.loadSAM = tk.Button(self, text="Load SAM", command=self.clickLoadSAM)
        self.actions.loadSAM.pack(side=tk.LEFT, padx=5, pady=5)
        self.actions.selectFolder = tk.Button(self, text="Select Folder", command=self.selectFolder)
        self.actions.selectFolder.pack(side=tk.LEFT, padx=5, pady=5)
        self.actions.autoSeg = tk.Button(self, text="Auto Segment", command=self.clickAutoSeg)
        self.actions.autoSeg.pack(side=tk.LEFT, padx=5, pady=5)
        self.actions.autoSeg.config(state=tk.DISABLED)  # Disabled initially
        self.actions.promptSeg = tk.Button(self, text="Prompt Segment", command=self.clickPromptSeg)
        self.actions.promptSeg.pack(side=tk.LEFT, padx=5, pady=5)
        self.actions.promptSeg.config(state=tk.DISABLED)  # Disabled initially
        
        self.image_label = tk.Label(self)
        self.image_label.pack(side=tk.TOP, padx=5, pady=5)
        self.image_path = None  # To store the path of the loaded image
        self.folder_path = None  # To store the path of the selected folder

    def clickLoadSAM(self):
        download_model(self.model_type)
        self.sam = sam_model_registry[self.model_type](checkpoint='{}.pth'.format(self.model_type))
        self.sam.to(device=self.device)
        self.predictor = SamPredictor(self.sam)
        self.actions.loadSAM.config(state=tk.DISABLED)
        self.actions.autoSeg.config(state=tk.NORMAL)
        self.actions.promptSeg.config(state=tk.NORMAL)

    def selectFolder(self):
        self.folder_path = filedialog.askdirectory()
        if self.folder_path:
            messagebox.showinfo("Folder Selected", f"Dossier sélectionné: {self.folder_path}")

    def load_image(self, image_path):
        self.image_path = image_path
        image = Image.open(image_path)
        image.thumbnail((800, 800))  # Resize for display purposes
        self.image = image
        self.display_image(image)

    def display_image(self, image):
        self.tk_image = ImageTk.PhotoImage(image)
        self.image_label.config(image=self.tk_image)
    
    def clickAutoSeg(self):
        if self.folder_path is None:
            messagebox.showerror("Erreur", "Veuillez sélectionner un dossier contenant des images avant de segmenter.")
            return

        for file_name in os.listdir(self.folder_path):
            if file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                image_path = os.path.join(self.folder_path, file_name)
                self.segment_image(image_path)

    def segment_image(self, image_path):
        image = Image.open(image_path).convert('RGB')  # Ensure image is RGB
        image_np = np.array(image)

        # Print the original image shape for debugging
        print("Original image shape:", image_np.shape)

        # Resize the image for SAM
        transformer = ResizeLongestSide(self.target_length)
        image_np_resized = transformer.apply_image(image_np)

        # Print the shape of the resized image for debugging
        print("Resized image shape:", image_np_resized.shape)

        # Check if the resized image has 3 dimensions
        if len(image_np_resized.shape) == 3:
            image_tensor = torch.as_tensor(image_np_resized).permute(2, 0, 1).unsqueeze(0).float().to(self.device)

            # Predict the mask
            self.predictor.set_image(image_tensor)
            masks, scores, _ = self.predictor.predict(boxes=None, masks=None)

            # Process the masks
            annotated_image = self.apply_masks_to_image(image_np_resized, masks)
            
            # Display the annotated image
            self.display_image(Image.fromarray(annotated_image))
        else:
            messagebox.showerror("Erreur", "L'image doit avoir 3 dimensions après le redimensionnement.")

    def apply_masks_to_image(self, image, masks):
        annotated_image = image.copy()
        for mask in masks:
            color = np.random.randint(0, 255, size=(3,), dtype=np.uint8)
            annotated_image[mask] = annotated_image[mask] * 0.5 + color * 0.5
        return annotated_image

    def clickPromptSeg(self):
        # Implement prompt-based segmentation
        pass

def download_model(model_type):
    # Function to download the model if not available
    # This function needs to be implemented based on how the models are being downloaded and stored.
    # For now, it's a placeholder.
    print(f"Downloading model {model_type}...")

if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()

# -*- coding: utf-8 -*-
"""
Created on Thu Apr 10 11:00:16 2025

@author: User
"""
from pathlib import Path
import torch
import numpy as np
import json
import matplotlib.pyplot as plt

from cnn_backend import InferenceEngine
from cnn_backend.utils import CNNRequest

class ImageGenerator:
    def __init__(self):
        # Initialiser l'engine
        self.engine = InferenceEngine()
        
        # Définir le chemin du JSON (basé sur l'emplacement actuel du fichier)
        self.json_path = Path(__file__).parent / ".." / "interface_graphique" / "filtres.json"
        self.filters_dict = self.load_filters()

        # Dossier de sortie
        self.output_dir = Path(__file__).parent / ".." / "generate_images"
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Nombre d'images à générer
        self.n_images = 6

    def load_filters(self):
        with open(self.json_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def generate_all(self):
        for i in range(self.n_images):
            latent_tensor = torch.randn((1, 128), device=self.engine.device)

            request = CNNRequest(  # ici tu peux aussi injecter `self.filters_dict` si nécessaire
                Hair_Color='Black',
                Sideburns="No",
                Bangs="Yes",
                No_Beard="Yes",
                Wearing_Necktie="No",
                Big_Lips="Unknown",
                Wearing_Lipstick="Yes",
                Straight_Hair="No",
                Chubby="No",
                Big_Nose="No",
                Pointy_Nose="Yes", 
                Goatee="No",
                Male="No", 
                Receding_Hairline="No", 
                Wearing_Necklace="Unknown", 
                Eyeglasses="Yes", 
                Wavy_Hair="Yes", 
                Wearing_Earrings="Yes", 
                Young="Yes"
            )

            image_tensor = self.engine.generate(latent_tensor, request)

            # Sauvegarde du tensor
            torch.save(image_tensor, self.output_dir / f"tensor_image{i}.pth")

            # Conversion en image PNG
            image_array = image_tensor.squeeze(0).permute(1, 2, 0).cpu().numpy()
            rotated_image = np.rot90(image_array, k=-1)
            plt.imsave(self.output_dir / f"image{i}.png", rotated_image)
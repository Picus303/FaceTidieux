import torch
import matplotlib.pyplot as plt
import json
#import os
import numpy as np
from pathlib import Path
import asyncio
import flet as ft

from cnn_backend import InferenceEngine
from cnn_backend.utils import CNNRequest
from interface_graphique.main import main


if __name__ == "__main__":
    
    asyncio.run(ft.app_async(target=main))

	# Initialize the Inference Engine
    engine = InferenceEngine()



    # Récupérer le chemin du fichier JSON
    chemin_fichier = Path(__file__).parent / "interface_graphique" / "filtres.json"
    # chemin_fichier = os.path.join("..", "interface_graphique", "filtres.json")
    with open(chemin_fichier, "r", encoding="utf-8") as fichier_json:
        filters_dict = json.load(fichier_json)
    print(filters_dict['filters_applied'])
    
    
    for i in range(6):
        
        # Generate a random latent tensor
        latent_tensor = torch.randn((1, 128), device=engine.device)
        
        # Build the request
        request = CNNRequest(
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

	# Generate the image
        image_tensor = engine.generate(latent_tensor, request)
        
        # Save the latent in a dictionary
        # Sauvegarder dans un fichier .npy
        torch.save(image_tensor, f"generate_images/tensor_image{i}.pth")
        
	# Convert the image tensor to numpy array
        image_array = image_tensor.squeeze(0).permute(1, 2, 0).cpu().numpy()
    
        plt.imsave(f"generate_images/image{i}.png", image_array)

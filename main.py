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
from interactions.generator_images import ImageGenerator


from algo_gene.genetic_operations import Mutations


if __name__ == "__main__":
    
    asyncio.run(ft.app_async(target=main))
    
    """
    generator = ImageGenerator()
    generator.generate_all()
    
    
    # Initialize the Inference Engine
    engine = InferenceEngine()

	# Generate a random latent tensor
    latent_tensor1 = torch.randn((1, 128), device=engine.device)
    latent_tensor2 = torch.randn((1, 128), device=engine.device)
    




	# Generate the fusion of both of these tensor :

	# Easy version (mean) :
	#latent_tensor_fused = (latent_tensor1 + latent_tensor2) / 2

	# Ponderation version :
	#alpha = 0.8
	#latent_tensor_fused = alpha * latent_tensor1 + (1 - alpha) * latent_tensor2


	# Equilibrated version :
	#lv1 = (latent_tensor1 - latent_tensor1.mean()) / latent_tensor1.std()
	#lv2 = (latent_tensor2 - latent_tensor2.mean()) / latent_tensor2.std()
	#latent_tensor_fused = (lv1 + lv2) / 2

	# Test integrating the class Mutations (that get in input a vector containing one or more latent vector and return them modified)
	# You can choose to comment the append in order to check if everything works for 0, 1 or 2 latent vectors
    list_of_latent_vectors = []
    list_of_latent_vectors.append(latent_tensor1)
    list_of_latent_vectors.append(latent_tensor2)

    test_unitary4 = Mutations(list_of_latent_vectors, number_of_new=6)
    list_fused_latent_vectors = test_unitary4.fusion()



	# Build the request
    request = CNNRequest(
		Hair_Color="Black",
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
		Eyeglasses="No",
		Wavy_Hair="Yes",
		Wearing_Earrings="Yes",
		Young="Yes"
	)

    stored_image_array = []
	# Generate the image n°1
    image_tensor1 = engine.generate(latent_tensor1, request)
	# Convert the image tensor to numpy array
    stored_image_array1 = image_tensor1.squeeze(0).permute(1, 2, 0).cpu().numpy()

	# Generate the image n°2
    image_tensor2 = engine.generate(latent_tensor2, request)
    stored_image_array2 = image_tensor2.squeeze(0).permute(1, 2, 0).cpu().numpy()

	# Checking that there is at least one fused latent vector
    if len(list_fused_latent_vectors) == 0:
        print(" Something is wrong :(")
        exit()

	# Generate the fused image
    image_tensor_fused = engine.generate(list_fused_latent_vectors[0], request) # this is for the first fused vector
    print(list_fused_latent_vectors[0])
    fused_image_array = image_tensor_fused.squeeze(0).permute(1, 2, 0).cpu().numpy()
    print(image_tensor_fused)

    stored_image_array.append(stored_image_array1)
    stored_image_array.append(stored_image_array2)
    stored_image_array.append(fused_image_array)
    
    print("ok")

	# Display both pictures and the fusion of the two :
    #fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(10, 3))

    for i in range(len(stored_image_array)):
        print(f"showing picture coming from {i}")
        rotated_image = np.rot90(stored_image_array[i], k=-1)
        plt.imsave(f"fusion_image{i}.png", rotated_image)
        #axes[i].imshow(stored_image_array[i])
        #axes[i].axis('off')
        #plt.show()
           
    with open("images_selected.json", "r", encoding="utf-8") as fichier_json:
        selected_images_dict = json.load(fichier_json)
    list_selected_tensor = []
    print("ok")
    for i in selected_images_dict["selected_image"]:
        image_number = i[5]
        selected_tensor = torch.load(f"generate_images/latent{image_number}.pth")
        list_selected_tensor.append(selected_tensor)
    test_unitary4 = Mutations(list_selected_tensor, number_of_new=6)
    list_fused_latent_vectors = test_unitary4.fusion()
    print(list_fused_latent_vectors)
    gen = ImageGenerator()
    gen.generate_all(latent_tensors=list_fused_latent_vectors)
        

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
        rotated_image_array = np.rot90(image_array, k=-1)
    
        plt.imsave(f"generate_images/image{i}.png", rotated_image_array)"""

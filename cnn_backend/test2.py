import torch
import matplotlib.pyplot as plt

from . import InferenceEngine
from .utils import CNNRequest


if __name__ == "__main__":

	# Initialize the Inference Engine
	engine = InferenceEngine()

	# Generate a random latent tensor
	latent_tensor1 = torch.randn((1, 128), device=engine.device)
	latent_tensor2 = torch.randn((1, 128), device=engine.device)

	# Generate the fusion of both of these tensor :

	# Easy version (mean) :
	#latent_tensor_fused = (latent_tensor1 + latent_tensor2) / 2

	# Ponderation version :
	alpha = 0.8
	latent_tensor_fused = alpha * latent_tensor1 + (1 - alpha) * latent_tensor2


	# Equilibrated version :
	#lv1 = (latent_tensor1 - latent_tensor1.mean()) / latent_tensor1.std()
	#lv2 = (latent_tensor2 - latent_tensor2.mean()) / latent_tensor2.std()
	#latent_tensor_fused = (lv1 + lv2) / 2



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
	# Convert the image tensor to numpy array
	stored_image_array2 = image_tensor2.squeeze(0).permute(1, 2, 0).cpu().numpy()

	# Generate the fused image
	image_tensor_fused = engine.generate(latent_tensor_fused, request)
	# Convert the image tensor to numpy array
	fused_image_array = image_tensor_fused.squeeze(0).permute(1, 2, 0).cpu().numpy()

	stored_image_array.append(stored_image_array1)
	stored_image_array.append(stored_image_array2)
	#stored_image_array.append(stored_image_array1)
	stored_image_array.append(fused_image_array)

	"""
	# Display the image
	plt.imshow(image_array)
	plt.axis("off")
	plt.show()
	"""

	# Display both pictures and the fusion of the two :
	fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(10, 3))

	for i in range(len(stored_image_array)):
		print(f"showing picture coming from {i}")
		axes[i].imshow(stored_image_array[i])
		axes[i].axis('off')
	plt.show()
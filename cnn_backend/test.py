import torch
import matplotlib.pyplot as plt

from . import InferenceEngine
from .utils import CNNRequest


if __name__ == "__main__":

	# Initialize the Inference Engine
	engine = InferenceEngine()

	# Generate a random latent tensor
	latent_tensor = torch.randn((1, 128), device=engine.device)

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

	# Generate the image
	image_tensor = engine.generate(latent_tensor, request)
	# Convert the image tensor to numpy array
	image_array = image_tensor.squeeze(0).permute(1, 2, 0).cpu().numpy()

	# Encode the generated image
	encoded_image = engine.encode(image_tensor, request)
	print(f"Encoded Image Shape: {encoded_image.shape}")

	# Display the image
	plt.imshow(image_array)
	plt.axis("off")
	plt.show()
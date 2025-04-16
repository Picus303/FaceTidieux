from .utils import CNNRequest
from .model import CVAEGenerator

from pathlib import Path
module_path = Path(__file__).parent.resolve()

import torch
from torch import Tensor

import pickle
from typing import List

MIN_FEATURE_INDEX = 0
MAX_FEATURE_INDEX = 57

FEATURE_COUNT = 19

MAX_LATENT_ESTIMATORS = 16


class InferenceEngine:
	"""
	A class to handle inference operations for the autoencoder model.
	"""
	def __init__(self) -> None:
		"""
		Initializes the InferenceEngine by setting up the device, loading the model,
		feature map, latent dictionary, and performing a model warm-up.
		"""
		self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

		# Load the Model
		self.model = CVAEGenerator().to(self.device)
		self.model.load_state_dict(torch.load(Path(module_path, "weights.pt"), map_location=self.device, weights_only=True))

		# Load the Feature Map
		with open(Path(module_path, "feature_map.pkl"), "rb") as file:
			self.feature_map = pickle.load(file)

		# Load the Latent Dictionary
		with open(Path(module_path, "latents_dict.pkl"), "rb") as file:
			self.latents_dict = pickle.load(file)

		# Model Warm-Up
		latent_tensor = torch.randn((1, 128), device=self.device)
		label_tensor = torch.randint(MIN_FEATURE_INDEX, MAX_FEATURE_INDEX+1, (1, FEATURE_COUNT), dtype=torch.int32, device=self.device)
		_ = self.model.decode(latent_tensor, label_tensor)


	def build_feature_tensor(self, request: CNNRequest) -> Tensor:
		"""
		Builds a feature tensor from the given request.

		Args:
			request (CNNRequest): A list of feature name-value pairs.

		Returns:
			Tensor: A tensor representing the features.
		"""
		# Build the Feature Tensor
		feature_tensor = torch.empty((1, FEATURE_COUNT), dtype=torch.int32, device=self.device)
		for i, feature in enumerate(request):
			name, value = feature
			feature_tensor[0, i] = self.feature_map[(name, value)]

		return feature_tensor


	def generate(self, latent_tensor: Tensor, request: CNNRequest) -> Tensor:
		"""
		Generates an image based on the given latent tensor and feature request.

		Args:
			latent_tensor (Tensor): The latent tensor for image generation.
			request (CNNRequest): A list of feature name-value pairs.

		Returns:
			Tensor: The generated image tensor.
		"""
		# Prepare the input tensors
		latent_tensor = latent_tensor.to(self.device)
		feature_tensor = self.build_feature_tensor(request)

		with torch.no_grad():
			self.model.eval()
			image = self.model.decode(latent_tensor, feature_tensor)

		return image


	def generate_latent(self, n_images: int, request: CNNRequest) -> List[Tensor]:
		"""
		Generates latent tensors based on the given feature request.

		Args:
			n_images (int): The number of latent tensors to generate.
			request (CNNRequest): A list of feature name-value pairs.

		Returns:
			List[Tensor]: A list of generated latent tensors.
		"""
		# Build the Feature Tensor -> Tuple
		feature_tensor = self.build_feature_tensor(request)
		feature_tuple = tuple(feature_tensor[0].tolist())

		# Compare the similarity with the references
		similarities = {}
		for ref in self.latents_dict.keys():
			# We take the two tuples and count the number of similar features
			similarities[ref] = sum(1 for i in range(FEATURE_COUNT) if feature_tuple[i] == ref[i])

		# Sort the similarities and pick the ones with the highest scores
		sorted_similarities = sorted(similarities.items(), key=lambda item: item[1], reverse=True)
		top_similarities = sorted_similarities[:MAX_LATENT_ESTIMATORS]
		top_similarity = top_similarities[0][1]

		mu_var_tensors = []
		for ref, score in top_similarities:
			if score == top_similarity:
				mu_var_tensors.append(self.latents_dict[ref])

		# Compute the average mu and logvar
		mus = [torch.tensor(pair[0]) for pair in mu_var_tensors]
		logvars = [torch.tensor(pair[1]) for pair in mu_var_tensors]

		mu = torch.mean(torch.stack(mus), dim=0)
		logvar = torch.mean(torch.stack(logvars), dim=0)

		# Generate the latent tensors
		latent_tensors = []
		for i in range(n_images):
			z = self.model.reparameterize(mu, logvar)
			latent_tensors.append(z)

		return latent_tensors
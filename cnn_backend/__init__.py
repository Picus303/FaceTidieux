from .utils import CNNRequest
from .model import CVAEGenerator

from pathlib import Path
module_path = Path(__file__).parent.resolve()

import torch
from torch import Tensor

import pickle

MIN_FEATURE_INDEX = 0
MAX_FEATURE_INDEX = 57

FEATURE_COUNT = 19


class InferenceEngine:
	def __init__(self) -> None:
		self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

		# Load the Model
		self.model = CVAEGenerator().to(self.device)
		self.model.load_state_dict(torch.load(Path(module_path, "weights.pt"), map_location=self.device, weights_only=True))

		# Load the Feature Map
		with open(Path(module_path, "feature_map.pkl"), "rb") as file:
			self.feature_map = pickle.load(file)

		# Model Warm-Up
		latent_tensor = torch.randn((1, 128), device=self.device)
		label_tensor = torch.randint(MIN_FEATURE_INDEX, MAX_FEATURE_INDEX+1, (1, FEATURE_COUNT), dtype=torch.int32, device=self.device)
		_ = self.model.decode(latent_tensor, label_tensor)


	def generate(self, latent_tensor: Tensor, request: CNNRequest) -> Tensor:
		# Build the Feature Tensor
		feature_tensor = torch.empty((1, FEATURE_COUNT), dtype=torch.int32, device=self.device)
		for i, feature in enumerate(request):
			name, value = feature
			feature_tensor[0, i] = self.feature_map[(name, value)]

		with torch.no_grad():
			image = self.model.decode(latent_tensor, feature_tensor)

		return image
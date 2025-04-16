# -*- coding: utf-8 -*-
"""
Created on Sat Apr 12 16:24:46 2025

@author: User
"""
import json
import torch
from pathlib import Path

from algo_gene.genetic_operations import Mutations
from interactions.generator_images import ImageGenerator


class LatentFusionPipeline:
    def __init__(self, json_path="images_selected.json", latents_dir="generate_images", n_outputs=6):
        """

        Parameters
        ----------
        json_path : string, optional
            Path where the file json with the selected images is located. The default is "images_selected.json".
        latents_dir : string, optional
            Directory where the latent vectors are located. The default is "generate_images".
        n_outputs : integer, optional
            number of images we need to create. The default is 6.

        Returns
        -------
        None.

        """
        
        self.json_path = Path(json_path)
        self.latents_dir = Path(latents_dir)
        self.n_outputs = n_outputs
        self.selected_tensors = []

    def load_selected_latents(self):
        """
        
        Load the latents of the selected images
        
        Returns
        -------
        None.

        """
        
        with open(self.json_path, "r", encoding="utf-8") as fichier_json:
            selected_images_dict = json.load(fichier_json)

        for image_name in selected_images_dict["selected_image"]:
            image_number = image_name[5]  # Search the number of the latent that correspond to the selected image
            tensor_path = self.latents_dir / f"latent{image_number}.pth"
            tensor = torch.load(tensor_path)
            self.selected_tensors.append(tensor)

    def fuse_latents(self):
        """
        Fuse the selected latents to create merged latents

        Returns
        -------
        None.

        """

        self.mutator = Mutations(self.selected_tensors, number_of_new=self.n_outputs)
        self.fused_latents = self.mutator.fusion()

    def generate_images(self):
        """
        Generate new images with the merged latents

        Returns
        -------
        None.

        """
        
        generator = ImageGenerator()
        generator.generate_all(latent_tensors=self.fused_latents)

    def run(self):
        """
        
        Run the algorithm

        Returns
        -------
        None.

        """
        
        self.load_selected_latents()

        self.fuse_latents()

        self.generate_images()

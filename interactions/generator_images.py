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
        
        # Fichier de version
        self.version_file = self.output_dir / "version.txt"
        self.version = self._load_and_increment_version()
        self._clean_previous_images()

        # Nombre d'images à générer
        self.n_images = 6
    
    def _load_and_increment_version(self):
        """
         Increment the version by 1 and save it in a file

        Returns
        -------
        version : integer
            Numero of version.

        """
        if self.version_file.exists():
            with open(self.version_file, "r") as f:
                version = int(f.read().strip())
        else:
            version = 0  # première exécution
            
         # Sauvegarde de la nouvelle version
        with open(self.version_file, "w") as f:
            f.write(str(version + 1))
            
        return version
    
    def _clean_previous_images(self):
        """
        Eliminate the previous images

        Returns
        -------
        TYPE
            DESCRIPTION.

        """
        
        previous_version = self.version - 1
        if previous_version < 0:
            return  # Aucune image précédente à supprimer

        pattern = f"image*_{previous_version}.png"
        for file_path in self.output_dir.glob(pattern):
            try:
                file_path.unlink()
                print(f"[INFO] Image supprimée : {file_path.name}")
            except Exception as e:
                print(f"[ERREUR] Impossible de supprimer {file_path.name} : {e}")

    def load_filters(self):
        """
        
        Load the filters chosen by the user

        Returns
        -------
        Dictionary
            Dictionary with filters chosen.

        """
        
        with open(self.json_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def generate_all(self, latent_tensors=None, first_run=False):
        """
        
        Generates 6 new images based on latents and save them

        Parameters
        ----------
        latent_tensors : , tensors, optional
            Latent tensors that will create the new images. The default is None.

        Returns
        -------
        None.

        """

        with open(self.json_path, "r", encoding="utf-8") as f:
            filters_dict = json.load(f)

        # Générer la requête à l'auto-encodeur
        request = CNNRequest(
            Hair_Color=filters_dict['Hair_Color'],
            Sideburns=filters_dict['Sideburns'],
            Bangs=filters_dict['Bangs'],
            No_Beard=filters_dict['No_Beard'],
            Wearing_Necktie=filters_dict['Wearing_Necktie'],
            Big_Lips=filters_dict['Big_Lips'],
            Wearing_Lipstick=filters_dict['Wearing_Lipstick'],
            Straight_Hair=filters_dict['Straight_Hair'],
            Chubby=filters_dict['Chubby'],
            Big_Nose=filters_dict['Big_Nose'],
            Pointy_Nose=filters_dict['Pointy_Nose'], 
            Goatee=filters_dict['Goatee'],
            Male=filters_dict['Male'], 
            Receding_Hairline=filters_dict['Receding_Hairline'], 
            Wearing_Necklace=filters_dict['Wearing_Necklace'], 
            Eyeglasses=filters_dict['Eyeglasses'], 
            Wavy_Hair=filters_dict['Wavy_Hair'], 
            Wearing_Earrings=filters_dict['Wearing_Earrings'], 
            Young=filters_dict['Young']
        )

        # Si c'est la première exécution, on laisse l'engine générer des latents
        if first_run:
            latent_tensors = self.engine.generate_latent(self.n_images, request)

        for i in range(self.n_images):
            # Soit on prend un latent donné, soit on le génère
            if latent_tensors is not None and i < len(latent_tensors):
                latent_tensor = latent_tensors[i].to(self.engine.device)
            else:
                # Sécurité: on est pas censé arriver ici
                latent_tensor = torch.randn((1, 128), device=self.engine.device)

            # Sauvegarde du vecteur latent
            torch.save(latent_tensor, self.output_dir / f"latent{i}.pth")

            image_tensor = self.engine.generate(latent_tensor, request)

            # Conversion en image PNG
            image_array = image_tensor.squeeze(0).permute(1, 2, 0).cpu().numpy()
            rotated_image = np.rot90(image_array, k=-1)
            plt.imsave(self.output_dir / f"image{i}_{self.version}.png", rotated_image)
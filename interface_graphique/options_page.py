
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 12 10:27:03 2025

@author: ouijdanejerid
"""

import flet as ft 
import json
import os 
from .selection_page import *
import time
from interactions.generator_fusion_images import LatentFusionPipeline

def selected_result_view(page: ft.Page):
    font_family = "Times New Roman"

    # Lire les images sélectionnées
    try:
        with open("images_selected.json", "r", encoding="utf-8") as fichier:
            data = json.load(fichier)
            selected_images = data.get("selected_image", [])
    except FileNotFoundError:
        selected_images = []

    # Affichage des images sélectionnées
    image_row = ft.Row(
        [
            ft.Image(
                src=os.path.join(IMAGE_DIR, img),
                width=150,
                height=150,
                fit=ft.ImageFit.COVER
            ) for img in selected_images
        ],
        wrap=True,
        alignment="center",
        spacing=10
    )

    mutated_images_container = ft.Column(spacing=10)

    # Ce bouton "Continue" ne s'affichera qu'après mutation
    continue_button = ft.ElevatedButton(
        text="Continue",
        visible=False,
        on_click=lambda e: page.go("/select")
    )
    
    def regenerate_images():
        pipeline = LatentFusionPipeline(n_outputs=6)
        pipeline.run() 
        
        

    def on_mutate(e):
            regenerate_images()
            page.go("/mutate")
            
    action_buttons = ft.Column(
            [
                ft.Container(
                    content=ft.TextButton(
                        "Mutate",
                        on_click=on_mutate,
                        style=ft.ButtonStyle(
                            padding=20,
                            bgcolor="#4CAF50",
                            color="white",
                            shape=ft.RoundedRectangleBorder(radius=12),
                            text_style=ft.TextStyle(size=18, weight=ft.FontWeight.BOLD)
                        )
                    ),
                    alignment=ft.alignment.center,
                    width=300
                ),
                ft.FilledButton("Go Back", on_click=lambda e: page.go("/select"))
            ],
            spacing=25,
            alignment="center"
        )

    layout = ft.Column(
        [
            ft.Container(
                ft.Text(
                    "Choose an option for your selected portraits",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                    font_family=font_family
                ),
                alignment=ft.alignment.center,
                padding=20
            ),
            image_row,
            ft.Container(action_buttons, alignment=ft.alignment.center, padding=20),
            mutated_images_container
        ],
        horizontal_alignment="center",
        spacing=30
    )

    return ft.View(route="/selected", controls=[layout], scroll="auto", bgcolor="white")

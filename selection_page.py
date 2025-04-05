#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 26 10:56:26 2025

@author: ouijdanejerid
"""

import flet as ft

import flet as ft
import os
import random

IMAGE_DIR = "images"  # Dossier local contenant les portraits (format PNG ou JPG)

# Fonction pour récupérer 6 images aléatoires
def get_random_images():
    all_images = [f for f in os.listdir(IMAGE_DIR) if f.endswith((".png", ".jpg", ".jpeg"))]
    return random.sample(all_images, k=6) if len(all_images) >= 6 else all_images

def select_portraits_view(page: ft.Page):
    font_family = "Times New Roman"

    # État dynamique des images à afficher
    image_container = ft.Row(wrap=True, alignment="center", spacing=10)

    def load_images():
        image_container.controls.clear()
        for img_name in get_random_images():
            img_path = os.path.join(IMAGE_DIR, img_name)
            image = ft.Image(src=img_path, width=150, height=150, fit=ft.ImageFit.COVER)
            image_container.controls.append(image)
        page.update()

    def other_images(e):
        load_images()

    # Titres et boutons
    title = ft.Text("Select one or more Portraits", size=26, weight=ft.FontWeight.BOLD, font_family=font_family)

    button_row = ft.Row([
        ft.FilledButton("Go Back", on_click=lambda e:page.go("/filters")),
        ft.FilledButton("Other", on_click=other_images)

    ], alignment="center", spacing=20)

    # Page structure
    layout = ft.Column([
        ft.Container(title, alignment=ft.alignment.center, padding=20),
        image_container,
        ft.Container(button_row, alignment=ft.alignment.center, padding=20)
    ], horizontal_alignment="center", spacing=20)

    # Initialisation
    load_images()

    return ft.View(route="/select", controls=[layout], scroll="auto",bgcolor="white")

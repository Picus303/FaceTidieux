#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 26 10:56:26 2025

@author: ouijdanejerid
"""

import flet as ft
import os
import random
import json

IMAGE_DIR = "interface_graphique/images"  # Dossier local contenant les portraits (PNG, JPG, JPEG)

def get_random_images():
    """Récupère 6 images aléatoires (ou moins si le dossier n'en contient pas assez)."""
    all_images = [f for f in os.listdir(IMAGE_DIR) if f.lower().endswith((".png", ".jpg", ".jpeg"))]
    return random.sample(all_images, k=6) if len(all_images) >= 6 else all_images

def select_portraits_view(page: ft.Page):
    font_family = "Times New Roman"

    # Liste qui contiendra des dictionnaires pour chaque image affichée
    # avec le nom, le contrôle image et l'état "selected"
    displayed_images = []

    # Conteneur des images (chaque image sera affichée via un GestureDetector)
    image_container = ft.Row(wrap=True, alignment="center", spacing=10)

    def toggle_selection(e, img_info):
        """Inverser l'état de sélection de l'image et mettre à jour l'affichage."""
        img_info["selected"] = not img_info["selected"]
        if img_info["selected"]:
            # Ajout d'une bordure bleue pour indiquer la sélection
            img_info["control"].border = ft.border.all(3, "blue")
        else:
            # Suppression de la bordure
            img_info["control"].border = None
        img_info["control"].update()

    def load_images():
        """Charge 6 images aléatoires et crée pour chacune un GestureDetector avec callback on_click."""
        image_container.controls.clear()
        displayed_images.clear()

        random_imgs = get_random_images()
        for img_name in random_imgs:
            img_path = os.path.join(IMAGE_DIR, img_name)
            # Création du contrôle image
            image_control = ft.Image(
                src=img_path,
                width=150,
                height=150,
                fit=ft.ImageFit.COVER
            )
            # On enregistre les infos de l'image dans la liste
            img_info = {"img_name": img_name, "control": image_control, "selected": False}
            displayed_images.append(img_info)

            # On encapsule l'image dans un GestureDetector pour capter le clic
            gd = ft.GestureDetector(
                content=image_control,
                on_tap=lambda e, img_info=img_info: toggle_selection(e, img_info)
            )
            image_container.controls.append(gd)
        page.update()

    def other_images(e):
        """Recharge d'autres images aléatoires."""
        load_images()

    def confirm_selected_images(e):
        """
        Parcourt la liste des images affichées et enregistre
        les noms des images sélectionnées dans un fichier JSON.
        """
        selected_images = [img_info["img_name"] for img_info in displayed_images if img_info["selected"]]
        filters_dict = {
            "filters_applied": False,  # Aucun filtre n'est appliqué, c'est une sélection manuelle
            "selected_images": selected_images
        }
        with open("filtres.json", "w", encoding="utf-8") as fichier_json:
            json.dump(filters_dict, fichier_json, ensure_ascii=False, indent=4)
        page.go("/next")

    title = ft.Text(
        "Select some Portraits by clicking on them",
        size=22,
        weight=ft.FontWeight.BOLD,
        font_family=font_family
    )

    button_row = ft.Row(
        [
            ft.FilledButton("Go Back", on_click=lambda e: page.go("/filters")),
            ft.FilledButton("Other", on_click=other_images),
            ft.FilledButton("Confirm selected images", on_click=confirm_selected_images)
        ],
        alignment="center",
        spacing=20
    )

    layout = ft.Column(
        [
            ft.Container(title, alignment=ft.alignment.center, padding=20),
            image_container,
            ft.Container(button_row, alignment=ft.alignment.center, padding=20)
        ],
        horizontal_alignment="center",
        spacing=20
    )

    load_images()
    return ft.View(route="/select", controls=[layout], scroll="auto", bgcolor="white")

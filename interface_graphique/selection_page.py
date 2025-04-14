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


chemin_relatif = f"generate_images"
chemin_absolu = os.path.abspath(chemin_relatif)
IMAGE_DIR = chemin_absolu
#IMAGE_DIR = "generate_images"  # Dossier local contenant les portraits (PNG, JPG, JPEG)




def get_random_images():
    """Récupère 6 images aléatoires (ou moins si le dossier n'en contient pas assez)."""
    all_images = [f for f in os.listdir(IMAGE_DIR) if f.lower().endswith((".png", ".jpg", ".jpeg"))]
    return random.sample(all_images, k=6) if len(all_images) >= 6 else all_images

def select_portraits_view(page: ft.Page):
    font_family = "Times New Roman"

    # Liste qui contiendra des dictionnaires pour chaque image affichée
    # avec le nom, le contrôle image et l'état "selected"
    displayed_images = []
    thumbnail_selected_images = []

    # Conteneur des images (chaque image sera affichée via un GestureDetector)
    image_container = ft.Row(wrap=True, alignment="center", spacing=10)

    def toggle_selection(e, img_info):
        img_name = img_info["img_name"]
        img_info["selected"] = not img_info["selected"]
    
        if img_info["selected"]:
            img_info["control"].border = ft.border.all(3, "blue")
            img_info["control"].scale = 0.95
    
            if img_name not in thumbnail_selected_images:
                thumbnail_selected_images.append(img_name)
                thumb = ft.Image(
                    src=os.path.join(IMAGE_DIR, img_name),
                    width=40,
                    height=40,
                    fit=ft.ImageFit.COVER,
                    key=img_name
                )
                selected_thumbnails.controls.append(thumb)
    
        else:
            img_info["control"].border = None
            img_info["control"].scale = 1
    
            if img_name in thumbnail_selected_images:
                thumbnail_selected_images.remove(img_name)
                selected_thumbnails.controls = [
                    t for t in selected_thumbnails.controls if t.key != img_name
                ]
    
        img_info["control"].update()
        page.update()
        
        img_info["control"].update()
    selected_thumbnails = ft.Column(wrap=True, spacing=5)
    thumbnail_panel = ft.Container(
        content=selected_thumbnails,
        bgcolor=ft.colors.WHITE,
        border_radius=10,
        padding=10,
        visible=False,  # caché au début
        width=200,
        height=200,
        alignment=ft.alignment.top_left,
        shadow=ft.BoxShadow(blur_radius=10, color=ft.colors.GREY),
    )
    
    toggle_button = ft.IconButton(
        icon=ft.icons.IMAGE,
        tooltip="Show selected",
        on_click=lambda e: toggle_panel()
    )
    
    def toggle_panel():
        thumbnail_panel.visible = not thumbnail_panel.visible
        page.update()
    

    def load_images():
        image_container.controls.clear()
        displayed_images.clear()
    
        random_imgs = get_random_images()
        for img_name in random_imgs:
            img_path = os.path.join(IMAGE_DIR, img_name)
    
            image_control = ft.Image(
                src=img_path,
                width=140,
                height=140,
                fit=ft.ImageFit.COVER
            )
    
            container = ft.Container(
                content=image_control,
                width=150,
                height=150,
                padding=5,
                alignment=ft.alignment.center,
                border_radius=8,
                animate=ft.Animation(200, "easeInOut"),
                scale=1,
            )
    
            img_info = {"img_name": img_name, "control": container, "selected": False}
            displayed_images.append(img_info)
    
            gd = ft.GestureDetector(
                content=container,
                on_tap=lambda e, img_info=img_info: toggle_selection(e, img_info)
            )
            image_container.controls.append(gd)
    
        page.update()

    def other_images(e):
        """Recharge d'autres images aléatoires."""
        load_images()

    def confirm_selected_images(e):
        if not thumbnail_selected_images:
            page.snack_bar = ft.SnackBar(ft.Text("No image selected."))
            page.snack_bar.open = True
            page.update()
            return
    
        with open("images_selected.json", "w", encoding="utf-8") as fichier_json:
            json.dump({"selected_image": thumbnail_selected_images}, fichier_json, ensure_ascii=False, indent=4)
    
        page.go("/selected")
            
    
    def clear_thumbnail(e):
        thumbnail_selected_images.clear()
        selected_thumbnails.controls.clear()
        page.update()
    
    
    title = ft.Text(
        "Select one ore more portraits",
        size=22,
        weight=ft.FontWeight.BOLD,
        font_family=font_family
    )
    
    
    clear_button = ft.IconButton(
    icon=ft.icons.DELETE,
    tooltip="Clear selected",
    on_click=clear_thumbnail
)

    page.overlay.append(clear_button)
    clear_button.top = 20
    clear_button.right = 60  # un peu à gauche du bouton image
        

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
    page.overlay.append(thumbnail_panel)
    page.overlay.append(toggle_button)
    
    # Pour positionner dans le coin haut droit :
    toggle_button.top = 20
    toggle_button.right = 20
    thumbnail_panel.top = 60
    thumbnail_panel.right = 20
    
    return ft.View(route="/select", controls=[layout], scroll="auto", bgcolor="white")

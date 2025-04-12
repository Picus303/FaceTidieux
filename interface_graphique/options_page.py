#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 12 10:27:03 2025

@author: ouijdanejerid
"""

import flet as ft 
import json
import os 
from .selection_page import *

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

    title = ft.Text(
        "Choose an option for your selected portraits",
        size=24,
        weight=ft.FontWeight.BOLD,
        font_family=font_family
    )

    # Action merge
    def merge_portraits(e):
        # À remplacer par ta vraie logique de fusion
        print("Fusion des portraits...")
        page.snack_bar = ft.SnackBar(ft.Text("Merging portraits... (to implement)"))
        page.snack_bar.open = True
        page.update()

    # Action mutate
    def mutate_portraits(e):
        # À remplacer par ta vraie logique de mutation
        print("Mutation des portraits...")
        page.snack_bar = ft.SnackBar(ft.Text("Mutating portraits... (to implement)"))
        page.snack_bar.open = True
        page.update()

    action_buttons = ft.Column(
    [
        ft.Container(
            content=ft.TextButton(
                "Merge portraits",
                on_click=merge_portraits,
                style=ft.ButtonStyle(
                    padding=20,
                    bgcolor="#1C8EBB",
                    color="white",
                    shape=ft.RoundedRectangleBorder(radius=12),
                    text_style=ft.TextStyle(size=18, weight=ft.FontWeight.BOLD)
                )
            ),
            alignment=ft.alignment.center,
            width=300
        ),
        ft.Container(
            content=ft.TextButton(
                "Mutate portraits",
                on_click=mutate_portraits,
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
            ft.Container(title, alignment=ft.alignment.center, padding=20),
            image_row,
            ft.Container(action_buttons, alignment=ft.alignment.center, padding=20)
        ],
        horizontal_alignment="center",
        spacing=30
    )

    return ft.View(route="/selected", controls=[layout], scroll="auto", bgcolor="white")
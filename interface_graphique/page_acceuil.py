import flet as ft
import asyncio
import os

from PIL import Image
from .tuto_page import *

def accueil_view(page):
    page.title = "FaceGen"
    page.bgcolor = "white"
    page.padding = 15
    page.scroll = "auto"

    # Police personnalisée
    font_family = "Times New Roman"

    # TOP BAR avec boutons gauche/droite
  #  ft.TextButton(content=ft.Text("Commencer - Présentation", font_family="Times New Roman", size=14), on_click=lambda e: print("Présentation")),
  # TOP BAR
    top_bar = ft.Row([
        ft.TextButton(
            content=ft.Text("Tutorial", font_family=font_family, size=14, weight=ft.FontWeight.BOLD),
            on_click=open_tutorial
        )
    ], alignment="end")

    # ft.TextButton(content=ft.Text("Tutorial",font_family="Times New Roman",size=16, weight=ft.FontWeight.BOLD, decoration=ft.TextDecoration.UNDERLINE
    #     ),
    #     on_click=lambda e: ft.app_async(target=tuto_page.tutorial_window)
    #  ) ], alignment="start")

    # TITRE et SOUS-TITRE
    title = ft.Text("Welcome to FaceGen !", size=30, weight=ft.FontWeight.BOLD, text_align="center", color="black", font_family=font_family)
    subtitle = ft.Text("An interactive tool to explore, combine and evolve human faces", size=16, text_align="center", color="black", font_family=font_family)

    # DESCRIPTION
    description = ft.Column([
    ft.Text("• Select one or more base portraits to begin.", italic=True, color="black", font_family="Times New Roman", size=15),
    ft.Text("• Optionally apply filters to refine the selection.", italic=True, color="black", font_family="Times New Roman", size=15),
    ft.Text("• With a single portrait, generate multiple variations.", italic=True, color="black", font_family="Times New Roman", size=15),
    ft.Text("• With multiple portraits, combine them to evolve new faces.", italic=True, color="black", font_family="Times New Roman", size=15),
], spacing=5, alignment="start")


    # BOUTON stylé
    start_btn = ft.ElevatedButton(
    content=ft.Text("Start →", font_family="Times New Roman", size=16, weight=ft.FontWeight.BOLD),
    style=ft.ButtonStyle(
        shape=ft.RoundedRectangleBorder(radius=30),
        padding=20,
        bgcolor="white",
        side=ft.BorderSide(2, "black"),
        color="black",
    ),
    on_click=lambda e: page.go("/filters")
)

    # IMAGES superposées
    
    # Récupération des chemins absolus pour accéder aux images 
    liste_chemins_absolus = []
    for i in range(3):
        chemin_relatif = f"interface_graphique/im{i+1}.png"
        chemin_absolu = os.path.abspath(chemin_relatif)
        liste_chemins_absolus.append(chemin_absolu)
    print(liste_chemins_absolus)
        
    # IMAGES superposées
    img_stack = ft.Stack([
    # Image 3 : tout au fond, la plus grande
    ft.Image(src=liste_chemins_absolus[2], width=510, top=10, left=25 ,bottom = 3),


    # Image 2 : par-dessus, centrée
    ft.Image(src=liste_chemins_absolus[0], width=500, top=3, left=15,bottom = 50),

    # Image 1 : légèrement décalée
    ft.Image(src=liste_chemins_absolus[1],  width=480, top=11, left=10, bottom =0),

], width=470, height=290)

    # img_stack = ft.Stack([
    #     ft.Image(src="/Users/ouijdanejerid/Desktop/im1.png", width=430, top=0, left=30),
    #     ft.Image(src="/Users/ouijdanejerid/Desktop/im2.png", width=420, top=20, left=0),
    # ], width=430, height=230)

    # ORGANISATION horizontale : texte + images
    content = ft.Row([
        ft.Column([
            description,
            ft.Container(start_btn, padding=20)
        ], expand=1, alignment="start", spacing=30),
        img_stack
    ], alignment="center", spacing=0)

    # ASSEMBLAGE FINAL
    page.add(
    top_bar,
    ft.Container(title, alignment=ft.alignment.center, padding=0),
    ft.Container(subtitle, alignment=ft.alignment.center, padding=5),
    ft.Divider(thickness=1),
    ft.Container(content, padding=ft.padding.only(top=20)))

    return ft.View(
       route="/",
       controls=[
           top_bar,
           ft.Container(title, alignment=ft.alignment.center, padding=0),
           ft.Container(subtitle, alignment=ft.alignment.center, padding=5),
           ft.Divider(thickness=1),
           ft.Container(content, padding=ft.padding.only(top=20))
       ],
       scroll="auto",
       padding=15,
       bgcolor="white"
)
